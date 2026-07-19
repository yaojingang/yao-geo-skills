# User Setup And Usage

This guide is for a user who has just installed `yao-deepseek-crawler` and wants to run real DeepSeek web crawls.

## What This Skill Needs

Fresh crawling requires local browser automation. The skill does not install OpenCLI, log in to DeepSeek, solve CAPTCHA, or bypass account checks.

Required for fresh crawls:

- Node.js 21+.
- Python 3.10+.
- OpenCLI CLI 1.8.4+ available as `opencli`.
- OpenCLI Browser Bridge extension connected to a Chrome or Edge profile.
- A logged-in DeepSeek web session in that connected profile.
- A DeepSeek browser crawler script. This skill bundles `scripts/geo-deepseek-browser-direct.mjs` by default; if your crawler is elsewhere, pass `--crawler-script <file>` or set `DEEPSEEK_CRAWLER_SCRIPT`.

Required for analysis-only usage:

- Node.js 18+.
- Python 3.10+.
- An existing `deepseek-crawl.json` or compatible DeepSeek raw JSON.
- Optional `OPENAI_API_KEY` if you want AI semantic review for competitor entities. Without it, `--semantic-review auto` uses local-rule fallback.

## 0. Connect Browser Bridge

If `opencli profile list` says no Browser Bridge profiles are connected, start a DeepSeek-specific browser profile from the skill directory:

```bash
node scripts/setup_deepseek_bridge.mjs
```

This setup opens `https://chat.deepseek.com/` only. Do not use setup scripts from other OpenCLI projects, such as `opencli-boss-ai`, because those scripts may open their own target sites.

## 1. Run Preflight

From the skill directory:

```bash
node scripts/preflight.mjs --profile <opencli-profile>
```

If the crawler script is not in the default local path:

```bash
node scripts/preflight.mjs \
  --profile <opencli-profile> \
  --crawler-script /absolute/path/to/geo-deepseek-browser-direct.mjs
```

For report generation from an existing JSON only:

```bash
node scripts/preflight.mjs --analysis-only
```

Preflight must pass before a fresh crawl. If it fails, fix the failed checks first.

## 2. Prepare Questions

Before running a standard report, prepare these four inputs:

```text
1. 关键词：one or more DeepSeek questions, one per line
2. 轮询次数：how many times each keyword should be queried
3. 目标实体：the entity to diagnose, for example 新东方、姚金刚、某产品名、某公司名
4. 实体类型：人, 公司, or 产品
```

Create a questions file with one keyword/question per line:

```text
出国留学公司推荐
出国留学机构
出国留学机构哪家好
出国留学公司哪家好
出国留学哪家靠谱
```

JSON input is also accepted:

```json
[
  {"id": "q01", "question": "出国留学公司推荐", "repeat": 5},
  {"id": "q02", "question": "出国留学机构", "repeat": 5}
]
```

## 3. Prepare Target Entity Aliases

The target entity and entity type are required for standard reports. Entity aliases make Top 1, Top 3, mention rate, and average-rank metrics more reliable.

User-facing alias prompt:

```text
目标实体别名：
例如 姚金刚先生、姚金刚老师、姚金刚xx等
```

Target matching uses contains logic plus aliases. If the target entity is `新东方`, aliases or extracted names such as `新东方前途出国` and `前途出国` can be merged into the target row. Short Latin aliases such as `AI` or `GEO` only match standalone tokens, not longer names. Competitors are kept only when they match the same entity type.

Company example `brands.txt`:

```text
启德教育|启德留学|启德
新东方前途出国|新东方|前途出国
指南者留学|指南者
优越留学|优越教育
```

Person example `experts.txt`:

```text
卢鑫|Echo Lu|Echo
孟庆涛
罗小军
李德仁
曲腾腾
```

If no entity file is supplied, the analyzer infers same-type competitors from the question wording and AI answer context. Use inferred competitors for exploration; use a reviewed alias file for final reporting.

## 4. Dry Run

Check the plan before opening DeepSeek:

```bash
node scripts/deepseek_batch_crawl.mjs \
  --questions questions.txt \
  --repeat 5 \
  --profile <opencli-profile> \
  --target-entity "新东方" \
  --entity-type company \
  --out-dir runs/my-deepseek-run \
  --dry-run
```

Expected output should show the planned sample count. Five questions repeated five times should produce 25 samples.
Dry-run only validates the plan and target fields; it does not require the crawler script, OpenCLI profile, or DeepSeek page to be available. Real crawling still requires all fresh-crawl prerequisites.

## 5. Run Fresh Crawl

For real DeepSeek web runs, use the safe random delay mode:

```bash
node scripts/deepseek_batch_crawl.mjs \
  --questions questions.txt \
  --repeat 5 \
  --profile <opencli-profile> \
  --target-entity "新东方" \
  --target-aliases "新东方前途出国,前途出国" \
  --entity-type company \
  --out-dir runs/my-deepseek-run \
  --safe-random-delay \
  --timeout 300
```

`--safe-random-delay` waits a random 5-20 minutes between fresh samples. Five questions repeated five times means 25 samples and 24 waits, so the waiting time alone is usually around 2-8 hours. This lowers request frequency but does not guarantee account safety or bypass platform risk controls.

Use a custom random interval when needed:

```bash
node scripts/deepseek_batch_crawl.mjs \
  --questions questions.txt \
  --repeat 5 \
  --profile <opencli-profile> \
  --target-entity "新东方" \
  --entity-type company \
  --out-dir runs/my-deepseek-run \
  --delay-min-minutes 5 \
  --delay-max-minutes 20
```

If your crawler script is outside the default path:

```bash
node scripts/deepseek_batch_crawl.mjs \
  --questions questions.txt \
  --repeat 5 \
  --profile <opencli-profile> \
  --target-entity "新东方" \
  --entity-type company \
  --crawler-script /absolute/path/to/geo-deepseek-browser-direct.mjs \
  --safe-random-delay \
  --out-dir runs/my-deepseek-run
```

Outputs:

- `runs/my-deepseek-run/deepseek-crawl.json`
- `runs/my-deepseek-run/raw/*.json`
- `runs/my-deepseek-run/logs/*.log`

Each sample opens a fresh DeepSeek browser session name. Keep the run single-threaded unless the underlying crawler explicitly supports concurrency.

## 6. Resume Interrupted Runs

If the run stops midway, rerun the same command with `--resume`:

```bash
node scripts/deepseek_batch_crawl.mjs \
  --questions questions.txt \
  --repeat 5 \
  --profile <opencli-profile> \
  --target-entity "新东方" \
  --entity-type company \
  --out-dir runs/my-deepseek-run \
  --resume
```

Resume only reuses raw JSON when it is valid, successful, has answer text, and matches the current question.

## 7. Generate The Report

```bash
python3 scripts/analyze_deepseek_results.py \
  runs/my-deepseek-run/deepseek-crawl.json \
  --target-entity "新东方" \
  --target-aliases "新东方前途出国,前途出国" \
  --entity-type company \
  --brands-file brands.txt \
  --semantic-review auto \
  --title "DeepSeek 搜索概率分析报告" \
  --out-dir runs/my-deepseek-run/report
```

Outputs:

- `runs/my-deepseek-run/report/summary.json`
- `runs/my-deepseek-run/report/structured-data.md`
- `runs/my-deepseek-run/report/structured-data.xlsx`
- `runs/my-deepseek-run/report/report.html`
- `runs/my-deepseek-run/report/semantic-review-cache.json` when AI semantic review produces cacheable results

The analyzer keeps `summary.json` as a machine-readable metric summary. `structured-data.md` and `structured-data.xlsx` contain the same cleaned structured tables: output file list, overview fields, question coverage, target metrics, same-type entity comparison, question-by-entity metrics, entity recognition candidates, semantic review labels and reasons, source/channel tables, frequent domains/sources/URLs/titles, and title-feature buckets. The HTML report defaults to Simplified Chinese and includes a top-right language toggle for English overview analysis. It starts with a numeric overview, directory, and metric explanations. It then includes core conclusions, target-vs-competitor comparison, sentiment analysis, average mention count, sample coverage, target entity recognition, mention probability, Top 1 / Top 3 / Top 5 probability, average rank, source channels, repeated domains, clickable repeated URLs/titles, title-feature charts, and GEO optimization recommendations. Domain displays use readable Chinese names where available. High-frequency URL rows show one clickable compact label per row, keep the full URL as link target/hover title, and avoid visually duplicated URL lines. GEO recommendations include priority bars, a conservative core-metric trend projection, method/check tables, and concise action cards. Detail lists are capped at 10 rows by default.

Semantic review options:

- `--semantic-review auto`: default. AI review runs when `OPENAI_API_KEY` is available. If AI is unavailable or fails, the analyzer falls back to local rules and records `semantic_review_status: fallback`.
- `--semantic-review required`: recommended for formal delivery. The analyzer fails if AI review is unavailable, incomplete, or invalid.
- `--semantic-review off`: only local rules are used.
- `--semantic-confidence-threshold 0.72`: minimum confidence for AI-reviewed direct competitors.
- `--semantic-review-cache <path>`: optional cache path; default is `semantic-review-cache.json` in the report directory.

Semantic review does not replace raw evidence. A competitor must still pass the local hard gates: not noise, not a generic category or attribute phrase, same entity type as the target, enough confidence, and at least one answer-body evidence snippet rather than source-title-only evidence.

Target type can be forced:

```bash
python3 scripts/analyze_deepseek_results.py \
  runs/my-deepseek-run/deepseek-crawl.json \
  --target-entity "孟庆涛" \
  --entity-type person \
  --out-dir runs/my-deepseek-run/report
```

Accepted standard entity types are `person/人`, `company/公司`, and `product/产品`.

## 8. Troubleshooting

| Symptom | Likely Cause | Fix |
|---|---|---|
| `opencli: command not found` | OpenCLI is not installed or not on `PATH`. | Install OpenCLI and verify `opencli --version`. |
| `No Browser Bridge profiles connected` | Browser extension is not connected. | Run `node scripts/setup_deepseek_bridge.mjs`, then run `opencli profile list`. |
| `Browser profile ... is not connected` | The selected profile is offline. | Use `opencli profile list`, then pass a connected profile with `--profile`. |
| `logged_in: false` | DeepSeek is not logged in. | Log in to DeepSeek in the connected browser, then run `opencli deepseek whoami -f json`. |
| `Crawler script not found` | The default local crawler path does not exist. | Pass `--crawler-script <file>` or set `DEEPSEEK_CRAWLER_SCRIPT`. |
| `Semantic review is required, but OPENAI_API_KEY is not set` | `--semantic-review required` was used without an AI API key. | Set `OPENAI_API_KEY`, use a valid semantic-review cache, or rerun with `--semantic-review auto/off` for exploratory analysis. |
| `references.count = 0` | DeepSeek source panel did not render, search was off, or DOM changed. | Confirm search mode, rerun one sample, and inspect the per-sample log. |
| Many samples fail after several successes | Browser bridge, account throttling, DeepSeek page instability, or platform risk controls. | Stop the run, wait before retrying, use `--safe-random-delay` or wider custom random intervals, rerun with `--resume`, and inspect failed logs. |

## Evidence And Privacy

The run directory stores raw DeepSeek answers, source titles, URLs, and logs. Treat it as audit evidence. Do not publish or commit run outputs if the questions, answers, or sources contain private or client-sensitive information.
