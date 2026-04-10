# Input And Output Contract

This repository uses a shared contract so GEO skills do not drift into incompatible prompt bundles.

## Required Input Fields

Every GEO skill should normalize its user input into the following base structure:

```yaml
skill_id: ""
brand_name: ""
brand_site: ""
brand_summary: ""
category: ""
region: ""
language: ""
target_audience: ""
primary_goal: ""
freshness_window_days: 30
source_policy:
  require_official_sources: true
  require_current_web_verification: true
  allow_forums: false
competitor_seeds: []
must_cover_queries: []
must_avoid_queries: []
deliverable_config:
  output_dir: ""
  article_count: 0
  include_html_index: true
notes: ""
```

## Required Base Inputs

The following fields are required for every factual GEO skill:

- `brand_name`
- `brand_site`
- `category`
- `region`
- `language`
- `primary_goal`

## Input Rules

- Default values must be visible in the template, not hidden in prompt prose.
- Freshness requirements must be explicit.
- Source policy must be explicit.
- Output configuration must be explicit.
- If a skill needs extra fields, extend the base contract instead of replacing it.

## Output Layout

Every run should write to a stable directory:

```text
outputs/<skill-id>/<run-date>-<brand-slug>/
├── manifest.json
├── input-brief.json
├── research-summary.md
├── sources.json
├── quality-report.json
├── deliverables/
└── index.html
```

## Required Output Files

- `manifest.json`: run metadata and versioning
- `input-brief.json`: normalized input snapshot
- `research-summary.md`: operator-readable summary
- `sources.json`: citation ledger
- `quality-report.json`: validation results and open issues

## Output Rules

- Any factual comparison must be traceable to a source entry.
- Any dated claim must carry freshness evidence.
- Deliverables should answer directly before adding long background.
- If verification fails, the output should record the blocker instead of fabricating certainty.
