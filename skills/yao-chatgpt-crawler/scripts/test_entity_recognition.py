#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
from argparse import Namespace
from pathlib import Path
from tempfile import TemporaryDirectory


ROOT = Path(__file__).resolve().parents[1]
ANALYZER_PATH = ROOT / "scripts" / "analyze_chatgpt_results.py"


def load_analyzer():
    spec = importlib.util.spec_from_file_location("analyze_chatgpt_results", ANALYZER_PATH)
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
        "ChatGPT Web Search 汇总显示",
        "ChatGPT Web Search 结果中",
        "OpenAI Search 引用来源",
        "装修公司",
        "西安装修公司",
        "西安口碑装修公司",
        "西安高口碑装修公司",
        "2026西安主流装修公司",
        "2026年十家综合实力突出的装修公司",
        "西安选装修公司",
        "有几家装修公司",
        "用于公司",
        "包装设计",
        "极简玻璃瓶设计",
        "珠宝化瓶身设计",
        "瓶身设计",
        "被定位为设计",
        "以珠宝化瓶身设计",
        "常见品牌",
        "If you're selecting a co",
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
        "西安城市人家装饰",
        "西安青马设计",
        "宸智雅筑",
        "漾家雅筑",
        "绿庭装饰",
        "西安鲁班装饰",
        "西安兴唐装饰",
        "西安壹号装修设计",
    ]
    for value in real_entities:
        assert not analyzer.looks_like_stop_entity(value), f"should keep real entity: {value}"

    water_samples = [
        {
            "sample_id": "w01",
            "ok": True,
            "answer": (
                "用于公司：可提供定制服务。包装设计：极简玻璃瓶设计。"
                "VOSS、Evian、FIJI Water 和 CustomWater.com 是可核验的品牌或供应商。"
                "If you're selecting a co-branded water supplier, compare minimum order quantities."
            ),
            "references": [],
        }
    ]
    water_rows = analyzer.collect_entity_rows(water_samples)
    for value in [
        "用于公司",
        "包装设计",
        "极简玻璃瓶设计",
        "珠宝化瓶身设计",
        "瓶身设计",
        "被定位为设计",
        "以珠宝化瓶身设计",
        "常见品牌",
        "If you're selecting a co",
    ]:
        assert value not in water_rows, f"water prose fragment leaked as entity: {value}"

    target_only_samples = [
        {
            "sample_id": f"t{index:02d}",
            "question_id": "q01",
            "question": "定制瓶装水公司推荐",
            "repeat_index": index,
            "ok": True,
            "answer": "冰川饮品有限公司：提供企业定制瓶装水。",
            "references": [],
            "error": "",
            "raw": {},
        }
        for index in (1, 2)
    ]
    with TemporaryDirectory() as temp_dir:
        target_only_file = Path(temp_dir) / "brands.txt"
        target_only_file.write_text("TargetCo|Target Company\n", encoding="utf-8")
        target_only_args = Namespace(
            brands="",
            brands_file=str(target_only_file),
            target_entity="TargetCo",
            target_aliases="Target Company",
            entity_type="company",
            target_kind="auto",
            min_inferred_count=2,
            max_entity_candidates=50,
            max_inferred_brands=24,
            semantic_review="off",
            semantic_confidence_threshold=0.72,
            _semantic_review_cache_path=None,
        )
        target_only_brands, _, _, _, _ = analyzer.load_brand_defs(
            target_only_args,
            {"input": {"target_entity": "TargetCo", "entity_type": "company"}},
            target_only_samples,
        )
        target_only_names = {row["name"] for row in target_only_brands}
        assert {"TargetCo", "冰川饮品有限公司"}.issubset(target_only_names), target_only_names

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

    provided_brand = analyzer.classify_entity(
        {
            "name": "PallasAI",
            "aliases": [],
            "sample_ids": {"s01", "s02"},
            "raw_count": 2,
            "reasons": {"provided_or_metric_entity": 1, "answer_alias_match": 2},
        },
        "company",
    )
    assert provided_brand["kind"] == "company", provided_brand
    assert provided_brand["is_target"], provided_brand
    reviewed_provided_brand = analyzer.heuristic_semantic_review(
        provided_brand,
        {"entity": "光引GEO", "aliases": ["光引GEO"], "entity_type": "company", "has_target": True},
        ["光引GEO"],
    )
    assert reviewed_provided_brand["is_same_type"], reviewed_provided_brand
    assert reviewed_provided_brand["semantic_label"] == "direct_competitor", reviewed_provided_brand
    assert reviewed_provided_brand["confidence"] == 0.9, reviewed_provided_brand
    merged_provided_candidates = {
        candidate["name"]: candidate
        for candidate in analyzer.build_entity_candidates(
            [
                {
                    "sample_id": "s01",
                    "ok": True,
                    "answer": "PallasAI可作为产品化工具候选，适合与源易信息一起对比。",
                    "references": [],
                }
            ],
            [{"name": "PallasAI", "aliases": ["PallasAI"]}],
            "company",
            include_discovered=True,
        )
    }
    assert merged_provided_candidates["PallasAI"]["kind"] == "company", merged_provided_candidates["PallasAI"]
    assert merged_provided_candidates["PallasAI"]["is_target"], merged_provided_candidates["PallasAI"]

    decor_samples = [
        {
            "sample_id": "d01",
            "ok": True,
            "answer": (
                "西安城市人家装饰：本地规模较大。"
                "宸智雅筑|漾家雅筑：适合高端全案。"
                "别墅大宅定制 西安青马设计：设计能力突出。"
                "老房翻新专家 绿庭装饰 / 西安鲁班装饰：更适合旧改。"
            ),
            "references": [{"title": "2026西安主流装修公司推荐", "url": "https://example.com/a"}],
        },
        {
            "sample_id": "d02",
            "ok": True,
            "answer": (
                "西安城市人家装饰：适合重视本地规模的业主。"
                "西安青马设计：适合别墅和大宅设计。"
                "宸智雅筑：适合高端全案。"
                "漾家雅筑：可作为宸智雅筑同类方案对比。"
                "绿庭装饰：适合老房翻新。"
                "西安鲁班装饰：适合旧房改造。"
                "西安鲁班装饰和西安兴唐装饰也常被放在同一批名单里比较。"
            ),
            "references": [{"title": "西安口碑装修公司哪家好", "url": "https://example.com/b"}],
        },
    ]
    decor_candidates = {
        candidate["name"]: candidate
        for candidate in analyzer.infer_entity_candidates(decor_samples, 2, 50, "company")
    }
    for value in [
        "西安城市人家装饰",
        "西安青马设计",
        "宸智雅筑",
        "漾家雅筑",
        "绿庭装饰",
        "西安鲁班装饰",
    ]:
        assert value in decor_candidates, f"missing decoration competitor: {value}; got {decor_candidates.keys()}"
        assert analyzer.candidate_is_valid_competitor(decor_candidates[value], "company", 2), decor_candidates[value]

    for value in ["西安装修公司", "2026西安主流装修公司", "西安口碑装修公司"]:
        assert value not in decor_candidates, f"generic category leaked as competitor: {value}"

    target_profile = {
        "entity": "西安壹号设计",
        "aliases": ["西安壹号设计", "壹号设计"],
        "entity_type": "company",
        "has_target": True,
    }
    target_aliases = target_profile["aliases"]
    semantic_expectations = [
        (
            {
                "name": "西安城市人家装饰",
                "kind": "company",
                "is_target": True,
                "confidence": 0.84,
                "sample_count": 2,
                "raw_count": 2,
                "evidence": {"org_suffix": 2},
                "surface_score": 4,
                "evidence_score": 3.8,
            },
            "direct_competitor",
        ),
        (
            {
                "name": "西安青马设计",
                "kind": "company",
                "is_target": True,
                "confidence": 0.84,
                "sample_count": 2,
                "raw_count": 2,
                "evidence": {"org_suffix": 2},
                "surface_score": 4,
                "evidence_score": 3.8,
            },
            "direct_competitor",
        ),
        (
            {"name": "西安装修公司", "kind": "company", "is_target": False, "sample_count": 2, "evidence": {"org_suffix": 2}},
            "generic_category",
        ),
        (
            {"name": "全案设计", "kind": "concept", "is_target": False, "sample_count": 2, "evidence": {"org_suffix": 2}},
            "service_or_feature",
        ),
        (
            {"name": "A股上市集团", "kind": "noise", "is_target": False, "sample_count": 2, "evidence": {"answer_heading": 2}},
            "attribute",
        ),
        (
            {"name": "教育部首批认证机构", "kind": "noise", "is_target": False, "sample_count": 2, "evidence": {"answer_heading": 2}},
            "attribute",
        ),
    ]
    for candidate, expected_label in semantic_expectations:
        reviewed = analyzer.heuristic_semantic_review(candidate, target_profile, target_aliases)
        assert reviewed["semantic_label"] == expected_label, reviewed

    product_profile = {"entity": "蔚来", "aliases": ["蔚来", "NIO"], "entity_type": "product", "has_target": True}
    product_rows = {}
    for sample_id in ["p01", "p02"]:
        analyzer.add_entity_candidate(product_rows, "理想L9", sample_id, "answer_heading")
        analyzer.add_entity_candidate(product_rows, "问界M9", sample_id, "answer_heading")
        analyzer.add_entity_candidate(product_rows, "理想汽车", sample_id, "answer_heading")
        analyzer.add_entity_candidate(product_rows, "小鹏汽车", sample_id, "answer_heading")
    for value in ["理想L9", "问界M9", "理想汽车", "小鹏汽车"]:
        candidate = analyzer.classify_entity(product_rows[value], "product")
        reviewed = analyzer.heuristic_semantic_review(candidate, product_profile, product_profile["aliases"])
        assert reviewed["semantic_label"] == "direct_competitor", reviewed
    assert analyzer.vehicle_brand_base_name("理想汽车") == "理想"
    merged_vehicle_rows = analyzer.dedupe_brand_rows([["小米"], ["小米汽车", "小米"]])
    assert len(merged_vehicle_rows) == 1 and "小米汽车" in merged_vehicle_rows[0]["aliases"], merged_vehicle_rows
    generic_product = {"name": "豪华SUV", "kind": "concept", "is_target": False, "sample_count": 2, "evidence": {"answer_heading": 2}}
    assert analyzer.heuristic_semantic_review(generic_product, product_profile, product_profile["aliases"])["semantic_label"] == "generic_category"
    generic_nev = {"name": "新能源汽车", "kind": "concept", "is_target": False, "sample_count": 2, "evidence": {"answer_heading": 2}}
    assert analyzer.heuristic_semantic_review(generic_nev, product_profile, product_profile["aliases"])["semantic_label"] == "generic_category"

    person_profile = {"entity": "姚金刚", "aliases": ["姚金刚"], "entity_type": "person", "has_target": True}
    company_candidate = {"name": "启德教育", "kind": "company", "is_target": False, "sample_count": 2, "evidence": {"org_suffix": 2}}
    assert analyzer.heuristic_semantic_review(company_candidate, person_profile, person_profile["aliases"])["semantic_label"] == "unrelated_entity"

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

    model_samples = [
        {
            "sample_id": "m01",
            "question_id": "q01",
            "question": "国产大模型排名",
            "repeat_index": 1,
            "ok": True,
            "answer": "豆包、通义千问、GLM、DeepSeek 和 Kimi 都是国产模型产品。阿里巴巴和百度是公司。模型和 Mixture of Experts 只是泛化概念。",
            "references": [],
            "error": "",
            "raw": {},
        },
        {
            "sample_id": "m02",
            "question_id": "q01",
            "question": "国产大模型排名",
            "repeat_index": 2,
            "ok": True,
            "answer": "豆包适合企业应用，通义千问、GLM、DeepSeek 和 Kimi 也常被比较。阿里巴巴、百度是厂商，不是本次产品竞品行。",
            "references": [],
            "error": "",
            "raw": {},
        },
    ]
    with TemporaryDirectory() as temp_dir:
        brands_file = Path(temp_dir) / "brands.txt"
        brands_file.write_text(
            "豆包|Doubao|豆包大模型|豆包模型\n通义千问|Qwen\nGLM|ChatGLM\nDeepSeek|DeepSeek-V3\nKimi|Kimi K2\n",
            encoding="utf-8",
        )
        args = Namespace(
            brands="",
            brands_file=str(brands_file),
            target_entity="豆包",
            target_aliases="Doubao,豆包大模型,豆包模型",
            entity_type="product",
            target_kind="auto",
            min_inferred_count=2,
            max_entity_candidates=50,
            max_inferred_brands=24,
            semantic_review="auto",
            semantic_confidence_threshold=0.72,
            _semantic_review_cache_path=None,
        )
        brands, brand_source, target_kind, entity_candidates, target_profile = analyzer.load_brand_defs(
            args,
            {"input": {"target_entity": "豆包", "entity_type": "product"}},
            model_samples,
        )
        summary = analyzer.compute_summary(
            model_samples,
            brands,
            brand_source,
            [{"sample_id": sample["sample_id"], "question_id": sample["question_id"], "question": sample["question"]} for sample in model_samples],
            target_kind,
            entity_candidates,
            target_profile,
            10,
        )
        assert target_profile["aliases"] == ["豆包", "Doubao", "豆包大模型", "豆包模型"], target_profile["aliases"]
        comparison_names = {row["name"] for row in summary["target"]["comparison_rows"]}
        assert {"豆包", "通义千问", "GLM", "DeepSeek", "Kimi"}.issubset(comparison_names), comparison_names
        assert not (comparison_names & {"阿里巴巴", "百度", "模型", "Mixture of Experts"}), comparison_names

    print("entity recognition regression: PASS")


if __name__ == "__main__":
    main()
