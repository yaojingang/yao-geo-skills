# yao-geoflow-cli

`yao-geoflow-cli` is a local operations skill for running an existing GEOFlow system through the project CLI. It is different from the GEO planning skills in this repository: it executes operational actions instead of generating research or strategy deliverables.

## 中文概述

`yao-geoflow-cli` 适用于已经部署好的 GEOFlow 系统。它通过本地 `geoflow` CLI 来完成登录、目录查询、任务管理、作业检查、文章上传、审核和发布，而不是进入 Web 后台手动操作。

当前 GEOFlow 重构版如果还没有 `bin/geoflow` 包装器，本 skill 会走 Laravel `/api/v1` fallback。Docker 部署时，需要先确认 Web 根地址、API Token 和容器服务状态，而不是直接读写数据库。

适合：

- 查 catalog ID
- 创建、启动、停止、入队任务
- 上传文章草稿
- 审核并发布文章
- 检查 job 是否失败
- 诊断 `/api/v1` 返回 HTML、代理错误或登录页导致的“非 JSON 响应”

不适合：

- 改 GEOFlow 后端代码
- 改数据库结构
- 绕开 CLI 直接写数据库

## English Overview

Use `yao-geoflow-cli` when a GEOFlow system already exists and the job is to operate it from the local CLI rather than from the admin UI.

For the current Laravel rewrite, this skill can fall back to `/api/v1` when `bin/geoflow` is not available. In Docker deployments, preflight must verify the exposed web root, API token, and container health before any write operation.

Best for:

- catalog lookup
- task lifecycle operations
- job inspection
- article draft upload
- article review and publish
- diagnosing non-JSON `/api/v1` responses caused by wrong base URLs, proxy pages, or Docker routing problems

Not for:

- backend implementation
- schema changes
- direct database writes

## Package Links

- Skill package: [skills/yao-geoflow-cli](../../skills/yao-geoflow-cli)
- Trigger boundary: [trigger_cases.json](../../skills/yao-geoflow-cli/evals/trigger_cases.json)
- CLI preflight: [geoflow_preflight.sh](../../skills/yao-geoflow-cli/scripts/geoflow_preflight.sh)
- Laravel API v1 / Docker fallback: [laravel-api-v1-docker.md](../../skills/yao-geoflow-cli/references/laravel-api-v1-docker.md)
- Public project: [GEOFlow](https://github.com/yaojingang/GEOFlow)
