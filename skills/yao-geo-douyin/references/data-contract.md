# 采集检查点

JSON、Excel和 `evidence/` 放同一目录。示例是格式说明，建议词为合成内容，不能充作实采证据。

相对路径基于调用方传入JSON路径的父目录；JSON文件本身为符号链接时仍使用该访问目录。Excel必须写入同一目录。

```json
{
  "platform": "douyin",
  "capture_mode": "input_only",
  "industry": "study_abroad",
  "conversion_goal": "咨询或委托留学服务机构进行申请规划与办理",
  "roots": ["留学公司"],
  "queries": [
    {
      "query": "留学公司",
      "depth": 0,
      "status": "ok",
      "observed_input": "留学公司",
      "captured_at": "2026-09-30T21:00:00+08:00",
      "page_url_before": "https://www.douyin.com/jingxuan",
      "page_url": "https://www.douyin.com/jingxuan",
      "screenshots": ["evidence/001-root.jpg"],
      "suggestions": [{"term": "留学公司咨询", "rank": 1}],
      "list_truncated": false,
      "note": "合成格式示例"
    }
  ]
}
```

- `depth:0` 为根词，`depth:1` 为不同一级词的检索；二级词只记录在其查询的 `suggestions` 中。检索词精确去重，根词兼作一级词时复用。
- 非根查询必须出现在本批次某根词的一级建议中；其他批次数据需另存JSON，不能混入当前检查点。
- 状态 `ok` 有建议词及真实截图，`empty` 有确认空列表截图及非空 `empty_confirmation`。两者需核对 `observed_input`，记录输入前后相同的抖音HTTPS URL和时区明确的ISO8601时间。截图路径必须位于当前包内，文件后缀匹配PNG/JPEG/WebP实际字节。
- `blocked` / `error` 的建议词为空，`note` 说明原因，可附受阻截图；`pending` 尚未输入，不必填时间URL。不能把浏览器故障、加载未确认或登录遮挡记为空结果。
- `rank` 从1开始按视觉排列，不能重复位置；实际相同词的不同位置仍保留。默认只收前10个可见建议，超过限制或视口未覆盖时标 `list_truncated:true` 并写 `note`。
- 每条建议可用 `screenshot` 指向该查询 `screenshots` 中能证明该行的图片；单张图可省略，多张图必须逐条填写。`./evidence/a.png` 与 `evidence/a.png` 规范化后视为同一路径。Excel关键词行链接对应图片，截图索引保留所有图片。
- 截图路径用 `/` 分隔，须为包内相对路径；拒绝反斜线、驱动器/网络路径、冒号、控制字符、Windows非法或保留文件名、以空格或点结尾的分段及上级目录。中文、内部空格、`#`、`%` 可保留，Excel链接会按URI规则编码，单元格显示实际文件路径。
- 不同检索使用不同截图文件，禁止复用或覆盖其他检索的证据；硬链接、符号链接及大小写别名均按实际文件归属核对。词条以文本类型保留原文，`= + - @` 开头的文本不生成公式、不插入额外字符。
- 所有Excel文本单元格最多32767字符，包括拼接的根词、备注及截图汇总；拒绝XML不支持的控制字符、孤立代理字符和U+FFFE/U+FFFF。超长或非法内容明确报错，拆分批次或核对原始记录后重导出，禁止静默截断或改写。导出失败不会替换已有Excel。
- 图片须可完整解码，尺寸最多5000万像素；签名或后缀正确但内容损坏时拒绝导出。
- 写检查点前先保存截图，JSON用同目录临时文件写入后替换，避免中断损坏。恢复时更新原查询记录。
- 导出会拒绝非抖音URL、输入核对不一致、URL发生变化的成功记录、重复查询、越界截图路径、错扩展名及行业目标不一致；发现问题先修复原始记录，禁止用虚构字段补过校验。
