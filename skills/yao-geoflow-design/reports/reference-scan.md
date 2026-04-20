# Reference Scan

## Local Reference 1: `yao-meta-skill`

Why inspected:
- the user explicitly asked to use it as the refactor model
- to align route description, evidence split, and quality-gate selection
- to decide whether this package should stay compact or move detail into references and scripts

What to borrow:
- compact `SKILL.md` plus deeper `references/` and deterministic `scripts/`
- mode-aware quality gates with reports and evals as evidence
- a larger context budget when the package owns multiple safe workflows

What not to borrow:
- generic skill-authoring language inside the runtime route description
- meta-skill framing that hides GEOFlow-specific operational boundaries

## Local Reference 2: `yao-geoflow-cli`

Why inspected:
- to match local skill packaging conventions
- to reuse the same sibling-skill skeleton style
- to keep the boundary between theme work and CLI ops explicit

What to borrow:
- compact `SKILL.md` with hard boundary
- `agents/interface.yaml` plus `agents/openai.yaml`
- `manifest.json`
- explicit trigger eval file

What not to borrow:
- CLI-operation ownership
- system-operation boundary that assumes `bin/geoflow`

## Local Reference 3: Current GEOFlow frontend

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

## Local Reference 4: Current GEOFlow theme system

Why inspected:
- the requested workflow is not just template planning anymore; it must run against the current theme system
- existing preview URLs, theme discovery, and admin activation should be reused instead of reinvented

Files inspected:
- `includes/theme_preview.php`
- `theme-preview.php`
- `router.php`
- `admin/site-settings.php`
- `themes/qiaomu-editorial-20260418/...`

What to borrow:
- `/themes/<theme-id>` as the authoritative theme package location
- preview URLs under `/preview/<theme-id>/...`
- admin theme discovery and post-review activation flow
- real editable surface inside `templates/*.php`, `assets/theme.css`, and theme manifests

What not to borrow:
- backup directories inside `/themes`
- runtime-only assumptions that depend on a live database connection being available during packaging

## Design Decision

This package should keep a `production` archetype with a `library` context budget:

- the route can be confused with generic frontend design, `yao-geoflow-template`, GEOFlow CLI ops, or direct system implementation
- the skill now owns theme discovery, preview-session creation, target-theme editing, and finalize branching
- the package should stay compact at the route level, but it needs deterministic helpers and explicit eval coverage
- the current GEOFlow codebase already has a preview and theme-selection system, so the skill should integrate with it instead of inventing detached packaging rules
