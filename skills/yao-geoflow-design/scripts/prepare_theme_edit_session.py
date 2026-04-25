#!/usr/bin/env python3
import argparse
import json
import re
import shutil
from datetime import datetime
from pathlib import Path


def load_json(path: Path) -> dict:
    if not path.is_file():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def write_json(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def sanitize_theme_id(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9_-]+", "-", value)
    value = re.sub(r"-{2,}", "-", value).strip("-")
    return value or "theme-edit"


def recursive_replace(value, old: str, new: str):
    if isinstance(value, str):
        return value.replace(old, new)
    if isinstance(value, list):
        return [recursive_replace(item, old, new) for item in value]
    if isinstance(value, dict):
        return {key: recursive_replace(item, old, new) for key, item in value.items()}
    return value


def build_preview_routes(theme_id: str) -> list[str]:
    return [
        "/",
        "/category/{slug}",
        "/article/{slug}",
        "/archive",
    ]


def main() -> None:
    parser = argparse.ArgumentParser(description="Create a preview edit session for an existing GEOFlow theme.")
    parser.add_argument("workspace", help="Path to the GEOFlow workspace")
    parser.add_argument("--base-theme", required=True, help="Existing theme id to fork")
    parser.add_argument("--new-theme-id", help="Preview theme id; auto-generated when omitted")
    parser.add_argument("--new-name", help="Preview theme display name")
    parser.add_argument("--change-request", default="", help="Short summary of requested frontend changes")
    args = parser.parse_args()

    workspace = Path(args.workspace).resolve()
    laravel_themes_root = workspace / "resources" / "views" / "theme"
    themes_root = laravel_themes_root if laravel_themes_root.is_dir() else workspace / "themes"
    framework = "laravel" if themes_root == laravel_themes_root else "legacy_php"
    base_theme_id = args.base_theme.strip()
    base_dir = themes_root / base_theme_id
    if not base_dir.is_dir():
        raise SystemExit(f"Base theme not found: {base_dir}")

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    preview_theme_id = sanitize_theme_id(args.new_theme_id or f"{base_theme_id}-edit-{timestamp}")
    preview_dir = themes_root / preview_theme_id
    if preview_dir.exists():
        raise SystemExit(f"Preview theme already exists: {preview_dir}")

    shutil.copytree(base_dir, preview_dir)

    manifest_path = preview_dir / "manifest.json"
    manifest = load_json(manifest_path)
    base_manifest = load_json(base_dir / "manifest.json")
    preview_name = args.new_name or f"{base_manifest.get('name', base_theme_id)} Preview Edit"
    manifest = recursive_replace(manifest, base_theme_id, preview_theme_id)
    manifest["name"] = preview_name
    manifest["base_theme_id"] = base_theme_id
    manifest["target_theme_id"] = base_theme_id
    manifest["mode"] = "edit_theme"
    manifest["session_state"] = "preview"
    manifest["created_at"] = datetime.now().astimezone().isoformat(timespec="seconds")
    manifest["preview_routes"] = build_preview_routes(preview_theme_id)
    notes = manifest.get("notes")
    if not isinstance(notes, list):
        notes = []
    notes.extend([
        f"Preview edit session forked from {base_theme_id}.",
        "Do not activate before review.",
    ])
    if args.change_request.strip():
        notes.append(f"Requested changes: {args.change_request.strip()}")
    manifest["notes"] = notes
    write_json(manifest_path, manifest)

    editable_files = []
    if framework == "laravel":
        for path in sorted(preview_dir.rglob("*.blade.php")):
            editable_files.append(path.relative_to(preview_dir).as_posix())
    else:
        for path in sorted((preview_dir / "templates").glob("*.php")):
            editable_files.append(path.relative_to(preview_dir).as_posix())
    for relative in ("assets/theme.css", "manifest.json", "tokens.json", "mapping.json"):
        if (preview_dir / relative).is_file():
            editable_files.append(relative)

    session_payload = {
        "base_theme_id": base_theme_id,
        "preview_theme_id": preview_theme_id,
        "framework": framework,
        "created_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "session_state": "preview",
        "change_request": args.change_request.strip(),
        "preview_routes": build_preview_routes(preview_theme_id),
        "preview_note": "Laravel GEOFlow does not expose isolated /preview/{theme} routes by default; use static previews or activate the preview theme only after operator confirmation.",
        "editable_files": editable_files,
        "finalize_options": [
            "publish_as_new_theme",
            "replace_base_theme",
            "activate_after_confirmation",
        ],
        "warnings": [
            "Preview the fork before any live replacement.",
            "Do not change business logic or data contracts in this session.",
        ],
    }
    write_json(preview_dir / "edit-session.json", session_payload)

    change_plan = preview_dir / "change-plan.md"
    change_plan.write_text(
        "\n".join([
            "# Theme Edit Session",
            "",
            f"- Base theme: `{base_theme_id}`",
            f"- Preview theme: `{preview_theme_id}`",
            f"- Framework: `{framework}`",
            f"- Requested changes: {args.change_request.strip() or 'TBD'}",
            "- Finalize options: `publish_as_new_theme` | `replace_base_theme` | `activate_after_confirmation`",
            "",
            "## Preview Checklist",
            "",
            "- check home/category/article/archive preview routes",
            "- for Laravel GEOFlow, confirm whether preview is static or temporarily activated through Site Settings",
            "- verify layout, typography, spacing, and module hierarchy",
            "- confirm GEOFlow data placeholders still render correctly",
        ]) + "\n",
        encoding="utf-8",
    )

    preview_notes = preview_dir / "preview-notes.md"
    if not preview_notes.exists():
        preview_notes.write_text("# Preview Notes\n\n- pending review\n", encoding="utf-8")

    result = {
        "workspace": str(workspace),
        "base_theme_id": base_theme_id,
        "preview_theme_id": preview_theme_id,
        "framework": framework,
        "preview_theme_path": str(preview_dir),
        "preview_routes": build_preview_routes(preview_theme_id),
        "preview_support": "admin_activation_or_static_preview" if framework == "laravel" else "legacy_preview_routes",
        "editable_files": editable_files,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
