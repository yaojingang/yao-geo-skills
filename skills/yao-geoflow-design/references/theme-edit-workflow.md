# Theme Edit Workflow

Use this workflow when the request is to adjust a theme that already exists in a GEOFlow workspace.

## System Signals To Detect

The current GEOFlow theme system is considered present when the workspace contains:

- `artisan`
- `routes/web.php`
- `resources/views/site`
- `resources/views/theme/<theme-id>/...`
- `app/Support/Site/SiteThemeViewResolver.php`
- theme selection in `resources/views/admin/site-settings/index.blade.php`
- `site_settings.active_theme` storing the active theme ID

Legacy PHP workspaces may still use `/themes`, `includes/theme_preview.php`, and `theme-preview.php`; treat those as fallback only.

## Workflow States

### 1. Discover

- inspect `resources/views/theme` first, then legacy `/themes` only when Laravel signals are absent
- read each `manifest.json`
- collect editable files:
  - `home.blade.php`
  - `category.blade.php`
  - `article.blade.php`
  - `archive-index.blade.php`
  - `archive-month.blade.php`
  - `layout.blade.php`
  - `partials/*.blade.php`
  - `assets/theme.css`
  - optional `tokens.json`
  - optional `mapping.json`
- note which themes already look like preview or edit-session forks

Recommended helper:
- `scripts/discover_themes.py`

### 2. Select

- resolve `target_theme_id`
- if the user did not specify a theme, prefer the active theme when known
- if the active theme is unknown, present the discovered themes and ask the model to keep the selection explicit in its plan

### 3. Fork Preview Session

- do not edit the target theme live on the first pass
- create a preview fork under `resources/views/theme/<preview-theme-id>` for Laravel GEOFlow
- mark the fork clearly as preview or edit-session in `manifest.json`
- emit public route samples and clearly note whether the current app has isolated preview routes

Recommended helper:
- `scripts/prepare_theme_edit_session.py`

### 4. AI Edit Loop

Safe edit surface:

- Blade files inside the selected theme
- `assets/theme.css`
- `manifest.json`
- optional tokens and mapping files

Fixed contracts during the edit loop:

- do not hard-code `/geo_admin`
- preserve SEO, canonical, and schema output
- preserve article rendered-HTML behavior and style tables/headings/lists/code blocks through CSS
- do not show filename-only image captions
- keep preview/activation separate

Typical requests:

- make the layout wider
- make titles bolder
- reduce card noise
- simplify metadata
- add a display module only when it can be built from existing GEOFlow data

### 5. Review Preview

- inspect preview URLs for home, category, article, and archive
- call out what changed, what remained fixed, and where risks still exist
- keep iterating on the preview fork until the operator confirms

### 6. Finalize

After preview approval, choose one path:

- `publish_as_new_theme`
  - keep the preview fork as a new theme or rename it to a stable theme id
  - the admin theme picker can then discover it as a new template
- `replace_base_theme`
  - back up the original target theme outside `/themes`
  - replace the target theme from the confirmed preview fork
  - warn that the live site may change immediately if that target theme is active
- `activate_after_confirmation`
  - activation should happen only after review
  - prefer the admin site-settings flow unless the user explicitly wants direct system mutation

Recommended helper:
- `scripts/finalize_theme_edit_session.py`

## Safety Rules

- preview first, live later
- keep backups outside `resources/views/theme` so admin discovery does not treat them as selectable templates
- do not add modules that require backend fields GEOFlow does not already expose
- do not touch routing, search, SEO generation, or schema generation unless the user explicitly expands scope
