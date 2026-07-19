# Yao DeepSeek Crawler

Simplified Chinese documentation is the default entry: [README.md](README.md)

`yao-deepseek-crawler` turns repeated DeepSeek web AI-search samples into GEO probability evidence. It uses a local OpenCLI Browser Bridge and an already logged-in DeepSeek web session, preserves raw evidence, and generates structured Markdown, Excel, and Kami-styled HTML diagnostic reports.

## What It Is For

- Run repeated samples for 1-20 keywords or questions.
- Preserve every DeepSeek answer, source-panel reference, raw JSON file, and execution log.
- Analyze one target entity with a declared entity type, then compare it with same-type competitors.
- Aggregate mention rate, average mention count, average rank, Top 1 / Top 3 / Top 5 probability, sentiment tendency, source structure, title features, repeated citations, and target-vs-competitor gaps.
- Produce four deliverables: canonical crawl JSON, structured Markdown, structured Excel workbook, and a visual HTML report.

It is not a generic website crawler and does not use the DeepSeek API.

## Requirements

- Node.js 21+ for live crawling; Node.js 18+ for analysis-only usage
- Python 3.10+
- OpenCLI CLI 1.8.4+
- OpenCLI Browser Bridge connected to a Chrome or Edge profile
- Logged-in DeepSeek web session
- Local DeepSeek browser crawler script bundled at `scripts/geo-deepseek-browser-direct.mjs`, or a custom path passed with `--crawler-script`
- Optional `OPENAI_API_KEY` for analysis-stage AI semantic review. Without it, the default mode falls back to local rules.

Detailed setup guide:

- [references/user-setup-and-usage.md](references/user-setup-and-usage.md)

## Connect Browser Bridge

If `opencli profile list` shows no connected profile, run this command from the skill directory:

```bash
node scripts/setup_deepseek_bridge.mjs
```

This helper opens `https://chat.deepseek.com/` only. Do not use Browser Bridge setup scripts from other projects such as `opencli-boss-ai`, because they may open their own target sites.

## Standard Inputs

```text
1. Keywords: one or more DeepSeek search questions
2. Repeat count: how many times to query each keyword
3. Target entity: for example New Oriental, Yao Jingang, a product name, or a company name
4. Entity type: person, company, or product
5. OpenCLI profile: connected Browser Bridge profile
6. Crawl interval: for example random 1-3 minutes, or safer random 5-20 minutes
```

Target aliases are optional but recommended:

```text
Target entity aliases:
Mr. Yao Jingang, Teacher Yao Jingang, Yao Jingang xx, etc.
```

## Preflight

For live crawling:

```bash
node scripts/preflight.mjs --profile <opencli-profile>
```

For report generation from an existing JSON file:

```bash
node scripts/preflight.mjs --analysis-only
```

## Stage 1: Batch Crawl

Create `questions.txt`, one question per line:

```text
新能源汽车推荐
豪华新能源SUV品牌推荐
哪个新能源电车品牌更靠谱
推荐一款靠谱的新能源汽车品牌
```

Then run:

```bash
node scripts/deepseek_batch_crawl.mjs \
  --questions questions.txt \
  --repeat 5 \
  --profile <opencli-profile> \
  --target-entity "蔚来" \
  --target-aliases "蔚来ES8,蔚来ES6,蔚来EC6,NIO" \
  --entity-type product \
  --delay-min-minutes 1 \
  --delay-max-minutes 3 \
  --safe-random-delay \
  --out-dir runs/nio-nev
```

Crawl outputs:

- `runs/nio-nev/deepseek-crawl.json`
- `runs/nio-nev/raw/*.json`
- `runs/nio-nev/logs/*.log`

Use `--dry-run` to check the plan without opening DeepSeek. For real long-running sampling, prefer `--safe-random-delay`, which defaults to a random 5-20 minute wait between fresh sessions. For short controlled tests, use `--delay-min-minutes 1 --delay-max-minutes 3`.

## Stage 2: Analyze And Render

Optional `brands.txt` helps manually review target aliases and competitor naming:

```text
蔚来|蔚来ES8|蔚来ES6|蔚来EC6|NIO
问界|AITO|问界M9|问界M7
理想汽车|理想L9|理想L8|理想L7
特斯拉|Tesla|Model Y|Model 3
```

Generate structured data and the HTML report:

```bash
python3 scripts/analyze_deepseek_results.py \
  runs/nio-nev/deepseek-crawl.json \
  --target-entity "蔚来" \
  --target-aliases "蔚来ES8,蔚来ES6,蔚来EC6,NIO" \
  --entity-type product \
  --brands-file brands.txt \
  --semantic-review auto \
  --out-dir runs/nio-nev/report
```

Analysis outputs:

- `runs/nio-nev/report/summary.json`
- `runs/nio-nev/report/structured-data.md`
- `runs/nio-nev/report/structured-data.xlsx`
- `runs/nio-nev/report/report.html`
- `runs/nio-nev/report/semantic-review-cache.json`, written when AI semantic review produces cacheable results

The standard report requires `--target-entity` and `--entity-type`. Entity type accepts `person/人`, `company/公司`, or `product/产品`. Target matching uses contains logic plus aliases, so target `蔚来` can consolidate aliases such as `蔚来ES8`, `蔚来ES6`, and `NIO`. Short Latin aliases are matched as standalone tokens to avoid accidental matches inside longer words. Competitors are limited to the same entity type as the target.

Analysis supports optional AI semantic review:

- `--semantic-review auto`: default mode. Use AI when available; if the API key is missing or the call fails, fall back to local rules and record `semantic_review_status: fallback` in `summary.json`.
- `--semantic-review required`: recommended before formal delivery. Analysis fails if AI review is unavailable, incomplete, or unparsable.
- `--semantic-review off`: use local rules only.
- `--semantic-confidence-threshold 0.72`: minimum confidence for AI-reviewed direct competitors.
- `--semantic-review-cache <path>`: cache path, defaulting to `semantic-review-cache.json` under the report directory.

Semantic review is an enhancement layer, not a replacement for raw logs, answer-body evidence, or hard rules. A competitor must still pass noise filtering, same-type checks, confidence gates, and answer-body evidence before it enters the competitor matrix. The report and structured exports preserve the AI semantic label, same-type flag, matrix inclusion decision, confidence, reason, and exclusion cause.

## Report Capabilities

The HTML report defaults to Simplified Chinese and includes an English summary toggle. It covers:

- Overview, table of contents, and metric definitions
- Core conclusions and target entity performance
- Target entity vs same-type competitor comparison
- Sentiment mentions, entity recognition, AI semantic review, and crawl coverage
- Probability ranking, Top 1 / Top 3 / Top 5, and average rank
- Channel distribution, source index position, frequent source names, frequent domains, and frequent URLs
- Title functional features, title length, freshness, and title intent
- GEO recommendations, optimization priorities, trend projection, and concrete execution methods

## Real NIO Sampling Example

The example is based on a real DeepSeek web sampling run on 2026-06-20:

- Keywords: 4
- Repeats per keyword: 5
- Planned samples: 20
- Successful samples: 20
- Failed samples: 0
- Source references: 199
- Target entity: NIO / 蔚来
- Aliases: 蔚来 ES8, 蔚来 ES6, 蔚来 EC6, NIO, etc.

Example files:

- [Question list](examples/nio-nev-deepseek-20260620/questions.txt)
- [Brand alias table](examples/nio-nev-deepseek-20260620/brands.txt)
- [Canonical crawl JSON](examples/nio-nev-deepseek-20260620/deepseek-crawl.json)
- [Brand/company Markdown](examples/nio-nev-deepseek-20260620/report-brand-company/structured-data.md)
- [Brand/company Excel](examples/nio-nev-deepseek-20260620/report-brand-company/structured-data.xlsx)
- [Brand/company HTML report](examples/nio-nev-deepseek-20260620/report-brand-company/report.html)
- [Product-scope HTML report](examples/nio-nev-deepseek-20260620/report/report.html)
- [Single-run raw samples](examples/nio-nev-deepseek-20260620/raw)
- [Single-run logs](examples/nio-nev-deepseek-20260620/logs)

## Offline Verification

```bash
bash scripts/run-tests.sh
```

## Boundaries

- This skill does not handle DeepSeek login, captchas, Cloudflare, bot checks, account risk control, or platform-limit bypassing.
- Probability metrics are repeated-sampling estimates, not market share or official platform ranking.
- Competitor entity recognition should prefer user-reviewed aliases; automatically recognized candidates still require human review. For formal reports, prefer `--semantic-review required`.
- AI semantic review is optional and does not override hard rules, answer-body evidence gates, or raw-log auditability.
- Live crawling opens browser windows and visits DeepSeek web pages. Follow the target website rules and account usage limits.

## Package Map

- `SKILL.md`: route trigger and workflow skeleton
- `references/user-setup-and-usage.md`: install prerequisites and end-user runbook
- `references/deepseek-crawl-workflow.md`: local crawler setup and crawl rules
- `references/report-contract.md`: JSON contract and metric definitions
- `scripts/preflight.mjs`: dependency and login-state checker
- `scripts/setup_deepseek_bridge.mjs`: DeepSeek-specific OpenCLI Browser Bridge setup helper
- `scripts/geo-deepseek-browser-direct.mjs`: bundled DeepSeek answer and citation-evidence collector
- `scripts/deepseek_batch_crawl.mjs`: repeated crawl orchestrator
- `scripts/test_geo_deepseek_browser_direct.mjs`: regression coverage for wrong-page rejection and browser-session cleanup
- `scripts/run-tests.sh`: offline verification entrypoint
- `scripts/analyze_deepseek_results.py`: aggregation and HTML rendering
- `fixtures/sample-deepseek-crawl.json`: offline test fixture
