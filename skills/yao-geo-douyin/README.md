# yao-geo-douyin

通过抖音网页版顶部搜索框采集两层下拉联想词。输入词根得到一级词，再逐个输入不同一级词得到二级词；逐次截图、记录排序和来源路径，按行业转化目标评分并生成Excel采集包。

沿用参考仓库的 [MIT许可证](LICENSE)。

采集循环固定在当前网页，只聚焦输入框、替换文字、观察与截图。无需提交搜索，不点击建议词或视频、不刷新页面。输入联想会产生平台请求，仍可能遇到登录或验证限制，受阻后保存检查点并停止。

## 使用

将压缩包中的 `yao-geo-douyin/` 放入 `~/.codex/skills/`（自定义Codex目录时使用其 `skills/`），或让Agent直接读取本目录的 `SKILL.md`。安装后的入口为 `~/.codex/skills/yao-geo-douyin/SKILL.md`。在Codex中默认使用电脑操作能力控制已授权的Chrome抖音窗口，通过原生UI定位、编辑搜索框、读取状态并截图；包内脚本负责离线校验、行业评分及Excel导出。

示例请求：

> 使用 yao-geo-douyin，采集“GEO公司、GEO服务商”的两层抖音下拉联想词，按咨询或委托GEO服务的意图评分，输出Excel和截图采集包。

根词、行业及转化目标确认后，按 [浏览器规程](references/browser-capture.md) 逐词操作，按 [数据约定](references/data-contract.md) 写 `capture.json`。登录和验证码由用户在当前页面处理。

## 导出

Python 3.10+；依赖见 `requirements.txt`。优先复用环境已有依赖，缺失时执行：

```bash
python3 -m pip install -r requirements.txt
python3 scripts/build_workbook.py --input capture.json --output 抖音关键词表.xlsx --industry geo_services
```

其他行业使用 `legal`、`medical`、`education`、`study_abroad`、`renovation` 或 `ecommerce`。新行业通过 `--profile <行业画像.json>` 指定。根词的转化目标应从画像中取实际值，不能填另一种业务。

Excel包含五张表，关键词表F列为商业价值评分，保留一级路径、位置、时间、实际URL、截图链接及评分理由。空结果及报错在采集记录中保留，未完成项进入待采集表。Excel与JSON、`evidence/`同目录打包交付，解压后相对链接可用。

## 验证范围

本版复用小红书Skill的队列、来源路径和行业评分逻辑，并增加输入核对、URL保持一致和截图真实格式校验。

```bash
python3 scripts/check_scoring.py
python3 scripts/check_workbook.py
python3 scripts/check_review_regressions.py
```

截图链接按相对路径编码，兼容中文、空格与特殊字符；关键词以Excel文本类型存储，保留原文。跨系统危险路径、非法字符和超过单元格上限的汇总文本会在导出时拒绝，已有文件保持完整。

2026-10-01已在登录后的macOS Chrome精选页完成“GEO公司”的两层实采：11次不同查询、110条路径记录、80个原文精确去重词、11张截图。原生输入异常会被完整值核对拦截；可通过完整填入和末尾键盘编辑触发稳定下拉。详见 [实测报告](reports/live-test-2026-10-01.md)、[详细复核报告](reports/detailed-review-2026-09-30.md) 和 [创建记录](reports/review-2026-09-30.md)。实测范围为这一会话；其他系统与大批量运行继续按浏览器规程验证。
