# Register Discord Commands

Use a script rather than registering commands inside every bot startup.

Expected script:

```text
scripts/register-discord-commands.ts
```

Required environment variables:

- `DISCORD_BOT_TOKEN`
- `DISCORD_CLIENT_ID`
- `DISCORD_GUILD_ID`

For V1, register commands to one guild, not globally. Guild command registration updates faster and fits the private-server requirement.
