# Operation Boundary

This skill is for operating a running GEOFlow system, not for developing the system itself.

## Allowed Actions

- Run `bin/geoflow` commands when the CLI exists
- Use Laravel `/api/v1` fallback when the current GEOFlow rewrite has no CLI wrapper
- Read command output
- Build JSON payload files when needed for `task create`, `task update`, or `article create`
- Inspect resulting task, job, and article state through the CLI

## Disallowed Actions

- Direct SQL against the project database
- Editing backend PHP just to complete an operations request
- Replacing the CLI with raw `curl` when the CLI exists and already supports the action
- Exposing a full bearer token in user-facing summaries

## Required Checks

Before the first mutating command in a workspace:

1. Verify whether `bin/geoflow` exists. If it does not, verify the workspace is a Laravel GEOFlow app with `artisan` and `routes/api.php`.
2. If CLI configuration is missing, run `geoflow login` first. If using API fallback, obtain a bearer token through `/api/v1/auth/login` or the provided token source.
3. If configuration exists but authenticated reads return `401`, `403`, or token-invalid output, refresh login/token.
4. If authenticated reads fail for another reason, report that failure instead of assuming login is the fix.
5. Verify the CLI resolves configuration, or verify the API base URL responds.
6. Verify an authenticated read such as `catalog` succeeds. `config show` or a public homepage check by itself is not sufficient.

After any mutating command:

1. Re-read the target resource.
2. Report the final persisted state.
3. If the action triggered a background job, inspect the job separately.
4. If the action published an article, verify the final frontend URL and report the `/article/{slug}` route rather than an `article.php?id=...` compatibility link.
5. For this system, the final article slug should be an 8-character short ASCII token such as `bc7af3fb`.

## Error Interpretation

Keep these failure classes separate:

- CLI/runtime failure: command missing, config missing, permission problem, malformed args
- API fallback setup failure: missing `GEOFLOW_BASE_URL`, missing bearer token, wrong `/api/v1` base path
- API failure: 401, 403, 404, 409, 422, 500
- Business-data failure: task inactive, missing titles, invalid category, review state conflict

Do not conflate a downstream job-data failure with a CLI failure.
If a task is blocked by business data and the user only needs a publish smoke test, stop the task before switching to a direct article-create fallback.
