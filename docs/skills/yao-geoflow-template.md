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

## Package Links

- Skill package: [skills/yao-geoflow-template](../../skills/yao-geoflow-template)
- Trigger boundary: [trigger_cases.json](../../skills/yao-geoflow-template/evals/trigger_cases.json)
- Frontend map: [geoflow-frontend-map.md](../../skills/yao-geoflow-template/references/geoflow-frontend-map.md)
- Theme contract: [theme-package-contract.md](../../skills/yao-geoflow-template/references/theme-package-contract.md)
- Example mapping report: [qiaomu-blog-mapping-2026-04-18.md](../../skills/yao-geoflow-template/reports/qiaomu-blog-mapping-2026-04-18.md)
- Public project: [GEOFlow](https://github.com/yaojingang/GEOFlow)
