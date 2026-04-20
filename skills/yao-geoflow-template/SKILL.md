---
name: yao-geoflow-template
description: Analyze the current GEOFlow frontend contract, map a reference URL onto GEOFlow's existing frontend modules, and prepare a preview-first template package plan for homepage, category, article, archive, and ad-slot UI replacement without changing business logic or data contracts. Use when the user wants GEOFlow frontend template cloning, UI template packaging, page-style replication from a reference site, or a GEOFlow-compatible theme/module map. Do not use for generic frontend redesign, arbitrary HTML copying, backend refactors, or direct production template activation.
---

# Yao GEOFlow Template

Use this skill when the job is to turn a visual reference into a GEOFlow-compatible frontend template plan while preserving the system's existing data model, rendering contract, and page responsibilities.

## What This Skill Owns

- GEOFlow frontend module inventory
- GEOFlow frontend variable and function mapping
- reference-site style and token extraction planning
- module-to-module mapping from a reference site to GEOFlow frontend pages
- preview-first theme package design
- system integration planning for template registration and activation

## What This Skill Does Not Cover

- direct deployment of a new frontend into production
- backend implementation of template activation unless explicitly requested
- arbitrary page scraping and raw HTML copying
- replacing GEOFlow data queries with hard-coded content
- changing routing, SEO contracts, or article/category data rules

## Required Preconditions

1. Confirm the target workspace is a GEOFlow codebase with `index.php`, `article.php`, `category.php`, `archive.php`, and `includes/header.php`.
2. Read the GEOFlow frontend contract in [references/geoflow-frontend-map.md](references/geoflow-frontend-map.md) before proposing any clone plan.
3. Preserve the existing module/data contract unless the user explicitly asks for a system change.
4. Treat preview and activation as separate steps. A cloned template should be previewed before it is considered for activation.

## Default Workflow

1. Identify the GEOFlow workspace and confirm the canonical frontend files.
2. Read [references/geoflow-frontend-map.md](references/geoflow-frontend-map.md) to understand current modules, variables, and rendering boundaries.
3. Read [references/template-boundary.md](references/template-boundary.md) to separate safe style replacement from prohibited contract changes.
4. If a reference URL is provided, inspect its visual tokens and layout patterns.
5. Map the reference site's style direction onto GEOFlow's stable modules rather than copying full pages verbatim.
6. Produce a theme package that targets:
   - homepage
   - category page
   - article detail page
   - archive page
   - header / footer
   - article detail ad block
7. When helpful, emit concrete package artifacts:
   - `outputs/<template-id>/tokens.json`
   - `outputs/<template-id>/mapping.json`
   - `outputs/<template-id>/manifest.json`
   - `preview/<template-id>/...` preview pages
8. Prefer a preview URL over prose-only output when the user wants to inspect the mapped style.
9. Keep output preview-first. Activation should only happen after review and explicit confirmation.
10. If the user asks for system implementation later, use the generated package and contract as the source of truth for the GEOFlow-side template feature.

## Response Rules

- When the user asks for template cloning, begin from GEOFlow's existing frontend contract, not from generic redesign advice.
- Always state which modules can be restyled safely and which contracts must remain fixed.
- Prefer module mapping, design tokens, and theme package structure over raw HTML replacement.
- If a requested reference site pattern conflicts with GEOFlow's data contract, say so and offer the closest compatible mapping.

## Reference Map

- Read [references/geoflow-frontend-map.md](references/geoflow-frontend-map.md) for the authoritative frontend module and variable map.
- Read [references/template-boundary.md](references/template-boundary.md) for safe/unsafe modification boundaries.
- Read [references/theme-package-contract.md](references/theme-package-contract.md) for the expected output of a clone run.
