# Iteration Directions

## Top 3 Next Moves

### 1. Add preview verification automation

- Add one deterministic helper that walks the generated preview URLs for home, category, article, and archive.
- Capture pass/fail notes or screenshots so the edit loop does not rely on manual memory alone.

### 2. Add optional active-theme resolution

- Add a helper that resolves `active_theme` when the local runtime database is reachable.
- When runtime access is unavailable, keep the selection explicit and warn instead of guessing.

### 3. Add reusable module-insertion patterns

- Add guarded patterns for common requests such as featured grids, author strips, topic highlights, or CTA panels.
- Keep the rule strict: new display modules must be powered by existing GEOFlow data or existing settings.
