# Yao DeepSeek Crawler

`yao-deepseek-crawler` 是一个 DeepSeek 网页端 AI 搜索重复采样与 GEO 概率分析 Skill。它会借助本地 OpenCLI Browser Bridge 和已登录的 DeepSeek 网页会话，对用户给定的一组关键词进行多轮独立采样，保存原始证据，并生成结构化 Markdown、Excel 和 HTML 可视化诊断报告。

英文说明：[README.en.md](README.en.md)

## 适合做什么

- 对 1-20 个关键词或问句做重复采样，每个关键词可独立设置轮询次数。
- 每次采样都保留 DeepSeek 回答、来源面板、raw JSON 和执行日志。
- 围绕一个目标实体进行分析，并按用户声明的实体类型识别同类型竞品。
- 聚合提及率、平均提及次数、平均排名、Top 1 / Top 3 / Top 5 概率、情感倾向、信源结构、标题特征、重复引用和竞品差距。
- 输出 4 类交付物：原始日志 JSON、结构化 Markdown、结构化 Excel、Kami 风格 HTML 报告。

它不是通用网站爬虫，也不调用 DeepSeek API。

## 前置条件

- Node.js 21+：真实抓取推荐版本；只做离线分析时 Node.js 18+ 即可
- Python 3.10+
- OpenCLI CLI 1.8.4+
- OpenCLI Browser Bridge 已连接 Chrome 或 Edge profile
- DeepSeek 网页端已登录
- 本地 DeepSeek browser crawler 脚本，默认使用本 skill 自带的 `scripts/geo-deepseek-browser-direct.mjs`，也可以通过 `--crawler-script` 指定
- 可选：`OPENAI_API_KEY`，用于分析阶段的 AI 语义复核；没有密钥时默认自动回退到本地规则

安装和使用细节见：

- [references/user-setup-and-usage.md](references/user-setup-and-usage.md)

## 连接 Browser Bridge

如果 `opencli profile list` 显示没有已连接 profile，先在 Skill 目录执行：

```bash
node scripts/setup_deepseek_bridge.mjs
```

这个脚本只会打开 `https://chat.deepseek.com/`，不会打开其他业务网站。不要使用其他项目里的 Browser Bridge setup 脚本，例如 `opencli-boss-ai`，因为它们可能会打开自己的目标站点。

## 标准输入

```text
1. 关键词：一个或多个 DeepSeek 搜索问句
2. 轮询次数：每个关键词查询几次
3. 目标实体：例如 新东方、姚金刚、某产品名、某公司名
4. 实体类型：人、公司、产品
5. OpenCLI profile：已连接的 Browser Bridge profile
6. 抓取间隔：例如 1-3 分钟随机，或 5-20 分钟安全随机
```

目标实体别名可选，但建议提供。示例：

```text
目标实体别名：
姚金刚先生、姚金刚老师、姚金刚xx等
```

## 抓取前检查

真实抓取前检查 OpenCLI profile：

```bash
node scripts/preflight.mjs --profile <opencli-profile>
```

只基于已有 JSON 生成报告时：

```bash
node scripts/preflight.mjs --analysis-only
```

## 第一阶段：批量采样

先创建 `questions.txt`，每行一个问题：

```text
新能源汽车推荐
豪华新能源SUV品牌推荐
哪个新能源电车品牌更靠谱
推荐一款靠谱的新能源汽车品牌
```

然后执行采样：

```bash
node scripts/deepseek_batch_crawl.mjs \
  --questions questions.txt \
  --repeat 5 \
  --profile <opencli-profile> \
  --target-entity "蔚来" \
  --target-aliases "蔚来ES8,蔚来ES6,蔚来EC6,NIO" \
  --entity-type product \
  --delay-min-minutes 1 \
  --delay-max-minutes 3 \
  --safe-random-delay \
  --out-dir runs/nio-nev
```

采样输出：

- `runs/nio-nev/deepseek-crawl.json`
- `runs/nio-nev/raw/*.json`
- `runs/nio-nev/logs/*.log`

可以先加 `--dry-run` 检查计划，不打开 DeepSeek。真实长期采样建议使用 `--safe-random-delay`，默认每次新会话之间随机等待 5-20 分钟；短测试可以指定 `--delay-min-minutes 1 --delay-max-minutes 3`。

## 第二阶段：分析与报告

可选的 `brands.txt` 用于人工校准目标实体别名和竞品口径：

```text
蔚来|蔚来ES8|蔚来ES6|蔚来EC6|NIO
问界|AITO|问界M9|问界M7
理想汽车|理想L9|理想L8|理想L7
特斯拉|Tesla|Model Y|Model 3
```

生成结构化数据和 HTML 报告：

```bash
python3 scripts/analyze_deepseek_results.py \
  runs/nio-nev/deepseek-crawl.json \
  --target-entity "蔚来" \
  --target-aliases "蔚来ES8,蔚来ES6,蔚来EC6,NIO" \
  --entity-type product \
  --brands-file brands.txt \
  --semantic-review auto \
  --out-dir runs/nio-nev/report
```

分析输出：

- `runs/nio-nev/report/summary.json`
- `runs/nio-nev/report/structured-data.md`
- `runs/nio-nev/report/structured-data.xlsx`
- `runs/nio-nev/report/report.html`
- `runs/nio-nev/report/semantic-review-cache.json`（仅当 AI 语义复核产生可缓存结果时写入）

标准报告需要 `--target-entity` 和 `--entity-type`。实体类型支持 `person/人`、`company/公司`、`product/产品`。目标匹配使用“包含 + 别名”逻辑，例如目标实体 `蔚来` 可以合并 `蔚来ES8`、`蔚来ES6`、`NIO` 等别名。短英文别名会按独立 token 匹配，避免误伤更长词。竞品只保留与目标实体同类型的实体。

分析阶段支持可选 AI 语义复核：

- `--semantic-review auto`：默认模式。能调用 AI 时复核候选实体；缺少密钥或调用失败时回退本地规则，并在 `summary.json` 记录 `semantic_review_status: fallback`。
- `--semantic-review required`：正式交付前建议使用。AI 复核不可用、返回缺项或解析失败时，分析会直接失败。
- `--semantic-review off`：关闭语义复核，只使用本地规则。
- `--semantic-confidence-threshold 0.72`：AI 判定为直接竞品时的最低置信度。
- `--semantic-review-cache <path>`：复核缓存路径，默认在报告目录下写入 `semantic-review-cache.json`。

语义复核只作为增强层，不替代原始日志、正文证据和硬规则。候选项必须同时通过噪声过滤、同类型判断、置信度阈值和正文回答证据，才能进入竞品矩阵。报告和结构化导出会保留 AI 语义标签、是否同类型、是否进入竞品矩阵、置信度、判定理由和被排除原因。

## 报告能力

HTML 报告默认使用中文简体，并包含英文总结切换入口。报告包含：

- 报告概览、目录和指标说明
- 核心结论与目标实体表现
- 目标实体 vs 同类型竞品对比
- 情感提及、实体识别、AI 语义复核和采集覆盖
- 概率排名、Top 1 / Top 3 / Top 5、平均排名
- 渠道分布、来源编号位置、高频来源名、高频域名和高频 URL
- 标题功能特征、标题长度、时间新旧和标题意图
- GEO 总结建议、优化优先级、趋势预测和具体执行方法

## 蔚来真实采样示例

示例基于 2026-06-20 的真实 DeepSeek 网页端采样：

- 关键词：4 个
- 每个关键词轮询：5 次
- 计划样本：20
- 成功样本：20
- 失败样本：0
- 引用来源：199 条
- 目标实体：蔚来
- 补充别名：蔚来 ES8、蔚来 ES6、蔚来 EC6、NIO 等

示例文件：

- [问题列表](examples/nio-nev-deepseek-20260620/questions.txt)
- [品牌别名表](examples/nio-nev-deepseek-20260620/brands.txt)
- [原始聚合 JSON](examples/nio-nev-deepseek-20260620/deepseek-crawl.json)
- [品牌/公司口径 Markdown](examples/nio-nev-deepseek-20260620/report-brand-company/structured-data.md)
- [品牌/公司口径 Excel](examples/nio-nev-deepseek-20260620/report-brand-company/structured-data.xlsx)
- [品牌/公司口径 HTML 报告](examples/nio-nev-deepseek-20260620/report-brand-company/report.html)
- [产品口径 HTML 报告](examples/nio-nev-deepseek-20260620/report/report.html)
- [单次 raw 样本目录](examples/nio-nev-deepseek-20260620/raw)
- [单次日志目录](examples/nio-nev-deepseek-20260620/logs)

## 离线验证

```bash
bash scripts/run-tests.sh
```

## 运行边界

- 不处理 DeepSeek 登录、验证码、Cloudflare、人机校验、账号风控或平台限制绕过。
- 概率指标是重复采样估计，不代表真实市场份额或平台官方排名。
- 竞品实体识别优先使用用户提供的别名表；自动识别候选仍建议人工复核，正式报告建议开启 `--semantic-review required`。
- AI 语义复核是可选增强，不会覆盖硬规则、正文证据要求或原始日志审计。
- 真实抓取会打开浏览器窗口并访问 DeepSeek 网页端，请遵守目标网站规则和账号使用限制。

## 包结构

- `SKILL.md`：路由触发和工作流骨架
- `references/user-setup-and-usage.md`：安装前置条件和用户运行手册
- `references/deepseek-crawl-workflow.md`：本地 crawler 配置和抓取规则
- `references/report-contract.md`：JSON 合约和指标定义
- `scripts/preflight.mjs`：依赖和登录状态检查
- `scripts/setup_deepseek_bridge.mjs`：DeepSeek 专用 OpenCLI Browser Bridge 连接助手
- `scripts/geo-deepseek-browser-direct.mjs`：自带的 DeepSeek 问答与引用证据采集入口
- `scripts/deepseek_batch_crawl.mjs`：重复采样编排
- `scripts/test_geo_deepseek_browser_direct.mjs`：错误页面拒绝和浏览器会话清理回归测试
- `scripts/run-tests.sh`：离线验证入口
- `scripts/analyze_deepseek_results.py`：聚合分析与 HTML 渲染
- `fixtures/sample-deepseek-crawl.json`：离线测试样例
