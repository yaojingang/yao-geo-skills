# 采集 JSON 格式

JSON 文件与 `evidence/` 文件夹同级；截图路径相对于 JSON 文件。每个不同检索词只出现一次。`depth` 为 0（词根）或 1（第一层词）。第二层建议词只记录在第一层词的 `suggestions` 内，无须再查询。建议词 `rank` 从 1 开始，按页面垂直顺序排列。查询记录必须及时落盘，以便中断后恢复。

```json
{
  "platform": "xiaohongshu",
  "industry": "study_abroad",
  "conversion_goal": "咨询或委托留学服务机构",
  "roots": ["留学公司"],
  "queries": [
    {
      "query": "留学公司",
      "depth": 0,
      "status": "ok",
      "captured_at": "2026-09-29T10:00:00+08:00",
      "page_url": "https://www.xiaohongshu.com/",
      "screenshots": ["evidence/001-root.png"],
      "suggestions": [
        {"term": "留学公司布置", "rank": 1},
        {"term": "留学公司咨询", "rank": 2}
      ]
    },
    {
      "query": "留学公司咨询",
      "depth": 1,
      "status": "ok",
      "captured_at": "2026-09-29T10:01:00+08:00",
      "page_url": "https://www.xiaohongshu.com/search_result?keyword=留学公司咨询",
      "screenshots": ["evidence/002-child.png"],
      "suggestions": [
        {"term": "留学公司咨询顾问", "rank": 1}
      ]
    }
  ]
}
```

上例只示范格式，词条来自用户截图，不能作为新采集结果使用。`industry` 和 `conversion_goal` 必须与评分画像一致。非 `ok` 状态的 `suggestions` 必须为空。`ok` 状态必须包含至少一条建议词和一张实际截图；`empty` 必须附证明空白下拉的截图。`blocked` 与 `error` 在 `note` 写明原因。非 `pending` 项应记录 ISO 8601 采集时间；实际访问过的 `ok` 和 `empty` 项应记录页面 URL。尚未查询的词可不列入 `queries`，导出程序会列入“待采集”；受阻和报错的词也会列入该表。
