# Yao GEOFlow Design

`yao-geoflow-design` is a local skill for analyzing the current GEOFlow frontend contract, mapping it to reference site styles, and optimizing or refining the current GEOFlow template through preview-first design packages.

## Primary Use

- inventory GEOFlow frontend modules, variables, and rendering boundaries
- inspect a reference URL and extract reusable visual direction
- map reference style tokens onto GEOFlow's existing frontend modules
- audit the current template for hierarchy, spacing, responsive, and module-consistency issues
- generate either a full theme-package specification or an incremental optimization patch plan
- prepare the system-facing integration plan for template preview, optimization, and activation

## Boundary

This skill does not directly deploy a template to production, rewrite GEOFlow backend business logic, or replace current data contracts with arbitrary copied HTML. It works by preserving GEOFlow's frontend modules and variables while changing presentation-layer structure and styles in a controlled package or optimization pass.

## Package Map

- `SKILL.md`: trigger boundary and execution workflow
- `agents/interface.yaml`: canonical interface metadata
- `agents/openai.yaml`: OpenAI-friendly interface metadata
- `references/geoflow-frontend-map.md`: current frontend module, variable, and function contract
- `references/template-boundary.md`: system boundary for safe template cloning and current-template optimization
- `references/theme-package-contract.md`: expected output format for generated theme packages and optimization passes
- `references/design-optimization-playbook.md`: optimization-mode workflow and heuristics
- `evals/trigger_cases.json`: trigger boundary checks
- `reports/intent-dialogue.md`: captured job framing
- `reports/reference-scan.md`: local-fit reference notes
- `reports/iteration-directions.md`: next engineering moves
