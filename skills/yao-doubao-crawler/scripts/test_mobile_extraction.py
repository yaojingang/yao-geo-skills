#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_ROOT = SCRIPT_DIR.parent
sys.path.insert(0, str(SCRIPT_DIR))

from doubao_mobile_crawl import (  # noqa: E402
    annotate_material_citations,
    collect_references_from_texts,
    extract_reference_keywords,
    extract_visible_search_materials,
    first_url_in_text,
    merge_visible_texts,
    normalize_entity_type,
    parse_reference_summary,
    parse_xml_nodes,
    semantic_title_match,
    visible_texts_from_xml,
)
from analyze_doubao_results import (  # noqa: E402
    mobile_evidence_summary,
    normalize_samples,
)


SAMPLE_XML = """<?xml version="1.0" encoding="UTF-8"?>
<hierarchy rotation="0">
  <node index="0" text="豆包" resource-id="com.larus.nova:id/title" class="android.widget.TextView" bounds="[0,40][300,100]" />
  <node index="1" text="GEO 服务商推荐" resource-id="" class="android.widget.TextView" bounds="[20,120][500,180]" />
  <node index="2" text="以下是几类常见 GEO 服务商：" class="android.widget.TextView" bounds="[20,210][900,260]" />
  <node index="3" text="1. 光引GEO：适合需要 AI 搜索可见度诊断和内容工程的企业。" class="android.widget.TextView" bounds="[20,270][900,340]" />
  <node index="4" text="光引GEO 服务介绍 https://example.com/geo-service" class="android.widget.TextView" bounds="[20,360][900,420]" />
  <node index="5" text="PallasAI GEO Platform pallasai.com" class="android.widget.TextView" bounds="[20,430][900,490]" />
  <node index="6" text="发送" resource-id="com.larus.nova:id/send" class="android.widget.Button" bounds="[900,1700][1030,1820]" clickable="true" enabled="true" />
</hierarchy>
"""


SAMPLE_SEARCH_MATERIAL_XML = """<?xml version="1.0" encoding="UTF-8"?>
<hierarchy rotation="0">
  <node index="0" text="搜索 3 个关键词，参考 4 篇资料" resource-id="com.larus.nova:id/tv_reference_title" class="android.widget.TextView" bounds="[77,706][767,775]" />
  <node index="1" text="“新东方2026年主营业务”、“新东方官网业务板块介绍”、“新东方最新业务布局官方公告”" resource-id="" class="android.widget.TextView" bounds="[33,792][1047,938]" />
  <node index="2" text="1." resource-id="com.larus.nova:id/tv_reference_index" class="android.widget.TextView" bounds="[77,982][146,1038]" />
  <node index="3" text="新东方教育科技（集团）有限公司2026年第三季度财务业绩" resource-id="com.larus.nova:id/tv_reference_content" class="android.widget.TextView" bounds="[146,978][1003,1038]" clickable="true" enabled="true" />
  <node index="4" text="2." resource-id="com.larus.nova:id/tv_reference_index" class="android.widget.TextView" bounds="[77,1070][146,1126]" />
  <node index="5" text="新东方-S(HK9901) 业务展望_F10_同花顺金融服务网" resource-id="com.larus.nova:id/tv_reference_content" class="android.widget.TextView" bounds="[146,1066][1003,1126]" clickable="true" enabled="true" />
  <node index="6" text="3." resource-id="com.larus.nova:id/tv_reference_index" class="android.widget.TextView" bounds="[77,1158][146,1214]" />
  <node index="7" text="俞敏洪，走出董宇辉阴影" resource-id="com.larus.nova:id/tv_reference_content" class="android.widget.TextView" bounds="[146,1154][1003,1214]" clickable="true" enabled="true" />
  <node index="8" text="4." resource-id="com.larus.nova:id/tv_reference_index" class="android.widget.TextView" bounds="[77,1246][146,1302]" />
  <node index="9" text="深耕三十二载，新东方荣膺“2025年度品牌实力教育集团”-新东方网" resource-id="com.larus.nova:id/tv_reference_content" class="android.widget.TextView" bounds="[146,1242][1003,1302]" clickable="true" enabled="true" />
</hierarchy>
"""


class MobileExtractionTest(unittest.TestCase):
    def test_visible_texts_are_deduped_from_xml(self) -> None:
        texts = visible_texts_from_xml(SAMPLE_XML)
        self.assertIn("以下是几类常见 GEO 服务商：", texts)
        self.assertIn("光引GEO 服务介绍 https://example.com/geo-service", texts)
        self.assertEqual(texts.count("豆包"), 1)

    def test_parse_nodes_keeps_bounds_and_clickability(self) -> None:
        nodes = parse_xml_nodes(SAMPLE_XML)
        send = [node for node in nodes if node.text == "发送"][0]
        self.assertEqual(send.center, (965, 1760))
        self.assertTrue(send.clickable)
        self.assertTrue(send.enabled)

    def test_merge_answer_excludes_baseline_prompt_and_controls(self) -> None:
        baseline = {"豆包", "发送"}
        texts = visible_texts_from_xml(SAMPLE_XML)
        answer = merge_visible_texts([texts], baseline, "GEO 服务商推荐")
        self.assertNotIn("豆包", answer)
        self.assertNotIn("发送", answer)
        self.assertNotIn("GEO 服务商推荐", answer)
        self.assertIn("光引GEO", answer)

    def test_collect_references_from_visible_text(self) -> None:
        texts = visible_texts_from_xml(SAMPLE_XML)
        refs = collect_references_from_texts(texts)
        self.assertEqual(refs["count"], 2)
        self.assertEqual(refs["items"][0]["url"], "https://example.com/geo-service")
        self.assertEqual(refs["items"][0]["domain"], "example.com")
        self.assertEqual(refs["items"][1]["domain"], "pallasai.com")
        self.assertEqual(refs["items"][1]["confidence"], "medium")

    def test_url_cleanup_removes_doubao_link_icon_marker(self) -> None:
        self.assertEqual(
            first_url_in_text("来源 https://www.neworiental.org/[__LINK_ICON]"),
            "https://www.neworiental.org/",
        )
        refs = collect_references_from_texts(
            [
                "官网 https://www.neworiental.org/[__LINK_ICON]",
                "官网 https://www.neworiental.org/",
            ]
        )
        self.assertEqual(refs["count"], 1)
        self.assertEqual(refs["items"][0]["url"], "https://www.neworiental.org/")
        self.assertEqual(refs["items"][0]["title"], "官网")

    def test_parse_expanded_search_materials(self) -> None:
        texts = visible_texts_from_xml(SAMPLE_SEARCH_MATERIAL_XML)
        summary = parse_reference_summary(texts)
        materials = extract_visible_search_materials(SAMPLE_SEARCH_MATERIAL_XML)
        self.assertEqual(summary["keyword_count"], 3)
        self.assertEqual(summary["material_count"], 4)
        self.assertEqual(len(materials), 4)
        self.assertEqual(materials[0]["index"], 1)
        self.assertEqual(materials[1]["title"], "新东方-S(HK9901) 业务展望_F10_同花顺金融服务网")
        self.assertTrue(materials[2]["clickable"])

    def test_extract_reference_keywords_ignores_quoted_titles(self) -> None:
        texts = [
            "“新东方2026年主营业务”、“新东方官网业务板块介绍”、“新东方最新业务布局官方公告”",
            "深耕三十二载，新东方荣膺“2025年度品牌实力教育集团”-新东方网",
        ]
        self.assertEqual(
            extract_reference_keywords(texts),
            ["新东方2026年主营业务", "新东方官网业务板块介绍", "新东方最新业务布局官方公告"],
        )
        self.assertEqual(extract_reference_keywords(["“单个搜索关键词”"]), ["单个搜索关键词"])

    def test_annotate_material_citations_marks_cited_and_uncited(self) -> None:
        materials = {
            "items": extract_visible_search_materials(SAMPLE_SEARCH_MATERIAL_XML),
            "count": 4,
        }
        references = {
            "items": [
                {
                    "number": 1,
                    "domain": "investor.neworiental.org",
                    "title": "新东方教育科技（集团）有限公司2026年第三季度财务业绩",
                    "url": "https://investor.neworiental.org/2026q3.pdf",
                },
                {
                    "number": 2,
                    "domain": "10jqka.com.cn",
                    "title": "新东方-S(HK9901) 业务展望_F10_同花顺金融服务网",
                    "url": "https://stockpage.10jqka.com.cn/basicweb/176/HK9901/business.html",
                },
            ]
        }
        annotated = annotate_material_citations(
            materials,
            "参考来源：新东方教育科技（集团）有限公司2026年第三季度财务业绩；新东方-S(HK9901) 业务展望_F10_同花顺金融服务网。",
            references,
        )
        self.assertEqual(annotated["cited_count"], 2)
        self.assertEqual(annotated["uncited_count"], 2)
        self.assertTrue(annotated["items"][0]["cited"])
        self.assertFalse(annotated["items"][2]["cited"])
        self.assertEqual(annotated["items"][0]["citation_count"], 1)

    def test_annotate_material_citations_handles_rewritten_finance_titles(self) -> None:
        materials = {
            "items": [
                {
                    "index": 1,
                    "title": "新东方教育科技（集团）有限公司2026年第三季度财务业绩",
                    "domain": "",
                    "url": "",
                },
                {
                    "index": 2,
                    "title": "新东方-S(HK9901) 业务展望_F10_同花顺金融服务网",
                    "domain": "",
                    "url": "",
                },
            ],
            "count": 2,
        }
        references = {
            "items": [
                {
                    "number": 1,
                    "domain": "investor.neworiental.org",
                    "title": "新东方2026财年第三季度官方财报（纽交所披露）",
                    "url": "https://investor.neworiental.org/2026q3.pdf",
                },
                {
                    "number": 2,
                    "domain": "stockpage.10jqka.com.cn",
                    "title": "同花顺财经（新东方-S 9901.HK 主营业务说明）",
                    "url": "https://stockpage.10jqka.com.cn/basicweb/176/HK9901/business.html",
                },
            ]
        }
        annotated = annotate_material_citations(materials, "", references)
        self.assertEqual(annotated["cited_count"], 2)
        self.assertEqual(annotated["items"][0]["citation_evidence"][0]["reason"], "same_entity_financial_period")
        self.assertEqual(annotated["items"][1]["citation_evidence"][0]["reason"], "same_stock_code_source")

    def test_semantic_title_match_is_not_hardcoded_to_neworiental(self) -> None:
        ok, reason, _ = semantic_title_match("某某科技有限公司2026年第三季度财务业绩", "某某科技2026财年第三季度官方财报")
        self.assertTrue(ok)
        self.assertEqual(reason, "same_entity_financial_period")
        ok, _, _ = semantic_title_match("甲公司2026年第三季度财务业绩", "乙公司2026财年第三季度官方财报")
        self.assertFalse(ok)

    def test_entity_type_normalization_matches_existing_analyzer_contract(self) -> None:
        self.assertEqual(normalize_entity_type("公司"), "company")
        self.assertEqual(normalize_entity_type("person"), "person")
        self.assertEqual(normalize_entity_type("平台"), "product")

    def test_mobile_fixture_shape_matches_canonical_dataset(self) -> None:
        fixture = SKILL_ROOT / "fixtures" / "sample-doubao-mobile-crawl.json"
        data = json.loads(fixture.read_text(encoding="utf-8"))
        self.assertEqual(data["schema_version"], "yao-doubao-crawler/v1")
        self.assertEqual(data["run"]["transport"], "appium-uiautomator2-avd")
        sample = data["samples"][0]
        self.assertTrue(sample["ok"])
        self.assertIn("answer", sample["result"])
        self.assertIn("references", sample["result"])
        self.assertEqual(sample["result"]["references"]["items"][1]["failure_reason"], "visible_reference_without_url")

    def test_mobile_fixture_builds_analysis_mobile_evidence(self) -> None:
        fixture = SKILL_ROOT / "fixtures" / "sample-doubao-mobile-crawl.json"
        data = json.loads(fixture.read_text(encoding="utf-8"))
        samples = normalize_samples(data)
        evidence = mobile_evidence_summary(samples, data.get("input") or {}, data.get("run") or {})
        self.assertEqual(evidence["transport"], "appium-uiautomator2-avd")
        self.assertEqual(evidence["sample_count"], 1)
        self.assertEqual(evidence["collected_material_rows"], 3)
        self.assertEqual(evidence["cited_material_rows"], 2)
        self.assertEqual(evidence["uncited_material_rows"], 1)
        self.assertEqual(evidence["by_question"][0]["material_rows"], 3)
        self.assertEqual(len(evidence["materials"]), 3)

    def test_targetless_mobile_report_omits_empty_target_charts(self) -> None:
        fixture = SKILL_ROOT / "fixtures" / "sample-doubao-mobile-crawl.json"
        data = json.loads(fixture.read_text(encoding="utf-8"))
        input_meta = data.get("input") or {}
        input_meta.pop("target_entity", None)
        input_meta.pop("target_aliases", None)
        for question in input_meta.get("questions", []):
            question.pop("target", None)
        for sample in data.get("samples", []):
            sample.pop("target", None)
            references = ((sample.get("result") or {}).get("references") or {}).get("items") or []
            for reference in references:
                reference["url"] = ""
                reference["domain"] = ""
            materials = (sample.get("result") or {}).get("mobile_search_materials") or {}
            for material in materials.get("items") or []:
                material["url"] = ""
                material["domain"] = ""

        with tempfile.TemporaryDirectory() as tmp:
            tmp_dir = Path(tmp)
            targetless_json = tmp_dir / "targetless-mobile.json"
            out_dir = tmp_dir / "report"
            targetless_json.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
            subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT_DIR / "analyze_doubao_results.py"),
                    str(targetless_json),
                    "--out-dir",
                    str(out_dir),
                ],
                check=True,
                capture_output=True,
                text=True,
            )
            html = (out_dir / "report.html").read_text(encoding="utf-8")

        self.assertIn("探索模式说明", html)
        self.assertNotIn("目标与最佳 3 个竞品", html)
        self.assertNotIn("Target vs Best 3 Competitors Radar", html)
        self.assertNotIn("目标实体情感分布", html)
        self.assertNotIn("高频 URL", html)
        self.assertNotIn("核心指标趋势预估", html)


if __name__ == "__main__":
    unittest.main()
