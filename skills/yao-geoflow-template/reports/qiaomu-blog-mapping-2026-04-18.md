# Qiaomu Blog Template Mapping Exercise

Reference URL:
- https://blog.qiaomu.ai/2026-04-17-qp2x50

Source date:
- 2026-04-18

Target system:
- 一个标准 GEOFlow PHP 工作区

## 1. Purpose

This exercise maps a real reference page from Qiaomu Blog onto GEOFlow's existing frontend contract.

The goal is not literal HTML copying. The goal is to extract:

- visual tokens
- layout direction
- editorial rhythm
- module composition patterns

and then map them onto GEOFlow's existing pages and blocks without changing:

- routing
- business logic
- SEO generation
- structured-data generation
- article/category/archive data contracts

## 2. Reference Site Summary

Observed reference page:
- long-form editorial article page
- sticky top navigation
- narrow centered reading column
- muted neutral background
- restrained border system
- accent-driven link and active-state color
- low-noise layout with reading-first spacing

Strong signals detected from the page source:
- CSS variable system is present:
  - `--background`
  - `--body-font`
  - `--editor-accent`
  - `--editor-ink`
  - `--editor-line`
  - `--editor-muted`
  - `--editor-panel`
  - `--logo-font`
  - `--stone-gray`
- article container uses a narrow readable width:
  - `max-w-3xl`
- header uses sticky + translucent / blurred treatment:
  - `backdrop-blur`
- navigation is lightweight and editorial rather than portal-like
- page reads like a blog publication rather than a CMS listing page

Visible product language:
- site name: `乔木博客`
- nav style: `论文学习 / GitHub / Twitter / RSS / 主题`
- article metadata is compact and subdued
- content area emphasizes prose readability over dense widgets

## 3. Extracted Design Direction

### 3.1 Visual character

The page direction is:

- editorial
- scholarly / calm
- typography-led
- border-light
- accent-constrained
- mobile-safe without looking app-like

It should not be cloned as:

- high-saturation marketing landing page
- dashboard-like card wall
- portal homepage

### 3.2 Token candidates

These are inferred theme tokens GEOFlow can safely adopt.

#### Color tokens

- `background`: warm light neutral
- `surface`: white or near-white
- `line`: very light gray border
- `ink`: dark neutral text
- `muted`: medium gray supporting text
- `accent`: controlled blue accent
- `panel`: slightly tinted neutral panel for metadata or callouts

#### Spacing and shape

- generous vertical whitespace
- thin borders instead of heavy shadows
- medium radius, not overly rounded
- narrow reading width for article prose

#### Typography

- body should feel editorial, not dashboard UI
- large headline, compact metadata
- paragraph rhythm is more important than card density
- navigation text is small and quiet

#### Header behavior

- sticky
- lightly bordered
- blurred / translucent backdrop
- centered inner container

## 4. GEOFlow Compatibility Judgment

This reference is compatible with GEOFlow as a style source, but only if the system preserves GEOFlow's data-driven modules.

Safe compatibility level:
- high for article page
- medium-high for homepage article list
- high for category and archive list styling
- medium for header/navigation
- medium for ad block styling

Unsafe areas:
- copying the reference site's full navigation information architecture
- copying external social links as runtime navigation requirements
- assuming the reference site's taxonomy labels exist in GEOFlow
- replacing GEOFlow's article card fields with fields the backend does not provide

## 5. Module-to-Module Mapping

This is the core output of the exercise.

### 5.1 Header Mapping

Reference source qualities:
- sticky top bar
- centered inner width
- light border bottom
- blurred background
- quiet navigation tone

Map to GEOFlow:
- `includes/header.php`
- modules:
  - `header.logo`
  - `header.primary_nav`
  - `header.category_dropdown`
  - `header.mobile_menu`
  - `header.admin_link`

Safe replacement:
- navigation spacing
- border and blur treatment
- logo and site-title styling
- category dropdown visual style

Must preserve:
- category source from `get_categories()`
- admin link
- current route awareness

### 5.2 Homepage Mapping

Reference source qualities:
- article-first listing
- quiet sectional rhythm
- minimal decorative noise

Map to GEOFlow homepage modules:
- `home.hero`
- `home.featured_list`
- `home.latest_list`
- `home.article_card`
- `home.pagination`

Recommended changes:
- reduce card chrome
- emphasize article title + excerpt
- use subtler category chips
- use editorial spacing instead of portal blocks
- keep featured section, but restyle it to feel like curated editorial highlights

### 5.3 Article Card Mapping

Reference source qualities:
- metadata is compact
- hierarchy is title-first
- supporting text is muted

Map to GEOFlow:
- `home.article_card`
- `category.article_card`
- `archive.article_card`

Suggested card structure:
- category chip
- title
- excerpt
- date / metadata row
- optional tags
- understated `Read More`

Must preserve existing GEOFlow data:
- `article.slug`
- `article.title`
- `article.excerpt`
- `article.created_at`
- category metadata

### 5.4 Article Detail Mapping

Reference source qualities:
- strong title
- compact metadata
- narrow reading column
- prose shell with minimal distractions

Map to GEOFlow:
- `article.hero`
- `article.prose_shell`
- `article.related_articles`
- `article.tags`

Recommended structure:
- breadcrumb above hero, but visually minimized
- category chip + title + metadata stack
- optional summary box retained, but styled as a quiet note panel
- markdown prose shell with narrower readable width
- related articles as a subdued continuation block, not a loud card carousel

Must preserve:
- GEOFlow markdown-rendered article body
- tags
- related articles source
- SEO/meta/schema output

### 5.5 Category Page Mapping

Reference source qualities:
- calm list page
- title + description + article flow

Map to GEOFlow:
- `category.header`
- `category.article_card`
- `category.pagination`

Recommended changes:
- category header should be simple and editorial
- cards reuse homepage card style
- avoid oversized category chrome

### 5.6 Archive Page Mapping

Reference source qualities:
- informational, not promotional

Map to GEOFlow:
- `archive.overview_row`
- `archive.article_card`

Recommended changes:
- archive overview rows should use thin separators and muted counts
- month pages should reuse article card styling from homepage/category

### 5.7 Sticky Ad Block Mapping

Reference source qualities:
- no obvious ad-heavy treatment on the reference page
- CTA blocks should be low-noise and text-first

Map to GEOFlow:
- `article.sticky_ad`

Recommended adaptation:
- restyle ad block as an editorial callout
- keep:
  - `badge`
  - `title`
  - `copy`
  - `button_text`
  - `button_url`
- reduce marketing-style gradients or loud call-to-action treatments

This is a style reinterpretation, not a 1:1 copy, because the reference page does not expose a matching ad slot contract.

## 6. Preview-First Theme Package Proposal

For this reference, the first generated template package should target:

```text
themes/
  qiaomu-editorial-20260418/
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

Suggested manifest fields:
- `id`: `qiaomu-editorial-20260418`
- `name`: `Qiaomu Editorial`
- `source_reference_url`: the reference URL
- `compatible_pages`:
  - `home`
  - `category`
  - `article`
  - `archive`
- `compatible_modules`:
  - `header`
  - `footer`
  - `home.article_card`
  - `article.hero`
  - `article.prose_shell`
  - `article.related_articles`
  - `article.sticky_ad`
- `notes`:
  - editorial clone direction
  - reading-first layout
  - no backend data contract changes

## 7. Preview Routes

This template should not be activated directly.

Recommended preview routes:
- `/preview/qiaomu-editorial-20260418/`
- `/preview/qiaomu-editorial-20260418/category/{slug}`
- `/preview/qiaomu-editorial-20260418/article/{slug}`
- `/preview/qiaomu-editorial-20260418/archive`

These previews should render against live GEOFlow data while swapping only the presentation layer.

## 8. What Can Be Cloned Safely

Safe clone surface:
- color palette direction
- spacing rhythm
- header border / blur style
- centered container widths
- title and metadata hierarchy
- article card density
- prose shell styling
- low-noise related article block
- editorial callout treatment for sticky ad

## 9. What Must Not Be Cloned Literally

Do not clone literally:
- external site navigation labels as system requirements
- external site social destinations as permanent GEOFlow header elements
- exact page HTML
- exact client-side framework behavior
- any data field GEOFlow does not already expose
- any structure that would remove GEOFlow breadcrumb, SEO, schema, or article rendering contract

## 10. Recommended MVP

The first implementation pass should not try to restyle every page equally.

Recommended MVP order:

1. `header`
2. `article.hero`
3. `article.prose_shell`
4. `home.article_card`
5. `category.article_card`
6. `article.related_articles`
7. `article.sticky_ad`

Reason:
- the reference site's strongest signal is article-reading quality
- GEOFlow's article page is the highest-value place to capture that signal
- homepage/category/archive can reuse one shared card language

## 11. System Work Needed After Skill Output

The skill output alone is not enough for production use.

GEOFlow system still needs:
- template registration
- template preview routing
- template selection in admin site settings
- confirmation-based activation

That system work should happen separately from the skill.

## 12. Final Judgment

This reference URL is a good first target for GEOFlow template cloning because:

- it has a strong editorial identity
- it maps well to GEOFlow's article-first pages
- it does not require impossible backend fields
- it can improve GEOFlow's article readability without changing any business logic

Best interpretation:
- not a full-site copy
- a GEOFlow-compatible editorial theme derived from Qiaomu Blog
