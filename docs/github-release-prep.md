# Yao GEO Skills GitHub 发布准备清单

本文档记录 `skills/` 目录下 GEO 相关 skill 的当前盘点、发布前阻塞项，以及面向 GitHub 用户需要补齐的说明体系。

## 当前盘点

- `skills/` 下共有 `21` 个 GEO 相关目录。
- `registry/skills.json` 中登记 `21` 个 skill，目录与 registry ID 一一对应。
- `21` 个目录均包含 `SKILL.md`，可按 skill 包继续核验。
- 当前仓库结构校验已通过。

按类型统计：

| 类型 | 数量 | Skill |
|---|---:|---|
| `geo-operations` | 3 | `yao-geoflow-cli`, `yao-geoflow-template`, `yao-geoflow-design` |
| `geo-strategy` | 2 | `yao-geo-panorama-audit`, `yao-geo-execution-roadmap` |
| `geo-page-technical` | 2 | `yao-geo-page-audit`, `yao-geo-page-blueprint` |
| `geo-content-production` | 6 | `yao-geo-title-optimizer`, `yao-geo-explainer-builder`, `yao-geo-comparison-builder`, `yao-geo-content-refiner`, `yao-geo-article-friendly`, `yao-geo-ranking-article-builder` |
| `geo-knowledge-assets` | 2 | `yao-geo-brand-graph`, `yao-geo-knowledge-base-builder` |
| `geo-measurement` | 5 | `yao-geo-tracking`, `yao-geo-effect-monitor`, `yao-deepseek-crawler`, `yao-doubao-crawler`, `yao-chatgpt-crawler` |
| `geo-research` | 1 | `yao-geo-intent-miner` |

按状态统计：

| 维度 | 统计 |
|---|---|
| 发布阶段 | `published: 20`, `incubating: 1` |
| 成熟度 | `stable: 1`, `beta: 18`, `draft: 1`, `scaffold: 1` |
| 需要联网 | `true: 15`, `false: 6` |

## 现有待梳理项

当前运行仓库校验：

```bash
python3 scripts/validate_repository.py
```

当前结果：

```text
Repository validation passed.
```

发布前建议继续保持：

| 优先级 | 项目 | 处理建议 |
|---|---|---|
| P1 | 本地检查产物 | `.gitignore` 已覆盖 `.DS_Store`、`tmp/`、`outputs/` 等路径；提交前继续确认它们没有进入 Git |

## 每个 Skill 的说明页结构

为了让 GitHub 用户快速理解每个 skill，建议每个 `docs/skills/<skill-id>.md` 保持同一结构：

1. 一句话定位：这个 skill 解决什么 GEO 工作。
2. 适用场景：用户什么时候该调用。
3. 不适用场景：和相邻 skill 的边界。
4. 必要输入：最少输入和增强输入。
5. 输出内容：默认交付件、结构化数据、报告格式。
6. 执行流程：按 5 到 10 个步骤说明。
7. 质量门：事实、证据、排版、合规、平台适配。
8. 示例入口：公开 demo 的 Markdown、HTML、Word、PDF、`report_input.json`。
9. 相关 skill：上游、下游和可替代 skill。

## GitHub 对外展示建议

README 应解决快速理解，`index.html` 应解决浏览和筛选。

README 建议保留这些模块：

- 仓库定位：说明这里的 GEO 是 `Generative Engine Optimization`，不是地图地理。
- 快速开始：安装、复制单个 skill、如何触发。
- Skill 总览：按 `strategy / page / content / knowledge / measurement / operations / research` 分组。
- 发布质量：结构校验、eval、公开案例、开源安全。
- 贡献规则：新增 skill 的目录结构、命名、registry 更新、文档更新。

HTML 导航页建议承担这些信息：

- 搜索和分类筛选。
- 每个 skill 的一句话用途、适用时机、主要输出。
- 直接链接到 `SKILL.md`、说明页、示例目录。
- 展示当前发布状态和成熟度。
- 单独标注 incubating 或 draft 项，避免用户误以为所有包都是稳定能力。

## 发布前检查

推荐按这个顺序做：

1. 补齐 P0/P1 缺口。
2. 清理 `.DS_Store`、`tmp/`、本地截图缓存和不应开源的测试中间产物。
3. 检查公开示例是否去除了客户隐私、内部域名、token、账号、报价敏感信息。
4. 对每个 skill 跑结构校验，至少确认 `SKILL.md`、`templates/`、`evals/`、`examples/` 可读。
5. 跑仓库校验：

```bash
python3 scripts/validate_repository.py
```

6. 检查 registry：

```bash
python3 -m json.tool registry/skills.json >/dev/null
```

7. 检查 Git 状态，只提交必要文件：

```bash
git status --short
```

8. 在浏览器打开 `index.html`，确认移动端和桌面端排版、筛选、链接都可用。

## 本次新增导航页

新增根目录：

```text
index.html
```

它是一个独立静态页，参考 `kami` 的暖纸面、油墨蓝、serif 层级和编辑式留白，但内容组织更偏 GitHub skill catalog。可直接本地打开，也可通过 GitHub Pages 发布。
