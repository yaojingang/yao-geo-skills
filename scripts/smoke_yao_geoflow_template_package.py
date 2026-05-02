#!/usr/bin/env python3

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
SKILL_ROOT = ROOT / "skills" / "yao-geoflow-template"
EXAMPLE_ID = "qiaomu-editorial-20260418"
EXAMPLE_README = SKILL_ROOT / "examples" / "qiaomu-editorial" / "README.md"
PREVIEW_ROOT = SKILL_ROOT / "preview" / EXAMPLE_ID
PACKAGE_ROOT = PREVIEW_ROOT / "package"
TOKENS_PATH = PACKAGE_ROOT / "tokens.json"
MAPPING_PATH = PACKAGE_ROOT / "mapping.json"

REQUIRED_PREVIEW_FILES = [
    PREVIEW_ROOT / "index.html",
    PREVIEW_ROOT / "category.html",
    PREVIEW_ROOT / "article.html",
    PREVIEW_ROOT / "archive.html",
    PREVIEW_ROOT / "assets" / "app.js",
    PREVIEW_ROOT / "assets" / "theme.css",
    TOKENS_PATH,
    MAPPING_PATH,
    EXAMPLE_README,
]

REQUIRED_TOKENS_FIELDS = {
    "id",
    "name",
    "source_reference_url",
    "created_at",
    "compatible_system",
    "style_direction",
    "tokens",
}

REQUIRED_MAPPING_FIELDS = {
    "id",
    "name",
    "mvp_order",
    "compatible_pages",
    "module_mapping",
    "safe_boundaries",
    "preview_routes",
}

ALLOWED_COVERAGE_STATUSES = {"complete", "partial", "draft"}
RUNTIME_OUTPUT_MARKERS = ("outputs/", "outputs\\", "outputs-demo/", "outputs-demo\\")
TEXT_SUFFIXES = {".html", ".css", ".js", ".json"}


def fail(message: str) -> None:
    print(f"ERROR: {message}")
    sys.exit(1)


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        fail(f"Missing JSON file: {rel(path)}")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"{rel(path)} is invalid JSON: {exc}")
    if not isinstance(data, dict):
        fail(f"{rel(path)} must contain a JSON object")
    return data


def require_files() -> None:
    missing = [rel(path) for path in REQUIRED_PREVIEW_FILES if not path.exists()]
    if missing:
        fail(f"Missing yao-geoflow-template package files: {', '.join(missing)}")


def require_non_empty_list(data: dict[str, Any], field: str, path: Path) -> list[Any]:
    value = data.get(field)
    if not isinstance(value, list) or not value:
        fail(f"{rel(path)} field {field!r} must be a non-empty list")
    return value


def require_non_empty_dict(data: dict[str, Any], field: str, path: Path) -> dict[str, Any]:
    value = data.get(field)
    if not isinstance(value, dict) or not value:
        fail(f"{rel(path)} field {field!r} must be a non-empty object")
    return value


def validate_tokens(tokens: dict[str, Any]) -> None:
    missing = sorted(REQUIRED_TOKENS_FIELDS - set(tokens))
    if missing:
        fail(f"{rel(TOKENS_PATH)} is missing fields: {', '.join(missing)}")

    if tokens.get("id") != EXAMPLE_ID:
        fail(f"{rel(TOKENS_PATH)} id must be {EXAMPLE_ID!r}")

    for field in ("name", "source_reference_url", "created_at", "compatible_system"):
        if not isinstance(tokens.get(field), str) or not tokens[field].strip():
            fail(f"{rel(TOKENS_PATH)} field {field!r} must be a non-empty string")

    require_non_empty_list(tokens, "style_direction", TOKENS_PATH)
    require_non_empty_dict(tokens, "tokens", TOKENS_PATH)


def validate_mapping(mapping: dict[str, Any], tokens: dict[str, Any]) -> None:
    missing = sorted(REQUIRED_MAPPING_FIELDS - set(mapping))
    if missing:
        fail(f"{rel(MAPPING_PATH)} is missing fields: {', '.join(missing)}")

    if mapping.get("id") != EXAMPLE_ID:
        fail(f"{rel(MAPPING_PATH)} id must be {EXAMPLE_ID!r}")
    if mapping.get("id") != tokens.get("id"):
        fail("tokens.json and mapping.json ids must match")

    if not isinstance(mapping.get("name"), str) or not mapping["name"].strip():
        fail(f"{rel(MAPPING_PATH)} field 'name' must be a non-empty string")

    require_non_empty_list(mapping, "mvp_order", MAPPING_PATH)
    require_non_empty_list(mapping, "compatible_pages", MAPPING_PATH)
    require_non_empty_list(mapping, "safe_boundaries", MAPPING_PATH)
    require_non_empty_dict(mapping, "module_mapping", MAPPING_PATH)

    coverage_status = mapping.get("coverage_status")
    if coverage_status not in ALLOWED_COVERAGE_STATUSES:
        fail(
            f"{rel(MAPPING_PATH)} coverage_status must be one of "
            f"{', '.join(sorted(ALLOWED_COVERAGE_STATUSES))}"
        )
    if coverage_status == "partial" and not isinstance(mapping.get("omitted_routes"), list):
        fail(f"{rel(MAPPING_PATH)} omitted_routes must be a list when coverage_status is partial")

    if mapping.get("activation_status") != "preview-only":
        fail(f"{rel(MAPPING_PATH)} activation_status must remain 'preview-only' for this public example")

    validate_preview_routes(mapping)
    validate_safe_boundaries(mapping)


def validate_preview_routes(mapping: dict[str, Any]) -> None:
    preview_routes = require_non_empty_list(mapping, "preview_routes", MAPPING_PATH)
    expected_routes = {
        f"preview/{EXAMPLE_ID}/index.html",
        f"preview/{EXAMPLE_ID}/category.html",
        f"preview/{EXAMPLE_ID}/article.html",
        f"preview/{EXAMPLE_ID}/archive.html",
    }
    route_values = set()

    for route in preview_routes:
        if not isinstance(route, str) or not route.strip():
            fail(f"{rel(MAPPING_PATH)} preview_routes entries must be non-empty strings")
        route_values.add(route)
        route_path = Path(route)
        if any(part in {"outputs", "outputs-demo"} for part in route_path.parts):
            fail(f"{rel(MAPPING_PATH)} preview route references ignored runtime output: {route}")
        if not route.startswith(f"preview/{EXAMPLE_ID}/"):
            fail(f"{rel(MAPPING_PATH)} preview route must stay under preview/{EXAMPLE_ID}/: {route}")
        resolved = SKILL_ROOT / route_path
        if not resolved.exists():
            fail(f"{rel(MAPPING_PATH)} preview route points to missing file: {route}")

    missing_routes = sorted(expected_routes - route_values)
    if missing_routes:
        fail(f"{rel(MAPPING_PATH)} is missing required preview routes: {', '.join(missing_routes)}")


def validate_safe_boundaries(mapping: dict[str, Any]) -> None:
    boundaries = " ".join(str(item).lower() for item in mapping.get("safe_boundaries", []))
    required_terms = {
        "routing": "routing boundary",
        "backend": "backend/query boundary",
        "activation": "preview/activation boundary",
    }
    missing = [label for term, label in required_terms.items() if term not in boundaries]
    if missing:
        fail(f"{rel(MAPPING_PATH)} safe_boundaries missing: {', '.join(missing)}")


def validate_runtime_output_references() -> None:
    for path in sorted(PREVIEW_ROOT.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        text = path.read_text(encoding="utf-8")
        marker = next((marker for marker in RUNTIME_OUTPUT_MARKERS if marker in text), None)
        if marker:
            fail(f"{rel(path)} references ignored runtime output marker {marker!r}")


def validate_example_readme() -> None:
    text = EXAMPLE_README.read_text(encoding="utf-8")
    required_mentions = [
        f"preview/{EXAMPLE_ID}/index.html",
        f"preview/{EXAMPLE_ID}/category.html",
        f"preview/{EXAMPLE_ID}/article.html",
        f"preview/{EXAMPLE_ID}/archive.html",
        f"preview/{EXAMPLE_ID}/package/tokens.json",
        f"preview/{EXAMPLE_ID}/package/mapping.json",
        "activation_status",
        "preview-only",
    ]
    missing = [mention for mention in required_mentions if mention not in text]
    if missing:
        fail(f"{rel(EXAMPLE_README)} is missing expected package references: {', '.join(missing)}")


def main() -> None:
    require_files()
    tokens = load_json(TOKENS_PATH)
    mapping = load_json(MAPPING_PATH)
    validate_tokens(tokens)
    validate_mapping(mapping, tokens)
    validate_runtime_output_references()
    validate_example_readme()
    print(f"Yao GEOFlow template package smoke test passed for {EXAMPLE_ID}.")


if __name__ == "__main__":
    main()
