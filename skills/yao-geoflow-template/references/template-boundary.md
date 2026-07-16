# Template Boundary

This package is now a legacy compatibility router. It must not be used as the primary guide for current GEOFlow frontend work.

## Legacy Context

Older notes in this package referenced a root-level PHP frontend with files such as:

- `index.php`
- `article.php`
- `category.php`
- `archive.php`
- `includes/header.php`
- `includes/footer.php`
- `includes/functions.php`

Those files are legacy assumptions. They are not required for current GEOFlow.

## Current Routing

Use `yao-geoflow-design` for:

- Laravel Blade themes under `resources/views/theme/{theme_id}`
- default site homepage module builder work
- `lead_form` homepage conversion modules
- live theme editor review
- reference-site cloning into current GEOFlow frontend contracts
- GeoFlow Agent target package capability checks
- default-vs-channel frontend sync planning

Stay in this skill only when the user explicitly asks about old PHP template packages or historical outputs.

## Safe Legacy Actions

- Read old `outputs/<template-id>/manifest.json`, `tokens.json`, and `mapping.json`.
- Explain why old PHP paths do not apply to current Laravel GEOFlow.
- Convert a legacy finding into a handoff note for `yao-geoflow-design`.

## Unsafe Actions

- Generating new current GEOFlow themes from the legacy PHP contract.
- Recommending Tailwind CDN or `includes/*.php` as current runtime requirements.
- Treating legacy previews as proof of current Laravel compatibility.
- Editing production frontend files or activating themes.
