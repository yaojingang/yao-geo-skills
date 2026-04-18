# geoflow-template

`geoflow-template` maps a reference site into a **GEOFlow-compatible theme package plan**. It does not replace the live frontend directly. Instead, it produces `tokens.json`, `mapping.json`, `manifest.json`, and a preview-first theme package structure that can later be wired into GEOFlow.

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

## Package Links

- Skill package: [skills/geoflow-template](../../skills/geoflow-template)
- Trigger boundary: [trigger_cases.json](../../skills/geoflow-template/evals/trigger_cases.json)
- Frontend map: [geoflow-frontend-map.md](../../skills/geoflow-template/references/geoflow-frontend-map.md)
- Theme contract: [theme-package-contract.md](../../skills/geoflow-template/references/theme-package-contract.md)
- Example mapping report: [qiaomu-blog-mapping-2026-04-18.md](../../skills/geoflow-template/reports/qiaomu-blog-mapping-2026-04-18.md)
- Public project: [GEOFlow](https://github.com/yaojingang/GEOFlow)
