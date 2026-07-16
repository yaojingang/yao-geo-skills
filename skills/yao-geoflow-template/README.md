# Yao GEOFlow Template Legacy Router

`yao-geoflow-template` is now a compatibility entrypoint for old PHP-template package notes. New GEOFlow frontend work should use `yao-geoflow-design`.

## Primary Use

- inspect historical `outputs/<template-id>/` artifacts
- explain old root-level PHP template assumptions
- route current Laravel Blade, homepage builder, theme editor, reference-site cloning, and channel frontend tasks to `yao-geoflow-design`

## Boundary

This skill does not create new current GEOFlow themes. It does not assume `index.php`, `article.php`, `category.php`, `archive.php`, or `includes/header.php` exist in the current Laravel codebase.

## Package Map

- `SKILL.md`: legacy routing boundary
- `agents/interface.yaml`: canonical interface metadata
- `agents/openai.yaml`: OpenAI-friendly interface metadata
- `references/geoflow-frontend-map.md`: short legacy map and current Laravel pointer
- `references/template-boundary.md`: safe legacy interpretation rules
- `references/theme-package-contract.md`: historical output shape and replacement path
- `evals/trigger_cases.json`: routing boundary checks
- `reports/geoflow-skill-upgrade-2026-07-05.md`: current upgrade evidence
