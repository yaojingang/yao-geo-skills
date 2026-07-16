# yao-geoflow-design

`yao-geoflow-design` 是当前 GEOFlow 前端体验的主 skill。它负责识别 Laravel Blade 主题、规划默认站首页模块、设计 `homepage-design.json`、处理已有 `lead_form` 的转化模块、拆解参考站、比较默认站和渠道目标包的 frontend capabilities，并把预览、导入、同步和发布拆成独立确认步骤。

当前版本已对 GEOFlow Laravel Blade 主题系统、首页 builder、在线主题编辑器和渠道前端能力同步做适配：主题目录为 `resources/views/theme/{theme_id}`，运行时资源通常在 `public/themes/{theme_id}`，缺失模板会回退到 `resources/views/site`；当系统暴露 `HomepageModuleBuilder`、`homepage_modules`、`homepage_style` 和后台导入路由时，可以输出可审核的 `homepage-design.json`。后台地址可自定义，设计 skill 不应硬编码 `/geo_admin` 或改动后端业务逻辑。

## 中文概述

适合：

- 识别当前 GEOFlow 系统里都有哪些主题和可编辑文件
- 指定一个现有主题，先 fork 出预览态模板再做 AI 调整
- 梳理 GEOFlow 当前前台的模块和变量契约
- 输入一个参考网址，抽取主色调、卡片风格、版式层级和模块结构
- 把参考站点风格映射到 GEOFlow 的首页、分类页、文章详情页、归档页和广告位
- 对当前模板做层级、间距、卡片一致性、响应式和广告位语气的优化
- 把默认首页从基础文章列表升级为企业官网、内容门户或知识中心式首页
- 基于 `homepageCarouselSlides`、`hotArticles`、`featuredArticles`、`articles`、`cardSummaries` 和站点文案增加大图、指标、CSS 图表、文本、服务/分类、案例/资源、CTA 等模块
- 基于 `homepage_modules` 和 `homepage_style` 生成可导入后台的首页设计 JSON，包括 `hero`、`rich_text`、`image_band`、`metric_band`、`chart_band`、`feature_grid`、`article_collection`、`cta_band`、`lead_form` 和安全的 `custom_html`
- 使用已存在且 active 的 `lead_form_slug` 绑定转化表单；本 skill 不创建 lead form
- 比较默认站支持模块和 GeoFlow Agent target package 支持模块，目标包不支持 `lead_form` 时改成 CTA/link 或提示先升级目标包
- 生成渠道前端能力差异、同步预览和降级策略
- 检查文章详情页图片、Markdown 渲染、SEO/schema、footer 和语言行为是否仍遵循系统契约
- 在现有数据契约允许的前提下，增加新的展示模块或信息块
- 输出 `theme-discovery.json`、`edit-session.json`、`design-audit.md`、`homepage-composition-plan.md`、`homepage-design.json`、`tokens.delta.json`、`mapping.delta.json`、`change-plan.md` 等产物
- 为系统后续的模板预览、模板启用、替换原模板和新增模板提供基础工作流

不适合：

- 直接复制任意站点的整页 HTML
- 跳过 GEOFlow 当前函数和数据契约，直接写死内容
- 实现 lead form 后端 CRUD、数据库迁移、API endpoint 或提交处理
- 在没有后端字段的情况下伪造客户 Logo、销售漏斗、真实图表或企业背书数据
- 未经确认直接导入 `homepage_modules` 或直接套用首页 preset 到线上
- 把 `lead_form` 静默塞进不支持该模块的 target package payload
- 不经过 preview 直接覆盖正式前台
- 顺手去改后台业务逻辑、SEO 契约、路由或文章查询规则
- 在主题里硬编码后台地址、数据库查询或独立语言切换逻辑

## English Overview

Use `yao-geoflow-design` as the primary frontend-experience skill for current GEOFlow systems: default-site homepage design, Laravel Blade themes, reference-site mapping, lead-form conversion modules, channel frontend-capability audits, and sync-preview planning.

Best for:

- discovering the themes that already exist in the current GEOFlow system
- selecting a target theme and forking a preview edit session before any live change
- inventorying GEOFlow frontend modules, variables, and rendering boundaries
- extracting visual tokens and layout direction from a reference URL
- mapping that style onto GEOFlow homepage, category, article, archive, and ad-slot modules
- auditing the current template for design debt and incremental improvement opportunities
- adjusting layout width, typography weight, hierarchy, or modules inside a preview theme fork
- enriching the default homepage into a corporate, portal, or knowledge-hub front page using existing GEOFlow homepage data
- generating reviewed homepage module/style JSON, including `lead_form` modules bound by an existing active `lead_form_slug`
- comparing default-site modules with target-package frontend capabilities before channel sync
- preparing preview-first theme packages or optimization patch packages for later publish-as-new or replace-base decisions

Not for:

- raw page copying
- hard-coded HTML that bypasses GEOFlow data contracts
- lead-form backend CRUD, migrations, API endpoint implementation, or submission handling
- invented corporate claims, customer logos, sales-funnel metrics, or chart data without backend support
- silently syncing unsupported `lead_form` modules into older target packages
- direct production replacement without preview
- backend refactors, SEO contract changes, or route rewrites

## Package Links

- Skill package: [skills/yao-geoflow-design](../../skills/yao-geoflow-design)
- Trigger boundary: [trigger_cases.json](../../skills/yao-geoflow-design/evals/trigger_cases.json)
- Frontend map: [geoflow-frontend-map.md](../../skills/yao-geoflow-design/references/geoflow-frontend-map.md)
- Theme contract: [theme-package-contract.md](../../skills/yao-geoflow-design/references/theme-package-contract.md)
- Laravel Blade contract: [laravel-theme-contract.md](../../skills/yao-geoflow-design/references/laravel-theme-contract.md)
- Homepage composition guide: [homepage-composition-guide.md](../../skills/yao-geoflow-design/references/homepage-composition-guide.md)
- Optimization playbook: [design-optimization-playbook.md](../../skills/yao-geoflow-design/references/design-optimization-playbook.md)
- Theme edit workflow: [theme-edit-workflow.md](../../skills/yao-geoflow-design/references/theme-edit-workflow.md)
- Channel frontend contract: [channel-frontend-contract.md](../../skills/yao-geoflow-design/references/channel-frontend-contract.md)
- Upgrade report: [geoflow-skill-upgrade-2026-07-05.md](../../skills/yao-geoflow-design/reports/geoflow-skill-upgrade-2026-07-05.md)
- Example mapping report: [qiaomu-blog-mapping-2026-04-18.md](../../skills/yao-geoflow-design/reports/qiaomu-blog-mapping-2026-04-18.md)
- Public project: [GEOFlow](https://github.com/yaojingang/GEOFlow)
