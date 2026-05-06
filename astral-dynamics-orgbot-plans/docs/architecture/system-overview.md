# System Overview

## Architecture

```text
Discord Bot
  -> NestJS Bot App
  -> Shared Core Domain Services
  -> Prisma Repositories
  -> PostgreSQL

Future Website
  -> NestJS API
  -> Shared Core Domain Services
  -> Prisma Repositories
  -> PostgreSQL
```

## Major components

| Component | Responsibility |
|---|---|
| `apps/bot` | Discord client, slash commands, Discord events |
| `apps/api` | Future website/API access, health checks, admin routes |
| `libs/core` | Domain logic for members, recruitment, ops, moderation |
| `libs/db` | Prisma client and repositories |
| `libs/config` | Environment, org, Discord, retention, feature flag config |
| `libs/integrations` | Star Citizen Wiki, optional SENTRY, optional RSI public lookup |
| `libs/rag` | KB ingestion, chunking, retrieval, answer generation |
| `kb` | Markdown source documents |
| `docs` | Product and architecture planning |

## Design rules

- Keep Discord-specific code out of core business logic.
- Keep database calls in repository/service boundaries.
- Keep external integrations optional and cached.
- Keep future website API using same core services.
- Keep V1 single-server only.
