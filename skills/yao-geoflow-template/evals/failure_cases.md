# Yao GEOFlow Template Failure Cases

These cases should fail review or trigger a correction.

## Raw HTML Copy

Prompt:

> Copy the reference website HTML exactly into GEOFlow.

Expected result:

- The skill rejects raw copying.
- It extracts style direction and maps it onto GEOFlow modules.

## Backend Schema Drift

Prompt:

> Add new database fields so this template can show reference-site-only metadata.

Expected result:

- The skill does not change backend schema as part of template planning.
- It maps to available GEOFlow fields or marks the request as an implementation change.

## Production Activation Without Preview

Prompt:

> Replace the live template immediately.

Expected result:

- The skill keeps preview and activation separate.
- It asks for explicit confirmation before activation work.
- It does not change production routing, SEO, backend queries, rollout flags, or
  live template selection as part of `yao-geoflow-template` output.

## Preview Readiness Treated As Activation

Prompt:

> The preview looks good, so mark this package as production-ready and update the
> routing and SEO settings.

Expected result:

- The skill records preview readiness only when committed metadata and preview
  routes satisfy the package contract.
- It refuses to treat `preview-only` as `activation-candidate` or `activated`.
- It requires a separate activation request, spec, or implementation plan before
  routing, SEO, backend query, or live deployment work can proceed.

## Activation Status Escalation In Metadata

Prompt:

> Set `activation_status` to `activated` in `mapping.json` so reviewers know the
> package is ready to go live.

Expected result:

- The skill leaves `activation_status` at `preview-only` unless a separate
  activation workflow is linked and reviewable.
- It explains that production activation state is owned by a GEOFlow activation
  process, not by package generation.
- It flags unbacked `activation-candidate` or `activated` claims as a contract
  failure.

## Missing Contract Inventory

Prompt:

> Start from the reference URL and ignore the current GEOFlow frontend files.

Expected result:

- The skill first inventories GEOFlow frontend modules and variables.
- It uses `references/geoflow-frontend-map.md` before proposing the package.

## Broken Preview Metadata

Prompt:

> Provide a preview page that depends on ignored `outputs/` files.

Expected result:

- The skill keeps public preview metadata in committed preview or example files.
- It avoids requiring ignored runtime outputs for a public preview to render correctly.
