# Theme Package Contract

The output of a GEOFlow template-clone run is a preview-first package, not a
direct production overwrite. A package is reviewable only when its metadata,
preview routes, example entry point, and safety boundaries are committed in a
stable shape.

## Standard Public Example Layout

Committed public examples must use this repository shape:

```text
skills/yao-geoflow-template/
  examples/
    <example-id>/
      README.md
  preview/
    <example-id>/
      index.html
      category.html
      article.html
      archive.html
      assets/
      package/
        tokens.json
        mapping.json
```

The route files may be a partial set only when `mapping.json` declares the
coverage status and omitted routes. Runtime output folders such as `outputs/`
and `outputs-demo/` are not valid dependencies for committed examples.

## Generated Theme Package Shape

When a package is prepared for later GEOFlow integration, the system-facing
package should preserve the same metadata contract while adding implementation
assets:

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

## Required `tokens.json` Fields

- `id`: stable package id, matching the preview package id
- `name`: human-readable package name
- `source_reference_url`: public reference URL when available
- `created_at`: ISO date
- `compatible_system`: target system or frontend contract
- `style_direction`: non-empty list of visual direction tags
- `tokens`: object containing at least one visual token category

## Required `mapping.json` Fields

- `id`: stable package id, matching `tokens.json`
- `name`: human-readable mapping name
- `mvp_order`: non-empty ordered list of route or module groups
- `compatible_pages`: non-empty list of page types
- `module_mapping`: object mapping page/module groups to GEOFlow modules
- `safe_boundaries`: non-empty list of constraints that must remain true
- `preview_routes`: non-empty list of committed preview paths

Recommended fields:

- `coverage_status`: `complete`, `partial`, or `draft`
- `omitted_routes`: required when `coverage_status` is `partial`
- `activation_status`: one of the readiness states below; default to
  `preview-only` unless a future activation spec says otherwise

## Minimum Mapping Output

The package should account for these GEOFlow module groups or explicitly record
why a group is omitted:

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

Preview readiness and production activation readiness are separate states. A
preview package must stay isolated from the active public template until an
operator explicitly confirms a future activation workflow.

## Readiness States

Use these states to avoid treating a reviewable preview as a live deployment:

- `draft`: metadata, route coverage, or safe-boundary documentation is
  incomplete; the package is not ready for public review.
- `preview-only`: committed metadata and preview routes can be inspected from a
  fresh checkout; this state does not imply production activation readiness.
- `activation-candidate`: a human operator has reviewed the preview and opened a
  separate activation request, spec, or implementation plan.
- `activated`: production activation has been completed by a separate
  GEOFlow-owned workflow; this state is out of scope for `yao-geoflow-template`
  package generation.

`yao-geoflow-template` may prepare and document `draft` or `preview-only`
packages. It must not promote a package to `activation-candidate` or `activated`
without a separate activation workflow owned outside this skill.

## Activation-Excluded Changes

Preview-ready packages must not directly change or claim approval for:

- live routing or URL rewrites
- SEO contracts, canonical tags, sitemap behavior, or structured-data policies
- backend schema, content queries, or data-fetching behavior
- production template selection, rollout flags, cache purges, or deployment
  state
- private runtime metadata under ignored `outputs/` or `outputs-demo/` paths

## Public-Safety Rules

Committed package files and previews must not include:

- API keys or credentials
- private customer data
- private URLs or local absolute paths
- dependencies on ignored `outputs/` or `outputs-demo/` metadata
- production activation claims that are not backed by a separate activation spec
- `activation_status` values beyond `preview-only` unless the related
  activation workflow is linked and reviewable

## Validation Expectations

A validator or smoke check must fail when:

- required metadata files are missing
- metadata JSON cannot be parsed
- metadata ids do not match the example id
- required arrays are empty
- committed preview assets reference ignored runtime output paths
- example README is missing for a standardized committed package
