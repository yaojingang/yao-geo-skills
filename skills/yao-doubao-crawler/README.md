# Yao Doubao Crawler

`yao-doubao-crawler` turns repeated Doubao AI-search crawls into GEO probability evidence.

It is designed for jobs like:

- 1-20 keywords/questions, each crawled repeatedly in a fresh Doubao web session or a low-frequency Android Appium session.
- Keep every raw answer plus visible Doubao URLs or compatible reference rows.
- Diagnose one target entity with a declared entity type, then compare it with same-type competitors extracted from AI answers.
- Run collection-only or exploratory analysis when no target entity is supplied; these reports label inferred candidates as heuristic instead of target metrics.
- Aggregate visibility, average mention count, average rank, Top 1 / Top 3 / Top 5 probability, sentiment tendency, source/channel mix, title patterns, repeated citations, and target-vs-competitor gaps.
- Generate a canonical JSON dataset, structured Markdown, structured Excel workbook, and a Kami-styled HTML report.

It is not a generic website crawler and does not use the Doubao API. The Android backend does not bypass login, CAPTCHA, risk controls, hidden APIs, or app network traffic.

## Requirements

- Node.js 18+
- Python 3.10+
- OpenCLI CLI 1.8.4+
- OpenCLI Browser Bridge connected to a Chrome or Edge profile
- Logged-in Doubao web session that can send messages from the connected browser profile
- Bundled crawler at `scripts/doubao_browser_crawl.mjs`, or pass `--crawler-script`

Optional for Android/Appium mobile crawling:

- Android SDK Platform-Tools with `adb`
- Android Emulator command line tools with a configured AVD, or a USB-debuggable Android device
- Appium 3 with the UiAutomator2 driver
- Python dependency from `requirements-mobile.txt`
- Doubao Android APK installed and logged in on the selected device

Start with the user setup guide:

- `references/user-setup-and-usage.md`
- `references/mobile-appium-workflow.md` for Android/Appium mobile collection

Preflight for fresh crawling:

```bash
node scripts/preflight.mjs --profile <opencli-profile>
```

Preflight for report generation from an existing JSON:

```bash
node scripts/preflight.mjs --analysis-only
```

## Stage 1: Batch Crawl

Default web backend:

Create `questions.txt` with one question per line, then run:

```bash
node scripts/doubao_batch_crawl.mjs \
  --questions questions.txt \
  --repeat 5 \
  --profile <opencli-profile> \
  --target-entity "新东方" \
  --target-aliases "新东方前途出国,前途出国" \
  --entity-type company \
  --safe-random-delay \
  --out-dir runs/doubao-study-abroad
```

Outputs:

- `runs/doubao-study-abroad/doubao-crawl.json`
- `runs/doubao-study-abroad/raw/*.json`
- `runs/doubao-study-abroad/logs/*.log`

Use `--dry-run` to verify the plan without opening Doubao; dry-run does not require the crawler script to exist. For real Doubao web runs, prefer `--safe-random-delay`, which waits a random 5-20 minutes between fresh samples. For short controlled tests, pass `--delay-min-minutes 1 --delay-max-minutes 3`. If the OpenCLI Doubao adapter can ask/read but cannot reliably open a fresh conversation, pass `--no-new` and label the run because samples may share conversation context.

Android/Appium mobile backend:

```bash
python3 -m pip install -r requirements-mobile.txt
appium driver install uiautomator2
appium
```

```bash
python3 scripts/doubao_mobile_crawl.py preflight \
  --device emulator-5554 \
  --app-package com.larus.nova \
  --server http://127.0.0.1:4723
```

```bash
python3 scripts/doubao_mobile_crawl.py batch \
  --questions questions.txt \
  --repeat 1 \
  --device emulator-5554 \
  --app-package com.larus.nova \
  --input-resource-id com.larus.nova:id/input_text \
  --target-entity "新东方" \
  --entity-type company \
  --out-dir runs/mobile-doubao-poc \
  --delay-min-minutes 5 \
  --delay-max-minutes 20
```

Mobile outputs use the same canonical `doubao-crawl.json` shape as the web backend, plus `raw/*.json`, `logs/*.log`, `screenshots/*`, and `xml/*`. The analyzer treats mobile answers and visible reference rows as compatible evidence.

When Doubao exposes `搜索 N 个关键词，参考 M 篇资料`, the mobile backend expands that block, stores the visible search-material list in `result.mobile_search_materials`, and marks each material as cited or uncited with `citation_count`. Add `--recover-material-links` for controlled runs where the script should tap each visible material row to recover URL/detail evidence. Add `--skip-search-materials` to disable this expanded-material stage.

Use a fresh app conversation for each sample when repeated answers must be isolated:

```bash
python3 scripts/doubao_mobile_crawl.py batch \
  --questions questions.txt \
  --repeat 5 \
  --device emulator-5554 \
  --app-package com.larus.nova \
  --server http://127.0.0.1:4725 \
  --fresh-chat \
  --require-fresh-chat \
  --delay-min-seconds 0 \
  --delay-max-seconds 30 \
  --out-dir runs/mobile-doubao-fresh
```

`--fresh-chat` taps the visible Doubao "创建新对话" control before sending each prompt. `--require-fresh-chat` fails a sample instead of accidentally continuing in an old conversation when that control cannot be found.

## Stage 2: Analyze And Render

Standard input fields:

```text
1. 关键词：出国留学公司推荐、出国留学机构哪家好
2. 轮询次数：每个关键词查询 5 次
3. 目标实体：新东方
4. 实体类型：公司
```

Optional `brands.txt` can provide reviewed aliases and competitors:

```text
新东方|新东方前途出国|前途出国
启德教育|启德留学|启德
新通教育
指南者留学|指南者
```

Run:

```bash
python3 scripts/analyze_doubao_results.py \
  runs/doubao-study-abroad/doubao-crawl.json \
  --target-entity "新东方" \
  --target-aliases "新东方前途出国,前途出国" \
  --entity-type company \
  --brands-file brands.txt \
  --out-dir runs/doubao-study-abroad/report
```

Outputs:

- `runs/doubao-study-abroad/report/summary.json`
- `runs/doubao-study-abroad/report/structured-data.md`
- `runs/doubao-study-abroad/report/structured-data.xlsx`
- `runs/doubao-study-abroad/report/report.html`

The standard diagnosis report requires `--target-entity` and `--entity-type`. Entity type accepts `person/人`, `company/公司`, or `product/产品`. Target matching uses contains logic plus aliases, so target `新东方` can consolidate `新东方前途出国` and `前途出国` into the same target row. Short Latin aliases such as `AI` or `GEO` only match standalone tokens to avoid accidental matches inside longer names. Competitors are limited to the same entity type as the target. The report compares the target and competitors by mention rate, average mentions per valid answer, Top 1 / Top 3 / Top 5 probability, average rank, dominant sentiment, negative share, and source mentions.

If no target entity is supplied, the analyzer still produces an exploratory report: it shows collection coverage, compatible references, mobile evidence, and inferred same-type candidates, but it does not claim target-vs-competitor metrics.

`structured-data.md` and `structured-data.xlsx` contain the same cleaned tables for overview fields, question coverage, mobile evidence, entity metrics, source/channel data, title features, and output file paths. The HTML defaults to Simplified Chinese and includes an English summary toggle, Chinese source display names when domains can be mapped, clickable repeated URLs/titles with unique compact URL labels, mobile search-material evidence with cited/uncited counts, normalized target-vs-best-3 radar scoring when a target exists, click-to-reveal bubble benchmarking, title intent analysis, compact domain treemap, and GEO recommendations with priority charts, conservative trend projections, and concrete methods. Doubao source analysis is limited to visible markdown links, bare URLs, or compatible reference rows exposed by the crawler output.

Exploratory legacy mode still supports `--target-kind auto/person/company/product/mixed`, but final reports should use the standard target fields above.

## Offline Verification

```bash
bash scripts/run-tests.sh
```

## Package Map

- `SKILL.md`: route trigger and workflow skeleton
- `references/user-setup-and-usage.md`: install prerequisites and end-user runbook
- `references/doubao-crawl-workflow.md`: local crawler setup and run rules
- `references/mobile-appium-workflow.md`: Android/Appium setup, preflight, mobile run rules, and failure handling
- `references/report-contract.md`: JSON contract and metric definitions
- `scripts/preflight.mjs`: dependency and login-state checker
- `scripts/doubao_browser_crawl.mjs`: single Doubao web sample collector
- `scripts/doubao_batch_crawl.mjs`: repeated crawl orchestrator
- `scripts/doubao_mobile_crawl.py`: Appium UiAutomator2 mobile preflight, single capture, and repeated batch collector
- `scripts/analyze_doubao_results.py`: aggregation and Kami-styled HTML rendering
- `scripts/test_entity_recognition.py`: entity recognition regression checks
- `scripts/test_mobile_extraction.py`: offline mobile XML/reference extraction checks
- `scripts/run-tests.sh`: offline verification gate for syntax checks, regression tests, and fixture report generation
- `fixtures/sample-doubao-crawl.json`: offline test fixture
- `fixtures/sample-doubao-mobile-crawl.json`: offline mobile compatibility fixture
