# Mobile Appium Workflow

This workflow adds a low-frequency Android collection backend to the existing Doubao crawler. It is for research evidence, UI debugging, and demonstrations where the Android app exposes useful visible text or citation cards.

It does not bypass Doubao login, CAPTCHA, account checks, platform risk controls, hidden APIs, app network traffic, or encrypted storage. If the app does not expose a URL through visible text, browser handoff, or share/copy UI, the sample is kept with screenshots/XML and marked low confidence.

## Requirements

- Android SDK Platform-Tools with `adb` on `PATH`.
- Android Emulator command line tools with at least one AVD, or a USB-debuggable Android device.
- Appium 3 server and the official UiAutomator2 driver.
- Python dependency from `requirements-mobile.txt`.
- Doubao Android APK installed from an official or trusted source.
- A logged-in Doubao Android session on the selected device.

Install Python dependency:

```bash
python3 -m pip install -r requirements-mobile.txt
```

Install and start Appium:

```bash
appium driver install uiautomator2
appium
```

Useful Android checks:

```bash
emulator -list-avds
emulator @Pixel_8_API_35
adb devices
adb install doubao.apk
```

The default package is `com.larus.nova`. Pass `--app-package` if the installed package differs. `--app-activity` is optional; when omitted, the mobile script creates a generic UiAutomator2 session and activates the package.

## Preflight

Run this before a real mobile capture:

```bash
python3 scripts/doubao_mobile_crawl.py preflight \
  --device emulator-5554 \
  --app-package com.larus.nova \
  --server http://127.0.0.1:4723
```

The preflight checks:

- `adb` executable and target device state.
- Installed package path for the selected app package.
- Appium `/status`.
- Appium Python client import.
- UiAutomator2 session creation.
- Screenshot, `page_source`, and clipboard write capability.

If `adb`, `emulator`, or `appium` is not on `PATH`, fix the local Android/Appium install first. Analysis-only report generation does not need these tools.

## Single Capture

```bash
python3 scripts/doubao_mobile_crawl.py capture \
  --prompt "GEO 服务商推荐" \
  --device emulator-5554 \
  --app-package com.larus.nova \
  --server http://127.0.0.1:4723 \
  --out runs/mobile-single/raw/q01-r01.json \
  --artifact-dir runs/mobile-single
```

Prompt input uses Appium clipboard paste first, then falls back to `send_keys`. It intentionally avoids `adb shell input text` as the primary path because Chinese text escaping is brittle.

The answer wait rule samples `page_source` every 2 seconds by default. The answer is considered complete when visible UI text is stable for 8 seconds and no stop-generating control is visible. Adjust with `--timeout`, `--poll-seconds`, and `--stable-seconds`.

Post-answer collection saves every captured screen:

- `screenshots/<sample_id>/screen-*.png`
- `xml/<sample_id>/screen-*.xml`

The script extracts answer text from visible XML text after subtracting baseline UI text and the submitted prompt. Use `--input-resource-id` or `--send-resource-id` if Doubao UI changes and the generic selectors cannot find the input or send button.

By default, citation extraction does not tap citation cards, but it does try to expand the visible `搜索 N 个关键词，参考 M 篇资料` block and collect the search-material list. Each material row is matched back to the final answer and annotated with `cited`, `citation_count`, and `citation_evidence`.

Add `--skip-search-materials` if you only want the older answer/reference capture. Add `--recover-material-links` for controlled manual tests where it is acceptable for the script to tap each visible search-material row and inspect clipboard/UI text for a URL. Add `--recover-links` to tap both compatible visible references and search-material rows.

## Batch Collection

```bash
python3 scripts/doubao_mobile_crawl.py batch \
  --questions questions.txt \
  --repeat 1 \
  --device emulator-5554 \
  --app-package com.larus.nova \
  --target-entity "新东方" \
  --entity-type company \
  --out-dir runs/mobile-doubao-poc \
  --delay-min-minutes 5 \
  --delay-max-minutes 20
```

Input formats match the web batch wrapper:

- Text: one question per line.
- JSON array of strings.
- JSON array of objects: `{"id":"q01","question":"...","repeat":1,"target":"..."}`.

Outputs:

- `runs/mobile-doubao-poc/doubao-crawl.json`
- `runs/mobile-doubao-poc/raw/*.json`
- `runs/mobile-doubao-poc/logs/*.log`
- `runs/mobile-doubao-poc/screenshots/*`
- `runs/mobile-doubao-poc/xml/*`

Use `--dry-run` to write the plan without opening Appium. Use `--resume` to reuse valid raw JSON files whose question and answer text match the current plan.

Use `--fresh-chat` when every sample must begin in a new Doubao app conversation:

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
  --out-dir runs/mobile-fresh-chat
```

`--fresh-chat` searches the current UI, and up to `--fresh-chat-back-steps` previous screens, for a visible new-chat control such as `创建新对话`. `--require-fresh-chat` makes this a hard sample requirement: if the new-chat control cannot be opened, the sample fails instead of contaminating the run with an old conversation. Use `--new-chat-resource-id` when the resource id is known, for example `com.larus.nova:id/right_img`.

## Compatible Analysis

Mobile batch output uses the same `yao-doubao-crawler/v1` aggregate shape as the web backend:

```bash
python3 scripts/analyze_doubao_results.py \
  runs/mobile-doubao-poc/doubao-crawl.json \
  --target-entity "新东方" \
  --entity-type company \
  --out-dir runs/mobile-doubao-poc/report
```

The analyzer reads `result.answer.text` and `result.references.items[]`. Mobile-only fields such as `mobile`, `artifacts`, `confidence`, `failure_reason`, and `action_trace` remain audit evidence in the raw JSON.
Android captures also write `result.mobile_search_materials` when the app exposes the search-material block. This field is audit evidence and does not replace `references.items[]`.
Analysis outputs additionally include `mobile_evidence` in `summary.json`, plus `移动端证据概览`, `移动端资料按问题`, `移动端资料按样本`, and `移动端资料明细` tables in Markdown/Excel. The HTML report shows a `移动端证据` section with fresh-chat counts, delay strategy, search-material rows, cited rows, uncited rows, and sample material details.

## Citation Handling

The mobile backend is conservative:

1. Visible URLs are stored as high-confidence references.
2. Visible domain-like citation text is stored as medium-confidence references without URL.
3. The visible `搜索 N 个关键词，参考 M 篇资料` block is expanded when available. The script scrolls and deduplicates material rows by visible index/title.
4. Material rows are marked cited or uncited by matching the final answer and compatible `references.items[]` through URL, domain, title similarity, or explicit bracket citation markers.
5. With `--recover-material-links`, the script may tap visible search-material rows and inspect clipboard/UI text for a URL.
6. With `--recover-links`, the script may also tap visible answer reference nodes.
7. If a citation card or search material has no recoverable URL, the sample keeps screenshot/XML evidence and marks the row or sample with a low-confidence failure reason.

OCR is intentionally out of scope for v1. If UI hierarchy does not expose citation text, use the screenshot/XML evidence for manual review or add a separate OCR stage later.

## Failure Handling

- Login, CAPTCHA, or risk-control screens are not solved by the script; stop and fix the device session manually.
- `page_source` with only chrome text means the app is not exposing content through UiAutomator2; keep the failure sample and inspect screenshots/XML.
- App UI changes can break generic selectors; rerun with explicit `--input-resource-id` and `--send-resource-id` after inspecting XML.
- If fresh-chat isolation is required and `--require-fresh-chat` fails, inspect the first XML/screenshot manually, then pass the exact `--new-chat-resource-id` or increase `--fresh-chat-back-steps`.
- Link-less citations are not errors. They are preserved as low- or medium-confidence visible references so the report denominator remains honest.
- The mobile backend is single-device and single-threaded. Do not use it for high-frequency runs.
