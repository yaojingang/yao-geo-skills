# 百度相关搜索词采集 Skill

给 Codex 一组目标关键词后，技能会逐词打开百度，在浏览器里截取搜索框联想词和第一页底部“相关搜索”，按行业转化目标评分，整理为带截图出处的 Excel。

## 使用

将本文件夹放入 Codex 的 skills 目录并重启 Codex，然后发送：

> 用 $yao-geo-baidu-keywords 按法律服务行业采集“婚姻律师、离婚律师”的百度下拉词和页尾相关搜索，以推荐或委托律师为目标评分，生成 Excel。

也可直接附上关键词清单。截图和 Excel 会保存在同一个运行文件夹。`关键词表` 的 F 列为 1–10 分商业价值评分，`采集记录` 用于查看每个目标词的采集状态，`截图索引` 可逐张打开证据。评分画像包括法律服务、医疗服务、教育培训、留学服务、装修家居和商品零售；其他行业可按 [评分规程](references/scoring.md)提供自定义画像。

运行环境需要浏览器交互工具、Python 3.10+ 和 `openpyxl`（见 `requirements.txt`）。浏览器负责采集与截图，`scripts/build_workbook.py` 负责校验采集 JSON、按行业评分并生成 Excel。遇到验证码时由用户处理。

已有采集 JSON 可直接重新生成带评分的工作簿：

```bash
python3 scripts/build_workbook.py --input /path/to/run/capture.json --output /path/to/run/关键词表_评分.xlsx --industry legal
```

输入 JSON 和输出 Excel 应在同一运行文件夹，以保持截图相对链接可用。不同转化目标用 `--profile /path/to/profile.json`。

## 公开案例

[出国留学相关搜索关键词表（公开示例）](examples/study-abroad/出国留学相关搜索关键词表_公开示例.xlsx)收录 5 个目标词、98 条相关词，展示留学服务行业的商业价值评分。公开版保留词条、来源、评分、采集状态和规范化搜索链接；原始浏览器截图未随仓库发布，截图列已清空。说明见[案例说明](examples/study-abroad/README.md)。

## 文件

- `SKILL.md`：触发条件、核心操作和交付约定
- `references/browser-capture.md`：页面采集与截图细则
- `references/data-contract.md`：采集 JSON 结构
- `references/scoring.md`、`references/industry-profiles.json`：行业选择、评分规则和自定义画像
- `scripts/build_workbook.py`：Excel 生成脚本
- `scripts/score_keywords.py`：行业评分逻辑
- `scripts/check_scoring.py`、`scripts/check_workbook.py`：回归检查
- `reports/`：输出风险与交付检查
