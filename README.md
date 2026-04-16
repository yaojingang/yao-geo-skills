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

## Skill Catalog

The catalog is grouped by job family so visitors can tell whether a skill is meant for execution, measurement, or research before they open the package.

### `operations`

<table>
  <tr>
    <td valign="top" width="100%">
      <strong><code>geoflow-cli-ops</code></strong><br>
      中文：通过本地 <code>geoflow</code> CLI 操作已有 GEOFlow 系统，用于 catalog 查询、任务管理、文章上传、审核和发布。<br>
      English: Operates an existing GEOFlow system through the local CLI for catalog lookup, task operations, and article publish flows.<br><br>
      <strong>Best for</strong><br>
      Existing GEOFlow deployments, operator workflows, catalog lookup, task lifecycle actions, article review and publish.<br><br>
      <strong>Links</strong><br>
      <a href="docs/skills/geoflow-cli-ops.md">Guide</a> ·
      <a href="skills/geoflow-cli-ops">Package</a> ·
      <a href="https://github.com/yaojingang/GEOFlow">Public project</a>
    </td>
  </tr>
</table>

### `measurement`

<table>
  <tr>
    <td valign="top" width="100%">
      <strong><code>geo-tracking-plan</code></strong><br>
      中文：输入公司名称和辅助信息，基于官网与官方资产生成 GEO 后端效果追踪方案，并明确区分国内 / 海外 / 混合 GEO 的不同监测逻辑。<br>
      English: Generates a company-specific GEO backend tracking plan from a company name plus supporting context, with explicit China-vs-overseas measurement logic.<br><br>
      <strong>Best for</strong><br>
      Official-site-first retrieval, business recognition, direct and indirect tracking design, HTML and DOCX deliverables.<br><br>
      <strong>Public demos</strong><br>
      Overseas demo: <a href="skills/geo-tracking-plan/examples/hubspot-demo/report_input.json">HubSpot input</a> ·
      <a href="skills/geo-tracking-plan/examples/hubspot-demo/hubspot-geo-tracking-plan.html">HTML</a> ·
      <a href="skills/geo-tracking-plan/examples/hubspot-demo/hubspot-geo-tracking-plan.docx">DOCX</a><br>
      China synthetic demo: <a href="skills/geo-tracking-plan/examples/xingfan-demo/report_input.json">星帆企服 input</a> ·
      <a href="skills/geo-tracking-plan/examples/xingfan-demo/xingfan-cn-geo-tracking-plan.html">HTML</a> ·
      <a href="skills/geo-tracking-plan/examples/xingfan-demo/xingfan-cn-geo-tracking-plan.docx">DOCX</a><br><br>
      <strong>Links</strong><br>
      <a href="docs/skills/geo-tracking-plan.md">Guide</a> ·
      <a href="skills/geo-tracking-plan">Package</a> ·
      <a href="skills/geo-tracking-plan/assets/screenshots/hubspot-geo-tracking-plan.png">Overseas screenshot</a> ·
      <a href="skills/geo-tracking-plan/assets/screenshots/xingfan-cn-geo-tracking-plan.png">China screenshot</a>
    </td>
  </tr>
</table>

### `research`

<table>
  <tr>
    <td valign="top" width="100%">
      <strong>Coming soon</strong><br>
      中文：当前仓库还没有正式发布的 research family skill；这一组会优先承载关键词发现、竞品证据扫描、品牌事实表、内容审计等 GEO 研究型工作。<br>
      English: There is no published research-family skill yet. This section is reserved for GEO keyword discovery, competitor evidence scans, brand fact sheets, and content audit packages.<br><br>
      <strong>Planned directions</strong><br>
      <code>geo-keyword-discovery</code> · <code>geo-competitor-scan</code> · <code>geo-brand-fact-sheet</code> · <code>geo-content-audit</code><br><br>
      <strong>Contribute</strong><br>
      If you are packaging a GEO research workflow, use the repository contract in <a href="docs/publishing-rules.md">Publishing Rules</a> and register the skill in <a href="registry/skills.json">registry/skills.json</a>.
    </td>
  </tr>
</table>

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
