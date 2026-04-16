# Output File Workflow

## Goal

当用户不只是要“方案文本”，而是要能直接打开、直接转交的交付件时，统一输出：

- `.html`
- `.docx`

## Rendering Flow

1. 先按证据和结论整理 `report_input.json`
2. 再运行：

```bash
python3 scripts/render_geo_tracking_plan.py \
  --input <report_input.json> \
  --output-dir <output-dir>
```

3. 默认生成两个文件：
   - `<slug>.html`
   - `<slug>.docx`

## Input Schema

最小结构如下：

```json
{
  "title": "报告标题",
  "subtitle": "副标题",
  "company_name": "公司名",
  "analysis_date": "YYYY-MM-DD",
  "prepared_by": "生成者",
  "slug": "output-file-name",
  "summary_cards": [
    {
      "label": "卡片标题",
      "value": "核心值",
      "note": "补充说明"
    }
  ],
  "sections": [
    {
      "title": "章节名",
      "paragraphs": ["段落1", "段落2"],
      "bullets": ["要点1", "要点2"],
      "flow": {
        "title": "流程图标题",
        "steps": [
          {
            "label": "阶段1",
            "title": "步骤标题",
            "note": "步骤说明"
          }
        ]
      },
      "allocation": {
        "title": "分配标题",
        "segments": [
          {
            "label": "Observed",
            "value": 35,
            "range": "30%~40%",
            "note": "说明"
          }
        ]
      },
      "table": {
        "headers": ["列1", "列2"],
        "rows": [["值1", "值2"]]
      }
    }
  ]
}
```

## Section Rules

- `paragraphs`、`bullets`、`flow`、`allocation`、`table` 都是可选
- `flow.steps` 适合表达 “AI 曝光 -> 承接 -> 识别 -> 归因 -> 复盘” 这类链路图示
- `allocation.segments` 适合表达 `Observed / Recoverable / Unobservable` 三层估算
- 如果 `allocation.segments.value` 使用百分比分配，建议合计为 `100`
- `table.headers` 与每行列数必须一致
- 内容里优先使用绝对日期
- 证据表优先包含：来源、更新时间、关键事实、用途

## Recommended Deliverable Sections

- 封面摘要
- 企业理解摘要
- 市场分层判断
- 公开证据表
- 官网核验
- 现状诊断
- 效果追踪方法与原理说明
- 直接效果追踪方案
- 间接效果追踪方案
- 监测效果边界说明
- 可观测性估算框架
- 归因口径与数据表设计
- 优先级路线图
- 置信度与缺口

## Demo

可直接参考：

- `examples/hubspot-demo/report_input.json`
- `examples/hubspot-demo/hubspot-geo-tracking-plan.html`
- `examples/hubspot-demo/hubspot-geo-tracking-plan.docx`
