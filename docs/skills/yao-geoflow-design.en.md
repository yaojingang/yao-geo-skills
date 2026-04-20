# yao-geoflow-design

`yao-geoflow-design` discovers the themes that already exist in a GEOFlow system, lets the operator pick a target theme, and then runs a **preview-first theme edit session** for frontend adjustments, module changes, or reference-guided restyling. It does not replace the live frontend directly. Instead, it creates an in-system preview theme first, then supports either publish-as-new or replace-base decisions after review.

## What It Is For

- discovering existing GEOFlow themes and their editable files
- selecting a target theme and creating a preview edit fork before any live mutation
- mapping GEOFlow frontend modules, variables, and rendering boundaries
- extracting visual tokens, layout patterns, and module treatment from a reference URL
- translating that direction into GEOFlow homepage, category, article, archive, and ad-slot modules
- auditing the current template for hierarchy, spacing, and consistency issues
- adjusting width, weight, spacing, and safe display modules inside a selected preview theme
- preparing safe preview-first theme packages or optimization patch packages for later publication or replacement

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
- Theme edit workflow: [theme-edit-workflow.md](../../skills/yao-geoflow-design/references/theme-edit-workflow.md)
- Example mapping report: [qiaomu-blog-mapping-2026-04-18.md](../../skills/yao-geoflow-design/reports/qiaomu-blog-mapping-2026-04-18.md)
- Public project: [GEOFlow](https://github.com/yaojingang/GEOFlow)
