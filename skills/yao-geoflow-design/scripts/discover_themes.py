#!/usr/bin/env python3
import argparse
import json
from pathlib import Path


def load_json(path: Path) -> dict:
    if not path.is_file():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def derive_preview_routes(theme_id: str, manifest: dict) -> list[str]:
    routes = manifest.get("preview_routes")
    if isinstance(routes, list) and routes:
        return [str(item) for item in routes]

    sample_routes = manifest.get("sample_routes")
    if isinstance(sample_routes, dict) and sample_routes:
        return [str(value) for value in sample_routes.values()]

    return [
        f"/preview/{theme_id}/",
        f"/preview/{theme_id}/category",
        f"/preview/{theme_id}/article",
        f"/preview/{theme_id}/archive",
    ]


def theme_record(theme_dir: Path) -> dict:
    theme_id = theme_dir.name
    manifest = load_json(theme_dir / "manifest.json")
    templates_dir = theme_dir / "templates"
    template_files = sorted(path.relative_to(theme_dir).as_posix() for path in templates_dir.glob("*.php")) if templates_dir.is_dir() else []

    editable_files = list(template_files)
    for relative in ("assets/theme.css", "manifest.json", "tokens.json", "mapping.json"):
        if (theme_dir / relative).is_file():
            editable_files.append(relative)

    session_state = str(manifest.get("session_state", "")).strip()
    is_preview_session = session_state == "preview" or theme_id.startswith("preview-") or theme_id.endswith("-preview")

    return {
        "id": theme_id,
        "name": manifest.get("name", theme_id),
        "description": manifest.get("description", ""),
        "version": manifest.get("version", ""),
        "base_theme_id": manifest.get("base_theme_id", ""),
        "mode": manifest.get("mode", ""),
        "session_state": session_state,
        "is_preview_session": is_preview_session,
        "preview_routes": derive_preview_routes(theme_id, manifest),
        "templates": [Path(item).stem for item in template_files],
        "editable_files": editable_files,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Discover themes in a GEOFlow workspace.")
    parser.add_argument("workspace", help="Path to the GEOFlow workspace")
    args = parser.parse_args()

    workspace = Path(args.workspace).resolve()
    themes_root = workspace / "themes"

    theme_system = {
        "themes_root_exists": themes_root.is_dir(),
        "theme_preview_php": (workspace / "includes/theme_preview.php").is_file(),
        "theme_preview_entry": (workspace / "theme-preview.php").is_file(),
        "admin_theme_settings": (workspace / "admin/site-settings.php").is_file(),
    }

    themes = []
    if themes_root.is_dir():
        for child in sorted(themes_root.iterdir()):
            if child.is_dir():
                themes.append(theme_record(child))

    report = {
        "workspace": str(workspace),
        "themes_root": str(themes_root),
        "theme_system_detected": all(theme_system.values()),
        "theme_system_signals": theme_system,
        "theme_count": len(themes),
        "themes": themes,
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
