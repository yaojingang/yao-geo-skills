<!--
Copyright © 2026 姚金刚. All rights reserved.
Project: yao-geoflow-cli
Created by: 姚金刚
Date: 2026-05-16
X: https://x.com/yaojingang
-->

# Yao GEOFlow Operations

`yao-geoflow-cli` operates an existing GEOFlow 2.1+ system through the local project CLI, Laravel API v1 fallback, or authenticated admin web flows. It is for production operations, not product-code implementation.

Public project repository:

- [GEOFlow](https://github.com/yaojingang/GEOFlow)

## Primary Use

- authenticate and preflight CLI/API/admin surfaces
- inspect catalog IDs and material libraries
- manage material libraries, material items, tasks, jobs, drafts, reviews, published articles, and trash flows
- configure task publish scope, distribution strategy, image count, multi-knowledge-base, review, loop, and auto metadata settings
- operate admin-only workflows: Distribution Management, Analytics, URL Import, System Updates, Site Settings, Theme Replication, Theme Editor, AI configuration, API tokens, admin users, and activity logs
- operate GEOFlow 2.1+ workflows: enterprise knowledge drafting/publish, knowledge-base Markdown and chunk refresh, growth-center lead forms/leads/export, frontend-capability refresh, and settings-sync preview
- diagnose Docker/base-URL problems when API fallback returns HTML instead of JSON

## Boundary

This skill does not implement GEOFlow backend/frontend code and does not write directly to the database. It prefers `bin/geoflow` only when present and when `--help` confirms the requested action. If the Laravel app has no CLI wrapper, it operates through `/api/v1` with bearer auth and idempotency keys.

Distribution management, enterprise knowledge, growth center, live theme editor, frontend-capability sync, system updates, site settings, API tokens, and admin-user management are admin web flows unless the target workspace exposes matching API routes. The skill may operate those flows through an authenticated admin session, but it must not claim they are API v1 endpoints.

High-risk actions such as force-delete, empty trash, secret reveal/rotation, package download, API token revoke, admin-user deletion, password update, system update apply/retry/rollback, theme publish, and bulk distribution writes require explicit target confirmation and post-action verification. Secrets are redacted in summaries.

## Package Map

- `SKILL.md`: trigger boundary and operating workflow
- `agents/interface.yaml`: canonical interface metadata
- `agents/openai.yaml`: OpenAI-friendly interface metadata
- `references/operation-boundary.md`: safety and scope rules
- `references/command-map.md`: capability-to-command/admin-route mapping
- `references/laravel-api-v1-docker.md`: Laravel API v1 fallback, Docker checks, scopes, and non-JSON diagnostics
- `references/geoflow-current-capability-map.md`: current GEOFlow 2.1+ API/admin coverage map
- `scripts/geoflow_preflight.sh`: deterministic CLI/config or API fallback preflight
- `evals/trigger_cases.json`: trigger boundary checks
- `reports/geoflow-skill-upgrade-2026-07-05.md`: upgrade evidence and verification notes
