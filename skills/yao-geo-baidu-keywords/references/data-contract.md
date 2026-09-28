# 采集数据结构

JSON 文件使用 UTF-8，放在本次运行文件夹，截图路径相对该文件夹。

```json
{
  "industry": "legal",
  "conversion_goal": "推荐、咨询或委托律师与律所",
  "items": [
    {
      "seed": "婚姻律师",
      "captured_at": "2026-09-28T18:30:00+08:00",
      "search_url": "https://www.baidu.com/s?wd=...",
      "autocomplete": {
        "status": "ok",
        "screenshots": ["evidence/001-autocomplete.png"],
        "terms": ["婚姻律师事务所", "婚姻律师咨询免费"]
      },
      "bottom": {
        "status": "ok",
        "screenshots": ["evidence/001-bottom.png"],
        "terms": ["婚姻律师事务所", "一般离婚律师怎么收费"]
      }
    }
  ]
}
```

`status` 可取 `ok`、`empty`、`blocked`、`error`。`ok` 必须有至少一条词和截图；其他状态的 `terms` 应为空数组。每个目标词都要有两类区块。`captured_at` 必须包含时区。采集到页尾相关搜索时必须记录实际结果页 URL。截图文件须存在。可用文本型 `note` 记录页面异常。

`industry` 推荐写入运行文件；旧数据可在生成 Excel 时通过 `--industry` 指定。`conversion_goal` 若填写，必须与所选内置或自定义评分画像一致。行业未知时先确认；不要静默使用通用画像。

Excel 中的“关键词表”每个目标词与相关词组合占一行，重复出现在两种来源时合并为一行，序号记录同一来源中首次出现的位置；不同目标词之间不合并。F 列为数值型“商业价值评分（10分）”。“采集记录”按目标词列出状态和数量，便于核对缺失项。“截图索引”逐张列出证据并提供链接；主表和采集记录的截图单元格列出所有路径，点击时打开第一张。词条保留页面原词，仅去除首尾和多余空白；不要改写含义。
