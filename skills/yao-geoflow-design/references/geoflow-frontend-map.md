# GEOFlow Frontend Module And Variable Map

This document is the current GEOFlow frontend contract for `yao-geoflow-design`. It is based on the Laravel rewrite, not the older root-level PHP frontend.

## 1. Current Workspace Baseline

Current GEOFlow signals:

- Laravel entry: `artisan`
- Public routes: `routes/web.php`
- Site controllers: `app/Http/Controllers/Site/*`
- Theme resolver: `app/Support/Site/SiteThemeViewResolver.php`
- Built-in frontend views: `resources/views/site`
- Selectable themes: `resources/views/theme/{theme_id}`
- Admin theme selection: `resources/views/admin/site-settings/index.blade.php`

Legacy PHP signals such as root `index.php`, `article.php`, `category.php`, `archive.php`, and `/themes` are fallback-only.

## 2. Route Contract

Do not change these public routes during a design-only run:

- `/`
- `/article/{slug}`
- `/category/{slug}`
- `/archive`
- `/archive/{year}/{month}`

Admin route base may be customized through `config/geoflow.php`; never hard-code `/geo_admin` in theme output.

## 3. Theme Resolution Contract

`SiteThemeViewResolver::first($template, $data)` resolves:

```text
theme.{active_theme}.{template}
site.{template}
```

If a theme does not provide a Blade view, GEOFlow falls back to `resources/views/site`.

Allowed theme ID pattern:

```text
^[a-zA-Z0-9_-]+$
```

## 4. Theme Package Files

Current theme root:

```text
resources/views/theme/{theme_id}/
```

Recommended files:

```text
manifest.json
tokens.json
mapping.json
home.blade.php
article.blade.php
category.blade.php
archive-index.blade.php
archive-month.blade.php
layout.blade.php
partials/header.blade.php
partials/footer.blade.php
partials/article-card.blade.php
assets/theme.css
```

Only `manifest.json` is required for discovery. Missing Blade views fall back to built-in `site.*`.

## 5. Built-In Frontend Views

Stable built-in views:

- `resources/views/site/layout.blade.php`
- `resources/views/site/home.blade.php`
- `resources/views/site/article.blade.php`
- `resources/views/site/category.blade.php`
- `resources/views/site/archive-index.blade.php`
- `resources/views/site/archive-month.blade.php`
- `resources/views/site/partials/header.blade.php`
- `resources/views/site/partials/footer.blade.php`
- `resources/views/site/partials/article-card.blade.php`

## 6. Shared Layout Modules

### `layout`

Owns:

- HTML shell
- page title and meta description
- canonical URL when provided
- JSON-LD / schema blocks when provided
- header / content / footer slots

Do not remove SEO, canonical, or schema output.

### `partials.header`

Owns:

- site name / logo
- Home link
- category navigation
- archive link when present
- responsive navigation

Inputs are controller-provided site settings and category collections. Do not query the database directly in a theme.

### `partials.footer`

Owns:

- public copyright line
- footer links and minimal public metadata

Keep it public-facing. Admin copyright/version UI is separate.

## 7. Home Page Modules

View: `home`

Stable modules:

- `home.hero`
- `home.featured_articles`
- `home.latest_articles`
- `home.article_card`
- `home.empty_state`
- `home.pagination`

Typical data:

- site settings
- categories
- featured articles
- paginated latest articles
- pagination metadata

## 8. Category Page Modules

View: `category`

Stable modules:

- `category.header`
- `category.description`
- `category.article_list`
- `category.article_card`
- `category.pagination`
- `category.empty_state`

Typical data:

- category
- articles
- pagination metadata

## 9. Article Page Modules

View: `article`

Stable modules:

- `article.header`
- `article.cover_image`
- `article.meta`
- `article.prose`
- `article.tags`
- `article.related_articles`
- `article.ad_slot`

Typical data:

- article
- author
- category
- tags
- related articles
- rendered article HTML
- article images
- article detail ad
- canonical URL and structured data

Important rendering rule: do not show image captions that are only filenames such as `333.png`; keep article images visual unless the system provides meaningful captions.

## 10. Archive Modules

Views: `archive-index`, `archive-month`

Stable modules:

- `archive.overview`
- `archive.month_group`
- `archive.article_list`
- `archive.article_card`
- `archive.pagination`

Typical data:

- archive months
- selected year/month
- articles
- pagination metadata

## 11. Safe Editing Surface

Safe in theme packages:

- Blade markup inside existing page/module boundaries
- CSS tokens, spacing, shadows, colors, borders, typography, responsive behavior
- card layouts and metadata presentation
- header/footer presentation
- ad slot presentation
- `manifest.json`, `tokens.json`, `mapping.json`

Unsafe without explicit system-change approval:

- controllers
- models
- migrations
- routing
- markdown renderer
- SEO/schema generation
- database queries
- admin theme activation

## 12. Preview Notes

Current Laravel GEOFlow does not guarantee an isolated `/preview/{theme}` route. A design run should either:

- generate static preview artifacts for review, or
- create a preview theme under `resources/views/theme` and ask the operator to activate it only after review, or
- use a dedicated preview route only when the current app actually provides one.

Never invent preview URLs from the legacy PHP system.
