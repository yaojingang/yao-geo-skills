# User Setup And Usage

This guide is for a user who has just installed `yao-doubao-crawler` and wants to run real Doubao web or Android/Appium crawls.

## What This Skill Needs

Fresh crawling requires local browser automation. The skill does not install OpenCLI, log in to Doubao, solve CAPTCHA, or bypass account checks.

Required for fresh crawls:

- Node.js 18+.
- Python 3.10+.
- OpenCLI CLI 1.8.4+ available as `opencli`.
- OpenCLI Browser Bridge extension connected to a Chrome or Edge profile.
- A logged-in Doubao web session in that connected profile that can send messages.
- The bundled Doubao browser crawler at `scripts/doubao_browser_crawl.mjs`. If using a compatible replacement, pass `--crawler-script <file>` or set `DOUBAO_CRAWLER_SCRIPT`.

Required for analysis-only usage:

- Node.js 18+.
- Python 3.10+.
- An existing `doubao-crawl.json` or compatible Doubao raw JSON.

Optional for Android/Appium mobile crawls:

- Android SDK Platform-Tools with `adb`.
- Android Studio AVD or a USB-debuggable Android device.
- Appium 3 with the UiAutomator2 driver.
- Python package from `requirements-mobile.txt`.
- Doubao Android APK installed and already logged in on the selected device.

For Android/Appium setup and run rules, read `references/mobile-appium-workflow.md`.

## 1. Run Preflight

From the skill directory:

```bash
node scripts/preflight.mjs --profile <opencli-profile>
```

If the crawler script is not in the default local path:

```bash
node scripts/preflight.mjs \
  --profile <opencli-profile> \
  --crawler-script /absolute/path/to/doubao_browser_crawl.mjs
```

For report generation from an existing JSON only:

```bash
node scripts/preflight.mjs --analysis-only
```

Preflight must pass before a fresh crawl. If `Doubao region access` fails, the connected browser opened a region block page and cannot crawl until the same profile can access `https://www.doubao.com`. If `Doubao login` fails, log in in the connected browser profile first.

For Android/Appium mobile preflight:

```bash
python3 -m pip install -r requirements-mobile.txt
appium driver install uiautomator2
appium
python3 scripts/doubao_mobile_crawl.py preflight \
  --device emulator-5554 \
  --app-package com.larus.nova \
  --server http://127.0.0.1:4723
```

## 2. Prepare Questions

Before running a standard diagnosis report, prepare these four inputs:

```text
1. 关键词：one or more Doubao questions, one per line
2. 轮询次数：how many times each keyword should be queried
3. 目标实体：the entity to diagnose, for example 新东方 or 孟庆涛
4. 实体类型：人, 公司, or 产品
```

For collection-only or exploratory analysis, target entity can be omitted. The analyzer will still generate coverage, source, mobile evidence, and inferred candidate tables, but it will not claim target-vs-competitor metrics.

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

The target entity and entity type are required for standard diagnosis reports. Entity aliases make Top 1, Top 3, mention rate, and average-rank metrics more reliable.

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

Check the plan before opening Doubao:

```bash
node scripts/doubao_batch_crawl.mjs \
  --questions questions.txt \
  --repeat 5 \
  --profile <opencli-profile> \
  --target-entity "新东方" \
  --entity-type company \
  --out-dir runs/my-doubao-run \
  --dry-run
```

Expected output should show the planned sample count. Five questions repeated five times should produce 25 samples.
Dry-run only validates the plan and target fields; it does not require the crawler script, OpenCLI profile, or Doubao page to be available. Real crawling still requires all fresh-crawl prerequisites.

## 5. Run Fresh Crawl

For real Doubao web runs, use the safe random delay mode:

```bash
node scripts/doubao_batch_crawl.mjs \
  --questions questions.txt \
  --repeat 5 \
  --profile <opencli-profile> \
  --target-entity "新东方" \
  --target-aliases "新东方前途出国,前途出国" \
  --entity-type company \
  --out-dir runs/my-doubao-run \
  --safe-random-delay \
  --timeout 300
```

`--safe-random-delay` waits a random 5-20 minutes between fresh samples. Five questions repeated five times means 25 samples and 24 waits, so the waiting time alone is usually around 2-8 hours. This lowers request frequency but does not guarantee account safety or bypass platform risk controls.

Use a custom random interval when needed:

```bash
node scripts/doubao_batch_crawl.mjs \
  --questions questions.txt \
  --repeat 5 \
  --profile <opencli-profile> \
  --target-entity "新东方" \
  --entity-type company \
  --out-dir runs/my-doubao-run \
  --delay-min-minutes 5 \
  --delay-max-minutes 20
```

If your crawler script is outside the default path:

```bash
node scripts/doubao_batch_crawl.mjs \
  --questions questions.txt \
  --repeat 5 \
  --profile <opencli-profile> \
  --target-entity "新东方" \
  --entity-type company \
  --crawler-script /absolute/path/to/doubao_browser_crawl.mjs \
  --safe-random-delay \
  --out-dir runs/my-doubao-run
```

Outputs:

- `runs/my-doubao-run/doubao-crawl.json`
- `runs/my-doubao-run/raw/*.json`
- `runs/my-doubao-run/logs/*.log`

Each sample starts a fresh Doubao conversation by default. Keep the run single-threaded unless the replacement crawler explicitly supports concurrency.

For Android/Appium mobile runs, use the mobile backend after preflight passes:

```bash
python3 scripts/doubao_mobile_crawl.py batch \
  --questions questions.txt \
  --repeat 1 \
  --device emulator-5554 \
  --app-package com.larus.nova \
  --target-entity "新东方" \
  --target-aliases "新东方前途出国,前途出国" \
  --entity-type company \
  --out-dir runs/my-doubao-mobile-run \
  --delay-min-minutes 5 \
  --delay-max-minutes 20
```

Mobile runs additionally write `screenshots/*` and `xml/*`. Treat mobile captures as UI evidence: when citation URLs are not exposed, the script keeps visible source text and marks the reference or sample with a lower confidence reason.

If every mobile sample must start from a separate Doubao app conversation, add fresh-chat isolation:

```bash
python3 scripts/doubao_mobile_crawl.py batch \
  --questions questions.txt \
  --repeat 5 \
  --device emulator-5554 \
  --app-package com.larus.nova \
  --fresh-chat \
  --require-fresh-chat \
  --delay-min-seconds 0 \
  --delay-max-seconds 30 \
  --out-dir runs/my-doubao-mobile-fresh-run
```

`--fresh-chat` taps the visible new-chat control before prompt entry. `--require-fresh-chat` fails a sample if a new conversation cannot be opened, which prevents accidental reuse of an old thread.

## 6. Resume Interrupted Runs

If the run stops midway, rerun the same command with `--resume`:

```bash
node scripts/doubao_batch_crawl.mjs \
  --questions questions.txt \
  --repeat 5 \
  --profile <opencli-profile> \
  --target-entity "新东方" \
  --entity-type company \
  --out-dir runs/my-doubao-run \
  --resume
```

Resume only reuses raw JSON when it is valid, successful, has answer text, and matches the current question.

## 7. Generate The Report

```bash
python3 scripts/analyze_doubao_results.py \
  runs/my-doubao-run/doubao-crawl.json \
  --target-entity "新东方" \
  --target-aliases "新东方前途出国,前途出国" \
  --entity-type company \
  --brands-file brands.txt \
  --title "Doubao 搜索概率分析报告" \
  --out-dir runs/my-doubao-run/report
```

Outputs:

- `runs/my-doubao-run/report/summary.json`
- `runs/my-doubao-run/report/structured-data.md`
- `runs/my-doubao-run/report/structured-data.xlsx`
- `runs/my-doubao-run/report/report.html`

The analyzer keeps `summary.json` as a machine-readable metric summary. `structured-data.md` and `structured-data.xlsx` contain the same cleaned structured tables: output file list, overview fields, question coverage, mobile evidence, target metrics, same-type entity comparison, question-by-entity metrics, entity recognition candidates, source/channel tables, frequent domains/sources/URLs/titles, and title-feature buckets. The HTML report defaults to Simplified Chinese and includes a top-right language toggle for English overview analysis. It starts with a numeric overview, directory, and metric explanations. It then includes core conclusions, target-vs-competitor comparison when a target exists, sentiment analysis, average mention count, sample coverage, mobile evidence, target entity recognition, mention probability, Top 1 / Top 3 / Top 5 probability, average rank, source channels, repeated domains, clickable repeated URLs/titles, title-feature charts, and GEO optimization recommendations. Domain displays use readable Chinese names where available. High-frequency URL rows show one clickable compact label per row, keep the full URL as link target/hover title, and avoid visually duplicated URL lines. GEO recommendations include priority bars, a conservative core-metric trend projection, method/check tables, and concise action cards. Detail lists are capped at 10 rows by default. Doubao source analysis is limited to visible URLs or compatible reference rows exposed by the crawler output.

Target type can be forced:

```bash
python3 scripts/analyze_doubao_results.py \
  runs/my-doubao-run/doubao-crawl.json \
  --target-entity "孟庆涛" \
  --entity-type person \
  --out-dir runs/my-doubao-run/report
```

Accepted standard entity types are `person/人`, `company/公司`, and `product/产品`.

## 8. Troubleshooting

| Symptom | Likely Cause | Fix |
|---|---|---|
| `opencli: command not found` | OpenCLI is not installed or not on `PATH`. | Install OpenCLI and verify `opencli --version`. |
| `No Browser Bridge profiles connected` | Browser extension is not connected. | Open the Chrome or Edge profile with OpenCLI Browser Bridge enabled, then run `opencli profile list`. |
| `Browser profile ... is not connected` | The selected profile is offline. | Use `opencli profile list`, then pass a connected profile with `--profile`. |
| `Doubao region access` fails or URL contains `region-ban` | The connected browser/network cannot access Doubao. | Open `https://www.doubao.com` manually in the same browser profile from an accessible network/session, then rerun preflight. |
| `logged_in: false` | Doubao is not logged in. | Log in to Doubao in the connected browser, then run `opencli doubao whoami -f json`. |
| `Crawler script not found` | The bundled crawler is missing or a custom path is wrong. | Repair `scripts/doubao_browser_crawl.mjs`, pass `--crawler-script <file>`, or set `DOUBAO_CRAWLER_SCRIPT`. |
| `references.count = 0` | Doubao answered without visible external URLs, or citations were not exposed as markdown links/bare URLs in OpenCLI text output. | Rerun one sample, inspect the raw answer/log, and treat source analysis as incomplete when URLs are absent. |
| Many samples fail after several successes | Browser bridge, account throttling, Doubao page instability, or platform risk controls. | Stop the run, wait before retrying, use `--safe-random-delay` or wider custom random intervals, rerun with `--resume`, and inspect failed logs. |
| Mobile `adb not found` | Android SDK Platform-Tools is not installed or not on `PATH`. | Install Android SDK Platform-Tools, add it to `PATH`, or pass `--adb-path`. |
| Mobile UiAutomator2 session fails | Appium server/driver/device/package mismatch. | Start `appium`, run `appium driver install uiautomator2`, verify `adb devices`, and rerun mobile preflight. |
| Mobile answer text is empty | Doubao UI did not expose answer text through UiAutomator2 or selectors failed. | Inspect `xml/*` and `screenshots/*`; pass `--input-resource-id` or `--send-resource-id` if needed. |
| Mobile fresh-chat fails | The new-chat control is not visible from the current screen or its resource id changed. | Inspect the current XML/screenshot, pass `--new-chat-resource-id`, or increase `--fresh-chat-back-steps`. |
| Mobile citation has no URL | App UI exposed a source card/domain but no URL. | Keep the low-confidence reference and screenshot/XML evidence; do not treat it as a recovered link. |

## Evidence And Privacy

The run directory stores raw Doubao answers, source titles, URLs, and logs. Treat it as audit evidence. Do not publish or commit run outputs if the questions, answers, or sources contain private or client-sensitive information.
