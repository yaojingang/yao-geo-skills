# Template Boundary

This skill is for GEOFlow frontend template cloning, optimization, and controlled design adjustments, not for replacing GEOFlow's rendering contract with arbitrary copied pages.

## Allowed Actions

- inventory existing frontend page modules
- inventory variables and helper functions used by the frontend pages
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
- copying an external site's full HTML as the runtime template contract

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

## Unsafe Replacement Surface

- removing required placeholders for article title, content, category, author, tags, slug, or ad CTA fields
- inventing modules that require backend data GEOFlow does not provide yet
- replacing canonical URLs or schema data contracts
- changing article content rendering away from the markdown-rendered article body unless the system is explicitly updated
