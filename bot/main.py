import asyncio
import discord
from discord.ext import commands

from config import DISCORD_TOKEN
from database.db import Database


class AstralBot(commands.Bot):
    def __init__(self) -> None:
        intents = discord.Intents.default()
        intents.members = True
        intents.message_content = True
        super().__init__(command_prefix="!", intents=intents)
        self.db = Database()

    async def setup_hook(self) -> None:
        await self.db.initialize()

        await self.load_extension("bot.cogs.role_management")
        await self.load_extension("bot.cogs.member_onboarding")
        await self.load_extension("bot.cogs.recruitment")

        # Register persistent views so buttons survive bot restarts
        from bot.utils.views import OrgApplicationView, StartOnboardingView, VerificationView

        self.add_view(StartOnboardingView(self))
        self.add_view(VerificationView(self))
        self.add_view(OrgApplicationView(self))

        await self.tree.sync()
        print("[bot] Application commands synced")

    async def on_ready(self) -> None:
        print(f"[bot] Logged in as {self.user} (ID: {self.user.id})")  # type: ignore[union-attr]
        await self.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name="the stars | /verify",
            )
        )

    async def on_command_error(
        self, ctx: commands.Context, error: commands.CommandError
    ) -> None:
        if not isinstance(error, commands.CommandNotFound):
            print(f"[bot] Command error: {error}")


def main() -> None:
    bot = AstralBot()
    bot.run(DISCORD_TOKEN, log_handler=None)


if __name__ == "__main__":
    main()
