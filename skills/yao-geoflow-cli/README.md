# Yao GEOFlow CLI

`yao-geoflow-cli` is a local operations skill for controlling an existing GEOFlow system through the project CLI instead of the web admin.

Public project repository:

- [GEOFlow](https://github.com/yaojingang/GEOFlow)

## Primary Use

- first-time login with GEOFlow admin credentials
- inspect catalog IDs
- create, start, stop, or enqueue tasks
- inspect jobs
- upload article drafts
- review and publish articles

## Boundary

This skill does not implement GEOFlow backend code and does not write directly to the database. It operates through `bin/geoflow`, which in turn calls `/api/v1`. First-time access should use `geoflow login` with the GEOFlow administrator username and password.

## Package Map

- `SKILL.md`: trigger boundary and operating workflow
- `agents/interface.yaml`: canonical interface metadata
- `agents/openai.yaml`: OpenAI-friendly interface metadata
- `references/operation-boundary.md`: safety and scope rules
- `references/command-map.md`: capability-to-command mapping
- `scripts/geoflow_preflight.sh`: deterministic CLI/config preflight
- `evals/trigger_cases.json`: trigger boundary checks
