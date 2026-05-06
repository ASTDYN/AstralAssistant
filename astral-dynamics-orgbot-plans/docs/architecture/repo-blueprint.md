# Repo Blueprint

```text
astral-dynamics-orgbot/
├── apps/
│   ├── api/
│   └── bot/
├── libs/
│   ├── core/
│   ├── db/
│   ├── config/
│   ├── integrations/
│   └── rag/
├── prisma/
├── kb/
├── docs/
├── scripts/
└── test/
```

## Apps

### `apps/api`

NestJS HTTP API. Used now for health/admin/API boundaries and later by the website.

### `apps/bot`

NestJS Discord bot application. Owns Discord client lifecycle, slash command dispatch, and Discord event handling.

## Libraries

### `libs/core`

Pure application/domain services.

Subdomains:

- members
- recruitment
- operations
- ranks
- permissions
- moderation
- audit
- retention

### `libs/db`

Prisma service and repository layer.

### `libs/config`

Zod/env validation, feature flags, Discord IDs, retention policy.

### `libs/integrations`

External adapters:

- Star Citizen Wiki
- SENTRY, optional
- RSI public lookup, optional and disabled by default

### `libs/rag`

Knowledge base ingestion and retrieval.
