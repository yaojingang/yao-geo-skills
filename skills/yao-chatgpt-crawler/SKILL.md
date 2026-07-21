---
name: yao-chatgpt-crawler
description: "Use when a user provides ChatGPT web AI-search keywords, repeat count, target entity, entity type, OpenCLI profile, and crawl interval preference, then needs repeated crawls aggregated into JSON plus a Kami HTML GEO report. Not for generic crawling, ChatGPT API chat, SEO writing, or one-off answers."
---

# Yao ChatGPT Crawler

## Inputs

Questions, repeat count, target entity/type (`person/company/product`), browser profile, delay preset, optional output directory, and same-type competitors.

Use random `30s-1m` by default; support `1-3m` and `3-10m` when requested.

## Workflow

1. Read `references/user-setup-and-usage.md`, `references/chatgpt-crawl-workflow.md`, and `references/report-contract.md` as needed.
2. Run `node scripts/preflight.mjs --profile <profile>` before fresh crawling.
3. Stage 1: run `scripts/chatgpt_batch_crawl.mjs` with questions, repeat, profile, target entity/type, interval preset, and output dir.
4. Stage 2: run `scripts/analyze_chatgpt_results.py`. Follow the competitor-review rules in the workflow reference; a target-only alias file never disables inference.
5. Return crawl JSON, summary, structured Markdown/Excel, HTML report, optional semantic-review cache, and failed logs.

## Honest Boundaries

- Reuses local ChatGPT web automation; does not bypass login, bot checks, or hidden data.
- Visible ChatGPT citations bound source analysis; probability metrics are repeated-sample estimates.
- Inferred competitors are heuristic. Review aliases before external use; use `--semantic-review required` when formal-report confidence demands it.
- The entity table is an audit surface; only rows entering the competitor matrix affect metrics.
- Preserve raw answers, reference titles, URLs, and logs so every conclusion can be audited.
