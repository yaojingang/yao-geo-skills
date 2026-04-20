---
name: yao-geoflow-design
description: Discover, preview, clone, and edit GEOFlow themes by selecting an existing template or mapping a reference site, then applying safe frontend changes without changing business logic or data contracts. Use for theme discovery, target-theme editing, cloning, optimization, and theme iteration. Not for raw HTML copying, backend refactors, or direct live activation.
---

# Yao GEOFlow Design

Use this skill to discover, preview, clone, or improve a GEOFlow frontend without breaking its rendering contract.

## What This Skill Owns

- GEOFlow theme discovery and target selection
- preview-first theme edit sessions for existing templates
- reference-site cloning into GEOFlow-compatible modules
- current-template optimization and incremental design adjustment
- confirmation flow for replace-base vs publish-as-new decisions

## What This Skill Does Not Cover

- direct deployment of a new frontend into production
- arbitrary page scraping and raw HTML copying
- changing GEOFlow data queries, routing, or SEO contracts

## Required Preconditions

1. Confirm the target workspace is a GEOFlow codebase with `index.php`, `article.php`, `category.php`, `archive.php`, and `includes/header.php`.
2. Read [references/geoflow-frontend-map.md](references/geoflow-frontend-map.md) and [references/template-boundary.md](references/template-boundary.md) before proposing changes.
3. Discover available themes in `/themes` before editing. Default to the user-selected theme, otherwise use the active theme if known.
4. Preserve the existing module/data contract unless the user explicitly asks for a system change.
5. Choose a work mode:
   - `edit_theme`: adjust a specified existing theme
   - `clone`: map a reference site into a new GEOFlow theme
   - `hybrid`: use a reference site to guide edits on a specified existing theme
6. Treat preview and activation as separate steps. Never edit the live target first when a preview fork can be created.

## Default Workflow

1. Identify the GEOFlow workspace and confirm the canonical frontend and theme-system files.
2. Run `scripts/discover_themes.py` to list existing themes, preview routes, and editable files.
3. Resolve a `target_theme_id` or decide to create a brand-new theme from a reference site.
4. For `edit_theme` or `hybrid`, create a preview fork with `scripts/prepare_theme_edit_session.py` instead of editing the target live.
5. For `clone` or `hybrid`, inspect the reference URL for tokens and layout rhythm. For `edit_theme` or `hybrid`, audit the target theme for hierarchy, spacing, density, responsiveness, and module consistency.
6. Edit only the allowed theme files: `templates/*.php`, `assets/theme.css`, `manifest.json`, and optional `tokens.json` / `mapping.json`.
7. Keep the work in preview status until the operator reviews the generated preview URLs.
8. After confirmation, choose one finalize path:
   - `publish_as_new_theme`: keep or rename the preview fork so it becomes a selectable admin theme
   - `replace_base_theme`: back up the target theme, then replace it from the confirmed preview fork
   - `activate_after_confirmation`: perform activation only after preview approval
9. Call out safe restyle surface, fixed contracts, and live-risk warnings before any finalize step.

## Reference Map

- [references/geoflow-frontend-map.md](references/geoflow-frontend-map.md): authoritative frontend module and variable map
- [references/template-boundary.md](references/template-boundary.md): safe and unsafe modification boundaries
- [references/theme-package-contract.md](references/theme-package-contract.md): expected output shape for theme edit sessions and clone flows
- [references/design-optimization-playbook.md](references/design-optimization-playbook.md): optimization heuristics and preferred outputs
- [references/theme-edit-workflow.md](references/theme-edit-workflow.md): end-to-end workflow for discover -> preview -> adjust -> finalize
