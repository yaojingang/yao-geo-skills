---
name: geoflow-cli-ops
description: Operate an existing GEOFlow system through the local geoflow CLI to inspect catalog data, create or update tasks, enqueue generation jobs, upload article drafts, review content, and publish articles. Use when the user wants CLI-based GEOFlow operations instead of the web admin, especially for task automation, article upload, bulk publish flows, or skill-driven local control. Do not use for backend implementation, schema changes, or direct database edits.
---

# GEOFlow CLI Ops

Use this skill when the system already has the GEOFlow API and `bin/geoflow` CLI available, and the job is to operate that system from local commands.

## What This Skill Owns

- GEOFlow CLI preflight checks
- Catalog lookup for model, prompt, title library, author, category, and knowledge-base IDs
- Task creation, update, start, stop, enqueue, and status inspection
- Job inspection after enqueue or worker execution
- Article draft upload, article update, review, publish, and trash actions
- Safe command construction with idempotency keys for write operations

## What This Skill Does Not Cover

- Implementing or refactoring GEOFlow backend code
- Direct database writes or bypassing `/api/v1`
- Web-admin-only flows that do not exist in `geoflow`
- URL import, title async generation, or image upload orchestration outside the current CLI surface
- Debugging worker internals beyond reporting what the CLI and API return

## Required Preconditions

1. Confirm the target workspace contains `bin/geoflow`.
2. Confirm the CLI can resolve config via `--config`, env vars, or the default config path.
3. If no config exists yet, ask the user for the GEOFlow address and administrator username, then run `geoflow login`. Let the CLI prompt for the password instead of echoing it in plain text.
4. If config exists but any authenticated read returns `401`/`403` or token-invalid errors, rerun `geoflow login --force` instead of treating the workspace as already logged in.
5. Run the bundled preflight script before the first mutating action in a new workspace.
6. Treat preflight as successful only when an authenticated read succeeds. `config show` alone is not enough because it only proves local config parsing, not API reachability or token validity.
7. If preflight fails, stop and report the exact missing prerequisite instead of guessing.

Use [references/operation-boundary.md](references/operation-boundary.md) for the enforced boundary and [references/command-map.md](references/command-map.md) for the supported commands.

## Default Workflow

1. Identify the target GEOFlow workspace. If the user did not specify one, prefer the current workspace when it contains `bin/geoflow`.
2. If config is missing, run `bin/geoflow login --base-url ... --username ...` and let the CLI prompt for the password.
3. If config exists, run an authenticated read such as `catalog` immediately. If it returns `401`, `403`, or token-invalid output, run `bin/geoflow login --base-url ... --username ... --force`.
4. Run `scripts/geoflow_preflight.sh "<workspace>" [config]` to verify the CLI entrypoint, authenticated API access, and current token.
5. For lookup work, call `geoflow catalog` first so IDs come from the system instead of memory.
6. For write operations, use an explicit `--idempotency-key`.
7. After any write, immediately run the corresponding read command to verify the actual persisted state.
8. After `article publish`, verify the final user-facing frontend URL using the system's slug route, not an `article.php?id=...` compatibility link. Treat `/article/{slug}` as the publish URL and prefer the canonical URL when the page exposes one.
9. For this system, the publish URL must use an 8-character short ASCII slug such as `/article/bc7af3fb`. If the persisted slug does not match that shape, treat it as a URL-rule mismatch and report it.
10. If a generation job fails, separate CLI/API success from business-data failure. Example: missing titles is a task-data issue, not a CLI issue.
11. If the user asked for a publish smoke test and task generation is blocked by business data such as missing titles, stop the affected task first when it is still active or queued, then fall back to `article create` + `article review` + `article publish` so the publish chain can still be validated without leaving noisy retries behind.
12. Report commands run, resource IDs touched, and the resulting state in concise operational terms.

## Command Discipline

- Prefer direct executable invocation:

```bash
"/path/to/workspace/bin/geoflow" --config /path/to/config ...
```

- If the file is not executable but exists, fall back to:

```bash
php "/path/to/workspace/bin/geoflow" --config /path/to/config ...
```

- Never synthesize API requests directly when the CLI already supports the action.
- Never store or print a full token in the final user-facing summary unless the user explicitly asked for it.

## Typical Flows

### 1. Inspect available resources

```bash
"/path/to/workspace/bin/geoflow" --config /path/to/config catalog
```

### 2. Create and run a task

```bash
"/path/to/workspace/bin/geoflow" --config /path/to/config task create --json ./task.json --idempotency-key task-create-001
"/path/to/workspace/bin/geoflow" --config /path/to/config task start 12 --idempotency-key task-start-12
"/path/to/workspace/bin/geoflow" --config /path/to/config task enqueue 12 --idempotency-key task-enqueue-12
"/path/to/workspace/bin/geoflow" --config /path/to/config job get 88
```

### 3. Upload and publish an article

```bash
"/path/to/workspace/bin/geoflow" --config /path/to/config article create --title "标题" --content-file ./article.md --task-id 12 --author-id 5 --category-id 2 --idempotency-key article-create-001
"/path/to/workspace/bin/geoflow" --config /path/to/config article review 101 --status approved --note "CLI review pass" --idempotency-key article-review-101
"/path/to/workspace/bin/geoflow" --config /path/to/config article publish 101 --idempotency-key article-publish-101
```

Then verify both:

- the article state through `article get 101`
- the final frontend URL using `/article/{slug}` with the persisted 8-character short slug

### 4. Fallback when task generation is blocked by business data

If `task jobs` or `job get` shows a business-data failure such as `没有可用的标题`, do not keep retrying the task as though the CLI were broken. If the user only needs a publish-path smoke test, stop the task first, then create a direct draft article instead:

```bash
"/path/to/workspace/bin/geoflow" --config /path/to/config task stop 12 --idempotency-key task-stop-12
"/path/to/workspace/bin/geoflow" --config /path/to/config article create \
  --title "测试文章" \
  --content-file ./article.md \
  --author-id 5 \
  --category-id 2 \
  --status draft \
  --review-status pending \
  --idempotency-key article-create-smoke-001
"/path/to/workspace/bin/geoflow" --config /path/to/config article review 101 --status approved --note "CLI smoke test" --idempotency-key article-review-101
"/path/to/workspace/bin/geoflow" --config /path/to/config article publish 101 --idempotency-key article-publish-101
```

## Response Rules

- When the user asks to operate GEOFlow, do the work through the CLI instead of just describing commands.
- If the user has not logged in yet, guide them through `geoflow login` first instead of asking them to create a token manually.
- If authenticated reads fail because the token is invalid or expired, treat that as a login problem and refresh with `geoflow login --force`.
- If authenticated reads fail for another reason, do not default to `login --force`; report the actual API or connectivity failure first.
- If the request implies batch operations, still keep each write idempotent and verify a sample of the outputs.
- Do not invent a frontend article URL rule from memory. Read the system's current routing or canonical behavior first, then return the final `/article/{slug}` URL with the persisted 8-character short slug, not a temporary `article.php?id=...` entrypoint.
- If the user asks for automation or a reusable flow, finish the operation first, then suggest whether an additional skill or automation is warranted.

## Reference Map

- Read [references/operation-boundary.md](references/operation-boundary.md) for safety and scope.
- Read [references/command-map.md](references/command-map.md) for CLI-to-capability mapping.
- Use [scripts/geoflow_preflight.sh](scripts/geoflow_preflight.sh) before mutating a new workspace.
- Inspect [evals/trigger_cases.json](evals/trigger_cases.json) when tightening or reviewing the trigger boundary.
- If you need the underlying CLI semantics, read the public project doc:
  [GEOFlow CLI Guide](https://github.com/yaojingang/GEOFlow/blob/main/docs/project/GEOFLOW_CLI.md)
