# Command Map

## Preflight

```bash
scripts/geoflow_preflight.sh "<workspace>" [config]
```

The preflight supports two modes:

- CLI mode when `<workspace>/bin/geoflow` exists.
- API fallback mode when the CLI is absent and `GEOFLOW_BASE_URL` plus `GEOFLOW_API_TOKEN` are available.

## First Login

Interactive password prompt:

```bash
"/path/to/workspace/bin/geoflow" login --base-url https://your-geoflow-host --username admin
```

Explicit password:

```bash
"/path/to/workspace/bin/geoflow" login --base-url https://your-geoflow-host --username admin --password <PASSWORD>
```

When config exists but the token is invalid or expired, refresh it in place:

```bash
"/path/to/workspace/bin/geoflow" login --base-url https://your-geoflow-host --username admin --force
```

## Catalog

```bash
"/path/to/workspace/bin/geoflow" --config /path/to/config catalog
```

Use this as the authoritative authenticated-read check before mutating commands. Only jump to `login --force` when the failure is clearly `401`, `403`, or token-invalid.

API fallback:

```bash
curl -sS \
  -H "Authorization: Bearer $GEOFLOW_API_TOKEN" \
  -H "Accept: application/json" \
  "$GEOFLOW_BASE_URL/api/v1/catalog"
```

## Task Operations

List tasks:

```bash
"/path/to/workspace/bin/geoflow" --config /path/to/config task list --status active --per-page 20
```

Create task:

```bash
"/path/to/workspace/bin/geoflow" --config /path/to/config task create --json ./task.json --idempotency-key task-create-001
```

API fallback:

```bash
curl -sS -X POST \
  -H "Authorization: Bearer $GEOFLOW_API_TOKEN" \
  -H "Accept: application/json" \
  -H "Content-Type: application/json" \
  -H "X-Idempotency-Key: task-create-001" \
  --data @./task.json \
  "$GEOFLOW_BASE_URL/api/v1/tasks"
```

Get task:

```bash
"/path/to/workspace/bin/geoflow" --config /path/to/config task get 12
```

Update task:

```bash
"/path/to/workspace/bin/geoflow" --config /path/to/config task update 12 --json ./task-patch.json --idempotency-key task-update-12
```

Start task:

```bash
"/path/to/workspace/bin/geoflow" --config /path/to/config task start 12 --idempotency-key task-start-12
```

API fallback:

```bash
curl -sS -X POST \
  -H "Authorization: Bearer $GEOFLOW_API_TOKEN" \
  -H "Accept: application/json" \
  -H "Content-Type: application/json" \
  -H "X-Idempotency-Key: task-start-12" \
  --data '{"enqueue_now":true}' \
  "$GEOFLOW_BASE_URL/api/v1/tasks/12/start"
```

Start and enqueue immediately:

```bash
"/path/to/workspace/bin/geoflow" --config /path/to/config task start 12 --enqueue-now --idempotency-key task-start-12
```

Stop task:

```bash
"/path/to/workspace/bin/geoflow" --config /path/to/config task stop 12 --idempotency-key task-stop-12
```

Manual enqueue:

```bash
"/path/to/workspace/bin/geoflow" --config /path/to/config task enqueue 12 --idempotency-key task-enqueue-12
```

List task jobs:

```bash
"/path/to/workspace/bin/geoflow" --config /path/to/config task jobs 12 --limit 20
```

Get job:

```bash
"/path/to/workspace/bin/geoflow" --config /path/to/config job get 88
```

## Article Operations

List articles:

```bash
"/path/to/workspace/bin/geoflow" --config /path/to/config article list --task-id 12 --per-page 20
```

API fallback:

```bash
curl -sS \
  -H "Authorization: Bearer $GEOFLOW_API_TOKEN" \
  -H "Accept: application/json" \
  "$GEOFLOW_BASE_URL/api/v1/articles?task_id=12&per_page=20"
```

Create article from markdown:

```bash
"/path/to/workspace/bin/geoflow" --config /path/to/config article create \
  --title "标题" \
  --content-file ./article.md \
  --task-id 12 \
  --author-id 5 \
  --category-id 2 \
  --idempotency-key article-create-001
```

Create article from JSON:

```bash
"/path/to/workspace/bin/geoflow" --config /path/to/config article create --json ./article.json --idempotency-key article-create-001
```

Update article:

```bash
"/path/to/workspace/bin/geoflow" --config /path/to/config article update 101 --json ./article-patch.json --idempotency-key article-update-101
```

Review article:

```bash
"/path/to/workspace/bin/geoflow" --config /path/to/config article review 101 --status approved --note "pass" --idempotency-key article-review-101
```

Publish article:

```bash
"/path/to/workspace/bin/geoflow" --config /path/to/config article publish 101 --idempotency-key article-publish-101
```

Then verify persisted state:

```bash
"/path/to/workspace/bin/geoflow" --config /path/to/config article get 101
```

Then verify the final frontend URL using `/article/{slug}` from the persisted article slug or the page's canonical URL. For this system the slug should be an 8-character short ASCII token. Do not return `article.php?id=...` as the published URL.

Trash article:

```bash
"/path/to/workspace/bin/geoflow" --config /path/to/config article trash 101 --idempotency-key article-trash-101
```
