# Qiaomu Editorial Example

This example documents the committed preview package for the Qiaomu editorial mapping exercise. It is a public, self-contained example for reviewing the `yao-geoflow-template` package contract.

## Preview Files

- `preview/qiaomu-editorial-20260418/index.html`
- `preview/qiaomu-editorial-20260418/category.html`
- `preview/qiaomu-editorial-20260418/article.html`
- `preview/qiaomu-editorial-20260418/archive.html`

## Package Metadata

- `preview/qiaomu-editorial-20260418/package/tokens.json`
- `preview/qiaomu-editorial-20260418/package/mapping.json`

## Purpose

The example shows how a reference site's editorial visual direction can be mapped onto GEOFlow homepage, category, article, and archive modules without changing routing, backend queries, or production activation state.

## Safety Boundary

- Metadata is committed under `preview/qiaomu-editorial-20260418/package/`.
- Preview files must not depend on ignored `outputs/` or `outputs-demo/` paths.
- `coverage_status` is `complete` for the preview routes listed above.
- `activation_status` is `preview-only`; this example does not activate a production GEOFlow theme.
- The example preserves GEOFlow routing, canonical URLs, article/category/archive data sources, and backend queries.

## Review Checklist

- `tokens.json` records package identity, public source reference, creation date, compatible system, visual direction, and token groups.
- `mapping.json` records route coverage, module mapping, safe boundaries, activation status, and committed preview routes.
- `assets/app.js` loads metadata from committed `package/*.json` files and shows a graceful unavailable state if metadata cannot be read.
