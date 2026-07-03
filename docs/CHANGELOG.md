# Yao GEO Skills 更新日志

该文档记录公开 skill 仓库的发布更新。后续每次向 GitHub 推送新 skill 或调整仓库入口时，同步更新本文件和英文版 `CHANGELOG.en.md`。

## 2026-07-03

### `yao-doubao-crawler` 首次发布

- 新增监测归因类 skill：`skills/yao-doubao-crawler`。
- 支持豆包网页端 OpenCLI 采样，以及 Android Studio AVD + Appium UiAutomator2 的豆包手机 App 可见 UI 采集。
- 输出 `yao-doubao-crawler/v1` 兼容 JSON、结构化 Markdown、Excel、Kami 风格 HTML 报告，以及移动端截图/XML 和搜索资料引用证据。
- 新增 `fresh-chat` 独立会话采集、移动端引用资料已引用/未引用标记、引用次数和 `mobile_evidence` 汇总。
- 更新 `registry/skills.json`、仓库首页、英文 README、可视化导航页和说明页：`docs/skills/yao-doubao-crawler.md`。

## 2026-05-21

### GEO skill 批量能力同步

- 同步本地 13 个 GEO skill 的最新迭代：`yao-geo-effect-monitor`、`yao-geo-panorama-audit`、`yao-geo-page-audit`、`yao-geo-page-blueprint`、`yao-geo-title-optimizer`、`yao-geo-explainer-builder`、`yao-geo-knowledge-base-builder`、`yao-geo-intent-miner`、`yao-geo-execution-roadmap`、`yao-geo-brand-graph`、`yao-geo-comparison-builder`、`yao-geo-content-refiner`、`yao-geo-ranking-article-builder`。
- 统一补强真实数据能力：区分公开网页、用户提供资料、授权数据、平台采样、无法访问资料，并在报告中保留来源新鲜度、证据等级和待补缺口。
- 统一补强四格式交付：多数组件报告现在围绕 Markdown、HTML、Word、PDF 同源输出，HTML 长报告默认包含下拉时固定跟随的目录菜单。
- 更新 `registry/skills.json`、仓库首页、英文 README、可视化导航页和对应 `docs/skills/*.md` 说明，确保 GitHub 用户能看到最新用途、输出和质量门。

## 2026-05-19

### `yao-geo-explainer-builder` 首次发布

- 新增内容生产类 skill：`skills/yao-geo-explainer-builder`。
- 用于生成 GEO 科普文章、How-to 教程、概念解释、怎么选、避坑指南、FAQ、术语表和品牌自然植入建议。
- 基于 GEO、RAG、长上下文位置偏差和 CoT 推理结构研究，新增研究依据模块、来源账本和可截取信息单元规则。
- 示例已真实生成 Markdown、HTML、Word、PDF 四个文件，并通过自动质量报告检查四格式存在性、品牌出现上限、来源账本、研究依据和 Word 表格结构。
- 更新 `registry/skills.json`、仓库首页、英文首页和说明页：`docs/skills/yao-geo-explainer-builder.md`。

### `yao-geo-page-audit` 首次发布

- 新增页面技术类 skill：`skills/yao-geo-page-audit`。
- 用于输入网址后诊断首页、代表性一级页和二级页的可抓取性、结构规范性、内容信号和 AI 可抽取性。
- 内置标准输入简报、研究依据、页面诊断方法、白底四件套排版规范、质量门和公开合成样例。
- 示例已真实生成 Markdown、HTML、Word、PDF 四个文件，并加入链接存在性自检要求。
- 更新 `registry/skills.json`、仓库首页、英文首页和说明页：`docs/skills/yao-geo-page-audit.md`。

### `yao-geo-ranking-article-builder` 研究增强与示例修复

- 新增内容生产类 skill：`skills/yao-geo-ranking-article-builder`。
- 补齐 Markdown、HTML、Word、PDF 四个真实示例报告，并生成可打开的 `index.html`。
- 基于 GEO、RAG、Generative Relevance Feedback、AutoGEO 和 AgenticGEO 研究，新增 EICAS 底层框架。
- 修复示例报告排版链路：HTML/PDF 使用自定义白底模板，Word 自动补写显式表格边框。

### `yao-geo-effect-monitor` 首次发布

- 新增监测闭环类 skill：`skills/yao-geo-effect-monitor`。
- 用于设计 GEO Signal Monitor，面向 DeepSeek、豆包、千问、Kimi、元宝建立 AI 答案监测、引用追踪、品牌事实纠偏、月报告警和谨慎归因闭环。
- 内置标准输入简报、五平台采样口径、指标与归因框架、纠偏任务模型、仪表盘字段、数据库表结构、API 草案和四格式示例报告。
- 基于 GEO、生成式搜索可验证性、生成式相关反馈、AgenticGEO、citation failure diagnosis 和 causal impact 研究，补强引用召回/准确、黑盒波动、多样化 Prompt 和谨慎归因标准。
- 示例报告已按同一 Markdown 源重新生成 Markdown、HTML、Word、PDF，并加入四格式真实存在和可抽取校验。
- 更新 `registry/skills.json`、仓库首页和说明页：`docs/skills/yao-geo-effect-monitor.md`。

### `yao-geo-brand-graph` 首次发布

- 新增知识资产类 skill：`skills/yao-geo-brand-graph`。
- 用于把企业信息转成品牌、产品、人物、地点、案例、证据和场景之间的可审计实体关系图。
- 内置实体/关系结构规范、证据与隐私策略、消歧流程、Mermaid、JSON-LD、RDF 三元组、白底四格式报告版式和渲染脚本。
- 新增合成示例，可从同一份 `report_input.json` 生成 Markdown、HTML、Word、PDF 和 `quality-report.json`。

### `yao-geo-intent-miner` 研究增强与示例修复

- 新增研究型 skill：`skills/yao-geo-intent-miner`。
- 补齐 Markdown、HTML、Word、PDF 四个真实示例报告，并增加 `quality-report.json`。
- 基于搜索意图分类、LLM 查询扩展、HyDE、对话式查询重写、TREC CAsT、BEIR/MS MARCO 迭代底层方法。
- 新增五段式查询重写、证据可得性约束、对话链路回放字段和四格式质量门。

### `yao-geo-panorama-audit` 首次发布

- 新增战略诊断类 skill：`skills/yao-geo-panorama-audit`。
- 用于建立品牌 GEO 基线，面向 DeepSeek、豆包、千问、Kimi、元宝诊断 AI 答案可见性、竞品差距、内容页面缺口和外部信源。
- 内置标准输入简报、国内平台采样字段、GEO 八维质量模型、质量门、白底四格式报告版式规范和合成示例。
- 更新 `registry/skills.json`、仓库首页、英文首页和说明页：`docs/skills/yao-geo-panorama-audit.md`。

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
