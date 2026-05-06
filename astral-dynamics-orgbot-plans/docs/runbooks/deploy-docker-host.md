# Docker Host Deployment Runbook

1. Copy repo to host.
2. Create `.env`.
3. Confirm `DATABASE_URL` uses the compose service name `postgres`.
4. Build and start.

```bash
docker compose up -d --build
```

5. Apply migrations.

```bash
docker compose exec api npm run db:deploy
```

6. Register Discord commands.

```bash
docker compose exec bot npm run commands:register
```

7. Check logs.

```bash
docker compose logs -f api
docker compose logs -f bot
```
