import discord
from discord import app_commands
from discord.ext import commands

from bot.config import ADMIN_NOTIFS_CHANNEL_ID, LOBBY_CHANNEL_ID
from bot.utils.views import StartOnboardingView, VerificationView


_WELCOME_MESSAGE = (
    "Welcome to **{guild_name}**! 👋\n\n"
    "To access the server, we need to verify your **Roberts Space Industries** account.\n\n"
    "**What you'll need:**\n"
    "• Your RSI handle (username)\n"
    "• ~2 minutes to complete the process\n\n"
    "Click **Begin Verification** to start, or **Skip** to join as Unverified."
)


class MemberOnboarding(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member) -> None:
        # Notify admins
        admin_channel = member.guild.get_channel(ADMIN_NOTIFS_CHANNEL_ID)
        if admin_channel:
            embed = discord.Embed(
                title="New Member Joined",
                color=discord.Color.green(),
                description=f"{member.mention} has joined the server.",
            )
            embed.add_field(name="Account Created", value=discord.utils.format_dt(member.created_at, "R"), inline=True)
            embed.add_field(name="Member #", value=str(member.guild.member_count), inline=True)
            embed.set_thumbnail(url=member.display_avatar.url)
            await admin_channel.send(embed=embed)  # type: ignore[union-attr]

        # Create DB record and generate verification code linkage
        await self.bot.db.upsert_member(member.id, guild_id=member.guild.id)  # type: ignore[attr-defined]

        # Send onboarding DM; fall back to lobby channel if DMs are closed
        view = StartOnboardingView(self.bot)  # type: ignore[arg-type]
        welcome_text = _WELCOME_MESSAGE.format(guild_name=member.guild.name)

        try:
            await member.send(welcome_text, view=view)
        except discord.Forbidden:
            lobby = member.guild.get_channel(LOBBY_CHANNEL_ID)
            if lobby:
                await lobby.send(  # type: ignore[union-attr]
                    f"{member.mention} — Welcome! Please enable DMs from server members "
                    "so we can send you your verification information. "
                    "You can also use `/verify` here to start the process."
                )

    # ─── /verify slash command ────────────────────────────────────────────────

    @app_commands.command(
        name="verify", description="Start or restart the RSI verification process"
    )
    async def verify(self, interaction: discord.Interaction) -> None:
        member_record = await self.bot.db.get_member(interaction.user.id)  # type: ignore[attr-defined]

        if member_record and member_record.is_verified:
            await interaction.response.send_message(
                "You are already verified! ✅", ephemeral=True
            )
            return

        # Ensure a DB record exists for DM-based verifications
        guild_id = interaction.guild.id if interaction.guild else (
            member_record.guild_id if member_record else None
        )
        if guild_id:
            await self.bot.db.upsert_member(interaction.user.id, guild_id=guild_id)  # type: ignore[attr-defined]

        if member_record and member_record.verification_code:
            # Re-send the verification code step
            view = VerificationView(self.bot)  # type: ignore[arg-type]
            await interaction.response.send_message(
                f"**RSI Verification**\n\n"
                f"Your verification code is:\n"
                f"```\n{member_record.verification_code}\n```\n"
                f"Add it to your RSI biography at <https://robertsspaceindustries.com/account/profile> "
                f"then click **Verify**.",
                view=view,
                ephemeral=False,
            )
        else:
            view = StartOnboardingView(self.bot)  # type: ignore[arg-type]
            await interaction.response.send_message(
                _WELCOME_MESSAGE.format(
                    guild_name=interaction.guild.name if interaction.guild else "AstralDynamics"
                ),
                view=view,
            )


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(MemberOnboarding(bot))
