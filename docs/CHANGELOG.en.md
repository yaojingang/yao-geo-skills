# Yao GEO Skills Changelog

This document tracks public repository releases for the skill catalog. Update this file together with the Chinese version in `CHANGELOG.md` whenever a new skill or a significant repository-level change is pushed.

## 2026-07-03

### `yao-doubao-crawler` Initial Release

- Added the measurement skill package: `skills/yao-doubao-crawler`.
- Supports Doubao web sampling through OpenCLI and Doubao Android App visible-UI collection through Android Studio AVD + Appium UiAutomator2.
- Outputs `yao-doubao-crawler/v1` compatible JSON, structured Markdown, Excel, Kami-style HTML reports, mobile screenshots/XML, and search-material citation evidence.
- Added fresh-chat isolation, mobile cited/uncited material flags, citation counts, and `mobile_evidence` summaries.
- Updated `registry/skills.json`, repository navigation, English README, visual catalog, and the guide at `docs/skills/yao-doubao-crawler.md`.

## 2026-05-21

### GEO Skill Batch Update

- Synced the latest local updates for 13 GEO skills: `yao-geo-effect-monitor`, `yao-geo-panorama-audit`, `yao-geo-page-audit`, `yao-geo-page-blueprint`, `yao-geo-title-optimizer`, `yao-geo-explainer-builder`, `yao-geo-knowledge-base-builder`, `yao-geo-intent-miner`, `yao-geo-execution-roadmap`, `yao-geo-brand-graph`, `yao-geo-comparison-builder`, `yao-geo-content-refiner`, and `yao-geo-ranking-article-builder`.
- Standardized real-data handling across the updated skills: public web evidence, user-supplied files, authorized data, platform sampling, unavailable data, source freshness, evidence grades, and gap lists are now separated explicitly.
- Standardized four-format delivery: most long-form reports now share one content structure across Markdown, HTML, Word, and PDF, with sticky-navigation HTML reports for long documents.
- Updated `registry/skills.json`, the repository homepage, the English README, the visual navigation page, and the relevant `docs/skills/*.md` guides so GitHub users can see the latest purpose, outputs, and quality gates.

## 2026-05-19

### `yao-geo-explainer-builder` Initial Release

- Added the content-production skill package: `skills/yao-geo-explainer-builder`.
- Generates GEO explainers, how-to guides, concept explanations, selection guides, pitfall guides, FAQs, glossaries, and controlled brand-insertion recommendations.
- Added a research foundation based on GEO, RAG, long-context position bias, and Chain-of-Thought prompting, plus a source ledger and citation-ready information units.
- The demo now includes real Markdown, HTML, Word, and PDF files, with automated checks for four-format existence, brand-mention limits, source ledger completeness, research grounding, and Word table preservation.
- Updated `registry/skills.json`, repository navigation, English navigation, and the guide at `docs/skills/yao-geo-explainer-builder.md`.

### `yao-geo-page-audit` Initial Release

- Added the page-technology skill package: `skills/yao-geo-page-audit`.
- Audits a target URL plus representative level-1 and level-2 pages for crawlability, structure, content signals, and AI extractability.
- Includes the standard brief, research foundation, page audit method, white-background four-format layout rules, quality gates, and a synthetic demo.
- The demo now includes real Markdown, HTML, Word, and PDF files, with a link-existence check requirement.
- Updated `registry/skills.json`, the repository homepage, English navigation, and the guide at `docs/skills/yao-geo-page-audit.md`.

### `yao-geo-ranking-article-builder` Research Upgrade And Example Fix

- Added the content-production skill package: `skills/yao-geo-ranking-article-builder`.
- Added four real example reports: Markdown, HTML, Word, and PDF, plus an openable `index.html`.
- Added the EICAS foundation based on GEO, RAG, Generative Relevance Feedback, AutoGEO, and AgenticGEO research.
- Fixed the delivery pipeline: HTML/PDF now use a custom white-background template, and Word output gets explicit table borders.

### `yao-geo-effect-monitor` Initial Release

- Added the monitoring-loop skill package: `skills/yao-geo-effect-monitor`.
- The skill designs a GEO Signal Monitor across DeepSeek, Doubao, Qianwen, Kimi, and Yuanbao, covering AI-answer monitoring, citation tracking, brand-fact correction, alerts, monthly reporting, and cautious attribution.
- Added a standard brief template, five-platform sampling rules, metrics and attribution guidance, correction-task model, dashboard fields, database tables, API draft guidance, and a four-format sample report.
- Strengthened the method with GEO, generative-search verifiability, generative relevance feedback, AgenticGEO, citation failure diagnosis, and causal impact research, adding citation recall/precision, black-box variation, diversified prompt expansion, and cautious attribution standards.
- Regenerated the sample report from one Markdown source into Markdown, HTML, Word, and PDF, with real-file and text-extraction checks.
- Updated `registry/skills.json`, repository navigation, and the human-readable guide at `docs/skills/yao-geo-effect-monitor.md`.

### `yao-geo-brand-graph` Initial Release

- Added the knowledge-assets skill package: `skills/yao-geo-brand-graph`.
- The skill turns company information into an auditable entity graph across brands, products, people, places, cases, evidence, and scenarios.
- Added entity/relationship schema guidance, evidence and privacy policy, disambiguation workflow, Mermaid, JSON-LD, RDF-style triples, white-background four-format report layout rules, and a renderer.
- Added a synthetic demo that generates Markdown, HTML, Word, PDF, and `quality-report.json` from one `report_input.json`.

### `yao-geo-intent-miner` Research Upgrade And Example Fix

- Added the research skill package: `skills/yao-geo-intent-miner`.
- Added four real example reports: Markdown, HTML, Word, and PDF, plus `quality-report.json`.
- Updated the method with search intent taxonomy, LLM query expansion, HyDE, conversational query rewriting, TREC CAsT, and BEIR/MS MARCO.
- Added five-stage query rewriting, evidence-availability constraints, replayable conversational-chain fields, and four-format quality gates.

### `yao-geo-panorama-audit` Initial Release

- Added the strategic diagnosis skill package: `skills/yao-geo-panorama-audit`.
- Establishes a brand GEO baseline across DeepSeek, Doubao, Qwen, Kimi, and Tencent Yuanbao, covering AI-answer visibility, competitor gaps, content/page gaps, and external source gaps.
- Includes the standard input brief, China-platform sampling fields, eight-dimensional GEO quality model, quality gates, white-background four-format report layout rules, and a synthetic demo.
- Updated `registry/skills.json`, the repository homepage, English navigation, and the human-readable guide at `docs/skills/yao-geo-panorama-audit.md`.

## 2026-04-26

### `yao-geoflow-cli` Laravel API v1 / Docker alignment

- Added `references/laravel-api-v1-docker.md` to document Laravel `/api/v1` fallback, Docker checks, API scopes, and token handling
- Hardened `geoflow_preflight.sh`:
  - prints Docker Compose guidance when the CLI is absent
  - verifies that `/api/v1/catalog` returns JSON
  - diagnoses HTML responses such as `<!doctype html>` as base URL / proxy / route problems
- Updated CLI documentation so non-JSON API responses are not confused with AI model response-format errors

### `yao-geoflow-design` Laravel Blade theme contract update

- Added stronger coverage for GEOFlow Laravel Blade theme roots, fallback behavior, and `active_theme`
- Clarified that themes must not hard-code `/geo_admin` or change backend routes, controllers, database queries, or independent language logic
- Added fixed rendering expectations for article image captions, markdown-rendered HTML, SEO/schema slots, footer behavior, and public language behavior
- Updated Chinese and English guides for the current GEOFlow rewrite

## 2026-04-20

### Renamed `geoflow-template` to `yao-geoflow-template`

- Moved the public skill package to `skills/yao-geoflow-template`
- Moved the public guides to:
  - `docs/skills/yao-geoflow-template.md`
  - `docs/skills/yao-geoflow-template.en.md`
- Updated the repository homepage, `registry/skills.json`, and public navigation links
- The rename does not change the skill boundary; it still covers GEOFlow frontend template mapping and preview-first output packages

### Initial publication of `yao-geoflow-design`

- Added `skills/yao-geoflow-design`
- Expanded the earlier `yao-geoflow-template` direction into a broader frontend design skill:
  - supports reference-site cloning onto GEOFlow modules
  - supports auditing, optimizing, and incrementally adjusting the current template
  - supports preview-first theme-package and optimization-pass outputs
- Added Chinese and English documentation:
  - `docs/skills/yao-geoflow-design.md`
  - `docs/skills/yao-geoflow-design.en.md`
- Updated the repository homepage and `registry/skills.json` so `yao-geoflow-design` is part of the public catalog

## 2026-04-18

### Initial publication of `geoflow-template` (current name: `yao-geoflow-template`)

- Initially published as `skills/geoflow-template`; the public package now lives at `skills/yao-geoflow-template`
- Added frontend template-cloning and theme-package planning support:
  - built around GEOFlow frontend modules, variables, and rendering contracts
  - maps a reference URL into a GEOFlow-compatible theme package plan
  - supports preview-first output targets such as `tokens.json`, `mapping.json`, and `manifest.json`
- Added Chinese and English documentation:
  - `docs/skills/yao-geoflow-template.md`
  - `docs/skills/yao-geoflow-template.en.md`
- Updated the repository homepage and `registry/skills.json` so the skill is part of the public catalog
