# yao-geoflow-design

`yao-geoflow-design` 用来识别当前 GEOFlow 系统里已有的模板，指定一个目标主题进入 **preview-first 的编辑会话**，并对这个主题做样式调整、模块增减和参考站风格映射。它不直接替换生产前台，而是先在当前 GEOFlow 系统里形成可预览的主题分支，确认后再决定替换原主题还是新增一个模板。

## 中文概述

适合：

- 识别当前 GEOFlow 系统里都有哪些主题和可编辑文件
- 指定一个现有主题，先 fork 出预览态模板再做 AI 调整
- 梳理 GEOFlow 当前前台的模块和变量契约
- 输入一个参考网址，抽取主色调、卡片风格、版式层级和模块结构
- 把参考站点风格映射到 GEOFlow 的首页、分类页、文章详情页、归档页和广告位
- 对当前模板做层级、间距、卡片一致性、响应式和广告位语气的优化
- 在现有数据契约允许的前提下，增加新的展示模块或信息块
- 输出 `theme-discovery.json`、`edit-session.json`、`design-audit.md`、`tokens.delta.json`、`mapping.delta.json`、`change-plan.md` 等产物
- 为系统后续的模板预览、模板启用、替换原模板和新增模板提供基础工作流

不适合：

- 直接复制任意站点的整页 HTML
- 跳过 GEOFlow 当前函数和数据契约，直接写死内容
- 不经过 preview 直接覆盖正式前台
- 顺手去改后台业务逻辑、SEO 契约、路由或文章查询规则

## English Overview

Use `yao-geoflow-design` when the job is to turn a reference frontend into a **GEOFlow-compatible theme package plan** or to optimize the current GEOFlow template without breaking its contract.

Best for:

- discovering the themes that already exist in the current GEOFlow system
- selecting a target theme and forking a preview edit session before any live change
- inventorying GEOFlow frontend modules, variables, and rendering boundaries
- extracting visual tokens and layout direction from a reference URL
- mapping that style onto GEOFlow homepage, category, article, archive, and ad-slot modules
- auditing the current template for design debt and incremental improvement opportunities
- adjusting layout width, typography weight, hierarchy, or modules inside a preview theme fork
- preparing preview-first theme packages or optimization patch packages for later publish-as-new or replace-base decisions

Not for:

- raw page copying
- hard-coded HTML that bypasses GEOFlow data contracts
- direct production replacement without preview
- backend refactors, SEO contract changes, or route rewrites

## Package Links

- Skill package: [skills/yao-geoflow-design](../../skills/yao-geoflow-design)
- Trigger boundary: [trigger_cases.json](../../skills/yao-geoflow-design/evals/trigger_cases.json)
- Frontend map: [geoflow-frontend-map.md](../../skills/yao-geoflow-design/references/geoflow-frontend-map.md)
- Theme contract: [theme-package-contract.md](../../skills/yao-geoflow-design/references/theme-package-contract.md)
- Optimization playbook: [design-optimization-playbook.md](../../skills/yao-geoflow-design/references/design-optimization-playbook.md)
- Theme edit workflow: [theme-edit-workflow.md](../../skills/yao-geoflow-design/references/theme-edit-workflow.md)
- Example mapping report: [qiaomu-blog-mapping-2026-04-18.md](../../skills/yao-geoflow-design/reports/qiaomu-blog-mapping-2026-04-18.md)
- Public project: [GEOFlow](https://github.com/yaojingang/GEOFlow)
