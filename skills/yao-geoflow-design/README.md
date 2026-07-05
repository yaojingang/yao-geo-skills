<!--
Copyright © 2026 姚金刚. All rights reserved.
Project: yao-geoflow-design
Created by: 姚金刚
Date: 2026-05-16
X: https://x.com/yaojingang
-->

# Yao GEOFlow Design

`yao-geoflow-design` is a local skill for discovering GEOFlow Laravel Blade themes, selecting a target theme, creating preview-first edit sessions, and then optimizing or refining the chosen frontend through safe theme packages.

It also understands the current GEOFlow homepage builder contract. When `HomepageModuleBuilder`, `homepage_modules`, `homepage_style`, and the admin import route are available, the skill can produce reviewed `homepage-design.json` payloads for multi-module homepages and custom homepage styles instead of forcing Blade-only edits.

As of the 2026-07-05 update, this is the primary skill for GEOFlow frontend experience design. It supports default-site `lead_form` homepage conversion modules by referencing an existing active `lead_form_slug`, and it treats GeoFlow Agent target-package module support as a separate remote capability check.

## Primary Use

- inventory GEOFlow frontend modules, variables, and rendering boundaries
- discover existing themes in `resources/views/theme` for the current Laravel GEOFlow workspace
- select a target theme and prepare a preview edit fork before touching live theme files
- inspect a reference URL and extract reusable visual direction
- map reference style tokens onto GEOFlow's existing frontend modules
- audit the target theme for hierarchy, spacing, responsive, and module-consistency issues
- enrich the default homepage with hero/media, chart-lite, metric, text, service/category, resource/case, large visual, and CTA modules using existing GEOFlow data
- add default-site conversion sections with `lead_form` modules when an active lead form already exists
- generate importable homepage builder JSON with `style` and `modules` for supported multi-module homepage and custom style changes
- compare default-site module types against target-package `frontend-capabilities` and downgrade unsupported `lead_form` modules to CTA/link fallbacks
- generate either a full theme package, a preview edit session, or an incremental optimization patch plan
- prepare the system-facing integration plan for preview, confirmation, replacement, or publish-as-new flows
- preserve SEO/schema slots, markdown-rendered HTML, image-caption behavior, footer rules, and configurable admin base paths while editing themes

## Boundary

This skill does not directly deploy a template to production, rewrite GEOFlow backend business logic, or replace current data contracts with arbitrary copied HTML. It works by preserving GEOFlow's Laravel Blade frontend modules and variables while changing presentation-layer structure and styles in a controlled preview session or theme package.

It also does not hard-code `/geo_admin`, add independent public language switching, create lead-form backend/admin records, or change controllers/routes/database queries during a design-only run.

## Package Map

- `SKILL.md`: trigger boundary and execution workflow
- `agents/interface.yaml`: canonical interface metadata
- `agents/openai.yaml`: OpenAI-friendly interface metadata
- `references/geoflow-frontend-map.md`: current frontend module, variable, and function contract
- `references/laravel-theme-contract.md`: current Laravel Blade theme package and preview contract
- `references/template-boundary.md`: system boundary for safe template cloning and current-template optimization
- `references/homepage-composition-guide.md`: safe homepage enrichment patterns for enterprise, portal, and content-hub front pages
- `homepage-design.json`: expected artifact when the current system supports homepage module builder import
- `references/theme-package-contract.md`: expected output format for generated theme packages, preview edit sessions, and optimization passes
- `references/design-optimization-playbook.md`: optimization-mode workflow and heuristics
- `references/theme-edit-workflow.md`: target-theme discovery, preview-fork editing, and finalize workflow
- `templates/homepage-design-template.json`: canonical builder payload example for homepage modules and style tokens
- `evals/trigger_cases.json`: trigger boundary checks
- `reports/geoflow-skill-upgrade-2026-07-05.md`: current upgrade evidence and validation notes
- `reports/intent-dialogue.md`: captured job framing
- `reports/reference-scan.md`: local-fit reference notes
- `reports/iteration-directions.md`: next engineering moves
