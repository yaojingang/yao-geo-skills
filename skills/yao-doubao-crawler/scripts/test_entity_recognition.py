#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ANALYZER_PATH = ROOT / "scripts" / "analyze_doubao_results.py"


def load_analyzer():
    spec = importlib.util.spec_from_file_location("analyze_doubao_results", ANALYZER_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load analyzer from {ANALYZER_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> None:
    analyzer = load_analyzer()

    non_entities = [
        "教育部首批认证机构",
        "首批教育部认证机构",
        "是教育部首批认证的合规机构",
        "是首批获得国家资质认证的机构",
        "上市公司",
        "A股上市集团",
        "是A股上市公司",
        "全国43个城市设有分公司",
        "海外留学",
        "自费出国留学",
        "2026海外留学申请机构",
        "2026留学中介机构",
        "专业靠谱的留学",
        "上海留学",
        "2026留学",
        "2026主流留学",
        "盘点多家机构",
        "帮你盘点靠谱的留学机构",
        "何甄选出国留学咨询机构",
        "本地靠谱机构",
        "横向测评机构",
        "中华人民共和国教育",
        "靠谱专业机构",
        "部分机构",
        "果机构",
        "这类机构",
        "海外15家直营公司",
        "市场上的留学机构",
        "老牌全链条机构",
        "收费低于同级别机构",
        "这份专业留学",
        "品牌与语培留学",
        "信赖老牌大机构",
        "真正有竞争力的机构",
        "上门咨询",
        "深入咨询",
        "线下咨询",
        "砍掉多余营销",
    ]
    for value in non_entities:
        assert analyzer.looks_like_stop_entity(value), f"should reject non-entity: {value}"

    real_entities = [
        "新东方",
        "启德教育",
        "优越留学",
        "立思辰留学",
        "指南者留学",
        "新通教育",
        "金吉列留学",
        "多次元教育",
        "致学博教育",
        "威久留学",
        "托普仕留学",
        "优悦教育",
        "北京环球教育",
        "恒学云留学",
        "金吉列出国留学咨询服务有限公司",
        "平安留学",
    ]
    for value in real_entities:
        assert not analyzer.looks_like_stop_entity(value), f"should keep real entity: {value}"

    prefix_sensitive_entities = {
        "在行": "在行",
        "当贝市场": "当贝市场",
        "和府捞面": "和府捞面",
    }
    for raw, expected in prefix_sensitive_entities.items():
        assert analyzer.normalize_entity_name(raw) == expected, f"should not strip real prefix: {raw}"

    recovery_cases = {
        "那么启德教育": "启德教育",
        "可以重点考察像优越留学": "优越留学",
        "在像指南者留学这类机构": "指南者留学",
        "且对留学": "留学",
    }
    rows = {}
    for raw, expected in recovery_cases.items():
        assert analyzer.normalize_entity_name(raw) == expected, f"normalize {raw}"
        analyzer.add_entity_candidate(rows, raw, "s01", "org_suffix")
    assert "启德教育" in rows
    assert "优越留学" in rows
    assert "指南者留学" in rows
    assert "留学" not in rows

    valid_rows = {}
    analyzer.add_entity_candidate(valid_rows, "启德教育", "s01", "org_suffix")
    analyzer.add_entity_candidate(valid_rows, "启德教育", "s02", "answer_heading")
    candidate = analyzer.classify_entity(valid_rows["启德教育"], "company")
    assert analyzer.candidate_is_valid_competitor(candidate, "company", 2), candidate

    one_off_fragment_rows = {}
    analyzer.add_entity_candidate(one_off_fragment_rows, "英国罗素集团", "s01", "org_suffix")
    one_off_fragment = analyzer.classify_entity(one_off_fragment_rows["英国罗素集团"], "company")
    assert not one_off_fragment["is_target"], one_off_fragment

    source_only_rows = {}
    analyzer.add_entity_candidate(source_only_rows, "平安留学", "s01", "source_title_org")
    analyzer.add_entity_candidate(source_only_rows, "平安留学", "s02", "source_title_org")
    source_only = analyzer.classify_entity(source_only_rows["平安留学"], "company")
    assert not source_only["is_target"], source_only
    assert not analyzer.candidate_is_valid_competitor(source_only, "company", 2), source_only

    title_fragment_rows = {}
    analyzer.add_entity_candidate(title_fragment_rows, "光引GEO完成品牌AI", "s01", "source_title_org")
    analyzer.add_entity_candidate(title_fragment_rows, "光引GEO完成品牌AI", "s02", "source_title_org")
    title_fragment = analyzer.classify_entity(title_fragment_rows["光引GEO完成品牌AI"], "company")
    merged_aliases = analyzer.merge_target_aliases(["光引GEO", "光引"], [title_fragment], [])
    assert "光引GEO完成品牌AI" not in merged_aliases, merged_aliases

    print("entity recognition regression: PASS")


if __name__ == "__main__":
    main()
