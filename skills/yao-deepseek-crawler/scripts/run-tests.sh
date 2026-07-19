#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

deepseek_report_dir=$(mktemp -d)
trap 'rm -rf -- "$deepseek_report_dir"' EXIT

node --check scripts/geo-deepseek-browser-direct.mjs
node --check scripts/deepseek_batch_crawl.mjs
node --check scripts/preflight.mjs
node --test scripts/test_geo_deepseek_browser_direct.mjs
python3 -m py_compile scripts/analyze_deepseek_results.py scripts/test_entity_recognition.py
python3 scripts/test_entity_recognition.py
python3 scripts/analyze_deepseek_results.py fixtures/sample-deepseek-crawl.json \
  --target-entity '光引GEO' \
  --entity-type company \
  --brands '光引GEO,源易信息,PallasAI' \
  --out-dir "$deepseek_report_dir"
python3 - "$deepseek_report_dir" <<'PY'
import json
import sys
from pathlib import Path

report_dir = Path(sys.argv[1])
summary = json.loads((report_dir / "summary.json").read_text(encoding="utf-8"))
reference_rows = summary["sources"]["reference_rows"]
assert reference_rows, "structured reference rows are missing"
assert {"source_origin", "title_origin", "summary_origin"}.issubset(reference_rows[0])
assert "provenance_counts" in summary["sources"]
assert "excluded_url_derived" in summary["titles"]

structured_markdown = (report_dir / "structured-data.md").read_text(encoding="utf-8")
assert "## 信源字段来源" in structured_markdown
assert "## 信源明细" in structured_markdown
assert "title_origin" in structured_markdown
PY
