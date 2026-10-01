# 示例与公开边界

本Skill已在macOS Chrome抖音精选页，以“GEO公司”完成一根两层采集：11次不同查询、110条来源路径记录、80个原文精确去重词、11张截图。范围见[实测报告](../reports/live-test-2026-10-01.md)。

已登录浏览器原始截图、账户界面和完整真实采集包保存在用户本地。仓库提供可运行的合成校验样例，验证两层路径、行业评分、截图归属和Excel输出；合成样例不表示抖音真实搜索结果。

```bash
python3 scripts/check_scoring.py
python3 scripts/check_workbook.py
python3 scripts/check_review_regressions.py
```

以上命令从Skill目录执行。完整运行需可用的Codex电脑操作能力和用户授权的抖音窗口；离线评分与导出使用已有采集JSON和截图。
