# yao-geoflow-cli

`yao-geoflow-cli` is an operations skill for running an existing GEOFlow 2.1+ system through supported CLI commands, Laravel API v1, or authenticated admin web flows. It executes operational actions instead of generating research or frontend design deliverables.

## 中文概述

`yao-geoflow-cli` 适用于已经部署好的 GEOFlow 2.1+ 系统。它优先通过受支持的本地 CLI 执行目录查询、任务管理、作业检查、文章上传、审核和发布；当 CLI 不覆盖目标能力时，再选择 Laravel `/api/v1` 或已登录后台流程。

当前能力还覆盖增长中心、企业知识库、URL 导入、分发渠道、前端能力刷新、同步预览和在线主题编辑等后台能力。新增增长中心和企业知识库能力优先走 Admin Web、artisan 和路由认知，不伪造不存在的 API v1 endpoint。

适合：

- 查 catalog ID
- 创建、启动、停止、入队任务
- 上传文章草稿
- 审核并发布文章
- 检查 job 是否失败
- 创建或管理线索表单、查看和导出 leads
- 上传企业知识库材料、生成草稿、刷新语义分块
- 刷新渠道前端能力并生成同步预览
- 打开主题 editor 的 draft/publish/discard 流程
- 诊断 `/api/v1` 返回 HTML、代理错误或登录页导致的“非 JSON 响应”

不适合：

- 改 GEOFlow 后端代码
- 改数据库结构
- 绕开 CLI 直接写数据库
- 设计首页模块或主题视觉，这类任务交给 `yao-geoflow-design`
- 绕过登录、CSRF、确认和备份计划执行高风险操作

## English Overview

Use `yao-geoflow-cli` when a GEOFlow system already exists and the job is to operate it through the safest supported surface: CLI first, API v1 for exposed content operations, then authenticated admin web flows for management capabilities that are not exposed as API v1 endpoints.

For Docker or production deployments, preflight must verify the exposed web root, API token, session, queue/runtime state, and backup/confirmation requirements before any write operation.

Best for:

- catalog lookup
- task lifecycle operations
- job inspection
- article draft upload
- article review and publish
- growth-center lead forms, leads, exports, and analytics entrypoints
- enterprise knowledge upload, draft, markdown edit, and semantic chunk refresh flows
- distribution, target package, frontend-capability refresh, and sync-preview operations
- diagnosing non-JSON `/api/v1` responses caused by wrong base URLs, proxy pages, or Docker routing problems

Not for:

- backend implementation
- schema changes
- direct database writes
- frontend design or homepage JSON planning

## Package Links

- Skill package: [skills/yao-geoflow-cli](../../skills/yao-geoflow-cli)
- Trigger boundary: [trigger_cases.json](../../skills/yao-geoflow-cli/evals/trigger_cases.json)
- CLI preflight: [geoflow_preflight.sh](../../skills/yao-geoflow-cli/scripts/geoflow_preflight.sh)
- Current capability map: [geoflow-current-capability-map.md](../../skills/yao-geoflow-cli/references/geoflow-current-capability-map.md)
- Laravel API v1 / Docker fallback: [laravel-api-v1-docker.md](../../skills/yao-geoflow-cli/references/laravel-api-v1-docker.md)
- Upgrade report: [geoflow-skill-upgrade-2026-07-05.md](../../skills/yao-geoflow-cli/reports/geoflow-skill-upgrade-2026-07-05.md)
- Public project: [GEOFlow](https://github.com/yaojingang/GEOFlow)
