# GEOFlow Template

`yao-geoflow-template` is a local skill for analyzing the current GEOFlow frontend contract, mapping it to reference site styles, and producing a reusable theme-package plan for previewable template variants.

## Primary Use

- inventory GEOFlow frontend modules, variables, and rendering boundaries
- inspect a reference URL and extract reusable visual direction
- map reference style tokens onto GEOFlow's existing frontend modules
- generate a theme-package specification for preview-first template work
- prepare the system-facing integration plan for template preview and activation

## Boundary

This skill does not directly deploy a template to production, rewrite GEOFlow backend business logic, or replace current data contracts with arbitrary copied HTML. It works by preserving GEOFlow's frontend modules and variables while changing presentation-layer structure and styles in a controlled package.

## Package Map

- `SKILL.md`: trigger boundary and execution workflow
- `agents/interface.yaml`: canonical interface metadata
- `agents/openai.yaml`: OpenAI-friendly interface metadata
- `references/geoflow-frontend-map.md`: current frontend module, variable, and function contract
- `references/template-boundary.md`: system boundary for safe template cloning
- `references/theme-package-contract.md`: expected output format for generated template packages
- `evals/trigger_cases.json`: trigger boundary checks
- `reports/intent-dialogue.md`: captured job framing
- `reports/reference-scan.md`: local-fit reference notes
- `reports/iteration-directions.md`: next engineering moves
