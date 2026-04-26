# Yao GEO Skills 更新日志

该文档记录公开 skill 仓库的发布更新。后续每次向 GitHub 推送新 skill 或调整仓库入口时，同步更新本文件和英文版 `CHANGELOG.en.md`。

## 2026-04-26

### `yao-geoflow-cli` Laravel API v1 / Docker 适配收尾

- 新增 `references/laravel-api-v1-docker.md`，明确 Laravel `/api/v1` fallback、Docker 部署检查、API scope 和 Token 使用规则
- 强化 `geoflow_preflight.sh`：
  - 缺少 CLI 时给出 Docker Compose 检查提示
  - 校验 `/api/v1/catalog` 是否返回 JSON
  - 对 `<!doctype html>` 这类 HTML 响应给出明确的 base URL / proxy / route 诊断
- 更新 CLI 文档，避免把非 JSON 响应误判为 AI 模型响应格式错误

### `yao-geoflow-design` Laravel Blade 主题契约补强

- 补充当前 GEOFlow Laravel Blade 主题目录、fallback 规则与 `active_theme` 约束
- 明确主题编辑不得硬编码 `/geo_admin`，不得修改后台路由、控制器、数据库查询或独立语言逻辑
- 补充文章详情页图片 caption、Markdown HTML 渲染、SEO/schema、footer 与语言行为的固定契约
- 更新中英文说明页，方便后续基于重构后的 GEOFlow 系统继续迭代模板能力

## 2026-04-20

### `geoflow-template` 更名为 `yao-geoflow-template`

- 将 skill 包目录调整为 `skills/yao-geoflow-template`
- 将中文与英文说明页调整为：
  - `docs/skills/yao-geoflow-template.md`
  - `docs/skills/yao-geoflow-template.en.md`
- 同步更新仓库首页、`registry/skills.json` 和对外导航入口
- 本次更名不改变 skill 的职责边界，仍然保持 GEOFlow 前台模板映射与 preview-first 产物输出

### `yao-geoflow-design` 首次发布

- 新增 `skills/yao-geoflow-design`
- 在 `yao-geoflow-template` 基础上扩展为更宽的 GEOFlow 前台设计能力：
  - 支持参考站点到 GEOFlow 模块的模板复刻
  - 支持当前模板的审计、优化、局部调整与 hybrid 迭代
  - 支持 preview-first 的主题包与优化包输出
- 新增中文与英文说明文档：
  - `docs/skills/yao-geoflow-design.md`
  - `docs/skills/yao-geoflow-design.en.md`
- 更新仓库首页和 `registry/skills.json`，把 `yao-geoflow-design` 加入公开导航

## 2026-04-18

### `geoflow-template` 首次发布（当前名称：`yao-geoflow-template`）

- 首次发布时新增 `skills/geoflow-template`，当前公开目录已更名为 `skills/yao-geoflow-template`
- 新增前台模板复刻与主题包规划能力：
  - 面向 GEOFlow 前台模块、变量和函数契约
  - 支持把参考网址映射为 GEOFlow 兼容的主题包方案
  - 支持 preview-first 的 `tokens.json / mapping.json / manifest.json` 输出方向
- 新增中文与英文说明文档：
  - `docs/skills/yao-geoflow-template.md`
  - `docs/skills/yao-geoflow-template.en.md`
- 更新仓库首页和 `registry/skills.json`，把该 skill 加入公开导航
