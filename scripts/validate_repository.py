#!/usr/bin/env python3

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent

TOP_LEVEL_REQUIRED_FILES = [
    ROOT / "README.md",
    ROOT / "docs" / "repository-design.md",
    ROOT / "docs" / "publishing-rules.md",
    ROOT / "registry" / "skills.json",
]

SKILL_REQUIRED_FILES = [
    "SKILL.md",
    "evals/trigger_cases.json",
    "evals/expected_artifacts.json",
    "templates/brief-template.md",
]

TRACKED_OUTPUT_PATH_PARTS = {"outputs"}


def fail(message: str) -> None:
    print(f"ERROR: {message}")
    sys.exit(1)


def load_registry() -> dict:
    registry_path = ROOT / "registry" / "skills.json"
    try:
        return json.loads(registry_path.read_text())
    except json.JSONDecodeError as exc:
        fail(f"registry/skills.json is invalid JSON: {exc}")


def validate_top_level_files() -> None:
    missing = [str(path.relative_to(ROOT)) for path in TOP_LEVEL_REQUIRED_FILES if not path.exists()]
    if missing:
        fail(f"Missing required top-level files: {', '.join(missing)}")


def validate_registry(registry: dict) -> dict:
    if "inventory_contract" not in registry:
        fail("registry/skills.json is missing inventory_contract")

    contract = registry["inventory_contract"]
    required_fields = contract.get("required_skill_fields")
    allowed_statuses = set(contract.get("allowed_statuses", []))
    allowed_maturity = set(contract.get("allowed_maturity", []))
    skills = registry.get("skills")

    if not isinstance(required_fields, list) or not required_fields:
        fail("inventory_contract.required_skill_fields must be a non-empty list")
    if not isinstance(skills, list):
        fail("registry.skills must be a list")

    seen_ids = set()
    for skill in skills:
        missing_fields = [field for field in required_fields if field not in skill]
        if missing_fields:
            fail(f"Skill entry {skill.get('id', '<missing-id>')} is missing fields: {', '.join(missing_fields)}")

        skill_id = skill["id"]
        if skill_id in seen_ids:
            fail(f"Duplicate skill id in registry: {skill_id}")
        seen_ids.add(skill_id)

        if skill["status"] not in allowed_statuses:
            fail(f"Skill {skill_id} has invalid status: {skill['status']}")
        if skill["maturity"] not in allowed_maturity:
            fail(f"Skill {skill_id} has invalid maturity: {skill['maturity']}")
        if not isinstance(skill["tags"], list):
            fail(f"Skill {skill_id} tags must be a list")
        if not isinstance(skill["primary_outputs"], list):
            fail(f"Skill {skill_id} primary_outputs must be a list")
        if not isinstance(skill["requires_web"], bool):
            fail(f"Skill {skill_id} requires_web must be a boolean")

    return {skill["id"]: skill for skill in skills}


def iter_skill_directories():
    skills_root = ROOT / "skills"
    if not skills_root.exists():
        fail("skills directory is missing")
    return sorted(path for path in skills_root.iterdir() if path.is_dir())


def validate_skill_directories(registry_by_id: dict) -> None:
    for skill_dir in iter_skill_directories():
        skill_id = skill_dir.name

        if skill_id.startswith("."):
            continue

        for rel_path in SKILL_REQUIRED_FILES:
            expected = skill_dir / rel_path
            if not expected.exists():
                fail(f"Skill {skill_id} is missing required file: {rel_path}")

        outputs_dir = skill_dir / "outputs"
        if outputs_dir.exists():
            fail(f"Skill {skill_id} must not commit outputs/ into the repository")

        examples_dir = skill_dir / "examples"
        if not examples_dir.exists():
            print(f"WARN: Skill {skill_id} has no examples/ directory")

        if skill_id not in registry_by_id:
            fail(f"Skill directory {skill_id} is not registered in registry/skills.json")

        registered_path = registry_by_id[skill_id]["path"]
        expected_path = f"skills/{skill_id}"
        if registered_path != expected_path:
            fail(f"Skill {skill_id} registry path mismatch: expected {expected_path}, got {registered_path}")


def validate_registry_paths_exist(registry_by_id: dict) -> None:
    for skill_id, metadata in registry_by_id.items():
        path = ROOT / metadata["path"]
        if not path.exists():
            fail(f"Registry entry {skill_id} points to missing path: {metadata['path']}")

        if any(part in TRACKED_OUTPUT_PATH_PARTS for part in Path(metadata["path"]).parts):
            fail(f"Registry entry {skill_id} points to an outputs path, which is not allowed")


def main() -> None:
    validate_top_level_files()
    registry = load_registry()
    registry_by_id = validate_registry(registry)
    validate_skill_directories(registry_by_id)
    validate_registry_paths_exist(registry_by_id)
    print("Repository validation passed.")


if __name__ == "__main__":
    main()
