# GEOFlow Frontend Map - Legacy Pointer

This reference is intentionally short. The full current frontend map lives in `yao-geoflow-design`.

## Legacy Signals

Old GEOFlow template notes used a root-level PHP frontend:

- public pages: `index.php`, `article.php`, `category.php`, `archive.php`
- shared files: `includes/header.php`, `includes/footer.php`, `includes/functions.php`
- asset assumptions: `assets/css/style.css`, `assets/css/custom.css`, Tailwind CDN

These are historical compatibility signals only.

## Current GEOFlow Signals

Current GEOFlow frontend work should look for:

- `artisan`
- `routes/web.php`
- `resources/views/site`
- `resources/views/theme/{theme_id}`
- `app/Support/Site/HomepageModuleBuilder.php`
- `resources/views/site/partials/homepage-modules.blade.php`
- `resources/views/site/partials/lead-form.blade.php`
- `app/Http/Controllers/Admin/SiteThemeEditorController.php`
- `app/Services/GeoFlow/DistributionTargetSitePackageBuilder.php`

If these current signals exist, route the task to `yao-geoflow-design`.

## Current Public Routes

Current design work should preserve:

- `/`
- `/article/{slug}`
- `/category/{slug}`
- `/archive`
- `/archive/{year}/{month}`
- `/forms/{slug}` when growth-center lead forms are enabled

Do not infer current routes from the old PHP frontend.
