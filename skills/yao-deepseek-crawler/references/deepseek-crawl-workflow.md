# DeepSeek Crawl Workflow

## Local Capability Source

Bundled local crawler:

```text
scripts/geo-deepseek-browser-direct.mjs
```

This is preferred over the archived `deepseek-crawler` because it captures the DeepSeek answer, answer length, target mention count, and displayed citation links from the active DeepSeek browser DOM. With the public OpenCLI DeepSeek adapter, the separate source-panel object is not exposed directly, so the bundled crawler preserves source evidence from the `X 个网页` answer citations: citation number, domain/source, URL, inferred title, and nearby answer context. Each reference records provenance fields for observed and inferred values. Reference collection requires a valid DeepSeek conversation URL, the latest submitted prompt, and the latest assistant DOM text to match the answer returned by the current OpenCLI command. It uses an owned temporary browser session and closes that session after successful and failed extraction, leaving the user's active tab untouched. The archived Playwright service is useful as historical evidence only; it mainly captures the final answer text.

Override the crawler path with `--crawler-script` or `DEEPSEEK_CRAWLER_SCRIPT` when the local project moves.

## Preflight

Run the skill preflight before a real crawl:

```bash
node scripts/preflight.mjs --profile <opencli-profile>
```

If the crawler script is not in the default local path:

```bash
node scripts/preflight.mjs \
  --profile <opencli-profile> \
  --crawler-script /absolute/path/to/geo-deepseek-browser-direct.mjs
```

The preflight wraps these underlying checks:

```bash
opencli --version
opencli doctor
opencli profile list
opencli deepseek whoami -f json
```

If Browser Bridge is disconnected, use this skill's DeepSeek-specific setup script:

```bash
node scripts/setup_deepseek_bridge.mjs
```

This script opens `https://chat.deepseek.com/` in a dedicated OpenCLI browser profile. Do not use the `opencli-boss-ai` bridge setup script for this skill, because that project intentionally opens BOSS Zhipin. DeepSeek web must already be logged in. The skill does not handle login, CAPTCHA, Cloudflare checks, or account recovery.

## Stage 1: Batch Crawl

Use the batch wrapper from this skill:

```bash
node scripts/deepseek_batch_crawl.mjs \
  --questions questions.txt \
  --repeat 5 \
  --profile <opencli-profile> \
  --target-entity "孟庆涛" \
  --entity-type person \
  --safe-random-delay \
  --out-dir runs/geo-deepseek-20260619
```

Input formats:

- Text: one question per line.
- JSON array of strings.
- JSON array of objects: `{"id":"q01","question":"...","repeat":5,"target":"..."}`.

Standard user inputs:

- `keywords/questions`: one or more questions.
- `repeat`: how many fresh samples per question.
- `target_entity`: the target entity to diagnose.
- `entity_type`: `person`, `company`, or `product`.

The wrapper records `target_entity`, `target_aliases`, `entity_type`, and delay strategy in `deepseek-crawl.json > input`.

The wrapper opens a fresh DeepSeek session name per sample. It writes per-sample raw JSON and logs, then writes `deepseek-crawl.json`.

## Run Rules

- Default to `--search` so the source panel can be captured.
- Prefer `--safe-random-delay` for real DeepSeek web runs. It waits a random 5-20 minutes between fresh samples.
- Use `--delay-min-minutes <n> --delay-max-minutes <n>` when a different random interval is needed.
- Use `--resume` to skip samples that already have valid raw JSON.
- Use `--delay-ms` only for controlled tests or trusted low-risk environments.
- Treat failed samples as evidence. Do not delete them from the dataset.
- If a question must be crawled 5 times, the denominator is 5 even when one sample fails; report completion and valid-sample counts separately.
- Slower random intervals reduce request frequency but do not guarantee account safety or bypass platform risk controls.

## Stage 2: Analyze And Render

```bash
python3 scripts/analyze_deepseek_results.py \
  runs/geo-deepseek-20260619/deepseek-crawl.json \
  --target-entity "孟庆涛" \
  --entity-type person \
  --brands-file brands.txt \
  --out-dir runs/geo-deepseek-20260619/report
```

The analyzer writes:

- `summary.json`: machine-readable analysis summary.
- `structured-data.md`: Markdown export of cleaned fields and data.
- `structured-data.xlsx`: Excel workbook with the same structured tables.
- `report.html`: visual diagnosis and analysis report.

Alias and competitor file format:

```text
目标实体|目标别名A|目标别名B
同类型竞品A|竞品别名A
同类型竞品B
```

Target matching uses contains logic plus aliases. For example, `--target-entity 新东方` can consolidate `新东方前途出国` and `前途出国`. Competitors are filtered to the same entity type as the target entity.

If no alias/competitor file is supplied, the analyzer infers same-type competitors from answer structure and marks lower-confidence candidates in the entity recognition table.

## Failure Handling

- `references.count = 0`: the search toggle may be off, the panel may not render, or DeepSeek DOM changed.
- `ok = false`: keep the raw file/log and include it in completion metrics.
- Repeated DOM failures: rerun one question manually with the existing crawler to inspect page state before changing this skill.

## Evidence Boundary

This skill analyzes what DeepSeek web displayed. It does not claim that cited source pages are correct, complete, or currently reachable. If downstream work needs external page truth, add a separate fetch-and-parse stage and label it separately.
