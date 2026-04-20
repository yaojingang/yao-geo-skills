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
    return value or "theme"


def recursive_replace(value, old: str, new: str):
    if isinstance(value, str):
        return value.replace(old, new)
    if isinstance(value, list):
        return [recursive_replace(item, old, new) for item in value]
    if isinstance(value, dict):
        return {key: recursive_replace(item, old, new) for key, item in value.items()}
    return value


def publish_as_new(themes_root: Path, preview_theme_id: str, new_theme_id: str | None, new_name: str | None) -> dict:
    preview_dir = themes_root / preview_theme_id
    target_theme_id = sanitize_theme_id(new_theme_id or preview_theme_id)
    target_dir = themes_root / target_theme_id
    if target_dir.exists() and target_theme_id != preview_theme_id:
        raise SystemExit(f"Target theme already exists: {target_dir}")

    if target_theme_id != preview_theme_id:
        shutil.move(str(preview_dir), str(target_dir))
    else:
        target_dir = preview_dir

    manifest_path = target_dir / "manifest.json"
    manifest = recursive_replace(load_json(manifest_path), preview_theme_id, target_theme_id)
    manifest["session_state"] = "published"
    manifest["mode"] = "theme"
    if new_name:
        manifest["name"] = new_name
    write_json(manifest_path, manifest)

    session_path = target_dir / "edit-session.json"
    session_payload = recursive_replace(load_json(session_path), preview_theme_id, target_theme_id)
    if session_payload:
        session_payload["session_state"] = "published"
        write_json(session_path, session_payload)

    return {
        "mode": "publish_as_new_theme",
        "theme_id": target_theme_id,
        "theme_path": str(target_dir),
        "next_step": "Review the new theme in admin/site-settings and activate it only after approval.",
    }


def replace_base(themes_root: Path, workspace: Path, preview_theme_id: str, base_theme_id: str | None, new_name: str | None, confirm_live_risk: bool) -> dict:
    if not confirm_live_risk:
        raise SystemExit("replace_base_theme requires --confirm-live-risk")

    preview_dir = themes_root / preview_theme_id
    session_payload = load_json(preview_dir / "edit-session.json")
    resolved_base = base_theme_id or session_payload.get("base_theme_id")
    if not resolved_base:
        raise SystemExit("Base theme id is required for replace_base_theme")

    resolved_base = str(resolved_base)
    base_dir = themes_root / resolved_base
    if not base_dir.is_dir():
        raise SystemExit(f"Base theme not found: {base_dir}")

    backups_root = workspace / ".theme-backups"
    backups_root.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    backup_dir = backups_root / f"{resolved_base}-{timestamp}"
    shutil.copytree(base_dir, backup_dir)

    temp_dir = themes_root / f"{resolved_base}__replace__tmp"
    if temp_dir.exists():
        shutil.rmtree(temp_dir)
    shutil.copytree(preview_dir, temp_dir)

    manifest_path = temp_dir / "manifest.json"
    manifest = recursive_replace(load_json(manifest_path), preview_theme_id, resolved_base)
    manifest["session_state"] = "replaced"
    manifest["mode"] = "theme"
    manifest["base_theme_id"] = resolved_base
    manifest["target_theme_id"] = resolved_base
    if new_name:
        manifest["name"] = new_name
    write_json(manifest_path, manifest)

    session_path = temp_dir / "edit-session.json"
    session_payload = recursive_replace(load_json(session_path), preview_theme_id, resolved_base)
    if session_payload:
        session_payload["session_state"] = "replaced"
        write_json(session_path, session_payload)

    shutil.rmtree(base_dir)
    temp_dir.rename(base_dir)

    return {
        "mode": "replace_base_theme",
        "replaced_theme_id": resolved_base,
        "backup_path": str(backup_dir),
        "warning": "If the replaced theme is active, the live site may reflect the change immediately.",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Finalize a GEOFlow preview theme edit session.")
    parser.add_argument("workspace", help="Path to the GEOFlow workspace")
    parser.add_argument("--preview-theme", required=True, help="Preview theme id")
    parser.add_argument("--mode", required=True, choices=["publish_as_new_theme", "replace_base_theme"])
    parser.add_argument("--base-theme", help="Base theme id; used by replace_base_theme")
    parser.add_argument("--new-theme-id", help="Stable theme id for publish_as_new_theme")
    parser.add_argument("--new-name", help="Theme display name after finalization")
    parser.add_argument("--confirm-live-risk", action="store_true", help="Required when replacing a base theme")
    args = parser.parse_args()

    workspace = Path(args.workspace).resolve()
    themes_root = workspace / "themes"
    preview_dir = themes_root / args.preview_theme
    if not preview_dir.is_dir():
        raise SystemExit(f"Preview theme not found: {preview_dir}")

    if args.mode == "publish_as_new_theme":
        result = publish_as_new(themes_root, args.preview_theme, args.new_theme_id, args.new_name)
    else:
        result = replace_base(
            themes_root,
            workspace,
            args.preview_theme,
            args.base_theme,
            args.new_name,
            args.confirm_live_risk,
        )

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
