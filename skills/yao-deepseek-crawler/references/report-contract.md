# Report Contract

## Canonical Dataset

Stage 1 writes `deepseek-crawl.json`:

```json
{
  "schema_version": "yao-deepseek-crawler/v1",
  "run": {"id": "...", "started_at": "...", "finished_at": "...", "transport": "batch-orchestrator", "sample_transports": []},
  "input": {
    "question_count": 10,
    "global_repeat": 5,
    "target_entity": "新东方",
    "target_aliases": ["新东方前途出国", "前途出国"],
    "entity_type": "company",
    "delay_strategy": {},
    "questions": []
  },
  "plan": [],
  "samples": [],
  "totals": {}
}
```

The run-level `transport` names the neutral batch wrapper. `sample_transports` lists the concrete transports observed in completed sample results.

Each sample keeps:

- `sample_id`, `question_id`, `question`, `repeat_index`
- `ok`, `status`, `started_at`, `finished_at`, `duration_ms`
- `raw_path`, `log_path`, `error`
- `result`, the normalized DeepSeek crawler JSON

The analyzer also accepts the existing `opencli-boss-ai` aggregate shape with top-level `results[]`.

## Analysis Outputs

Stage 2 writes these analysis artifacts in the selected report directory:

- `summary.json`: machine-readable metric summary used by all downstream artifacts.
- `structured-data.md`: Markdown export of cleaned fields and data tables.
- `structured-data.xlsx`: Excel workbook with the same structured tables as the Markdown export.
- `report.html`: Kami-styled visual diagnosis and analysis report.
- `semantic-review-cache.json`: optional AI semantic-review cache, written when AI review produces reusable candidate classifications.

The structured Markdown and Excel workbook must be generated from the same summary object as the HTML report. They should include output file paths, overview fields, semantic review status, question coverage, target metrics, same-type entity comparison, question-by-entity metrics, entity recognition candidates, AI semantic labels and reasons, source/channel tables, frequent domains/sources/URLs/titles, title-feature buckets, and other cleaned fields that feed the visible report. The raw crawl JSON remains the audit source of truth; the structured exports are analysis-stage derivatives.

## Metric Definitions

- `planned_samples`: question count x repeat count.
- `completed_samples`: samples that finished with a raw result or a captured failure.
- `valid_samples`: completed samples with `ok=true` and non-empty answer text.
- `failed_samples`: completed samples with `ok=false` or empty answer text.
- `pending_samples`: planned samples that do not yet have a sample record, usually from an interrupted run.
- `completion_rate = completed_samples / planned_samples`.
- `valid_rate = valid_samples / planned_samples`.
- `answer_chars`: sum of answer text length across valid samples.
- `reference_count`: total number of displayed DeepSeek source-panel references.
- `unique_urls`: unique cited URLs.
- `unique_domains`: unique cited domains.

## Target Entity Recognition

Standard mode: user supplies four inputs:

- `keywords/questions`: one or more DeepSeek questions.
- `repeat`: how many times each keyword should be queried.
- `target_entity`: the target entity to diagnose.
- `entity_type`: one of `person`, `company`, or `product`.

The target entity uses contains matching plus aliases. For example, `target_entity = 新东方` can merge `新东方前途出国` and `前途出国` into the target row when those aliases are supplied or extracted from the answers.
Short Latin aliases such as `AI` or `GEO` only match standalone tokens, not substrings inside longer names such as `PallasAI` or `GEOFlow`.

Preferred mode: user supplies a canonical target row and same-type competitor rows with aliases. The same `brands.txt` format is reused for companies, people, or products.

Fallback mode: infer same-type competitor entities from answer headings, list rows, person-role context, organization/product suffixes, and cited source titles. The analyzer classifies each candidate as:

- `person`
- `company`
- `product`
- `concept`
- `noise`

Entity recognition uses a local hybrid NER gate:

1. Generate candidate spans from answer headings, role patterns, organization/product suffixes, English brand-like tokens, and source titles.
2. Normalize context fragments before scoring. For example, `那么启德教育` becomes `启德教育`, and `在像指南者留学这类机构` becomes `指南者留学`.
3. Reject attributes, categories, qualification phrases, title-intent fragments, and generic descriptors before metric calculation.
4. Score entity surface quality separately from evidence quality. Strong legal/organization suffixes score higher than weak suffixes such as `教育` or `留学`; weak suffixes require a clean brand-like prefix.
5. Inferred competitors must pass type consistency, minimum repeated-sample count, answer-body evidence, surface score, and evidence score gates. Source-title-only names remain in source/title analysis but do not create competitor rows.
6. Keep regression examples for both false positives and false negatives in `scripts/test_entity_recognition.py`.

When a target entity is supplied, the analyzer can add AI semantic review after local candidate recall. Semantic review is optional and does not replace raw logs or hard-rule evidence.

Semantic review modes:

- `--semantic-review auto`: default. Use AI when `OPENAI_API_KEY` is available; otherwise fall back to local rules and write `semantic_review_status: fallback`.
- `--semantic-review required`: fail analysis if AI review is unavailable, incomplete, or invalid. Use this for formal report delivery.
- `--semantic-review off`: skip AI review and use local rules only.
- `--semantic-confidence-threshold`: default `0.72`.
- `--semantic-review-cache`: default `<out-dir>/semantic-review-cache.json`.

Semantic labels are fixed:

- `target_alias`
- `direct_competitor`
- `generic_category`
- `attribute`
- `service_or_feature`
- `source_or_title`
- `unrelated_entity`
- `uncertain`

AI review receives a candidate context containing the target entity, target aliases, declared entity type, keywords, candidate name, candidate aliases, rule classification, sample count, evidence counters, evidence scores, and answer-body snippets. It must return strict JSON with label, same-type flag, direct-competitor flag, confidence, normalized name, recommended action, and a short reason.

Competitors may enter metric calculation only when all of these are true:

- the local rule layer does not mark the candidate as noise, generic category, attribute, service/feature, or source/title-only
- the candidate is a concrete `person`, `company`, or `product`
- the candidate type matches the target entity type
- the candidate has answer-body evidence, not only source-title evidence
- sample count and local surface/evidence scores pass the local gates
- if AI review is enforced, the AI label is `direct_competitor`, `is_same_type = true`, `is_direct_competitor = true`, and `confidence >= 0.72`

`summary.json`, `structured-data.md`, `structured-data.xlsx`, and the HTML entity-recognition table must expose semantic review status plus these candidate fields: AI semantic label, same-type flag, direct-competitor flag, whether the candidate entered the competitor matrix, semantic confidence, source (`ai`, `cache`, `heuristic`, or `off`), recommended action, and reason. Excluded candidates and reasons must remain visible for audit.

Standard target type is controlled by `--entity-type`:

- `person` / `人`: only people enter target-vs-competitor metrics.
- `company` / `公司`: only companies, brands, institutions, and organizations enter target-vs-competitor metrics.
- `product` / `产品`: only products, tools, platforms, software, apps, and models enter target-vs-competitor metrics.

Legacy exploratory mode may use `--target-kind auto/person/company/product/mixed`, but final reports should provide `--target-entity` and `--entity-type`.

The report must show the classification table so excluded concepts or noise can be audited.

## Entity Ranking

Preferred mode: user supplies a target entity, target aliases, and same-type competitor aliases.

Fallback mode: infer same-type competitor entities and label metrics as lower-confidence candidates.

For each valid sample:

1. Find the target entity and each same-type competitor's earliest alias position in the answer.
2. Sort mentioned entities by earliest position.
3. Assign ranks from 1.

Global entity metrics:

- `mention_rate = mentioned_samples / valid_samples`
- `mention_total`: number of alias mentions across valid samples where the entity appears.
- `avg_mentions_per_sample = mention_total / valid_samples`.
- `avg_mentions_per_mentioned_sample = mention_total / mentioned_samples`.
- `top1_rate = top1_samples / valid_samples`
- `top3_rate = top3_samples / valid_samples`
- `top5_rate = top5_samples / valid_samples`
- `average_rank = average(rank) among mentioned samples`
- `dominant_sentiment`: `positive`, `neutral`, or `negative`, inferred from local text around entity mentions.
- `negative_rate = negative entity mention contexts / sentiment_total`.

Missing entities count as not mentioned, not as infinite rank. Show mention rate next to rank so absence is visible.
Sentiment is heuristic and should be treated as a directional signal, not a human-reviewed judgment.

Target-vs-competitor comparison:

- Always put the target entity first when it has metrics.
- Compare only competitors with the same `entity_type`.
- Competitors must be named entities, not attributes, categories, policy/qualification descriptions, title-intent fragments, or generic descriptors. Exclude phrases such as `教育部首批认证机构`, `首批认证机构`, `上市公司`, `A股上市集团`, `头部留学机构`, `大型教育集团`, `国有企业`, `海外留学`, `2026留学中介机构`, `对留学`, or `本地服务商` from the entity pool unless the user explicitly provides them as aliases for a real named entity.
- Inferred competitors should come from answer-body evidence, not source-title-only mentions. Source titles remain part of source and title-feature analysis, but they should not create target-vs-competitor rows unless the same entity is also present in the answer text or explicitly provided by the user.
- Show `mention_rate`, `avg_mentions_per_sample`, `top1_rate`, `top3_rate`, `top5_rate`, `average_rank`, `reference_mentions`, `gap_vs_target_top3`, and `gap_vs_target_top5`.
- Use a benchmark radar for target entity plus the Top 3 competitors. Convert each radar axis to a 0-100 score where the best value among same-type benchmark entities is 100.
- Use a bubble benchmark where x-axis is Top 5 probability, y-axis is mention rate, bubble size is average mentions, and the target entity is visually highlighted. Render bubbles as solid filled circles without visible outline strokes. Use a compact same-family palette so each shown entity has a legend swatch below the chart. Do not show entity labels by default; reveal a compact label only on click or keyboard focus, with native tooltip fallback.
- Default detail cap is 10 rows: target plus up to 9 competitors.

## Source And Channel Analysis

Flatten every `references.items[]` row. Preserve `number`, `source`, `source_origin`, `domain`, `title`, `title_origin`, `date`, `url`, `summary`, and `summary_origin`. Origin fields distinguish browser-observed values from URL-derived labels and nearby answer context. Structured Markdown and Excel outputs must retain every reference row and these origin fields.

Channel classifier is heuristic:

- `official`: government, school, organization, official company domains
- `academic`: arXiv, DOI, ACM, journal, university research pages
- `media`: news and portal media
- `community`: Zhihu, Xiaohongshu, forums, social posts
- `commerce`: ecommerce, marketplace, local services
- `encyclopedia`: Baike, Wikipedia, wiki-like pages
- `developer`: developer docs, cloud community, technical blogs
- `other`: unclassified

The report should show top domains, top source names, channel share, repeated URLs/titles, source-position distribution, and a compact domain-share treemap.
Domain rows should include a readable Simplified Chinese display name when it can be inferred from the DeepSeek source label or a maintained domain-name mapping.
High-frequency URLs and repeated titles must preserve their URLs and render as clickable links in the HTML report.
High-frequency domain charts should use a compact source-row layout: primary readable name, secondary domain, bar, and count-only numeric column. High-frequency URL charts should show each URL only once as the clickable primary label, then the bar and count; do not repeat the same URL as a secondary line. Compact URL labels should retain enough path tail to distinguish same-domain/same-directory pages, while the full URL remains the link target and hover title. Long domains and URLs must ellipsize inside the label area, not expand the numeric column.
The `信源结构` chart order is fixed: first row `渠道分布`, `来源编号位置`, `高频来源名`; second row `高频域名`, `域名占比树图`, `高频 URL`.
The domain-share treemap should use small domain text, stable compact cards, ellipsis for long domains, and a count/mini-bar so it does not compete with body typography.

## Title Features

For every browser-observed cited title, compute the following features. Exclude `title_origin = url-derived` labels from title metrics and repeated-title aggregates while retaining them in reference and URL tables.

- length bucket
- has number
- has date or year
- has question punctuation
- has bracket or colon
- contains a supplied or inferred target/competitor alias
- title intent buckets such as ranking/list, comparison/evaluation, recommendation/choice, risk avoidance, guide/how-to, trend/news, profile/introduction, and research/paper

Use these as patterns, not proof of quality.
Do not duplicate the high-frequency cited-title table with another repeated-title chart. Use the second title chart slot for title intent analysis instead.

## Kami Report Rules

The HTML report is a high-trust analysis artifact:

- start with `报告概览`, including a numeric overview paragraph, directory links, and metric explanations
- default to Simplified Chinese, with a top-right language toggle for English overview, key findings, metric notes, and GEO recommendations
- each large module should have a short summary paragraph before charts/tables
- detail lists and tables should show no more than 10 rows by default unless the user asks for more
- include a fixed top navigation bar with a text logo/title and anchor links
- label the target-vs-competitor nav item as `竞品分析`, and include a separate `总结建议` nav anchor
- include sentiment analysis, average mention count, and Top 5 probability alongside the original mention, rank, Top 1, Top 3, and source metrics
- render the target sentiment mix as a compact donut chart because it has three part-whole categories: positive, neutral, and negative; keep the donut centered, place the category percentages and counts below the chart, and never let numeric columns overflow into adjacent cards
- render compact part-whole source modules, especially channel distribution and citation-position buckets, as centered donut charts with the category percentages and counts below the chart instead of right-side number columns
- source module bucket labels should stay readable in Simplified Chinese where possible, including `unknown` source-position buckets as `未识别`
- use multiple chart types where they help comparison: bars, stacked bars, normalized radar, benchmark bubble, lollipop, heatmap/matrix, and treemap
- do not show the old target ranking funnel card under `目标实体概率`
- do not show the old neutral-or-better visible primary metric; show dominant sentiment and negative share instead
- render time-recency buckets in Simplified Chinese labels, such as `本年`, `近一年`, `更早`, and `未识别`
- add a `总结建议与 GEO 优化措施` block after high-frequency cited titles, including an optimization-priority chart, a conservative before/after/monthly trend projection for core metrics, a method/check table, and six concise recommendation cards so the desktop 3-column grid completes cleanly
- show the hero `实体口径` note on a new line so the target/competitor recognition rule is scannable
- keep radar and bubble chart strokes light enough that overlapping series remain readable
- warm parchment background `#f5f4ed`
- ink-blue accent `#1B365D`
- warm grays only
- serif-led hierarchy
- solid tag backgrounds, no rgba
- compact metrics and tables
- charts must be readable without JavaScript
- every conclusion must trace back to a visible metric or table

Do not include absolute local filesystem paths in the HTML body. Put local file paths in the final assistant response, not inside the report artifact.
