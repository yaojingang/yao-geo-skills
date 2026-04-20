# Reference Scan

## Local Reference 1: `geoflow-cli-ops`

Why inspected:
- to match local skill packaging conventions
- to reuse the same production-archetype skeleton style

What to borrow:
- compact `SKILL.md` with hard boundary
- `agents/interface.yaml` plus `agents/openai.yaml`
- `manifest.json`
- explicit trigger eval file

What not to borrow:
- CLI-operation ownership
- system-operation boundary that assumes `bin/geoflow`

## Local Reference 2: Current GEOFlow frontend

Why inspected:
- the new skill depends on the actual frontend contract rather than abstract redesign theory

Files inspected:
- `index.php`
- `article.php`
- `category.php`
- `archive.php`
- `includes/header.php`
- `includes/footer.php`
- `includes/functions.php`
- `includes/seo_functions.php`
- `router.php`

What to borrow:
- page/module decomposition
- stable helper-function contract
- route and SEO invariants
- article detail ad slot structure

What not to borrow:
- legacy or archived prototype pages
- test and backup files

## Design Decision

This package should be a `production` archetype:

- the route can be confused with generic frontend design, `geoflow-template`, or GEOFlow CLI ops
- the skill needs one authoritative frontend contract reference
- the package should stay compact, but it must defend its boundary clearly
- the package must separate `clone`, `optimize`, and `hybrid` jobs early so outputs do not drift
