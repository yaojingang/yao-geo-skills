# Intent Dialogue

## Recurring Job

Build a reusable skill that can:

- understand GEOFlow's current frontend module and variable contract
- take a reference URL as input
- replicate the reference site's UI direction in a GEOFlow-compatible way
- output a preview-first template package plan rather than a raw HTML copy

## Required Outputs

- a GEOFlow frontend module and variable map
- a formal skill package skeleton
- a clear boundary between safe template replacement and prohibited contract changes

## Explicit Constraints

- do not change current GEOFlow business logic
- do not break existing frontend data contracts
- preserve GEOFlow page/module responsibilities
- keep the skill distinct from `geoflow-cli-ops`

## Future System Direction

The long-term system direction implied by the request is:

- skill generates template package
- GEOFlow later adds template preview and activation in site settings
- preview stays separate from production activation
