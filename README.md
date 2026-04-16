# Yao GEO Skills

面向 `GEO`（`Generative Engine Optimization`）工作流的开源 Skill 仓库。

英文说明文档：
[英文版 README](docs/README.en.md)

说明：
本仓库里的 `GEO` 指生成式引擎优化，不是地理信息或地图相关工具。

## 仓库定位与背景

`yao-geo-skills` 用来沉淀一批可复用、可验证、可开源分享的 GEO Skill。  
这里关注的不是零散 prompt，而是完整的执行资产：

- 有清晰边界的 `SKILL.md`
- 有稳定接口的 `agents/interface.yaml`
- 有参考方法、样例、脚本和 eval 的完整包
- 有公开可复用的示例输入、输出和截图

这个仓库适合沉淀以下类型的能力：

- GEO 运营流程
- GEO 效果追踪与归因
- GEO 研究与证据扫描
- GEO 相关的共享模板、schema、rubric 和交付规则

如果一句话概括，这个仓库的目标是：
把 GEO 相关的重复工作，整理成团队可以长期复用的 Skill 包。

## 仓库特点

- 强调可复用：每个 skill 都应该能在相似任务里重复使用，而不是一次性 prompt。
- 强调可验证：仓库和 skill 都有结构校验，不鼓励“能跑就行”的散装内容。
- 强调边界：明确什么时候该用、什么时候不该用，避免 skill 泛化成空话。
- 强调开源安全：公开案例必须去隐私、去内网依赖、去私有系统绑定。
- 强调交付：不少 skill 不只输出文字，还会生成 HTML、DOCX 等可直接交付的产物。
- 强调方法沉淀：复杂方法会拆到 `references/`、`scripts/`、`evals/` 中，而不是堆在一个超长 prompt 里。

## 适用范围

适合：

- 想复用 GEO 相关方法，而不是每次重写 prompt
- 想把 GEO 任务做成标准化 skill 包
- 想公开分享 GEO 工作流，同时控制质量和隐私
- 想沉淀可阅读、可验证、可演示的 GEO 样例

不适合：

- 只想存放一批零散 prompt
- 只想记录临时脑暴，不关心复用与维护
- 需要私有系统、私有文档、私有 API 才能运行的内容
- 与 GEO 无关的通用型 skill 仓库

## 仓库逻辑

本仓库的组织逻辑很简单：

1. 一个 skill 解决一个明确工作。
2. `skills/` 存技能包本体。
3. `docs/skills/` 存更适合人读的说明页。
4. `registry/skills.json` 记录仓库内 skill 清单。
5. `shared/` 存共享模板、schema、约定。
6. `scripts/validate_repository.py` 负责做仓库级结构校验。

对外展示时，这个仓库优先传达三件事：

- 这个 skill 是干什么的
- 这个 skill 怎么保证质量
- 这个 skill 有没有公开可看的示例

## 下载方式

### 下载整个仓库

#### 方式 1：`git clone`

```bash
git clone https://github.com/yaojingang/yao-geo-skills.git
cd yao-geo-skills
```

#### 方式 2：GitHub 页面下载 ZIP

在 GitHub 仓库页面点击：

`Code` -> `Download ZIP`

### 只拉取某个 skill

#### 方式 1：Sparse Checkout

```bash
git clone --filter=blob:none --no-checkout https://github.com/yaojingang/yao-geo-skills.git
cd yao-geo-skills
git sparse-checkout init --cone
git sparse-checkout set skills/geo-tracking-plan docs/skills/geo-tracking-plan.md
git checkout main
```

#### 方式 2：手动下载

直接打开对应 skill 目录，在 GitHub 页面按需下载文件：

- [skills/geo-tracking-plan](skills/geo-tracking-plan)
- [skills/geoflow-cli-ops](skills/geoflow-cli-ops)

## Skills 导航

当前 catalog 按工作类型分成 `operations / measurement / research` 三组，方便快速判断一个 skill 是偏执行、偏监测，还是偏研究。

### `operations`

<table>
  <tr>
    <td valign="top" width="100%">
      <strong><code>geoflow-cli-ops</code></strong><br>
      作用：通过本地 <code>geoflow</code> CLI 操作已有的 GEOFlow 系统，用于目录查询、任务管理、文章上传、审核与发布。<br><br>
      适合：已经有 GEOFlow 系统，需要通过 CLI 做运营动作、批量处理或自动化编排。<br><br>
      相关入口：<br>
      <a href="docs/skills/geoflow-cli-ops.md">说明页</a> ·
      <a href="skills/geoflow-cli-ops">Skill 包</a> ·
      <a href="https://github.com/yaojingang/GEOFlow">GEOFlow 项目</a>
    </td>
  </tr>
</table>

### `measurement`

<table>
  <tr>
    <td valign="top" width="100%">
      <strong><code>geo-tracking-plan</code></strong><br>
      作用：输入公司名称和辅助信息，基于官网与官方资产生成 GEO 后端效果追踪方案，显式区分国内 / 海外 / 混合 GEO 的不同监测逻辑。<br><br>
      适合：官网优先检索、业务识别、直接与间接效果设计、可视化 HTML 报告、DOCX 交付。<br><br>
      公开示例：<br>
      海外示例：<a href="skills/geo-tracking-plan/examples/hubspot-demo/report_input.json">HubSpot 输入</a> ·
      <a href="skills/geo-tracking-plan/examples/hubspot-demo/hubspot-geo-tracking-plan.html">HTML</a> ·
      <a href="skills/geo-tracking-plan/examples/hubspot-demo/hubspot-geo-tracking-plan.docx">DOCX</a><br>
      国内合成示例：<a href="skills/geo-tracking-plan/examples/lingxu-demo/report_input.json">岭序商机云输入</a> ·
      <a href="skills/geo-tracking-plan/examples/lingxu-demo/lingxu-cn-geo-tracking-plan.html">HTML</a> ·
      <a href="skills/geo-tracking-plan/examples/lingxu-demo/lingxu-cn-geo-tracking-plan.docx">DOCX</a><br><br>
      相关入口：<br>
      <a href="docs/skills/geo-tracking-plan.md">说明页</a> ·
      <a href="skills/geo-tracking-plan">Skill 包</a> ·
      <a href="skills/geo-tracking-plan/assets/screenshots/hubspot-geo-tracking-plan.png">海外截图</a> ·
      <a href="skills/geo-tracking-plan/assets/screenshots/lingxu-cn-geo-tracking-plan.png">国内截图</a>
    </td>
  </tr>
</table>

### `research`

<table>
  <tr>
    <td valign="top" width="100%">
      <strong>待发布</strong><br>
      当前仓库还没有正式发布的 research family skill；这一组会优先承载关键词发现、竞品证据扫描、品牌事实表、内容审计等 GEO 研究型工作。<br><br>
      规划方向：<br>
      <code>geo-keyword-discovery</code> ·
      <code>geo-competitor-scan</code> ·
      <code>geo-brand-fact-sheet</code> ·
      <code>geo-content-audit</code><br><br>
      如需贡献 research 类 skill，请先阅读：<br>
      <a href="docs/publishing-rules.md">发布规则</a> ·
      <a href="registry/skills.json">技能清单</a>
    </td>
  </tr>
</table>

## 相关示例

目前仓库里最完整的公开示例来自 `geo-tracking-plan`：

- 海外公开公司示例：HubSpot
- 国内公开合成示例：岭序商机云
- 示例输出形态：`report_input.json`、`HTML`、`DOCX`、截图

这些示例的作用不是给出“真实经营结论”，而是展示：

- 方法论如何落到结构化输入
- Skill 如何把方法渲染成可视化交付物
- 国内与海外 GEO 的监测逻辑有什么不同

## 目录导航

```text
yao-geo-skills/
├── README.md
├── LICENSE
├── .github/
├── docs/
│   ├── README.en.md
│   ├── repository-design.md
│   ├── input-output-contract.md
│   ├── naming-conventions.md
│   ├── eval-policy.md
│   ├── publishing-rules.md
│   └── skills/
├── registry/
├── scripts/
├── shared/
└── skills/
```

常用目录说明：

- [skills/](skills)：Skill 包本体
- [docs/skills/](docs/skills)：适合直接阅读的 skill 说明文档
- [registry/skills.json](registry/skills.json)：仓库 skill 清单
- [scripts/validate_repository.py](scripts/validate_repository.py)：仓库级校验脚本
- [docs/](docs)：仓库规则、契约、命名和发布说明

## 仓库文档

- [英文首页说明](docs/README.en.md)
- [仓库设计](docs/repository-design.md)
- [输入输出契约](docs/input-output-contract.md)
- [命名规范](docs/naming-conventions.md)
- [评测策略](docs/eval-policy.md)
- [发布规则](docs/publishing-rules.md)

## 设计原则

- 一个 skill 只做一件明确的事
- 优先公开可验证资料，不鼓励事实型 skill 依赖未授权信息
- 输出既要人能读，也要机器能校验
- 公开示例必须去隐私、去内网依赖、去私有客户数据
- eval 和结构检查是默认要求，不是可选项
- 与其堆提示词，不如沉淀长期可维护的技能包

## 贡献与发布流程

1. 在 `skills/<skill-id>/` 下新增或更新 skill。
2. 在 `docs/skills/` 下补充对应说明页。
3. 在 [`registry/skills.json`](registry/skills.json) 中登记 skill。
4. 运行仓库校验：

```bash
python3 scripts/validate_repository.py
```

5. 自查 diff，确认没有私有数据、临时文件或错误示例。
6. 提交并推送。
7. 非小改动建议通过 PR 方式合并。

更细的发布规则见：
[docs/publishing-rules.md](docs/publishing-rules.md)
