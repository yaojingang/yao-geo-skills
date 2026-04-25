# Template Boundary

This skill is for GEOFlow frontend template cloning, theme discovery, preview-first theme editing, and controlled design adjustments, not for replacing GEOFlow's rendering contract with arbitrary copied pages.

## Allowed Actions

- inventory existing frontend page modules
- inventory variables and helper functions used by the frontend pages
- discover existing themes and their editable files in the current workspace, preferring `resources/views/theme` for Laravel GEOFlow
- select a target theme and fork it into a preview edit session
- inspect a reference URL for design tokens and layout direction
- design a GEOFlow-compatible theme package
- audit the current template for hierarchy, spacing, typography, density, and responsive issues
- propose incremental token refinement and module-level visual cleanup
- generate before/after preview notes for touched modules
- generate a preview-first integration plan
- suggest how the admin should later expose template selection

## Disallowed Actions

- rewriting GEOFlow business logic just to imitate a reference site
- replacing existing PHP data queries with hard-coded mock content
- changing routing rules such as `/article/{slug}`, `/category/{slug}`, or `/archive/...`
- removing SEO or structured-data generation
- direct production activation without preview and confirmation
- editing the live target theme first when a preview fork has not yet been reviewed
- copying an external site's full HTML as the runtime template contract
- editing Laravel controllers, models, migrations, or routes during a design-only request

## Non-Negotiable GEOFlow Contracts

- homepage remains data-driven by published articles, featured articles, categories, search state, and pagination
- article detail remains data-driven by article, related articles, tags, SEO blocks, and the article detail ad slot
- category page remains driven by category metadata and paginated article lists
- archive page remains driven by archive overview or month-specific archive data
- frontend continues to use GEOFlow routing, helpers, and data fields

## Safe Replacement Surface

- HTML structure inside module containers
- CSS tokens, spacing, shadows, borders, and colors
- iconography and button styles
- layout composition of existing modules
- design hierarchy, visual density, and responsive behavior of existing modules
- consistency cleanup across repeated cards, section headers, and metadata rows
- ad-block visual presentation
- header / footer presentation
- theme manifest metadata, preview routes, and non-runtime notes

## Unsafe Replacement Surface

- removing required placeholders for article title, content, category, author, tags, slug, or ad CTA fields
- inventing modules that require backend data GEOFlow does not provide yet
- replacing canonical URLs or schema data contracts
- changing article content rendering away from the markdown-rendered article body unless the system is explicitly updated
- storing preview-session backups under `resources/views/theme` or `/themes` in a way that makes them look like live templates without clear preview labeling
- claiming isolated preview URLs exist in Laravel GEOFlow unless `routes/web.php` provides them
