# AstralAssistant — AstralDynamics Discord Bot

A Discord bot for the AstralDynamics Star Citizen organisation. Handles RSI account verification, member onboarding, and org recruitment workflow.

## Features

- **RSI Verification** — Members verify their RSI account by placing a generated code in their bio
- **New Member Onboarding** — Guided DM flow collecting timezone, gameplay style, and recruiter
- **Recruitment Workflow** — SC-Verified members are guided to apply to the org; officers review via `/admittance`
- **Automatic Role Management** — Bot creates required roles on startup and persists them to the database

## Roles managed

| Role | Purpose |
|------|---------|
| `SC-Unverified` | Joined but not RSI-verified |
| `SC-Verified` | RSI account confirmed |
| `Officer` | Can process admittance requests |
| `Rank1` | Accepted org member |

## Quick start (Docker)

1. Copy `.env.example` to `.env` and fill in your values:

```env
DISCORD_TOKEN=your_token
POSTGRES_PASSWORD=a_secure_password
ADMIN_NOTIFS_CHANNEL_ID=...
RECRUITMENT_CHANNEL_ID=...
LOBBY_CHANNEL_ID=...
```

2. Pull and run:

```bash
docker compose up -d
```

The bot auto-creates database tables on first run.

## Development setup

Requires Python 3.11+ and [Poetry](https://python-poetry.org/).

```bash
poetry install
cp .env.example .env   # fill in values
poetry run bot
```

A local PostgreSQL instance is required. The `docker-compose.yml` can be used to run just the database:

```bash
docker compose up -d db
DATABASE_URL=postgresql://astral:password@localhost:5432/astralbot poetry run bot
```

## Required Discord permissions & intents

**Bot permissions:** Manage Roles, Send Messages, Read Message History, Embed Links, Use Application Commands

**Privileged Gateway Intents:** Server Members Intent, Message Content Intent

## CI/CD

Pushing to `main` triggers a GitHub Actions workflow that builds a multi-arch Docker image (`linux/amd64` + `linux/arm64`) and pushes it to the GitHub Container Registry (`ghcr.io`).

```
ghcr.io/astdyn/astralassistant:latest
ghcr.io/astdyn/astralassistant:sha-<short-sha>
```

## Environment variables

| Variable | Description |
|----------|-------------|
| `DISCORD_TOKEN` | Bot token from Discord Developer Portal |
| `DATABASE_URL` | PostgreSQL connection string |
| `ADMIN_NOTIFS_CHANNEL_ID` | Channel ID for new-member notifications |
| `RECRUITMENT_CHANNEL_ID` | Channel ID for recruitment officer notifications |
| `LOBBY_CHANNEL_ID` | Channel ID for public-facing messages |
