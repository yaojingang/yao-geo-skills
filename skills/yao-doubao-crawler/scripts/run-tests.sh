#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

node --check scripts/doubao_batch_crawl.mjs
node --check scripts/doubao_browser_crawl.mjs
node --test scripts/test_doubao_browser_crawl.mjs
python3 -m py_compile \
  scripts/analyze_doubao_results.py \
  scripts/doubao_mobile_crawl.py \
  scripts/test_entity_recognition.py \
  scripts/test_mobile_extraction.py
python3 scripts/test_entity_recognition.py
python3 scripts/test_mobile_extraction.py
python3 scripts/analyze_doubao_results.py fixtures/sample-doubao-crawl.json \
  --target-entity "光引GEO" \
  --entity-type company \
  --brands "光引GEO,源易信息,PallasAI" \
  --out-dir /tmp/yao-doubao-crawler-report
python3 scripts/analyze_doubao_results.py fixtures/sample-doubao-mobile-crawl.json \
  --target-entity "光引GEO" \
  --entity-type company \
  --brands "光引GEO,源易信息,PallasAI" \
  --out-dir /tmp/yao-doubao-mobile-crawler-report
