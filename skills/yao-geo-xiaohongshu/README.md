# yao-geo-xiaohongshu

小红书顶部搜索框联想词两层采集 Skill。输入词根后，依次查询词根及第一层建议词，保存每次的真实截图、列表位置和查询路径，按行业商业意图评分并导出 Excel。

## 使用

将本目录作为 Codex Skill 安装，然后提出例如“采集小红书词根‘留学公司’的两层相关词，按留学服务意图评分”。执行者通过可用浏览器工具逐词操作。需遵守小红书页面访问状态；登录或验证由用户处理。

采集完成后运行：

```bash
python3 scripts/build_workbook.py --input capture.json --output 小红书关键词表.xlsx --industry study_abroad
```

Excel 包含“关键词表”“采集记录”“截图索引”“去重词库”“待采集”五张表。关键词表 F 列为 1–10 分商业价值。采集 JSON 格式见 `references/data-contract.md`。浏览器采集规程见 `references/browser-capture.md`。

## 依赖

`python3 -m pip install -r requirements.txt`
