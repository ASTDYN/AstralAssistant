# Local Development Runbook

1. Install Node.js.
2. Install npm dependencies.

```bash
npm install
```

3. Copy environment.

```bash
cp .env.example .env
```

The default `DATABASE_URL` in `.env.example` targets **host development**: it uses `127.0.0.1:5432` so Prisma and Nest on your machine can reach Postgres after `docker compose up -d postgres` (published on `127.0.0.1:5432`). The Docker Compose **`api`** and **`bot`** services override `DATABASE_URL` to use the hostname **`postgres`** on the compose network, so you do not need two `.env` files for that split.

4. Start Postgres.

```bash
docker compose up -d postgres
```

5. Generate Prisma client.

```bash
npm run db:generate
```

6. Run migrations.

```bash
npm run db:migrate
```

7. Seed demo data.

```bash
npm run db:seed
```

8. Register Discord commands.

```bash
npm run commands:register
```

9. Start API.

```bash
npm run start:dev:api
```

10. Start bot.

```bash
npm run start:dev:bot
```
