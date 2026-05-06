import discord
from discord import app_commands
from discord.ext import commands

from bot.config import ROLE_NAMES
from bot.utils.views import AdmittanceView, OrgApplicationView

_ORG_URL = "https://robertsspaceindustries.com/en/orgs/ASTDYN"

_APPLY_MESSAGE = (
    "🎉 **You're now SC-Verified!**\n\n"
    "The next step is to apply to the **AstralDynamics** organisation on RSI:\n"
    f"{_ORG_URL}\n\n"
    "Once you've submitted your application on the RSI website, "
    "click the button below so our officers can review it."
)


class Recruitment(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    # ─── Detect SC-Verified role assignment ───────────────────────────────────

    @commands.Cog.listener()
    async def on_member_update(
        self, before: discord.Member, after: discord.Member
    ) -> None:
        verified_name = ROLE_NAMES["verified"]
        before_role_names = {r.name for r in before.roles}
        after_role_names = {r.name for r in after.roles}

        if verified_name in after_role_names and verified_name not in before_role_names:
            await self._handle_newly_verified(after)

    async def _handle_newly_verified(self, member: discord.Member) -> None:
        view = OrgApplicationView(self.bot)  # type: ignore[arg-type]
        try:
            await member.send(_APPLY_MESSAGE, view=view)
        except discord.Forbidden:
            pass

    # ─── /admittance slash command ────────────────────────────────────────────

    @app_commands.command(
        name="admittance",
        description="Process a member's AstralDynamics org admittance (Officer only)",
    )
    @app_commands.describe(member="The member whose application you are reviewing")
    async def admittance(
        self, interaction: discord.Interaction, member: discord.Member
    ) -> None:
        # Verify caller has Officer role
        officer_role_record = await self.bot.db.get_role(  # type: ignore[attr-defined]
            interaction.guild.id, ROLE_NAMES["officer"]
        )
        if officer_role_record:
            officer_role = interaction.guild.get_role(officer_role_record.role_id)
            if officer_role and officer_role not in interaction.user.roles:  # type: ignore[attr-defined]
                await interaction.response.send_message(
                    "You must have the **Officer** role to use this command.",
                    ephemeral=True,
                )
                return

        member_record = await self.bot.db.get_member(member.id)  # type: ignore[attr-defined]

        embed = discord.Embed(
            title=f"Admittance Review — {member.display_name}",
            color=discord.Color.orange(),
        )
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.add_field(
            name="RSI Handle",
            value=member_record.rsi_username if member_record else "N/A",
            inline=True,
        )
        embed.add_field(
            name="Timezone",
            value=member_record.timezone if member_record else "N/A",
            inline=True,
        )
        embed.add_field(
            name="Gameplay Style",
            value=member_record.gameplay_style if member_record else "N/A",
            inline=True,
        )
        if member_record and member_record.recruiter_id:
            recruiter = interaction.guild.get_member(member_record.recruiter_id)
            embed.add_field(
                name="Recruiter",
                value=recruiter.mention if recruiter else str(member_record.recruiter_id),
                inline=True,
            )
        embed.add_field(
            name="Applied to Org",
            value="Yes ✅" if (member_record and member_record.applied_to_org) else "Not confirmed",
            inline=True,
        )

        view = AdmittanceView(self.bot, member.id, interaction.guild.id)  # type: ignore[arg-type]
        await interaction.response.send_message(
            f"Reviewing application for {member.mention}:",
            embed=embed,
            view=view,
        )


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Recruitment(bot))
