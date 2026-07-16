# Yao GEO Skills

面向 `GEO`（`Generative Engine Optimization`）工作流的开源 Skill 仓库。

英文说明文档：
[英文版 README](docs/README.en.md)

可视化导航页：
[index.html](index.html)

说明：
本仓库里的 `GEO` 指生成式引擎优化，不是地理信息或地图相关工具。

## 当前状态

当前仓库包含 `21` 个 GEO 相关 skill，覆盖战略诊断、页面技术、内容生产、知识资产、监测归因、研究拓词和 GEOFlow 运营。

| 分类 | 数量 | 代表场景 |
|---|---:|---|
| `geo-operations` | 3 | GEOFlow CLI 操作、模板映射、Laravel Blade 主题编辑 |
| `geo-strategy` | 2 | GEO 全景诊断、30/60/90 天执行路线图 |
| `geo-page-technical` | 2 | 页面 GEO 诊断、GEO 友好页面蓝图 |
| `geo-content-production` | 6 | 标题、科普、对比、文章 AI 友好化、旧文改造、榜单评测 |
| `geo-knowledge-assets` | 2 | 品牌知识图谱、品牌知识库和事实卡 |
| `geo-measurement` | 5 | GEO 归因追踪、AI 答案监测月报、DeepSeek 重复采样、豆包 App/Web 重复采样、ChatGPT AI Search 采样概率报告 |
| `geo-research` | 1 | AI 搜索问题集、意图簇和监测 Prompt |

每个正式 skill 至少包含：

- `SKILL.md`：Agent 调用入口和执行边界
- `manifest.json`：公开元信息
- `templates/brief-template.md`：输入简报模板
- `evals/trigger_cases.json` 与 `evals/expected_artifacts.json`：触发和产物校验
- `docs/skills/<skill-id>.md`：适合 GitHub 用户阅读的说明页

可运行仓库校验：

```bash
python3 scripts/validate_repository.py
```

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
git sparse-checkout set skills/yao-geo-tracking docs/skills/yao-geo-tracking.md
git checkout main
```

#### 方式 2：手动下载

直接打开对应 skill 目录，在 GitHub 页面按需下载文件：

- [skills/yao-geo-tracking](skills/yao-geo-tracking)
- [skills/yao-deepseek-crawler](skills/yao-deepseek-crawler)
- [skills/yao-doubao-crawler](skills/yao-doubao-crawler)
- [skills/yao-chatgpt-crawler](skills/yao-chatgpt-crawler)
- [skills/yao-geo-effect-monitor](skills/yao-geo-effect-monitor)
- [skills/yao-geo-panorama-audit](skills/yao-geo-panorama-audit)
- [skills/yao-geo-page-audit](skills/yao-geo-page-audit)
- [skills/yao-geo-ranking-article-builder](skills/yao-geo-ranking-article-builder)
- [skills/yao-geo-article-friendly](skills/yao-geo-article-friendly)
- [skills/yao-geo-explainer-builder](skills/yao-geo-explainer-builder)
- [skills/yao-geo-content-refiner](skills/yao-geo-content-refiner)
- [skills/yao-geo-title-optimizer](skills/yao-geo-title-optimizer)
- [skills/yao-geo-comparison-builder](skills/yao-geo-comparison-builder)
- [skills/yao-geo-execution-roadmap](skills/yao-geo-execution-roadmap)
- [skills/yao-geo-page-blueprint](skills/yao-geo-page-blueprint)
- [skills/yao-geo-brand-graph](skills/yao-geo-brand-graph)
- [skills/yao-geo-knowledge-base-builder](skills/yao-geo-knowledge-base-builder)
- [skills/yao-geo-intent-miner](skills/yao-geo-intent-miner)
- [skills/yao-geoflow-cli](skills/yao-geoflow-cli)
- [skills/yao-geoflow-template](skills/yao-geoflow-template)
- [skills/yao-geoflow-design](skills/yao-geoflow-design)

## Skills 导航

当前 catalog 按工作类型分成 `operations / strategy / page-technical / content-production / knowledge-assets / measurement / research`，方便快速判断一个 skill 是偏执行、偏战略诊断、偏页面技术、偏内容生产、偏知识资产、偏监测，还是偏研究。

### `operations`

<table>
  <tr>
    <td valign="top" width="100%">
      <strong><code>yao-geoflow-cli</code></strong><br>
      作用：通过受支持的 CLI、Laravel <code>/api/v1</code> 和已登录后台操作 GEOFlow 2.1+ 系统，覆盖任务、素材、文章、分发、增长中心、企业知识库、主题编辑和前端能力同步。<br><br>
      适合：已经有 GEOFlow 系统，需要做运营动作、增长线索导出、知识库草稿流、渠道能力刷新、批量处理、Docker 部署预检或高风险操作前确认。<br><br>
      相关入口：<br>
      <a href="docs/skills/yao-geoflow-cli.md">说明页</a> ·
      <a href="skills/yao-geoflow-cli">Skill 包</a> ·
      <a href="https://github.com/yaojingang/GEOFlow">GEOFlow 项目</a>
    </td>
  </tr>
  <tr>
    <td valign="top" width="100%">
      <strong><code>yao-geoflow-template</code></strong><br>
      作用：保留旧 GEOFlow PHP 模板包的兼容入口，用来解释历史 <code>index.php</code>、<code>article.php</code>、<code>includes/*.php</code> 输出契约，并生成交给 design skill 的迁移说明。<br><br>
      适合：明确查看 legacy template skill、旧 PHP 模板包、历史 mapping/tokens 输出；当前 Laravel Blade 主题、参考站拆解和首页模块设计应转交 <code>yao-geoflow-design</code>。<br><br>
      相关入口：<br>
      <a href="docs/skills/yao-geoflow-template.md">说明页</a> ·
      <a href="docs/skills/yao-geoflow-template.en.md">English Guide</a> ·
      <a href="skills/yao-geoflow-template">Skill 包</a> ·
      <a href="https://github.com/yaojingang/GEOFlow">GEOFlow 项目</a>
    </td>
  </tr>
  <tr>
    <td valign="top" width="100%">
      <strong><code>yao-geoflow-design</code></strong><br>
      作用：作为当前 GEOFlow 前端体验主 skill，识别 Laravel Blade 主题、设计 homepage module/style JSON、处理 <code>lead_form</code> 转化模块、比较默认站和渠道目标包能力，并规划同步预览。<br><br>
      适合：默认站首页设计、参考站拆解、主题预览编辑、在线主题编辑策略、渠道前端能力适配、target package 能力差异和不破坏 SEO/schema 的前端迭代。<br><br>
      相关入口：<br>
      <a href="docs/skills/yao-geoflow-design.md">说明页</a> ·
      <a href="docs/skills/yao-geoflow-design.en.md">English Guide</a> ·
      <a href="skills/yao-geoflow-design">Skill 包</a> ·
      <a href="https://github.com/yaojingang/GEOFlow">GEOFlow 项目</a>
    </td>
  </tr>
</table>

### `strategy`

<table>
  <tr>
    <td valign="top" width="100%">
      <strong><code>yao-geo-panorama-audit</code></strong><br>
      作用：建立品牌 GEO 全景基线，面向 DeepSeek、豆包、千问、Kimi、元宝诊断 AI 答案可见性、竞品差距、内容页面缺口、官网证据和外部信源，并输出机会地图与 P0/P1 优先级。<br><br>
      适合：项目启动、季度复盘、竞品追赶、投放前评估，以及需要先判断 GEO 机会和资源优先级的战略诊断。<br><br>
      合成示例：<br>
      <a href="skills/yao-geo-panorama-audit/examples/lingxu-synthetic-panorama/lingxu-panorama-audit.md">Markdown</a> ·
      <a href="skills/yao-geo-panorama-audit/examples/lingxu-synthetic-panorama/lingxu-panorama-audit.html">HTML</a> ·
      <a href="skills/yao-geo-panorama-audit/examples/lingxu-synthetic-panorama/lingxu-panorama-audit.docx">Word</a> ·
      <a href="skills/yao-geo-panorama-audit/examples/lingxu-synthetic-panorama/lingxu-panorama-audit.pdf">PDF</a><br><br>
      相关入口：<br>
      <a href="docs/skills/yao-geo-panorama-audit.md">说明页</a> ·
      <a href="skills/yao-geo-panorama-audit">Skill 包</a>
    </td>
  </tr>
  <tr>
    <td valign="top" width="100%">
      <strong><code>yao-geo-execution-roadmap</code></strong><br>
      作用：把 GEO 全景诊断、机会地图和平台采样结论转成系统、详细、完整的 30/60/90 天执行路线图，覆盖真实数据采集计划、来源新鲜度、分析完整性矩阵、证据成熟度、资源预算、治理节奏、六个项目包、国内平台适配和 kami 风格四格式交付。<br><br>
      适合：诊断完成后，需要面向 CEO、市场、增长、内容、技术和客户交付团队拆项目包、责任分工、验收指标、预算优先级和风险预案。<br><br>
      公开示例：<br>
      <a href="skills/yao-geo-execution-roadmap/examples/lingxu-demo/report_input.json">输入</a> ·
      <a href="skills/yao-geo-execution-roadmap/examples/lingxu-demo/lingxu-cn-yao-geo-execution-roadmap.md">Markdown</a> ·
      <a href="skills/yao-geo-execution-roadmap/examples/lingxu-demo/lingxu-cn-yao-geo-execution-roadmap.html">HTML</a> ·
      <a href="skills/yao-geo-execution-roadmap/examples/lingxu-demo/lingxu-cn-yao-geo-execution-roadmap.docx">Word</a> ·
      <a href="skills/yao-geo-execution-roadmap/examples/lingxu-demo/lingxu-cn-yao-geo-execution-roadmap.pdf">PDF</a><br><br>
      相关入口：<br>
      <a href="docs/skills/yao-geo-execution-roadmap.md">说明页</a> ·
      <a href="skills/yao-geo-execution-roadmap">Skill 包</a>
    </td>
  </tr>
</table>

### `page-technical`

<table>
  <tr>
    <td valign="top" width="100%">
      <strong><code>yao-geo-page-audit</code></strong><br>
      作用：输入网址后诊断首页、代表性一级页和二级页的可抓取性、结构规范性、内容信号、权威证据和 AI 可抽取性，输出代码层与内容层修复清单、Schema/HTML 建议和固定目录 HTML 报告。<br><br>
      适合：官网首页、栏目页、产品页、文章页、帮助中心、文档页、案例页和落地页的 GEO Page Audit，以及需要 Word/PDF/HTML/Markdown 四件套报告的页面诊断交付。<br><br>
      公开示例：<br>
      <a href="skills/yao-geo-page-audit/examples/example-site-demo/example-site-geo-page-audit.md">Markdown</a> ·
      <a href="skills/yao-geo-page-audit/examples/example-site-demo/example-site-geo-page-audit.html">HTML</a> ·
      <a href="skills/yao-geo-page-audit/examples/example-site-demo/example-site-geo-page-audit.docx">Word</a> ·
      <a href="skills/yao-geo-page-audit/examples/example-site-demo/example-site-geo-page-audit.pdf">PDF</a><br><br>
      相关入口：<br>
      <a href="docs/skills/yao-geo-page-audit.md">说明页</a> ·
      <a href="skills/yao-geo-page-audit">Skill 包</a>
    </td>
  </tr>
  <tr>
    <td valign="top" width="100%">
      <strong><code>yao-geo-page-blueprint</code></strong><br>
      作用：生成 GEO 友好页面的信息架构、真实数据核验计划、AI 可抽取模块、用户转化模块、HTML 语义结构、Schema 建议、CMS 字段清单，以及 Word/PDF/HTML/Markdown 四格式页面蓝图报告。<br><br>
      适合：官网产品页、专题页、文章页、榜单页、对比页、FAQ页、知识库页和案例页设计，尤其是需要同时服务国内 AI 平台抽取和真实用户转化的页面技术场景。<br><br>
      公开示例：<br>
      <a href="skills/yao-geo-page-blueprint/examples/demo/report_input.json">输入</a> ·
      <a href="skills/yao-geo-page-blueprint/examples/demo/lingxu-yao-geo-page-blueprint-demo.md">Markdown</a> ·
      <a href="skills/yao-geo-page-blueprint/examples/demo/lingxu-yao-geo-page-blueprint-demo.html">HTML</a> ·
      <a href="skills/yao-geo-page-blueprint/examples/demo/lingxu-yao-geo-page-blueprint-demo.docx">Word</a> ·
      <a href="skills/yao-geo-page-blueprint/examples/demo/lingxu-yao-geo-page-blueprint-demo.pdf">PDF</a><br><br>
      相关入口：<br>
      <a href="docs/skills/yao-geo-page-blueprint.md">说明页</a> ·
      <a href="skills/yao-geo-page-blueprint">Skill 包</a>
    </td>
  </tr>
</table>

### `content-production`

<table>
  <tr>
    <td valign="top" width="100%">
      <strong><code>yao-geo-title-optimizer</code></strong><br>
      作用：为文章、页面、FAQ 和专题生成 GEO 标题候选库，覆盖国内 AI 平台适配、品牌隔离、公开证据快照、分析维度、合规过滤、标题评分和文章结构映射。<br><br>
      适合：内容矩阵标题库、选题命名、标题候选评审、标题到文章结构映射，以及需要 Word/PDF/HTML/Markdown 四格式交付的标题系统。<br><br>
      相关入口：<br>
      <a href="docs/skills/yao-geo-title-optimizer.md">说明页</a> ·
      <a href="skills/yao-geo-title-optimizer">Skill 包</a>
    </td>
  </tr>
  <tr>
    <td valign="top" width="100%">
      <strong><code>yao-geo-comparison-builder</code></strong><br>
      作用：生成目标品牌与竞品、同类方案、传统方案或自建方案的 GEO 对比内容，覆盖真实数据获取、来源访问验证、同口径维度、证据锚点、场景选择、FAQ、风险治理和国内 AI 平台适配。<br><br>
      适合：品牌替代方案、选型页、竞品对比页、FAQ 页、商业决策类内容，以及需要 Word/PDF/HTML/Markdown 四格式交付的对比内容生产。<br><br>
      HubSpot 示例：<br>
      <a href="skills/yao-geo-comparison-builder/examples/hubspot-cn-demo/hubspot-cn-comparison-report.md">Markdown</a> ·
      <a href="skills/yao-geo-comparison-builder/examples/hubspot-cn-demo/hubspot-cn-comparison-report.html">HTML</a> ·
      <a href="skills/yao-geo-comparison-builder/examples/hubspot-cn-demo/hubspot-cn-comparison-report.docx">Word</a> ·
      <a href="skills/yao-geo-comparison-builder/examples/hubspot-cn-demo/hubspot-cn-comparison-report.pdf">PDF</a> ·
      <a href="skills/yao-geo-comparison-builder/examples/hubspot-cn-demo/quality-report.json">质量报告</a><br><br>
      相关入口：<br>
      <a href="docs/skills/yao-geo-comparison-builder.md">说明页</a> ·
      <a href="skills/yao-geo-comparison-builder">Skill 包</a>
    </td>
  </tr>
  <tr>
    <td valign="top" width="100%">
      <strong><code>yao-geo-ranking-article-builder</code></strong><br>
      作用：基于品牌 Brief、选题 JSON、竞品库和可信来源生成 GEO 榜单评测文章，覆盖真实数据边界、来源可达审计、分析完整性、评选方法、核心对比表、榜单正文、适合人群、FAQ 和来源表。<br><br>
      适合：best、top、alternatives、vs、人群和场景类榜单内容生产，以及需要 Word/PDF/HTML/Markdown 四格式文章包的投放和代理商交付。<br><br>
      公开示例：<br>
      <a href="skills/yao-geo-ranking-article-builder/examples/synthetic-demo/demo-geo-ranking-article.md">Markdown</a> ·
      <a href="skills/yao-geo-ranking-article-builder/examples/synthetic-demo/demo-geo-ranking-article.html">HTML</a> ·
      <a href="skills/yao-geo-ranking-article-builder/examples/synthetic-demo/demo-geo-ranking-article.docx">Word</a> ·
      <a href="skills/yao-geo-ranking-article-builder/examples/synthetic-demo/demo-geo-ranking-article.pdf">PDF</a><br><br>
      相关入口：<br>
      <a href="docs/skills/yao-geo-ranking-article-builder.md">说明页</a> ·
      <a href="skills/yao-geo-ranking-article-builder">Skill 包</a>
    </td>
  </tr>
  <tr>
    <td valign="top" width="100%">
      <strong><code>yao-geo-explainer-builder</code></strong><br>
      作用：生成可发布的完整 GEO 科普文章，并附带 How-to 教程、概念解释、怎么选、避坑指南、FAQ、术语表、真实数据接入状态、事实核验矩阵和品牌自然植入建议。<br><br>
      适合：品牌教育、行业知识、购买前科普、公众号教程、AI 搜索问答素材，以及需要 kami 版式 Word/PDF/HTML/Markdown 四格式交付的内容生产。<br><br>
      公开示例：<br>
      <a href="skills/yao-geo-explainer-builder/examples/acme-sleep-demo/rendered/deliverables/acme-sleep-geo-explainer.md">Markdown</a> ·
      <a href="skills/yao-geo-explainer-builder/examples/acme-sleep-demo/rendered/deliverables/html-package/index.html">HTML</a> ·
      <a href="skills/yao-geo-explainer-builder/examples/acme-sleep-demo/rendered/deliverables/acme-sleep-geo-explainer.docx">Word</a> ·
      <a href="skills/yao-geo-explainer-builder/examples/acme-sleep-demo/rendered/deliverables/acme-sleep-geo-explainer.pdf">PDF</a> ·
      <a href="skills/yao-geo-explainer-builder/examples/acme-sleep-demo/rendered/quality-report.json">质量报告</a><br><br>
      相关入口：<br>
      <a href="docs/skills/yao-geo-explainer-builder.md">说明页</a> ·
      <a href="skills/yao-geo-explainer-builder">Skill 包</a>
    </td>
  </tr>
  <tr>
    <td valign="top" width="100%">
      <strong><code>yao-geo-content-refiner</code></strong><br>
      作用：把已有 SEO 文章、公众号文章、官网文章、白皮书和产品页文案改造成结构化、可信、可引用、可抽取的 GEO 内容。<br><br>
      适合：旧文 GEO 改造、AI 可引用内容修复、FAQ、原子事实、真实数据核验、语义实体、平台适配、证据强度、CMS 发布建议，以及带 sticky HTML 菜单和 Kami 编辑排版的 Word/PDF/HTML/Markdown 四格式交付。<br><br>
      HubSpot 国内 AI 平台测试示例：<br>
      <a href="skills/yao-geo-content-refiner/examples/hubspot-cn-demo/hubspot-cn-geo-content-refiner-report.md">Markdown</a> ·
      <a href="skills/yao-geo-content-refiner/examples/hubspot-cn-demo/hubspot-cn-geo-content-refiner-report.html">HTML</a> ·
      <a href="skills/yao-geo-content-refiner/examples/hubspot-cn-demo/hubspot-cn-geo-content-refiner-report.docx">Word</a> ·
      <a href="skills/yao-geo-content-refiner/examples/hubspot-cn-demo/hubspot-cn-geo-content-refiner-report.pdf">PDF</a> ·
      <a href="skills/yao-geo-content-refiner/examples/hubspot-cn-demo/quality-report.json">质量报告</a><br><br>
      相关入口：<br>
      <a href="docs/skills/yao-geo-content-refiner.md">说明页</a> ·
      <a href="skills/yao-geo-content-refiner">Skill 包</a>
    </td>
  </tr>
  <tr>
    <td valign="top" width="100%">
      <strong><code>yao-geo-article-friendly</code></strong><br>
      作用：把已有文章改造成 GEO/AI 搜索友好的发布草稿，保留原文核心观点，强化结构、证据边界、可引用性和语义密度。<br><br>
      适合：已有文章轻量改造、AI 可引用性修复、FAQ 和摘要结构补强，以及需要明确区分原文支持、外部已核验和建议补充的内容生产。<br><br>
      相关入口：<br>
      <a href="docs/skills/yao-geo-article-friendly.md">说明页</a> ·
      <a href="skills/yao-geo-article-friendly">Skill 包</a>
    </td>
  </tr>
</table>

### `knowledge-assets`

<table>
  <tr>
    <td valign="top" width="100%">
      <strong><code>yao-geo-brand-graph</code></strong><br>
      作用：把企业信息转成品牌、产品、人物、地点、案例、证据和场景之间的实体关系图，输出来源核验、实体清单、关系清单、可信等级、Mermaid、JSON-LD、三元组和图谱补强建议。<br><br>
      适合：知识库升级、页面结构设计、监测纠偏、品牌百科化和 AI 内容一致性治理，尤其是需要解决品牌错指、简称歧义、产品关系不清和证据链缺失的场景。<br><br>
      公开示例：
      <a href="skills/yao-geo-brand-graph/examples/hubspot-domestic-ai-test/report_input.json">输入</a> ·
      <a href="skills/yao-geo-brand-graph/examples/hubspot-domestic-ai-test/hubspot-domestic-ai-yao-geo-brand-graph.md">Markdown</a> ·
      <a href="skills/yao-geo-brand-graph/examples/hubspot-domestic-ai-test/hubspot-domestic-ai-yao-geo-brand-graph.html">HTML</a> ·
      <a href="skills/yao-geo-brand-graph/examples/hubspot-domestic-ai-test/hubspot-domestic-ai-yao-geo-brand-graph.docx">Word</a> ·
      <a href="skills/yao-geo-brand-graph/examples/hubspot-domestic-ai-test/hubspot-domestic-ai-yao-geo-brand-graph.pdf">PDF</a><br><br>
      相关入口：<br>
      <a href="docs/skills/yao-geo-brand-graph.md">说明页</a> ·
      <a href="skills/yao-geo-brand-graph">Skill 包</a>
    </td>
  </tr>
  <tr>
    <td valign="top" width="100%">
      <strong><code>yao-geo-knowledge-base-builder</code></strong><br>
      作用：基于官网、产品页、帮助中心、白皮书、销售材料、媒体稿和资质文件生成系统化 GEO 品牌知识库、完整实体清单、真实数据获取边界、事实卡、FAQ、禁用表达、Prompt 输入包和来源索引。<br><br>
      适合：内容生成、内容改造、页面设计、监测和客服问答前置准备，尤其是面向 Kimi、千问、DeepSeek、豆包、元宝复用结构化品牌事实的知识资产场景。<br><br>
      公开示例：
      <a href="skills/yao-geo-knowledge-base-builder/examples/hubspot-demo/report_input.json">输入</a> ·
      <a href="skills/yao-geo-knowledge-base-builder/examples/hubspot-demo/deliverables/hubspot-demo-geo-knowledge-base.html">HTML</a> ·
      <a href="skills/yao-geo-knowledge-base-builder/examples/hubspot-demo/deliverables/hubspot-demo-geo-knowledge-base.md">Markdown</a> ·
      <a href="skills/yao-geo-knowledge-base-builder/examples/hubspot-demo/deliverables/hubspot-demo-geo-knowledge-base.docx">Word</a> ·
      <a href="skills/yao-geo-knowledge-base-builder/examples/hubspot-demo/deliverables/hubspot-demo-geo-knowledge-base.pdf">PDF</a><br><br>
      相关入口：<br>
      <a href="docs/skills/yao-geo-knowledge-base-builder.md">说明页</a> ·
      <a href="skills/yao-geo-knowledge-base-builder">Skill 包</a>
    </td>
  </tr>
</table>

### `measurement`

<table>
  <tr>
    <td valign="top" width="100%">
      <strong><code>yao-geo-tracking</code></strong><br>
      作用：输入公司名称和辅助信息，基于官网与官方资产生成 GEO 后端效果追踪方案，显式区分国内 / 海外 / 混合 GEO 的不同监测逻辑。<br><br>
      适合：官网优先检索、业务识别、直接与间接效果设计、可视化 HTML 报告、DOCX 交付。<br><br>
      公开示例：<br>
      海外示例：<a href="skills/yao-geo-tracking/examples/hubspot-demo/report_input.json">HubSpot 输入</a> ·
      <a href="skills/yao-geo-tracking/examples/hubspot-demo/hubspot-yao-geo-tracking.html">HTML</a> ·
      <a href="skills/yao-geo-tracking/examples/hubspot-demo/hubspot-yao-geo-tracking.docx">DOCX</a><br>
      国内合成示例：<a href="skills/yao-geo-tracking/examples/lingxu-demo/report_input.json">岭序商机云输入</a> ·
      <a href="skills/yao-geo-tracking/examples/lingxu-demo/lingxu-cn-yao-geo-tracking.html">HTML</a> ·
      <a href="skills/yao-geo-tracking/examples/lingxu-demo/lingxu-cn-yao-geo-tracking.docx">DOCX</a><br><br>
      相关入口：<br>
      <a href="docs/skills/yao-geo-tracking.md">说明页</a> ·
      <a href="skills/yao-geo-tracking">Skill 包</a> ·
      <a href="skills/yao-geo-tracking/assets/screenshots/hubspot-yao-geo-tracking.png">海外截图</a> ·
      <a href="skills/yao-geo-tracking/assets/screenshots/lingxu-cn-yao-geo-tracking.png">国内截图</a>
    </td>
  </tr>
  <tr>
    <td valign="top" width="100%">
      <strong><code>yao-geo-effect-monitor</code></strong><br>
      作用：设计 GEO Signal Monitor，面向 DeepSeek、豆包、千问、Kimi、元宝建立 AI 答案监测、引用追踪、真实数据获取、报告完整性模型、品牌事实纠偏、月报告警和谨慎归因闭环。<br><br>
      适合：GEO 长期运营、客户月报、内容迭代、页面优化、外部信源建设、品牌事实纠偏和看板/API 字段规划。<br><br>
      示例报告：<a href="skills/yao-geo-effect-monitor/examples/synthetic-demo/xinglan-effect-monitor-demo.md">Markdown</a> ·
      <a href="skills/yao-geo-effect-monitor/examples/synthetic-demo/xinglan-effect-monitor-demo.html">HTML</a> ·
      <a href="skills/yao-geo-effect-monitor/examples/synthetic-demo/xinglan-effect-monitor-demo.docx">Word</a> ·
      <a href="skills/yao-geo-effect-monitor/examples/synthetic-demo/xinglan-effect-monitor-demo.pdf">PDF</a><br><br>
      相关入口：<br>
      <a href="docs/skills/yao-geo-effect-monitor.md">说明页</a> ·
      <a href="skills/yao-geo-effect-monitor">Skill 包</a>
    </td>
  </tr>
  <tr>
    <td valign="top" width="100%">
      <strong><code>yao-deepseek-crawler</code></strong><br>
      作用：通过 OpenCLI Browser Bridge 调用 DeepSeek 网页端，按关键词和轮询次数做独立重复采样，输出原始 JSON、结构化 Markdown、Excel 和 Kami 风格可视化报告。<br><br>
      适合：评估目标实体在 DeepSeek AI 搜索里的提及率、平均提及次数、Top 1 / Top 3 / Top 5 概率、平均排名、同类型竞品对比、信源结构和 GEO 优化建议。<br><br>
      蔚来真实采样示例：<br>
      <a href="skills/yao-deepseek-crawler/examples/nio-nev-deepseek-20260620/deepseek-crawl.json">原始 JSON</a> ·
      <a href="skills/yao-deepseek-crawler/examples/nio-nev-deepseek-20260620/report-brand-company/structured-data.md">Markdown</a> ·
      <a href="skills/yao-deepseek-crawler/examples/nio-nev-deepseek-20260620/report-brand-company/structured-data.xlsx">Excel</a> ·
      <a href="skills/yao-deepseek-crawler/examples/nio-nev-deepseek-20260620/report-brand-company/report.html">HTML 报告</a><br><br>
      相关入口：<br>
      <a href="docs/skills/yao-deepseek-crawler.md">说明页</a> ·
      <a href="skills/yao-deepseek-crawler">Skill 包</a>
    </td>
  </tr>
  <tr>
    <td valign="top" width="100%">
      <strong><code>yao-doubao-crawler</code></strong><br>
      作用：通过豆包网页端或 Android Studio AVD + Appium UiAutomator2 的豆包手机 App 做关键词重复采样，输出原始 JSON、结构化 Markdown/Excel、移动端截图/XML 证据和 Kami 风格可视化报告。<br><br>
      适合：评估目标实体在豆包 AI 搜索里的提及率、Top 1 / Top 3 / Top 5 概率、同类型竞品对比、信源结构、引用资料卡片和移动端已引用/未引用资料统计。<br><br>
      验证入口：<a href="skills/yao-doubao-crawler/fixtures/sample-doubao-crawl.json">网页 fixture</a> ·
      <a href="skills/yao-doubao-crawler/fixtures/sample-doubao-mobile-crawl.json">移动端 fixture</a> ·
      <a href="skills/yao-doubao-crawler/scripts/run-tests.sh">离线测试脚本</a><br><br>
      相关入口：<br>
      <a href="docs/skills/yao-doubao-crawler.md">说明页</a> ·
      <a href="skills/yao-doubao-crawler">Skill 包</a>
    </td>
  </tr>
  <tr>
    <td valign="top" width="100%">
      <strong><code>yao-chatgpt-crawler</code></strong><br>
      作用：通过 OpenCLI Browser Bridge 连接已登录的 ChatGPT web profile，对 AI Search 问题做多次采样，抓取答案、可见来源和来源入口，生成目标实体与同类型竞品的概率分析报告。<br><br>
      适合：ChatGPT Web Search 真实采样、实体/竞品语义审计、Top 1/Top 3/Top 5 概率、引用来源分析、标题意图分析和 HTML 报告交付。<br><br>
      真实测试：<a href="skills/yao-chatgpt-crawler/examples/doubao-model-products-real/questions.txt">豆包问题列表</a> ·
      <a href="skills/yao-chatgpt-crawler/examples/doubao-model-products-real/report/summary.json">summary.json</a> ·
      <a href="skills/yao-chatgpt-crawler/examples/doubao-model-products-real/report/report.html">HTML 报告</a><br><br>
      相关入口：<br>
      <a href="docs/skills/yao-chatgpt-crawler.md">说明页</a> ·
      <a href="skills/yao-chatgpt-crawler">Skill 包</a>
    </td>
  </tr>
</table>

### `research`

<table>
  <tr>
    <td valign="top" width="100%">
      <strong><code>yao-geo-intent-miner</code></strong><br>
      作用：把种子词、品牌、产品、竞品、区域、人群和业务材料扩展成 AI 搜索问题集、意图簇、追问链路、查询重写、内容选题、FAQ 题库、知识库条目计划、证据缺口和监测 Prompt 库。<br><br>
      适合：内容生产前建立问题底座，尤其是需要面向 DeepSeek、豆包、千问、Kimi、元宝适配国内平台问法，并输出 Word/PDF/HTML/Markdown 四格式交付的意图拓词场景。<br><br>
      公开示例：<br>
      <a href="skills/yao-geo-intent-miner/examples/hubspot-cn-demo/input/report_input.json">示例输入</a> ·
      <a href="skills/yao-geo-intent-miner/examples/hubspot-cn-demo/expected-output/hubspot-cn-ai-intent-miner-demo.html">HTML</a> ·
      <a href="skills/yao-geo-intent-miner/examples/hubspot-cn-demo/expected-output/hubspot-cn-ai-intent-miner-demo.docx">Word</a> ·
      <a href="skills/yao-geo-intent-miner/examples/hubspot-cn-demo/expected-output/hubspot-cn-ai-intent-miner-demo.pdf">PDF</a> ·
      <a href="skills/yao-geo-intent-miner/examples/hubspot-cn-demo/expected-output/hubspot-cn-ai-intent-miner-demo.md">Markdown</a> ·
      <a href="skills/yao-geo-intent-miner/examples/hubspot-cn-demo/expected-output/quality-report.json">质量报告</a><br><br>
      相关入口：<br>
      <a href="docs/skills/yao-geo-intent-miner.md">说明页</a> ·
      <a href="skills/yao-geo-intent-miner">Skill 包</a>
    </td>
  </tr>
</table>

## 相关示例

仓库内已包含多组公开或合成示例，重点用于展示输入结构、方法链路、四格式交付和质量门：

- `yao-geo-tracking`：海外公开公司示例 HubSpot、国内公开合成示例岭序商机云
- `yao-deepseek-crawler`：蔚来新能源汽车 DeepSeek 网页端真实采样示例
- `yao-doubao-crawler`：豆包网页端与 Android/Appium 移动端 fixture，用于离线报告验证
- `yao-chatgpt-crawler`：豆包模型产品 ChatGPT Web Search 真实采样脱敏示例
- `yao-geo-panorama-audit`：岭序商机云 GEO 全景诊断合成示例、HubSpot 国内 AI 平台测试示例
- `yao-geo-page-audit`：示例云服页面 GEO 诊断合成示例、HubSpot 页面诊断示例
- `yao-geo-page-blueprint`：页面蓝图示例和 HubSpot 中文页面蓝图示例
- `yao-geo-ranking-article-builder`：榜单评测文章合成示例和 HubSpot 示例
- `yao-geo-comparison-builder`：HubSpot 中文对比报告示例
- `yao-geo-content-refiner`：HubSpot 旧文 GEO 改造示例
- `yao-geo-article-friendly`：轻量文章 AI 友好化改造方法、评分与证据边界示例契约
- `yao-geo-explainer-builder`：Acme Sleep 科普文章、真实数据核验和 kami 四格式报告示例
- `yao-geo-brand-graph`：HubSpot 国内 AI 平台品牌图谱示例
- `yao-geo-knowledge-base-builder`：HubSpot 品牌知识库示例
- `yao-geo-intent-miner`：HubSpot 中文 AI 意图拓词示例
- 示例输出形态：`Markdown`、`HTML`、`Word`、`PDF`、`report_input.json`、`quality-report.json`、截图或预览图（视 skill 类型而定）

这些示例的作用不是给出“真实经营结论”，而是展示：

- 方法论如何落到结构化输入
- Skill 如何把方法渲染成可视化交付物
- 国内与海外 GEO 的监测逻辑有什么不同

## 目录导航

```text
yao-geo-skills/
├── index.html
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
- [更新日志](docs/CHANGELOG.md)
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
