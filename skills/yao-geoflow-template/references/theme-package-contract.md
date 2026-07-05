# Theme Package Contract

This contract documents historical outputs only. It is not the current GEOFlow theme-generation contract.

## Historical Output Shape

Old template runs may contain:

```text
outputs/<template-id>/
  manifest.json
  tokens.json
  mapping.json

preview/<template-id>/
  index.html
  category.html
  article.html
  archive.html
```

These artifacts are useful for reviewing visual intent, token choices, and page mapping decisions. They are not directly deployable into current GEOFlow without a Laravel Blade mapping pass.

## Current Replacement Path

For new work, use `yao-geoflow-design` and produce current artifacts such as:

- Laravel Blade theme package under `resources/views/theme/{theme_id}`
- optional public assets under `public/themes/{theme_id}`
- reviewed `homepage-design.json` for homepage module/style imports
- channel frontend settings JSON and sync preview reports
- target-package capability gap report when syncing to GeoFlow Agent channels

## Review Rule

When a user provides an old template output, summarize it as:

- visual tokens worth keeping
- page/module mapping intent
- incompatible legacy assumptions
- recommended `yao-geoflow-design` handoff
