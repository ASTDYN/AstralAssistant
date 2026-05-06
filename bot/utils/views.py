"""
All Discord UI components (Views, Modals, Selects, Buttons).

Persistent views (timeout=None, registered in setup_hook) use fixed custom_ids
so they survive bot restarts. They identify the acting user via interaction.user.id.

Non-persistent views (ProfileDetailsView, AdmittanceView) use timeout-based cleanup
since they expect prompt interaction.
"""

from __future__ import annotations

import secrets
import string
from typing import TYPE_CHECKING

import discord
from discord import ui

from bot.config import GAMEPLAY_STYLES, LOBBY_CHANNEL_ID, RECRUITMENT_CHANNEL_ID, ROLE_NAMES, TIMEZONES

if TYPE_CHECKING:
    from bot.main import AstralBot


# ─── Helpers ─────────────────────────────────────────────────────────────────


def generate_code() -> str:
    alphabet = string.ascii_uppercase + string.digits
    return "".join(secrets.choice(alphabet) for _ in range(10))


async def assign_role(
    bot: AstralBot,
    guild: discord.Guild,
    member: discord.Member,
    role_key: str,
    reason: str = "",
) -> bool:
    role_record = await bot.db.get_role(guild.id, ROLE_NAMES[role_key])
    if not role_record:
        return False
    role = guild.get_role(role_record.role_id)
    if not role:
        return False
    await member.add_roles(role, reason=reason)
    return True


# ─── Pre-compute static select options ───────────────────────────────────────

_TIMEZONE_OPTIONS = [
    discord.SelectOption(label=label, value=value) for label, value in TIMEZONES
]

_GAMEPLAY_OPTIONS = [
    discord.SelectOption(label=style, value=style) for style in GAMEPLAY_STYLES
]


# ─── Onboarding Step 1 — RSI Username Modal ──────────────────────────────────


class RSIUsernameModal(ui.Modal, title="RSI Account Verification"):
    rsi_handle = ui.TextInput(
        label="RSI Handle",
        placeholder="Your RSI handle (case-sensitive)",
        min_length=2,
        max_length=64,
    )

    def __init__(self, bot: AstralBot, member_id: int, guild_id: int) -> None:
        super().__init__()
        self.bot = bot
        self.member_id = member_id
        self.guild_id = guild_id

    async def on_submit(self, interaction: discord.Interaction) -> None:
        handle = self.rsi_handle.value.strip()
        await self.bot.db.upsert_member(self.member_id, rsi_username=handle)
        view = ProfileDetailsView(self.bot, self.member_id, self.guild_id)
        await interaction.response.send_message(
            "**Step 2 of 3 — Profile Details**\n"
            "Please select your timezone, gameplay style, and recruiter (if applicable), "
            "then click **Continue**.",
            view=view,
        )


# ─── Onboarding Step 1 — Start View (persistent) ─────────────────────────────


class StartOnboardingView(ui.View):
    """Persistent view sent via DM on member join. Identified by interaction.user.id."""

    def __init__(self, bot: AstralBot) -> None:
        super().__init__(timeout=None)
        self.bot = bot

    @ui.button(
        label="Begin Verification",
        style=discord.ButtonStyle.green,
        emoji="✅",
        custom_id="persist:onboard_begin",
    )
    async def begin(self, interaction: discord.Interaction, button: ui.Button) -> None:
        member_record = await self.bot.db.get_member(interaction.user.id)
        if not member_record or not member_record.guild_id:
            await interaction.response.send_message(
                "Onboarding record not found. Please ask an admin to re-send your welcome message.",
                ephemeral=True,
            )
            return
        modal = RSIUsernameModal(self.bot, interaction.user.id, member_record.guild_id)
        await interaction.response.send_modal(modal)

    @ui.button(
        label="Skip Verification",
        style=discord.ButtonStyle.secondary,
        emoji="⏭️",
        custom_id="persist:onboard_skip",
    )
    async def skip(self, interaction: discord.Interaction, button: ui.Button) -> None:
        member_record = await self.bot.db.get_member(interaction.user.id)
        guild = self.bot.get_guild(member_record.guild_id) if member_record else None
        member = guild.get_member(interaction.user.id) if guild else None

        if member and guild:
            await assign_role(
                self.bot, guild, member, "unverified", reason="Skipped verification"
            )

        for child in self.children:
            child.disabled = True  # type: ignore[union-attr]
        await interaction.response.edit_message(
            content=(
                "You have been assigned the **SC-Unverified** role.\n"
                "You can complete verification at any time using `/verify`."
            ),
            view=self,
        )


# ─── Onboarding Step 2 — Profile Details (non-persistent) ────────────────────


class ProfileDetailsView(ui.View):
    def __init__(self, bot: AstralBot, member_id: int, guild_id: int) -> None:
        super().__init__(timeout=300)
        self.bot = bot
        self.member_id = member_id
        self.guild_id = guild_id
        self.timezone: str | None = None
        self.gameplay_style: str | None = None
        self.recruiter_id: int | None = None

    @ui.select(
        placeholder="🌍  Select your Timezone",
        options=_TIMEZONE_OPTIONS,
        row=0,
    )
    async def timezone_select(
        self, interaction: discord.Interaction, select: ui.Select
    ) -> None:
        if interaction.user.id != self.member_id:
            await interaction.response.send_message(
                "This form belongs to another user.", ephemeral=True
            )
            return
        self.timezone = select.values[0]
        await interaction.response.defer()

    @ui.select(
        placeholder="⚔️  Select your Gameplay Style",
        options=_GAMEPLAY_OPTIONS,
        row=1,
    )
    async def gameplay_select(
        self, interaction: discord.Interaction, select: ui.Select
    ) -> None:
        if interaction.user.id != self.member_id:
            await interaction.response.send_message(
                "This form belongs to another user.", ephemeral=True
            )
            return
        self.gameplay_style = select.values[0]
        await interaction.response.defer()

    @ui.user_select(
        placeholder="👤  Select your Recruiter (Optional)",
        min_values=0,
        max_values=1,
        row=2,
    )
    async def recruiter_select(
        self, interaction: discord.Interaction, select: ui.UserSelect
    ) -> None:
        if interaction.user.id != self.member_id:
            await interaction.response.send_message(
                "This form belongs to another user.", ephemeral=True
            )
            return
        self.recruiter_id = select.values[0].id if select.values else None
        await interaction.response.defer()

    @ui.button(label="Continue ➜", style=discord.ButtonStyle.green, row=3)
    async def continue_btn(
        self, interaction: discord.Interaction, button: ui.Button
    ) -> None:
        if interaction.user.id != self.member_id:
            await interaction.response.send_message(
                "This form belongs to another user.", ephemeral=True
            )
            return
        if not self.timezone or not self.gameplay_style:
            await interaction.response.send_message(
                "Please select your **Timezone** and **Gameplay Style** before continuing.",
                ephemeral=True,
            )
            return

        member_record = await self.bot.db.get_member(self.member_id)
        code = (
            member_record.verification_code
            if member_record and member_record.verification_code
            else generate_code()
        )

        await self.bot.db.upsert_member(
            self.member_id,
            timezone=self.timezone,
            gameplay_style=self.gameplay_style,
            recruiter_id=self.recruiter_id,
            verification_code=code,
        )

        for child in self.children:
            child.disabled = True  # type: ignore[union-attr]
        await interaction.response.edit_message(
            content="Profile details saved! ✅", view=self
        )

        verify_view = VerificationView(self.bot)
        await interaction.followup.send(
            f"**Step 3 of 3 — RSI Verification**\n\n"
            f"Your unique verification code is:\n"
            f"```\n{code}\n```\n"
            f"**Instructions:**\n"
            f"1. Go to <https://robertsspaceindustries.com/account/profile>\n"
            f"2. Add the code anywhere in your **Biography** field and save\n"
            f"3. Click **Verify** below\n\n"
            f"You may remove the code from your bio after verification.\n"
            f"Alternatively, click **Bypass** to receive the Unverified role now.",
            view=verify_view,
        )


# ─── Onboarding Step 3 — Verification (persistent) ───────────────────────────


class VerificationView(ui.View):
    """Persistent view — lives in DMs until the user interacts."""

    def __init__(self, bot: AstralBot) -> None:
        super().__init__(timeout=None)
        self.bot = bot

    @ui.button(
        label="Verify",
        style=discord.ButtonStyle.green,
        emoji="🔍",
        custom_id="persist:verify",
    )
    async def verify(self, interaction: discord.Interaction, button: ui.Button) -> None:
        await interaction.response.defer(thinking=True)

        member_id = interaction.user.id
        member_record = await self.bot.db.get_member(member_id)

        if (
            not member_record
            or not member_record.rsi_username
            or not member_record.verification_code
        ):
            await interaction.followup.send(
                "No verification data found. Please use `/verify` to restart onboarding.",
                ephemeral=True,
            )
            return

        from bot.utils.rsi import check_verification_code

        verified = await check_verification_code(
            member_record.rsi_username, member_record.verification_code
        )

        guild = self.bot.get_guild(member_record.guild_id) if member_record.guild_id else None
        member = guild.get_member(member_id) if guild else None

        if verified:
            await self.bot.db.upsert_member(member_id, is_verified=True)
            if member and guild:
                await assign_role(
                    self.bot, guild, member, "verified", reason="RSI verification passed"
                )

            for child in self.children:
                child.disabled = True  # type: ignore[union-attr]
            await interaction.message.edit(view=self)  # type: ignore[union-attr]
            await interaction.followup.send(
                "**Verification successful!** 🎉\n"
                "You have been assigned the **SC-Verified** role. Welcome to AstralDynamics!"
            )
        else:
            if member and guild:
                await assign_role(
                    self.bot, guild, member, "unverified", reason="RSI verification failed"
                )
            await interaction.followup.send(
                "**Verification failed.**\n"
                f"The code `{member_record.verification_code}` was not found in the biography of RSI handle "
                f"`{member_record.rsi_username}`.\n\n"
                "Please make sure you:\n"
                "• Entered the correct RSI handle\n"
                "• Saved the code to your RSI profile bio\n\n"
                "Click **Verify** again once your bio is updated. "
                "You have been assigned **SC-Unverified** for now."
            )

    @ui.button(
        label="Bypass Verification",
        style=discord.ButtonStyle.secondary,
        emoji="⏭️",
        custom_id="persist:bypass",
    )
    async def bypass(self, interaction: discord.Interaction, button: ui.Button) -> None:
        member_id = interaction.user.id
        member_record = await self.bot.db.get_member(member_id)
        guild = self.bot.get_guild(member_record.guild_id) if member_record and member_record.guild_id else None
        member = guild.get_member(member_id) if guild else None

        if member and guild:
            await assign_role(
                self.bot, guild, member, "unverified", reason="Bypassed RSI verification"
            )

        for child in self.children:
            child.disabled = True  # type: ignore[union-attr]
        await interaction.response.edit_message(view=self)
        await interaction.followup.send(
            "You have been assigned the **SC-Unverified** role.\n"
            "Complete verification at any time with `/verify`."
        )


# ─── Recruitment — Org Application (persistent) ──────────────────────────────


class OrgApplicationView(ui.View):
    """Persistent view sent to a member after they receive SC-Verified."""

    def __init__(self, bot: AstralBot) -> None:
        super().__init__(timeout=None)
        self.bot = bot

    @ui.button(
        label="I've Applied!",
        style=discord.ButtonStyle.green,
        emoji="🚀",
        custom_id="persist:applied",
    )
    async def applied(self, interaction: discord.Interaction, button: ui.Button) -> None:
        member_id = interaction.user.id
        member_record = await self.bot.db.get_member(member_id)
        if not member_record or not member_record.guild_id:
            await interaction.response.send_message(
                "Could not find your record. Please contact an admin.", ephemeral=True
            )
            return

        await self.bot.db.upsert_member(member_id, applied_to_org=True)

        guild = self.bot.get_guild(member_record.guild_id)
        if guild:
            recruitment_channel = guild.get_channel(RECRUITMENT_CHANNEL_ID)
            member = guild.get_member(member_id)

            officer_role_record = await self.bot.db.get_role(
                guild.id, ROLE_NAMES["officer"]
            )
            officer_mention = (
                guild.get_role(officer_role_record.role_id).mention
                if officer_role_record and guild.get_role(officer_role_record.role_id)
                else "@Officer"
            )

            if recruitment_channel and member:
                embed = discord.Embed(
                    title="New Org Application",
                    color=discord.Color.blue(),
                    description=f"{member.mention} has applied to the org and confirmed below.",
                )
                embed.add_field(
                    name="RSI Handle",
                    value=member_record.rsi_username or "N/A",
                    inline=True,
                )
                embed.add_field(
                    name="Timezone",
                    value=member_record.timezone or "N/A",
                    inline=True,
                )
                embed.add_field(
                    name="Gameplay Style",
                    value=member_record.gameplay_style or "N/A",
                    inline=True,
                )
                if member_record.recruiter_id:
                    recruiter = guild.get_member(member_record.recruiter_id)
                    embed.add_field(
                        name="Recruiter",
                        value=recruiter.mention if recruiter else str(member_record.recruiter_id),
                        inline=True,
                    )
                embed.set_thumbnail(url=member.display_avatar.url)

                await recruitment_channel.send(  # type: ignore[union-attr]
                    f"{officer_mention} A new application needs review. "
                    f"Use `/admittance @{member.display_name}` to process it.",
                    embed=embed,
                )

        for child in self.children:
            child.disabled = True  # type: ignore[union-attr]
        await interaction.response.edit_message(
            content=(
                "Application confirmed! ✅\n"
                "Officers have been notified and will review your application soon. "
                "Please be patient while they process it."
            ),
            view=self,
        )


# ─── Recruitment — Admittance (non-persistent, officer-triggered) ─────────────


class AdmittanceView(ui.View):
    def __init__(
        self, bot: AstralBot, target_member_id: int, guild_id: int
    ) -> None:
        super().__init__(timeout=300)
        self.bot = bot
        self.target_member_id = target_member_id
        self.guild_id = guild_id

    @ui.button(label="Accept", style=discord.ButtonStyle.green, emoji="✅")
    async def accept(self, interaction: discord.Interaction, button: ui.Button) -> None:
        guild = self.bot.get_guild(self.guild_id)
        target = guild.get_member(self.target_member_id) if guild else None

        if not target or not guild:
            await interaction.response.send_message(
                "Member not found in the server.", ephemeral=True
            )
            return

        await assign_role(
            self.bot,
            guild,
            target,
            "rank1",
            reason=f"Accepted by {interaction.user}",
        )

        for child in self.children:
            child.disabled = True  # type: ignore[union-attr]
        await interaction.response.edit_message(
            content=f"**Accepted** {target.mention} — Rank1 role assigned.", view=self
        )

        try:
            await target.send(
                "🎉 **Congratulations!**\n"
                "Your application to AstralDynamics has been **accepted**.\n"
                "You have been assigned the **Rank1** role. Welcome to the crew, pilot!"
            )
        except discord.Forbidden:
            pass

    @ui.button(label="Deny", style=discord.ButtonStyle.red, emoji="❌")
    async def deny(self, interaction: discord.Interaction, button: ui.Button) -> None:
        guild = self.bot.get_guild(self.guild_id)
        target = guild.get_member(self.target_member_id) if guild else None

        if not target or not guild:
            await interaction.response.send_message(
                "Member not found in the server.", ephemeral=True
            )
            return

        for child in self.children:
            child.disabled = True  # type: ignore[union-attr]
        await interaction.response.edit_message(
            content=f"**Denied** {target.mention}.", view=self
        )

        lobby_channel = guild.get_channel(LOBBY_CHANNEL_ID)
        if lobby_channel:
            await lobby_channel.send(  # type: ignore[union-attr]
                f"{target.mention} — Unfortunately your application to AstralDynamics "
                "has not been accepted at this time. Please feel free to reach out to an "
                "Officer if you have any questions."
            )
