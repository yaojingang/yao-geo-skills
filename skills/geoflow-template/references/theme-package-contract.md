# Theme Package Contract

The output of a GEOFlow template-clone run should be a preview-first package rather than a direct production overwrite.

## Recommended Package Shape

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

## Minimum Manifest Fields

- `id`
- `name`
- `source_reference_url`
- `created_at`
- `compatible_pages`
- `compatible_modules`
- `preview_routes`
- `notes`

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

## Preview Contract

The package should be previewed on at least:

- homepage preview
- category preview
- article detail preview
- archive overview preview

Preview must be isolated from the active public template until the operator confirms activation.
