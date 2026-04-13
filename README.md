# Yao GEO Skills

Open-source GEO workflows for reusable agent skills.

`GEO` in this repository means `Generative Engine Optimization`, not geospatial tooling.

This repository is for skill packages that help teams research, generate, audit, and optimize content for AI-native discovery and answer surfaces. The goal is not to collect loose prompts. The goal is to publish reusable GEO assets with stable contracts, clear boundaries, and repeatable evaluation.

## What Lives Here

- Narrow, reusable GEO skill packages under `skills/`
- Shared input schemas, templates, and rubrics under `shared/`
- Repository-level design and publishing rules under `docs/`
- A registry of published and planned skills under `registry/skills.json`

## Design Principles

- One skill, one job
- Structured input over hidden prompt assumptions
- Human-readable and machine-checkable outputs
- Current-source verification for factual GEO work
- Evaluation is required, not optional

## Repository Docs

- [Repository Design](docs/repository-design.md)
- [Input And Output Contract](docs/input-output-contract.md)
- [Naming Conventions](docs/naming-conventions.md)
- [Eval Policy](docs/eval-policy.md)
- [Publishing Rules](docs/publishing-rules.md)

## Initial Skill Families

- `geo-keyword-discovery`
- `geo-competitor-scan`
- `geo-answer-optimizer`
- `geo-brand-fact-sheet`
- `geo-content-audit`

## Published Skills

- `geoflow-cli-ops`: operate an existing [GEOFlow](https://github.com/yaojingang/GEOFlow) system through the local `geoflow` CLI for task management, article upload, review, and publish flows.

## Repository Layout

```text
yao-geo-skills/
├── README.md
├── LICENSE
├── docs/
├── registry/
├── shared/
└── skills/
```

## Push Flow

1. Update or add the skill package locally.
2. Run the skill-level checks and repository-level validation.
3. Review the diff and stage only intended files.
4. Commit with a terse scope-first message.
5. Push to GitHub.
6. Open a PR for non-trivial changes. Direct push to `main` is reserved for repository bootstrap and very small maintenance edits.

The detailed GitHub workflow lives in [docs/publishing-rules.md](docs/publishing-rules.md).
