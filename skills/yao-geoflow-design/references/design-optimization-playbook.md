# Design Optimization Playbook

Use this reference when the request is to improve an existing GEOFlow theme rather than replace it wholesale.

## Optimization Modes

- `polish`: tighten spacing, typography, chips, borders, shadows, and visual rhythm
- `structural_cleanup`: simplify noisy sections, unify repeated cards, and reduce layout inconsistency
- `page_specific_tuning`: improve one or two pages such as homepage or article detail without redesigning the full system
- `hybrid_restyle`: use a reference site as direction while staying anchored to the current template
- `target_theme_edit`: apply the changes inside a selected theme fork that can be previewed in the live GEOFlow system

## Default Audit Checklist

- header density and navigation clarity
- hero hierarchy and section rhythm
- card consistency across home/category/archive
- article readability, metadata treatment, and related-content treatment
- ad block tone and how aggressive it feels
- mobile spacing, stacking, and overflow risk
- repeated token drift across colors, radii, borders, and shadows
- whether the requested new display modules can be built from existing GEOFlow data fields

## Preferred Outputs

- `design-audit.md`: current-template issues, constraints, and opportunities
- `tokens.delta.json`: only the token changes needed for the optimization pass
- `mapping.delta.json`: touched modules and what changes inside each one
- `change-plan.md`: priority order, rollout notes, and preview focus
- preview pages or preview notes for every touched route
- a preview theme id and preview URLs when the edit runs against an existing target theme

## Guardrails

- preserve GEOFlow routes, helpers, and data queries
- optimize modules that already exist before inventing new ones
- prefer shared card and metadata patterns over one-off page styling
- when the current template is acceptable structurally, bias toward token cleanup and hierarchy fixes instead of large rewrites
- default to preview-fork editing instead of live-theme editing on the first pass
