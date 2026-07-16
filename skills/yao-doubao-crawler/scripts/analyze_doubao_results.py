#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime as dt
import html
import json
import math
import re
import zipfile
from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import urlparse


STOP_ENTITIES = {
    "AI",
    "GEO",
    "SEO",
    "Doubao",
    "ChatGPT",
    "Kimi",
    "国内",
    "领域",
    "专家",
    "推荐",
    "理由",
    "来源",
    "网页",
    "回答",
    "搜索",
    "根据",
    "公开信息",
    "核心贡献",
    "推荐理由",
    "如何选择",
    "个网页",
    "已阅读",
    "适合人群",
    "机构名称",
    "核心优势",
    "参考信息",
    "退费条款",
    "强项赛道",
    "同时",
    "Offer",
    "机构",
    "公司",
    "企业",
    "集团",
    "平台",
    "服务商",
    "品牌",
    "留学",
    "教育",
    "咨询",
    "中介",
    "上市公司",
    "上市企业",
    "上市集团",
    "A股上市公司",
    "A股上市集团",
    "港股上市公司",
    "美股上市公司",
}

COMMON_SURNAMES = set(
    "赵钱孙李周吴郑王冯陈褚卫蒋沈韩杨朱秦尤许何吕施张孔曹严华金魏陶姜"
    "戚谢邹喻柏水窦章云苏潘葛奚范彭郎鲁韦昌马苗凤花方俞任袁柳鲍史唐费"
    "廉岑薛雷贺倪汤滕殷罗毕郝邬安常乐于时傅皮卞齐康伍余元卜顾孟平黄和"
    "穆萧尹姚邵湛汪祁毛禹狄米贝明臧计伏成戴谈宋庞熊纪舒屈项祝董梁杜阮"
    "蓝闵席季麻强贾路娄危江童颜郭梅盛林刁钟徐邱骆高夏蔡田胡凌霍虞万支"
    "柯管卢莫经房裘缪干解应宗丁宣邓郁单杭洪包诸左石崔吉龚程邢裴陆荣翁"
    "刘曾叶"
)

NOISE_ENTITY_PATTERNS = [
    r"适合|关键|方法论|场景|背书|研究专长|核心|特点|选择|三问|如何|服务商",
    r"指标|数据|体系|标准|技术路径|效果|算法|团队|案例|平台覆盖",
    r"个网页|已阅读|问题|回答|来源|参考|推荐|理由",
    r"增长官|强于|理论|基于|应能|指导|底层|量化|迭代",
]

STRONG_ENTITY_CONTEXT_PREFIX_RE = re.compile(
    r"^(?:"
    r"如果|那么|并且|而且|同时|因此|所以|但是|"
    r"可以重点考察像|可以重点考察|重点考察|可以询问|直接询问|"
    r"例如|比如|以及|目前|代表人物|专家|老师|推荐|关注|选择|分为|在像"
    r")"
)

WEAK_ENTITY_CONTEXT_PREFIX_RE = re.compile(r"^(?:若|当|但|且|对|在|像|如|和|或|现)")

ENTITY_CONTEXT_TAIL_RE = re.compile(
    r"(?:这类|此类|这一类|这一类的|这类的|一类|类型|这种|这家|这些|那些|等)"
    r"(?:机构|公司|企业|集团|平台|服务商|品牌|单位)?$"
)

ENTITY_FRAGMENT_PATTERNS = [
    r"^(?:我|你|我们|这|这份|这些|那|那些|某|该|各|每|部分|不同|很多|真正|最好的|可以|建议|了解了|特别|花点时间).{0,18}(?:机构|公司|企业|集团|平台|服务商|品牌|留学|教育|咨询|中介)$",
    r"^(?:若|当|但|且|对|在|像|如|和|或|现).{0,16}(?:机构|公司|企业|集团|平台|服务商|品牌|留学|教育|咨询|中介)$",
    r"^.{0,18}(?:整理|考察|看重|信赖|值得|核实|查看|分析|挑选|选择|了解|砍掉|覆盖|进行|参与|申请|避坑|投诉|梯队|进度|收费|营销|服务能力).{0,12}(?:机构|公司|企业|集团|平台|服务商|品牌|留学|教育|咨询|中介)$",
    r"^(?:上门|深入|线下|实地|升学转学甚至移民|多方|第三方|免费|付费).{0,12}咨询$",
    r"^.{0,12}(?:砍掉|多余|线上|线下|投放|获客|内容).{0,12}营销$",
]

ENTITY_ATTRIBUTE_PATTERNS = [
    r"^(?:自费|公费|准备|申请|计划|打算|想要|海外|国内)?出国$",
    r"^(?:20\d{2}(?:年)?)?(?:出国|海外|美国|英国|加拿大|澳洲|香港|新加坡|上海|北京|广州|深圳|国内|国际|自费|公费|主流|专业|靠谱|正规|本地|当地|高端|老牌|头部|综合|一站式|全链条|专业靠谱的)*留学(?:申请|服务|咨询|中介|机构|公司){0,2}$",
    r"^(?:20\d{2}(?:年)?)?(?:美国|英国|加拿大|澳洲|香港|新加坡|海外|出国)?留学(?:中介|机构|公司|服务机构|申请机构)$",
    r"^(?:A股|港股|美股|H股|主板|创业板|科创板|纳斯达克|纽交所|港交所)?上市(?:公司|企业|集团|机构|平台|服务商)$",
    r"^(?:是|属于|作为)?(?:A股|港股|美股|H股|上市).{0,8}(?:公司|企业|集团|机构|平台|服务商)$",
    r"^(?:国有|央企|国企|民营|外资|合资|股份制|连锁|本土|国内|海外|跨国)(?:公司|企业|集团|机构|平台|服务商)$",
    r"^(?:头部|大型|知名|老牌|传统|正规|本地|当地|全国性|综合性|高端|专业|全链条|一站式){1,4}(?:教育|留学|咨询|服务)?(?:公司|企业|集团|机构|平台|服务商)$",
    r"^(?:头部|大型|知名|老牌|传统|正规|本地|当地|全国性|综合性|高端|专业|全链条)(?:教育|留学|咨询|服务)?(?:公司|企业|集团|机构|平台|服务商)$",
    r"^(?:教育|留学|咨询|服务|中介|培训)(?:公司|企业|集团|机构|平台|服务商)$",
    r"^(?:A股|港股|美股|H股|上市|国有|民营|外资|合资|连锁|大型|头部|知名|老牌|传统|正规|高端|专业|全链条)(?:教育|留学|咨询|服务)?(?:集团|公司|企业|机构)$",
    r"^(?:教育部|工信部|商务部|民政部|市场监管总局|国家|官方|政府|行业|协会|权威)?(?:首批|首家|唯一|指定|认证|认可|备案|批准|授权|资质|合规|正规|持牌|牌照|许可|监管|推荐|示范|试点|重点|白名单).{0,10}(?:机构|公司|企业|集团|平台|服务商|品牌|单位)$",
    r"^.{0,16}(?:首批|首家|唯一|指定|认证|认可|备案|批准|授权|资质|合规|正规|持牌|牌照|许可|监管|推荐|示范|试点|重点|白名单).{0,8}(?:机构|公司|企业|集团|平台|服务商|品牌|单位)$",
    r"^(?:部分|不同|多家|代表|这类|哪类|市场|市面上|市场上|主流|本地|靠谱|专业|靠谱专业|横向测评|盘点|挑选|选择|选|再选|要求|看重|重视|追求|申请季挑选|帮你盘点|我整理了几个|我把几家|直接询问|可以询问).{0,14}(?:机构|公司|企业|集团|平台|服务商|品牌|留学|教育|咨询|中介)$",
    r"^.{0,12}(?:盘点|测评|评测|对比|避坑|攻略|指南(?!者)|推荐|排名|排行|榜单|甄选|哪家|哪个|如何|怎么|何选|何甄选).{0,12}(?:机构|公司|企业|集团|平台|服务商|品牌|留学|教育|咨询|中介)$",
    r"^.{0,12}(?:教育留学|语培留学|留学机构|咨询机构|中介机构)$",
    r"^(?:北京|上海|广州|深圳|国内|海外|全国|本地|当地).{0,12}留学.{0,10}(?:公司|机构|辅导机构|中介|服务|咨询)$",
    r"^(?:全国|本地|当地|北京|大型|综合|连锁|头部|高端|低龄|艺术|海外|社区|公立|私立).{0,14}(?:大机构|机构|公司|大学|留学|分公司)$",
    r"^(?:北京|上海|广州|深圳)?选机构$",
    r"^.{0,12}(?:业务覆盖|收费低于|同步进行|语言考试|境外服务|细分领域|影响整个|并参与|不仅做|除了看|砍掉|隐形消费|服务短板).{0,12}(?:机构|公司|企业|集团|平台|服务商|品牌|留学|教育|咨询|中介)$",
    r"^(?:中华人民共和国|国家|教育部|政府|官方).{0,12}(?:教育|机构|公司|企业|集团|平台|服务商|品牌)$",
    r"^.{0,12}\d+(?:家|个城市|座城市|个国家).{0,12}(?:公司|机构|集团|分公司|分支机构)$",
    r"^[\u4e00-\u9fa5]?(?:机构|公司|企业|集团|平台|服务商)$",
]

ENGLISH_ACRONYM_NOISE = {
    "AI",
    "B2B",
    "CEO",
    "CGO",
    "GEO",
    "GEO 2.0",
    "GIS",
    "ISO",
    "ISO 19170-4",
    "MOE",
    "SEO",
}

PERSON_ROLE_WORDS = (
    "院士|教授|博士|研究员|副研究员|助理研究员|老师|专家|创始人|CEO|CGO|负责人|主任|主席|Fellow|操盘手"
)

ORG_SUFFIX_WORDS = (
    "公司|科技|集团|研究院|研究所|实验室|大学|学院|中心|平台|服务商|机构|传媒|教育|留学|出国|智能|数据|AI"
)

COMPANY_SUFFIX_WORDS = (
    "公司|科技|集团|研究院|研究所|实验室|大学|学院|中心|服务商|机构|传媒|教育|留学|出国"
)

PRODUCT_SUFFIX_WORDS = (
    "产品|工具|平台|系统|软件|应用|App|APP|模型|助手|插件|方案|服务|AI"
)

STRONG_COMPANY_SUFFIX_RE = re.compile(
    r"(?:有限责任公司|股份有限公司|有限公司|公司|集团|大学|学院|研究院|研究所|实验室|中心|科技|传媒)$"
)

REPORT_ITEM_LIMIT = 10

ENTITY_TYPE_ALIASES = {
    "auto": "auto",
    "person": "person",
    "people": "person",
    "human": "person",
    "人": "person",
    "人物": "person",
    "人名": "person",
    "专家": "person",
    "brand": "company",
    "company": "company",
    "organization": "company",
    "org": "company",
    "公司": "company",
    "机构": "company",
    "品牌": "company",
    "服务商": "company",
    "product": "product",
    "tool": "product",
    "产品": "product",
    "工具": "product",
    "平台": "product",
    "mixed": "mixed",
    "混合": "mixed",
}

ENTITY_TYPE_LABELS = {
    "person": "人",
    "company": "公司",
    "product": "产品",
    "mixed": "混合",
    "auto": "自动",
}

POSITIVE_SENTIMENT_WORDS = [
    "推荐",
    "靠谱",
    "优势",
    "专业",
    "领先",
    "适合",
    "透明",
    "稳定",
    "优秀",
    "成熟",
    "权威",
    "官方",
    "口碑",
    "成功",
    "丰富",
    "优质",
    "全面",
    "突出",
    "首选",
    "值得",
    "强",
    "高",
]

NEGATIVE_SENTIMENT_WORDS = [
    "不推荐",
    "风险",
    "避坑",
    "投诉",
    "负面",
    "谨慎",
    "问题",
    "缺点",
    "失败",
    "套路",
    "吐槽",
    "争议",
    "不适合",
    "差",
    "退费",
    "踩雷",
    "黑",
    "贵",
    "低",
]

SENTIMENT_LABELS = {
    "positive": "积极",
    "neutral": "中性",
    "negative": "负向",
}

SENTIMENT_LABELS_EN = {
    "positive": "Positive",
    "neutral": "Neutral",
    "negative": "Negative",
}

CHANNEL_LABELS_ZH = {
    "official": "官方",
    "media": "媒体",
    "community": "社区",
    "developer": "开发者",
    "encyclopedia": "百科",
    "other": "其他",
}

SOURCE_POSITION_LABELS_ZH = {
    "1-3": "1-3",
    "4-6": "4-6",
    "7+": "7+",
    "unknown": "未识别",
}

SHARE_DONUT_COLORS = ["#173A63", "#6F8395", "#9D8B63", "#7B9A83", "#AEB8C4", "#C8BFA4"]

RECENCY_LABELS = {
    "current_year": "本年",
    "last_year": "近一年",
    "older": "更早",
    "unknown": "未识别",
}

TITLE_INTENT_PATTERNS = [
    ("榜单排名", r"(?:排名|排行|榜单|TOP|Top|top|前\s*\d|盘点|清单|名录|有哪些)"),
    ("对比评测", r"(?:对比|评测|测评|横评|比较|VS|vs|实力|矩阵|哪家强)"),
    ("推荐选择", r"(?:推荐|哪家|哪个好|靠谱|值得选|选择|怎么选|首选)"),
    ("避坑风险", r"(?:避坑|陷阱|风险|短板|投诉|退费|隐形消费|注意|谨慎)"),
    ("指南攻略", r"(?:指南|攻略|必读|申请|流程|条件|怎么|如何|方法|技巧)"),
    ("趋势新闻", r"(?:趋势|发布|出炉|观察|报告|标准|政策|新规|20\d{2})"),
    ("资料介绍", r"(?:介绍|百科|官网|是什么|简介|大学|学院|教授|专家|机构)"),
    ("研究论文", r"(?:论文|研究|arxiv|doi|Optimization|GEO:)"),
]

DOMAIN_NAME_OVERRIDES = {
    "gaokao.eol.cn": "中国教育在线",
    "eol.cn": "中国教育在线",
    "wx.sll.cn": "立思辰留学云",
    "sll.cn": "立思辰留学云",
    "eic.org.cn": "启德教育",
    "weiyangx.com": "未央网",
    "sohu.com": "搜狐",
    "liuxue.test.xdf.cn": "新东方留学",
    "xdf.cn": "新东方",
    "cuc.fjnu.edu.cn": "福建师范大学协和学院",
    "iccs.fjnu.edu.cn": "福建师范大学海外教育学院",
    "fjnu.edu.cn": "福建师范大学",
    "baike.baidu.com": "百度百科",
    "m.gmw.cn": "光明网",
    "news.gmw.cn": "光明网",
    "gmw.cn": "光明网",
    "cloud.tencent.cn": "腾讯云开发者",
    "m.ithome.com": "IT之家",
    "ithome.com": "IT之家",
    "m.bjnews.com.cn": "新京报",
    "bjnews.com.cn": "新京报",
    "people.ucas.ac.cn": "中国科学院大学",
    "people.ucas.edu.cn": "中国科学院大学",
    "news.qq.com": "腾讯新闻",
    "qq.com": "腾讯网",
    "ar5iv.labs.arxiv.org": "arXiv 论文镜像",
    "mech.pku.edu.cn": "北京大学工学院",
    "dky.njnu.edu.cn": "南京师范大学地理科学学院",
}

SOURCE_NAME_OVERRIDES = {
    "Fjnu": "福建师范大学协和学院",
    "QQ News": "腾讯新闻",
    "tencent.cn": "腾讯云",
    "arXiv": "arXiv 论文",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Analyze Doubao repeated crawl JSON and render a Kami-styled HTML report."
    )
    parser.add_argument("input_json", help="doubao-crawl.json, results-all.json, or a single Doubao raw JSON")
    parser.add_argument("--brands", dest="brands", help="Comma, semicolon, or newline separated target/competitor names")
    parser.add_argument("--entities", dest="brands", help="Alias for --brands")
    parser.add_argument("--brands-file", dest="brands_file", help="Target/competitor alias file. Format: canonical|alias1|alias2")
    parser.add_argument("--entities-file", dest="brands_file", help="Alias for --brands-file")
    parser.add_argument("--target-entity", help="Primary target entity, for example 新东方, 孟庆涛, or 光引GEO")
    parser.add_argument("--target-aliases", help="Optional aliases for the primary target entity, separated by comma, pipe, semicolon, or newline")
    parser.add_argument("--entity-type", help="Target entity type: 人/person, 公司/company, or 产品/product")
    parser.add_argument("--out-dir", help="Output directory. Default: <input-dir>/report")
    parser.add_argument("--title", default="Doubao AI 搜索概率分析报告")
    parser.add_argument("--min-inferred-count", type=int, default=2)
    parser.add_argument("--max-inferred-brands", type=int, default=24)
    parser.add_argument(
        "--target-kind",
        choices=["auto", "person", "brand", "company", "product", "mixed"],
        default="auto",
        help="Target entity type for inferred candidates. auto uses the question wording.",
    )
    parser.add_argument("--max-entity-candidates", type=int, default=48)
    parser.add_argument("--max-report-items", type=int, default=REPORT_ITEM_LIMIT)
    return parser.parse_args()


def read_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def clean_text(value: object) -> str:
    return re.sub(r"\s+", " ", str(value or "")).strip()


def normalize_domain(value: str) -> str:
    value = clean_text(value).lower()
    value = re.sub(r"^www\.", "", value)
    return value


def domain_from_url(url: str) -> str:
    try:
        return normalize_domain(urlparse(url).hostname or "")
    except Exception:
        return ""


def normalize_ref(ref: dict) -> dict:
    url = clean_text(ref.get("url"))
    domain = normalize_domain(ref.get("domain") or domain_from_url(url))
    return {
        "number": ref.get("number"),
        "source": clean_text(ref.get("source")),
        "domain": domain,
        "title": clean_text(ref.get("title")),
        "date": clean_text(ref.get("date")),
        "url": url,
        "summary": clean_text(ref.get("summary")),
    }


def normalize_samples(data: dict) -> list[dict]:
    samples: list[dict] = []
    if str(data.get("schema_version", "")).startswith("yao-doubao-crawler/"):
        for index, sample in enumerate(data.get("samples", []), start=1):
            result = sample.get("result") or {}
            refs = ((result.get("references") or {}).get("items") or [])
            samples.append(
                {
                    "sample_id": sample.get("sample_id") or f"s{index:03d}",
                    "question_id": sample.get("question_id") or f"q{index:02d}",
                    "question": sample.get("question") or result.get("question") or "",
                    "repeat_index": sample.get("repeat_index") or 1,
                    "ok": bool(sample.get("ok")) and bool(clean_text((result.get("answer") or {}).get("text"))),
                    "answer": clean_text((result.get("answer") or {}).get("text")),
                    "references": [normalize_ref(ref) for ref in refs],
                    "mobile_search_materials": result.get("mobile_search_materials") or {},
                    "action_trace": result.get("action_trace") or [],
                    "transport": result.get("transport") or (data.get("run") or {}).get("transport") or "",
                    "error": clean_text(sample.get("error")),
                    "raw": sample,
                }
            )
        return samples

    if isinstance(data.get("results"), list):
        for index, result in enumerate(data.get("results", []), start=1):
            refs = result.get("references") or []
            samples.append(
                {
                    "sample_id": f"q{int(result.get('index') or index):02d}-r01",
                    "question_id": f"q{int(result.get('index') or index):02d}",
                    "question": result.get("question") or "",
                    "repeat_index": 1,
                    "ok": bool(result.get("ok")) and bool(clean_text(result.get("answer"))),
                    "answer": clean_text(result.get("answer")),
                    "references": [normalize_ref(ref) for ref in refs],
                    "mobile_search_materials": result.get("mobile_search_materials") or {},
                    "action_trace": result.get("action_trace") or [],
                    "transport": result.get("transport") or "",
                    "error": "",
                    "raw": result,
                }
            )
        return samples

    if data.get("engine") == "doubao" or data.get("answer"):
        refs = ((data.get("references") or {}).get("items") or [])
        samples.append(
            {
                "sample_id": "q01-r01",
                "question_id": "q01",
                "question": data.get("question") or "",
                "repeat_index": 1,
                "ok": bool(data.get("ok")) and bool(clean_text((data.get("answer") or {}).get("text"))),
                "answer": clean_text((data.get("answer") or {}).get("text")),
                "references": [normalize_ref(ref) for ref in refs],
                "mobile_search_materials": data.get("mobile_search_materials") or {},
                "action_trace": data.get("action_trace") or [],
                "transport": data.get("transport") or "",
                "error": "",
                "raw": data,
            }
        )
        return samples

    raise ValueError("Unsupported input JSON shape.")


def normalize_plan(data: dict, samples: list[dict]) -> list[dict]:
    if str(data.get("schema_version", "")).startswith("yao-doubao-crawler/"):
        plan = data.get("plan") or []
        if plan:
            return [
                {
                    "sample_id": item.get("sample_id") or f"planned-{index:03d}",
                    "question_id": item.get("question_id") or f"q{index:02d}",
                    "question": item.get("question") or "",
                }
                for index, item in enumerate(plan, start=1)
            ]
        questions = ((data.get("input") or {}).get("questions") or [])
        if questions:
            entries = []
            for q_index, question in enumerate(questions, start=1):
                qid = question.get("id") or f"q{q_index:02d}"
                repeat = int(question.get("repeat") or (data.get("input") or {}).get("global_repeat") or 1)
                for repeat_index in range(1, repeat + 1):
                    entries.append(
                        {
                            "sample_id": f"{qid}-r{repeat_index:02d}",
                            "question_id": qid,
                            "question": question.get("question") or "",
                        }
                    )
            return entries
    return [
        {
            "sample_id": sample.get("sample_id") or f"s{index:03d}",
            "question_id": sample.get("question_id") or f"q{index:02d}",
            "question": sample.get("question") or "",
        }
        for index, sample in enumerate(samples, start=1)
    ]


def split_brand_line(line: str) -> list[str]:
    parts = re.split(r"[|,，;；\t]+", line)
    return [clean_text(part) for part in parts if clean_text(part)]


def split_aliases(value: object) -> list[str]:
    if isinstance(value, list):
        aliases = []
        for item in value:
            aliases.extend(split_aliases(item))
        return aliases
    return split_brand_line(str(value or ""))


def normalize_entity_type(value: object, allow_auto: bool = False) -> str:
    raw = clean_text(value)
    if not raw:
        return ""
    normalized = ENTITY_TYPE_ALIASES.get(raw) or ENTITY_TYPE_ALIASES.get(raw.lower())
    if normalized == "auto" and not allow_auto:
        return ""
    if not normalized:
        raise ValueError(f"Unsupported entity type: {raw}. Use 人/person, 公司/company, or 产品/product.")
    return normalized or ""


def has_cjk(value: str) -> bool:
    return bool(re.search(r"[\u4e00-\u9fff]", value or ""))


def compact_latin_key(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", value.lower())


def alias_matches_entity_name(value: str, alias: str) -> bool:
    name = normalize_entity_name(value)
    candidate = normalize_entity_name(alias)
    if not name or not candidate:
        return False
    name_lower = name.lower()
    candidate_lower = candidate.lower()
    if name_lower == candidate_lower:
        return True
    if has_cjk(candidate):
        cjk_len = len(re.findall(r"[\u4e00-\u9fff]", candidate))
        return cjk_len >= 2 and (candidate_lower in name_lower or name_lower in candidate_lower)

    alias_key = compact_latin_key(candidate)
    name_key = compact_latin_key(name)
    return len(alias_key) >= 4 and bool(alias_key and name_key) and (alias_key in name_key or name_key in alias_key)


def target_kind_from_args(args: argparse.Namespace, samples: list[dict], input_meta: dict) -> str:
    explicit = normalize_entity_type(args.entity_type or input_meta.get("entity_type") or input_meta.get("entityType"))
    if explicit:
        return explicit
    legacy = normalize_entity_type(args.target_kind, allow_auto=True)
    if legacy and legacy != "auto":
        return legacy
    return infer_target_kind(samples, args.target_kind)


def resolve_target_profile(args: argparse.Namespace, data: dict, samples: list[dict]) -> dict:
    input_meta = data.get("input") or {}
    target_entity = clean_text(
        args.target_entity
        or input_meta.get("target_entity")
        or input_meta.get("targetEntity")
        or input_meta.get("target")
    )
    has_explicit_entity_type = bool(args.entity_type or input_meta.get("entity_type") or input_meta.get("entityType"))
    if target_entity and not has_explicit_entity_type and args.target_kind == "auto":
        raise ValueError("Target entity analysis requires --entity-type 人/person, 公司/company, or 产品/product.")
    entity_type = target_kind_from_args(args, samples, input_meta)
    aliases = [target_entity] if target_entity else []
    aliases.extend(split_aliases(args.target_aliases))
    aliases.extend(split_aliases(input_meta.get("target_aliases") or input_meta.get("targetAliases")))
    seen: set[str] = set()
    deduped_aliases = []
    for alias in aliases:
        alias = normalize_entity_name(alias)
        key = alias.lower()
        if alias and key not in seen:
            seen.add(key)
            deduped_aliases.append(alias)
    return {
        "entity": target_entity,
        "aliases": deduped_aliases,
        "entity_type": entity_type,
        "entity_type_label": ENTITY_TYPE_LABELS.get(entity_type, entity_type),
        "has_target": bool(target_entity),
    }


def matches_target_entity(value: str, target_aliases: list[str]) -> bool:
    for alias in target_aliases:
        if alias_matches_entity_name(value, alias):
            return True
    return False


def merge_target_aliases(target_aliases: list[str], candidates: list[dict], provided_rows: list[list[str]]) -> list[str]:
    aliases = list(target_aliases)
    for row in provided_rows:
        if any(matches_target_entity(item, aliases) for item in row):
            aliases.extend(item for item in row if not looks_like_stop_entity(item))
    for candidate in candidates:
        if not candidate.get("is_target") or not candidate_has_answer_evidence(candidate):
            continue
        names = [candidate.get("name", ""), *candidate.get("aliases", [])]
        if any(matches_target_entity(item, aliases) for item in names):
            aliases.extend(item for item in names if not looks_like_stop_entity(item))
    seen: set[str] = set()
    out = []
    for alias in aliases:
        alias = normalize_entity_name(alias)
        key = alias.lower()
        if alias and key not in seen:
            seen.add(key)
            out.append(alias)
    return out


def annotate_entity_roles(brands: list[dict], target_profile: dict) -> list[dict]:
    target_aliases = target_profile.get("aliases") or []
    entity_type = target_profile.get("entity_type") or "mixed"
    for brand in brands:
        aliases = brand.get("aliases", [brand["name"]])
        is_target = bool(target_aliases) and any(matches_target_entity(alias, target_aliases) for alias in aliases)
        brand["role"] = "target" if is_target else "competitor"
        brand["entity_type"] = entity_type
    return brands


def candidate_has_answer_evidence(candidate: dict) -> bool:
    evidence = candidate.get("evidence") or {}
    return any(not key.startswith("source_title") for key in evidence)


def candidate_evidence_score(candidate: dict) -> float:
    evidence = Counter(candidate.get("evidence") or {})
    score = 0.0
    if evidence.get("provided_or_metric_entity"):
        score += 5.0
    if evidence.get("answer_alias_match"):
        score += 3.0
    if evidence.get("org_suffix") or evidence.get("english_brand_like"):
        score += 2.0
    if any(key.startswith("person") for key in evidence):
        score += 2.0
    if evidence.get("answer_heading"):
        score += 1.0
    if evidence.get("source_title_org") or evidence.get("source_title_person"):
        score += 0.5
    score += min(candidate.get("sample_count") or 0, 5) * 0.4
    return round(score, 2)


def candidate_is_valid_competitor(candidate: dict, target_kind: str, min_count: int) -> bool:
    if not candidate.get("is_target"):
        return False
    if candidate.get("kind") not in {"person", "company", "product"}:
        return False
    if (candidate.get("sample_count") or 0) < min_count:
        return False
    if not candidate_has_answer_evidence(candidate):
        return False
    surface_score = candidate.get("surface_score")
    if surface_score is None:
        surface_score, _ = entity_surface_score(candidate.get("name", ""), target_kind)
    evidence_score = candidate.get("evidence_score")
    if evidence_score is None:
        evidence_score = candidate_evidence_score(candidate)
    return surface_score >= 3 and evidence_score >= 3.4


def load_brand_defs(
    args: argparse.Namespace,
    data: dict,
    samples: list[dict],
) -> tuple[list[dict], str, str, list[dict], dict]:
    rows: list[list[str]] = []
    target_profile = resolve_target_profile(args, data, samples)
    target_kind = target_profile["entity_type"]
    if args.brands:
        for part in re.split(r"[\n;；]+", args.brands):
            part = clean_text(part)
            if not part:
                continue
            if "|" in part:
                rows.append(split_brand_line(part))
            else:
                rows.extend([[item] for item in split_brand_line(part)])
    if args.brands_file:
        for line in Path(args.brands_file).read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            rows.append(split_brand_line(line))

    if target_profile["has_target"]:
        entity_candidates = infer_entity_candidates(samples, args.min_inferred_count, args.max_entity_candidates, target_kind)
        target_aliases = merge_target_aliases(target_profile["aliases"], entity_candidates, rows)
        target_profile["aliases"] = target_aliases
        target_row = [target_profile["entity"], *[alias for alias in target_aliases if alias != target_profile["entity"]]]
        competitor_rows = [
            row
            for row in rows
            if row and not any(matches_target_entity(item, target_aliases) for item in row)
        ]
        for candidate in entity_candidates:
            if not candidate_is_valid_competitor(candidate, target_kind, args.min_inferred_count):
                continue
            names = [candidate["name"], *candidate.get("aliases", [])]
            if any(matches_target_entity(item, target_aliases) for item in names):
                continue
            competitor_rows.append(names)
        brands = dedupe_brand_rows([target_row, *competitor_rows])
        brands = annotate_entity_roles(brands, target_profile)
        entity_candidates = build_entity_candidates(samples, brands, target_kind, include_discovered=True)
        return brands, "target_entity", target_kind, entity_candidates, target_profile

    if rows:
        brands = dedupe_brand_rows(rows)
        profile = {"entity": "", "aliases": [], "entity_type": target_kind, "entity_type_label": ENTITY_TYPE_LABELS.get(target_kind, target_kind), "has_target": False}
        return brands, "provided", target_kind, build_entity_candidates(samples, brands, target_kind, include_discovered=False), profile

    entity_candidates = infer_entity_candidates(samples, args.min_inferred_count, args.max_entity_candidates, target_kind)
    target_rows = [
        [candidate["name"], *candidate.get("aliases", [])]
        for candidate in entity_candidates
        if candidate_is_valid_competitor(candidate, target_kind, args.min_inferred_count)
    ][: args.max_inferred_brands]
    if target_rows:
        profile = {"entity": "", "aliases": [], "entity_type": target_kind, "entity_type_label": ENTITY_TYPE_LABELS.get(target_kind, target_kind), "has_target": False}
        return dedupe_brand_rows(target_rows), "inferred_target_entity", target_kind, entity_candidates, profile

    inferred = infer_brand_rows(samples, args.min_inferred_count, args.max_inferred_brands)
    brands = dedupe_brand_rows(inferred)
    profile = {"entity": "", "aliases": [], "entity_type": target_kind, "entity_type_label": ENTITY_TYPE_LABELS.get(target_kind, target_kind), "has_target": False}
    return brands, "inferred", target_kind, build_entity_candidates(samples, brands, target_kind, include_discovered=False), profile


def dedupe_brand_rows(rows: list[list[str]]) -> list[dict]:
    seen: set[str] = set()
    brands = []
    for row in rows:
        aliases = []
        for alias in row:
            if looks_like_stop_entity(alias):
                continue
            if alias and alias.lower() not in {item.lower() for item in aliases}:
                aliases.append(alias)
        if not aliases:
            continue
        canonical = aliases[0]
        key = canonical.lower()
        if key in seen:
            continue
        seen.add(key)
        brands.append({"name": canonical, "aliases": aliases})
    return brands


def infer_brand_rows(samples: list[dict], min_count: int, limit: int) -> list[list[str]]:
    counter: Counter[str] = Counter()
    for sample in samples:
        lines = re.split(r"[\n\r。！？!?]+", sample.get("answer", ""))
        for raw_line in lines:
            line = raw_line.strip()
            line = re.sub(r"^[\s\-*•·\d.、一二三四五六七八九十]+", "", line)
            if not line or len(line) > 80:
                continue
            head = re.split(r"[：:（(，,。;\t\-—]", line, maxsplit=1)[0].strip()
            head = re.sub(r"\s+", " ", head)
            if 2 <= len(head) <= 24 and not looks_like_stop_entity(head):
                counter[head] += 1

            for match in re.findall(r"[A-Z][A-Za-z0-9&.\- ]{1,28}(?:AI|GEO|SEO|Tech|Data|Cloud|Labs|Group|Inc|Co)?", line):
                entity = clean_text(match)
                if 2 <= len(entity) <= 30 and not looks_like_stop_entity(entity):
                    counter[entity] += 1

    rows = []
    for entity, count in counter.most_common(limit * 3):
        if count < min_count:
            continue
        if looks_like_stop_entity(entity):
            continue
        rows.append([entity])
        if len(rows) >= limit:
            break
    return rows


def looks_like_stop_entity(value: str) -> bool:
    cleaned = clean_text(value).strip("：:,.，。()（）[]【】")
    if cleaned in STOP_ENTITIES:
        return True
    if looks_like_entity_attribute(cleaned):
        return True
    if looks_like_entity_fragment(cleaned):
        return True
    if re.search(r"(已阅读|个网页|适合人群|机构名称|核心优势|参考信息)", cleaned):
        return True
    if re.search(r"(?:是一个|是一款|是一种|属于|作为).{0,12}(?:产品|工具|平台|软件|公司|机构|品牌)$", cleaned):
        return True
    if re.search(r"(语言培训[和与]留学|主流留学机构|市面上留学机构|看重机构|老牌机构)", cleaned):
        return True
    if re.fullmatch(r"(?:19|20)\d{2}年的留学", cleaned):
        return True
    if re.fullmatch(r"\d+家.*(?:分公司|分支机构|机构|门店|中心)", cleaned):
        return True
    if re.fullmatch(
        r"(?:出国)?留学(?:机构|公司|中介)?|主流留学机构|国内\d+家分支机构|语言培训[和与]留学|老牌机构|看重机构",
        cleaned,
    ):
        return True
    if re.fullmatch(
        r"(?:老牌|看重|主流|头部|大型|靠谱|专业|高端|传统|本地|当地|线上|线下|综合|知名|主打|适合|正规)(?:留学)?(?:机构|公司|中介|服务商)",
        cleaned,
    ):
        return True
    if re.fullmatch(r"(TOP|QS)?\d+", cleaned, flags=re.IGNORECASE):
        return True
    if re.search(r"(退费条款|强项赛道|留学公司|选择留学|避坑|提醒|陷阱|预算|人群|数据|指标|院校|录取|案例|文书|透明|全程|背景|需求|推荐理由)", cleaned):
        return True
    if re.search(r"(推荐|说明|依据|观察|选择|阶段|如下|包括|需要|如果|希望|当前|以下|根据)$", cleaned):
        return True
    if re.fullmatch(r"[0-9A-Za-z .:/-]+", cleaned) and len(cleaned.split()) > 4:
        return True
    return False


def looks_like_entity_attribute(value: str) -> bool:
    cleaned = normalize_entity_name(value)
    if not cleaned:
        return True
    for pattern in ENTITY_ATTRIBUTE_PATTERNS:
        if re.fullmatch(pattern, cleaned, flags=re.IGNORECASE):
            return True
    return False


def looks_like_entity_fragment(value: str) -> bool:
    cleaned = normalize_entity_name(value)
    if not cleaned:
        return True
    return any(re.fullmatch(pattern, cleaned) for pattern in ENTITY_FRAGMENT_PATTERNS)


def infer_target_kind(samples: list[dict], requested: str) -> str:
    normalized = normalize_entity_type(requested, allow_auto=True)
    if normalized and normalized != "auto":
        return normalized
    text = " ".join(sample.get("question", "") for sample in samples)
    wants_person = re.search(r"(专家|人物|老师|顾问|院士|教授|博士|达人|操盘手|负责人|创始人)", text)
    wants_company = re.search(r"(品牌|公司|机构|服务商|厂商|供应商)", text)
    wants_product = re.search(r"(产品|工具|平台|软件|系统|模型|应用|插件)", text)
    wanted = [kind for kind, matched in [("person", wants_person), ("company", wants_company), ("product", wants_product)] if matched]
    if len(wanted) == 1:
        return wanted[0]
    if len(wanted) > 1:
        return "mixed"
    if wants_person and not wants_company and not wants_product:
        return "person"
    return "mixed"


def stripped_context_candidate_is_plausible(value: str) -> bool:
    if not value:
        return False
    if value in STOP_ENTITIES:
        return True
    if len(value) < 2:
        return False
    if any(re.fullmatch(pattern, value, flags=re.IGNORECASE) for pattern in ENTITY_ATTRIBUTE_PATTERNS):
        return True
    if any(re.fullmatch(pattern, value) for pattern in ENTITY_FRAGMENT_PATTERNS):
        return True
    return bool(re.search(f"(?:{ORG_SUFFIX_WORDS}|{PRODUCT_SUFFIX_WORDS})$", value))


def normalize_entity_name(value: str) -> str:
    cleaned = clean_text(value)
    cleaned = cleaned.strip("：:,.，。；;、()（）[]【】<>《》“”\"' ")
    for _ in range(3):
        next_cleaned = STRONG_ENTITY_CONTEXT_PREFIX_RE.sub("", cleaned).strip()
        if next_cleaned != cleaned:
            cleaned = next_cleaned
            continue
        weak_cleaned = WEAK_ENTITY_CONTEXT_PREFIX_RE.sub("", cleaned).strip()
        if weak_cleaned != cleaned and stripped_context_candidate_is_plausible(weak_cleaned):
            cleaned = weak_cleaned
            continue
        break
    cleaned = ENTITY_CONTEXT_TAIL_RE.sub("", cleaned).strip()
    cleaned = re.sub(r"(?:等|之一|方面|方向|领域)$", "", cleaned)
    return clean_text(cleaned)


def looks_like_chinese_person_name(value: str) -> bool:
    name = normalize_entity_name(value)
    if not re.fullmatch(r"[\u4e00-\u9fa5]{2,4}", name):
        return False
    if name[0] not in COMMON_SURNAMES:
        return False
    if re.search(ORG_SUFFIX_WORDS, name):
        return False
    if looks_like_stop_entity(name):
        return False
    if any(re.search(pattern, name) for pattern in NOISE_ENTITY_PATTERNS):
        return False
    return True


def weak_org_prefix_is_clean(name: str) -> bool:
    if not re.search(r"(?:教育|留学|出国)$", name):
        return True
    prefix = re.sub(r"(?:教育|留学|出国)$", "", name)
    if len(prefix) < 2 or len(prefix) > 8:
        return False
    return not bool(
        re.search(
            r"\d|[与和及]|(?:专业|靠谱|主流|海外|国内|自费|公费|准备|计划|打算|想要|出国|这份|纠结|看重|信赖|品牌|语培|申请|服务|咨询|中介|机构|公司|集团|可以|那么|特别|对|且|你|我|在像|像)",
            prefix,
        )
    )


def entity_surface_score(value: str, target_kind: str) -> tuple[int, list[str]]:
    name = normalize_entity_name(value)
    reasons: list[str] = []
    if not name or looks_like_stop_entity(name):
        return 0, ["属性、泛称或噪声短语"]
    score = 1
    if target_kind in {"company", "brand", "mixed"}:
        if STRONG_COMPANY_SUFFIX_RE.search(name):
            score = max(score, 5)
            reasons.append("强组织后缀")
        elif re.search(r"(?:机构|平台|服务商)$", name) and not looks_like_entity_fragment(name):
            score = max(score, 3)
            reasons.append("组织类后缀")
        elif re.search(r"(?:教育|留学|出国)$", name) and weak_org_prefix_is_clean(name):
            score = max(score, 3)
            reasons.append("品牌化弱后缀")
    if target_kind in {"product", "mixed"} and re.search(f"(?:{PRODUCT_SUFFIX_WORDS})$", name):
        score = max(score, 3)
        reasons.append("产品类后缀")
    if target_kind in {"person", "mixed"} and looks_like_chinese_person_name(name):
        score = max(score, 4)
        reasons.append("中文姓名形态")
    if re.search(r"[A-Za-z]", name) and not re.fullmatch(r"[0-9A-Za-z .:/-]+", name):
        score += 1
        reasons.append("中英混合品牌形态")
    return min(score, 6), reasons


def looks_like_org_entity(value: str) -> bool:
    name = normalize_entity_name(value)
    if looks_like_stop_entity(name):
        return False
    if re.search(r"(?:教育|留学|出国)$", name):
        if not weak_org_prefix_is_clean(name):
            return False
    return bool(re.search(f"(?:{COMPANY_SUFFIX_WORDS})$", name))


def looks_like_product_entity(value: str) -> bool:
    name = normalize_entity_name(value)
    if looks_like_stop_entity(name):
        return False
    return bool(re.search(f"(?:{PRODUCT_SUFFIX_WORDS})$", name))


def looks_like_noise_entity(value: str) -> bool:
    name = normalize_entity_name(value)
    if not name:
        return True
    if looks_like_stop_entity(name):
        return True
    if name.upper() in ENGLISH_ACRONYM_NOISE:
        return True
    if any(re.search(pattern, name, flags=re.IGNORECASE) for pattern in NOISE_ENTITY_PATTERNS):
        return True
    if re.fullmatch(r"[A-Za-z0-9 .:+-]{2,30}", name) and not re.search(r"(AI|Tech|Data|Cloud|Labs|Group)", name):
        return True
    return False


def add_entity_candidate(
    rows: dict[str, dict],
    name: str,
    sample_id: str,
    reason: str,
    alias: str = "",
) -> None:
    normalized = normalize_entity_name(name)
    if not normalized or len(normalized) > 36 or looks_like_stop_entity(normalized):
        return
    row = rows.setdefault(
        normalized,
        {
            "name": normalized,
            "aliases": [],
            "sample_ids": set(),
            "reasons": Counter(),
            "raw_count": 0,
        },
    )
    if alias:
        alias = normalize_entity_name(alias)
        if alias and alias.lower() != normalized.lower() and alias not in row["aliases"]:
            row["aliases"].append(alias)
    row["sample_ids"].add(sample_id)
    row["reasons"][reason] += 1
    row["raw_count"] += 1


def collect_entity_rows(samples: list[dict]) -> dict[str, dict]:
    rows: dict[str, dict] = {}
    person_role = PERSON_ROLE_WORDS
    org_suffix = ORG_SUFFIX_WORDS
    for sample in samples:
        if not sample.get("ok"):
            continue
        sid = sample["sample_id"]
        text = sample.get("answer", "")
        lines = re.split(r"[\n\r。！？!?]+", text)
        for raw_line in lines:
            line = clean_text(raw_line)
            if not line:
                continue
            short_line = re.sub(r"^[\s\-*•·👑🔬🌍📡🖥️💡🗺️🛰️\d.、一二三四五六七八九十]+", "", line)
            head = re.split(r"[：:（(，,。;\t\-—]", short_line, maxsplit=1)[0].strip()
            if 2 <= len(head) <= 24:
                add_entity_candidate(rows, head, sid, "answer_heading")

            for match in re.finditer(rf"(?:^|[，。、：:；;\s（(])([\u4e00-\u9fa5]{{2,4}})\s*(?:{person_role})", line):
                add_entity_candidate(rows, match.group(1), sid, "person_role_after")
            for match in re.finditer(rf"(?:{person_role})\s*([\u4e00-\u9fa5]{{2,4}})([A-Z][A-Za-z]{{2,20}})?", line):
                add_entity_candidate(rows, match.group(1), sid, "person_role_before", match.group(2) or "")
            for match in re.finditer(r"([\u4e00-\u9fa5]{2,4})\s*[\(（]([A-Z][A-Za-z .-]{1,30})[\)）]", line):
                add_entity_candidate(rows, match.group(1), sid, "person_alias", match.group(2))
            for match in re.finditer(r"([\u4e00-\u9fa5]{2,4})([A-Z][A-Za-z]{2,20})(?:\s|：|:|，|,|$)", line):
                if looks_like_chinese_person_name(match.group(1)):
                    add_entity_candidate(rows, match.group(1), sid, "person_alias", match.group(2))
            for match in re.finditer(rf"([\u4e00-\u9fa5A-Za-z0-9]{{2,24}}(?:{org_suffix}))", line):
                add_entity_candidate(rows, match.group(1), sid, "org_suffix")
            for match in re.finditer(r"[A-Z][A-Za-z0-9&.\- ]{1,28}(?:AI|GEO|SEO|Tech|Data|Cloud|Labs|Group|Inc|Co)", line):
                add_entity_candidate(rows, match.group(0), sid, "english_brand_like")

        for ref in sample.get("references", []):
            title = ref.get("title", "")
            for match in re.finditer(r"^([\u4e00-\u9fa5]{2,4})[-_—]", title):
                add_entity_candidate(rows, match.group(1), sid, "source_title_person")
            for match in re.finditer(r"([\u4e00-\u9fa5]{2,4})与", title):
                add_entity_candidate(rows, match.group(1), sid, "source_title_person")
            for match in re.finditer(rf"([\u4e00-\u9fa5A-Za-z0-9]{{2,24}}(?:{org_suffix}))", title):
                add_entity_candidate(rows, match.group(1), sid, "source_title_org")
    return rows


def classify_entity(row: dict, target_kind: str) -> dict:
    name = row["name"]
    reasons = row["reasons"]
    aliases = row.get("aliases", [])
    kind = "concept"
    confidence = 0.35
    why: list[str] = []
    if looks_like_noise_entity(name):
        kind = "noise"
        confidence = 0.1
        why.append("通用词/指标/缩写，非目标实体")
    elif reasons.get("provided_or_metric_entity") and target_kind in {"person", "company", "product"}:
        kind = target_kind
        confidence = 0.9
        why.append("用户提供或进入指标计算的实体")
    elif looks_like_chinese_person_name(name) and any(key.startswith("person") or key == "source_title_person" for key in reasons):
        kind = "person"
        confidence = 0.72
        why.append("中文姓名且邻近专家职务或来源标题")
    elif looks_like_product_entity(name):
        kind = "product"
        confidence = 0.68
        why.append("带产品/工具/平台类后缀")
    elif looks_like_org_entity(name):
        kind = "company"
        confidence = 0.68
        why.append("带机构/公司/平台类后缀")
    elif aliases and looks_like_chinese_person_name(name):
        kind = "person"
        confidence = 0.68
        why.append("中文姓名带英文别名")
    elif looks_like_chinese_person_name(name) and reasons.get("answer_heading"):
        kind = "person"
        confidence = 0.58
        why.append("疑似中文姓名且作为回答条目出现")

    sample_count = len(row.get("sample_ids", []))
    surface_score, surface_reasons = entity_surface_score(name, target_kind)
    evidence_score = candidate_evidence_score(
        {
            "evidence": dict(reasons),
            "sample_count": sample_count,
        }
    )
    confidence += min(sample_count, 5) * 0.04
    confidence += min(surface_score, 5) * 0.02
    if reasons.get("source_title_person") or reasons.get("source_title_org"):
        confidence += 0.08
    if kind == "noise":
        confidence = min(confidence, 0.2)
    confidence = max(0.0, min(0.95, confidence))

    provided_or_metric = bool(reasons.get("provided_or_metric_entity"))
    has_answer_evidence = any(not key.startswith("source_title") for key in reasons)
    is_target = kind in {"person", "company", "product"} if target_kind == "mixed" else kind == target_kind
    if not provided_or_metric and (
        not has_answer_evidence
        or sample_count < 2
        or surface_score < 3
        or evidence_score < 3.4
    ):
        is_target = False
    if kind == "noise":
        is_target = False
    if is_target:
        why.append(f"匹配目标类型：{target_kind}")
    return {
        "name": name,
        "aliases": aliases,
        "kind": kind,
        "is_target": is_target,
        "confidence": round(confidence, 3),
        "sample_count": sample_count,
        "raw_count": row.get("raw_count", 0),
        "evidence": dict(reasons),
        "evidence_score": evidence_score,
        "surface_score": surface_score,
        "surface_reasons": surface_reasons,
        "reasons": why,
    }


def infer_entity_candidates(samples: list[dict], min_count: int, limit: int, target_kind: str) -> list[dict]:
    rows = collect_entity_rows(samples)
    candidates = [classify_entity(row, target_kind) for row in rows.values()]
    candidates = [
        candidate
        for candidate in candidates
        if candidate["sample_count"] >= min_count
    ]
    candidates.sort(
        key=lambda item: (
            1 if item["is_target"] else 0,
            item["confidence"],
            item["sample_count"],
            item["raw_count"],
        ),
        reverse=True,
    )
    return candidates[:limit]


def build_entity_candidates(
    samples: list[dict],
    brands: list[dict],
    target_kind: str,
    include_discovered: bool = False,
) -> list[dict]:
    rows = collect_entity_rows(samples) if include_discovered else {}
    for brand in brands:
        name = brand["name"]
        row = rows.setdefault(
            name,
            {
                "name": name,
                "aliases": [alias for alias in brand.get("aliases", []) if alias != name],
                "sample_ids": set(),
                "reasons": Counter({"provided_or_metric_entity": 1}),
                "raw_count": 1,
            },
        )
        for alias in brand.get("aliases", []):
            if alias != name and alias not in row["aliases"]:
                row["aliases"].append(alias)
        aliases = brand.get("aliases", [name])
        for sample in samples:
            if sample.get("ok") and find_alias_position(sample.get("answer", ""), aliases) is not None:
                row["sample_ids"].add(sample["sample_id"])
                row["reasons"]["answer_alias_match"] += 1
                row["raw_count"] += 1
    return [classify_entity(row, target_kind) for row in rows.values()]


def find_alias_position(text: str, aliases: list[str]) -> int | None:
    if not text:
        return None
    lower = text.lower()
    positions = []
    for alias in aliases:
        alias = clean_text(alias)
        if not alias:
            continue
        alias_lower = alias.lower()
        if has_cjk(alias):
            cjk_len = len(re.findall(r"[\u4e00-\u9fff]", alias))
            if cjk_len < 2:
                continue
            idx = lower.find(alias_lower)
            if idx >= 0:
                positions.append(idx)
            continue

        alias_key = compact_latin_key(alias)
        if len(alias_key) < 4:
            match = re.search(rf"(?<![A-Za-z0-9]){re.escape(alias)}(?![A-Za-z0-9])", text, flags=re.IGNORECASE)
            if match:
                positions.append(match.start())
            continue

        idx = lower.find(alias_lower)
        if idx >= 0:
            positions.append(idx)
    return min(positions) if positions else None


def text_contains_alias(text: str, aliases: list[str]) -> bool:
    return find_alias_position(text, aliases) is not None


def alias_spans(text: str, aliases: list[str]) -> list[tuple[int, int]]:
    if not text:
        return []
    lower = text.lower()
    spans: list[tuple[int, int]] = []
    for alias in aliases:
        alias = clean_text(alias)
        if not alias:
            continue
        alias_lower = alias.lower()
        if has_cjk(alias):
            if len(re.findall(r"[\u4e00-\u9fff]", alias)) < 2:
                continue
            start = 0
            while True:
                idx = lower.find(alias_lower, start)
                if idx < 0:
                    break
                spans.append((idx, idx + len(alias)))
                start = idx + max(len(alias), 1)
            continue

        alias_key = compact_latin_key(alias)
        if len(alias_key) < 4:
            for match in re.finditer(rf"(?<![A-Za-z0-9]){re.escape(alias)}(?![A-Za-z0-9])", text, flags=re.IGNORECASE):
                spans.append((match.start(), match.end()))
            continue

        start = 0
        while True:
            idx = lower.find(alias_lower, start)
            if idx < 0:
                break
            spans.append((idx, idx + len(alias)))
            start = idx + max(len(alias), 1)

    spans.sort(key=lambda item: (item[0], -(item[1] - item[0])))
    merged: list[tuple[int, int]] = []
    for start, end in spans:
        if not merged or start >= merged[-1][1]:
            merged.append((start, end))
        elif end > merged[-1][1]:
            merged[-1] = (merged[-1][0], end)
    return merged


def count_alias_mentions(text: str, aliases: list[str]) -> int:
    return len(alias_spans(text, aliases))


def count_sentiment_hits(context: str) -> tuple[int, int]:
    negative = sum(1 for word in NEGATIVE_SENTIMENT_WORDS if word in context)
    positive_context = context
    for word in NEGATIVE_SENTIMENT_WORDS:
        positive_context = positive_context.replace(word, " ")
    positive = sum(1 for word in POSITIVE_SENTIMENT_WORDS if word in positive_context)
    return positive, negative


def sentiment_for_alias_context(text: str, aliases: list[str]) -> str:
    spans = alias_spans(text, aliases)
    if not spans:
        return "neutral"
    windows = []
    for start, end in spans[:6]:
        windows.append(text[max(0, start - 80) : min(len(text), end + 120)])
    context = clean_text("。".join(windows))
    positive, negative = count_sentiment_hits(context)
    if positive > negative:
        return "positive"
    if negative > positive:
        return "negative"
    return "neutral"


def brand_ranks_for_sample(sample: dict, brands: list[dict]) -> dict[str, int]:
    found = []
    text = sample.get("answer", "")
    for brand in brands:
        pos = find_alias_position(text, brand["aliases"])
        if pos is not None:
            found.append((pos, brand["name"]))
    found.sort(key=lambda item: (item[0], item[1]))
    return {name: index + 1 for index, (_, name) in enumerate(found)}


def rate(numerator: int, denominator: int) -> float:
    return numerator / denominator if denominator else 0.0


def pct(value: float) -> str:
    return f"{value * 100:.1f}%"


def pp(value: float | None) -> str:
    value = value or 0.0
    sign = "+" if value > 0 else ""
    return f"{sign}{value * 100:.1f}pp"


def compute_brand_metrics(samples: list[dict], brands: list[dict]) -> dict:
    valid_samples = [sample for sample in samples if sample["ok"]]
    denominator = len(valid_samples)
    by_brand = {}
    by_question: dict[str, dict[str, dict]] = defaultdict(dict)
    question_denominators = Counter(sample["question_id"] for sample in valid_samples)
    ranks_by_sample = {
        sample["sample_id"]: brand_ranks_for_sample(sample, brands)
        for sample in valid_samples
    }

    for brand in brands:
        ranks = []
        top1 = 0
        top3 = 0
        top5 = 0
        mentioned = 0
        mention_total = 0
        sentiment_counts: Counter[str] = Counter()
        reference_mentions = 0
        reference_domains: set[str] = set()
        reference_urls: set[str] = set()
        for sample in valid_samples:
            ranks_for_sample = ranks_by_sample.get(sample["sample_id"], {})
            rank = ranks_for_sample.get(brand["name"])
            mention_count = count_alias_mentions(sample.get("answer", ""), brand["aliases"])
            if rank is not None:
                mentioned += 1
                ranks.append(rank)
                if rank == 1:
                    top1 += 1
                if rank <= 3:
                    top3 += 1
                if rank <= 5:
                    top5 += 1
                mention_total += mention_count
                sentiment_counts[sentiment_for_alias_context(sample.get("answer", ""), brand["aliases"])] += 1
            for ref in sample.get("references", []):
                ref_text = " ".join(
                    [
                        ref.get("source", ""),
                        ref.get("domain", ""),
                        ref.get("title", ""),
                        ref.get("summary", ""),
                        ref.get("url", ""),
                    ]
                )
                if text_contains_alias(ref_text, brand["aliases"]):
                    reference_mentions += 1
                    if ref.get("domain"):
                        reference_domains.add(ref["domain"])
                    if ref.get("url"):
                        reference_urls.add(ref["url"])

            qid = sample["question_id"]
            qrow = by_question[qid].setdefault(
                brand["name"],
                {"mentioned": 0, "top1": 0, "top3": 0, "top5": 0, "ranks": [], "mention_total": 0},
            )
            if rank is not None:
                qrow["mentioned"] += 1
                qrow["mention_total"] += mention_count
                qrow["ranks"].append(rank)
                if rank == 1:
                    qrow["top1"] += 1
                if rank <= 3:
                    qrow["top3"] += 1
                if rank <= 5:
                    qrow["top5"] += 1

        sentiment_total = sum(sentiment_counts.values())
        dominant_sentiment = "neutral"
        if sentiment_counts:
            dominant_sentiment = max(
                ("positive", "neutral", "negative"),
                key=lambda key: (sentiment_counts.get(key, 0), 1 if key == "neutral" else 0),
            )

        by_brand[brand["name"]] = {
            "aliases": brand["aliases"],
            "role": brand.get("role", "entity"),
            "entity_type": brand.get("entity_type"),
            "mentioned_samples": mentioned,
            "mention_rate": rate(mentioned, denominator),
            "mention_total": mention_total,
            "avg_mentions_per_sample": mention_total / denominator if denominator else 0,
            "avg_mentions_per_mentioned_sample": mention_total / mentioned if mentioned else 0,
            "top1_samples": top1,
            "top1_rate": rate(top1, denominator),
            "top3_samples": top3,
            "top3_rate": rate(top3, denominator),
            "top5_samples": top5,
            "top5_rate": rate(top5, denominator),
            "average_rank": sum(ranks) / len(ranks) if ranks else None,
            "sentiment_counts": dict(sentiment_counts),
            "sentiment_total": sentiment_total,
            "dominant_sentiment": dominant_sentiment,
            "negative_rate": rate(sentiment_counts.get("negative", 0), sentiment_total),
            "reference_mentions": reference_mentions,
            "reference_domain_count": len(reference_domains),
            "reference_url_count": len(reference_urls),
        }

    by_question_out = {}
    for qid, brands_map in by_question.items():
        qden = question_denominators[qid]
        by_question_out[qid] = {}
        for name, row in brands_map.items():
            by_question_out[qid][name] = {
                "mentioned_samples": row["mentioned"],
                "mention_rate": rate(row["mentioned"], qden),
                "avg_mentions_per_sample": row["mention_total"] / qden if qden else 0,
                "top1_rate": rate(row["top1"], qden),
                "top3_rate": rate(row["top3"], qden),
                "top5_rate": rate(row["top5"], qden),
                "average_rank": sum(row["ranks"]) / len(row["ranks"]) if row["ranks"] else None,
            }

    return {
        "valid_sample_count": denominator,
        "brand_count": len(brands),
        "by_brand": by_brand,
        "by_question": by_question_out,
    }


def classify_channel(ref: dict) -> str:
    text = " ".join([ref.get("source", ""), ref.get("domain", ""), ref.get("title", ""), ref.get("url", "")]).lower()
    domain = ref.get("domain", "")
    if re.search(r"(gov\.cn|\.gov|edu\.cn|\.edu|ac\.cn|协会|学会|大学|学院|研究院|官网|official)", text):
        return "official"
    if re.search(r"(arxiv|doi\.org|dl\.acm|journal|research|论文|学术|kdd|acm|ieee)", text):
        return "academic"
    if re.search(r"(baike|wikipedia|wiki)", text):
        return "encyclopedia"
    if re.search(r"(zhihu|xiaohongshu|weibo|douban|forum|bbs|社区|知乎|小红书|贴吧)", text):
        return "community"
    if re.search(r"(jd\.com|taobao|tmall|meituan|dianping|ctrip|amazon|shop|store|商城|电商)", text):
        return "commerce"
    if re.search(r"(developer|cloud\.tencent|csdn|github|gitlab|docs|dev|技术|开发者)", text):
        return "developer"
    if re.search(r"(news|sohu|sina|qq\.com|163\.com|bjnews|36kr|huxiu|媒体|日报|新闻|财经)", text):
        return "media"
    if domain.endswith(".org"):
        return "official"
    return "other"


def flatten_references(samples: list[dict]) -> list[dict]:
    rows = []
    for sample in samples:
        for ref in sample["references"]:
            row = dict(ref)
            row["sample_id"] = sample["sample_id"]
            row["question_id"] = sample["question_id"]
            row["question"] = sample["question"]
            row["channel"] = classify_channel(ref)
            rows.append(row)
    return rows


def parse_year(value: str) -> int | None:
    match = re.search(r"(20\d{2}|19\d{2})", value or "")
    return int(match.group(1)) if match else None


def title_features(refs: list[dict], brands: list[dict]) -> dict:
    total = len(refs)
    counters = Counter()
    length_buckets = Counter()
    aliases = [alias for brand in brands for alias in brand["aliases"]]
    current_year = dt.datetime.now().year
    year_buckets = Counter()
    intent_counts = Counter()
    for ref in refs:
        title = ref.get("title", "")
        length = len(title)
        if length <= 12:
            length_buckets["0-12"] += 1
        elif length <= 24:
            length_buckets["13-24"] += 1
        elif length <= 40:
            length_buckets["25-40"] += 1
        else:
            length_buckets["41+"] += 1
        if re.search(r"\d", title):
            counters["has_number"] += 1
        if re.search(r"(20\d{2}|19\d{2})", title):
            counters["has_year"] += 1
        if re.search(r"[?？]", title):
            counters["has_question"] += 1
        if re.search(r"[：:【】\[\]（）()]", title):
            counters["has_structure_punctuation"] += 1
        if any(alias and alias.lower() in title.lower() for alias in aliases):
            counters["contains_brand"] += 1
        matched_intent = False
        for label, pattern in TITLE_INTENT_PATTERNS:
            if re.search(pattern, title, flags=re.IGNORECASE):
                intent_counts[label] += 1
                matched_intent = True
        if not matched_intent:
            intent_counts["其他信息"] += 1
        year = parse_year(ref.get("date", "")) or parse_year(title)
        if year is None:
            year_buckets["unknown"] += 1
        elif year >= current_year:
            year_buckets["current_year"] += 1
        elif year >= current_year - 1:
            year_buckets["last_year"] += 1
        else:
            year_buckets["older"] += 1
    return {
        "total": total,
        "feature_counts": dict(counters),
        "feature_rates": {key: rate(value, total) for key, value in counters.items()},
        "length_buckets": dict(length_buckets),
        "recency_buckets": dict(year_buckets),
        "intent_counts": dict(intent_counts),
    }


def source_position_buckets(refs: list[dict]) -> dict:
    buckets = Counter()
    for ref in refs:
        try:
            number = int(ref.get("number") or 0)
        except Exception:
            number = 0
        if 1 <= number <= 3:
            buckets["1-3"] += 1
        elif 4 <= number <= 6:
            buckets["4-6"] += 1
        elif number >= 7:
            buckets["7+"] += 1
        else:
            buckets["unknown"] += 1
    return dict(buckets)


def safe_int(value: object) -> int:
    try:
        return int(value or 0)
    except Exception:
        return 0


def sample_has_fresh_chat(sample: dict) -> bool:
    return any(
        event.get("action") == "fresh_chat_opened" and event.get("ok")
        for event in sample.get("action_trace", [])
    )


def flatten_mobile_materials(samples: list[dict]) -> list[dict]:
    rows = []
    for sample in samples:
        materials = sample.get("mobile_search_materials") or {}
        for item_index, item in enumerate(materials.get("items") or [], start=1):
            url = clean_text(item.get("url"))
            domain = normalize_domain(item.get("domain") or domain_from_url(url))
            cited = bool(item.get("cited"))
            rows.append(
                {
                    "sample_id": sample.get("sample_id", ""),
                    "question_id": sample.get("question_id", ""),
                    "question": sample.get("question", ""),
                    "repeat_index": sample.get("repeat_index", ""),
                    "material_index": item.get("index") or item_index,
                    "title": clean_text(item.get("title")),
                    "source": clean_text(item.get("source")),
                    "domain": domain,
                    "url": url,
                    "cited": cited,
                    "citation_count": safe_int(item.get("citation_count")),
                    "confidence": clean_text(item.get("confidence")),
                    "failure_reason": clean_text(item.get("failure_reason")),
                    "clickable": bool(item.get("clickable")),
                }
            )
    return rows


def mobile_evidence_summary(samples: list[dict], input_meta: dict | None = None, run_meta: dict | None = None) -> dict:
    input_meta = input_meta or {}
    run_meta = run_meta or {}
    material_rows = flatten_mobile_materials(samples)
    material_samples = [
        sample for sample in samples
        if (sample.get("mobile_search_materials") or {}).get("items")
    ]
    reported_material_count = sum(safe_int((sample.get("mobile_search_materials") or {}).get("material_count")) for sample in samples)
    cited_rows = [row for row in material_rows if row.get("cited")]
    total_citation_count = sum(safe_int(row.get("citation_count")) for row in material_rows)
    title_counts = Counter(row["title"] for row in material_rows if row.get("title"))
    domain_counts = Counter(row["domain"] for row in material_rows if row.get("domain"))
    source_counts = Counter(row["source"] for row in material_rows if row.get("source"))

    grouped: dict[str, dict] = {}
    for sample in samples:
        qid = sample.get("question_id", "")
        row = grouped.setdefault(
            qid,
            {
                "question_id": qid,
                "question": sample.get("question", ""),
                "samples": 0,
                "fresh_chat_ok": 0,
                "material_rows": 0,
                "reported_material_count": 0,
                "cited_material_rows": 0,
                "uncited_material_rows": 0,
                "citation_count": 0,
            },
        )
        row["samples"] += 1
        row["fresh_chat_ok"] += 1 if sample_has_fresh_chat(sample) else 0
        materials = sample.get("mobile_search_materials") or {}
        items = materials.get("items") or []
        row["material_rows"] += len(items)
        row["reported_material_count"] += safe_int(materials.get("material_count"))
        row["cited_material_rows"] += sum(1 for item in items if item.get("cited"))
        row["uncited_material_rows"] += sum(1 for item in items if not item.get("cited"))
        row["citation_count"] += sum(safe_int(item.get("citation_count")) for item in items)

    sample_rows = []
    for sample in samples:
        materials = sample.get("mobile_search_materials") or {}
        items = materials.get("items") or []
        sample_rows.append(
            {
                "sample_id": sample.get("sample_id", ""),
                "question_id": sample.get("question_id", ""),
                "question": sample.get("question", ""),
                "ok": sample.get("ok", False),
                "fresh_chat_ok": sample_has_fresh_chat(sample),
                "reported_material_count": safe_int(materials.get("material_count")),
                "material_rows": len(items),
                "cited_material_rows": sum(1 for item in items if item.get("cited")),
                "uncited_material_rows": sum(1 for item in items if not item.get("cited")),
                "citation_count": sum(safe_int(item.get("citation_count")) for item in items),
            }
        )

    return {
        "transport": run_meta.get("transport") or next((sample.get("transport") for sample in samples if sample.get("transport")), ""),
        "delay_strategy": input_meta.get("delay_strategy") or {},
        "fresh_chat_ok_samples": sum(1 for sample in samples if sample_has_fresh_chat(sample)),
        "sample_count": len(samples),
        "samples_with_materials": len(material_samples),
        "reported_material_count": reported_material_count,
        "collected_material_rows": len(material_rows),
        "cited_material_rows": len(cited_rows),
        "uncited_material_rows": len(material_rows) - len(cited_rows),
        "total_citation_count": total_citation_count,
        "top_material_titles": [{"name": name, "count": count} for name, count in title_counts.most_common(REPORT_ITEM_LIMIT)],
        "top_material_domains": [{"name": name, "count": count} for name, count in domain_counts.most_common(REPORT_ITEM_LIMIT)],
        "top_material_sources": [{"name": name, "count": count} for name, count in source_counts.most_common(REPORT_ITEM_LIMIT)],
        "by_question": sorted(grouped.values(), key=lambda row: row["question_id"]),
        "by_sample": sample_rows,
        "materials": material_rows,
    }


def question_metrics(samples: list[dict], plan_entries: list[dict]) -> list[dict]:
    grouped: dict[str, list[dict]] = defaultdict(list)
    planned_grouped: dict[str, list[dict]] = defaultdict(list)
    questions = {}
    for item in plan_entries:
        qid = item["question_id"]
        planned_grouped[qid].append(item)
        if item.get("question"):
            questions[qid] = item["question"]
    for sample in samples:
        grouped[sample["question_id"]].append(sample)
        questions.setdefault(sample["question_id"], sample["question"])
    rows = []
    all_question_ids = sorted(set(planned_grouped) | set(grouped))
    for qid in all_question_ids:
        q_samples = grouped.get(qid, [])
        planned_count = len(planned_grouped.get(qid, [])) or len(q_samples)
        valid = [sample for sample in q_samples if sample["ok"]]
        failed = [sample for sample in q_samples if not sample["ok"]]
        pending = max(planned_count - len(q_samples), 0)
        refs = sum(len(sample["references"]) for sample in valid)
        chars = sum(len(sample["answer"]) for sample in valid)
        material_rows = sum(len((sample.get("mobile_search_materials") or {}).get("items") or []) for sample in q_samples)
        cited_material_rows = sum(
            sum(1 for item in ((sample.get("mobile_search_materials") or {}).get("items") or []) if item.get("cited"))
            for sample in q_samples
        )
        fresh_chat_ok = sum(1 for sample in q_samples if sample_has_fresh_chat(sample))
        rows.append(
            {
                "question_id": qid,
                "question": questions.get(qid, ""),
                "planned": planned_count,
                "completed": len(q_samples),
                "valid": len(valid),
                "failed": len(failed),
                "pending": pending,
                "valid_rate": rate(len(valid), planned_count),
                "reference_count": refs,
                "avg_references": refs / len(valid) if valid else 0,
                "answer_chars": chars,
                "avg_answer_chars": chars / len(valid) if valid else 0,
                "mobile_material_rows": material_rows,
                "mobile_cited_material_rows": cited_material_rows,
                "mobile_uncited_material_rows": material_rows - cited_material_rows,
                "fresh_chat_ok": fresh_chat_ok,
            }
        )
    return rows


def top_counter(counter: Counter, limit: int = REPORT_ITEM_LIMIT) -> list[dict]:
    return [{"name": key or "(blank)", "count": count} for key, count in counter.most_common(limit)]


def clean_source_label(value: str, domain: str = "") -> str:
    label = clean_text(value)
    if not label:
        return ""
    lower = label.lower()
    if lower.startswith(("http://", "https://")):
        return ""
    if domain and lower in {domain, f"www.{domain}"}:
        return ""
    if len(label) > 24 and re.fullmatch(r"[A-Za-z0-9 .:/_-]+", label):
        return ""
    return label


def domain_display_name(domain: str, source_counter: Counter | None = None) -> str:
    domain = normalize_domain(domain)
    if not domain:
        return ""
    if domain in DOMAIN_NAME_OVERRIDES:
        return DOMAIN_NAME_OVERRIDES[domain]
    parts = domain.split(".")
    for index in range(1, len(parts) - 1):
        suffix = ".".join(parts[index:])
        if suffix in DOMAIN_NAME_OVERRIDES:
            return DOMAIN_NAME_OVERRIDES[suffix]
    if source_counter:
        for source, _ in source_counter.most_common():
            label = clean_source_label(source, domain)
            if label:
                return label
    return domain


def source_display_name(source: str, domain: str = "") -> str:
    source = clean_text(source)
    if source in SOURCE_NAME_OVERRIDES:
        return SOURCE_NAME_OVERRIDES[source]
    if domain:
        display = domain_display_name(domain)
        if display and (not source or source.lower() in {domain.lower(), f"www.{domain.lower()}"}):
            return display
    return source


def source_home_url(domain: str) -> str:
    return f"https://{domain}" if domain else ""


def short_url_label(url: str) -> str:
    if not url:
        return "(blank)"
    parsed = urlparse(url)
    domain = normalize_domain(parsed.hostname or "")
    path = re.sub(r"/+", "/", parsed.path or "/").strip("/")
    if not path:
        return domain or url
    path_parts = [part for part in path.split("/") if part]
    if len(path_parts) > 3:
        suffix = f"{path_parts[0]}/.../{path_parts[-1]}"
    else:
        suffix = "/".join(path_parts)
    return f"{domain}/{suffix}" if suffix else domain


def top_domain_rows(refs: list[dict], limit: int = REPORT_ITEM_LIMIT) -> list[dict]:
    counts = Counter(ref["domain"] for ref in refs if ref.get("domain"))
    sources_by_domain: dict[str, Counter] = defaultdict(Counter)
    for ref in refs:
        domain = ref.get("domain")
        if domain:
            sources_by_domain[domain][ref.get("source") or ""] += 1
    rows = []
    for domain, count in counts.most_common(limit):
        display = domain_display_name(domain, sources_by_domain.get(domain))
        rows.append(
            {
                "name": domain,
                "display_name": display,
                "count": count,
                "url": source_home_url(domain),
            }
        )
    return rows


def top_url_rows(refs: list[dict], limit: int = REPORT_ITEM_LIMIT) -> list[dict]:
    counts = Counter(ref["url"] for ref in refs if ref.get("url"))
    info: dict[str, dict] = {}
    for ref in refs:
        url = ref.get("url")
        if not url or url in info:
            continue
        info[url] = {
            "title": ref.get("title") or "",
            "source": ref.get("source") or "",
            "domain": ref.get("domain") or domain_from_url(url),
        }
    rows = []
    for url, count in counts.most_common(limit):
        row = info.get(url, {})
        label = row.get("title") or short_url_label(url)
        rows.append(
            {
                "name": label,
                "display_name": label,
                "url": url,
                "count": count,
                "domain": row.get("domain", ""),
                "source": row.get("source", ""),
            }
        )
    return rows


def top_title_rows(refs: list[dict], limit: int = REPORT_ITEM_LIMIT) -> list[dict]:
    counts = Counter(ref["title"] for ref in refs if ref.get("title"))
    urls_by_title: dict[str, Counter] = defaultdict(Counter)
    sources_by_title: dict[str, Counter] = defaultdict(Counter)
    domains_by_title: dict[str, Counter] = defaultdict(Counter)
    for ref in refs:
        title = ref.get("title")
        if not title:
            continue
        if ref.get("url"):
            urls_by_title[title][ref["url"]] += 1
        if ref.get("source"):
            sources_by_title[title][ref["source"]] += 1
        if ref.get("domain"):
            domains_by_title[title][ref["domain"]] += 1
    rows = []
    for title, count in counts.most_common(limit):
        url = urls_by_title[title].most_common(1)[0][0] if urls_by_title[title] else ""
        source = sources_by_title[title].most_common(1)[0][0] if sources_by_title[title] else ""
        domain = domains_by_title[title].most_common(1)[0][0] if domains_by_title[title] else domain_from_url(url)
        rows.append({"name": title, "count": count, "url": url, "source": source, "domain": domain})
    return rows


def build_entity_analysis(candidates: list[dict], brand_metrics: dict, target_kind: str, source: str) -> dict:
    metrics = brand_metrics.get("by_brand", {})
    rows = []
    for candidate in candidates:
        metric = metrics.get(candidate["name"], {})
        row = dict(candidate)
        row["role"] = metric.get("role") or "candidate"
        row["entity_type"] = metric.get("entity_type") or row.get("kind")
        row["metrics"] = {
            "mentioned_samples": metric.get("mentioned_samples", 0),
            "mention_rate": metric.get("mention_rate", 0),
            "mention_total": metric.get("mention_total", 0),
            "avg_mentions_per_sample": metric.get("avg_mentions_per_sample", 0),
            "top1_rate": metric.get("top1_rate", 0),
            "top3_rate": metric.get("top3_rate", 0),
            "top5_rate": metric.get("top5_rate", 0),
            "average_rank": metric.get("average_rank"),
            "dominant_sentiment": metric.get("dominant_sentiment", "neutral"),
            "negative_rate": metric.get("negative_rate", 0),
            "reference_mentions": metric.get("reference_mentions", 0),
        }
        rows.append(row)
    rows.sort(
        key=lambda item: (
            1 if item.get("is_target") else 0,
            item["metrics"].get("top3_rate") or 0,
            item["metrics"].get("top5_rate") or 0,
            item["metrics"].get("mention_rate") or 0,
            item.get("confidence") or 0,
            item.get("sample_count") or 0,
        ),
        reverse=True,
    )
    return {
        "target_kind": target_kind,
        "source": source,
        "target_count": sum(1 for row in rows if row.get("role") == "target"),
        "competitor_count": sum(1 for row in rows if row.get("role") == "competitor"),
        "same_type_candidate_count": sum(1 for row in rows if row.get("is_target")),
        "noise_count": sum(1 for row in rows if row.get("kind") == "noise"),
        "candidate_count": len(rows),
        "candidates": rows,
        "target_entities": [row for row in rows if row.get("role") == "target"],
        "competitor_entities": [row for row in rows if row.get("role") == "competitor"],
    }


def sorted_metric_entries(brand_metrics: dict, key: str = "top3_rate") -> list[tuple[str, dict]]:
    rows = list((brand_metrics.get("by_brand") or {}).items())
    return sorted(
        rows,
        key=lambda item: (
            item[1].get(key) or 0,
            item[1].get("mention_rate") or 0,
            item[1].get("top1_rate") or 0,
        ),
        reverse=True,
    )


def build_target_diagnostics(brand_metrics: dict, target_profile: dict, limit: int) -> dict:
    rows = brand_metrics.get("by_brand", {})
    target_name = ""
    target_metric = None
    for name, metric in rows.items():
        if metric.get("role") == "target":
            target_name = name
            target_metric = metric
            break
    competitors = [
        {"name": name, **metric}
        for name, metric in sorted_metric_entries(brand_metrics, "top3_rate")
        if metric.get("role") == "competitor"
    ]
    top_competitor = competitors[0] if competitors else None
    comparison_rows = []
    if target_metric:
        comparison_rows.append({"name": target_name, **target_metric, "gap_vs_target_top3": 0.0, "gap_vs_target_top5": 0.0})
    target_top3 = (target_metric or {}).get("top3_rate") or 0
    target_top5 = (target_metric or {}).get("top5_rate") or 0
    for competitor in competitors[: max(limit - len(comparison_rows), 0)]:
        competitor["gap_vs_target_top3"] = competitor.get("top3_rate", 0) - target_top3
        competitor["gap_vs_target_top5"] = competitor.get("top5_rate", 0) - target_top5
        comparison_rows.append(competitor)
    return {
        "entity": target_profile.get("entity") or target_name,
        "aliases": target_profile.get("aliases") or [],
        "entity_type": target_profile.get("entity_type"),
        "entity_type_label": target_profile.get("entity_type_label"),
        "has_target": bool(target_metric),
        "metrics": target_metric or {},
        "top_competitor": top_competitor,
        "competitor_count": len(competitors),
        "comparison_rows": comparison_rows[:limit],
    }


def compute_summary(
    samples: list[dict],
    brands: list[dict],
    brand_source: str,
    plan_entries: list[dict],
    target_kind: str,
    entity_candidates: list[dict],
    target_profile: dict,
    item_limit: int,
    input_meta: dict | None = None,
    run_meta: dict | None = None,
) -> dict:
    new_conversation = (input_meta or {}).get("new_conversation") is not False
    valid_samples = [sample for sample in samples if sample["ok"]]
    failed_samples = [sample for sample in samples if not sample["ok"]]
    planned_count = len(plan_entries) or len(samples)
    completed_count = len(samples)
    pending_count = max(planned_count - completed_count, 0)
    refs = flatten_references(samples)
    unique_urls = {ref["url"] for ref in refs if ref.get("url")}
    unique_domains = {ref["domain"] for ref in refs if ref.get("domain")}
    brand_metrics = compute_brand_metrics(samples, brands)
    entity_analysis = build_entity_analysis(entity_candidates, brand_metrics, target_kind, brand_source)
    channel_counts = Counter(ref["channel"] for ref in refs)
    source_counts = Counter(ref["source"] or ref["domain"] for ref in refs)
    title_stats = title_features(refs, brands)
    target_diagnostics = build_target_diagnostics(brand_metrics, target_profile, item_limit)
    mobile_evidence = mobile_evidence_summary(samples, input_meta, run_meta)
    return {
        "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "report": {
            "item_limit": item_limit,
        },
        "input": {
            "delay_strategy": (input_meta or {}).get("delay_strategy") or {},
            "new_conversation": new_conversation,
        },
        "samples": {
            "planned": planned_count,
            "completed": completed_count,
            "valid": len(valid_samples),
            "failed": len(failed_samples),
            "pending": pending_count,
            "valid_rate": rate(len(valid_samples), planned_count),
            "completion_rate": rate(completed_count, planned_count),
            "question_count": len({item["question_id"] for item in plan_entries} | {sample["question_id"] for sample in samples}),
            "answer_chars": sum(len(sample["answer"]) for sample in valid_samples),
            "reference_count": len(refs),
            "unique_urls": len(unique_urls),
            "unique_domains": len(unique_domains),
            "mobile_search_material_count": mobile_evidence.get("collected_material_rows", 0),
            "mobile_cited_search_material_count": mobile_evidence.get("cited_material_rows", 0),
            "mobile_uncited_search_material_count": mobile_evidence.get("uncited_material_rows", 0),
            "fresh_chat_ok_samples": mobile_evidence.get("fresh_chat_ok_samples", 0),
        },
        "target": target_diagnostics,
        "brand_source": brand_source,
        "entities": entity_analysis,
        "brands": brand_metrics,
        "questions": question_metrics(samples, plan_entries),
        "sources": {
            "channel_counts": dict(channel_counts),
            "top_domains": top_domain_rows(refs),
            "top_sources": top_counter(source_counts),
            "top_titles": top_title_rows(refs),
            "top_urls": top_url_rows(refs),
            "position_buckets": source_position_buckets(refs),
        },
        "mobile_evidence": mobile_evidence,
        "titles": title_stats,
    }


def export_value(value: object) -> object:
    if value is None:
        return ""
    if isinstance(value, (str, int, float, bool)):
        return value
    return json.dumps(value, ensure_ascii=False, sort_keys=True)


def strip_xml_control_chars(value: str) -> str:
    return re.sub(r"[\x00-\x08\x0B\x0C\x0E-\x1F]", "", value)


def export_text(value: object) -> str:
    value = export_value(value)
    if isinstance(value, bool):
        return "TRUE" if value else "FALSE"
    return strip_xml_control_chars(str(value))


def export_columns(rows: list[dict], preferred: list[str]) -> list[str]:
    columns = list(preferred)
    for row in rows:
        for key in row.keys():
            if key not in columns:
                columns.append(key)
    return columns


def export_table(name: str, rows: list[dict], preferred: list[str] | None = None, description: str = "") -> dict:
    preferred = preferred or []
    columns = export_columns(rows, preferred)
    return {"name": name, "description": description, "columns": columns, "rows": rows}


def metric_row(name: str, row: dict) -> dict:
    out = {"entity": name}
    out.update(row or {})
    out.pop("name", None)
    if isinstance(out.get("aliases"), list):
        out["aliases"] = "、".join(str(item) for item in out["aliases"])
    if isinstance(out.get("sentiment_counts"), dict):
        out["sentiment_counts"] = json.dumps(out["sentiment_counts"], ensure_ascii=False, sort_keys=True)
    return out


def bucket_rows(counter: dict, label_map: dict[str, str] | None = None) -> list[dict]:
    label_map = label_map or {}
    total = sum(counter.values()) or 0
    rows = []
    for name, count in counter.items():
        rows.append(
            {
                "bucket": label_map.get(name, name),
                "raw_bucket": name,
                "count": count,
                "rate": rate(count, total) if total else 0,
            }
        )
    return rows


def structured_export_tables(summary: dict, output_files: dict[str, str]) -> list[dict]:
    samples = summary.get("samples", {})
    target = summary.get("target", {})
    entities = summary.get("entities", {})
    brands = summary.get("brands", {})
    sources = summary.get("sources", {})
    mobile = summary.get("mobile_evidence", {})
    titles = summary.get("titles", {})
    target_metrics = target.get("metrics") or {}
    item_limit = int((summary.get("report") or {}).get("item_limit") or REPORT_ITEM_LIMIT)

    overview_rows = [
        {"field": "generated_at", "value": summary.get("generated_at"), "description": "分析生成时间"},
        {"field": "input_file", "value": summary.get("input_file"), "description": "输入原始 JSON 文件名"},
        {"field": "target_entity", "value": target.get("entity"), "description": "目标实体"},
        {"field": "target_aliases", "value": "、".join(target.get("aliases") or []), "description": "目标实体别名"},
        {"field": "entity_type", "value": target.get("entity_type"), "description": "目标实体类型"},
        {"field": "entity_type_label", "value": target.get("entity_type_label"), "description": "目标实体类型中文"},
        {"field": "brand_source", "value": summary.get("brand_source"), "description": "实体来源口径"},
        {"field": "planned_samples", "value": samples.get("planned"), "description": "计划采样次数"},
        {"field": "completed_samples", "value": samples.get("completed"), "description": "已完成采样次数"},
        {"field": "valid_samples", "value": samples.get("valid"), "description": "有效采样次数"},
        {"field": "failed_samples", "value": samples.get("failed"), "description": "失败采样次数"},
        {"field": "pending_samples", "value": samples.get("pending"), "description": "未完成采样次数"},
        {"field": "valid_rate", "value": samples.get("valid_rate"), "description": "有效采样率"},
        {"field": "completion_rate", "value": samples.get("completion_rate"), "description": "完成率"},
        {"field": "question_count", "value": samples.get("question_count"), "description": "关键词/问题数量"},
        {"field": "answer_chars", "value": samples.get("answer_chars"), "description": "有效回答总字数"},
        {"field": "reference_count", "value": samples.get("reference_count"), "description": "Doubao 可见 URL 或兼容引用总数"},
        {"field": "unique_urls", "value": samples.get("unique_urls"), "description": "唯一 URL 数"},
        {"field": "unique_domains", "value": samples.get("unique_domains"), "description": "唯一域名数"},
        {"field": "mobile_search_material_count", "value": samples.get("mobile_search_material_count"), "description": "移动端搜索资料行数"},
        {"field": "mobile_cited_search_material_count", "value": samples.get("mobile_cited_search_material_count"), "description": "移动端判定被引用的搜索资料行数"},
        {"field": "mobile_uncited_search_material_count", "value": samples.get("mobile_uncited_search_material_count"), "description": "移动端判定未引用的搜索资料行数"},
        {"field": "fresh_chat_ok_samples", "value": samples.get("fresh_chat_ok_samples"), "description": "移动端新建对话成功样本数"},
        {"field": "competitor_count", "value": target.get("competitor_count"), "description": "同类型竞品数量"},
        {"field": "entity_candidate_count", "value": entities.get("candidate_count"), "description": "实体识别候选总数"},
        {"field": "report_item_limit", "value": item_limit, "description": "HTML 报告默认明细上限"},
    ]

    output_rows = [
        {"file_type": key, "path": value, "description": description}
        for key, value, description in [
            ("raw_json", output_files.get("raw_json", ""), "抓取阶段原始聚合 JSON 日志"),
            ("summary_json", output_files.get("summary_json", ""), "分析阶段机器可读 summary JSON"),
            ("structured_markdown", output_files.get("structured_markdown", ""), "结构化字段与数据 Markdown"),
            ("structured_excel", output_files.get("structured_excel", ""), "结构化字段与数据 Excel"),
            ("html_report", output_files.get("html_report", ""), "正式可视化诊断分析报告"),
        ]
    ]

    target_rows = [metric_row(target.get("entity") or "", target_metrics)] if target_metrics else []
    comparison_rows = [metric_row(row.get("name", ""), row) for row in target.get("comparison_rows", [])]
    by_question_rows = []
    for question_id, by_entity in (brands.get("by_question") or {}).items():
        question_text = next((row.get("question") for row in summary.get("questions", []) if row.get("question_id") == question_id), "")
        for entity, metrics in by_entity.items():
            row = metric_row(entity, metrics)
            row["question_id"] = question_id
            row["question"] = question_text
            by_question_rows.append(row)

    candidate_rows = []
    for row in entities.get("candidates", []):
        item = dict(row)
        if isinstance(item.get("aliases"), list):
            item["aliases"] = "、".join(str(value) for value in item["aliases"])
        if isinstance(item.get("surface_reasons"), list):
            item["surface_reasons"] = "、".join(str(value) for value in item["surface_reasons"])
        if isinstance(item.get("reasons"), list):
            item["reasons"] = "、".join(str(value) for value in item["reasons"])
        if isinstance(item.get("metrics"), dict):
            for metric_key, metric_value in item.pop("metrics").items():
                item[f"metric_{metric_key}"] = metric_value
        candidate_rows.append(item)

    mobile_overview_rows = [
        {"field": "transport", "value": mobile.get("transport"), "description": "移动端采集通道"},
        {"field": "delay_strategy", "value": mobile.get("delay_strategy"), "description": "采集间隔策略"},
        {"field": "sample_count", "value": mobile.get("sample_count"), "description": "移动端样本数"},
        {"field": "fresh_chat_ok_samples", "value": mobile.get("fresh_chat_ok_samples"), "description": "新建对话成功样本数"},
        {"field": "samples_with_materials", "value": mobile.get("samples_with_materials"), "description": "采集到搜索资料的样本数"},
        {"field": "reported_material_count", "value": mobile.get("reported_material_count"), "description": "App UI 汇总显示的参考资料总数"},
        {"field": "collected_material_rows", "value": mobile.get("collected_material_rows"), "description": "实际从 UI 层级采集到的资料行数"},
        {"field": "cited_material_rows", "value": mobile.get("cited_material_rows"), "description": "被回答引用的资料行数"},
        {"field": "uncited_material_rows", "value": mobile.get("uncited_material_rows"), "description": "未被回答引用的资料行数"},
        {"field": "total_citation_count", "value": mobile.get("total_citation_count"), "description": "资料引用次数合计"},
    ]

    channel_rows = bucket_rows(sources.get("channel_counts", {}), CHANNEL_LABELS_ZH)
    position_rows = bucket_rows(sources.get("position_buckets", {}), SOURCE_POSITION_LABELS_ZH)
    title_feature_rows = []
    for key, count in (titles.get("feature_counts") or {}).items():
        title_feature_rows.append(
            {
                "feature": key,
                "count": count,
                "rate": (titles.get("feature_rates") or {}).get(key, 0),
            }
        )

    return [
        export_table("输出文件", output_rows, ["file_type", "path", "description"], "本次分析产物清单。"),
        export_table("概览字段", overview_rows, ["field", "value", "description"], "采样、实体、信源和报告级核心字段。"),
        export_table("问题采集", summary.get("questions", []), ["question_id", "question", "planned", "completed", "valid", "failed", "pending", "valid_rate", "reference_count", "avg_references", "mobile_material_rows", "mobile_cited_material_rows", "mobile_uncited_material_rows", "fresh_chat_ok", "answer_chars", "avg_answer_chars"], "每个关键词/问题的采集覆盖情况。"),
        export_table("移动端证据概览", mobile_overview_rows, ["field", "value", "description"], "Android/Appium 采集证据、搜索资料和新建对话状态。"),
        export_table("移动端资料按问题", mobile.get("by_question", []), ["question_id", "question", "samples", "fresh_chat_ok", "reported_material_count", "material_rows", "cited_material_rows", "uncited_material_rows", "citation_count"], "每个关键词的移动端搜索资料引用/未引用统计。"),
        export_table("移动端资料按样本", mobile.get("by_sample", []), ["sample_id", "question_id", "question", "ok", "fresh_chat_ok", "reported_material_count", "material_rows", "cited_material_rows", "uncited_material_rows", "citation_count"], "每个样本的新建对话和搜索资料采集状态。"),
        export_table("移动端资料明细", mobile.get("materials", []), ["sample_id", "question_id", "question", "repeat_index", "material_index", "title", "source", "domain", "url", "cited", "citation_count", "confidence", "failure_reason", "clickable"], "移动端搜索资料明细，包含是否被回答引用和引用次数。"),
        export_table("目标实体指标", target_rows, ["entity", "role", "entity_type", "aliases", "mentioned_samples", "mention_rate", "mention_total", "avg_mentions_per_sample", "avg_mentions_per_mentioned_sample", "top1_samples", "top1_rate", "top3_samples", "top3_rate", "top5_samples", "top5_rate", "average_rank", "dominant_sentiment", "negative_rate", "sentiment_total", "sentiment_counts", "reference_mentions", "reference_domain_count", "reference_url_count"], "目标实体的核心诊断指标。"),
        export_table("同类型实体对比", comparison_rows, ["entity", "role", "entity_type", "aliases", "mentioned_samples", "mention_rate", "mention_total", "avg_mentions_per_sample", "top1_rate", "top3_rate", "top5_rate", "average_rank", "dominant_sentiment", "negative_rate", "reference_mentions", "gap_vs_target_top3", "gap_vs_target_top5"], "目标实体与同类型竞品的指标矩阵。"),
        export_table("问题实体明细", by_question_rows, ["question_id", "question", "entity", "mentioned_samples", "mention_rate", "avg_mentions_per_sample", "top1_rate", "top3_rate", "top5_rate", "average_rank"], "每个问题下各实体的表现。"),
        export_table("实体识别候选", candidate_rows, ["name", "kind", "role", "entity_type", "is_target", "confidence", "sample_count", "raw_count", "evidence_score", "surface_score", "surface_reasons", "reasons"], "实体识别、清洗、过滤和分类候选。"),
        export_table("信源渠道分布", channel_rows, ["bucket", "raw_bucket", "count", "rate"], "Doubao 引用信源的渠道结构。"),
        export_table("来源编号位置", position_rows, ["bucket", "raw_bucket", "count", "rate"], "Doubao 可见引用编号位置分布。"),
        export_table("高频域名", sources.get("top_domains", []), ["display_name", "name", "count", "url"], "高频引用域名。"),
        export_table("高频来源名", sources.get("top_sources", []), ["name", "count"], "高频引用来源名称。"),
        export_table("高频URL", sources.get("top_urls", []), ["display_name", "name", "url", "domain", "source", "count"], "高频引用 URL。"),
        export_table("高频引用标题", sources.get("top_titles", []), ["name", "url", "source", "domain", "count"], "被重复引用的标题。"),
        export_table("标题功能特征", title_feature_rows, ["feature", "count", "rate"], "引用标题的功能信号。"),
        export_table("标题长度", bucket_rows(titles.get("length_buckets", {})), ["bucket", "raw_bucket", "count", "rate"], "引用标题长度分布。"),
        export_table("时间新旧", bucket_rows(titles.get("recency_buckets", {}), RECENCY_LABELS), ["bucket", "raw_bucket", "count", "rate"], "引用标题或日期的新旧分布。"),
        export_table("标题意图", bucket_rows(titles.get("intent_counts", {})), ["bucket", "raw_bucket", "count", "rate"], "引用标题意图特征分布。"),
    ]


def markdown_cell(value: object) -> str:
    text = export_text(value)
    return text.replace("\\", "\\\\").replace("|", "\\|").replace("\n", "<br>")


def write_structured_markdown(path: Path, summary: dict, tables: list[dict]) -> None:
    lines = [
        "# Doubao 结构化字段与数据",
        "",
        f"- 生成时间：{export_text(summary.get('generated_at'))}",
        f"- 输入文件：{export_text(summary.get('input_file'))}",
        f"- 目标实体：{export_text((summary.get('target') or {}).get('entity'))}",
        f"- 实体类型：{export_text((summary.get('target') or {}).get('entity_type_label'))}",
        "",
        "本文件保存分析阶段从原始 Doubao JSON 中清洗出的结构化字段和对应数据，表结构与同目录 Excel 文件保持一致。",
        "",
    ]
    for table in tables:
        columns = table["columns"]
        rows = table["rows"]
        lines.extend([f"## {table['name']}", ""])
        if table.get("description"):
            lines.extend([table["description"], ""])
        lines.append(f"- 行数：{len(rows)}")
        lines.append("")
        if not columns:
            lines.extend(["无数据。", ""])
            continue
        lines.append("| " + " | ".join(markdown_cell(column) for column in columns) + " |")
        lines.append("| " + " | ".join("---" for _ in columns) + " |")
        for row in rows:
            lines.append("| " + " | ".join(markdown_cell(row.get(column, "")) for column in columns) + " |")
        lines.append("")
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def xlsx_col_name(index: int) -> str:
    name = ""
    index += 1
    while index:
        index, remainder = divmod(index - 1, 26)
        name = chr(65 + remainder) + name
    return name


def xlsx_sheet_name(name: str, used: set[str]) -> str:
    cleaned = re.sub(r"[\[\]:*?/\\]", "_", clean_text(name))[:31] or "Sheet"
    base = cleaned
    suffix = 1
    while cleaned in used:
        tail = f"_{suffix}"
        cleaned = f"{base[:31 - len(tail)]}{tail}"
        suffix += 1
    used.add(cleaned)
    return cleaned


def xlsx_cell_xml(value: object, row_index: int, col_index: int) -> str:
    ref = f"{xlsx_col_name(col_index)}{row_index}"
    if isinstance(value, bool):
        return f'<c r="{ref}" t="b"><v>{1 if value else 0}</v></c>'
    if isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(float(value)):
        return f'<c r="{ref}"><v>{value}</v></c>'
    text = html.escape(export_text(value), quote=True)
    return f'<c r="{ref}" t="inlineStr"><is><t xml:space="preserve">{text}</t></is></c>'


def xlsx_sheet_xml(table: dict) -> str:
    columns = table["columns"]
    rows = [dict(zip(columns, columns))]
    rows.extend(table["rows"])
    row_xml = []
    for row_number, row in enumerate(rows, start=1):
        cells = [xlsx_cell_xml(row.get(column, ""), row_number, col_index) for col_index, column in enumerate(columns)]
        row_xml.append(f'<row r="{row_number}">{"".join(cells)}</row>')
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
        '<sheetViews><sheetView workbookViewId="0"><pane ySplit="1" topLeftCell="A2" activePane="bottomLeft" state="frozen"/></sheetView></sheetViews>'
        f'<sheetData>{"".join(row_xml)}</sheetData>'
        '</worksheet>'
    )


def write_structured_xlsx(path: Path, tables: list[dict]) -> None:
    used_names: set[str] = set()
    sheets = [(xlsx_sheet_name(table["name"], used_names), table) for table in tables]
    workbook_sheets = []
    workbook_rels = []
    content_types = [
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
        '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">',
        '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>',
        '<Default Extension="xml" ContentType="application/xml"/>',
        '<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>',
        '<Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>',
    ]
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as workbook:
        workbook.writestr("_rels/.rels", '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/></Relationships>')
        for index, (sheet_name, table) in enumerate(sheets, start=1):
            workbook.writestr(f"xl/worksheets/sheet{index}.xml", xlsx_sheet_xml(table))
            escaped_name = html.escape(sheet_name, quote=True)
            workbook_sheets.append(f'<sheet name="{escaped_name}" sheetId="{index}" r:id="rId{index}"/>')
            workbook_rels.append(f'<Relationship Id="rId{index}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet{index}.xml"/>')
            content_types.append(f'<Override PartName="/xl/worksheets/sheet{index}.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>')
        workbook_rels.append(f'<Relationship Id="rId{len(sheets) + 1}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>')
        workbook.writestr("xl/workbook.xml", '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><sheets>' + "".join(workbook_sheets) + '</sheets></workbook>')
        workbook.writestr("xl/_rels/workbook.xml.rels", '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">' + "".join(workbook_rels) + '</Relationships>')
        workbook.writestr("xl/styles.xml", '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"><fonts count="1"><font><sz val="11"/><name val="Arial"/></font></fonts><fills count="1"><fill><patternFill patternType="none"/></fill></fills><borders count="1"><border/></borders><cellStyleXfs count="1"><xf/></cellStyleXfs><cellXfs count="1"><xf xfId="0"/></cellXfs></styleSheet>')
        content_types.append("</Types>")
        workbook.writestr("[Content_Types].xml", "".join(content_types))


def esc(value: object) -> str:
    return html.escape(str(value if value is not None else ""), quote=True)


def fmt_num(value: float | int | None, digits: int = 1) -> str:
    if value is None:
        return "n/a"
    if isinstance(value, int):
        return f"{value:,}"
    if math.isnan(value):
        return "n/a"
    return f"{value:,.{digits}f}"


def sorted_brand_rows(summary: dict, key: str) -> list[tuple[str, dict]]:
    rows = list(summary["brands"]["by_brand"].items())
    return sorted(rows, key=lambda item: (item[1].get(key) or 0, item[1].get("mention_rate") or 0), reverse=True)


def clamp(value: float, minimum: float = 0.0, maximum: float = 1.0) -> float:
    return max(minimum, min(maximum, value))


def bar_rows(rows: list[tuple[str, float, str]], max_value: float | None = None) -> str:
    if not rows:
        return '<p class="empty">No data.</p>'
    max_value = max_value if max_value is not None else max([value for _, value, _ in rows] or [1])
    max_value = max(max_value, 0.000001)
    out = []
    for name, value, label in rows:
        width = max(2, min(100, value / max_value * 100))
        out.append(
            f'<div class="bar-row"><div class="bar-name">{esc(name)}</div>'
            f'<div class="bar-track"><div class="bar-fill" style="width:{width:.2f}%"></div></div>'
            f'<div class="bar-value">{esc(label)}</div></div>'
        )
    return "\n".join(out)


def link_html(label: str, url: str) -> str:
    if not url:
        return esc(label)
    return f'<a class="inline-link" href="{esc(url)}" title="{esc(url)}" target="_blank" rel="noopener noreferrer">{esc(label)}</a>'


def bar_link_rows(rows: list[dict], max_value: float | None = None) -> str:
    if not rows:
        return '<p class="empty">No data.</p>'
    max_value = max_value if max_value is not None else max([row.get("value", row.get("count", 0)) for row in rows] or [1])
    max_value = max(max_value, 0.000001)
    out = []
    for row in rows:
        value = row.get("value", row.get("count", 0))
        label = row.get("display_name") or row.get("name") or row.get("url") or "(blank)"
        shown = row.get("label") or str(row.get("count", value))
        width = max(2, min(100, value / max_value * 100))
        out.append(
            f'<div class="bar-row"><div class="bar-name">{link_html(label, row.get("url", ""))}</div>'
            f'<div class="bar-track"><div class="bar-fill" style="width:{width:.2f}%"></div></div>'
            f'<div class="bar-value">{esc(shown)}</div></div>'
        )
    return "\n".join(out)


def source_bar_rows(rows: list[dict], max_value: float | None = None) -> str:
    if not rows:
        return '<p class="empty">No data.</p>'
    max_value = max_value if max_value is not None else max([row.get("value", row.get("count", 0)) for row in rows] or [1])
    max_value = max(max_value, 0.000001)
    out = []
    for row in rows:
        value = row.get("value", row.get("count", 0))
        title = row.get("display_name") or row.get("name") or row.get("url") or "(blank)"
        secondary_value = row.get("secondary")
        secondary = secondary_value if secondary_value is not None else (row.get("domain") or row.get("url") or "")
        url = row.get("url") or ""
        width = max(2, min(100, value / max_value * 100))
        title_html = link_html(title, url) if url else esc(title)
        secondary_html = link_html(secondary, url) if (url and secondary) else esc(secondary)
        secondary_markup = f'<span>{secondary_html}</span>' if secondary else ""
        out.append(
            '<div class="source-row">'
            f'<div class="source-label"><strong>{title_html}</strong>{secondary_markup}</div>'
            f'<div class="source-track"><div class="source-fill" style="width:{width:.2f}%"></div></div>'
            f'<div class="source-count">{esc(row.get("count", value))}</div>'
            '</div>'
        )
    return "\n".join(out)


def metric_card(value: object, label: str, note: str = "") -> str:
    return (
        '<div class="metric-card">'
        f'<div class="metric-value">{esc(value)}</div>'
        f'<div class="metric-label">{esc(label)}</div>'
        f'<div class="metric-note">{esc(note)}</div>'
        '</div>'
    )


def sentiment_label(value: str) -> str:
    return SENTIMENT_LABELS.get(value, "中性")


def sentiment_label_en(value: str) -> str:
    return SENTIMENT_LABELS_EN.get(value, "Neutral")


def metric_card_row(metrics: dict, lang: str = "zh") -> str:
    if lang == "en":
        rows = [
            ("Mention", pct(metrics.get("mention_rate") or 0)),
            ("Avg Mentions", fmt_num(metrics.get("avg_mentions_per_sample") or 0, 2)),
            ("Top 1", pct(metrics.get("top1_rate") or 0)),
            ("Top 3", pct(metrics.get("top3_rate") or 0)),
            ("Top 5", pct(metrics.get("top5_rate") or 0)),
            ("Avg Rank", fmt_num(metrics.get("average_rank"))),
            ("Sentiment", sentiment_label_en(metrics.get("dominant_sentiment") or "neutral")),
        ]
    else:
        rows = [
            ("提及率", pct(metrics.get("mention_rate") or 0)),
            ("平均提及", fmt_num(metrics.get("avg_mentions_per_sample") or 0, 2)),
            ("Top 1", pct(metrics.get("top1_rate") or 0)),
            ("Top 3", pct(metrics.get("top3_rate") or 0)),
            ("Top 5", pct(metrics.get("top5_rate") or 0)),
            ("平均排名", fmt_num(metrics.get("average_rank"))),
            ("情感倾向", sentiment_label(metrics.get("dominant_sentiment") or "neutral")),
        ]
    return "".join(
        f'<div class="kpi-mini"><span>{esc(label)}</span><strong>{esc(value)}</strong></div>'
        for label, value in rows
    )


def section_summary(text: str) -> str:
    return f'<p class="section-summary">{esc(text)}</p>'


def bilingual_summary(zh: str, en: str) -> str:
    return f'<p class="section-summary lang-zh">{esc(zh)}</p><p class="section-summary lang-en">{esc(en)}</p>'


def render_stacked_bar(segments: list[tuple[str, int, str]], total: int | None = None) -> str:
    total = total if total is not None else sum(value for _, value, _ in segments)
    if not total:
        return '<p class="empty">No data.</p>'
    blocks = []
    legend = []
    for label, value, css_class in segments:
        width = max(0, value / total * 100)
        if value:
            blocks.append(f'<span class="{esc(css_class)}" style="width:{width:.2f}%"></span>')
        legend.append(f'<span><i class="{esc(css_class)}"></i>{esc(label)} <b>{pct(value / total)}</b></span>')
    return f'<div class="stacked-bar">{"".join(blocks)}</div><div class="stacked-legend">{"".join(legend)}</div>'


def render_sentiment_donut(segments: list[tuple[str, int, str]], total: int | None = None) -> str:
    total = total if total is not None else sum(value for _, value, _ in segments)
    if not total:
        return '<p class="empty">No data.</p>'
    colors = {
        "seg-positive": "#97B9A1",
        "seg-neutral": "#B8C2CF",
        "seg-negative": "#D8A69E",
    }
    dominant_label, dominant_value, _ = max(segments, key=lambda item: item[1])
    offset = 0.0
    circles = ['<circle class="sentiment-donut-base" cx="90" cy="90" r="54" />']
    legend = []
    for label, value, css_class in segments:
        share = rate(value, total) * 100
        color = colors.get(css_class, "#7E8C9A")
        if value:
            circles.append(
                f'<circle class="sentiment-donut-segment" cx="90" cy="90" r="54" '
                f'pathLength="100" stroke="{color}" stroke-dasharray="{share:.3f} {100 - share:.3f}" '
                f'stroke-dashoffset="{-offset:.3f}" transform="rotate(-90 90 90)" />'
            )
        offset += share
        legend.append(
            '<div class="sentiment-donut-row">'
            f'<span><i style="background:{color}"></i>{esc(label)}</span>'
            f'<strong>{pct(rate(value, total))}</strong>'
            f'<em>{esc(value)}</em>'
            '</div>'
        )
    return (
        '<div class="sentiment-donut-wrap">'
        '<div class="sentiment-donut-stage">'
        '<svg class="viz-svg sentiment-donut-svg" viewBox="0 0 180 180" role="img" aria-label="目标实体情感分布圆环图">'
        f'{"".join(circles)}'
        f'<text class="sentiment-donut-main" x="90" y="82" text-anchor="middle">{esc(dominant_label)}</text>'
        f'<text class="sentiment-donut-value" x="90" y="106" text-anchor="middle">{pct(rate(dominant_value, total))}</text>'
        '</svg>'
        '</div>'
        f'<div class="sentiment-donut-legend">{"".join(legend)}</div>'
        '</div>'
    )


def render_share_donut(rows: list[tuple[str, int]], label_map: dict[str, str] | None = None, aria_label: str = "占比圆环图") -> str:
    cleaned = [(name, int(value or 0)) for name, value in rows if int(value or 0) >= 0]
    total = sum(value for _, value in cleaned)
    if not total:
        return '<p class="empty">No data.</p>'
    label_map = label_map or {}
    dominant_name, dominant_value = max(cleaned, key=lambda item: item[1])
    offset = 0.0
    circles = ['<circle class="share-donut-base" cx="90" cy="90" r="55" />']
    legend = []
    for index, (name, value) in enumerate(cleaned):
        share = rate(value, total) * 100
        color = SHARE_DONUT_COLORS[index % len(SHARE_DONUT_COLORS)]
        label = label_map.get(name, name)
        if value:
            circles.append(
                f'<circle class="share-donut-segment" cx="90" cy="90" r="55" '
                f'pathLength="100" stroke="{color}" stroke-dasharray="{share:.3f} {100 - share:.3f}" '
                f'stroke-dashoffset="{-offset:.3f}" transform="rotate(-90 90 90)" />'
            )
        offset += share
        legend.append(
            '<div class="share-donut-row">'
            f'<span><i style="background:{color}"></i>{esc(label)}</span>'
            f'<strong>{pct(rate(value, total))}</strong>'
            f'<em>{esc(value)}</em>'
            '</div>'
        )
    dominant_label = label_map.get(dominant_name, dominant_name)
    return (
        '<div class="share-donut-wrap">'
        '<div class="share-donut-stage">'
        f'<svg class="viz-svg share-donut-svg" viewBox="0 0 180 180" role="img" aria-label="{esc(aria_label)}">'
        f'{"".join(circles)}'
        f'<text class="share-donut-main" x="90" y="82" text-anchor="middle">{esc(dominant_label)}</text>'
        f'<text class="share-donut-value" x="90" y="106" text-anchor="middle">{pct(rate(dominant_value, total))}</text>'
        '</svg>'
        '</div>'
        f'<div class="share-donut-legend">{"".join(legend)}</div>'
        '</div>'
    )


def benchmark_maxima(rows: list[tuple[str, dict]], specs: list[tuple[str, str]]) -> dict[str, float]:
    maxima = {}
    for key, _ in specs:
        maxima[key] = max((metric.get(key) or 0 for _, metric in rows), default=0) or 0.000001
    return maxima


def score_metric(value: float, maximum: float) -> float:
    return clamp(value / max(maximum, 0.000001)) * 100


def render_benchmark_radar(selected_rows: list[dict], benchmark_rows: list[tuple[str, dict]]) -> str:
    selected = selected_rows[:4]
    if not selected:
        return '<p class="empty">No data.</p>'
    specs = [
        ("mention_rate", "提及"),
        ("avg_mentions_per_sample", "提及强度"),
        ("top1_rate", "Top 1"),
        ("top3_rate", "Top 3"),
        ("top5_rate", "Top 5"),
        ("reference_mentions", "信源"),
    ]
    maxima = benchmark_maxima(benchmark_rows, specs)
    cx = cy = 150
    radius = 96
    colors = ["#1B365D", "#7E8C9A", "#9C8C68", "#6E8A78"]
    axes = []
    labels = []
    rings = []
    for scale, label in [(0.25, "25"), (0.50, "50"), (0.75, "75"), (1.0, "100")]:
        ring_points = []
        for index in range(len(specs)):
            angle = -math.pi / 2 + index * 2 * math.pi / len(specs)
            ring_points.append(f"{cx + math.cos(angle) * radius * scale:.1f},{cy + math.sin(angle) * radius * scale:.1f}")
        rings.append(f'<polygon points="{" ".join(ring_points)}" />')
        rings.append(f'<text x="{cx + 5}" y="{cy - radius * scale + 4:.1f}">{label}</text>')
    for index, (_, label) in enumerate(specs):
        angle = -math.pi / 2 + index * 2 * math.pi / len(specs)
        outer_x = cx + math.cos(angle) * radius
        outer_y = cy + math.sin(angle) * radius
        label_x = cx + math.cos(angle) * (radius + 26)
        label_y = cy + math.sin(angle) * (radius + 24)
        axes.append(f'<line x1="{cx}" y1="{cy}" x2="{outer_x:.1f}" y2="{outer_y:.1f}" />')
        labels.append(f'<text x="{label_x:.1f}" y="{label_y:.1f}" text-anchor="middle">{esc(label)}</text>')

    series = []
    legend = []
    for series_index, row in enumerate(selected):
        color = colors[series_index % len(colors)]
        points = []
        dots = []
        for index, (key, _) in enumerate(specs):
            angle = -math.pi / 2 + index * 2 * math.pi / len(specs)
            score = score_metric(row.get(key) or 0, maxima[key])
            x = cx + math.cos(angle) * radius * score / 100
            y = cy + math.sin(angle) * radius * score / 100
            points.append(f"{x:.1f},{y:.1f}")
            dots.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3.2" fill="{color}" />')
        role_class = " target-series" if row.get("role") == "target" else ""
        fill = f' fill="{color}" fill-opacity="0.12"' if row.get("role") == "target" else ' fill="none"'
        dash = "" if row.get("role") == "target" else ' stroke-dasharray="5 4"'
        series.append(
            f'<g class="radar-series{role_class}"><polygon points="{" ".join(points)}" stroke="{color}"{fill}{dash} />{"".join(dots)}</g>'
        )
        legend.append(
            f'<span><i style="background:{color}"></i>{esc(row.get("name", ""))}</span>'
        )
    return (
        '<div class="benchmark-chart">'
        '<svg class="viz-svg radar benchmark-radar" viewBox="0 0 420 320" role="img" aria-label="目标与竞品 100 分制雷达对标">'
        f'<g class="radar-grid">{"".join(rings)}{"".join(axes)}</g>'
        f'{"".join(series)}'
        f'<g class="radar-labels">{"".join(labels)}</g>'
        '<text class="axis-label" x="300" y="292">行业最优 = 100 分</text>'
        '</svg>'
        f'<div class="chart-legend">{"".join(legend)}</div>'
        '</div>'
    )


def render_benchmark_bubble_chart(rows: list[tuple[str, dict]], target_name: str, limit: int) -> str:
    selected = rows[:limit]
    target_entry = next(
        ((name, metric) for name, metric in rows if name == target_name or metric.get("role") == "target"),
        None,
    )
    if target_entry and all(name != target_entry[0] for name, _ in selected):
        selected = [target_entry] + selected[: max(limit - 1, 0)]
    if not selected:
        return '<p class="empty">No data.</p>'
    width = 520
    height = 330
    left = 62
    right = 34
    top = 28
    bottom = 54
    max_radius = max((metric.get("avg_mentions_per_sample") or 0 for _, metric in selected), default=1) or 1
    bubble_palette = ["#2B4668", "#365678", "#436887", "#567A99", "#6E8EA9", "#86A2B8", "#9BAFC0", "#6E8A78", "#8A9A83", "#9C8C68"]
    grid = []
    for tick in (0.25, 0.5, 0.75, 1.0):
        x = left + tick * (width - left - right)
        y = top + (1 - tick) * (height - top - bottom)
        grid.append(f'<line class="grid-line" x1="{x:.1f}" y1="{top}" x2="{x:.1f}" y2="{height-bottom}" />')
        grid.append(f'<line class="grid-line" x1="{left}" y1="{y:.1f}" x2="{width-right}" y2="{y:.1f}" />')
        grid.append(f'<text class="tick-label" x="{x:.1f}" y="{height-bottom+18}" text-anchor="middle">{int(tick*100)}</text>')
        grid.append(f'<text class="tick-label" x="{left-10}" y="{y+4:.1f}" text-anchor="end">{int(tick*100)}</text>')
    nodes = []
    color_index = 0
    legend = []
    for index, (name, metric) in enumerate(selected):
        x = left + clamp(metric.get("top5_rate") or 0) * (width - left - right)
        y = top + (1 - clamp(metric.get("mention_rate") or 0)) * (height - top - bottom)
        radius = 5 + clamp((metric.get("avg_mentions_per_sample") or 0) / max_radius) * 14
        is_target = name == target_name or metric.get("role") == "target"
        if is_target:
            fill = "#1B365D"
        else:
            fill = bubble_palette[color_index % len(bubble_palette)]
            color_index += 1
        opacity = "0.96" if is_target else "0.86"
        anchor = "end" if x > width - 150 else "start"
        label_x = max(left + 8, min(width - right - 8, x - radius - 8 if anchor == "end" else x + radius + 8))
        label_y = y - radius - 7 if y > top + 32 else y + radius + 15
        label_y = max(top + 12, min(height - bottom - 6, label_y))
        label = name[:14] + ("..." if len(name) > 14 else "")
        aria = (
            f"{name}，Top 5 {pct(metric.get('top5_rate') or 0)}，"
            f"提及率 {pct(metric.get('mention_rate') or 0)}，平均提及 {fmt_num(metric.get('avg_mentions_per_sample') or 0, 2)}"
        )
        nodes.append(
            f'<g class="bubble-node{" is-target" if is_target else ""}" tabindex="0" role="button" aria-label="{esc(aria)}">'
            f'<title>{esc(aria)}</title>'
            f'<circle class="bubble-point" cx="{x:.1f}" cy="{y:.1f}" r="{radius:.1f}" fill="{fill}" fill-opacity="{opacity}" />'
            f'<text class="bubble-name" x="{label_x:.1f}" y="{label_y:.1f}" text-anchor="{anchor}">{esc(label)}</text>'
            '</g>'
        )
        legend.append(f'<span><i style="background:{fill}"></i>{esc(name)}</span>')
    return (
        '<div class="benchmark-chart bubble-benchmark">'
        f'<svg class="viz-svg bubble-plot" viewBox="0 0 {width} {height}" role="img" aria-label="Top 5 概率与提及率气泡对标">'
        '<rect class="bubble-zone" x="62" y="28" width="424" height="248" />'
        f'{"".join(grid)}'
        f'<line class="axis" x1="{left}" y1="{height-bottom}" x2="{width-right}" y2="{height-bottom}" />'
        f'<line class="axis" x1="{left}" y1="{top}" x2="{left}" y2="{height-bottom}" />'
        '<text class="axis-label" x="274" y="320" text-anchor="middle">Top 5 概率</text>'
        '<text class="axis-label" x="18" y="155" transform="rotate(-90 18 155)" text-anchor="middle">提及率</text>'
        '<text class="quadrant-label" x="382" y="48">高覆盖 / 高提及</text>'
        f'{"".join(nodes)}'
        '</svg>'
        f'<div class="chart-legend bubble-legend">{"".join(legend)}</div>'
        '</div>'
    )


def render_metric_matrix(rows: list[tuple[str, dict]], limit: int) -> str:
    headers = [("mention_rate", "提及"), ("avg_mentions_per_sample", "均次"), ("top1_rate", "Top1"), ("top3_rate", "Top3"), ("top5_rate", "Top5")]
    body = []
    max_mentions = max((metric.get("avg_mentions_per_sample") or 0 for _, metric in rows[:limit]), default=1) or 1
    for name, metric in rows[:limit]:
        cells = []
        for key, label in headers:
            raw = (metric.get(key) or 0)
            value = raw / max_mentions if key == "avg_mentions_per_sample" else raw
            bucket = min(5, int(clamp(value) * 5 + 0.999))
            shown = fmt_num(raw, 2) if key == "avg_mentions_per_sample" else pct(raw)
            cells.append(f'<td class="heat h{bucket}">{esc(shown)}</td>')
        body.append(f'<tr><th>{esc(name)}</th>{"".join(cells)}</tr>')
    header = "".join(f"<th>{esc(label)}</th>" for _, label in headers)
    return f'<table class="kami-table matrix-table"><thead><tr><th>实体</th>{header}</tr></thead><tbody>{"".join(body)}</tbody></table>'


def render_lollipop_chart(rows: list[tuple[str, dict]], limit: int) -> str:
    selected = rows[:limit]
    max_value = max((metric.get("avg_mentions_per_sample") or 0 for _, metric in selected), default=1) or 1
    out = []
    for name, metric in selected:
        value = metric.get("avg_mentions_per_sample") or 0
        width = max(2, value / max_value * 100)
        out.append(
            f'<div class="lollipop-row"><span>{esc(name)}</span><div><i style="width:{width:.2f}%"></i><b style="left:clamp(0px, calc({width:.2f}% - 6px), calc(100% - 12px))"></b></div><strong>{fmt_num(value, 2)}</strong></div>'
        )
    return '<div class="lollipop">' + "".join(out) + '</div>' if out else '<p class="empty">No data.</p>'


def render_coverage_snapshot(samples: dict, question_rows: list[dict]) -> str:
    segments = [
        ("有效", samples.get("valid", 0), "seg-positive"),
        ("失败", samples.get("failed", 0), "seg-negative"),
        ("未完成", samples.get("pending", 0), "seg-neutral"),
    ]
    cards = [
        ("完成率", pct(samples.get("completion_rate") or 0)),
        ("有效率", pct(samples.get("valid_rate") or 0)),
        ("平均信源", fmt_num(sum(row.get("avg_references", 0) for row in question_rows) / len(question_rows) if question_rows else 0)),
        ("平均字数", fmt_num(sum(row.get("avg_answer_chars", 0) for row in question_rows) / len(question_rows) if question_rows else 0, 0)),
    ]
    return (
        '<div class="coverage-snapshot">'
        '<h3>采样状态构成</h3>'
        f'{render_stacked_bar(segments, samples.get("planned", 0))}'
        '<div class="coverage-cards">'
        + "".join(f'<div><span>{esc(label)}</span><strong>{esc(value)}</strong></div>' for label, value in cards)
        + '</div></div>'
    )


def render_treemap(rows: list[dict], limit: int = 8) -> str:
    selected = rows[:limit]
    max_value = max((row.get("count", 0) for row in selected), default=1) or 1
    blocks = []
    for row in selected:
        value = row.get("count", 0)
        width = max(3, value / max_value * 100)
        display = row.get("display_name") or row.get("name", "")
        domain = row.get("name", "")
        blocks.append(
            '<div class="treemap-cell" role="listitem">'
            '<div class="treemap-cell-head">'
            f'<strong>{esc(display)}</strong><span class="treemap-count">{esc(value)}</span>'
            '</div>'
            f'<div class="treemap-domain">{esc(domain)}</div>'
            f'<div class="treemap-share"><i style="width:{width:.2f}%"></i></div>'
            '</div>'
        )
    return '<div class="treemap" role="list">' + "".join(blocks) + '</div>' if blocks else '<p class="empty">No data.</p>'


def feature_rate_rows(features: dict) -> list[tuple[str, float, str]]:
    labels = {
        "has_number": "标题含数字",
        "has_year": "标题含年份",
        "has_question": "标题含疑问",
        "has_structure_punctuation": "标题含结构符",
        "contains_brand": "标题含实体",
    }
    total = max(features.get("total") or 0, 1)
    rows = []
    for key, label in labels.items():
        count = features.get("feature_counts", {}).get(key, 0)
        rows.append((label, count / total, f"{pct(count / total)} · {count}"))
    return rows


def title_intent_rows(features: dict, limit: int = REPORT_ITEM_LIMIT) -> list[tuple[str, float, str]]:
    total = max(features.get("total") or 0, 1)
    counts = Counter(features.get("intent_counts") or {})
    return [
        (label, count / total, f"{pct(count / total)} · {count}")
        for label, count in counts.most_common(limit)
    ]


def select_radar_rows(target: dict, benchmark_rows: list[tuple[str, dict]]) -> list[dict]:
    comparison_rows = target.get("comparison_rows") or []
    target_rows = [row for row in comparison_rows if row.get("role") == "target"]
    if not target_rows:
        target_rows = [
            {"name": name, **metric}
            for name, metric in benchmark_rows
            if metric.get("role") == "target"
        ][:1]
    competitor_rows = [
        {"name": name, **metric}
        for name, metric in benchmark_rows
        if metric.get("role") == "competitor"
    ]
    competitor_rows.sort(
        key=lambda row: (
            row.get("top3_rate") or 0,
            row.get("top5_rate") or 0,
            row.get("mention_rate") or 0,
            row.get("avg_mentions_per_sample") or 0,
            row.get("reference_mentions") or 0,
        ),
        reverse=True,
    )
    return target_rows[:1] + competitor_rows[:3]


def top_insights(summary: dict) -> list[str]:
    insights = []
    target = summary.get("target", {})
    target_metrics = target.get("metrics") or {}
    if target.get("entity"):
        insights.append(
            f"目标实体「{target['entity']}」提及率 {pct(target_metrics.get('mention_rate') or 0)}，Top 5 概率 {pct(target_metrics.get('top5_rate') or 0)}，Top 3 概率 {pct(target_metrics.get('top3_rate') or 0)}。"
        )
        insights.append(
            f"目标实体平均每条有效回答提及 {fmt_num(target_metrics.get('avg_mentions_per_sample') or 0, 2)} 次，情感以「{sentiment_label(target_metrics.get('dominant_sentiment') or 'neutral')}」为主。"
        )
        if target.get("top_competitor"):
            competitor = target["top_competitor"]
            gap = (target_metrics.get("top3_rate") or 0) - (competitor.get("top3_rate") or 0)
            insights.append(f"Top 3 最强竞品是 {competitor['name']}，目标实体相对差距 {pp(gap)}。")
    entities = summary.get("entities", {})
    if entities:
        kind_label = {"person": "人", "company": "公司", "product": "产品", "mixed": "混合实体"}.get(
            entities.get("target_kind"),
            entities.get("target_kind", "mixed"),
        )
        insights.append(f"竞品识别口径为「{kind_label}」，共识别 {entities.get('competitor_count', 0)} 个同类型竞品实体。")
    brands = sorted_brand_rows(summary, "top1_rate")
    if brands:
        name, row = brands[0]
        insights.append(f"Top 1 概率最高的是 {name}，为 {pct(row['top1_rate'])}。")
    brands3 = sorted_brand_rows(summary, "top3_rate")
    if brands3:
        name, row = brands3[0]
        insights.append(f"Top 3 覆盖最稳定的是 {name}，为 {pct(row['top3_rate'])}，提及率 {pct(row['mention_rate'])}。")
    brands5 = sorted_brand_rows(summary, "top5_rate")
    if brands5:
        name, row = brands5[0]
        insights.append(f"Top 5 覆盖最高的是 {name}，为 {pct(row['top5_rate'])}。")
    channels = Counter(summary["sources"]["channel_counts"])
    if channels:
        channel, count = channels.most_common(1)[0]
        total = sum(channels.values())
        insights.append(f"信源渠道以 {channel} 为主，占 {pct(rate(count, total))}。")
    domains = summary["sources"]["top_domains"]
    if domains:
        insights.append(f"最常被引用的域名是 {domains[0]['name']}，出现 {domains[0]['count']} 次。")
    title_rates = summary["titles"]["feature_rates"]
    if title_rates:
        key, value = max(title_rates.items(), key=lambda item: item[1])
        label = {
            "has_number": "含数字",
            "has_year": "含年份",
            "has_question": "含疑问",
            "has_structure_punctuation": "含结构符",
            "contains_brand": "含实体",
        }.get(key, key)
        insights.append(f"标题特征中「{label}」最突出，占 {pct(value)}。")
    if not insights:
        insights.append("有效样本不足，当前报告只展示采集覆盖情况，不生成概率结论。")
    return insights


def render_heatmap(summary: dict, question_rows: list[dict], brand_limit: int = 8) -> str:
    brands = [name for name, _ in sorted_brand_rows(summary, "top3_rate")[:brand_limit]]
    if not brands or not question_rows:
        return '<p class="empty">No brand heatmap data.</p>'
    header = "".join(f"<th>{esc(name)}</th>" for name in brands)
    rows = []
    for question in question_rows:
        cells = []
        qid = question["question_id"]
        for brand in brands:
            row = summary["brands"]["by_question"].get(qid, {}).get(brand, {})
            value = row.get("top3_rate", 0)
            bucket = min(5, int(value * 5 + 0.999))
            cells.append(f'<td class="heat h{bucket}">{pct(value)}</td>')
        rows.append(
            f'<tr><th>{esc(qid)}</th>{"".join(cells)}'
            f'<td class="question-cell">{esc(question["question"])}</td></tr>'
        )
    return (
        '<table class="kami-table heatmap"><thead><tr><th>Query</th>'
        f'{header}<th>Question</th></tr></thead><tbody>{"".join(rows)}</tbody></table>'
    )


def report_overview_text(summary: dict) -> str:
    samples = summary["samples"]
    target = summary.get("target", {})
    metrics = target.get("metrics") or {}
    mobile = summary.get("mobile_evidence") or {}
    entity_name = target.get("entity") or "目标实体"
    entity_type = target.get("entity_type_label") or ENTITY_TYPE_LABELS.get(summary.get("entities", {}).get("target_kind"), "实体")
    mobile_note = ""
    context_note = ""
    if (summary.get("input") or {}).get("new_conversation") is False:
        context_note = "本次 Web 采集未新建独立对话，样本可能共享同一对话上下文，概率指标可能受到前序消息影响。"
    if mobile.get("collected_material_rows"):
        mobile_note = (
            f"移动端补充采集搜索资料 {mobile.get('collected_material_rows', 0)} 行，"
            f"其中判定被引用 {mobile.get('cited_material_rows', 0)} 行、未引用 {mobile.get('uncited_material_rows', 0)} 行，"
            f"新建对话成功 {mobile.get('fresh_chat_ok_samples', 0)}/{mobile.get('sample_count', 0)}。"
        )
    if not target.get("has_target"):
        return (
            f"本报告基于 {samples['question_count']} 个关键词、{samples['planned']} 次计划采样、{samples['valid']} 条有效 Doubao AI 搜索结果。"
            f"本次未指定目标实体，因此报告以「{entity_type}」候选识别、采集覆盖、信源结构和移动端证据为探索性分析重点。"
            f"本次识别同类型候选 {summary.get('entities', {}).get('same_type_candidate_count', 0)} 个，兼容引用信源 {samples['reference_count']} 条。"
            f"{mobile_note}"
            f"{context_note}"
        )
    return (
        f"本报告基于 {samples['question_count']} 个关键词、{samples['planned']} 次计划采样、{samples['valid']} 条有效 Doubao AI 搜索结果，"
        f"评估{entity_type}「{entity_name}」的提及、推荐排序、竞品对比和信源结构。"
        f"目标实体 Top 5 概率为 {pct(metrics.get('top5_rate') or 0)}，Top 3 概率为 {pct(metrics.get('top3_rate') or 0)}，"
        f"平均提及 {fmt_num(metrics.get('avg_mentions_per_sample') or 0, 2)} 次，情感倾向为「{sentiment_label(metrics.get('dominant_sentiment') or 'neutral')}」，"
        f"本次识别同类型竞品 {target.get('competitor_count', 0)} 个，引用信源 {samples['reference_count']} 条。"
        f"{mobile_note}"
        f"{context_note}"
    )


def report_overview_text_en(summary: dict) -> str:
    samples = summary["samples"]
    target = summary.get("target", {})
    metrics = target.get("metrics") or {}
    mobile = summary.get("mobile_evidence") or {}
    entity_name = target.get("entity") or "target entity"
    mobile_note = ""
    context_note = ""
    if (summary.get("input") or {}).get("new_conversation") is False:
        context_note = " This Web run reused the current conversation. Samples may share the same conversation context, and probability estimates can be influenced by earlier messages."
    if mobile.get("collected_material_rows"):
        mobile_note = (
            f" Mobile evidence includes {mobile.get('collected_material_rows', 0)} search-material rows, "
            f"{mobile.get('cited_material_rows', 0)} cited rows, {mobile.get('uncited_material_rows', 0)} uncited rows, "
            f"and {mobile.get('fresh_chat_ok_samples', 0)}/{mobile.get('sample_count', 0)} fresh-chat confirmations."
        )
    if not target.get("has_target"):
        return (
            f"This report is based on {samples['question_count']} keywords, {samples['planned']} planned samples, "
            f"and {samples['valid']} valid Doubao AI search answers. No target entity was supplied, so the report is exploratory and focuses on same-type candidates, coverage, citation structure, and mobile UI evidence. "
            f"The run identified {summary.get('entities', {}).get('same_type_candidate_count', 0)} same-type candidates and {samples['reference_count']} compatible citations."
            f"{mobile_note}"
            f"{context_note}"
        )
    return (
        f"This report is based on {samples['question_count']} keywords, {samples['planned']} planned samples, "
        f"and {samples['valid']} valid Doubao AI search answers. It evaluates the target entity \"{entity_name}\" "
        f"across mentions, recommendation ranking, same-type competitors, and citation structure. "
        f"The target Top 5 probability is {pct(metrics.get('top5_rate') or 0)}, Top 3 probability is {pct(metrics.get('top3_rate') or 0)}, "
        f"average mentions per valid answer are {fmt_num(metrics.get('avg_mentions_per_sample') or 0, 2)}, "
        f"and the dominant sentiment is {sentiment_label_en(metrics.get('dominant_sentiment') or 'neutral')}. "
        f"The run identified {target.get('competitor_count', 0)} same-type competitors and {samples['reference_count']} citations."
        f"{mobile_note}"
        f"{context_note}"
    )


def top_insights_en(summary: dict) -> list[str]:
    insights = []
    target = summary.get("target", {})
    target_metrics = target.get("metrics") or {}
    if target.get("entity"):
        insights.append(
            f"Target \"{target['entity']}\" has a mention rate of {pct(target_metrics.get('mention_rate') or 0)}, "
            f"Top 5 probability of {pct(target_metrics.get('top5_rate') or 0)}, and Top 3 probability of {pct(target_metrics.get('top3_rate') or 0)}."
        )
        insights.append(
            f"The target is mentioned {fmt_num(target_metrics.get('avg_mentions_per_sample') or 0, 2)} times per valid answer on average, "
            f"with dominant sentiment: {sentiment_label_en(target_metrics.get('dominant_sentiment') or 'neutral')}."
        )
        if target.get("top_competitor"):
            competitor = target["top_competitor"]
            gap = (target_metrics.get("top3_rate") or 0) - (competitor.get("top3_rate") or 0)
            insights.append(f"The strongest Top 3 competitor is {competitor['name']}; target gap is {pp(gap)}.")
    entities = summary.get("entities", {})
    if entities:
        insights.append(f"The competitor scope identified {entities.get('competitor_count', 0)} same-type entities.")
    channels = Counter(summary["sources"]["channel_counts"])
    if channels:
        channel, count = channels.most_common(1)[0]
        insights.append(f"The leading citation channel is {channel}, accounting for {pct(rate(count, sum(channels.values())))}.")
    domains = summary["sources"]["top_domains"]
    if domains:
        insights.append(f"The most cited domain is {domains[0].get('display_name') or domains[0]['name']}, with {domains[0]['count']} citations.")
    return insights


def geo_action_rows(summary: dict, lang: str = "zh") -> list[dict]:
    target = summary.get("target", {})
    metrics = target.get("metrics") or {}
    competitor = target.get("top_competitor") or {}
    channels = Counter(summary.get("sources", {}).get("channel_counts", {}))
    channel_total = sum(channels.values()) or 1
    official_rate = rate(channels.get("official", 0), channel_total)
    media_rate = rate(channels.get("media", 0), channel_total)
    title_rates = summary.get("titles", {}).get("feature_rates", {})
    target_name = target.get("entity") or ("目标实体" if lang == "zh" else "the target entity")
    target_top3 = metrics.get("top3_rate") or 0
    competitor_top3 = competitor.get("top3_rate") or 0
    gap = max(0.0, competitor_top3 - target_top3)
    avg_mentions = metrics.get("avg_mentions_per_sample") or 0
    title_signal = max(
        title_rates.get("has_year") or 0,
        title_rates.get("has_number") or 0,
        title_rates.get("contains_brand") or 0,
        title_rates.get("has_structure_punctuation") or 0,
    )

    def row(dimension: str, score: float, metric: str, method: str) -> dict:
        return {
            "dimension": dimension,
            "priority": int(round(clamp(score / 100) * 100)),
            "metric": metric,
            "method": method,
        }

    if lang == "en":
        rows = [
            row(
                "Ranking coverage",
                45 + gap * 100 if gap else max(35, 65 - target_top3 * 40),
                f"Target Top 3 {pct(target_top3)}; competitor gap {pp(gap)}",
                f"Build comparison, recommendation, and use-case pages that explicitly name {target_name} in the title, lead, comparison table, and FAQ.",
            ),
            row(
                "Official citability",
                max(25, (0.35 - official_rate) / 0.35 * 100),
                f"Official source share {pct(official_rate)}",
                "Create official explainer, service, case, pricing/process, and FAQ pages with stable URLs, concise summaries, and clear entity names.",
            ),
            row(
                "Third-party proof",
                max(25, (0.30 - media_rate) / 0.30 * 100),
                f"Media source share {pct(media_rate)}",
                "Seed industry portals, evaluation articles, partner cases, and list/ranking pages using consistent entity aliases and citations.",
            ),
            row(
                "Title intent fit",
                max(45, title_signal * 100),
                f"Strongest title signal {pct(title_signal)}",
                "Prioritize titles with year, ranking, comparison, recommendation, question, and risk-avoidance wording that matches cited-title patterns.",
            ),
            row(
                "Mention intensity",
                max(35, (1.8 - min(avg_mentions, 1.8)) / 1.8 * 100),
                f"Avg mentions {fmt_num(avg_mentions, 2)}",
                f"Place {target_name} in the first paragraph, summary bullets, comparison tables, conclusion, alt text, and reusable source snippets.",
            ),
            row(
                "Measurement loop",
                55,
                f"{summary.get('samples', {}).get('question_count', 0)} keywords tracked",
                "Repeat the same keyword set weekly after content updates, then compare Top 3, Top 5, mention intensity, and citation-domain movement.",
            ),
        ]
    else:
        rows = [
            row(
                "推荐覆盖",
                45 + gap * 100 if gap else max(35, 65 - target_top3 * 40),
                f"目标 Top 3 {pct(target_top3)}；竞品差距 {pp(gap)}",
                f"建设包含「{target_name}」的对比页、推荐页和场景页，并在标题、首段、对比表和 FAQ 中稳定出现目标实体。",
            ),
            row(
                "官方信源",
                max(25, (0.35 - official_rate) / 0.35 * 100),
                f"官方信源占比 {pct(official_rate)}",
                "补充官网说明页、服务页、案例页、流程/价格页和 FAQ，保持 URL 稳定、摘要清晰、实体名称一致。",
            ),
            row(
                "第三方背书",
                max(25, (0.30 - media_rate) / 0.30 * 100),
                f"媒体信源占比 {pct(media_rate)}",
                "布局行业门户、媒体测评、合作案例、榜单/排名页，统一目标实体名称、别名和引用口径。",
            ),
            row(
                "标题意图匹配",
                max(45, title_signal * 100),
                f"最强标题信号 {pct(title_signal)}",
                "优先使用年份、榜单、排名、对比、推荐、疑问和避坑类标题，贴近当前被 Doubao 引用的标题表达。",
            ),
            row(
                "提及强度",
                max(35, (1.8 - min(avg_mentions, 1.8)) / 1.8 * 100),
                f"平均提及 {fmt_num(avg_mentions, 2)} 次",
                f"让「{target_name}」进入首段、摘要条目、对比表、结论、图片替代文本和可被引用的短句片段。",
            ),
            row(
                "复测归因",
                55,
                f"跟踪 {summary.get('samples', {}).get('question_count', 0)} 个关键词",
                "每周复测同一批关键词，记录内容更新后 Top 3、Top 5、提及强度和引用域名的变化，定位有效页面。",
            ),
        ]
    rows.sort(key=lambda item: item["priority"], reverse=True)
    return rows[:6]


def geo_recommendations(summary: dict, lang: str = "zh") -> list[str]:
    return [row["method"] for row in geo_action_rows(summary, lang)[:6]]


def render_geo_priority_chart(rows: list[dict]) -> str:
    if not rows:
        return '<p class="empty">No recommendations.</p>'
    out = []
    for row in rows:
        value = row.get("priority", 0)
        out.append(
            '<div class="priority-row">'
            f'<span>{esc(row.get("dimension", ""))}</span>'
            f'<div><i style="width:{value:.0f}%"></i></div>'
            f'<strong>{value:.0f}</strong>'
            '</div>'
        )
    return '<div class="priority-list">' + "".join(out) + '</div>'


def render_geo_trend_chart(summary: dict, rows: list[dict], lang: str = "zh") -> str:
    target_metrics = (summary.get("target") or {}).get("metrics") or {}
    if not target_metrics:
        return '<p class="empty">No trend data.</p>'
    priority_signal = sum(row.get("priority", 0) for row in rows) / max(len(rows), 1) / 100
    stages = ["当前", "优化后", "1个月", "3个月", "6个月"] if lang == "zh" else ["Now", "After", "1M", "3M", "6M"]
    multipliers = [0, 0.32, 0.55, 0.78, 1.0]
    series_specs = [
        ("mention_rate", "提及率" if lang == "zh" else "Mention", "#1B365D", 0.14),
        ("top3_rate", "Top 3", "#7E8C9A", 0.12),
        ("top5_rate", "Top 5", "#9C8C68", 0.10),
    ]
    width = 620
    height = 270
    left = 56
    right = 28
    top = 26
    bottom = 48
    chart_w = width - left - right
    chart_h = height - top - bottom
    x_step = chart_w / (len(stages) - 1)

    def project(start: float, max_lift: float) -> list[float]:
        start = clamp(start)
        lift = min(0.98 - start, max_lift * (0.55 + priority_signal * 0.45))
        lift = max(0, lift)
        return [clamp(start + lift * scale, 0, 0.98) for scale in multipliers]

    grid = []
    for tick in (0, 0.25, 0.5, 0.75, 1.0):
        y = top + (1 - tick) * chart_h
        grid.append(f'<line class="trend-grid-line" x1="{left}" y1="{y:.1f}" x2="{width-right}" y2="{y:.1f}" />')
        grid.append(f'<text class="trend-tick" x="{left-10}" y="{y+4:.1f}" text-anchor="end">{int(tick * 100)}</text>')
    for index, stage in enumerate(stages):
        x = left + index * x_step
        grid.append(f'<text class="trend-stage" x="{x:.1f}" y="{height-18}" text-anchor="middle">{esc(stage)}</text>')

    lines = []
    legend = []
    for key, label, color, max_lift in series_specs:
        points = []
        dots = []
        for index, value in enumerate(project(target_metrics.get(key) or 0, max_lift)):
            x = left + index * x_step
            y = top + (1 - value) * chart_h
            points.append(f"{x:.1f},{y:.1f}")
            dots.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3.0" fill="{color}" />')
        lines.append(
            f'<g class="trend-series"><polyline points="{" ".join(points)}" stroke="{color}" />{"".join(dots)}</g>'
        )
        legend.append(f'<span><i style="background:{color}"></i>{esc(label)}</span>')

    note = "基于当前缺口和优化优先级的保守预估，非真实历史数据。" if lang == "zh" else "Conservative projection from current gaps and action priority; not historical data."
    return (
        '<div class="trend-chart-wrap">'
        f'<svg class="viz-svg trend-chart" viewBox="0 0 {width} {height}" role="img" aria-label="{esc(note)}">'
        f'{"".join(grid)}'
        f'<line class="trend-axis" x1="{left}" y1="{height-bottom}" x2="{width-right}" y2="{height-bottom}" />'
        f'<line class="trend-axis" x1="{left}" y1="{top}" x2="{left}" y2="{height-bottom}" />'
        f'{"".join(lines)}'
        '</svg>'
        f'<div class="chart-legend">{"".join(legend)}</div>'
        f'<p class="chart-note">{esc(note)}</p>'
        '</div>'
    )


def render_geo_method_table(rows: list[dict], lang: str = "zh") -> str:
    if not rows:
        return '<p class="empty">No recommendations.</p>'
    headers = ("维度", "优先级", "当前指标", "具体方法") if lang == "zh" else ("Dimension", "Priority", "Current Metric", "Action Method")
    body = "".join(
        f'<tr><td>{esc(row.get("dimension", ""))}</td><td>{esc(row.get("priority", 0))}</td>'
        f'<td>{esc(row.get("metric", ""))}</td><td>{esc(row.get("method", ""))}</td></tr>'
        for row in rows
    )
    return (
        '<table class="kami-table geo-method-table"><thead><tr>'
        + "".join(f"<th>{esc(header)}</th>" for header in headers)
        + f"</tr></thead><tbody>{body}</tbody></table>"
    )


def render_recommendations(items: list[str]) -> str:
    if not items:
        return '<p class="empty">No recommendations.</p>'
    return '<div class="recommendation-list">' + "".join(f'<div class="recommendation-item">{esc(item)}</div>' for item in items) + '</div>'


def report_toc_html(enabled_ids: set[str] | None = None) -> str:
    items = [
        ("overview", "报告概览", "Overview"),
        ("insights", "核心结论", "Key Findings"),
        ("comparison", "竞品分析", "Competitor Analysis"),
        ("sentiment", "情感提及", "Sentiment"),
        ("entities", "实体识别", "Entity Audit"),
        ("coverage", "采集覆盖", "Coverage"),
        ("mobile", "移动证据", "Mobile Evidence"),
        ("probability", "概率排名", "Probability"),
        ("sources", "信源结构", "Sources"),
        ("titles", "标题特征", "Titles"),
        ("recommendations", "总结建议", "Recommendations"),
    ]
    if enabled_ids is not None:
        items = [item for item in items if item[0] in enabled_ids]
    return "".join(
        f'<a href="#{anchor}"><span class="lang-zh">{esc(zh)}</span><span class="lang-en">{esc(en)}</span></a>'
        for anchor, zh, en in items
    )


def metric_definition_html(lang: str = "zh") -> str:
    if lang == "en":
        rows = [
            ("Mention Rate", "Share of valid answers where the entity appears."),
            ("Average Mentions", "Average number of entity mentions per valid answer."),
            ("Top 1 Probability", "Share of valid answers where the entity ranks first."),
            ("Top 3 Probability", "Share of valid answers where the entity enters the top three positions."),
            ("Top 5 Probability", "Share of valid answers where the entity enters the top five positions."),
            ("Average Rank", "Average recommendation rank when the entity appears. Lower is better."),
            ("Sentiment", "Heuristic sentiment around the entity mention: positive, neutral, or negative."),
            ("Citation", "Source title, domain, channel, and URL cited by Doubao."),
        ]
    else:
        rows = [
            ("提及率", "实体在有效回答中被提到的比例。"),
            ("平均提及次数", "实体在每条有效回答中被提到的平均次数。"),
            ("Top 1 概率", "实体在推荐排序中位列第 1 的比例。"),
            ("Top 3 概率", "实体进入前 3 个推荐位置的比例。"),
            ("Top 5 概率", "实体进入前 5 个推荐位置的比例。"),
            ("平均排名", "实体出现时的平均推荐位置，数值越低越好。"),
            ("情感倾向", "基于实体附近文本词表的启发式判断，分为积极、中性、负向。"),
            ("信源引用", "Doubao 回答引用的来源标题、域名、渠道和 URL。"),
        ]
    return "".join(f'<div class="definition"><strong>{esc(name)}</strong><span>{esc(text)}</span></div>' for name, text in rows)


def render_report(title: str, input_name: str, summary: dict) -> str:
    samples = summary["samples"]
    mobile = summary.get("mobile_evidence") or {}
    item_limit = int((summary.get("report") or {}).get("item_limit") or REPORT_ITEM_LIMIT)
    target = summary.get("target", {})
    target_metrics = target.get("metrics") or {}
    brand_source_note = {
        "provided": "用户提供实体表",
        "target_entity": "围绕目标实体识别同类型竞品",
        "inferred_target_entity": "自动识别目标实体",
        "inferred": "自动推断候选实体",
    }.get(summary["brand_source"], summary["brand_source"])
    entity_kind_label = {
        "person": "人",
        "company": "公司",
        "product": "产品",
        "mixed": "混合实体",
    }.get(summary.get("entities", {}).get("target_kind"), summary.get("entities", {}).get("target_kind", "mixed"))
    top1_rows = [
        (name, row["top1_rate"], f"{pct(row['top1_rate'])} · {row['top1_samples']}")
        for name, row in sorted_brand_rows(summary, "top1_rate")[:item_limit]
    ]
    top3_rows = [
        (name, row["top3_rate"], f"{pct(row['top3_rate'])} · {row['top3_samples']}")
        for name, row in sorted_brand_rows(summary, "top3_rate")[:item_limit]
    ]
    top5_rows = [
        (name, row["top5_rate"], f"{pct(row['top5_rate'])} · {row['top5_samples']}")
        for name, row in sorted_brand_rows(summary, "top5_rate")[:item_limit]
    ]
    mention_rows = [
        (name, row["mention_rate"], f"{pct(row['mention_rate'])} · {row['mentioned_samples']}")
        for name, row in sorted_brand_rows(summary, "mention_rate")[:item_limit]
    ]
    avg_mention_rows = [
        (name, row["avg_mentions_per_sample"], fmt_num(row["avg_mentions_per_sample"], 2))
        for name, row in sorted_brand_rows(summary, "avg_mentions_per_sample")[:item_limit]
    ]
    avg_mention_metric_rows = sorted_brand_rows(summary, "avg_mentions_per_sample")
    negative_rows = [
        (name, row["negative_rate"], f"{pct(row['negative_rate'])} · {sentiment_label(row.get('dominant_sentiment') or 'neutral')}")
        for name, row in sorted_brand_rows(summary, "negative_rate")[:item_limit]
    ]
    ranked_by_average_rank = sorted(
        (
            (name, row)
            for name, row in summary["brands"]["by_brand"].items()
            if row.get("average_rank") is not None
        ),
        key=lambda item: (item[1].get("average_rank") or 999, -(item[1].get("mention_rate") or 0)),
    )
    rank_rows = [
        (name, 1 / max(row["average_rank"] or 999, 1), fmt_num(row["average_rank"]))
        for name, row in ranked_by_average_rank[:item_limit]
    ]
    metric_rows = sorted_brand_rows(summary, "top5_rate")
    channel_rows = [
        (name, count)
        for name, count in Counter(summary["sources"]["channel_counts"]).most_common()
    ]
    domain_max = max([row["count"] for row in summary["sources"]["top_domains"]] or [1])
    domain_rows = [
        {
            "display_name": row.get("display_name") or row["name"],
            "secondary": row["name"],
            "value": row["count"],
            "count": row["count"],
        }
        for row in summary["sources"]["top_domains"][:item_limit]
    ]
    source_rows = [(source_display_name(row["name"]), row["count"], str(row["count"])) for row in summary["sources"]["top_sources"]]
    position_rows = [
        (name, count)
        for name, count in summary["sources"]["position_buckets"].items()
    ]
    length_total = sum(summary["titles"]["length_buckets"].values()) or 1
    length_rows = [
        (name, count / length_total, f"{pct(count / length_total)} · {count}")
        for name, count in summary["titles"]["length_buckets"].items()
    ]
    recency_total = sum(summary["titles"]["recency_buckets"].values()) or 1
    recency_rows = [
        (RECENCY_LABELS.get(name, name), count / recency_total, f"{pct(count / recency_total)} · {count}")
        for name, count in summary["titles"]["recency_buckets"].items()
    ]
    url_link_rows = [
        {
            "display_name": short_url_label(row.get("url", "")),
            "secondary": "",
            "url": row.get("url", ""),
            "value": row.get("count", 0),
            "count": row.get("count", 0),
        }
        for row in summary["sources"]["top_urls"][:item_limit]
    ]
    title_link_rows = [
        {
            "display_name": row.get("name", ""),
            "url": row.get("url", ""),
            "value": row.get("count", 0),
            "count": row.get("count", 0),
        }
        for row in summary["sources"]["top_titles"][:item_limit]
    ]
    question_rows = summary["questions"]
    display_question_rows = question_rows[:item_limit]
    question_chart_rows = [
        (row["question_id"], row["valid_rate"], f"{row['valid']}/{row['planned']}")
        for row in display_question_rows
    ]
    insights = top_insights(summary)
    insights_en = top_insights_en(summary)
    geo_actions = geo_action_rows(summary, "zh")
    geo_actions_en = geo_action_rows(summary, "en")
    recommendations = geo_recommendations(summary, "zh")
    recommendations_en = geo_recommendations(summary, "en")
    delay_strategy = mobile.get("delay_strategy") or {}
    if delay_strategy.get("mode") == "random":
        delay_note = f"{fmt_num(delay_strategy.get('min_seconds') or 0, 0)}-{fmt_num(delay_strategy.get('max_seconds') or 0, 0)} 秒随机间隔"
    elif delay_strategy:
        delay_note = f"{fmt_num(delay_strategy.get('delay_seconds') or 0, 0)} 秒固定间隔"
    else:
        delay_note = "未记录间隔策略"
    target_sentiment_counts = target_metrics.get("sentiment_counts") or {}
    sentiment_total = sum(target_sentiment_counts.values())
    sentiment_segments = [
        ("积极", int(target_sentiment_counts.get("positive", 0)), "seg-positive"),
        ("中性", int(target_sentiment_counts.get("neutral", 0)), "seg-neutral"),
        ("负向", int(target_sentiment_counts.get("negative", 0)), "seg-negative"),
    ]
    comparison_rows = target.get("comparison_rows", [])[:item_limit]
    radar_rows = select_radar_rows(target, metric_rows)

    brand_table = "".join(
        f"<tr><td>{esc(name)}</td><td>{pct(row['mention_rate'])}</td><td>{fmt_num(row['avg_mentions_per_sample'], 2)}</td>"
        f"<td>{pct(row['top1_rate'])}</td><td>{pct(row['top3_rate'])}</td><td>{pct(row['top5_rate'])}</td>"
        f"<td>{fmt_num(row['average_rank'])}</td>"
        f"<td>{esc(' / '.join(row['aliases']))}</td></tr>"
        for name, row in sorted_brand_rows(summary, "top3_rate")[:item_limit]
    )
    comparison_table = "".join(
        f"<tr><td>{'目标' if row.get('role') == 'target' else '竞品'}</td><td>{esc(row['name'])}</td>"
        f"<td>{pct(row.get('mention_rate') or 0)}</td><td>{fmt_num(row.get('avg_mentions_per_sample') or 0, 2)}</td>"
        f"<td>{pct(row.get('top1_rate') or 0)}</td><td>{pct(row.get('top3_rate') or 0)}</td><td>{pct(row.get('top5_rate') or 0)}</td>"
        f"<td>{fmt_num(row.get('average_rank'))}</td>"
        f"<td>{row.get('reference_mentions', 0)}</td><td>{'基准' if row.get('role') == 'target' else pp(row.get('gap_vs_target_top3'))}</td>"
        f"<td>{'基准' if row.get('role') == 'target' else pp(row.get('gap_vs_target_top5'))}</td></tr>"
        for row in comparison_rows
    )
    entity_table = "".join(
        f"<tr><td>{esc(row['name'])}</td><td>{esc(row['kind'])}</td><td>{esc({'target': '目标', 'competitor': '竞品', 'candidate': '候选'}.get(row.get('role'), row.get('role')))}</td>"
        f"<td>{'是' if row.get('is_target') else '否'}</td><td>{pct(row.get('confidence') or 0)}</td>"
        f"<td>{row.get('sample_count', 0)}</td><td>{pct(row.get('metrics', {}).get('mention_rate') or 0)}</td>"
        f"<td>{pct(row.get('metrics', {}).get('top3_rate') or 0)}</td><td>{pct(row.get('metrics', {}).get('top5_rate') or 0)}</td>"
        f"<td>{esc('；'.join(row.get('reasons') or ['候选项']))}</td></tr>"
        for row in summary.get("entities", {}).get("candidates", [])[:item_limit]
    )
    title_table = "".join(
        f"<tr><td>{index}</td><td>{link_html(row['name'], row.get('url', ''))}</td><td>{esc(source_display_name(row.get('source') or '', row.get('domain') or '') or domain_display_name(row.get('domain') or ''))}</td><td>{row['count']}</td></tr>"
        for index, row in enumerate(summary["sources"]["top_titles"][:item_limit], start=1)
    )
    query_table = "".join(
        f"<tr><td>{esc(row['question_id'])}</td><td>{esc(row['question'])}</td>"
        f"<td>{row['completed']}/{row['planned']}</td><td>{row['valid']}</td><td>{row['failed']}</td><td>{row['pending']}</td>"
        f"<td>{fmt_num(row['avg_references'])}</td><td>{row.get('mobile_material_rows', 0)}</td><td>{row.get('fresh_chat_ok', 0)}</td><td>{fmt_num(row['avg_answer_chars'], 0)}</td></tr>"
        for row in display_question_rows
    )
    mobile_question_table = "".join(
        f"<tr><td>{esc(row.get('question_id'))}</td><td>{esc(row.get('question'))}</td>"
        f"<td>{row.get('fresh_chat_ok', 0)}/{row.get('samples', 0)}</td><td>{row.get('material_rows', 0)}</td>"
        f"<td>{row.get('cited_material_rows', 0)}</td><td>{row.get('uncited_material_rows', 0)}</td><td>{row.get('citation_count', 0)}</td></tr>"
        for row in (mobile.get("by_question") or [])[:item_limit]
    )
    mobile_material_table = "".join(
        f"<tr><td>{esc(row.get('sample_id'))}</td><td>{esc(row.get('question'))}</td><td>{esc(row.get('material_index'))}</td>"
        f"<td>{link_html(row.get('title') or '', row.get('url') or '')}</td><td>{esc(source_display_name(row.get('source') or '', row.get('domain') or '') or row.get('domain') or '')}</td>"
        f"<td>{'是' if row.get('cited') else '否'}</td><td>{row.get('citation_count', 0)}</td><td>{esc(row.get('confidence') or '')}</td></tr>"
        for row in (mobile.get("materials") or [])[:item_limit]
    )

    has_target = bool(target.get("has_target") and target_metrics)

    def chart_card(title_html: str, body_html: str, extra_class: str = "") -> str:
        class_attr = f"chart {extra_class}".strip()
        return f'<div class="{class_attr}"><h3>{title_html}</h3>{body_html}</div>'

    if has_target:
        target_metric_block = f"""
      <h3><span class="lang-zh">目标实体指标数据</span><span class="lang-en">Target Entity Metrics</span></h3>
      <div class="kpi-strip lang-zh">{metric_card_row(target_metrics, 'zh')}</div>
      <div class="kpi-strip lang-en">{metric_card_row(target_metrics, 'en')}</div>
"""
        cover_lede_zh = "基于重复采样的 Doubao AI 搜索结果，识别真正的目标人物或品牌/机构，再衡量提及、平均提及、Top 1 / Top 3 / Top 5 概率、情感倾向、信源结构和移动端 UI 证据。"
        cover_lede_en = "Based on repeated Doubao AI search samples, this report identifies the real target person, brand, or organization, then measures mentions, average mentions, Top 1 / Top 3 / Top 5 probability, sentiment, citations, title patterns, and mobile UI evidence."
        insights_summary_zh = f"基于目标实体、同类型竞品、有效样本和引用信源生成最多 {item_limit} 条高优先级结论，优先呈现目标实体相对竞品的排序与概率差距。"
        insights_summary_en = f"Up to {item_limit} priority findings are generated from the target entity, same-type competitors, valid samples, and cited sources, with emphasis on relative ranking and probability gaps."
    else:
        target_metric_block = """
      <h3><span class="lang-zh">探索模式说明</span><span class="lang-en">Exploratory Mode</span></h3>
      <p class="overview-text lang-zh">本次未指定目标实体，因此不会生成目标对标、目标情感或目标趋势类图表。报告保留采集覆盖、候选实体、信源结构、移动端证据和可复核原始数据。</p>
      <p class="overview-text lang-en">No target entity was supplied, so target benchmark, target sentiment, and target trend charts are omitted. The report keeps coverage, candidate entities, source structure, mobile evidence, and auditable raw data.</p>
"""
        cover_lede_zh = "基于重复采样的 Doubao AI 搜索结果，汇总候选实体、采集覆盖、信源结构和移动端 UI 证据。本报告未指定目标实体，所有候选结论均为探索性结果。"
        cover_lede_en = "Based on repeated Doubao AI search samples, this report summarizes candidate entities, coverage, source structure, and mobile UI evidence. No target entity was supplied, so candidate findings are exploratory."
        insights_summary_zh = f"本次未指定目标实体，核心结论聚焦采集覆盖、候选实体、引用结构和移动端证据；候选项为启发式识别，最多展示 {item_limit} 条。"
        insights_summary_en = f"No target entity was supplied. Key findings focus on coverage, candidate entities, citation structure, and mobile evidence; candidates are heuristic and capped at {item_limit} items."

    comparison_section = ""
    if has_target and comparison_rows:
        comparison_section = f"""
  <section class="section" id="comparison">
    <h2><span class="lang-zh">竞品分析</span><span class="lang-en">Competitor Analysis</span></h2>
    {bilingual_summary(
        f"本模块只比较与目标实体类型一致的实体，目标实体「{target.get('entity') or '未指定'}」作为基准，最多展示 1 个目标实体和 {max(item_limit - 1, 0)} 个同类型竞品。",
        f"This section compares only same-type entities. The target entity \"{target.get('entity') or 'not specified'}\" is the baseline, with up to {max(item_limit - 1, 0)} competitors shown.",
    )}
    <div class="chart-grid">
      {chart_card('<span class="lang-zh">目标与最佳 3 个竞品 100 分制雷达</span><span class="lang-en">Target vs Best 3 Competitors Radar</span>', render_benchmark_radar(radar_rows, metric_rows))}
      {chart_card('<span class="lang-zh">Top 5 概率 x 提及率气泡对标</span><span class="lang-en">Top 5 Probability x Mention Rate Bubble Benchmark</span>', render_benchmark_bubble_chart(metric_rows, target.get("entity") or "", item_limit))}
    </div>
    <h3><span class="lang-zh">同类型实体多指标矩阵</span><span class="lang-en">Same-Type Entity Metric Matrix</span></h3>
    {render_metric_matrix(metric_rows, item_limit)}
    <table class="kami-table">
      <thead><tr><th>角色</th><th>实体</th><th>提及率</th><th>平均提及</th><th>Top 1</th><th>Top 3</th><th>Top 5</th><th>平均排名</th><th>信源命中</th><th>Top 3 差距</th><th>Top 5 差距</th></tr></thead>
      <tbody>{comparison_table}</tbody>
    </table>
  </section>
"""

    sentiment_cards: list[str] = []
    if has_target and sentiment_total:
        sentiment_cards.append(
            chart_card(
                '<span class="lang-zh">目标实体情感分布</span><span class="lang-en">Target Sentiment Mix</span>',
                render_sentiment_donut(sentiment_segments, sentiment_total),
            )
        )
    if avg_mention_metric_rows:
        sentiment_cards.append(
            chart_card(
                '<span class="lang-zh">平均提及次数</span><span class="lang-en">Average Mentions</span>',
                render_lollipop_chart(avg_mention_metric_rows, item_limit),
            )
        )
    if negative_rows:
        sentiment_cards.append(
            chart_card(
                '<span class="lang-zh">负向占比</span><span class="lang-en">Negative Share</span>',
                bar_rows(negative_rows, 1),
            )
        )
    sentiment_section = ""
    if sentiment_cards:
        sentiment_section = f"""
  <section class="section" id="sentiment">
    <h2><span class="lang-zh">情感与提及强度</span><span class="lang-en">Sentiment and Mention Strength</span></h2>
    {bilingual_summary(
        f"情感分析基于实体附近文本的启发式词表判断，平均提及次数统计每条有效回答里同一实体被重复提到的强度；图表默认展示前 {item_limit} 个实体。",
        f"Sentiment is inferred from text near entity mentions, while average mentions measure how often the same entity appears in each valid answer. Charts show up to {item_limit} entities.",
    )}
    <div class="chart-grid three">
      {''.join(sentiment_cards)}
    </div>
  </section>
"""

    probability_section = ""
    if metric_rows:
        probability_title_zh = "目标实体概率" if has_target else "候选实体概率"
        probability_title_en = "Entity Probability" if has_target else "Candidate Probability"
        probability_summary_zh = (
            f"概率指标来自有效样本中的重复推荐位置估计，图表最多展示 {item_limit} 个实体；Top 1、Top 3、Top 5 分别观察首位推荐、核心推荐区和扩展推荐区的稳定性。"
            if has_target
            else f"本模块展示自动识别候选实体的重复采样指标，最多展示 {item_limit} 个候选项；无目标实体时这些数据用于探索，不用于目标对标结论。"
        )
        probability_summary_en = (
            f"Probability metrics are estimated from repeated valid samples. Charts show up to {item_limit} entities across Top 1, Top 3, Top 5, mentions, and average rank."
            if has_target
            else f"This section shows repeated-sample metrics for heuristic candidate entities, capped at {item_limit} items. Without a target entity, these rows are exploratory and not target benchmarks."
        )
        probability_section = f"""
  <section class="section" id="probability">
    <h2><span class="lang-zh">{esc(probability_title_zh)}</span><span class="lang-en">{esc(probability_title_en)}</span></h2>
    {bilingual_summary(probability_summary_zh, probability_summary_en)}
    <div class="chart-grid three">
      {chart_card('Top 1 概率', bar_rows(top1_rows, 1))}
      {chart_card('Top 3 概率', bar_rows(top3_rows, 1))}
      {chart_card('Top 5 概率', bar_rows(top5_rows, 1))}
      {chart_card('提及率', bar_rows(mention_rows, 1))}
      {chart_card('平均提及次数', bar_rows(avg_mention_rows, None))}
      {chart_card('平均排名 · 数值越低越好', bar_rows(rank_rows, None))}
    </div>
    <h3>{'目标实体明细' if has_target else '候选实体明细'}</h3>
    <table class="kami-table target-detail-table">
      <thead><tr><th>实体</th><th>提及率</th><th>平均提及</th><th>Top 1</th><th>Top 3</th><th>Top 5</th><th>平均排名</th><th>别名</th></tr></thead>
      <tbody>{brand_table}</tbody>
    </table>
    <h3>问题 x {'目标实体' if has_target else '候选实体'} Top 3 热力图</h3>
    {render_heatmap(summary, display_question_rows, item_limit)}
  </section>
"""

    source_cards: list[str] = []
    if sum(value for _, value in channel_rows):
        source_cards.append(chart_card("渠道分布", render_share_donut(channel_rows, CHANNEL_LABELS_ZH, "信源渠道分布圆环图"), "share-chart"))
    if sum(value for _, value in position_rows):
        source_cards.append(chart_card("来源编号位置", render_share_donut(position_rows, SOURCE_POSITION_LABELS_ZH, "来源编号位置圆环图"), "share-chart"))
    if source_rows:
        source_cards.append(chart_card("高频来源名", bar_rows(source_rows, None)))
    if domain_rows:
        source_cards.append(chart_card("高频域名", source_bar_rows(domain_rows, domain_max)))
        source_cards.append(chart_card("域名占比树图", render_treemap(summary["sources"]["top_domains"], item_limit)))
    if url_link_rows:
        source_cards.append(chart_card("高频 URL", source_bar_rows(url_link_rows, None), "source-url-chart"))
    source_section = ""
    if source_cards:
        source_section = f"""
  <section class="section" id="sources">
    <h2><span class="lang-zh">信源结构</span><span class="lang-en">Citation Sources</span></h2>
    {bilingual_summary(
        f"信源结构用于判断 Doubao 回答更依赖官方、媒体、社区、开发者或其他渠道；域名、URL 和来源明细只在采集到对应字段时展示。",
        f"Source structure shows whether Doubao relies more on official, media, community, developer, or other channels. Domain and URL modules are shown only when those fields are available.",
    )}
    <div class="chart-grid three">
      {''.join(source_cards)}
    </div>
  </section>
"""

    trend_card_zh = chart_card("核心指标趋势预估", render_geo_trend_chart(summary, geo_actions, "zh")) if target_metrics else ""
    trend_card_en = chart_card("Core Metric Trend Projection", render_geo_trend_chart(summary, geo_actions_en, "en")) if target_metrics else ""
    recommendations_section = f"""
  <section class="section" id="recommendations">
    <h2><span class="lang-zh">总结建议</span><span class="lang-en">Recommendations</span></h2>
    <div class="lang-zh">
      <h3>总结建议与 GEO 优化措施</h3>
      <div class="geo-action-overview">
        {chart_card("优化优先级", render_geo_priority_chart(geo_actions))}
        {trend_card_zh}
      </div>
      <div class="chart geo-method-card"><h3>具体方法与验收指标</h3>{render_geo_method_table(geo_actions, 'zh')}</div>
      {render_recommendations(recommendations)}
    </div>
    <div class="lang-en">
      <h3>Summary and GEO Optimization Actions</h3>
      <div class="geo-action-overview">
        {chart_card("Optimization Priority", render_geo_priority_chart(geo_actions_en))}
        {trend_card_en}
      </div>
      <div class="chart geo-method-card"><h3>Action Methods and Checks</h3>{render_geo_method_table(geo_actions_en, 'en')}</div>
      {render_recommendations(recommendations_en)}
    </div>
  </section>
"""

    enabled_sections = {"overview", "insights", "entities", "coverage", "titles", "recommendations"}
    if comparison_section:
        enabled_sections.add("comparison")
    if sentiment_section:
        enabled_sections.add("sentiment")
    if mobile.get("sample_count") or mobile.get("collected_material_rows"):
        enabled_sections.add("mobile")
    if probability_section:
        enabled_sections.add("probability")
    if source_section:
        enabled_sections.add("sources")
    toc_html = report_toc_html(enabled_sections)

    css = """
:root {
  --parchment:#f5f4ed; --ivory:#faf9f5; --brand:#1B365D; --brand-light:#2D5A8A;
	  --near-black:#141413; --dark-warm:#3d3d3a; --olive:#504e49; --stone:#6b6a64;
	  --border:#e8e6dc; --border-soft:#e5e3d8; --tag:#EEF2F7; --ok:#E9F3EA; --warn:#F5EFE3;
  --serif:"TsangerJinKai02","Source Han Serif SC","Noto Serif CJK SC","Songti SC","STSong",Charter,Georgia,serif;
  --mono:"JetBrains Mono","SF Mono",Consolas,Monaco,"Source Han Serif SC",monospace;
}
* { box-sizing: border-box; }
html { scroll-behavior:smooth; scroll-padding-top:92px; }
body { margin:0; color:var(--near-black); background:var(--parchment); font-family:var(--serif); line-height:1.55; letter-spacing:0; }
body.lang-zh .lang-en { display:none !important; }
body.lang-en .lang-zh { display:none !important; }
main { max-width:1180px; margin:0 auto; padding:104px 28px 80px; }
.report-nav { position:fixed; top:0; left:0; right:0; z-index:40; background:var(--parchment); border-bottom:1px solid var(--border); box-shadow:0 10px 28px #e4e1d4; }
.report-nav-shell { max-width:1180px; min-height:64px; margin:0 auto; padding:0 28px; display:flex; align-items:center; justify-content:space-between; gap:16px; }
.report-brand { min-width:0; display:flex; align-items:baseline; gap:10px; color:var(--near-black); text-decoration:none; }
.report-brand-mark { flex:0 0 auto; color:var(--brand); font-family:var(--mono); font-size:13px; font-weight:600; letter-spacing:0; line-height:1; text-transform:uppercase; }
.report-brand-title { min-width:0; max-width:360px; color:var(--stone); font-size:13px; line-height:1; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }
.nav-actions { min-width:0; display:flex; align-items:center; justify-content:flex-end; gap:10px; flex:1; }
.report-nav-inner { min-width:0; display:flex; align-items:center; justify-content:flex-end; gap:2px; overflow-x:auto; padding:4px 0; }
.report-nav-inner a { flex:0 0 auto; color:var(--dark-warm); text-decoration:none; font-family:var(--mono); font-size:11px; line-height:1; letter-spacing:0; padding:10px 8px; border-radius:6px; white-space:nowrap; }
.report-nav-inner a:hover, .report-nav-inner a:focus-visible { color:var(--brand); background:var(--tag); outline:none; }
.language-toggle { flex:0 0 auto; display:flex; align-items:center; gap:2px; padding:2px; border:1px solid var(--border); border-radius:6px; background:var(--ivory); }
.language-toggle button { appearance:none; border:0; background:transparent; color:var(--stone); font-family:var(--mono); font-size:11px; line-height:1; padding:7px 8px; border-radius:4px; cursor:pointer; }
.language-toggle button.is-active { color:var(--brand); background:var(--tag); }
.cover { padding:32px 0 42px; border-bottom:1px solid var(--border); }
.eyebrow { font-family:var(--mono); color:var(--brand); font-size:12px; letter-spacing:0; text-transform:uppercase; margin-bottom:18px; }
h1 { font-size:48px; line-height:1.12; font-weight:500; margin:0 0 18px; max-width:920px; }
h2 { font-size:24px; line-height:1.25; font-weight:500; margin:42px 0 14px; display:flex; align-items:center; gap:12px; }
h2::before { content:""; width:5px; height:28px; background:var(--brand); border-radius:2px; flex:0 0 auto; }
h3 { font-size:17px; line-height:1.3; font-weight:500; margin:24px 0 10px; color:var(--dark-warm); }
p { margin:0 0 12px; color:var(--olive); }
.lede { font-size:18px; max-width:1120px; color:var(--dark-warm); text-wrap:pretty; }
.tag { display:inline-block; background:var(--tag); color:var(--brand); border-radius:4px; padding:2px 8px; font-family:var(--mono); font-size:12px; letter-spacing:0; white-space:nowrap; }
.overview-card { background:var(--ivory); border:1px solid var(--border); border-radius:8px; padding:18px; margin:18px 0; }
.overview-text { color:var(--dark-warm); font-size:16px; max-width:none; text-wrap:pretty; }
.toc-links { display:flex; flex-wrap:wrap; gap:8px; margin:10px 0 2px; }
.toc-links a { color:var(--brand); background:var(--tag); border-radius:6px; padding:7px 10px; text-decoration:none; font-family:var(--mono); font-size:12px; }
.definition-grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(230px,1fr)); gap:10px; margin-top:10px; }
.definition { background:var(--parchment); border:1px solid var(--border-soft); border-radius:6px; padding:11px 12px; }
.definition strong { display:block; color:var(--brand); font-size:13px; margin-bottom:4px; }
.definition span { color:var(--olive); font-size:13px; }
.metric-grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(170px,1fr)); gap:14px; margin:28px 0; }
.metric-card { background:var(--ivory); border:1px solid var(--border); border-radius:8px; padding:18px 18px 16px; min-height:118px; }
.metric-value { font-size:30px; line-height:1.1; color:var(--brand); font-weight:500; font-variant-numeric:tabular-nums; }
.metric-label { margin-top:8px; color:var(--dark-warm); font-size:14px; }
.metric-note { margin-top:6px; color:var(--stone); font-size:12px; }
.section { margin-top:32px; }
.section-summary { width:100%; max-width:none; color:var(--dark-warm); background:var(--ivory); border:1px solid var(--border-soft); border-radius:6px; padding:12px 14px; margin:0 0 14px; text-wrap:pretty; }
.chart-grid { display:grid; grid-template-columns:1fr 1fr; gap:18px; align-items:start; }
.chart-grid.three { grid-template-columns:repeat(auto-fit,minmax(340px,1fr)); }
.coverage-layout { display:grid; grid-template-columns:minmax(0,1.25fr) minmax(320px,.75fr); gap:18px; align-items:start; }
.chart-grid > *, .coverage-layout > * { min-width:0; }
.chart { min-width:0; background:var(--ivory); border:1px solid var(--border); border-radius:8px; padding:18px; }
.bar-row { display:grid; grid-template-columns:minmax(120px,170px) minmax(120px,1fr) minmax(118px,max-content); align-items:center; gap:12px; margin:9px 0; font-size:13px; }
.chart-grid.three .bar-row { grid-template-columns:minmax(108px,150px) minmax(64px,1fr) minmax(96px,max-content); gap:8px; }
.bar-name { color:var(--dark-warm); overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }
.inline-link { color:var(--brand); text-decoration:none; border-bottom:1px solid color-mix(in srgb, var(--brand) 36%, transparent); }
.inline-link:hover, .inline-link:focus-visible { color:var(--brand-light); border-bottom-color:var(--brand-light); outline:none; }
.bar-track { height:14px; background:var(--border-soft); border-radius:3px; overflow:hidden; }
.bar-fill { height:100%; background:var(--brand); border-radius:3px; }
.bar-value { color:var(--stone); text-align:right; font-variant-numeric:tabular-nums; font-family:var(--mono); font-size:12px; white-space:nowrap; min-width:118px; }
.chart-grid.three .bar-value { min-width:96px; font-size:11px; }
.source-row { display:grid; grid-template-columns:minmax(0,1.1fr) minmax(76px,.9fr) 36px; align-items:center; gap:10px; margin:10px 0; }
.source-label { min-width:0; display:grid; gap:2px; }
.source-label strong, .source-label span { min-width:0; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }
.source-label strong { color:var(--dark-warm); font-size:13px; font-weight:500; line-height:1.25; }
.source-label span { color:var(--stone); font-family:var(--mono); font-size:10px; line-height:1.2; }
.source-label a { color:var(--brand); text-decoration:none; border-bottom:1px solid color-mix(in srgb, var(--brand) 28%, transparent); }
.source-label strong a, .source-label span a { display:block; min-width:0; max-width:100%; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }
.source-track { min-width:0; height:14px; background:var(--border-soft); border-radius:3px; overflow:hidden; }
.source-fill { height:100%; background:var(--brand); border-radius:3px; }
.source-count { color:var(--stone); text-align:right; font-family:var(--mono); font-size:12px; line-height:1; white-space:nowrap; font-variant-numeric:tabular-nums; }
.insights { display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:12px; margin:18px 0; }
.insight { background:var(--ivory); border-radius:6px; padding:14px 16px; color:var(--dark-warm); }
.kami-table { width:100%; border-collapse:collapse; margin:14px 0 24px; font-size:13px; background:var(--ivory); border:1px solid var(--border); }
.kami-table th { text-align:left; color:var(--dark-warm); font-weight:500; padding:9px 10px; border-bottom:1px solid var(--border); }
.kami-table td { padding:8px 10px; border-bottom:1px solid var(--border-soft); vertical-align:top; color:var(--olive); }
.kami-table th:not(:first-child), .kami-table td:not(:first-child) { font-variant-numeric:tabular-nums; }
.kami-table tr:last-child td { border-bottom:0; }
.target-detail-table { table-layout:auto; }
.target-detail-table th:first-child,
.target-detail-table td:first-child { width:112px; min-width:112px; white-space:nowrap; }
.target-detail-table th:nth-child(n+2):nth-child(-n+7),
.target-detail-table td:nth-child(n+2):nth-child(-n+7) { width:82px; min-width:70px; white-space:nowrap; }
.target-detail-table th:last-child,
.target-detail-table td:last-child { min-width:420px; white-space:normal; line-height:1.5; word-break:break-word; overflow-wrap:anywhere; }
.question-cell { max-width:360px; }
.heatmap td, .heatmap th { text-align:center; }
.heatmap .question-cell { text-align:left; }
.heat { color:var(--brand); font-family:var(--mono); font-variant-numeric:tabular-nums; }
.h0 { background:#faf9f5; } .h1 { background:#EEF2F7; } .h2 { background:#E4ECF5; }
.h3 { background:#D6E1EE; } .h4 { background:#D0DCE9; } .h5 { background:#b8cadf; }
.kpi-strip { display:grid; grid-template-columns:repeat(auto-fit,minmax(130px,1fr)); gap:10px; margin:14px 0; }
.kpi-mini { background:var(--parchment); border:1px solid var(--border-soft); border-radius:6px; padding:10px 12px; }
.kpi-mini span { display:block; color:var(--stone); font-size:12px; }
.kpi-mini strong { display:block; color:var(--brand); font-size:18px; font-variant-numeric:tabular-nums; white-space:nowrap; margin-top:3px; }
.viz-svg { width:100%; height:auto; display:block; }
.benchmark-chart { display:grid; gap:8px; }
.benchmark-radar .radar-grid polygon { fill:none; stroke:var(--border); stroke-width:.75; }
.benchmark-radar .radar-grid line { stroke:var(--border-soft); stroke-width:.7; }
.benchmark-radar .radar-grid text { fill:#a09d93; font-family:var(--mono); font-size:8px; }
.benchmark-radar .radar-series polygon { stroke-width:1.45; stroke-linejoin:round; }
.benchmark-radar .target-series polygon { stroke-width:1.9; }
.benchmark-radar text, .bubble-plot text { fill:var(--stone); font-family:var(--mono); font-size:10px; letter-spacing:0; }
.radar-labels text { font-size:11px; fill:var(--dark-warm); }
.chart-legend { display:flex; flex-wrap:wrap; gap:8px 12px; color:var(--stone); font-family:var(--mono); font-size:11px; }
.chart-legend span { display:inline-flex; align-items:center; gap:5px; min-width:0; }
.chart-legend i { width:9px; height:9px; border-radius:50%; display:inline-block; flex:0 0 auto; }
.bubble-zone { fill:#fbfaf6; stroke:var(--border-soft); }
.bubble-plot .grid-line { stroke:var(--border-soft); stroke-width:1; stroke-dasharray:2 4; }
.bubble-plot .axis { stroke:var(--border); stroke-width:1.2; }
.bubble-plot .bubble-node { cursor:pointer; outline:none; }
.bubble-plot .bubble-point { stroke:none; }
.bubble-plot .bubble-node:focus-visible .bubble-point { stroke:none; filter:drop-shadow(0 0 4px color-mix(in srgb, var(--brand) 34%, transparent)); }
.bubble-plot .bubble-name { display:none; fill:var(--dark-warm); font-size:9px; paint-order:stroke; stroke:var(--ivory); stroke-width:3px; stroke-linejoin:round; pointer-events:none; }
.bubble-plot .bubble-node.is-active .bubble-name, .bubble-plot .bubble-node:focus .bubble-name { display:block; }
.bubble-legend { margin-top:2px; }
.tick-label, .axis-label, .quadrant-label { fill:var(--stone); }
.quadrant-label { font-size:10px; }
.stacked-bar { display:flex; height:18px; overflow:hidden; border-radius:4px; background:var(--border-soft); margin:10px 0; }
.stacked-bar span { display:block; min-width:2px; }
.seg-positive { background:#CFE5D4; }
.seg-neutral { background:#D9DEE7; }
.seg-negative { background:#E8C9C2; }
.stacked-legend { display:flex; flex-wrap:wrap; gap:10px; color:var(--stone); font-size:12px; font-family:var(--mono); }
.stacked-legend span { white-space:nowrap; }
.stacked-legend i { display:inline-block; width:9px; height:9px; border-radius:2px; margin-right:5px; vertical-align:-1px; }
.sentiment-donut-wrap { display:grid; grid-template-columns:1fr; gap:16px; align-items:center; justify-items:center; min-height:260px; }
.sentiment-donut-stage { width:100%; display:flex; justify-content:center; }
.sentiment-donut-svg { width:min(190px, 68%); max-width:190px; min-width:150px; margin:0 auto; overflow:visible; }
.sentiment-donut-base { fill:none; stroke:var(--border-soft); stroke-width:22; }
.sentiment-donut-segment { fill:none; stroke-width:22; stroke-linecap:butt; }
.sentiment-donut-main { fill:var(--dark-warm); font-size:16px; font-weight:500; }
.sentiment-donut-value { fill:var(--brand); font-family:var(--mono); font-size:18px; font-weight:600; font-variant-numeric:tabular-nums; }
.sentiment-donut-legend { width:100%; display:grid; grid-template-columns:repeat(3, minmax(0,1fr)); gap:8px; }
.sentiment-donut-row { min-width:0; display:grid; grid-template-rows:auto auto auto; align-items:center; justify-items:center; gap:4px; padding:9px 8px; border:1px solid var(--border); border-radius:8px; color:var(--stone); font-size:12px; font-family:var(--mono); background:var(--ivory); }
.sentiment-donut-row span { min-width:0; max-width:100%; display:flex; align-items:center; justify-content:center; gap:6px; color:var(--dark-warm); white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }
.sentiment-donut-row i { width:11px; height:11px; border-radius:50%; flex:0 0 auto; }
.sentiment-donut-row strong { max-width:100%; color:var(--brand); text-align:center; font-size:14px; font-variant-numeric:tabular-nums; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }
.sentiment-donut-row em { max-width:100%; color:var(--stone); font-style:normal; text-align:center; font-size:11px; font-variant-numeric:tabular-nums; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }
.share-chart { display:grid; align-content:start; }
.share-donut-wrap { display:grid; grid-template-columns:1fr; gap:15px; align-items:center; justify-items:center; min-height:282px; }
.share-donut-stage { width:100%; display:flex; justify-content:center; }
.share-donut-svg { width:min(178px, 66%); max-width:178px; min-width:144px; margin:0 auto; overflow:visible; }
.share-donut-base { fill:none; stroke:var(--border-soft); stroke-width:24; }
.share-donut-segment { fill:none; stroke-width:24; stroke-linecap:butt; }
.share-donut-main { fill:var(--dark-warm); font-size:15px; font-weight:500; }
.share-donut-value { fill:var(--brand); font-family:var(--mono); font-size:17px; font-weight:600; font-variant-numeric:tabular-nums; }
.share-donut-legend { width:100%; display:grid; grid-template-columns:repeat(auto-fit, minmax(68px, 1fr)); gap:7px; }
.share-donut-row { min-width:0; display:grid; grid-template-rows:auto auto auto; align-items:center; justify-items:center; gap:4px; padding:8px 6px; border:1px solid var(--border); border-radius:8px; color:var(--stone); font-size:11px; font-family:var(--mono); background:var(--ivory); }
.share-donut-row span { min-width:0; max-width:100%; display:flex; align-items:center; justify-content:center; gap:5px; color:var(--dark-warm); white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }
.share-donut-row i { width:10px; height:10px; border-radius:50%; flex:0 0 auto; }
.share-donut-row strong { max-width:100%; color:var(--brand); text-align:center; font-size:13px; font-variant-numeric:tabular-nums; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }
.share-donut-row em { max-width:100%; color:var(--stone); font-style:normal; text-align:center; font-size:11px; font-variant-numeric:tabular-nums; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }
.lollipop { display:grid; gap:11px; }
.lollipop-row { display:grid; grid-template-columns:minmax(110px,160px) minmax(120px,1fr) 70px; align-items:center; gap:10px; font-size:13px; }
.lollipop-row span { overflow:hidden; text-overflow:ellipsis; white-space:nowrap; color:var(--dark-warm); }
.lollipop-row div { position:relative; height:16px; }
.lollipop-row i { position:absolute; top:7px; left:0; height:2px; background:var(--brand); display:block; }
.lollipop-row b { position:absolute; top:2px; width:12px; height:12px; border-radius:50%; background:var(--brand); }
.lollipop-row strong { text-align:right; color:var(--stone); font-family:var(--mono); font-size:12px; white-space:nowrap; font-variant-numeric:tabular-nums; }
.coverage-snapshot h3 { margin-top:0; }
.coverage-cards { display:grid; grid-template-columns:1fr 1fr; gap:10px; margin-top:14px; }
.coverage-cards div { background:var(--parchment); border:1px solid var(--border-soft); border-radius:6px; padding:10px; }
.coverage-cards span { display:block; color:var(--stone); font-size:12px; }
.coverage-cards strong { display:block; color:var(--brand); font-size:18px; font-variant-numeric:tabular-nums; white-space:nowrap; }
.matrix-table td, .matrix-table th { text-align:center; white-space:nowrap; }
.matrix-table th:first-child { text-align:left; }
.treemap { display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:8px; min-height:0; }
.treemap-cell { min-width:0; min-height:72px; background:var(--tag); border:1px solid var(--border-soft); border-radius:6px; padding:9px 10px; color:var(--brand); display:grid; grid-template-rows:auto 1fr auto; gap:5px; }
.treemap-cell-head { min-width:0; display:flex; align-items:flex-start; justify-content:space-between; gap:8px; }
.treemap-cell strong { min-width:0; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; font-size:12px; line-height:1.25; }
.treemap-count { flex:0 0 auto; color:var(--brand); font-family:var(--mono); font-size:11px; line-height:1.25; font-variant-numeric:tabular-nums; }
.treemap-domain { min-width:0; color:var(--stone); font-family:var(--mono); font-size:10px; line-height:1.25; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; align-self:end; }
.treemap-share { height:5px; background:var(--border-soft); border-radius:999px; overflow:hidden; }
.treemap-share i { display:block; height:100%; background:var(--brand); border-radius:999px; }
.geo-action-overview { display:grid; grid-template-columns:minmax(280px,.68fr) minmax(460px,1.32fr); gap:16px; align-items:start; margin:10px 0 16px; }
.priority-list { display:grid; gap:10px; }
.priority-row { display:grid; grid-template-columns:minmax(92px,130px) minmax(120px,1fr) 42px; align-items:center; gap:10px; color:var(--dark-warm); font-size:13px; }
.priority-row span { min-width:0; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }
.priority-row div { height:12px; background:var(--border-soft); border-radius:999px; overflow:hidden; }
.priority-row i { display:block; height:100%; background:var(--brand); border-radius:999px; }
.priority-row strong { color:var(--stone); font-family:var(--mono); font-size:12px; font-variant-numeric:tabular-nums; text-align:right; }
.geo-method-table { margin:0; font-size:12px; }
.geo-method-table th, .geo-method-table td { padding:8px 9px; }
.geo-method-table td:last-child { min-width:260px; white-space:normal; line-height:1.5; }
.geo-method-card { margin:0 0 12px; }
.trend-chart-wrap { display:grid; gap:8px; }
.trend-grid-line { stroke:var(--border-soft); stroke-width:1; stroke-dasharray:2 4; }
.trend-axis { stroke:var(--border); stroke-width:1; }
.trend-series polyline { fill:none; stroke-width:1.7; stroke-linecap:round; stroke-linejoin:round; }
.trend-tick, .trend-stage { fill:var(--stone); font-family:var(--mono); font-size:10px; }
.chart-note { margin:0; color:var(--stone); font-size:12px; line-height:1.45; }
	.recommendation-list { display:grid; grid-template-columns:repeat(auto-fit,minmax(280px,1fr)); gap:10px; margin-top:12px; align-items:stretch; }
	.recommendation-item { background:var(--ivory); border:1px solid var(--border); border-radius:6px; padding:12px 14px; color:var(--dark-warm); font-size:14px; line-height:1.55; }
	.empty { color:var(--stone); font-size:13px; }
	.entity-note { background:var(--warn); border:1px solid var(--border); border-radius:6px; padding:12px 14px; color:var(--dark-warm); }
	footer { margin-top:56px; padding-top:18px; border-top:1px solid var(--border); color:var(--stone); font-size:12px; }
@media (max-width: 860px) {
  html { scroll-padding-top:126px; }
  main { padding:126px 18px 56px; }
  .report-nav-shell { min-height:96px; padding:10px 18px 9px; flex-direction:column; align-items:flex-start; gap:8px; }
  .report-brand { width:100%; }
  .report-brand-title { max-width:none; }
  .nav-actions { width:100%; flex-direction:column; align-items:stretch; gap:8px; }
  .report-nav-inner { width:100%; justify-content:flex-start; }
  .language-toggle { align-self:flex-end; }
  h1 { font-size:34px; }
  .metric-grid, .chart-grid, .chart-grid.three, .insights, .coverage-layout { grid-template-columns:1fr; }
  .bar-row { grid-template-columns:minmax(90px,120px) minmax(90px,1fr) minmax(104px,max-content); }
  .bar-value { min-width:104px; }
  .source-row { grid-template-columns:minmax(0,1.15fr) minmax(64px,.85fr) 34px; gap:8px; }
  .sentiment-donut-wrap { gap:12px; min-height:236px; }
  .sentiment-donut-svg { width:min(174px, 76%); min-width:136px; }
  .sentiment-donut-legend { width:100%; grid-template-columns:repeat(3, minmax(0,1fr)); gap:6px; }
  .sentiment-donut-row { padding:8px 5px; gap:3px; font-size:11px; }
  .sentiment-donut-row strong { font-size:12px; }
  .share-donut-wrap { gap:12px; min-height:258px; }
  .share-donut-svg { width:min(166px, 72%); min-width:132px; }
  .share-donut-legend { gap:6px; grid-template-columns:repeat(auto-fit, minmax(66px, 1fr)); }
  .share-donut-row { padding:7px 5px; gap:3px; font-size:10px; }
  .share-donut-row strong { font-size:12px; }
  .lollipop-row { grid-template-columns:92px minmax(90px,1fr) 64px; }
  .treemap { grid-template-columns:1fr; }
  .geo-action-overview { grid-template-columns:1fr; }
  .geo-method-table td:last-child { min-width:220px; }
  .kami-table { display:block; max-width:100%; overflow-x:auto; -webkit-overflow-scrolling:touch; }
  .kami-table th, .kami-table td { white-space:nowrap; }
  .kami-table .question-cell { min-width:260px; white-space:normal; }
  .target-detail-table th:first-child,
  .target-detail-table td:first-child { width:104px; min-width:104px; white-space:nowrap; }
  .target-detail-table th:last-child,
  .target-detail-table td:last-child { min-width:360px; white-space:normal; }
}
"""

    html_doc = f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="generator" content="Kami">
  <title>{esc(title)}</title>
  <style>{css}</style>
</head>
<body class="lang-zh">
<main>
  <nav class="report-nav" aria-label="报告目录">
    <div class="report-nav-shell">
      <a class="report-brand" href="#top" aria-label="回到报告顶部">
        <span class="report-brand-mark">Doubao GEO</span>
        <span class="report-brand-title"><span class="lang-zh">AI 搜索概率报告</span><span class="lang-en">AI Search Probability Report</span></span>
      </a>
      <div class="nav-actions">
        <div class="report-nav-inner">{toc_html}</div>
        <div class="language-toggle" aria-label="Language">
          <button type="button" class="is-active" data-lang="zh">中文</button>
          <button type="button" data-lang="en">EN</button>
        </div>
      </div>
    </div>
  </nav>

  <section class="cover" id="top">
    <div class="eyebrow">DOUBAO GEO CRAWL REPORT</div>
    <h1>{esc(title)}</h1>
	    <p class="lede lang-zh">{esc(cover_lede_zh)}<br><span class="entity-scope">实体口径：<span class="tag">{esc(brand_source_note)}</span></span></p>
	    <p class="lede lang-en">{esc(cover_lede_en)}</p>
  </section>

  <section class="section" id="overview">
    <h2><span class="lang-zh">报告概览</span><span class="lang-en">Report Overview</span></h2>
    <div class="overview-card">
      <h3><span class="lang-zh">概述</span><span class="lang-en">Overview</span></h3>
      <p class="overview-text lang-zh">{esc(report_overview_text(summary))}</p>
      <p class="overview-text lang-en">{esc(report_overview_text_en(summary))}</p>
      <h3><span class="lang-zh">目录</span><span class="lang-en">Contents</span></h3>
	      <div class="toc-links">{toc_html}</div>
	      <h3><span class="lang-zh">指标说明</span><span class="lang-en">Metric Notes</span></h3>
	      <div class="definition-grid lang-zh">{metric_definition_html('zh')}</div>
	      <div class="definition-grid lang-en">{metric_definition_html('en')}</div>
	      {target_metric_block}
    </div>
  </section>

  <section class="metric-grid">
    {metric_card(samples['question_count'], '问题数', input_name)}
    {metric_card(samples['planned'], '计划样本', f"完成 {samples['completed']}，未完成 {samples['pending']}")}
    {metric_card(samples['valid'], '有效样本', f"失败 {samples['failed']}，有效率 {pct(samples['valid_rate'])}")}
    {metric_card(samples['reference_count'], '信源引用', f"{samples['unique_domains']} 个域名 · {samples['unique_urls']} 个 URL")}
    {metric_card(mobile.get('collected_material_rows', 0), '搜索资料行', f"引用 {mobile.get('cited_material_rows', 0)} · 未引用 {mobile.get('uncited_material_rows', 0)}")}
    {metric_card(mobile.get('fresh_chat_ok_samples', 0), '新建对话', f"{mobile.get('fresh_chat_ok_samples', 0)}/{mobile.get('sample_count', 0)} · {delay_note}")}
    {metric_card(samples['answer_chars'], '回答字数', f"完成率 {pct(samples['completion_rate'])}")}
  </section>

	  <section class="section" id="insights">
	    <h2><span class="lang-zh">核心结论</span><span class="lang-en">Key Findings</span></h2>
    {bilingual_summary(insights_summary_zh, insights_summary_en)}
    <div class="insights lang-zh">
      {''.join(f'<div class="insight">{esc(item)}</div>' for item in insights)}
    </div>
    <div class="insights lang-en">
      {''.join(f'<div class="insight">{esc(item)}</div>' for item in insights_en)}
    </div>
	  </section>

  {comparison_section}

  {sentiment_section}

	  <section class="section" id="entities">
	    <h2><span class="lang-zh">目标实体识别</span><span class="lang-en">Entity Identification</span></h2>
	    <p class="entity-note">目标类型：{esc(entity_kind_label)}。系统会把人、公司、产品、概念词和噪声词分开；只有同类型候选项会进入目标与竞品概率计算。自动识别是启发式判断，正式报告仍建议提供实体别名表校准。</p>
	    <table class="kami-table">
	      <thead><tr><th>候选项</th><th>类型</th><th>角色</th><th>同类型</th><th>置信度</th><th>样本数</th><th>提及率</th><th>Top 3</th><th>Top 5</th><th>判断依据</th></tr></thead>
	      <tbody>{entity_table}</tbody>
	    </table>
	  </section>

  <section class="section" id="coverage">
    <h2><span class="lang-zh">采集覆盖</span><span class="lang-en">Collection Coverage</span></h2>
    {bilingual_summary(
        f"本次计划采样 {samples['planned']} 次，完成 {samples['completed']} 次，有效 {samples['valid']} 次；下方最多展示 {item_limit} 个关键词的采样覆盖情况。",
        f"This run planned {samples['planned']} samples, completed {samples['completed']}, and produced {samples['valid']} valid samples. Up to {item_limit} keyword coverage rows are shown below.",
    )}
    <div class="coverage-layout">
      <div class="chart">
        <h3>每个问题的有效采样率</h3>
        {bar_rows(question_chart_rows, 1)}
      </div>
      <div class="chart">{render_coverage_snapshot(samples, display_question_rows)}</div>
    </div>
    <table class="kami-table">
      <thead><tr><th>问题</th><th>问句</th><th>完成/计划</th><th>有效</th><th>失败</th><th>未完成</th><th>平均信源</th><th>搜索资料</th><th>新对话</th><th>平均回答字数</th></tr></thead>
      <tbody>{query_table}</tbody>
    </table>
  </section>

  <section class="section" id="mobile">
    <h2><span class="lang-zh">移动端证据</span><span class="lang-en">Mobile Evidence</span></h2>
    {bilingual_summary(
        f"移动端通过 Android/Appium 采集 UI 可见证据。本次 {mobile.get('fresh_chat_ok_samples', 0)}/{mobile.get('sample_count', 0)} 个样本确认新建对话成功，采集间隔策略为 {delay_note}；共采集搜索资料 {mobile.get('collected_material_rows', 0)} 行，其中判定被引用 {mobile.get('cited_material_rows', 0)} 行、未引用 {mobile.get('uncited_material_rows', 0)} 行。",
        f"Mobile evidence is collected from visible Android/Appium UI. Fresh chat was confirmed for {mobile.get('fresh_chat_ok_samples', 0)}/{mobile.get('sample_count', 0)} samples. The delay strategy is {delay_note}; {mobile.get('collected_material_rows', 0)} material rows were collected, with {mobile.get('cited_material_rows', 0)} cited and {mobile.get('uncited_material_rows', 0)} uncited.",
    )}
    <div class="chart-grid">
      <div class="chart">
        <h3>移动端资料按问题</h3>
        <table class="kami-table">
          <thead><tr><th>问题</th><th>问句</th><th>新对话</th><th>资料行</th><th>被引用</th><th>未引用</th><th>引用次数</th></tr></thead>
          <tbody>{mobile_question_table}</tbody>
        </table>
      </div>
      <div class="chart">
        <h3>高频搜索资料标题</h3>
        {bar_rows([(row.get('name', ''), row.get('count', 0), str(row.get('count', 0))) for row in (mobile.get('top_material_titles') or [])[:item_limit]], None)}
      </div>
    </div>
    <h3>移动端搜索资料明细 · 前 {item_limit} 条</h3>
    <table class="kami-table">
      <thead><tr><th>样本</th><th>问句</th><th>编号</th><th>标题</th><th>来源</th><th>被引用</th><th>引用次数</th><th>置信度</th></tr></thead>
      <tbody>{mobile_material_table}</tbody>
    </table>
  </section>

  {probability_section}

  {source_section}

  <section class="section" id="titles">
    <h2><span class="lang-zh">标题特征</span><span class="lang-en">Title Patterns</span></h2>
    {bilingual_summary(
        f"标题特征用于观察被引用内容的表达方式，包括数字、年份、疑问句、结构符和是否包含目标或竞品实体。高频标题最多展示 {item_limit} 条。",
        f"Title patterns show how cited content is framed, including numbers, years, questions, structural punctuation, and entity mentions. Up to {item_limit} frequent titles are shown.",
    )}
    <div class="chart-grid">
      <div class="chart"><h3>标题功能特征</h3>{bar_rows(feature_rate_rows(summary['titles']), 1)}</div>
      <div class="chart"><h3>标题长度</h3>{bar_rows(length_rows, 1)}</div>
      <div class="chart"><h3>时间新旧</h3>{bar_rows(recency_rows, 1)}</div>
      <div class="chart"><h3>标题意图特征分析</h3>{bar_rows(title_intent_rows(summary['titles'], item_limit), 1)}</div>
    </div>
    <h3>高频引用标题</h3>
    <table class="kami-table">
      <thead><tr><th>#</th><th>标题</th><th>来源</th><th>次数</th></tr></thead>
      <tbody>{title_table}</tbody>
    </table>
  </section>

  {recommendations_section}

  <footer>
    Generated at {esc(summary['generated_at'])}. Metrics are repeated-sample estimates from visible Doubao output, not external truth claims.
  </footer>
</main>
<script>
(function() {{
  const buttons = document.querySelectorAll('[data-lang]');
  function setLanguage(lang) {{
    document.body.classList.toggle('lang-zh', lang === 'zh');
    document.body.classList.toggle('lang-en', lang === 'en');
    document.documentElement.lang = lang === 'en' ? 'en' : 'zh-CN';
    buttons.forEach(function(button) {{
      button.classList.toggle('is-active', button.getAttribute('data-lang') === lang);
    }});
  }}
  buttons.forEach(function(button) {{
    button.addEventListener('click', function() {{
      setLanguage(button.getAttribute('data-lang') || 'zh');
    }});
  }});
  document.querySelectorAll('.bubble-node').forEach(function(node) {{
    function toggleNode() {{
      const svg = node.closest('svg');
      if (svg) {{
        svg.querySelectorAll('.bubble-node.is-active').forEach(function(activeNode) {{
          if (activeNode !== node) activeNode.classList.remove('is-active');
        }});
      }}
      node.classList.toggle('is-active');
    }}
    node.addEventListener('click', toggleNode);
    node.addEventListener('keydown', function(event) {{
      if (event.key === 'Enter' || event.key === ' ') {{
        event.preventDefault();
        toggleNode();
      }}
    }});
  }});
}}());
</script>
</body>
</html>"""
    return html_doc


def main() -> None:
    args = parse_args()
    input_path = Path(args.input_json).resolve()
    data = read_json(input_path)
    samples = normalize_samples(data)
    plan_entries = normalize_plan(data, samples)
    brands, brand_source, target_kind, entity_candidates, target_profile = load_brand_defs(args, data, samples)
    item_limit = max(1, min(int(args.max_report_items or REPORT_ITEM_LIMIT), 50))
    summary = compute_summary(
        samples,
        brands,
        brand_source,
        plan_entries,
        target_kind,
        entity_candidates,
        target_profile,
        item_limit,
        data.get("input") or {},
        data.get("run") or {},
    )
    summary["input_file"] = input_path.name
    out_dir = Path(args.out_dir).resolve() if args.out_dir else input_path.parent / "report"
    out_dir.mkdir(parents=True, exist_ok=True)
    summary_path = out_dir / "summary.json"
    markdown_path = out_dir / "structured-data.md"
    excel_path = out_dir / "structured-data.xlsx"
    report_path = out_dir / "report.html"
    write_json(summary_path, summary)
    output_files = {
        "raw_json": str(input_path),
        "summary_json": str(summary_path),
        "structured_markdown": str(markdown_path),
        "structured_excel": str(excel_path),
        "html_report": str(report_path),
    }
    export_tables = structured_export_tables(summary, output_files)
    write_structured_markdown(markdown_path, summary, export_tables)
    write_structured_xlsx(excel_path, export_tables)
    report_path.write_text(render_report(args.title, input_path.name, summary), encoding="utf-8")
    print(
        json.dumps(
            {
                "ok": True,
                "raw_json": str(input_path),
                "summary": str(summary_path),
                "structured_markdown": str(markdown_path),
                "structured_excel": str(excel_path),
                "html": str(report_path),
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
