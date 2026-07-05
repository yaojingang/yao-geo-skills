# yao-geoflow-design

`yao-geoflow-design` is the primary frontend-experience skill for current GEOFlow systems. It discovers Laravel Blade themes, plans default-site homepage modules, designs reviewed `homepage-design.json`, handles `lead_form` conversion modules bound to existing active forms, maps reference sites, compares default-site and target-package frontend capabilities, and keeps preview, import, sync, and activation as separate confirmation steps.

This version is aligned with the GEOFlow Laravel Blade theme system, homepage builder, live theme editor, and channel frontend-capability surfaces. Theme packages live under `resources/views/theme/{theme_id}`, runtime assets commonly live under `public/themes/{theme_id}`, missing templates fall back to `resources/views/site`, and the admin base path is configurable. The skill must not hard-code `/geo_admin` or alter backend business logic during a design-only run.

## What It Is For

- discovering existing GEOFlow themes and their editable files
- selecting a target theme and creating a preview edit fork before any live mutation
- mapping GEOFlow frontend modules, variables, and rendering boundaries
- extracting visual tokens, layout patterns, and module treatment from a reference URL
- translating that direction into GEOFlow homepage, category, article, archive, and ad-slot modules
- auditing the current template for hierarchy, spacing, and consistency issues
- adjusting width, weight, spacing, and safe display modules inside a selected preview theme
- enriching the default homepage into a corporate, portal, or knowledge-hub front page with hero media, metrics, CSS-only charts, text/value blocks, service/topic blocks, case/resource modules, and CTAs
- using existing homepage data such as `homepageCarouselSlides`, `hotArticles`, `featuredArticles`, `articles`, `cardSummaries`, and site copy instead of inventing backend content
- generating importable homepage builder JSON with `style` and `modules`, including supported types such as `hero`, `rich_text`, `image_band`, `metric_band`, `chart_band`, `feature_grid`, `article_collection`, `cta_band`, `lead_form`, and sanitized `custom_html`
- using `lead_form_slug` only for an existing active lead form; this skill does not create the form
- comparing default-site supported modules with target-package frontend capabilities before channel sync
- downgrading unsupported `lead_form` modules to CTA/link or requiring a target package upgrade
- checking article images, markdown-rendered HTML, SEO/schema slots, footer behavior, and public language behavior against the current contract
- preparing safe preview-first theme packages or optimization patch packages for later publication or replacement

## What It Is Not For

- copying raw HTML page-by-page
- bypassing GEOFlow's current data and function contract
- implementing lead-form CRUD, migrations, API endpoints, or submission handling
- inventing customer logos, sales-funnel metrics, corporate proof, or chart data when the current view does not provide them
- applying `homepage_modules` imports or homepage presets to the live homepage without review
- silently syncing unsupported `lead_form` modules into older target packages
- pushing a reference design live without preview
- changing backend logic, routing, SEO rules, or content-query behavior
- hard-coding admin URLs, database queries, or independent language-switch logic inside a theme

## Package Links

- Skill package: [skills/yao-geoflow-design](../../skills/yao-geoflow-design)
- Trigger boundary: [trigger_cases.json](../../skills/yao-geoflow-design/evals/trigger_cases.json)
- Frontend map: [geoflow-frontend-map.md](../../skills/yao-geoflow-design/references/geoflow-frontend-map.md)
- Theme contract: [theme-package-contract.md](../../skills/yao-geoflow-design/references/theme-package-contract.md)
- Laravel Blade contract: [laravel-theme-contract.md](../../skills/yao-geoflow-design/references/laravel-theme-contract.md)
- Homepage composition guide: [homepage-composition-guide.md](../../skills/yao-geoflow-design/references/homepage-composition-guide.md)
- Optimization playbook: [design-optimization-playbook.md](../../skills/yao-geoflow-design/references/design-optimization-playbook.md)
- Theme edit workflow: [theme-edit-workflow.md](../../skills/yao-geoflow-design/references/theme-edit-workflow.md)
- Channel frontend contract: [channel-frontend-contract.md](../../skills/yao-geoflow-design/references/channel-frontend-contract.md)
- Upgrade report: [geoflow-skill-upgrade-2026-07-05.md](../../skills/yao-geoflow-design/reports/geoflow-skill-upgrade-2026-07-05.md)
- Example mapping report: [qiaomu-blog-mapping-2026-04-18.md](../../skills/yao-geoflow-design/reports/qiaomu-blog-mapping-2026-04-18.md)
- Public project: [GEOFlow](https://github.com/yaojingang/GEOFlow)
