# Yao GEOFlow Design

`yao-geoflow-design` is a local skill for discovering GEOFlow themes, selecting a target theme, creating preview-first edit sessions, and then optimizing or refining the chosen frontend through safe theme packages.

## Primary Use

- inventory GEOFlow frontend modules, variables, and rendering boundaries
- discover existing themes in the current GEOFlow workspace
- select a target theme and prepare a preview edit fork before touching live theme files
- inspect a reference URL and extract reusable visual direction
- map reference style tokens onto GEOFlow's existing frontend modules
- audit the target theme for hierarchy, spacing, responsive, and module-consistency issues
- generate either a full theme package, a preview edit session, or an incremental optimization patch plan
- prepare the system-facing integration plan for preview, confirmation, replacement, or publish-as-new flows

## Boundary

This skill does not directly deploy a template to production, rewrite GEOFlow backend business logic, or replace current data contracts with arbitrary copied HTML. It works by preserving GEOFlow's frontend modules and variables while changing presentation-layer structure and styles in a controlled preview session or theme package.

## Package Map

- `SKILL.md`: trigger boundary and execution workflow
- `agents/interface.yaml`: canonical interface metadata
- `agents/openai.yaml`: OpenAI-friendly interface metadata
- `references/geoflow-frontend-map.md`: current frontend module, variable, and function contract
- `references/template-boundary.md`: system boundary for safe template cloning and current-template optimization
- `references/theme-package-contract.md`: expected output format for generated theme packages, preview edit sessions, and optimization passes
- `references/design-optimization-playbook.md`: optimization-mode workflow and heuristics
- `references/theme-edit-workflow.md`: target-theme discovery, preview-fork editing, and finalize workflow
- `evals/trigger_cases.json`: trigger boundary checks
- `reports/intent-dialogue.md`: captured job framing
- `reports/reference-scan.md`: local-fit reference notes
- `reports/iteration-directions.md`: next engineering moves
