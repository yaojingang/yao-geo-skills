# Yao GEO Skills 更新日志

该文档记录公开 skill 仓库的发布更新。后续每次向 GitHub 推送新 skill 或调整仓库入口时，同步更新本文件和英文版 `CHANGELOG.en.md`。

## 2026-04-20

### `yao-geoflow-design` 首次发布

- 新增 `skills/yao-geoflow-design`
- 在 `geoflow-template` 基础上扩展为更宽的 GEOFlow 前台设计能力：
  - 支持参考站点到 GEOFlow 模块的模板复刻
  - 支持当前模板的审计、优化、局部调整与 hybrid 迭代
  - 支持 preview-first 的主题包与优化包输出
- 新增中文与英文说明文档：
  - `docs/skills/yao-geoflow-design.md`
  - `docs/skills/yao-geoflow-design.en.md`
- 更新仓库首页和 `registry/skills.json`，把 `yao-geoflow-design` 加入公开导航

## 2026-04-18

### geoflow-template 首次发布

- 新增 `skills/geoflow-template`
- 新增前台模板复刻与主题包规划能力：
  - 面向 GEOFlow 前台模块、变量和函数契约
  - 支持把参考网址映射为 GEOFlow 兼容的主题包方案
  - 支持 preview-first 的 `tokens.json / mapping.json / manifest.json` 输出方向
- 新增中文与英文说明文档：
  - `docs/skills/geoflow-template.md`
  - `docs/skills/geoflow-template.en.md`
- 更新仓库首页和 `registry/skills.json`，把 `geoflow-template` 加入公开导航
