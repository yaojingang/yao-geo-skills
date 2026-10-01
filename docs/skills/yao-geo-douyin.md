# yao-geo-douyin

默认通过Codex电脑操作能力控制已授权的Chrome抖音窗口，在顶部搜索框原生输入词根，采集第一层下拉联想词；再逐个输入不同的一级词，获取第二层。逐词截图、记录视觉位置与来源路径，按行业转化目标评分并生成Excel采集包。

## 适用场景

- 核心词扩展、两层搜索意图研究和行业关键词商业价值初筛。
- 需要保留原文、展示位置、真实截图和采集时间的GEO研究。
- 通过已有JSON和截图重新评分、导出可筛选关键词表。

视频、评论、账号、热榜及搜索量查询另行使用对应工具。商业价值分数用于当前行业的相对意图判断，不代表成交概率、搜索量或竞价。

## 使用

将[Skill包](../../skills/yao-geo-douyin)放入Codex的skills目录，准备[输入简报](../../skills/yao-geo-douyin/templates/brief-template.md)，在Chrome打开并登录抖音网页版。

> 使用yao-geo-douyin，采集“GEO公司、GEO服务商”的两层抖音下拉联想词，按咨询或委托GEO优化服务的意图评分，输出Excel和截图采集包。

每次核对完整输入及稳定的新列表，截图包含搜索框与采集行。采集循环仅聚焦、输入、观察和截图，不点击、不提交搜索、不刷新。输入联想仍会产生平台请求；登录、验证码和频率限制由用户处理，受阻后保存检查点并停止。

## 输入与输出

输入词根、行业和转化目标；未覆盖行业提供自定义画像，跨行业分批运行。默认最多200个不同查询，每次最多10条可见建议；仅扩展到第二层，保留未完成范围。

采集包包含同目录的capture.json、evidence/和Excel。工作簿含“关键词表”“采集记录”“截图索引”“去重词库”“待采集”，F列为1–10分商业价值评分，并附理由、时间、位置、实际URL与截图链接。

从已有采集包导出：

```bash
python3 -m pip install -r requirements.txt
python3 scripts/build_workbook.py --input /path/to/run/capture.json --output /path/to/run/关键词表.xlsx --industry geo_services
```

命令从Skill目录执行。七个内置行业画像覆盖法律、医疗、教育、留学、装修、电商和GEO服务；新行业通过--profile指定。网页操作由Codex电脑操作能力完成，脚本负责离线整理、评分和导出。

## 验证与公开示例

macOS Chrome的“GEO公司”实测完成11次不同查询、110条路径记录、80个去重词和11张截图，循环未鼠标点击、提交搜索或刷新。已登录页面的原始截图与真实采集包保留在用户本地，公开包提供合成校验样例。

- [实测范围](../../skills/yao-geo-douyin/reports/live-test-2026-10-01.md)
- [示例与隐私边界](../../skills/yao-geo-douyin/examples/README.md)
- [浏览器规程](../../skills/yao-geo-douyin/references/browser-capture.md)
- [评分说明](../../skills/yao-geo-douyin/references/scoring.md)

运行scripts/check_scoring.py、scripts/check_workbook.py及scripts/check_review_regressions.py检查评分和输出契约。其他系统、未来页面与大批量连续运行按实际状态验证。
