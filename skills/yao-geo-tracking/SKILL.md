---
name: yao-geo-tracking
description: Build a company-specific GEO backend tracking plan from a company name plus optional supporting information, using authoritative retrieval anchored on the official website, business-feature recognition, and market-aware GEO monitoring methods, then deliver a direct-vs-indirect attribution design, data model, roadmap, and optional openable HTML and Word reports. Use when asked to 设计 GEO 后端效果归因框架、GEO 效果跟踪体系、AI 搜索效果监测方案、GEO 转化追踪方案、GEO attribution plan、GEO tracking plan、GEO 后端分析 HTML 或 Word 交付件. Do not use for generic GEO education, content planning, pure brand research, or CRM/BI implementation work without GEO attribution design.
---

# Yao GEO Tracking

## When To Use

- 输入公司名、品牌名和少量辅助信息，希望系统自行完成权威检索，并生成适合这家公司的 GEO 后端效果归因框架与跟踪体系方案。
- 需要以官网为核心依据，结合公开资料和用户补充信息，识别业务特征，再输出个性化的直接效果与间接效果监测设计。
- 交付物需要是结构化方案，最好还能直接生成 `HTML` 与 `Word` 文件。
- 需要把“企业类型、转化链路、现有站点能力、可追踪信号”映射成优先级明确的落地路线图。

## Do Not Use

- 用户只是想了解 GEO 是什么，或者只要一套泛方法论科普。
- 用户只想做 GEO 内容策略、选题规划、信源分析或竞品调研。
- 用户只想做 SEO、SEM、CRM 埋点或 BI 看板实现，不需要 GEO 归因框架设计。
- 用户明确只要代码实施，不要分析方案、数据口径和归因设计。

## Required Inputs

最少输入只有公司名。下面这些信息如果用户给了，就一起吸收：

- 品牌别名、英文名、产品名、核心业务线
- 已知官网或疑似官网链接
- 目标市场、客群、典型转化动作
- 已有落地页、表单、热线、企微、优惠码、顾问入口等承接资产
- 重点 AI 平台、重点关键词主题、希望监测的核心动作
- 是否需要直接输出 `HTML` / `Word`

如果用户没有补充信息，也要从公司名启动，并在结尾显式列出信息缺口。

## Required Reading

开始前按需读：

- `references/evidence-sourcing-workflow.md`
- `references/attribution-framework.md`
- `references/personalization-matrix.md`
- `references/market-split-framework.md`
- `references/quality-gates.md`
- `references/html-output-outline.md`
- `references/report-ui-rules.md`
- `references/output-file-workflow.md`
- `references/open-source-sanitization.md`
- `references/observability-estimation-framework.md`

## Workflow

1. 先统一企业实体。
   - 规范化公司全称、品牌名、产品名、别名和英文名。
   - 如果同名公司不止一个，先做候选对齐，再继续分析。
2. 不使用内部系统作为默认依赖。
   - 优先使用用户提供的信息与公开可验证资料。
   - 若可联网，先确认官方域名，再补充官网、产品页、关于页、联系页、定价页、案例页、招聘页等公开证据。
   - 若不能联网，则显式声明仅基于用户提供材料输出低置信度版本。
3. 判断市场范围与平台环境。
   - 明确当前分析更偏 `国内 GEO`、`海外 GEO` 或 `混合 GEO`。
   - 国内 GEO 若主要围绕 `DeepSeek`、`豆包`、`元宝`、`Kimi` 等平台，要提高对口令、问卷、企微、电话、活动页和专属承接动作的权重。
   - 海外 GEO 若主要围绕 `ChatGPT`、`Gemini`、`Perplexity` 等平台，可更强依赖官网内容结构、落地页、表单字段、Web analytics 和官方页面矩阵。
4. 建立公开证据账本。
   - 每条关键资料都记录 `source_system`、`source_locator`、`absolute_time`、`fact_or_inference`、`how_used`。
   - “最新”相关结论必须写绝对日期；拿不到日期时，不能说“最新”。
5. 先判断业务类型与转化链路。
   - 至少判定 `B2B 销售型`、`PLG / SaaS`、`电商 / 标准化消费`、`预约 / 咨询型服务` 中的主类型。
   - 结合 `references/personalization-matrix.md` 选择最匹配的承接动作与指标口径。
6. 核验官方网站，不要把二手页面当官网。
   - 核验品牌自称、关于我们、联系方式、法律页、社媒或招聘页的一致性。
   - 不要把媒体稿、目录站、代理商页误判成官网。
7. 建立企业 GEO 后端分析底稿。
   - 至少记录公司定位、核心产品、目标人群、典型转化路径、现有承接资产、当前监测能力、站点能力限制。
   - 明确哪些是已验证事实，哪些是基于事实的推断。
8. 按“直接效果 / 间接效果”双层建模。
   - 先把 GEO 价值拆成 `品牌层价值` 与 `效果转化层价值`。
   - 品牌层价值强调 AI 平台中的“第三方背书”作用，包括品牌认知、信任建立、心智强化和后续成交阻力下降。
   - 效果转化层价值再拆成 `可直接监测的效果` 与 `间接促进的效果`。
   - 直接效果：专属电话、专属手机号、专属微信号、专属顾问入口、专属福利口令、AI 专属落地页、表单字段、来源参数、活动页、定制 CTA。
   - 间接效果：品牌词检索量、官网 UV、落地页 UV、CTA 点击率、注册率、预约率、线索率、成交率、自报来源问卷。
   - 在 `现状诊断` 下必须增加 `效果追踪方法与原理说明` 模块，用表格列出所有直接与间接监测的原理、方法、适用条件、执行动作建议；如交付为 HTML，优先再配一组流程图示。
   - 在 `间接效果追踪方案` 下必须增加 `监测效果边界说明` 模块，说明可直接观测的 GEO 效果通常只是总贡献的一部分，常见保守规划假设约为 `20%~30%`，海外官网承接强的场景可能更高；该比例只能作为规划与解释边界，不能写成跨行业固定事实。
   - 在 `监测效果边界说明` 下必须继续增加 `可观测性估算框架` 模块，输出 `Observed / Recoverable / Unobservable` 三层规划值或区间、适用前提、主要决定因素和下一阶段校准动作。
   - 明确说明：GEO 总效果通常不能被完整追踪，方案重点是建立足够解释趋势、校准方向和指导优化动作的最小闭环。
9. 结合企业实际情况和市场类型筛选方案。
   - 高客单、长决策链业务优先做线索归因、专属顾问入口、表单字段、问卷补充。
   - 标准化消费业务优先做落地页、优惠口令、来源参数、注册转化、购买后自报来源。
   - 海外 GEO 可更多围绕官网页矩阵、表单来源、页面事件和升级路径设计。
   - 国内 GEO 通常要更重视口令、活动页、企微/电话、问卷补录和跨端来源补丁。
   - 如果官网能力弱，要优先补承接页和最小归因闭环，而不是堆复杂指标。
10. 输出个性化方案。
   - 至少覆盖目标、口径、数据源、实现方式、优先级、负责方、可解释性、缺口与风险。
   - 如果用户要“分析方案”而不是“实施方案”，也要给出最小可落地动作清单。
11. 若用户要求交付文件。
   - 先把结论整理成 `report_input.json`。
   - 再运行：
   - `python3 scripts/render_yao_geo_tracking.py --input <report_input.json> --output-dir <输出目录>`
   - 默认生成 `.html` 与 `.docx`。
12. 公开版 skill 必须保持隐私干净。
   - 不要要求任何私有 CLI、内网地址、私有表、公司内部文档。
   - 不要把私有公司样本、未公开指标、内部截图写进 examples、assets、reports 或交付示例。

## Output Contract

每次执行至少返回以下内容：

- `企业理解摘要`：公司定位、产品、目标人群、典型转化动作
- `市场分层判断`：国内 / 海外 / 混合 GEO 及其对方案的影响
- `公开证据表`：官网与公开材料的来源、绝对日期、关键事实、用途
- `官网核验`：官方域名、核验依据、相关公开页面
- `现状诊断`：现有 GEO 承接与归因能力、明显缺口、已具备资产
- `效果追踪方法与原理说明`：品牌价值、转化价值、直接与间接监测逻辑，至少包含一张方法表和一组图示或流程结构
- `直接效果追踪方案`
- `间接效果追踪方案`
- `监测效果边界说明`
- `可观测性估算框架`
- `归因口径与数据表设计`
- `优先级路线图`
- `置信度与缺口`
- `可视化 HTML 方案`
- `可交付文件`：如用户要求，真实生成 `.html` 与 `.docx`

## Validation Checklist

- 输出没有依赖任何私有系统、私有 API、内部知识库或未授权资料。
- 官方网站已经显式核验，而不是凭搜索结果主观认定。
- 已判断国内 / 海外 / 混合 GEO 场景，并据此调整监测方法重点。
- 每条关键判断都能回到证据表，并区分事实与推断。
- “最新”相关说法都带绝对日期。
- 输出明确区分了直接效果和间接效果。
- 输出明确区分了品牌层价值、直接效果和间接效果，并解释三者关系。
- 输出包含 `效果追踪方法与原理说明`、`监测效果边界说明` 以及 `可观测性估算框架`。
- 如果输出了 `Observed / Recoverable / Unobservable` 三层百分比分配，三者合计必须为 `100%`。
- 方案体现企业业务类型、转化链路和站点能力差异，而不是通用模板套话。
- `20%~30%` 之类的可观测占比若被使用，必须写成保守规划假设或边界说明，不能冒充普适结论。
- 如果公开证据不足，显式写出信息缺口与降低确定性的原因。
- 如用户要求交付件，必须真实生成 `.html` 与 `.docx` 文件，而不是只说会生成。

## Reference Map

- `references/evidence-sourcing-workflow.md`：公开证据获取顺序与证据表规范
- `references/attribution-framework.md`：直接效果、间接效果和数据设计框架
- `references/personalization-matrix.md`：按业务类型个性化选择归因动作
- `references/market-split-framework.md`：国内 GEO 与海外 GEO 的监测差异和路由规则
- `references/quality-gates.md`：开源版 skill 的质量门
- `references/html-output-outline.md`：HTML 报告结构与可视化模块
- `references/report-ui-rules.md`：设计系统化的 HTML 报告 UI 规则
- `references/output-file-workflow.md`：报告输入结构与文件生成流程
- `references/open-source-sanitization.md`：去隐私、去内网依赖、公开样例替换规则
- `references/observability-estimation-framework.md`：三层可观测性估算框架与区间规则
- `scripts/render_yao_geo_tracking.py`：生成 HTML / Word 交付件
- `examples/hubspot-demo/report_input.json`：公开演示输入样例
- `evals/trigger_cases.json`：触发边界
- `evals/quality_cases.json`：质量与隐私门样例
