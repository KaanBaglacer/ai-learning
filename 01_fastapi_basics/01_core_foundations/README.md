PostgreSQL with Docker Compose

Files added:
- `docker-compose.yml` : starts a `postgres:15-alpine` container, exposes 5432, mounts an init SQL script and a named volume.
- `.env` : contains POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB used by the image.

Quick start (Windows, Command Prompt):

1) From project root run:

```
cd c:\Users\kaanb\IdeaProjects\ai-learning\01_fastapi_basics\01_core_foundations
docker compose up -d
```

2) Check logs:

```
docker compose logs -f db
```

3) Connect and run a query (using container's psql):

```
docker compose exec db psql -U %POSTGRES_USER% -d %POSTGRES_DB% -c "SELECT * FROM sample;"
```

Notes:
- The init SQL script is executed only on the first initialization of the data volume.
- To reset the DB for testing, stop compose and remove the volume:

```
docker compose down -v
```

Security:
- The `.env` contains plaintext credentials for local/dev use only. For production, use a secrets manager.

If you want, I can also:
- produce a Dockerfile that builds a custom image,
- add a healthcheck, or
- wire this DB into your FastAPI app in the repo.

