# Yao GEOFlow Template

`yao-geoflow-template` maps a reference site into a **GEOFlow-compatible theme package plan**. It does not replace the live frontend directly. Instead, it produces `tokens.json`, `mapping.json`, `manifest.json`, and a preview-first theme package structure that can later be wired into GEOFlow.

## What It Is For

- mapping GEOFlow frontend modules, variables, and rendering boundaries
- extracting visual tokens, layout patterns, and module treatment from a reference URL
- translating that direction into GEOFlow homepage, category, article, archive, and ad-slot modules
- preparing safe preview-first theme packages for later activation

## What It Is Not For

- copying raw HTML page-by-page
- bypassing GEOFlow's current data and function contract
- pushing a reference design live without preview
- changing backend logic, routing, SEO rules, or content-query behavior

## Standard Package Contract

A committed public example should be reviewable from a fresh checkout. The
minimum standardized package shape is:

- `examples/<example-id>/README.md`
- `preview/<example-id>/package/tokens.json`
- `preview/<example-id>/package/mapping.json`
- `preview/<example-id>/index.html`
- `preview/<example-id>/category.html`
- `preview/<example-id>/article.html`
- `preview/<example-id>/archive.html`

`tokens.json` records package identity, source reference, creation date,
compatible system, visual direction, and token groups. `mapping.json` records
route coverage, module mapping, safe boundaries, and committed preview routes.

Reviewer checklist:

- package metadata is committed and parses as JSON
- preview files do not depend on ignored `outputs/` or `outputs-demo/` paths
- omitted routes or modules are explicit
- preview readiness is separate from production activation readiness

## Preview Readiness Vs Production Activation Readiness

`preview-only` means the package can be reviewed from committed metadata and
committed preview routes. It does not mean the package is approved for live
traffic, routing changes, SEO changes, backend query changes, or production
template selection.

Production activation requires a separate activation request, spec, or
implementation plan owned by the GEOFlow project. `yao-geoflow-template` should
not set `activation_status` beyond `preview-only` unless that activation
workflow is linked and reviewable.

Out-of-scope activation work includes:

- live route or URL rewrites
- SEO contract, canonical, sitemap, or structured-data changes
- backend schema, content-query, or data-fetching changes
- deployment state, rollout flags, cache purge, or production template switches

## Package Links

- Skill package: [skills/yao-geoflow-template](../../skills/yao-geoflow-template)
- Trigger boundary: [trigger_cases.json](../../skills/yao-geoflow-template/evals/trigger_cases.json)
- Frontend map: [geoflow-frontend-map.md](../../skills/yao-geoflow-template/references/geoflow-frontend-map.md)
- Theme contract: [theme-package-contract.md](../../skills/yao-geoflow-template/references/theme-package-contract.md)
- Example mapping report: [qiaomu-blog-mapping-2026-04-18.md](../../skills/yao-geoflow-template/reports/qiaomu-blog-mapping-2026-04-18.md)
- Public project: [GEOFlow](https://github.com/yaojingang/GEOFlow)
