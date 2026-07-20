# ChatGPT Crawl Workflow

## Local Capability Source

Preferred local crawler:

```text
scripts/chatgpt_browser_crawl.mjs
```

The crawler uses the OpenCLI `chatgpt` site adapter. It sends one prompt to ChatGPT web, waits for the answer, normalizes the answer text, extracts visible ChatGPT citation pills, source-flyout links, markdown links, and bare URLs as references, and records answer length plus optional target mention count.

Override the crawler path with `--crawler-script` or `CHATGPT_CRAWLER_SCRIPT` only when using a compatible replacement.

## Preflight

Run the skill preflight before a real crawl:

```bash
node scripts/preflight.mjs --profile <opencli-profile>
```

If the crawler script is not in the default local path:

```bash
node scripts/preflight.mjs \
  --profile <opencli-profile> \
  --crawler-script /absolute/path/to/chatgpt_browser_crawl.mjs
```

The preflight wraps these underlying checks:

```bash
opencli --version
opencli doctor
opencli profile list
opencli chatgpt status -f json
opencli chatgpt whoami -f json
```

ChatGPT web must be able to send messages. A session can sometimes send answer-only messages even when `opencli chatgpt whoami` cannot read a full session cookie. Web Search and account-specific tools still depend on what the current ChatGPT account/session exposes. The skill does not handle login, CAPTCHA, Cloudflare checks, or account recovery.

## Stage 1: Batch Crawl

Use the batch wrapper from this skill:

```bash
node scripts/chatgpt_batch_crawl.mjs \
  --questions questions.txt \
  --repeat 5 \
  --profile <opencli-profile> \
  --target-entity "光引GEO" \
  --target-aliases "光引" \
  --entity-type company \
  --delay-preset 1-3m \
  --out-dir runs/geo-chatgpt-20260619
```

Input formats:

- Text: one question per line.
- JSON array of strings.
- JSON array of objects: `{"id":"q01","question":"...","repeat":5,"target":"..."}`.

Standard user inputs:

- `keywords/questions`: one or more ChatGPT questions.
- `repeat`: how many fresh samples per question.
- `target_entity`: the target entity to diagnose.
- `entity_type`: `person`, `company`, or `product`.
- `profile`: the connected OpenCLI Browser Bridge profile, usually an Edge or Chrome profile.
- `single_query_interval`: random delay between fresh samples. Default is `30s-1m`; supported presets are `30s-1m`, `1-3m`, and `3-10m`.

The wrapper records `target_entity`, `target_aliases`, `entity_type`, ChatGPT mode/search options, and delay strategy in `chatgpt-crawl.json > input`.

The wrapper starts a fresh ChatGPT conversation per sample by default. It writes per-sample raw JSON and logs, then writes `chatgpt-crawl.json`.

## Run Rules

- Default to Web Search so citation pills, source-flyout links, and markdown URLs are more likely to appear in the answer.
- Use `--no-search` for answer-only sampling.
- If OpenCLI reports `Could not find the ChatGPT Web Search tool option`, the crawler retries without the explicit tool toggle and still captures any visible ChatGPT sources that the account displays.
- Use `--model instant|thinking|pro` when the account supports a specific ChatGPT mode.
- Use `--deep-research` only for deliberate long-running Deep Research samples; increase `--timeout` accordingly.
- Default fresh-crawl interval is `--delay-preset 30s-1m`, which waits a random 30-60 seconds between samples.
- Use `--delay-preset 1-3m` for a slower balanced run, especially above a few samples.
- Use `--delay-preset 3-10m` for a conservative run when account throttling risk matters more than speed.
- `--safe-random-delay` is an alias for the conservative `3-10m` preset.
- Use `--delay-min-minutes <n> --delay-max-minutes <n>` when a different random interval is needed.
- Use `--resume` to skip samples that already have valid raw JSON.
- Use `--delay-ms` only for controlled tests or trusted low-risk environments.
- Treat failed samples as evidence. Do not delete them from the dataset.
- If a question must be crawled 5 times, the denominator is 5 even when one sample fails; report completion and valid-sample counts separately.
- Slower random intervals reduce request frequency but do not guarantee account safety or bypass platform risk controls.

## Stage 2: Analyze And Render

```bash
python3 scripts/analyze_chatgpt_results.py \
  runs/geo-chatgpt-20260619/chatgpt-crawl.json \
  --target-entity "光引GEO" \
  --target-aliases "光引" \
  --entity-type company \
  --brands-file brands.txt \
  --out-dir runs/geo-chatgpt-20260619/report
```

Alias and competitor file format:

```text
目标实体|目标别名A|目标别名B
同类型竞品A|竞品别名A
同类型竞品B
```

Target matching uses contains logic plus aliases. For example, `--target-entity 新东方` can consolidate `新东方前途出国` and `前途出国`. Competitors are filtered to the same entity type as the target entity.

If no alias/competitor file is supplied, the analyzer infers same-type competitors from answer structure and marks lower-confidence candidates in the entity recognition table.

A file containing only the target entity and its aliases is a target-alias file, not a complete competitor list. The analyzer must keep fallback competitor inference enabled in this case.

For formal English brand/company reports without user-supplied competitors, review repeated brand names from the captured answers into the alias file before final rendering, or run with `--semantic-review required`. Pure Latin brand names often lack legal or organization suffixes, so local suffix rules alone are an exploratory fallback.

## Failure Handling

- `references.count = 0`: Web Search may be off, ChatGPT may have answered without visible links, or citations/source controls may not be exposed in the DOM or answer text.
- `ok = false`: keep the raw file/log and include it in completion metrics.
- Repeated adapter failures: rerun one question manually with `node scripts/chatgpt_browser_crawl.mjs --prompt "..." --profile <profile>` and inspect the per-sample log before changing this skill.

## Evidence Boundary

This skill analyzes what ChatGPT web displayed. It does not claim that cited source pages are correct, complete, or currently reachable. If downstream work needs external page truth, add a separate fetch-and-parse stage and label it separately.
