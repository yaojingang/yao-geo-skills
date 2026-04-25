# Theme Edit and Package Contract

The output of a GEOFlow design run should be a preview-first session or package rather than a direct production overwrite.

## Mode A: Full New Theme Package

```text
resources/views/theme/
  template-YYYYMMDD-XXX/
    manifest.json
    tokens.json
    mapping.json
    assets/
      theme.css
      preview.css
    layout.blade.php
    home.blade.php
    category.blade.php
    article.blade.php
    archive-index.blade.php
    archive-month.blade.php
    partials/
      header.blade.php
      footer.blade.php
      article-card.blade.php
```

## Mode B: Preview Theme Edit Session

```text
resources/views/theme/
  target-theme-edit-YYYYMMDD-XXX/
    manifest.json
    edit-session.json
    design-audit.md
    tokens.delta.json
    mapping.delta.json
    change-plan.md
    preview-notes.md
    assets/
      theme.css
      preview.css
    home.blade.php
    category.blade.php
    article.blade.php
    archive-index.blade.php
    archive-month.blade.php
    partials/
      header.blade.php
      footer.blade.php
      article-card.blade.php
```

## Minimum Manifest Fields

- `id`
- `name`
- `mode`
- `created_at`
- `compatible_pages`
- `compatible_modules`
- `preview_routes`
- `notes`
- Optional:
  - `source_reference_url`
  - `base_template_id`
  - `target_theme_id`
  - `optimization_goals`
  - `change_scope`
  - `session_state`

## Minimum Edit-Session Fields

- `base_theme_id`
- `preview_theme_id`
- `created_at`
- `change_request`
- `preview_routes`
- `finalize_options`

## Minimum Mapping Output

- `header`
- `footer`
- `home.hero`
- `home.featured_list`
- `home.article_card`
- `category.article_card`
- `article.hero`
- `article.prose_shell`
- `article.related_articles`
- `article.sticky_ad`
- `archive.overview_row`
- `archive.article_card`
- When `mode = edit_theme` or `mode = optimize`:
  - `change_scope`
  - `unchanged_contracts`
  - `delta_strategy`
  - `edited_files`

## Finalize Paths

- `publish_as_new_theme`: keep or rename the preview fork so admin theme discovery can list it as a new template
- `replace_base_theme`: back up the original target theme and then replace it from the confirmed preview fork
- `activate_after_confirmation`: activate only after the operator confirms the reviewed preview session

## Preview Contract

The package should be previewed on at least:

- homepage preview
- category preview
- article detail preview
- archive overview preview

Current Laravel GEOFlow may not provide isolated `/preview/{theme}` URLs. Preview theme edit sessions should clearly say whether review uses static preview artifacts, temporary admin activation, or a real preview route discovered in `routes/web.php`.

Optimization runs should also include a short before/after rationale for each touched module.

Preview must be isolated from the active public template until the operator confirms replacement, publish-as-new, or activation.
