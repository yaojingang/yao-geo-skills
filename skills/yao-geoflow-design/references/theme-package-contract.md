# Theme and Optimization Package Contract

The output of a GEOFlow design run should be a preview-first package rather than a direct production overwrite.

## Mode A: Full Theme Package

```text
themes/
  template-YYYYMMDD-XXX/
    manifest.json
    tokens.json
    mapping.json
    assets/
      theme.css
      preview.css
    templates/
      header.php
      footer.php
      home.php
      category.php
      article.php
      archive.php
      blocks/
        article-card.php
        related-articles.php
        ad-sticky.php
```

## Mode B: Optimization Patch Package

```text
design-passes/
  design-pass-YYYYMMDD-XXX/
    manifest.json
    design-audit.md
    tokens.delta.json
    mapping.delta.json
    change-plan.md
    preview-notes.md
    assets/
      preview.css
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
  - `optimization_goals`
  - `change_scope`

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
- When `mode = optimize`:
  - `change_scope`
  - `unchanged_contracts`
  - `delta_strategy`

## Preview Contract

The package should be previewed on at least:

- homepage preview
- category preview
- article detail preview
- archive overview preview

Optimization runs should also include a short before/after rationale for each touched module.

Preview must be isolated from the active public template until the operator confirms activation or patch application.
