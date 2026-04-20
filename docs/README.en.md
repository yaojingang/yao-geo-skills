# Yao GEO Skills

Open-source skill library for `GEO` (`Generative Engine Optimization`) workflows.

Chinese homepage:
[README.md](../README.md)

Note:
`GEO` in this repository means generative engine optimization, not geospatial tooling.

## Positioning And Background

`yao-geo-skills` is a repository for reusable GEO skills that can be shared, validated, and maintained over time.

This repository is not meant to be a loose prompt collection. It is designed to hold complete skill packages with:

- a clear `SKILL.md`
- a stable `agents/interface.yaml`
- references, scripts, evals, and examples when needed
- public sample inputs and outputs

The repository is intended for workflows such as:

- GEO operations
- GEO measurement and attribution planning
- GEO research and evidence collection
- shared GEO templates, schemas, rubrics, and delivery rules

In short:
this repository turns repeated GEO work into reusable skill packages.

## Key Characteristics

- Reusable: each skill should solve a repeatable job, not a one-off request.
- Verifiable: repository-level and skill-level validation are part of the contract.
- Bounded: each skill should say what it is for and what it is not for.
- Open-source safe: public examples must be sanitized and free of private-system dependencies.
- Deliverable-oriented: some skills generate HTML, DOCX, or other shareable outputs.
- Method-driven: complex logic is pushed into `references/`, `scripts/`, and `evals/`, not hidden inside a giant prompt.

## Scope

Good fit for:

- teams that want reusable GEO methods instead of rewriting prompts every time
- people packaging GEO workflows into maintainable skill bundles
- public-facing GEO assets that need quality control and privacy hygiene
- repositories that need readable examples, evaluations, and delivery outputs

Not a fit for:

- storing random prompts
- temporary brainstorming with no packaging intent
- workflows that only work with private systems, private docs, or private APIs
- unrelated generic skill collections

## Repository Logic

The repository follows a simple structure:

1. One skill should own one clear job.
2. `skills/` stores the actual packages.
3. `docs/skills/` stores human-readable guides.
4. `registry/skills.json` stores the inventory.
5. `shared/` stores shared templates, schemas, and conventions.
6. `scripts/validate_repository.py` runs repository-level validation.

The external-facing contract of the repository is centered on three questions:

- What does this skill do?
- How is the quality of this skill controlled?
- Are there public examples that people can inspect?

## Download Options

### Download The Entire Repository

#### Option 1: `git clone`

```bash
git clone https://github.com/yaojingang/yao-geo-skills.git
cd yao-geo-skills
```

#### Option 2: GitHub ZIP

On GitHub, click:

`Code` -> `Download ZIP`

### Download A Single Skill

#### Option 1: Sparse Checkout

```bash
git clone --filter=blob:none --no-checkout https://github.com/yaojingang/yao-geo-skills.git
cd yao-geo-skills
git sparse-checkout init --cone
git sparse-checkout set skills/geo-tracking-plan docs/skills/geo-tracking-plan.md
git checkout main
```

#### Option 2: Manual Download

Open the skill folder in GitHub and download the files you need:

- [skills/geo-tracking-plan](../skills/geo-tracking-plan)
- [skills/geoflow-cli-ops](../skills/geoflow-cli-ops)
- [skills/geoflow-template](../skills/geoflow-template)
- [skills/yao-geoflow-design](../skills/yao-geoflow-design)

## Skill Navigation

The current catalog is grouped into `operations / measurement / research`.

### `operations`

- `geoflow-cli-ops`
  - Purpose: operate an existing GEOFlow system through the local CLI.
  - Best for: catalog lookup, task operations, article upload, review, and publishing.
  - Links:
    - [Guide](skills/geoflow-cli-ops.md)
    - [Package](../skills/geoflow-cli-ops)
    - [GEOFlow project](https://github.com/yaojingang/GEOFlow)

- `geoflow-template`
  - Purpose: map a reference frontend into a GEOFlow-compatible theme package plan with tokens, module mappings, and preview-first structure.
  - Best for: frontend template cloning, GEOFlow theme planning, reference-site style mapping, and preview-safe theme package preparation.
  - Links:
    - [Guide (CN)](skills/geoflow-template.md)
    - [Guide (EN)](skills/geoflow-template.en.md)
    - [Package](../skills/geoflow-template)
    - [GEOFlow project](https://github.com/yaojingang/GEOFlow)

- `yao-geoflow-design`
  - Purpose: clone, optimize, and refine GEOFlow-compatible frontends through design audits, token deltas, module mappings, and preview-first packages.
  - Best for: current-template optimization, hybrid reference-plus-optimization jobs, incremental GEOFlow theme iteration, and safe frontend design adjustments.
  - Links:
    - [Guide (CN)](skills/yao-geoflow-design.md)
    - [Guide (EN)](skills/yao-geoflow-design.en.md)
    - [Package](../skills/yao-geoflow-design)
    - [GEOFlow project](https://github.com/yaojingang/GEOFlow)

### `measurement`

- `geo-tracking-plan`
  - Purpose: generate a company-specific GEO backend tracking plan from a company name and supporting context.
  - Best for: official-site-first retrieval, business recognition, direct-vs-indirect measurement design, HTML and DOCX deliverables.
  - Public demos:
    - Overseas demo:
      - [HubSpot input](../skills/geo-tracking-plan/examples/hubspot-demo/report_input.json)
      - [HTML](../skills/geo-tracking-plan/examples/hubspot-demo/hubspot-geo-tracking-plan.html)
      - [DOCX](../skills/geo-tracking-plan/examples/hubspot-demo/hubspot-geo-tracking-plan.docx)
    - China synthetic demo:
      - [Lingxu input](../skills/geo-tracking-plan/examples/lingxu-demo/report_input.json)
      - [HTML](../skills/geo-tracking-plan/examples/lingxu-demo/lingxu-cn-geo-tracking-plan.html)
      - [DOCX](../skills/geo-tracking-plan/examples/lingxu-demo/lingxu-cn-geo-tracking-plan.docx)
  - Links:
    - [Guide](skills/geo-tracking-plan.md)
    - [Package](../skills/geo-tracking-plan)
    - [Overseas screenshot](../skills/geo-tracking-plan/assets/screenshots/hubspot-geo-tracking-plan.png)
    - [China screenshot](../skills/geo-tracking-plan/assets/screenshots/lingxu-cn-geo-tracking-plan.png)

### `research`

- Coming soon
  - Reserved for GEO keyword discovery, competitor evidence scans, brand fact sheets, and content audit skills.

## Example Outputs

The most complete public examples in the repository currently come from `geo-tracking-plan`:

- public-company overseas demo: HubSpot
- public synthetic China demo: Lingxu
- sample deliverables: `report_input.json`, `HTML`, `DOCX`, screenshots

These examples are not published as real operating conclusions. They exist to show:

- how methodology becomes structured input
- how a skill renders that input into a delivery artifact
- how China and overseas GEO measurement logic differ

## Directory Guide

```text
yao-geo-skills/
├── README.md
├── LICENSE
├── .github/
├── docs/
│   ├── README.en.md
│   ├── repository-design.md
│   ├── input-output-contract.md
│   ├── naming-conventions.md
│   ├── eval-policy.md
│   ├── publishing-rules.md
│   └── skills/
├── registry/
├── scripts/
├── shared/
└── skills/
```

Useful paths:

- [skills/](../skills): actual skill packages
- [docs/skills/](skills): human-readable guides
- [registry/skills.json](../registry/skills.json): skill inventory
- [scripts/validate_repository.py](../scripts/validate_repository.py): repository validator
- [docs/](.): repository rules and contracts

## Repository Documents

- [Chinese homepage](../README.md)
- [Changelog](CHANGELOG.en.md)
- [Repository Design](repository-design.md)
- [Input And Output Contract](input-output-contract.md)
- [Naming Conventions](naming-conventions.md)
- [Eval Policy](eval-policy.md)
- [Publishing Rules](publishing-rules.md)

## Design Principles

- One skill, one clear job
- Prefer public, verifiable evidence for factual GEO work
- Outputs should be readable by humans and checkable by machines
- Public examples must be sanitized and safe to share
- Evaluation is expected, not optional
- Long-term maintainable skill packages matter more than large prompt dumps

## Contribution And Publishing

1. Add or update a skill under `skills/<skill-id>/`.
2. Add or update the matching guide under `docs/skills/`.
3. Register the skill in [`registry/skills.json`](../registry/skills.json).
4. Run validation:

```bash
python3 scripts/validate_repository.py
```

5. Review the diff carefully.
6. Commit and push.
7. Use a PR for non-trivial changes.

For more detail, see:
[publishing-rules.md](publishing-rules.md)
