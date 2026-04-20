# Iteration Directions

## Top 3 Next Moves

### 1. Add a reference-URL inspection asset

- Add one deterministic helper that captures a reference site's color palette, typography, spacing, and primary layout blocks.
- Keep it focused on token extraction rather than full scraping.

### 2. Add a template-package generator stub

- Generate `manifest.json`, `tokens.json`, and `mapping.json` for a preview-first theme package.
- Do not activate or deploy the package yet.

### 3. Add system integration guidance

- Write the GEOFlow-side implementation plan for:
  - template registration
  - preview routes
  - activation in site settings
- Keep activation separate from generation and preview.
