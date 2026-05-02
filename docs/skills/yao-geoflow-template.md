# Yao GEOFlow Template

`yao-geoflow-template` 用来把一个参考网址的前台视觉风格，映射成 **GEOFlow 兼容的主题包方案**。它不直接替换生产前台，而是先输出 `tokens.json`、`mapping.json`、`manifest.json` 和 preview-first 的模板包结构。

## 中文概述

适合：

- 梳理 GEOFlow 当前前台的模块和变量契约
- 输入一个参考网址，抽取主色调、卡片风格、版式层级和模块结构
- 把参考站点风格映射到 GEOFlow 的首页、分类页、文章详情页、归档页和广告位
- 为系统后续的模板预览、模板启用和模板二次编辑提供基础包结构

不适合：

- 直接复制任意站点的整页 HTML
- 跳过 GEOFlow 当前函数和数据契约，直接写死内容
- 不经过 preview 直接覆盖正式前台
- 顺手去改后台业务逻辑、SEO 契约、路由或文章查询规则

## English Overview

Use `yao-geoflow-template` when the job is to turn a reference frontend into a **GEOFlow-compatible theme package plan**.

Best for:

- inventorying GEOFlow frontend modules, variables, and rendering boundaries
- extracting visual tokens and layout direction from a reference URL
- mapping that style onto GEOFlow homepage, category, article, archive, and ad-slot modules
- preparing preview-first theme packages for later preview, activation, and iteration

Not for:

- raw page copying
- hard-coded HTML that bypasses GEOFlow data contracts
- direct production replacement without preview
- backend refactors, SEO contract changes, or route rewrites

## 标准化主题包合同

公开提交的示例必须在 fresh checkout 后也能被审阅，不依赖本地运行时
`outputs/` 或 `outputs-demo/` 目录。最低标准结构为：

- `examples/<example-id>/README.md`
- `preview/<example-id>/package/tokens.json`
- `preview/<example-id>/package/mapping.json`
- `preview/<example-id>/index.html`
- `preview/<example-id>/category.html`
- `preview/<example-id>/article.html`
- `preview/<example-id>/archive.html`

`tokens.json` 记录主题包身份、参考来源、创建日期、兼容系统、视觉方向和
token 分组。`mapping.json` 记录路由覆盖、模块映射、安全边界和已提交的
preview 路由。

审阅时至少确认：

- package metadata 已提交并且是可解析 JSON
- preview 文件不依赖 ignored `outputs/` 或 `outputs-demo/` 路径
- 未覆盖的路由或模块被显式记录
- preview readiness 与 production activation readiness 分开

## Preview readiness 与 production activation readiness

`preview-only` 表示这个主题包已经可以通过已提交的 metadata 和 preview
routes 进行审阅。它不表示可以直接承接线上流量，也不表示 routing、SEO、
backend query 或 production template selection 已经获得批准。

production activation 必须由 GEOFlow 项目另行发起 activation request、
Spec Kit spec 或 implementation plan。除非这个 activation workflow 已经可追踪、
可审阅，`yao-geoflow-template` 不应把 `activation_status` 提升到
`activation-candidate` 或 `activated`。

以下 activation 工作不属于 `yao-geoflow-template` 的 preview package 输出范围：

- live route 或 URL rewrite
- SEO contract、canonical、sitemap 或 structured-data 变更
- backend schema、content-query 或 data-fetching 变更
- deployment state、rollout flags、cache purge 或 production template switch

## Package Links

- Skill package: [skills/yao-geoflow-template](../../skills/yao-geoflow-template)
- Trigger boundary: [trigger_cases.json](../../skills/yao-geoflow-template/evals/trigger_cases.json)
- Frontend map: [geoflow-frontend-map.md](../../skills/yao-geoflow-template/references/geoflow-frontend-map.md)
- Theme contract: [theme-package-contract.md](../../skills/yao-geoflow-template/references/theme-package-contract.md)
- Example mapping report: [qiaomu-blog-mapping-2026-04-18.md](../../skills/yao-geoflow-template/reports/qiaomu-blog-mapping-2026-04-18.md)
- Public project: [GEOFlow](https://github.com/yaojingang/GEOFlow)
