# Channel and Role Configuration

The bot identifies Discord channels and roles by ID via environment variables.
Channel and role names are not used because they can be renamed at any time.

All identifiers below are **pending** until the live AstralDynamics Discord
server is finalized. The bot is designed to start with empty values; commands
that require a specific channel or role simply degrade gracefully when the ID
is missing.

## Channels

| Env var | Purpose |
|---|---|
| `DISCORD_ONBOARDING_CHANNEL_ID` | Where new members are routed for `/start-here`, `/register`. |
| `DISCORD_ADMIN_LOG_CHANNEL_ID` | Audit-style log of moderation actions, recruit pipeline events, role changes. |
| `DISCORD_OPS_CHANNEL_ID` | Where operations are announced, RSVPs surface, and `/op` output lands. |
| `DISCORD_BOT_OUTPUT_CHANNEL_ID` | Default fallback for non-channel-specific bot output. |
| `DISCORD_RULES_CHANNEL_ID` | Source channel referenced by `/rules`. |
| `DISCORD_ANNOUNCEMENTS_CHANNEL_ID` | Where the bot posts org-wide announcements. |

## Roles

| Env var | Purpose |
|---|---|
| `DISCORD_ADMIN_ROLE_ID` | Sole source of truth for admin permission. Mirrored to `MemberProfile.websiteRole = ADMIN` on `/sync-roles`. |
| `DISCORD_MEMBER_ROLE_ID` | Granted on accepted recruitment. |
| `DISCORD_RECRUIT_ROLE_ID` | Granted when an application is created. |
| `DISCORD_TRIAL_MEMBER_ROLE_ID` | Granted when an admin runs `/set-trial`. |
| `DISCORD_BOT_MANAGER_ROLE_ID` | Reserved for future use; currently unused. |

## Separation of concerns

These IDs are **Discord-server permissions only**. They do not encode:

- Org rank labels `#1`–`#5` (stored in `Rank` and `MemberProfile.rankLabel`)
- Gameplay interest tags (stored in `InterestTag` and `Application.interests`)
- Website permissions (`WebsiteRole.ADMIN` / `WebsiteRole.USER`)

See [`docs/architecture/permissions-model.md`](permissions-model.md) for the
canonical four-concept split.

## Where these are loaded

Environment values land in [`libs/config/src/discord.config.ts`](../../libs/config/src/discord.config.ts)
through the `discordConfig` constant and are validated at boot via the Zod schema in
[`libs/config/src/env.schema.ts`](../../libs/config/src/env.schema.ts). The `.env.example`
file at the repo root carries placeholders that should be filled before running
`npm run commands:register` or starting the bot in a real guild.

## Admin detection rule

A Discord user is treated as an admin if their guild member object has the
role identified by `DISCORD_ADMIN_ROLE_ID`. The bot mirrors this state into
`MemberProfile.websiteRole` whenever `/sync-roles` runs so that the future
website can reuse the same admin set without re-querying Discord.
