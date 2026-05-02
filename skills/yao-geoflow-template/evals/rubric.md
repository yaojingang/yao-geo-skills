# Yao GEOFlow Template Rubric

Use this rubric to review outputs produced by `yao-geoflow-template`.

## Scoring

Score each dimension from `1` to `5`.

- `5`: fully satisfies the contract and produces a preview-safe package plan
- `3`: mostly satisfies the contract but leaves integration ambiguity
- `1`: violates GEOFlow boundaries or copies a reference site unsafely

## Dimensions

### 1. Trigger Boundary

- Uses this skill for GEOFlow-compatible template planning and preview packages.
- Rejects generic frontend redesign, backend schema changes, and raw page copying.
- Starts from the GEOFlow frontend contract, not from a blank design brief.

### 2. Contract Preservation

- Preserves routing, SEO, data-query responsibilities, and module boundaries.
- Maps reference patterns onto GEOFlow modules instead of replacing data contracts.
- Calls out conflicts between the reference site and GEOFlow's available fields.

### 3. Reference Analysis

- Extracts visual tokens, layout rhythm, typography, color, and interaction direction.
- Distinguishes observed reference facts from inferred design direction.
- Avoids copying proprietary navigation, content, or full HTML structures.

### 4. Package Completeness

- Provides manifest, tokens, mapping, example entry point, and preview-route expectations.
- Defines the standardized public example shape: `examples/<example-id>/README.md`, `preview/<example-id>/package/tokens.json`, and `preview/<example-id>/package/mapping.json`.
- Records required identity, source, creation date, compatible system, token, route coverage, module mapping, safe-boundary, and preview-route metadata.
- Covers homepage, category, article detail, archive, header/footer, and ad-slot treatment.
- Keeps package metadata self-contained enough for preview review.

### 5. Preview-First Safety

- Treats preview and production activation as separate steps.
- Does not activate a template without explicit operator confirmation.
- Produces inspectable preview artifacts when the user asks to see the mapped style.
- Avoids committed preview dependencies on ignored `outputs/` or `outputs-demo/` runtime paths.

## Passing Threshold

A passing run should average at least `4.0`, with no dimension below `3`.
