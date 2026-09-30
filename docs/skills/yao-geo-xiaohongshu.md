# yao-geo-xiaohongshu

在已授权的真实浏览器中输入一个或多个词根，采集小红书顶部搜索框的联想词；再把第一层词逐个输入，获得第二层词。每次保存下拉截图，记录词条的展示位置与来源路径，并根据行业转化目标生成商业价值评分和 Excel。

## 适用场景

- 从词根扩展小红书相关搜索词，保留第一层与第二层的关系。
- 比较同一行业内不同建议词的服务咨询或购买意图。
- 需要截图证据、展示位置和可筛选关键词表的 GEO 研究。

查笔记内容、话题热度、账号数据或搜索量时不使用本 Skill。评分仅代表相对商业意图，不代表搜索量、投放报价或实际成交。

## 输入与输出

输入词根、行业和转化目标；未覆盖的行业提供自定义评分画像。跨行业任务分批运行。完整采集包包含同目录下的 `capture.json`、`evidence/` 截图和 Excel 工作簿。Excel 包含“关键词表”“采集记录”“截图索引”“去重词库”“待采集”；F 列为 1–10 分数值评分。登录和验证码由用户处理，受阻词保留状态。

安装 `openpyxl` 后可从已有 JSON 重新导出工作簿：

```bash
python3 scripts/build_workbook.py --input /path/to/run/capture.json --output /path/to/run/关键词表.xlsx --industry study_abroad
```

运行检查：

```bash
python3 scripts/check_scoring.py
python3 scripts/check_workbook.py
```

## 公开示例

[示例与隐私边界](../../skills/yao-geo-xiaohongshu/examples/README.md)。已登录页面截图仅保存在用户自己的采集包中；仓库中的合成测试样例不代表真实搜索结果。
