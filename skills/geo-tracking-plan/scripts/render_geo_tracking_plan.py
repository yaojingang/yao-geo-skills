#!/usr/bin/env python3
"""Render GEO tracking plan reports to HTML and DOCX."""

from __future__ import annotations

import argparse
import datetime as dt
import html
import json
import re
import zipfile
from pathlib import Path
from typing import Any
from xml.sax.saxutils import escape as xml_escape


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Render GEO tracking plan report.")
    parser.add_argument("--input", required=True, help="Path to normalized report input JSON.")
    parser.add_argument(
        "--output-dir",
        required=True,
        help="Directory where the HTML and DOCX outputs should be written.",
    )
    return parser.parse_args()


def load_input(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    required = ["title", "company_name", "analysis_date", "summary_cards", "sections"]
    missing = [key for key in required if key not in data]
    if missing:
        raise ValueError(f"Missing required input keys: {', '.join(missing)}")
    return data


def slugify(value: str) -> str:
    lowered = value.lower().strip()
    lowered = re.sub(r"[^a-z0-9]+", "-", lowered)
    lowered = re.sub(r"-{2,}", "-", lowered)
    return lowered.strip("-") or "geo-tracking-plan"


def render_html(data: dict[str, Any]) -> str:
    title = html.escape(data["title"])
    subtitle = html.escape(data.get("subtitle", ""))
    company = html.escape(data["company_name"])
    analysis_date = html.escape(data["analysis_date"])
    prepared_by = html.escape(data.get("prepared_by", "geo-tracking-plan"))

    cards_html = []
    for card in data["summary_cards"]:
        cards_html.append(
            f"""
            <article class="summary-card">
              <p class="summary-label">{html.escape(card['label'])}</p>
              <p class="summary-value">{html.escape(card['value'])}</p>
              <p class="summary-note">{html.escape(card.get('note', ''))}</p>
            </article>
            """.strip()
        )

    sections_html = []
    nav_links = []
    for index, section in enumerate(data["sections"], start=1):
        section_id = html.escape(section.get("id", f"section-{index}"))
        section_title = html.escape(section["title"])
        section_number = f"{index:02d}"
        nav_links.append(
            """
            <a class="nav-chip" href="#{section_id}">
              <span class="nav-chip-index">{section_number}</span>
              <span class="nav-chip-label">{section_title}</span>
            </a>
            """.format(
                section_id=section_id,
                section_number=section_number,
                section_title=section_title,
            ).strip()
        )
        parts = [
            f"<section class=\"report-section\" id=\"{section_id}\">"
            "<div class=\"section-head\">"
            "<div class=\"section-heading\">"
            f"<p class=\"section-kicker\">Module {section_number}</p>"
            f"<h2>{section_title}</h2>"
            "</div>"
            f"<a class=\"section-anchor\" href=\"#{section_id}\">#{section_number}</a>"
            "</div>"
        ]
        for paragraph in section.get("paragraphs", []):
            parts.append(f"<p>{html.escape(paragraph)}</p>")
        if section.get("callout"):
            parts.append(f"<aside class=\"callout\">{html.escape(section['callout'])}</aside>")
        if section.get("bullets"):
            bullets = "\n".join(f"<li>{html.escape(item)}</li>" for item in section["bullets"])
            parts.append(f"<ul>{bullets}</ul>")
        if section.get("flow"):
            parts.append(render_flow_html(section["flow"]))
        if section.get("allocation"):
            parts.append(render_allocation_html(section["allocation"]))
        if section.get("table"):
            headers = "".join(
                f"<th>{html.escape(header)}</th>" for header in section["table"]["headers"]
            )
            rows = []
            for row in section["table"]["rows"]:
                row_html = "".join(f"<td>{format_html_cell(cell)}</td>" for cell in row)
                rows.append(f"<tr>{row_html}</tr>")
            parts.append(
                "<div class=\"table-wrap\"><table>"
                f"<thead><tr>{headers}</tr></thead>"
                f"<tbody>{''.join(rows)}</tbody>"
                "</table></div>"
            )
        parts.append("</section>")
        sections_html.append("\n".join(parts))

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <style>
    :root {{
      --font-sans: "IBM Plex Sans", "Source Han Sans SC", "PingFang SC", "Microsoft YaHei", sans-serif;
      --font-serif: "IBM Plex Serif", "Songti SC", Georgia, serif;
      --ink: #16202a;
      --muted: #5a6b7c;
      --line: #d7e0e8;
      --line-strong: #b9c6d2;
      --bg: #edf2f5;
      --panel: rgba(255, 255, 255, 0.86);
      --panel-strong: #ffffff;
      --panel-muted: #f7fafc;
      --accent: #ae5630;
      --accent-soft: #f8e1d5;
      --accent-alt: #1f5a73;
      --success: #557a46;
      --navy-soft: #eef4f7;
      --shadow: 0 18px 42px rgba(22, 32, 42, 0.08);
      --shadow-soft: 0 10px 24px rgba(22, 32, 42, 0.05);
    }}

    * {{
      box-sizing: border-box;
    }}

    body {{
      margin: 0;
      font-family: var(--font-sans);
      color: var(--ink);
      background:
        linear-gradient(180deg, rgba(255, 255, 255, 0.7), rgba(255, 255, 255, 0)) 0 0 / 100% 140px no-repeat,
        radial-gradient(circle at top left, rgba(174, 86, 48, 0.12), transparent 26%),
        radial-gradient(circle at top right, rgba(31, 90, 115, 0.1), transparent 24%),
        linear-gradient(180deg, #f6f8fa 0%, var(--bg) 100%);
      line-height: 1.7;
    }}

    .page {{
      width: min(1240px, calc(100vw - 36px));
      margin: 22px auto 72px;
    }}

    .hero {{
      background:
        linear-gradient(180deg, rgba(255, 255, 255, 0.98), rgba(250, 252, 253, 0.96)),
        linear-gradient(120deg, rgba(174, 86, 48, 0.04), rgba(31, 90, 115, 0.04));
      border: 1px solid rgba(22, 32, 42, 0.08);
      border-radius: 32px;
      box-shadow: var(--shadow);
      padding: 40px 42px 30px;
      position: relative;
      overflow: hidden;
    }}

    .hero::after {{
      content: "";
      position: absolute;
      inset: 0 auto auto 0;
      width: 100%;
      height: 5px;
      background: linear-gradient(90deg, var(--accent-alt), var(--accent), var(--success));
    }}

    .eyebrow {{
      letter-spacing: 0.12em;
      text-transform: uppercase;
      font-size: 12px;
      color: var(--accent-alt);
      margin: 0 0 12px;
    }}

    h1 {{
      font-family: var(--font-serif);
      font-size: clamp(34px, 4vw, 52px);
      line-height: 1.08;
      margin: 0 0 14px;
      max-width: 880px;
    }}

    .subtitle {{
      font-size: 17px;
      color: var(--muted);
      margin: 0 0 20px;
      max-width: 840px;
    }}

    .meta {{
      display: flex;
      flex-wrap: wrap;
      gap: 12px;
      color: var(--muted);
      font-size: 14px;
    }}

    .meta span {{
      padding: 7px 12px;
      border: 1px solid rgba(31, 90, 115, 0.16);
      border-radius: 999px;
      background: rgba(247, 250, 252, 0.92);
    }}

    .summary-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
      gap: 18px;
      margin-top: 24px;
    }}

    .summary-card {{
      position: relative;
      background: var(--panel);
      border: 1px solid rgba(22, 32, 42, 0.08);
      border-radius: 22px;
      padding: 20px 20px 18px;
      min-height: 170px;
      backdrop-filter: blur(10px);
    }}

    .summary-card::before {{
      content: "";
      position: absolute;
      inset: 0 auto auto 0;
      width: 100%;
      height: 4px;
      background: linear-gradient(90deg, rgba(31, 90, 115, 0.8), rgba(174, 86, 48, 0.7));
    }}

    .summary-label {{
      margin: 0 0 10px;
      font-size: 12px;
      font-weight: 700;
      letter-spacing: 0.12em;
      text-transform: uppercase;
      color: var(--accent-alt);
    }}

    .summary-value {{
      margin: 0 0 10px;
      font-family: var(--font-serif);
      font-size: 30px;
      line-height: 1.15;
    }}

    .summary-note {{
      margin: 0;
      color: var(--muted);
      font-size: 14px;
    }}

    .report-nav {{
      margin-top: 18px;
      background: rgba(255, 255, 255, 0.9);
      border: 1px solid rgba(22, 32, 42, 0.08);
      border-radius: 24px;
      padding: 18px 20px 20px;
      box-shadow: var(--shadow-soft);
      backdrop-filter: blur(10px);
    }}

    .report-nav-head {{
      display: flex;
      flex-wrap: wrap;
      gap: 10px 18px;
      align-items: baseline;
      margin-bottom: 14px;
    }}

    .report-nav-title {{
      margin: 0;
      font-size: 13px;
      font-weight: 700;
      letter-spacing: 0.12em;
      text-transform: uppercase;
      color: var(--accent-alt);
    }}

    .report-nav-note {{
      margin: 0;
      color: var(--muted);
      font-size: 13px;
    }}

    .report-nav-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
      gap: 12px;
    }}

    .nav-chip {{
      display: flex;
      gap: 12px;
      align-items: flex-start;
      padding: 13px 14px;
      border-radius: 18px;
      border: 1px solid rgba(22, 32, 42, 0.08);
      background: var(--panel-muted);
      color: inherit;
      text-decoration: none;
      transition: transform 120ms ease, border-color 120ms ease, box-shadow 120ms ease;
    }}

    .nav-chip:hover {{
      transform: translateY(-1px);
      border-color: rgba(31, 90, 115, 0.26);
      box-shadow: 0 10px 20px rgba(22, 32, 42, 0.06);
      text-decoration: none;
    }}

    .nav-chip-index {{
      flex: 0 0 auto;
      min-width: 34px;
      padding: 5px 0;
      border-radius: 999px;
      background: rgba(31, 90, 115, 0.1);
      color: var(--accent-alt);
      font-size: 12px;
      font-weight: 700;
      text-align: center;
    }}

    .nav-chip-label {{
      font-size: 14px;
      font-weight: 600;
      line-height: 1.45;
    }}

    .report-section {{
      margin-top: 26px;
      background: var(--panel-strong);
      border: 1px solid rgba(22, 32, 42, 0.08);
      border-radius: 24px;
      padding: 28px 30px;
      box-shadow: var(--shadow-soft);
    }}

    .section-head {{
      display: flex;
      gap: 16px;
      justify-content: space-between;
      align-items: flex-start;
      margin-bottom: 16px;
      padding-bottom: 14px;
      border-bottom: 1px solid var(--line);
    }}

    .section-heading {{
      min-width: 0;
    }}

    .section-kicker {{
      margin: 0 0 8px;
      font-size: 12px;
      font-weight: 700;
      letter-spacing: 0.14em;
      text-transform: uppercase;
      color: var(--accent-alt);
    }}

    .section-anchor {{
      flex: 0 0 auto;
      padding: 7px 10px;
      border-radius: 999px;
      border: 1px solid rgba(22, 32, 42, 0.08);
      background: var(--navy-soft);
      color: var(--muted);
      font-size: 12px;
      font-weight: 700;
      text-decoration: none;
    }}

    .section-anchor:hover {{
      color: var(--accent-alt);
      text-decoration: none;
    }}

    .report-section h2 {{
      margin: 0;
      font-family: var(--font-serif);
      font-size: 28px;
      line-height: 1.2;
    }}

    .report-section p,
    .report-section li {{
      font-size: 15px;
    }}

    .report-section ul {{
      margin: 12px 0 0 1.2em;
      padding: 0;
    }}

    .callout {{
      margin: 16px 0;
      border-left: 4px solid var(--accent-alt);
      background: linear-gradient(180deg, rgba(239, 246, 249, 0.96), rgba(248, 250, 251, 0.98));
      padding: 16px 18px 16px 20px;
      border-radius: 14px;
      font-weight: 600;
    }}

    .table-wrap {{
      overflow-x: auto;
      margin-top: 16px;
      border-radius: 18px;
      border: 1px solid var(--line);
      background: white;
      box-shadow: inset 0 0 0 1px rgba(22, 32, 42, 0.02);
    }}

    .flow-block {{
      margin-top: 18px;
      padding: 18px;
      border: 1px solid rgba(31, 90, 115, 0.14);
      border-radius: 20px;
      background: linear-gradient(180deg, rgba(247, 249, 252, 0.96), rgba(255, 255, 255, 0.98));
    }}

    .flow-title {{
      margin: 0 0 14px;
      font-size: 14px;
      font-weight: 700;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      color: var(--accent-alt);
    }}

    .flow-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(170px, 1fr));
      gap: 14px;
      align-items: stretch;
    }}

    .flow-step {{
      position: relative;
      padding: 16px 16px 14px;
      border-radius: 18px;
      background: white;
      border: 1px solid rgba(28, 36, 49, 0.08);
      box-shadow: 0 8px 18px rgba(28, 36, 49, 0.05);
    }}

    .flow-step::after {{
      content: "→";
      position: absolute;
      right: -12px;
      top: 50%;
      transform: translateY(-50%);
      color: rgba(31, 90, 115, 0.45);
      font-size: 18px;
      font-weight: 700;
    }}

    .flow-step:last-child::after {{
      display: none;
    }}

    .flow-label {{
      margin: 0 0 8px;
      font-size: 11px;
      font-weight: 700;
      letter-spacing: 0.12em;
      text-transform: uppercase;
      color: var(--accent);
    }}

    .flow-step-title {{
      margin: 0 0 8px;
      font-family: Georgia, "Songti SC", serif;
      font-size: 21px;
      line-height: 1.2;
    }}

    .flow-step-note {{
      margin: 0;
      color: var(--muted);
      font-size: 13px;
      line-height: 1.6;
    }}

    .allocation-block {{
      margin-top: 18px;
      padding: 18px;
      border-radius: 20px;
      border: 1px solid rgba(28, 36, 49, 0.08);
      background: linear-gradient(180deg, rgba(255, 255, 255, 0.98), rgba(247, 245, 241, 0.96));
    }}

    .allocation-title {{
      margin: 0 0 14px;
      font-size: 14px;
      font-weight: 700;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      color: var(--accent-alt);
    }}

    .allocation-bar {{
      display: flex;
      min-height: 24px;
      overflow: hidden;
      border-radius: 999px;
      background: #e7edf3;
      box-shadow: inset 0 0 0 1px rgba(28, 36, 49, 0.06);
    }}

    .allocation-segment {{
      display: flex;
      align-items: center;
      justify-content: center;
      color: white;
      font-size: 12px;
      font-weight: 700;
      letter-spacing: 0.04em;
      min-width: 52px;
      padding: 0 8px;
      white-space: nowrap;
    }}

    .allocation-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
      gap: 14px;
      margin-top: 14px;
    }}

    .allocation-card {{
      border-radius: 18px;
      background: white;
      border: 1px solid rgba(28, 36, 49, 0.08);
      padding: 14px 15px;
      box-shadow: 0 8px 18px rgba(28, 36, 49, 0.05);
    }}

    .allocation-card-label {{
      margin: 0 0 8px;
      font-size: 12px;
      font-weight: 700;
      letter-spacing: 0.1em;
      text-transform: uppercase;
    }}

    .allocation-card-value {{
      margin: 0 0 6px;
      font-family: Georgia, "Songti SC", serif;
      font-size: 28px;
      line-height: 1.1;
    }}

    .allocation-card-range {{
      margin: 0 0 8px;
      color: var(--muted);
      font-size: 13px;
    }}

    .allocation-card-note {{
      margin: 0;
      color: var(--muted);
      font-size: 13px;
      line-height: 1.6;
    }}

    table {{
      width: 100%;
      border-collapse: collapse;
      min-width: 680px;
      background: white;
    }}

    thead {{
      background: linear-gradient(135deg, #203345, #365671);
      color: white;
    }}

    th,
    td {{
      padding: 12px 14px;
      border-bottom: 1px solid var(--line);
      text-align: left;
      vertical-align: top;
      font-size: 14px;
    }}

    tbody tr:nth-child(even) {{
      background: #f8fbfd;
    }}

    a {{
      color: var(--accent-alt);
      text-decoration: none;
      word-break: break-all;
    }}

    a:hover {{
      text-decoration: underline;
    }}

    .footer {{
      margin-top: 26px;
      text-align: center;
      color: var(--muted);
      font-size: 13px;
    }}

    @media (max-width: 760px) {{
      .page {{
        width: min(100vw - 24px, 1160px);
        margin-top: 12px;
      }}

      .hero,
      .report-section,
      .report-nav {{
        padding: 22px 18px;
        border-radius: 20px;
      }}

      .section-head {{
        flex-direction: column;
      }}

      .flow-step::after {{
        display: none;
      }}
    }}
  </style>
</head>
<body>
  <main class="page">
    <header class="hero">
      <p class="eyebrow">GEO Tracking Plan</p>
      <h1>{title}</h1>
      <p class="subtitle">{subtitle}</p>
      <div class="meta">
        <span>公司：{company}</span>
        <span>分析日期：{analysis_date}</span>
        <span>生成方式：{prepared_by}</span>
      </div>
      <section class="summary-grid">
        {''.join(cards_html)}
      </section>
    </header>
    <section class="report-nav" aria-label="Report modules">
      <div class="report-nav-head">
        <p class="report-nav-title">Report Modules</p>
        <p class="report-nav-note">Design-system style navigation for quick scanning, review, and handoff.</p>
      </div>
      <div class="report-nav-grid">
        {''.join(nav_links)}
      </div>
    </section>
    {''.join(sections_html)}
    <p class="footer">Generated on {html.escape(dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))}</p>
  </main>
</body>
</html>
"""


def format_html_cell(cell: Any) -> str:
    text = str(cell)
    if text.startswith("http://") or text.startswith("https://"):
        safe = html.escape(text)
        return f"<a href=\"{safe}\">{safe}</a>"
    return html.escape(text)


def render_flow_html(flow: dict[str, Any]) -> str:
    title = html.escape(flow.get("title", "Process Flow"))
    step_html = []
    for step in flow.get("steps", []):
        step_html.append(
            """
            <article class="flow-step">
              <p class="flow-label">{label}</p>
              <h3 class="flow-step-title">{title}</h3>
              <p class="flow-step-note">{note}</p>
            </article>
            """.format(
                label=html.escape(step.get("label", "")),
                title=html.escape(step.get("title", "")),
                note=html.escape(step.get("note", "")),
            ).strip()
        )
    return (
        f"<div class=\"flow-block\"><p class=\"flow-title\">{title}</p>"
        f"<div class=\"flow-grid\">{''.join(step_html)}</div></div>"
    )


def render_allocation_html(allocation: dict[str, Any]) -> str:
    title = html.escape(allocation.get("title", "Allocation"))
    palette = ["#1f5a73", "#9c3d26", "#6c8b3c", "#7b5ea7"]
    segments = allocation.get("segments", [])
    numeric_values = [max(parse_numeric(segment.get("value")), 0.0) for segment in segments]
    total = sum(numeric_values) or 1.0

    bar_html = []
    card_html = []
    for index, segment in enumerate(segments):
        color = palette[index % len(palette)]
        value = numeric_values[index]
        width = max((value / total) * 100, 8 if value > 0 else 0)
        label = html.escape(str(segment.get("label", "")))
        value_text = html.escape(str(segment.get("value", "")))
        range_text = html.escape(str(segment.get("range", "")))
        note_text = html.escape(str(segment.get("note", "")))
        bar_html.append(
            f"<div class=\"allocation-segment\" style=\"background:{color};width:{width:.2f}%\">"
            f"{label} {value_text}%</div>"
        )
        card_html.append(
            f"""
            <article class="allocation-card">
              <p class="allocation-card-label" style="color:{color}">{label}</p>
              <p class="allocation-card-value">{value_text}%</p>
              <p class="allocation-card-range">建议区间：{range_text}</p>
              <p class="allocation-card-note">{note_text}</p>
            </article>
            """.strip()
        )

    return (
        f"<div class=\"allocation-block\"><p class=\"allocation-title\">{title}</p>"
        f"<div class=\"allocation-bar\">{''.join(bar_html)}</div>"
        f"<div class=\"allocation-grid\">{''.join(card_html)}</div></div>"
    )


def parse_numeric(value: Any) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def render_docx(data: dict[str, Any], output_path: Path) -> None:
    body = []
    body.append(paragraph_xml(data["title"], size=34, bold=True, align="center", after=180))
    if data.get("subtitle"):
        body.append(paragraph_xml(data["subtitle"], size=22, color="666666", align="center"))
    meta = (
        f"公司：{data['company_name']}    分析日期：{data['analysis_date']}    "
        f"生成方式：{data.get('prepared_by', 'geo-tracking-plan')}"
    )
    body.append(paragraph_xml(meta, size=18, color="666666", align="center", after=220))

    summary_headers = ["摘要卡片", "核心值", "补充说明"]
    summary_rows = [
        [card["label"], card["value"], card.get("note", "")]
        for card in data["summary_cards"]
    ]
    body.append(paragraph_xml("摘要卡片", size=26, bold=True, after=120))
    body.append(table_xml(summary_headers, summary_rows))

    for section in data["sections"]:
        body.append(paragraph_xml(section["title"], size=28, bold=True, after=120, before=180))
        for paragraph in section.get("paragraphs", []):
            body.append(paragraph_xml(paragraph, size=21))
        if section.get("callout"):
            body.append(paragraph_xml(f"提示：{section['callout']}", size=21, bold=True))
        for bullet in section.get("bullets", []):
            body.append(paragraph_xml(f"• {bullet}", size=21))
        if section.get("flow"):
            flow = section["flow"]
            flow_title = flow.get("title")
            if flow_title:
                body.append(paragraph_xml(flow_title, size=22, bold=True, after=100))
            flow_headers = ["阶段", "步骤", "说明"]
            flow_rows = [
                [step.get("label", ""), step.get("title", ""), step.get("note", "")]
                for step in flow.get("steps", [])
            ]
            if flow_rows:
                body.append(table_xml(flow_headers, flow_rows))
        if section.get("allocation"):
            allocation = section["allocation"]
            allocation_title = allocation.get("title")
            if allocation_title:
                body.append(paragraph_xml(allocation_title, size=22, bold=True, after=100))
            allocation_headers = ["层级", "规划值", "建议区间", "说明"]
            allocation_rows = [
                [
                    segment.get("label", ""),
                    f"{segment.get('value', '')}%",
                    segment.get("range", ""),
                    segment.get("note", ""),
                ]
                for segment in allocation.get("segments", [])
            ]
            if allocation_rows:
                body.append(table_xml(allocation_headers, allocation_rows))
        if section.get("table"):
            body.append(table_xml(section["table"]["headers"], section["table"]["rows"]))

    body.append(
        "<w:sectPr><w:pgSz w:w=\"11906\" w:h=\"16838\"/>"
        "<w:pgMar w:top=\"1134\" w:right=\"1134\" w:bottom=\"1134\" "
        "w:left=\"1134\" w:header=\"708\" w:footer=\"708\" w:gutter=\"0\"/>"
        "</w:sectPr>"
    )

    document_xml = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:wpc="http://schemas.microsoft.com/office/word/2010/wordprocessingCanvas"
 xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006"
 xmlns:o="urn:schemas-microsoft-com:office:office"
 xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
 xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"
 xmlns:v="urn:schemas-microsoft-com:vml"
 xmlns:wp14="http://schemas.microsoft.com/office/word/2010/wordprocessingDrawing"
 xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"
 xmlns:w10="urn:schemas-microsoft-com:office:word"
 xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"
 xmlns:w14="http://schemas.microsoft.com/office/word/2010/wordml"
 xmlns:wpg="http://schemas.microsoft.com/office/word/2010/wordprocessingGroup"
 xmlns:wpi="http://schemas.microsoft.com/office/word/2010/wordprocessingInk"
 xmlns:wne="http://schemas.microsoft.com/office/word/2006/wordml"
 xmlns:wps="http://schemas.microsoft.com/office/word/2010/wordprocessingShape"
 mc:Ignorable="w14 wp14">
  <w:body>
    {''.join(body)}
  </w:body>
</w:document>
"""

    content_types = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
  <Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
  <Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>
  <Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>
</Types>
"""

    package_rels = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>
  <Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/>
</Relationships>
"""

    document_rels = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
</Relationships>
"""

    styles_xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:style w:type="paragraph" w:default="1" w:styleId="Normal">
    <w:name w:val="Normal"/>
    <w:qFormat/>
  </w:style>
</w:styles>
"""

    now = (
        dt.datetime.now(dt.timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )
    core_xml = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties"
 xmlns:dc="http://purl.org/dc/elements/1.1/"
 xmlns:dcterms="http://purl.org/dc/terms/"
 xmlns:dcmitype="http://purl.org/dc/dcmitype/"
 xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <dc:title>{xml_escape(data["title"])}</dc:title>
  <dc:creator>{xml_escape(data.get("prepared_by", "geo-tracking-plan"))}</dc:creator>
  <cp:lastModifiedBy>{xml_escape(data.get("prepared_by", "geo-tracking-plan"))}</cp:lastModifiedBy>
  <dcterms:created xsi:type="dcterms:W3CDTF">{now}</dcterms:created>
  <dcterms:modified xsi:type="dcterms:W3CDTF">{now}</dcterms:modified>
</cp:coreProperties>
"""

    app_xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties"
 xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">
  <Application>Codex</Application>
</Properties>
"""

    with zipfile.ZipFile(output_path, "w", compression=zipfile.ZIP_DEFLATED) as docx:
        docx.writestr("[Content_Types].xml", content_types)
        docx.writestr("_rels/.rels", package_rels)
        docx.writestr("word/document.xml", document_xml)
        docx.writestr("word/_rels/document.xml.rels", document_rels)
        docx.writestr("word/styles.xml", styles_xml)
        docx.writestr("docProps/core.xml", core_xml)
        docx.writestr("docProps/app.xml", app_xml)


def paragraph_xml(
    text: str,
    *,
    size: int = 22,
    bold: bool = False,
    color: str | None = None,
    align: str | None = None,
    before: int = 0,
    after: int = 120,
) -> str:
    properties = [f'<w:spacing w:before="{before}" w:after="{after}"/>']
    if align:
        properties.append(f'<w:jc w:val="{align}"/>')
    run_props = [f'<w:sz w:val="{size * 2}"/>', f'<w:szCs w:val="{size * 2}"/>']
    if bold:
        run_props.append("<w:b/>")
    if color:
        run_props.append(f'<w:color w:val="{color}"/>')
    escaped = xml_escape(text)
    return (
        "<w:p>"
        f"<w:pPr>{''.join(properties)}</w:pPr>"
        f"<w:r><w:rPr>{''.join(run_props)}</w:rPr><w:t xml:space=\"preserve\">{escaped}</w:t></w:r>"
        "</w:p>"
    )


def table_xml(headers: list[str], rows: list[list[Any]]) -> str:
    if any(len(row) != len(headers) for row in rows):
        raise ValueError("Every table row must have the same number of columns as headers.")

    width = int(9000 / max(len(headers), 1))
    table_parts = [
        "<w:tbl>",
        "<w:tblPr>"
        "<w:tblW w:w=\"0\" w:type=\"auto\"/>"
        "<w:tblBorders>"
        "<w:top w:val=\"single\" w:sz=\"8\" w:space=\"0\" w:color=\"D7DFE8\"/>"
        "<w:left w:val=\"single\" w:sz=\"8\" w:space=\"0\" w:color=\"D7DFE8\"/>"
        "<w:bottom w:val=\"single\" w:sz=\"8\" w:space=\"0\" w:color=\"D7DFE8\"/>"
        "<w:right w:val=\"single\" w:sz=\"8\" w:space=\"0\" w:color=\"D7DFE8\"/>"
        "<w:insideH w:val=\"single\" w:sz=\"8\" w:space=\"0\" w:color=\"D7DFE8\"/>"
        "<w:insideV w:val=\"single\" w:sz=\"8\" w:space=\"0\" w:color=\"D7DFE8\"/>"
        "</w:tblBorders>"
        "</w:tblPr>",
    ]
    table_parts.append("<w:tr>")
    for header in headers:
        table_parts.append(table_cell_xml(header, width, bold=True))
    table_parts.append("</w:tr>")
    for row in rows:
        table_parts.append("<w:tr>")
        for cell in row:
            table_parts.append(table_cell_xml(str(cell), width))
        table_parts.append("</w:tr>")
    table_parts.append("</w:tbl>")
    return "".join(table_parts)


def table_cell_xml(text: str, width: int, bold: bool = False) -> str:
    run_props = ['<w:sz w:val="20"/><w:szCs w:val="20"/>']
    if bold:
        run_props.append("<w:b/>")
    escaped = xml_escape(text)
    return (
        "<w:tc>"
        f"<w:tcPr><w:tcW w:w=\"{width}\" w:type=\"dxa\"/></w:tcPr>"
        "<w:p><w:pPr><w:spacing w:before=\"60\" w:after=\"60\"/></w:pPr>"
        f"<w:r><w:rPr>{''.join(run_props)}</w:rPr><w:t xml:space=\"preserve\">{escaped}</w:t></w:r>"
        "</w:p></w:tc>"
    )


def main() -> None:
    args = parse_args()
    input_path = Path(args.input)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    data = load_input(input_path)
    slug = data.get("slug") or slugify(data["company_name"])

    html_path = output_dir / f"{slug}.html"
    docx_path = output_dir / f"{slug}.docx"

    html_path.write_text(render_html(data), encoding="utf-8")
    render_docx(data, docx_path)

    print(f"Rendered HTML: {html_path}")
    print(f"Rendered DOCX: {docx_path}")


if __name__ == "__main__":
    main()
