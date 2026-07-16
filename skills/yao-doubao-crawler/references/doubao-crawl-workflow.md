# Doubao Crawl Workflow

## Local Capability Source

Preferred local crawler:

```text
scripts/doubao_browser_crawl.mjs
```

The crawler uses the OpenCLI `doubao` site adapter. It opens a fresh conversation, sends one prompt to Doubao web, waits for the answer, normalizes the answer text, extracts visible external markdown links and bare URLs as references, and records answer length plus optional target mention count. When a compatible replacement crawler can expose richer citation rows, it should preserve `references.items[]` with `number`, `source`, `domain`, `title`, `date`, `url`, and `summary`.

Override the crawler path with `--crawler-script` or `DOUBAO_CRAWLER_SCRIPT` when the local project moves.

## Preflight

Run the skill preflight before a real crawl:

```bash
node scripts/preflight.mjs --profile <opencli-profile>
```

If the crawler script is not in the default local path:

```bash
node scripts/preflight.mjs \
  --profile <opencli-profile> \
  --crawler-script /absolute/path/to/doubao_browser_crawl.mjs
```

The preflight wraps these underlying checks:

```bash
opencli --version
opencli doctor
opencli profile list
opencli doubao status -f json
opencli doubao whoami -f json
```

Doubao web must already be logged in and reachable from the connected profile. The skill does not handle login, region blocks, CAPTCHA, Cloudflare checks, or account recovery.

## Stage 1: Batch Crawl

Use the batch wrapper from this skill:

```bash
node scripts/doubao_batch_crawl.mjs \
  --questions questions.txt \
  --repeat 5 \
  --profile <opencli-profile> \
  --target-entity "孟庆涛" \
  --entity-type person \
  --safe-random-delay \
  --out-dir runs/geo-doubao-20260619
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

The wrapper records `target_entity`, `target_aliases`, `entity_type`, and delay strategy in `doubao-crawl.json > input`.

The wrapper calls `opencli doubao new` before each sample through `scripts/doubao_browser_crawl.mjs` by default. It writes per-sample raw JSON and logs, then writes `doubao-crawl.json`. If the OpenCLI Doubao adapter's new-conversation flow only reloads `/chat` or repeatedly returns no visible messages, use `--no-new` for controlled web runs; this keeps the current Doubao site session and asks sequentially while still preserving raw logs and answer evidence.

## Run Rules

- Doubao's OpenCLI adapter does not expose model switching or a dedicated Web Search flag; source extraction is limited to visible URLs unless a replacement crawler provides richer compatible references.
- Use `--no-reference-extraction` when URL extraction is not needed. `--no-search` is accepted as a compatibility alias for the same behavior.
- Use `--no-new` when the web adapter can send and read answers but cannot reliably open a fresh Doubao conversation. Label runs that use this option because samples may share the same Doubao conversation context.
- Prefer `--safe-random-delay` for real Doubao web runs. It waits a random 5-20 minutes between fresh samples.
- Use `--delay-min-minutes <n> --delay-max-minutes <n>` when a different random interval is needed.
- Use `--resume` to skip samples that already have valid raw JSON.
- Use `--delay-ms` only for controlled tests or trusted low-risk environments.
- Treat failed samples as evidence. Do not delete them from the dataset.
- If a question must be crawled 5 times, the denominator is 5 even when one sample fails; report completion and valid-sample counts separately.
- Slower random intervals reduce request frequency but do not guarantee account safety or bypass platform risk controls.

## Stage 2: Analyze And Render

```bash
python3 scripts/analyze_doubao_results.py \
  runs/geo-doubao-20260619/doubao-crawl.json \
  --target-entity "孟庆涛" \
  --entity-type person \
  --brands-file brands.txt \
  --out-dir runs/geo-doubao-20260619/report
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

- `references.count = 0`: Doubao may have answered without visible links, citations may not be exposed as markdown links or bare URLs, or a replacement crawler did not provide compatible reference rows.
- `ok = false`: keep the raw file/log and include it in completion metrics.
- Repeated adapter failures: rerun one question manually with `node scripts/doubao_browser_crawl.mjs --prompt "..." --profile <profile>` and inspect the per-sample log before changing this skill.

## Evidence Boundary

This skill analyzes what Doubao web displayed. It does not claim that cited source pages are correct, complete, or currently reachable. If downstream work needs external page truth, add a separate fetch-and-parse stage and label it separately.
