# Yao GEO Skills Changelog

This document tracks public repository releases for the skill catalog. Update this file together with the Chinese version in `CHANGELOG.md` whenever a new skill or a significant repository-level change is pushed.

## 2026-04-20

### Renamed `geoflow-template` to `yao-geoflow-template`

- Moved the public skill package to `skills/yao-geoflow-template`
- Moved the public guides to:
  - `docs/skills/yao-geoflow-template.md`
  - `docs/skills/yao-geoflow-template.en.md`
- Updated the repository homepage, `registry/skills.json`, and public navigation links
- The rename does not change the skill boundary; it still covers GEOFlow frontend template mapping and preview-first output packages

### Initial publication of `yao-geoflow-design`

- Added `skills/yao-geoflow-design`
- Expanded the earlier `yao-geoflow-template` direction into a broader frontend design skill:
  - supports reference-site cloning onto GEOFlow modules
  - supports auditing, optimizing, and incrementally adjusting the current template
  - supports preview-first theme-package and optimization-pass outputs
- Added Chinese and English documentation:
  - `docs/skills/yao-geoflow-design.md`
  - `docs/skills/yao-geoflow-design.en.md`
- Updated the repository homepage and `registry/skills.json` so `yao-geoflow-design` is part of the public catalog

## 2026-04-18

### Initial publication of `geoflow-template` (current name: `yao-geoflow-template`)

- Initially published as `skills/geoflow-template`; the public package now lives at `skills/yao-geoflow-template`
- Added frontend template-cloning and theme-package planning support:
  - built around GEOFlow frontend modules, variables, and rendering contracts
  - maps a reference URL into a GEOFlow-compatible theme package plan
  - supports preview-first output targets such as `tokens.json`, `mapping.json`, and `manifest.json`
- Added Chinese and English documentation:
  - `docs/skills/yao-geoflow-template.md`
  - `docs/skills/yao-geoflow-template.en.md`
- Updated the repository homepage and `registry/skills.json` so the skill is part of the public catalog
