# Repository Design

`yao-geo-skills` is a collection repository, not a single skill package.

The repository should stay opinionated and compact:

- `skills/` stores reusable GEO skills
- `shared/` stores repository-wide contracts and reusable materials
- `docs/` stores policy and design rules
- `registry/skills.json` is the fact source for repository inventory

## Skill Package Shape

Each skill should follow this layout:

```text
skills/<skill-id>/
├── SKILL.md
├── agents/
│   └── interface.yaml
├── evals/
│   ├── trigger_cases.json
│   ├── expected_artifacts.json
│   ├── rubric.md
│   └── failure_cases.md
├── references/
├── scripts/
└── templates/
```

Not every skill needs every folder, but every skill must have:

- `SKILL.md`
- `evals/trigger_cases.json`
- `evals/expected_artifacts.json`
- `templates/brief-template.md`

## Shared Assets

`shared/` is for contracts reused by multiple GEO skills:

- `shared/schemas/`: common schemas such as brand brief inputs
- `shared/templates/`: reusable deliverable templates
- `shared/rubrics/`: repository-wide scoring rubrics

Only put something in `shared/` if at least two skills can use it without local specialization.

## Output Philosophy

GEO work should produce both:

- readable deliverables for operators
- machine-checkable artifacts for validation and regression

That is why skills should prefer paired outputs like:

- `research-summary.md`
- `sources.json`
- `quality-report.json`

## Registry

`registry/skills.json` tracks:

- `id`
- `status`
- `owner`
- `stage`
- `path`
- `summary`
- `public_repo_path`
- `last_updated`

The registry is the source of truth for what the repository intends to maintain.
