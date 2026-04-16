# Repository Design

`yao-geo-skills` is a collection repository, not a single skill package.

The repository should stay opinionated and compact:

- `skills/` stores reusable GEO skills
- `shared/` stores repository-wide contracts and reusable materials
- `docs/` stores policy, design rules, and human-facing skill guides
- `scripts/` stores repository-level validation and maintenance helpers
- `registry/skills.json` is the fact source for repository inventory

## Top-Level Storage Rule

Keep `skills/` flat until there is real evidence that family subfolders improve navigation more than they increase friction.

Current rule:

- use `skills/<skill-id>/`
- do not introduce `skills/content/`, `skills/workflow/`, or similar family subfolders yet
- revisit only after the repository has enough published skills to justify another layer

## Skill Package Shape

Each skill should follow this layout:

```text
skills/<skill-id>/
├── SKILL.md
├── agents/
│   └── interface.yaml
├── assets/
├── evals/
│   ├── trigger_cases.json
│   ├── expected_artifacts.json
│   ├── rubric.md
│   └── failure_cases.md
├── examples/
│   ├── input/
│   └── expected-output/
├── references/
├── scripts/
└── templates/
```

Not every skill needs every folder, but every skill must have:

- `SKILL.md`
- `evals/trigger_cases.json`
- `evals/expected_artifacts.json`
- `templates/brief-template.md`

For public reusable skills, `examples/` is strongly recommended and should contain only sanitized samples.

## Human-Facing Guides

Each published public skill should also have a guide page under:

```text
docs/skills/<skill-id>.md
```

Guide pages should explain:

- what the skill does
- what it does not do
- key inputs and outputs
- public example files
- screenshots when visual deliverables matter

`README.md` should link to these guides. `registry/skills.json` remains the machine-facing fact source.

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

These artifacts should exist as runtime outputs, not as committed repository history, unless they have been sanitized and moved into `examples/`.

## Registry

`registry/skills.json` tracks:

- `id`
- `family`
- `maturity`
- `tags`
- `requires_web`
- `primary_outputs`
- `status`
- `owner`
- `stage`
- `path`
- `summary`
- `public_repo_path`
- `last_updated`

The registry is the source of truth for what the repository intends to maintain.

Recommended semantics:

- `family`: high-level bucket such as `research`, `generation`, `optimization`, or `audit`
- `maturity`: `scaffold`, `draft`, `beta`, `stable`
- `requires_web`: whether live web verification is required for normal operation
- `primary_outputs`: the main artifact names the skill is expected to produce
