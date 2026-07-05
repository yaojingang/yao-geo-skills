---
name: yao-geoflow-cli
description: Use when operating an existing GEOFlow 2.1+ system from CLI, API v1, or authenticated admin web for catalog/material/task/job/article operations, enterprise knowledge, growth-center leads, distribution, analytics, URL import, theme editor, frontend-capability sync, system updates, settings, tokens, users, or preflight. Do not use for implementation, schema changes, direct DB edits, frontend design, or invented API routes.
---

# Yao GEOFlow Operations

Operate a running GEOFlow instance. Prefer supported `bin/geoflow`, then API v1 for exposed content operations, then authenticated admin web for management workflows absent from API v1.

## Boundary

- Owns operational CLI/API/admin work, CSRF/session handling, idempotency, readback verification, high-risk confirmation, and secret/personal-data redaction.
- Excludes product-code edits, migrations, direct SQL, frontend design, route invention, auth bypass, and secret exposure.
- Use `yao-geoflow-design` for homepage/design payload planning.

## Checks

1. Confirm `artisan` or `bin/geoflow`.
2. Run `scripts/geoflow_preflight.sh "<workspace>" [config] [checks]` before first mutation.
3. Inspect CLI help, `routes/api.php`, or `php artisan route:list` before choosing a surface.
4. API fallback uses bearer auth, JSON, `Accept: application/json`, and `X-Idempotency-Key`.
5. Admin web reads the target page first, keeps CSRF/cookies, posts the owning route, then verifies readback.
6. Require explicit target/action for destructive, secret-revealing, package-download, theme-publish, bulk sync, lead export, or update-center operations.

## References

[operation-boundary.md](references/operation-boundary.md), [command-map.md](references/command-map.md), [laravel-api-v1-docker.md](references/laravel-api-v1-docker.md), [geoflow-current-capability-map.md](references/geoflow-current-capability-map.md), [trigger_cases.json](evals/trigger_cases.json), [upgrade report](reports/geoflow-skill-upgrade-2026-07-05.md).
