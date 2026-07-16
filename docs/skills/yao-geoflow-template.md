# Yao GEOFlow Template

`yao-geoflow-template` 现在是 legacy 兼容入口。它只用于解释旧 GEOFlow PHP 模板包、历史 `tokens.json` / `mapping.json` / `manifest.json` 输出，以及旧 `index.php`、`article.php`、`category.php`、`archive.php`、`includes/*.php` 契约。当前 Laravel Blade 主题、参考站拆解、首页模块、`lead_form` 和渠道前端适配统一交给 `yao-geoflow-design`。

## 中文概述

适合：

- 查看旧 PHP 模板包为什么要求 `index.php`、`article.php`、`category.php`、`archive.php`
- 识别历史 `outputs/qiaomu-editorial-20260418` 里的 mapping、tokens 和 manifest
- 把旧模板包总结成可交给 `yao-geoflow-design` 的迁移说明
- 处理用户明确要求的 “legacy GEOFlow template skill” 或 “旧 PHP 模板包” 问题

不适合：

- 当前 Laravel Blade 主题设计
- 参考站克隆、首页模块设计、主题视觉改造
- `lead_form`、homepage builder、渠道 frontend-capabilities 或 target package 映射
- 旧 PHP 模板包直接部署到当前 Laravel GEOFlow
- 后端实现、数据库迁移、SEO 契约或路由变更

## English Overview

Use `yao-geoflow-template` only for explicit legacy GEOFlow template-skill questions or historical PHP template-package outputs. Route current GEOFlow frontend work to `yao-geoflow-design`.

Best for:

- explaining old PHP template-package contracts
- reviewing historical mapping, tokens, and manifest files
- writing migration notes for `yao-geoflow-design`

Not for:

- new Laravel Blade themes
- reference-site cloning or homepage module design
- lead forms, channel frontend capability checks, or target-package mapping
- direct deployment of legacy PHP templates
- backend refactors, SEO contract changes, or route rewrites

## Package Links

- Skill package: [skills/yao-geoflow-template](../../skills/yao-geoflow-template)
- Trigger boundary: [trigger_cases.json](../../skills/yao-geoflow-template/evals/trigger_cases.json)
- Frontend map: [geoflow-frontend-map.md](../../skills/yao-geoflow-template/references/geoflow-frontend-map.md)
- Theme contract: [theme-package-contract.md](../../skills/yao-geoflow-template/references/theme-package-contract.md)
- Upgrade report: [geoflow-skill-upgrade-2026-07-05.md](../../skills/yao-geoflow-template/reports/geoflow-skill-upgrade-2026-07-05.md)
- Example mapping report: [qiaomu-blog-mapping-2026-04-18.md](../../skills/yao-geoflow-template/reports/qiaomu-blog-mapping-2026-04-18.md)
- Public project: [GEOFlow](https://github.com/yaojingang/GEOFlow)
