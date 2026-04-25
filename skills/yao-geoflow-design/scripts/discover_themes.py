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


def view_name(relative_path: str) -> str:
    if relative_path.endswith(".blade.php"):
        relative_path = relative_path[:-10]
    return relative_path.replace("/", ".")


def derive_preview_routes(theme_id: str, manifest: dict, framework: str) -> list[str]:
    routes = manifest.get("preview_routes")
    if isinstance(routes, list) and routes:
        return [str(item) for item in routes]

    sample_routes = manifest.get("sample_routes")
    if isinstance(sample_routes, dict) and sample_routes:
        return [str(value) for value in sample_routes.values()]

    if framework == "laravel":
        return ["/", "/category/{slug}", "/article/{slug}", "/archive"]

    return [
        f"/preview/{theme_id}/",
        f"/preview/{theme_id}/category",
        f"/preview/{theme_id}/article",
        f"/preview/{theme_id}/archive",
    ]


def theme_record(theme_dir: Path, framework: str) -> dict:
    theme_id = theme_dir.name
    manifest = load_json(theme_dir / "manifest.json")

    if framework == "laravel":
        blade_files = sorted(
            path.relative_to(theme_dir).as_posix()
            for path in theme_dir.rglob("*.blade.php")
            if ".theme-backups" not in path.parts
        )
        editable_files = list(blade_files)
    else:
        templates_dir = theme_dir / "templates"
        template_files = sorted(path.relative_to(theme_dir).as_posix() for path in templates_dir.glob("*.php")) if templates_dir.is_dir() else []
        editable_files = list(template_files)
        blade_files = []

    for relative in ("assets/theme.css", "manifest.json", "tokens.json", "mapping.json"):
        if (theme_dir / relative).is_file() and relative not in editable_files:
            editable_files.append(relative)

    for relative in ("edit-session.json", "change-plan.md", "preview-notes.md"):
        if (theme_dir / relative).is_file() and relative not in editable_files:
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
        "preview_routes": derive_preview_routes(theme_id, manifest, framework),
        "templates": [view_name(item) for item in blade_files] if framework == "laravel" else [Path(item).stem for item in editable_files if item.startswith("templates/")],
        "editable_files": editable_files,
    }


def detect_workspace(workspace: Path) -> dict:
    laravel_root = workspace / "resources" / "views" / "theme"
    legacy_root = workspace / "themes"
    laravel_signals = {
        "artisan": (workspace / "artisan").is_file(),
        "routes_web": (workspace / "routes" / "web.php").is_file(),
        "site_views": (workspace / "resources" / "views" / "site").is_dir(),
        "theme_views": laravel_root.is_dir(),
        "theme_resolver": (workspace / "app" / "Support" / "Site" / "SiteThemeViewResolver.php").is_file(),
    }
    legacy_signals = {
        "themes_root_exists": legacy_root.is_dir(),
        "theme_preview_php": (workspace / "includes" / "theme_preview.php").is_file(),
        "theme_preview_entry": (workspace / "theme-preview.php").is_file(),
        "admin_theme_settings": (workspace / "admin" / "site-settings.php").is_file(),
    }

    if laravel_signals["theme_views"] or (laravel_signals["artisan"] and laravel_signals["site_views"]):
        return {
            "framework": "laravel",
            "themes_root": laravel_root,
            "theme_system_detected": laravel_signals["artisan"] and laravel_signals["site_views"] and laravel_signals["theme_views"],
            "theme_system_signals": laravel_signals,
            "preview_support": "admin_activation_or_static_preview",
        }

    return {
        "framework": "legacy_php",
        "themes_root": legacy_root,
        "theme_system_detected": all(legacy_signals.values()),
        "theme_system_signals": legacy_signals,
        "preview_support": "legacy_preview_routes",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Discover themes in a GEOFlow workspace.")
    parser.add_argument("workspace", help="Path to the GEOFlow workspace")
    args = parser.parse_args()

    workspace = Path(args.workspace).resolve()
    detected = detect_workspace(workspace)
    themes_root = detected["themes_root"]

    themes = []
    if themes_root.is_dir():
        for child in sorted(themes_root.iterdir()):
            if child.is_dir():
                themes.append(theme_record(child, str(detected["framework"])))

    report = {
        "workspace": str(workspace),
        "framework": detected["framework"],
        "themes_root": str(themes_root),
        "theme_system_detected": detected["theme_system_detected"],
        "theme_system_signals": detected["theme_system_signals"],
        "preview_support": detected["preview_support"],
        "theme_count": len(themes),
        "themes": themes,
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
