# Yao GEOFlow CLI

`yao-geoflow-cli` is a local operations skill for controlling an existing GEOFlow system through the project CLI or Laravel API v1 fallback instead of the web admin.

Public project repository:

- [GEOFlow](https://github.com/yaojingang/GEOFlow)

## Primary Use

- first-time login with GEOFlow admin credentials
- inspect catalog IDs
- create, start, stop, or enqueue tasks
- inspect jobs
- upload article drafts
- review and publish articles
- run Laravel `/api/v1` fallback preflight when the CLI wrapper is absent
- diagnose Docker/base-URL problems when API fallback returns HTML instead of JSON

## Boundary

This skill does not implement GEOFlow backend code and does not write directly to the database. It prefers `bin/geoflow` when present. If the current Laravel rewrite has no CLI wrapper, it may operate through `/api/v1` with bearer auth and idempotency keys. First-time access should use `geoflow login` when the CLI exists, or `/api/v1/auth/login` when using API fallback.

## Package Map

- `SKILL.md`: trigger boundary and operating workflow
- `agents/interface.yaml`: canonical interface metadata
- `agents/openai.yaml`: OpenAI-friendly interface metadata
- `references/operation-boundary.md`: safety and scope rules
- `references/command-map.md`: capability-to-command mapping
- `references/laravel-api-v1-docker.md`: Laravel API v1 fallback, Docker checks, scopes, and non-JSON diagnostics
- `scripts/geoflow_preflight.sh`: deterministic CLI/config or API fallback preflight
- `evals/trigger_cases.json`: trigger boundary checks
