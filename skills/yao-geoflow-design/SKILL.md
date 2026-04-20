---
name: yao-geoflow-design
description: Clone or optimize GEOFlow frontends by mapping reference sites or refining the current template without changing business logic or data contracts. Use for cloning, optimization, and theme iteration. Not for generic redesign, raw HTML copying, backend refactors, or direct activation.
---

# Yao GEOFlow Design

Use this skill to clone or improve a GEOFlow frontend without breaking its rendering contract.

## What This Skill Owns

- GEOFlow frontend contract mapping
- reference-site cloning into GEOFlow-compatible modules
- current-template optimization and incremental design adjustment
- preview-first theme packages and optimization passes

## What This Skill Does Not Cover

- direct deployment of a new frontend into production
- arbitrary page scraping and raw HTML copying
- changing GEOFlow data queries, routing, or SEO contracts

## Required Preconditions

1. Confirm the target workspace is a GEOFlow codebase with `index.php`, `article.php`, `category.php`, `archive.php`, and `includes/header.php`.
2. Read [references/geoflow-frontend-map.md](references/geoflow-frontend-map.md) and [references/template-boundary.md](references/template-boundary.md) before proposing changes.
3. Preserve the existing module/data contract unless the user explicitly asks for a system change.
4. Choose a work mode:
   - `clone`: map a reference site into GEOFlow-compatible templates
   - `optimize`: improve the current GEOFlow template with incremental design changes
   - `hybrid`: use a reference site to guide current-template optimization
5. Treat preview and activation as separate steps. A cloned or optimized template should be previewed before it is considered for activation.

## Default Workflow

1. Identify the GEOFlow workspace and confirm the canonical frontend files.
2. Decide whether the request is `clone`, `optimize`, or `hybrid`.
3. For `clone` or `hybrid`, inspect the reference URL for tokens and layout rhythm.
4. For `optimize` or `hybrid`, audit the current template for hierarchy, spacing, density, responsiveness, and ad tone.
5. Map the design direction onto stable GEOFlow modules: `header`, `footer`, `home`, `category`, `article`, `archive`, `article.sticky_ad`.
6. Output one of:
   - full theme package: `tokens.json`, `mapping.json`, `manifest.json`, preview pages
   - optimization pass: `design-audit.md`, `tokens.delta.json`, `mapping.delta.json`, `change-plan.md`, preview notes
7. Call out safe restyle surface vs fixed contracts before activation.

## Reference Map

- [references/geoflow-frontend-map.md](references/geoflow-frontend-map.md): authoritative frontend module and variable map
- [references/template-boundary.md](references/template-boundary.md): safe and unsafe modification boundaries
- [references/theme-package-contract.md](references/theme-package-contract.md): expected output shape for clone and optimize modes
- [references/design-optimization-playbook.md](references/design-optimization-playbook.md): optimization heuristics and preferred outputs
