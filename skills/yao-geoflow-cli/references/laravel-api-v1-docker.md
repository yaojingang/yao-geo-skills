# Laravel API v1 and Docker Fallback

Use this reference when the target GEOFlow workspace is the Laravel rewrite and no `bin/geoflow` wrapper is available yet.

## Detection

A Laravel GEOFlow workspace should contain:

- `artisan`
- `routes/api.php`
- `app/Http/Controllers/Api/V1`
- `docker-compose.yml` or `compose.yml` when deployed through Docker

Do not assume the old root-level PHP entrypoints exist.

## API Base URL

`GEOFLOW_BASE_URL` must point to the public web root:

```bash
export GEOFLOW_BASE_URL="http://127.0.0.1:18080"
```

Do not set it to:

- `http://127.0.0.1:18080/api/v1`
- `http://127.0.0.1:18080/geo_admin`
- an internal Docker service name unless the agent is running inside the same network
- a proxy endpoint that returns an HTML error page

The skill appends `/api/v1/...` itself.

## Required Token

API fallback requires:

```bash
export GEOFLOW_API_TOKEN="..."
```

The token must allow the scopes needed for the requested operation:

- `catalog:read`
- `tasks:read`
- `tasks:write`
- `jobs:read`
- `articles:read`
- `articles:write`
- `articles:publish`

If no token exists, obtain one through the authenticated admin API:

```bash
curl -sS -X POST \
  -H "Accept: application/json" \
  -H "Content-Type: application/json" \
  --data '{"username":"admin","password":"<password>"}' \
  "$GEOFLOW_BASE_URL/api/v1/auth/login"
```

Do not print the full token in user-facing output.

## Docker Checks

From the GEOFlow workspace:

```bash
docker compose ps
docker compose exec app php artisan route:list --path=api/v1
docker compose exec app php artisan about
```

If the PHP service name is not `app`, inspect `docker compose ps` and use the actual service name.

For database host issues, remember:

- inside Docker Compose, `DB_HOST=postgres` is usually correct when the service is named `postgres`
- outside Docker Compose, `postgres` will not resolve unless DNS/hosts provides it
- browser access should use the exposed host port, for example `127.0.0.1:18080`

## Preflight

Run:

```bash
skills/yao-geoflow-cli/scripts/geoflow_preflight.sh "/path/to/GEOFlow"
```

Preflight is successful only when an authenticated `GET /api/v1/catalog` returns JSON.

## Non-JSON Response Diagnosis

If the response body starts with HTML, for example:

```text
<!doctype html>
```

Do not diagnose this as an AI response-format error. It usually means:

- `GEOFLOW_BASE_URL` points to the wrong path
- the app is behind a proxy error page
- the request reached the frontend/admin web route instead of `/api/v1`
- the Docker service is not exposing the Laravel app on the expected port
- the server returned a framework error page instead of JSON

Correct the URL, proxy, container, or Laravel route setup before retrying business operations.

## Current API Surface

The Laravel rewrite exposes these API v1 paths:

- `POST /api/v1/auth/login`
- `GET /api/v1/catalog`
- `GET /api/v1/tasks`
- `POST /api/v1/tasks`
- `GET /api/v1/tasks/{id}`
- `PATCH /api/v1/tasks/{id}`
- `POST /api/v1/tasks/{id}/start`
- `POST /api/v1/tasks/{id}/stop`
- `POST /api/v1/tasks/{id}/enqueue`
- `GET /api/v1/tasks/{id}/jobs`
- `GET /api/v1/jobs/{id}`
- `GET /api/v1/articles`
- `POST /api/v1/articles`
- `GET /api/v1/articles/{id}`
- `PATCH /api/v1/articles/{id}`
- `POST /api/v1/articles/{id}/review`
- `POST /api/v1/articles/{id}/publish`
- `POST /api/v1/articles/{id}/trash`

Mutating endpoints should use `X-Idempotency-Key`.
