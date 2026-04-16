# Publishing Rules

This document defines how `yao-geo-skills` should be published and pushed to GitHub.

## Repository-Level Rules

- The canonical public repository is `yaojingang/yao-geo-skills`.
- `main` is the stable public branch.
- Direct push to `main` is allowed only for repository bootstrap and very small maintenance updates.
- New skills, large refactors, and policy changes should go through a pull request.

## Pre-Push Checklist

Before pushing, confirm:

- the change is in scope
- generated outputs are not accidentally committed
- public examples are sanitized and intentionally committed
- secrets, account traces, and private client data are absent
- repository docs still match the actual structure
- skill-level eval files exist for any new skill
- `registry/skills.json` is updated for any new or renamed public skill
- a human-facing guide exists under `docs/skills/` for any new public skill

## Commit Rules

- Use short, scope-first commit messages
- Prefer formats like:
  - `bootstrap yao-geo-skills`
  - `add geo-keyword-discovery scaffold`
  - `tighten eval policy`

## Branch Rules

- Bootstrap can start on `main`
- Normal feature work should use `codex/<topic>`
- Keep one topic per branch

## PR Rules

Create a PR when the change:

- adds a new skill
- changes repository policy
- changes shared schemas or rubrics
- changes evaluation thresholds
- changes repository validation scripts or GitHub Actions

PR descriptions should cover:

- what changed
- why it changed
- impact on future skill packages
- validation performed

For public-facing GEO skills, also include:

- whether examples are sanitized
- whether screenshots are intentionally committed
- whether the guide and README navigation were updated

## GitHub Push Flow

1. Review `git status` and confirm the scope.
2. Stage only intended files.
3. Run repository validation before pushing.
4. Commit with a terse message.
5. Push to the correct branch.
6. Open a PR if the change is not a bootstrap or tiny maintenance edit.

## Public Repository Safety

Never push:

- API keys
- local caches
- `outputs/` artifacts from real client work
- unsanitized example materials
- internal benchmark documents without permission
- private URLs that should not be public

## Registry Update Rule

Any new public skill should update `registry/skills.json` in the same change set so the repository inventory remains accurate.

## CI Enforcement

The repository should keep a GitHub Actions workflow that checks:

- required top-level policy files exist
- `registry/skills.json` is valid JSON and follows the repository contract
- public skill packages contain required files
- committed `outputs/` directories are rejected
- public skills are synchronized with the registry
