# Iteration Directions

## Top 3 Next Moves

### 1. Add a current-template audit asset

- Add one deterministic helper that scores current GEOFlow templates for spacing drift, card inconsistency, metadata noise, and responsive issues.
- Keep it focused on actionable module findings instead of generic critique.

### 2. Add an optimization delta generator stub

- Generate `design-audit.md`, `tokens.delta.json`, `mapping.delta.json`, and `change-plan.md` for optimization mode.
- Do not activate or deploy the package yet.

### 3. Add before/after preview guidance

- Write the GEOFlow-side preview guidance for:
  - full theme packages
  - patch-style optimization passes
  - module-level before/after checks
- Keep activation separate from generation and preview.
