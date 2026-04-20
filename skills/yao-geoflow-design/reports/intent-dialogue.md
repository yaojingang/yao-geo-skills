# Intent Dialogue

## Recurring Job

Build a reusable skill that can:

- understand GEOFlow's current frontend module and variable contract
- take a reference URL as input when the job is clone or hybrid
- inspect the current template when the job is optimization
- replicate a reference site's UI direction in a GEOFlow-compatible way
- refine the current template through controlled token, module, and layout changes
- output a preview-first template package plan or optimization patch plan rather than a raw HTML copy

## Required Outputs

- a GEOFlow frontend module and variable map
- a formal skill package skeleton
- a clear boundary between safe template replacement and prohibited contract changes
- an optimization-mode workflow for incremental current-template improvement

## Explicit Constraints

- do not change current GEOFlow business logic
- do not break existing frontend data contracts
- preserve GEOFlow page/module responsibilities
- keep the skill distinct from `yao-geoflow-cli`

## Future System Direction

The long-term system direction implied by the request is:

- skill generates template package or optimization package
- GEOFlow later adds template preview and activation in site settings
- preview stays separate from production activation
