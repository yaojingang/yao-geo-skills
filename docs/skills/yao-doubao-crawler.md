<!--
Copyright © 2026 姚金刚. All rights reserved.
Project: yao-doubao-crawler
Created by: 姚金刚
Date: 2026-07-03
X: https://x.com/yaojingang
-->

# yao-doubao-crawler

`yao-doubao-crawler` 是一个豆包 AI 搜索重复采样与 GEO 概率分析 skill。它支持两条采集后端：网页端 OpenCLI 自动化，以及 Android Studio AVD + Appium UiAutomator2 的豆包手机 App 可见 UI 采集。输出统一为 `yao-doubao-crawler/v1` 兼容 JSON，并生成结构化 Markdown、Excel 和 Kami 风格 HTML 可视化报告。

## 适用场景

- 评估品牌、公司、人物或产品在豆包 AI 搜索结果里的可见性
- 对同一组关键词做多轮重复采样，估算提及率、Top 1 / Top 3 / Top 5 概率和平均排名
- 分析豆包可见引用来源、标题意图、域名分布和中文来源名
- 通过 Android/Appium 保留手机 App 截图、XML、引用资料卡片、已引用/未引用状态和引用次数
- 在无目标实体时做 collection-only 或 exploratory 分析，作为后续 GEO 诊断证据

## 标准输入

```text
1. 关键词或问题列表
2. 每个关键词采集次数
3. 后端：web 或 mobile
4. 输出目录
5. 目标实体与实体类型（仅标准诊断报告需要）
6. 移动端设备、Appium server、豆包包名（mobile 后端需要）
```

目标实体和实体类型用于标准 target-vs-competitor 诊断；只做采集或探索时可以省略。

## 核心输出

- `doubao-crawl.json`：规范化后的豆包重复采样证据数据集
- `raw/*.json`：每次独立采样的原始抓取结果
- `logs/*.log`：采集日志
- `summary.json`：机器可读分析指标，移动端数据会包含 `mobile_evidence`
- `structured-data.md`：结构化字段和分析表格的 Markdown 导出
- `structured-data.xlsx`：与 Markdown 对应的 Excel 工作簿
- `report.html`：Kami 风格可视化诊断报告
- `screenshots/`、`xml/`：Android/Appium 可见 UI 证据

## 移动端链路

移动端后端使用 Android Studio AVD、Appium 3、UiAutomator2 driver 和 Python Appium Client。它只采集豆包 App 可见 UI，不绕过登录、验证码、风控、隐藏 API、网络抓包或 App 存储。

关键命令入口：

```bash
python3 -m pip install -r requirements-mobile.txt
appium driver install uiautomator2
appium --address 127.0.0.1 --port 4725
```

```bash
python3 scripts/doubao_mobile_crawl.py preflight \
  --device emulator-5554 \
  --app-package com.larus.nova \
  --server http://127.0.0.1:4725
```

```bash
python3 scripts/doubao_mobile_crawl.py batch \
  --questions questions.txt \
  --repeat 5 \
  --device emulator-5554 \
  --app-package com.larus.nova \
  --server http://127.0.0.1:4725 \
  --fresh-chat \
  --require-fresh-chat \
  --out-dir runs/mobile-doubao-poc
```

## 分析命令

```bash
python3 scripts/analyze_doubao_results.py \
  runs/mobile-doubao-poc/doubao-crawl.json \
  --target-entity "新东方" \
  --entity-type company \
  --out-dir runs/mobile-doubao-poc/report
```

如果不传 `--target-entity`，报告会进入探索模式，仅展示采集覆盖、来源结构、移动端证据和启发式候选，不声称目标对比指标。

## 验证

```bash
bash scripts/run-tests.sh
```

该命令会执行 Node/Python 静态检查、实体识别回归、移动端资料解析回归，并用网页端与移动端 fixture 生成报告。

## 运行边界

- 不处理豆包登录、验证码、人机校验、账号风控或平台限制绕过。
- Android/Appium 只做低频 UI 证据采集，不做逆向 API、抓包、账号池、自动注册或高频并发。
- 概率指标是重复采样估计，不是真实市场份额或平台官方排名。
- 引用资料 URL 依赖豆包 UI 可见入口；拿不到 URL 时保留截图/XML 并标记低置信度。

## 包路径

- Skill package: [skills/yao-doubao-crawler](../../skills/yao-doubao-crawler)
