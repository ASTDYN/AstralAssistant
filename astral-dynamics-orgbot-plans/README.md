# AstralDynamics OrgBot — Cursor Planning Package

This package contains planning artifacts for a Discord-first Star Citizen organization management bot.

The V1 MVP is intentionally scoped to:

- Discord onboarding and registration
- RSI handle / in-game identity tracking
- Recruit pipeline
- Rank/status management
- Admin-controlled operation planning
- Member RSVP
- RAG/helpbot knowledge base
- Admin-only notes, warnings, and incidents
- Website-ready backend architecture

This is not intended to be a finished app. It is a Cursor handoff package that defines the repo shape, domain model, config boundaries, and implementation sequence.

## Current fixed decisions

```json
{
  "projectName": "AstralDynamics OrgBot",
  "packageManager": "npm",
  "backendFramework": "NestJS",
  "deploymentTarget": "Docker host",
  "discordScope": "single private Discord server",
  "orgName": "AstralDynamics",
  "rankLabels": ["#1", "#2", "#3", "#4", "#5"],
  "identityRule": {
    "technicalPrimaryId": "discordUserId",
    "orgFacingIdentity": "rsiHandle",
    "displayNameDefault": "rsiHandle",
    "discordUsername": "snapshot only"
  },
  "externalLookups": {
    "starCitizenWiki": "enabled",
    "sentry": "optional disabled by default",
    "rsiPublicLookup": "disabled by default",
    "rsiLoginScraping": "prohibited boundary"
  },
  "retention": {
    "warningsDays": 30,
    "incidentsDays": 60,
    "adminNotesDays": 90
  },
  "channelConfig": "pending",
  "discordRoleConfig": "pending"
}
```

## How to use in Cursor

1. Upload or unzip this package into Cursor.
2. Start with `CURSOR_HANDOFF.md`.
3. Use `docs/product/v1-scope.md` to keep implementation constrained.
4. Use `docs/architecture/repo-blueprint.md` for folder structure.
5. Use `docs/architecture/data-model.md` and `prisma/schema.prisma` for the first schema pass.
6. Use `docs/product/command-map.md` to implement commands in phases.
7. Keep future modules in `TODO.md` until V1 is stable.
