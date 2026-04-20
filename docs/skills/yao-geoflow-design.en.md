# yao-geoflow-design

`yao-geoflow-design` maps a reference site into a **GEOFlow-compatible theme package plan** and can also optimize the current GEOFlow template through preview-first design passes. It does not replace the live frontend directly. Instead, it produces theme or optimization artifacts that can later be wired into GEOFlow.

## What It Is For

- mapping GEOFlow frontend modules, variables, and rendering boundaries
- extracting visual tokens, layout patterns, and module treatment from a reference URL
- translating that direction into GEOFlow homepage, category, article, archive, and ad-slot modules
- auditing the current template for hierarchy, spacing, and consistency issues
- preparing safe preview-first theme packages or optimization patch packages for later activation

## What It Is Not For

- copying raw HTML page-by-page
- bypassing GEOFlow's current data and function contract
- pushing a reference design live without preview
- changing backend logic, routing, SEO rules, or content-query behavior

## Package Links

- Skill package: [skills/yao-geoflow-design](../../skills/yao-geoflow-design)
- Trigger boundary: [trigger_cases.json](../../skills/yao-geoflow-design/evals/trigger_cases.json)
- Frontend map: [geoflow-frontend-map.md](../../skills/yao-geoflow-design/references/geoflow-frontend-map.md)
- Theme contract: [theme-package-contract.md](../../skills/yao-geoflow-design/references/theme-package-contract.md)
- Optimization playbook: [design-optimization-playbook.md](../../skills/yao-geoflow-design/references/design-optimization-playbook.md)
- Example mapping report: [qiaomu-blog-mapping-2026-04-18.md](../../skills/yao-geoflow-design/reports/qiaomu-blog-mapping-2026-04-18.md)
- Public project: [GEOFlow](https://github.com/yaojingang/GEOFlow)
