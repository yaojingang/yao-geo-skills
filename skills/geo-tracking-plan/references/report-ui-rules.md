# Report UI Rules

## Design-System Lens

这个 HTML 报告的 UI 规则参考了 [awesome-design-systems](https://github.com/alexpate/awesome-design-systems) 所强调的几个共同点：

- 设计系统首先是 `principles + best practices` 的文档系统
- 不只是组件库，还包括 `Voice & Tone`
- 最好能映射到 `Components` 与 `Source code`

因此这个 skill 的报告页不应该只是“长页面 + 表格堆叠”，而应该像一个轻量的设计系统文档页：结构清楚、组件复用、语气稳定、可持续迭代。

## UI Principles

### 1. Token First

- 所有颜色、间距、圆角、阴影、字号都通过 token 控制
- 不直接在局部组件里硬编码视觉常量，除非是数据驱动色块

### 2. Component First

报告页至少应由这些稳定组件构成：

- Hero
- Summary card
- Section nav
- Section shell
- Callout
- Table wrapper
- Flow block
- Allocation block

### 3. Documentation First

- 页面更像“文档型信息系统”，不是营销落地页
- 先解决导航、层级、可读性、检索效率，再考虑装饰
- 重要结构应能被快速扫读，而不是靠长段落理解

### 4. Voice And Tone

- 语气应冷静、证据优先、少修辞
- UI 文案要像方法说明，不像广告 copy
- 强调 `事实 / 推断 / 规划假设 / 边界` 的区分

## Layout Rules

### Overall Structure

- 页面宽度应控制在适合长文档阅读的范围
- 顶部应先给出摘要，再给出模块导航
- 每个 section 应是独立 card，而不是一整页没有分层的大容器

### Navigation

- 必须提供 section 级导航
- 导航文案应与正文标题一致
- 在移动端导航应自然折行，不能依赖 hover

### Section Shell

- 每个 section 应有编号、标题和锚点
- 标题与正文之间留出明显但不过度夸张的间距
- section 外观要统一，不能每节都像另一套设计语言

## Data Display Rules

### Tables

- 表格是主组件，不是附属组件
- 表头必须有高对比背景
- 单元格间距、行高和条纹要稳定，便于长时间阅读
- 不要在同一页混用多套表格视觉风格

### Flow And Allocation

- 流程图示应表达“阶段关系”，而不是追求复杂图形
- `Observed / Recoverable / Unobservable` 估算模块应用统一色阶和卡片结构
- 分配图既要有视觉总览，也要有文本解释与校准动作

## Responsive Rules

- 在窄屏时，模块应优先纵向堆叠
- 横向箭头、复杂分栏、超宽表格都必须有降级策略
- 报告页应在移动端仍可读，不以桌面端为唯一目标

## Accessibility Rules

- 保持文本与背景足够对比
- 不依赖颜色单独传达意义
- 重要结论必须有文字，不只在图形里出现
- HTML 必须在禁用脚本的前提下完整可读

## Non-Goals

- 不做营销站风格的大型动画
- 不做依赖前端框架或构建系统的重实现
- 不为“炫”而加入与分析无关的图表或装饰
