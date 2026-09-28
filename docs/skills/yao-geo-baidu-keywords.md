# yao-geo-baidu-keywords

在真实浏览器中逐个检索百度目标词，采集搜索框联想词和第一页主结果区页尾“相关搜索”，保存两处截图，再根据所属行业与转化目标给相关词评 1–10 分，生成 Excel 关键词表。

## 适用场景

- 从一批核心词扩展百度相关搜索词，并保留页面证据。
- 比较同一行业内不同词的商业转化意图，例如留学服务中的“出国留学机构”与“出国留学费用”。
- 将分批采集的结果整理成可筛选、可追溯的关键词表。

仅查询百度指数、热搜榜、普通网页链接或广告竞价时，不使用本 skill。评分判断搜索意图，不推断搜索量、竞价或实际成交额。

## 输入与输出

输入为目标关键词、行业和转化目标。可直接粘贴词表，也可提供文本或表格。跨行业任务按行业分批评分。

完整运行输出 `capture.json`、`evidence/` 截图和 Excel 工作簿，三者放在同一目录。工作簿包含“关键词表”“采集记录”“截图索引”；关键词表 F 列是数值型商业价值评分。页面缺失的区块保留空值并记录状态。验证码由用户处理。

已有采集 JSON 可在安装 `openpyxl` 后重新生成工作簿：

```bash
python3 scripts/build_workbook.py --input /path/to/run/capture.json --output /path/to/run/关键词表.xlsx --industry study_abroad
```

## 公开案例

- [留学服务 Excel 公开示例](../../skills/yao-geo-baidu-keywords/examples/study-abroad/出国留学相关搜索关键词表_公开示例.xlsx)
- [案例数据与隐私处理说明](../../skills/yao-geo-baidu-keywords/examples/study-abroad/README.md)

示例覆盖 5 个目标词、98 条相关词。公开版移除了浏览器个人界面截图和截图超链接；完整运行仍应保留截图证据。

## 质量检查

```bash
python3 scripts/check_scoring.py
python3 scripts/check_workbook.py
```

浏览器采集必须由可用的浏览器交互工具完成。截图文件、词条顺序、来源和搜索结果页 URL 应来自实际页面。运行环境没有浏览器交互或截图保存能力时，应说明未完成部分。
