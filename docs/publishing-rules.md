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
- secrets, account traces, and private client data are absent
- repository docs still match the actual structure
- skill-level eval files exist for any new skill

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

PR descriptions should cover:

- what changed
- why it changed
- impact on future skill packages
- validation performed

## GitHub Push Flow

1. Review `git status` and confirm the scope.
2. Stage only intended files.
3. Commit with a terse message.
4. Push to the correct branch.
5. Open a PR if the change is not a bootstrap or tiny maintenance edit.

## Public Repository Safety

Never push:

- API keys
- local caches
- `outputs/` artifacts from real client work
- internal benchmark documents without permission
- private URLs that should not be public

## Registry Update Rule

Any new public skill should update `registry/skills.json` in the same change set so the repository inventory remains accurate.
