# Cursor Handoff

## Goal

Create a Docker-hosted, npm-based, NestJS monorepo for `AstralDynamics OrgBot`.

The first usable product is a private Discord server bot. The backend must be designed so a future website can reuse the same domain services and database.

## Build constraints

- Use npm workspaces.
- Use NestJS for both the API app and bot app.
- Use PostgreSQL.
- Use Prisma.
- Use Docker Compose for local/dev and Docker-host deployment.
- Target one private Discord server for V1.
- Do not build multi-tenant org support in V1.
- Do not scrape RSI login-protected pages.
- Keep SENTRY optional and disabled by default.
- Keep ship/fleet, treasury, training, diplomacy, analytics, live dispatch, and mission board modules out of V1.

## Implementation order

1. Create root npm workspace.
2. Create NestJS monorepo with:
   - `apps/api`
   - `apps/bot`
   - `libs/core`
   - `libs/db`
   - `libs/config`
   - `libs/integrations`
   - `libs/rag`
3. Add Docker Compose with Postgres, API, and bot services.
4. Add Prisma schema from `prisma/schema.prisma`.
5. Add seed data from `prisma/seed-data`.
6. Implement Discord bot boot/login.
7. Implement slash command registration.
8. Implement identity commands:
   - `/register`
   - `/profile`
   - `/set-rsi-handle`
   - `/set-timezone`
   - `/set-interests`
9. Implement recruitment:
   - `/apply`
   - `/applicant-list`
   - `/approve-recruit`
   - `/reject-recruit`
   - `/set-trial`
10. Implement roles/ranks:
   - `#1` through `#5`
   - website role: `ADMIN` or `USER`
   - Discord role sync placeholders
11. Implement operation planning:
   - admin creates/controls ops
   - members view/join/leave
12. Implement admin moderation:
   - warnings
   - incidents
   - notes
   - audit logs
13. Implement retention configuration.
14. Add markdown KB ingestion.
15. Implement `/ask`, `/rules`, `/start-here`.
16. Add website-ready API routes but defer full web UI.

## Definition of done for V1

- A new Discord member can register with an RSI handle.
- A member can submit a short application.
- Admins can approve/reject/set trial status.
- Admins can promote/demote rank labels `#1`–`#5`.
- Admins can create operations.
- Members can view/join/leave operations.
- Admins can view operation rosters.
- Admins can create warnings/incidents/notes.
- The bot can answer from local KB markdown documents.
- The app runs through Docker Compose on a Docker host.
