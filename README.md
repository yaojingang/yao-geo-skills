# Yao GEO Skills

面向 `GEO`（`Generative Engine Optimization`）内容、研究、追踪与工作流的 Skill 开源合集。

`GEO` in this repository means `Generative Engine Optimization`, not geospatial tooling.

This repository publishes reusable GEO skill packages with stable contracts, clear boundaries, public examples, and repeatable evaluation. It is not a prompt dump. It is a maintained library of GEO-oriented execution assets.

## 仓库定位 / What This Repository Is For

### 中文

这个仓库用于沉淀可以复用的 GEO Skill，覆盖：

- GEO 研究与证据收集
- GEO 内容优化与结构化输出
- GEO 后端效果追踪与归因方案
- GEO 工作流中的共享模板、schema 和 rubric

这里的重点不是“多放几个 prompt”，而是把可以长期复用、能公开分享、能被验证的 GEO 资产整理成标准化 skill 包。

### English

This repository is for reusable GEO skills that support:

- GEO research and evidence gathering
- GEO content optimization and structured outputs
- GEO backend tracking and attribution planning
- shared templates, schemas, and rubrics for GEO workflows

The goal is not to collect loose prompts. The goal is to publish reliable GEO assets that teams can understand, reuse, and extend.

## 快速导航 / Quick Navigation

- Skills directory: [`skills/`](skills)
- Skill guides: [`docs/skills/`](docs/skills)
- Repository policies: [`docs/`](docs)
- Inventory registry: [`registry/skills.json`](registry/skills.json)
- Shared schemas and templates: [`shared/`](shared)
- Repository validation script: [`scripts/validate_repository.py`](scripts/validate_repository.py)

## Skills Navigation

| Skill | 中文说明 | English Summary | Status | Docs | Package |
|---|---|---|---|---|---|
| `geoflow-cli-ops` | 通过本地 `geoflow` CLI 操作已有 GEOFlow 系统，用于 catalog 查询、任务管理、文章上传、审核和发布。 | Operates an existing GEOFlow system through the local CLI for catalog lookup, task operations, and article publish flows. | `active / stable` | [Guide](docs/skills/geoflow-cli-ops.md) | [skills/geoflow-cli-ops](skills/geoflow-cli-ops) |
| `geo-tracking-plan` | 从公司名和辅助信息出发，基于官网权威检索生成 GEO 后端效果追踪方案，区分国内 / 海外 / 混合 GEO。 | Generates a company-specific GEO backend tracking plan using official-site-first retrieval and China-vs-overseas measurement logic. | `active / beta` | [Guide](docs/skills/geo-tracking-plan.md) | [skills/geo-tracking-plan](skills/geo-tracking-plan) |

## Featured Skills

### `geoflow-cli-ops`

如果你的系统里已经有 GEOFlow，而你希望通过 CLI 做 catalog 查询、任务编排、文章上传、审核和发布，这个 skill 就是面向“系统操作”而不是“策略生成”的。它和 `geo-tracking-plan` 的关系很清楚：前者偏执行，后者偏方案。

Use it when the system already exists and the job is operational. It is a local-control skill, not a planning or research skill.

- Skill guide: [docs/skills/geoflow-cli-ops.md](docs/skills/geoflow-cli-ops.md)
- Package: [skills/geoflow-cli-ops](skills/geoflow-cli-ops)
- Public project: [GEOFlow](https://github.com/yaojingang/GEOFlow)

### `geo-tracking-plan`

用于输入公司名称和少量辅助信息后，自动完成官网优先的权威检索、业务特征识别、市场分层判断，并输出直接效果与间接效果并行的 GEO 追踪方案。它适合开源使用，因为不依赖飞书、私有 CLI、内网地址或未授权资料。

Use it when you need an official-site-centered GEO tracking plan rather than generic GEO theory. The skill is especially useful when you need to explain why China GEO often needs promo codes, surveys, consultant entry points, or manual source recovery, while overseas GEO can rely more on official web properties, form fields, and upgrade funnels.

- Skill guide: [docs/skills/geo-tracking-plan.md](docs/skills/geo-tracking-plan.md)
- Demo input: [skills/geo-tracking-plan/examples/hubspot-demo/report_input.json](skills/geo-tracking-plan/examples/hubspot-demo/report_input.json)
- Demo HTML: [skills/geo-tracking-plan/examples/hubspot-demo/hubspot-geo-tracking-plan.html](skills/geo-tracking-plan/examples/hubspot-demo/hubspot-geo-tracking-plan.html)
- Demo DOCX: [skills/geo-tracking-plan/examples/hubspot-demo/hubspot-geo-tracking-plan.docx](skills/geo-tracking-plan/examples/hubspot-demo/hubspot-geo-tracking-plan.docx)
- Case screenshot: [hubspot-geo-tracking-plan.png](skills/geo-tracking-plan/assets/screenshots/hubspot-geo-tracking-plan.png)

## 下载方式 / Download Options

### 1. 下载整个仓库 / Download The Whole Repository

#### Git clone

```bash
git clone https://github.com/yaojingang/yao-geo-skills.git
cd yao-geo-skills
```

#### GitHub ZIP

On GitHub, open the repository page and use:

`Code` -> `Download ZIP`

### 2. 只拉取某个 skill / Download A Single Skill

#### Sparse checkout

```bash
git clone --filter=blob:none --no-checkout https://github.com/yaojingang/yao-geo-skills.git
cd yao-geo-skills
git sparse-checkout init --cone
git sparse-checkout set skills/geo-tracking-plan docs/skills/geo-tracking-plan.md
git checkout main
```

#### Manual download

Open the skill folder on GitHub and download the files manually:

- [skills/geo-tracking-plan](skills/geo-tracking-plan)

## Repository Docs

- [Repository Design](docs/repository-design.md)
- [Input And Output Contract](docs/input-output-contract.md)
- [Naming Conventions](docs/naming-conventions.md)
- [Eval Policy](docs/eval-policy.md)
- [Publishing Rules](docs/publishing-rules.md)

## Skill Families

- `geo-operations`
- `geo-measurement`
- `geo-keyword-discovery`
- `geo-competitor-scan`
- `geo-answer-optimizer`
- `geo-brand-fact-sheet`
- `geo-content-audit`
## Repository Layout

```text
yao-geo-skills/
├── README.md
├── LICENSE
├── .github/
├── docs/
│   └── skills/
├── registry/
├── scripts/
├── shared/
└── skills/
```

## Design Principles

- One skill, one job
- Keep `skills/` flat until there is strong evidence for another navigation layer
- Official-source verification for factual GEO work
- Structured input over hidden prompt assumptions
- Human-readable and machine-checkable outputs
- Public sanitized examples over real private run outputs
- Evaluation is required, not optional

## Contribution And Push Flow

1. Add or update a skill package under `skills/<skill-id>/`.
2. Add or update the matching guide under `docs/skills/`.
3. Register the skill in [`registry/skills.json`](registry/skills.json).
4. Run repository validation:

```bash
python3 scripts/validate_repository.py
```

5. Review the diff carefully.
6. Commit with a short scope-first message.
7. Push to GitHub and open a PR for non-trivial changes.

The detailed GitHub workflow lives in [docs/publishing-rules.md](docs/publishing-rules.md).
