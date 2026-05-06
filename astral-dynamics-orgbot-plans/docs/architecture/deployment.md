# Deployment

## Target

Docker host.

## Services

- `postgres`
- `api`
- `bot`

## Local/dev command shape

```bash
cp .env.example .env
docker compose up -d postgres
npm install
npm run db:generate
npm run db:migrate
npm run db:seed
npm run commands:register
npm run start:dev:bot
npm run start:dev:api
```

## Docker deployment shape

```bash
docker compose up -d --build
```

## Notes

- `api` and `bot` should be independently restartable.
- Postgres volume should be persistent.
- Secrets belong in `.env`, not committed.
- Discord command registration should be a script, not done on every startup unless intentional.
