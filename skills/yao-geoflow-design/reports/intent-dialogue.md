# Intent Dialogue

## Recurring Job

Build a reusable skill that can:

- inspect the current GEOFlow system and discover the existing themes under `/themes`
- let the operator select a target theme explicitly before edits begin
- fork the selected theme into a preview edit session inside the current GEOFlow system
- understand GEOFlow's current frontend module and variable contract
- take a reference URL as input when the job is clone or hybrid
- inspect the current target theme when the job is optimization or edit-theme
- replicate a reference site's UI direction in a GEOFlow-compatible way
- refine the current theme through controlled token, module, and layout changes
- keep the work in preview URLs that can be reviewed inside GEOFlow before any live decision
- finalize the reviewed work as either `publish_as_new_theme` or `replace_base_theme`
- actively remind the operator about boundaries, confirmation points, and live-risk steps

## Required Outputs

- a theme discovery inventory for the current GEOFlow workspace
- a preview theme edit session with preview URLs
- a GEOFlow frontend module and variable map
- a formal skill package skeleton
- a clear boundary between safe template replacement and prohibited contract changes
- an optimization-mode workflow for incremental current-template improvement
- a safe finalize flow for replace-vs-publish decisions

## Explicit Constraints

- do not change current GEOFlow business logic
- do not break existing frontend data contracts
- preserve GEOFlow page/module responsibilities
- do not overwrite the live target theme on the first pass when a preview fork can be created
- only add display modules when they can be powered by existing GEOFlow data
- back up the base theme before replace flow
- keep the skill distinct from `yao-geoflow-cli`

## Future System Direction

The long-term system direction implied by the request is:

- skill works with GEOFlow's existing `/themes`, `/preview/...`, and `admin/site-settings.php` theme system
- theme edits happen through an in-system preview workflow rather than detached static mockups
- preview remains separate from production activation or replacement
- confirmation decides whether the preview fork becomes a new admin-selectable template or replaces the original theme
