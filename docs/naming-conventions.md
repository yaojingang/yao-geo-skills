# Naming Conventions

Consistency matters more than cleverness.

## Repository

- Repository name: `yao-geo-skills`

## Skill IDs

- Use lowercase kebab-case
- Always use the `geo-` prefix
- Prefer `object + action` naming
- Keep names narrow and operational

Good examples:

- `geo-keyword-discovery`
- `geo-competitor-scan`
- `geo-answer-optimizer`
- `geo-brand-fact-sheet`
- `geo-content-audit`

Avoid:

- `geo-assistant`
- `geo-toolkit`
- `geo-master`
- `best-geo-skill`

## File And Directory Names

Repository-wide filenames should stay fixed:

- `SKILL.md`
- `agents/interface.yaml`
- `templates/brief-template.md`
- `evals/trigger_cases.json`
- `evals/expected_artifacts.json`
- `research-summary.md`
- `sources.json`
- `quality-report.json`

## Family Suffixes

Use these suffix patterns to keep the skill family understandable:

- research: `-scan`, `-discovery`
- generation: `-generator`, `-builder`
- optimization: `-optimizer`
- audit: `-audit`
- reference asset creation: `-fact-sheet`

## Registry Consistency

These values must match exactly:

- directory name
- `SKILL.md` frontmatter `name`
- `registry/skills.json` `id`
