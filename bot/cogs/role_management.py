import discord
from discord.ext import commands

from bot.config import ROLE_NAMES


class RoleManagement(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        for guild in self.bot.guilds:
            await self._ensure_roles(guild)

    async def _ensure_roles(self, guild: discord.Guild) -> None:
        existing = {role.name: role for role in guild.roles}

        for role_key, role_name in ROLE_NAMES.items():
            if role_name in existing:
                role = existing[role_name]
                print(f"[roles] '{role_name}' already exists in {guild.name}")
            else:
                role = await guild.create_role(
                    name=role_name,
                    reason="AstralBot automatic role setup",
                )
                print(f"[roles] Created '{role_name}' in {guild.name}")

            await self.bot.db.upsert_role(guild.id, role_name, role.id)  # type: ignore[attr-defined]


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(RoleManagement(bot))
