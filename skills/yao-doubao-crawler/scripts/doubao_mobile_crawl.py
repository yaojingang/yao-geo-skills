#!/usr/bin/env python3
from __future__ import annotations

import argparse
import base64
import datetime as dt
import difflib
import hashlib
import json
import os
import random
import re
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path
from typing import Any


DEFAULT_APP_PACKAGE = "com.larus.nova"
DEFAULT_SERVER = "http://127.0.0.1:4723"
MINUTE_SECONDS = 60
MAX_DELAY_SECONDS = 24 * 60 * 60
STOP_GENERATING_RE = re.compile(
    r"(停止生成|停止回答|暂停生成|stop generating|stop responding|cancel response)",
    re.I,
)
URL_RE = re.compile(r"https?://[^\s<>\")'\]\[]+")
DOMAIN_RE = re.compile(
    r"(?<!@)\b([a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?"
    r"(?:\.[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?)+)\b",
    re.I,
)
CONTROL_TEXT_RE = re.compile(
    r"^(发送|重新生成|复制|分享|更多|菜单|返回|关闭|停止生成|停止回答|"
    r"请输入|问问豆包|有问题尽管问|输入消息|send|copy|share|more|back)$",
    re.I,
)
REFERENCE_TITLE_RE = re.compile(r"搜索\s*(\d+)\s*个关键词[，,]\s*参考\s*(\d+)\s*篇资料")
MATERIAL_INDEX_RE = re.compile(r"^(\d+)[.。]?$")


@dataclass
class MobileNode:
    text: str
    content_desc: str
    resource_id: str
    class_name: str
    bounds: tuple[int, int, int, int] | None
    clickable: bool
    enabled: bool

    @property
    def label(self) -> str:
        return clean_text(self.text or self.content_desc)

    @property
    def center(self) -> tuple[int, int] | None:
        if not self.bounds:
            return None
        left, top, right, bottom = self.bounds
        return ((left + right) // 2, (top + bottom) // 2)


def utc_now() -> str:
    return dt.datetime.now(dt.UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def clean_text(value: Any) -> str:
    return re.sub(r"[ \t\f\v]+", " ", str(value or "")).strip()


def multiline_text(value: Any) -> str:
    text = str(value or "").replace("\r\n", "\n").replace("\r", "\n")
    lines = [clean_text(line) for line in text.split("\n")]
    return "\n".join(line for line in lines if line)


def stable_hash(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()[:16]


def parse_bounds(value: str) -> tuple[int, int, int, int] | None:
    match = re.match(r"\[(\d+),(\d+)\]\[(\d+),(\d+)\]", str(value or ""))
    if not match:
        return None
    return tuple(int(part) for part in match.groups())  # type: ignore[return-value]


def parse_bool(value: str) -> bool:
    return str(value or "").lower() == "true"


def strip_url_punctuation(value: str) -> str:
    text = str(value or "").strip()
    text = re.sub(r"\[__LINK_ICON\]?$", "", text)
    return text.rstrip(").,，。;；、]")


def strip_link_icon_marker(value: str) -> str:
    return re.sub(r"\[?__LINK_ICON\]?", "", str(value or ""))


def domain_from_url(url: str) -> str:
    text = strip_url_punctuation(url)
    match = re.match(r"https?://([^/?#]+)", text, re.I)
    if not match:
        return ""
    return normalize_domain(match.group(1))


def normalize_domain(value: str) -> str:
    return re.sub(r"^www\.", "", clean_text(value).lower())


def parse_xml_nodes(xml_text: str) -> list[MobileNode]:
    if not clean_text(xml_text):
        return []
    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError:
        return []
    nodes: list[MobileNode] = []
    for element in root.iter():
        attrib = element.attrib
        class_name = attrib.get("class", "")
        if element.tag != "node" and not class_name:
            class_name = element.tag
        if element.tag == "hierarchy":
            continue
        nodes.append(
            MobileNode(
                text=attrib.get("text", ""),
                content_desc=attrib.get("content-desc", ""),
                resource_id=attrib.get("resource-id", ""),
                class_name=class_name,
                bounds=parse_bounds(attrib.get("bounds", "")),
                clickable=parse_bool(attrib.get("clickable", "")),
                enabled=parse_bool(attrib.get("enabled", "")),
            )
        )
    return nodes


def visible_texts_from_xml(xml_text: str) -> list[str]:
    values: list[str] = []
    seen: set[str] = set()
    for node in parse_xml_nodes(xml_text):
        for raw in (node.text, node.content_desc):
            text = multiline_text(raw)
            if not text:
                continue
            for line in text.split("\n"):
                line = clean_text(line)
                if not line or line in seen:
                    continue
                seen.add(line)
                values.append(line)
    return values


def merge_visible_texts(screens: list[list[str]], baseline: set[str], prompt: str) -> str:
    prompt_clean = clean_text(prompt)
    lines: list[str] = []
    seen: set[str] = set()
    for screen in screens:
        for line in screen:
            text = clean_text(line)
            if not text or text in seen:
                continue
            if text == prompt_clean:
                continue
            if text in baseline and len(text) <= 120:
                continue
            if CONTROL_TEXT_RE.search(text):
                continue
            seen.add(text)
            lines.append(text)
    if not lines:
        for screen in screens:
            for line in screen:
                text = clean_text(line)
                if text and text != prompt_clean and text not in seen and not CONTROL_TEXT_RE.search(text):
                    seen.add(text)
                    lines.append(text)
    return "\n".join(lines)


def collect_references_from_texts(texts: list[str]) -> dict[str, Any]:
    items: list[dict[str, Any]] = []
    seen: set[str] = set()

    def add(title: str, url: str = "", source: str = "", domain: str = "", confidence: str = "low") -> None:
        cleaned_url = strip_url_punctuation(url)
        detected_domain = normalize_domain(domain or domain_from_url(cleaned_url))
        if not detected_domain and not cleaned_url:
            domain_match = DOMAIN_RE.search(title)
            if domain_match:
                detected_domain = normalize_domain(domain_match.group(1))
        if detected_domain == "doubao.com":
            return
        key = (cleaned_url or f"{detected_domain}|{clean_text(title)}").lower()
        if not key or key in seen:
            return
        seen.add(key)
        label = clean_text(source) or detected_domain
        items.append(
            {
                "number": len(items) + 1,
                "source": label,
                "domain": detected_domain,
                "title": clean_text(title) or detected_domain or cleaned_url,
                "date": "",
                "url": cleaned_url,
                "summary": "",
                "confidence": confidence,
                "failure_reason": "" if cleaned_url else "visible_reference_without_url",
            }
        )

    for text in texts:
        line = clean_text(text)
        if not line:
            continue
        for match in URL_RE.finditer(line):
            matched_url = match.group(0)
            url = strip_url_punctuation(matched_url)
            title = strip_link_icon_marker(line.replace(matched_url, "")).strip(" -:：[]")
            add(title or url, url, confidence="high")
        if URL_RE.search(line):
            continue
        domain_match = DOMAIN_RE.search(line)
        if domain_match:
            domain = normalize_domain(domain_match.group(1))
            add(line, "", domain, domain, confidence="medium")

    return {
        "requested": True,
        "count": len(items),
        "items": items,
        "note": "" if items else "No visible URL or domain-like citation text was found in the mobile UI.",
    }


def normalize_match_text(value: str) -> str:
    text = clean_text(value).lower()
    text = text.replace("[__link_icon]", "")
    text = re.sub(r"https?://\S+", " ", text)
    text = re.sub(r"[^\w\u4e00-\u9fff]+", "", text)
    return text


def parse_reference_summary(texts: list[str]) -> dict[str, int | None]:
    for text in texts:
        match = REFERENCE_TITLE_RE.search(clean_text(text))
        if match:
            return {"keyword_count": int(match.group(1)), "material_count": int(match.group(2))}
    return {"keyword_count": None, "material_count": None}


def extract_reference_keywords(texts: list[str]) -> list[str]:
    keywords: list[str] = []
    seen: set[str] = set()
    for text in texts:
        if REFERENCE_TITLE_RE.search(clean_text(text)):
            continue
        matches = re.findall(r"[“\"]([^”\"]{2,80})[”\"]", text)
        if len(matches) < 2:
            remainder = re.sub(r"[“\"]([^”\"]{2,80})[”\"]", "", text).strip(" \t,，、;；")
            if len(matches) != 1 or remainder:
                continue
        for keyword in matches:
            cleaned = clean_text(keyword)
            if cleaned and cleaned not in seen:
                seen.add(cleaned)
                keywords.append(cleaned)
    return keywords


def extract_visible_search_materials(xml_text: str) -> list[dict[str, Any]]:
    materials: list[dict[str, Any]] = []
    pending_index: int | None = None
    pending_index_bounds: tuple[int, int, int, int] | None = None
    for node in parse_xml_nodes(xml_text):
        if node.resource_id == "com.larus.nova:id/tv_reference_index":
            match = MATERIAL_INDEX_RE.match(clean_text(node.label))
            if match:
                pending_index = int(match.group(1))
                pending_index_bounds = node.bounds
            continue
        if node.resource_id != "com.larus.nova:id/tv_reference_content":
            continue
        title = clean_text(node.label)
        if not title:
            continue
        index = pending_index if pending_index is not None else len(materials) + 1
        materials.append(
            {
                "index": index,
                "number": index,
                "title": title,
                "source": "",
                "domain": domain_from_url(first_url_in_text(title)),
                "url": first_url_in_text(title),
                "summary": "",
                "visible_bounds": {
                    "index": list(pending_index_bounds) if pending_index_bounds else None,
                    "title": list(node.bounds) if node.bounds else None,
                },
                "clickable": node.clickable,
                "confidence": "medium",
                "failure_reason": "" if node.clickable else "visible_material_not_clickable",
                "detail_artifacts": {},
            }
        )
        pending_index = None
        pending_index_bounds = None
    return materials


def merge_search_materials(existing: dict[int, dict[str, Any]], visible: list[dict[str, Any]]) -> None:
    for item in visible:
        index = int(item.get("index") or len(existing) + 1)
        current = existing.get(index)
        if current is None:
            existing[index] = item
            continue
        for key in ("title", "source", "domain", "url", "summary", "confidence", "failure_reason"):
            if not current.get(key) and item.get(key):
                current[key] = item[key]
        current["visible_bounds"] = item.get("visible_bounds") or current.get("visible_bounds") or {}
        current["clickable"] = bool(current.get("clickable") or item.get("clickable"))


def title_similarity(left: str, right: str) -> float:
    a = normalize_match_text(left)
    b = normalize_match_text(right)
    if not a or not b:
        return 0.0
    if a in b or b in a:
        return 1.0 if min(len(a), len(b)) >= 6 else 0.75
    ratio = difflib.SequenceMatcher(None, a, b).ratio()
    a_chars = set(a)
    b_chars = set(b)
    overlap = len(a_chars & b_chars) / max(1, min(len(a_chars), len(b_chars)))
    return max(ratio, overlap * 0.9)


def longest_common_substring_length(left: str, right: str) -> int:
    if not left or not right:
        return 0
    previous = [0] * (len(right) + 1)
    best = 0
    for left_char in left:
        current = [0] * (len(right) + 1)
        for index, right_char in enumerate(right, start=1):
            if left_char == right_char:
                current[index] = previous[index - 1] + 1
                best = max(best, current[index])
        previous = current
    return best


def strip_title_match_noise(value: str) -> str:
    text = normalize_match_text(value)
    text = re.sub(r"20\d{2}", "", text)
    for token in (
        "第一季度",
        "第二季度",
        "第三季度",
        "第四季度",
        "第1季度",
        "第2季度",
        "第3季度",
        "第4季度",
        "一季度",
        "二季度",
        "三季度",
        "四季度",
        "q1",
        "q2",
        "q3",
        "q4",
        "财年",
        "财务业绩",
        "财报",
        "业绩",
        "官方",
        "披露",
        "主营业务",
        "业务说明",
        "股份有限公司",
        "有限公司",
        "集团",
        "公司",
    ):
        text = text.replace(token, "")
    return text


def has_meaningful_title_overlap(left: str, right: str) -> bool:
    stripped_left = strip_title_match_noise(left)
    stripped_right = strip_title_match_noise(right)
    if not stripped_left or not stripped_right:
        return False
    if title_similarity(stripped_left, stripped_right) >= 0.55:
        return True
    return longest_common_substring_length(stripped_left, stripped_right) >= 3


def title_years(value: str) -> set[str]:
    return set(re.findall(r"20\d{2}", value or ""))


def title_quarters(value: str) -> set[int]:
    text = clean_text(value).lower()
    quarters: set[int] = set()
    zh = {"一": 1, "二": 2, "三": 3, "四": 4, "1": 1, "2": 2, "3": 3, "4": 4}
    for match in re.finditer(r"第?\s*([一二三四1234])\s*(?:季度|财季)", text):
        quarters.add(zh[match.group(1)])
    for match in re.finditer(r"\bq([1-4])\b", text):
        quarters.add(int(match.group(1)))
    return quarters


def stock_codes(value: str) -> set[str]:
    codes = set(re.findall(r"\b(?:hk)?(\d{4,6})(?:\.hk)?\b", clean_text(value).lower()))
    return {code for code in codes if code != "2026" and code != "2025"}


def semantic_title_match(left: str, right: str) -> tuple[bool, str, float]:
    a = normalize_match_text(left)
    b = normalize_match_text(right)
    if not a or not b:
        return False, "", 0.0
    years_a = title_years(left)
    years_b = title_years(right)
    quarters_a = title_quarters(left)
    quarters_b = title_quarters(right)
    has_same_period = bool(years_a & years_b) and bool(quarters_a & quarters_b)
    finance_terms_a = any(term in a for term in ("财务业绩", "财报", "业绩"))
    finance_terms_b = any(term in b for term in ("财务业绩", "财报", "业绩"))
    if has_same_period and finance_terms_a and finance_terms_b and has_meaningful_title_overlap(left, right):
        return True, "same_entity_financial_period", 0.86

    codes_a = stock_codes(left)
    codes_b = stock_codes(right)
    if codes_a & codes_b:
        if "同花顺" in a or "同花顺" in b or "f10" in a or "f10" in b or has_meaningful_title_overlap(left, right):
            return True, "same_stock_code_source", 0.84

    source_terms = ("同花顺", "新东方网", "腾讯新闻", "新京报", "经济观察报", "南方都市报", "企查查")
    for term in source_terms:
        if term in left and term in right and has_meaningful_title_overlap(left, right):
            return True, "same_named_source", 0.8
    return False, "", 0.0


def bracket_citation_count(answer_text: str, index: int) -> int:
    patterns = [
        rf"[［\[]\s*{index}\s*[］\]]",
        rf"【\s*{index}\s*】",
        rf"\^\s*{index}\b",
    ]
    return sum(len(re.findall(pattern, answer_text)) for pattern in patterns)


def annotate_material_citations(
    materials: dict[str, Any],
    answer_text: str,
    references: dict[str, Any],
) -> dict[str, Any]:
    reference_items = list((references or {}).get("items") or [])
    for material in materials.get("items", []):
        evidence: list[dict[str, Any]] = []
        count = 0
        material_url = strip_url_punctuation(clean_text(material.get("url")))
        material_domain = normalize_domain(clean_text(material.get("domain")) or domain_from_url(material_url))
        material_title = clean_text(material.get("title"))

        index_count = bracket_citation_count(answer_text, int(material.get("index") or 0))
        if index_count:
            evidence.append({"type": "number_marker", "count": index_count})
            count += index_count

        if material_url:
            url_count = answer_text.count(material_url)
            if url_count:
                evidence.append({"type": "url_match", "url": material_url, "count": url_count})
                count += url_count

        best_reference_score = 0.0
        matched_reference_numbers: list[int] = []
        for ref in reference_items:
            ref_url = strip_url_punctuation(clean_text(ref.get("url")))
            ref_domain = normalize_domain(clean_text(ref.get("domain")) or domain_from_url(ref_url))
            ref_title = clean_text(ref.get("title"))
            matched = False
            if material_url and ref_url and material_url == ref_url:
                evidence.append({"type": "reference_url_match", "reference_number": ref.get("number"), "url": ref_url})
                matched = True
            elif material_domain and ref_domain and material_domain == ref_domain:
                evidence.append({"type": "reference_domain_match", "reference_number": ref.get("number"), "domain": ref_domain})
                matched = True
            else:
                semantic_ok, semantic_reason, semantic_score = semantic_title_match(material_title, ref_title)
                if semantic_ok:
                    evidence.append(
                        {
                            "type": "reference_semantic_title_match",
                            "reference_number": ref.get("number"),
                            "reason": semantic_reason,
                            "score": round(semantic_score, 3),
                        }
                    )
                    matched = True
                    score = semantic_score
                else:
                    score = title_similarity(material_title, ref_title)
                best_reference_score = max(best_reference_score, score)
                if not matched and score >= 0.82:
                    evidence.append(
                        {
                            "type": "reference_title_match",
                            "reference_number": ref.get("number"),
                            "score": round(score, 3),
                        }
                    )
                    matched = True
            if matched:
                matched_reference_numbers.append(int(ref.get("number") or 0))

        if matched_reference_numbers:
            count = max(count, len(set(matched_reference_numbers)))
        elif material_title:
            direct_title_count = answer_text.count(material_title)
            if direct_title_count:
                evidence.append({"type": "answer_title_match", "count": direct_title_count})
                count += direct_title_count
            elif best_reference_score >= 0.72:
                evidence.append({"type": "weak_title_similarity", "score": round(best_reference_score, 3)})

        material["domain"] = material_domain
        material["cited"] = count > 0
        material["citation_count"] = count
        material["citation_evidence"] = evidence
        if not count and not evidence:
            material["citation_evidence"] = []

    cited_count = sum(1 for item in materials.get("items", []) if item.get("cited"))
    materials["cited_count"] = cited_count
    materials["uncited_count"] = len(materials.get("items", [])) - cited_count
    materials["total_citation_count"] = sum(int(item.get("citation_count") or 0) for item in materials.get("items", []))
    return materials


def empty_search_materials(requested: bool, note: str = "") -> dict[str, Any]:
    return {
        "requested": requested,
        "found": False,
        "keyword_count": None,
        "material_count": None,
        "keywords": [],
        "count": 0,
        "cited_count": 0,
        "uncited_count": 0,
        "total_citation_count": 0,
        "items": [],
        "note": note,
    }


def first_url_in_text(value: str) -> str:
    match = URL_RE.search(value or "")
    return strip_url_punctuation(match.group(0)) if match else ""


def find_reference_node(xml_text: str, ref: dict[str, Any]) -> MobileNode | None:
    terms = [
        clean_text(ref.get("url")),
        clean_text(ref.get("title")),
        clean_text(ref.get("domain")),
        clean_text(ref.get("source")),
    ]
    terms = [term for term in terms if term]
    if not terms:
        return None
    scored: list[tuple[int, MobileNode]] = []
    for node in parse_xml_nodes(xml_text):
        label = node.label
        if not label or not node.center:
            continue
        score = 0
        for term in terms:
            if term and term in label:
                score += 40
            elif term and label in term and len(label) >= 4:
                score += 15
        if node.clickable:
            score += 10
        if score:
            scored.append((score, node))
    if not scored:
        return None
    return sorted(scored, key=lambda item: item[0], reverse=True)[0][1]


def recover_reference_links(
    driver: Any,
    references: dict[str, Any],
    artifact_dir: Path,
    sample_id: str,
    app_package: str,
    trace: list[dict[str, Any]],
) -> None:
    if not references.get("items"):
        return
    for index, ref in enumerate(references["items"], start=1):
        if ref.get("url"):
            continue
        source_before = driver.page_source
        node = find_reference_node(source_before, ref)
        if not node or not node.center:
            ref["failure_reason"] = ref.get("failure_reason") or "no_clickable_reference_node"
            continue
        x, y = node.center
        try:
            tap_point(driver, x, y, trace, "tap_reference_for_link")
            time.sleep(2.0)
            recovered_texts: list[str] = []
            try:
                recovered_texts.append(clean_text(driver.get_clipboard_text()))
            except Exception as error:
                trace.append({"at": utc_now(), "action": "read_clipboard_after_reference", "ok": False, "error": str(error)})
            try:
                recovered_texts.extend(visible_texts_from_xml(driver.page_source))
            except Exception:
                pass
            recovered_url = ""
            for text in recovered_texts:
                recovered_url = first_url_in_text(text)
                if recovered_url:
                    break
            attempt_prefix = f"link-attempt-{index:02d}"
            xml_file = artifact_dir / "xml" / sample_id / f"{attempt_prefix}.xml"
            shot_file = artifact_dir / "screenshots" / sample_id / f"{attempt_prefix}.png"
            write_text(xml_file, driver.page_source)
            save_screenshot(driver, shot_file)
            trace.append(
                {
                    "at": utc_now(),
                    "action": "capture_reference_link_attempt",
                    "reference_number": ref.get("number") or index,
                    "screenshot": os.path.relpath(shot_file, artifact_dir),
                    "page_source": os.path.relpath(xml_file, artifact_dir),
                    "recovered_url": recovered_url,
                }
            )
            if recovered_url:
                ref["url"] = recovered_url
                ref["domain"] = domain_from_url(recovered_url)
                ref["confidence"] = "high"
                ref["failure_reason"] = ""
            else:
                ref["confidence"] = ref.get("confidence") or "low"
                ref["failure_reason"] = ref.get("failure_reason") or "link_recovery_attempt_failed"
        except Exception as error:
            ref["failure_reason"] = ref.get("failure_reason") or f"link_recovery_error: {error}"
            trace.append({"at": utc_now(), "action": "recover_reference_link_failed", "reference_number": ref.get("number") or index, "error": str(error)})
        finally:
            try:
                driver.back()
                time.sleep(0.5)
            except Exception:
                pass
            activate_app(driver, app_package, trace)


def find_search_material_toggle_node(xml_text: str) -> MobileNode | None:
    candidates: list[MobileNode] = []
    for node in parse_xml_nodes(xml_text):
        if node.resource_id == "com.larus.nova:id/ll_reference_title" and node.center:
            candidates.append(node)
        elif node.center and node.clickable and REFERENCE_TITLE_RE.search(node.label):
            candidates.append(node)
    if candidates:
        return sorted(candidates, key=lambda node: len(node.label), reverse=True)[0]
    title_node = next(
        (
            node
            for node in parse_xml_nodes(xml_text)
            if node.resource_id == "com.larus.nova:id/tv_reference_title" and REFERENCE_TITLE_RE.search(node.label)
        ),
        None,
    )
    if title_node and title_node.center:
        return title_node
    return None


def find_material_content_node(xml_text: str, material: dict[str, Any]) -> MobileNode | None:
    wanted_index = int(material.get("index") or 0)
    wanted_title = clean_text(material.get("title"))
    pending_index: int | None = None
    best: tuple[float, MobileNode] | None = None
    for node in parse_xml_nodes(xml_text):
        if node.resource_id == "com.larus.nova:id/tv_reference_index":
            match = MATERIAL_INDEX_RE.match(clean_text(node.label))
            pending_index = int(match.group(1)) if match else None
            continue
        if node.resource_id != "com.larus.nova:id/tv_reference_content" or not node.center:
            continue
        if wanted_index and pending_index == wanted_index:
            return node
        score = title_similarity(wanted_title, node.label)
        if score > (best[0] if best else 0):
            best = (score, node)
    return best[1] if best and best[0] >= 0.82 else None


def scroll_material_panel(driver: Any, trace: list[dict[str, Any]]) -> bool:
    size = driver.get_window_size()
    left = int(size["width"] * 0.12)
    top = int(size["height"] * 0.38)
    width = int(size["width"] * 0.82)
    height = int(size["height"] * 0.44)
    try:
        result = driver.execute_script(
            "mobile: swipeGesture",
            {"left": left, "top": top, "width": width, "height": height, "direction": "up", "percent": 0.82},
        )
        trace.append({"at": utc_now(), "action": "scroll_search_materials", "ok": bool(result), "method": "swipeGesture"})
        return bool(result)
    except Exception as swipe_error:
        try:
            result = driver.execute_script(
                "mobile: scrollGesture",
                {"left": left, "top": top, "width": width, "height": height, "direction": "down", "percent": 0.82},
            )
            trace.append({"at": utc_now(), "action": "scroll_search_materials", "ok": bool(result), "method": "scrollGesture"})
            return bool(result)
        except Exception as scroll_error:
            trace.append(
                {
                    "at": utc_now(),
                    "action": "scroll_search_materials",
                    "ok": False,
                    "swipe_error": str(swipe_error),
                    "scroll_error": str(scroll_error),
                }
            )
            return False


def capture_search_material_screen(
    driver: Any,
    artifact_dir: Path,
    sample_id: str,
    screen_index: int,
    trace: list[dict[str, Any]],
) -> tuple[str, list[str], str, str]:
    source = driver.page_source
    texts = visible_texts_from_xml(source)
    xml_file = artifact_dir / "xml" / sample_id / f"search-materials-{screen_index:02d}.xml"
    shot_file = artifact_dir / "screenshots" / sample_id / f"search-materials-{screen_index:02d}.png"
    write_text(xml_file, source)
    save_screenshot(driver, shot_file)
    xml_ref = os.path.relpath(xml_file, artifact_dir)
    shot_ref = os.path.relpath(shot_file, artifact_dir)
    trace.append(
        {
            "at": utc_now(),
            "action": "capture_search_materials_screen",
            "index": screen_index,
            "text_count": len(texts),
            "screenshot": shot_ref,
            "page_source": xml_ref,
        }
    )
    return source, texts, xml_ref, shot_ref


def recover_url_from_texts(texts: list[str]) -> tuple[str, str]:
    for text in texts:
        url = first_url_in_text(text)
        if url and domain_from_url(url) != "doubao.com":
            return url, domain_from_url(url)
    for text in texts:
        match = DOMAIN_RE.search(text)
        if match:
            domain = normalize_domain(match.group(1))
            if domain and domain != "doubao.com":
                return "", domain
    return "", ""


def reset_search_material_panel(driver: Any, trace: list[dict[str, Any]]) -> bool:
    source = driver.page_source
    toggle = find_search_material_toggle_node(source)
    if not toggle or not toggle.center:
        trace.append({"at": utc_now(), "action": "reset_search_material_panel", "ok": False, "reason": "toggle_not_visible"})
        return False
    try:
        if extract_visible_search_materials(source):
            x, y = toggle.center
            tap_point(driver, x, y, trace, "collapse_search_materials")
            time.sleep(0.5)
            source = driver.page_source
            toggle = find_search_material_toggle_node(source)
            if not toggle or not toggle.center:
                trace.append({"at": utc_now(), "action": "reset_search_material_panel", "ok": False, "reason": "toggle_missing_after_collapse"})
                return False
        x, y = toggle.center
        tap_point(driver, x, y, trace, "expand_search_materials")
        time.sleep(0.8)
        ok = bool(extract_visible_search_materials(driver.page_source))
        trace.append({"at": utc_now(), "action": "reset_search_material_panel", "ok": ok})
        return ok
    except Exception as error:
        trace.append({"at": utc_now(), "action": "reset_search_material_panel", "ok": False, "error": str(error)})
        return False


def recover_search_material_details(
    driver: Any,
    materials: dict[str, Any],
    artifact_dir: Path,
    sample_id: str,
    app_package: str,
    args: argparse.Namespace,
    trace: list[dict[str, Any]],
) -> None:
    for material in materials.get("items", []):
        reset_search_material_panel(driver, trace)
        source = driver.page_source
        node = find_material_content_node(source, material)
        if not node:
            for _ in range(args.material_max_scrolls):
                if not scroll_material_panel(driver, trace):
                    break
                time.sleep(0.7)
                source = driver.page_source
                node = find_material_content_node(source, material)
                if node:
                    break
        if not node or not node.center:
            material["failure_reason"] = material.get("failure_reason") or "material_not_visible_for_detail"
            continue
        try:
            x, y = node.center
            tap_point(driver, x, y, trace, "tap_search_material")
            time.sleep(args.material_detail_wait_seconds)
            recovered_texts: list[str] = []
            try:
                recovered_texts.append(clean_text(driver.get_clipboard_text()))
            except Exception as error:
                trace.append({"at": utc_now(), "action": "read_clipboard_after_material", "ok": False, "error": str(error)})
            detail_source = driver.page_source
            recovered_texts.extend(visible_texts_from_xml(detail_source))
            recovered_url, recovered_domain = recover_url_from_texts(recovered_texts)
            index = int(material.get("index") or 0)
            prefix = f"search-material-detail-{index:02d}" if index else "search-material-detail"
            xml_file = artifact_dir / "xml" / sample_id / f"{prefix}.xml"
            shot_file = artifact_dir / "screenshots" / sample_id / f"{prefix}.png"
            write_text(xml_file, detail_source)
            save_screenshot(driver, shot_file)
            material["detail_artifacts"] = {
                "page_source": os.path.relpath(xml_file, artifact_dir),
                "screenshot": os.path.relpath(shot_file, artifact_dir),
            }
            if recovered_url:
                material["url"] = recovered_url
                material["domain"] = domain_from_url(recovered_url)
                material["confidence"] = "high"
                material["failure_reason"] = ""
            elif recovered_domain:
                material["domain"] = recovered_domain
                material["confidence"] = "medium"
                material["failure_reason"] = material.get("failure_reason") or "detail_visible_without_full_url"
            else:
                material["confidence"] = "low"
                material["failure_reason"] = material.get("failure_reason") or "material_detail_without_url"
            trace.append(
                {
                    "at": utc_now(),
                    "action": "capture_search_material_detail",
                    "material_index": material.get("index"),
                    "url": material.get("url") or "",
                    "domain": material.get("domain") or "",
                    "screenshot": material["detail_artifacts"].get("screenshot"),
                    "page_source": material["detail_artifacts"].get("page_source"),
                }
            )
        except Exception as error:
            material["failure_reason"] = material.get("failure_reason") or f"material_detail_error: {error}"
            trace.append({"at": utc_now(), "action": "recover_search_material_detail_failed", "material_index": material.get("index"), "error": str(error)})
        finally:
            try:
                driver.back()
                time.sleep(0.7)
            except Exception:
                pass
            activate_app(driver, app_package, trace)


def collect_search_materials(
    driver: Any,
    args: argparse.Namespace,
    sample_id: str,
    artifact_dir: Path,
    answer_text: str,
    references: dict[str, Any],
    trace: list[dict[str, Any]],
) -> dict[str, Any]:
    if getattr(args, "skip_search_materials", False):
        return empty_search_materials(False, "Search material extraction was disabled.")

    source = driver.page_source
    texts = visible_texts_from_xml(source)
    summary = parse_reference_summary(texts)
    toggle = find_search_material_toggle_node(source)
    already_expanded = bool(extract_visible_search_materials(source))
    if not already_expanded:
        if not toggle or not toggle.center:
            trace.append({"at": utc_now(), "action": "search_materials_not_found"})
            return empty_search_materials(True, "No visible search-material entry was found.")
        x, y = toggle.center
        tap_point(driver, x, y, trace, "tap_search_materials_title")
        time.sleep(0.8)

    collected: dict[int, dict[str, Any]] = {}
    artifacts = {"screenshots": [], "page_sources": []}
    seen_signatures: set[str] = set()
    keywords: list[str] = []
    for screen_index in range(1, args.material_max_scrolls + 2):
        source, texts, xml_ref, shot_ref = capture_search_material_screen(driver, artifact_dir, sample_id, screen_index, trace)
        artifacts["page_sources"].append(xml_ref)
        artifacts["screenshots"].append(shot_ref)
        screen_summary = parse_reference_summary(texts)
        summary = {
            "keyword_count": summary.get("keyword_count") or screen_summary.get("keyword_count"),
            "material_count": summary.get("material_count") or screen_summary.get("material_count"),
        }
        for keyword in extract_reference_keywords(texts):
            if keyword not in keywords:
                keywords.append(keyword)
        merge_search_materials(collected, extract_visible_search_materials(source))
        expected_count = summary.get("material_count")
        signature = stable_hash("\n".join(f"{key}:{item.get('title')}" for key, item in sorted(collected.items())))
        if expected_count and len(collected) >= int(expected_count):
            break
        if signature in seen_signatures:
            trace.append({"at": utc_now(), "action": "stop_search_material_scroll", "reason": "repeated_material_signature"})
            break
        seen_signatures.add(signature)
        if screen_index > args.material_max_scrolls:
            break
        if not scroll_material_panel(driver, trace):
            break
        time.sleep(0.8)

    items = [collected[index] for index in sorted(collected)]
    materials = {
        "requested": True,
        "found": bool(items),
        "keyword_count": summary.get("keyword_count"),
        "material_count": summary.get("material_count"),
        "keywords": keywords,
        "count": len(items),
        "cited_count": 0,
        "uncited_count": len(items),
        "total_citation_count": 0,
        "items": items,
        "artifacts": artifacts,
        "note": "",
    }
    expected = materials.get("material_count")
    if expected and len(items) < int(expected):
        missing = [index for index in range(1, int(expected) + 1) if index not in collected]
        materials["missing_indices"] = missing
        materials["note"] = f"Only {len(items)} of {expected} visible search materials were exposed through UiAutomator2."
    if items and (getattr(args, "recover_material_links", False) or getattr(args, "recover_links", False)):
        recover_search_material_details(driver, materials, artifact_dir, sample_id, args.app_package, args, trace)
    return annotate_material_citations(materials, answer_text, references)


def extract_headings(text: str) -> list[str]:
    headings: list[str] = []
    for line in text.splitlines():
        cleaned = clean_text(line)
        if re.match(r"^#{1,6}\s+\S", cleaned):
            headings.append(re.sub(r"^#{1,6}\s+", "", cleaned))
        elif re.match(r"^(\d+[.、]|[一二三四五六七八九十]+[、.])\s*\S+", cleaned):
            headings.append(cleaned)
    return headings[:50]


def count_occurrences(text: str, target: str) -> int | None:
    if not target:
        return None
    return len(re.findall(re.escape(target), text, flags=re.I))


def read_json(file: Path) -> dict[str, Any] | None:
    try:
        data = json.loads(file.read_text(encoding="utf-8"))
    except Exception:
        return None
    return data if isinstance(data, dict) else None


def write_json(file: Path, value: Any) -> None:
    file.parent.mkdir(parents=True, exist_ok=True)
    file.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_text(file: Path, value: str) -> None:
    file.parent.mkdir(parents=True, exist_ok=True)
    file.write_text(value, encoding="utf-8")


def append_text(file: Path, value: str) -> None:
    file.parent.mkdir(parents=True, exist_ok=True)
    with file.open("a", encoding="utf-8") as handle:
        handle.write(value)


def run_command(command: list[str], timeout: int = 30) -> dict[str, Any]:
    try:
        result = subprocess.run(
            command,
            check=False,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout,
        )
        return {
            "ok": result.returncode == 0,
            "returncode": result.returncode,
            "stdout": result.stdout.strip(),
            "stderr": result.stderr.strip(),
        }
    except FileNotFoundError as error:
        return {"ok": False, "returncode": None, "stdout": "", "stderr": str(error)}
    except subprocess.TimeoutExpired as error:
        return {
            "ok": False,
            "returncode": None,
            "stdout": (error.stdout or "").strip() if isinstance(error.stdout, str) else "",
            "stderr": "command timed out",
        }


def adb_command(args: argparse.Namespace, extra: list[str], timeout: int = 30) -> dict[str, Any]:
    adb = args.adb_path or "adb"
    command = [adb]
    if getattr(args, "device", ""):
        command.extend(["-s", args.device])
    command.extend(extra)
    return run_command(command, timeout=timeout)


def appium_status(server: str, timeout: int = 5) -> dict[str, Any]:
    url = server.rstrip("/") + "/status"
    try:
        with urllib.request.urlopen(url, timeout=timeout) as response:
            body = response.read().decode("utf-8", errors="replace")
        parsed = json.loads(body)
        return {"ok": True, "url": url, "response": parsed}
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as error:
        return {"ok": False, "url": url, "error": str(error)}


def import_appium() -> tuple[Any, Any, Any]:
    try:
        from appium import webdriver
        from appium.options.android import UiAutomator2Options
        from appium.webdriver.common.appiumby import AppiumBy
    except Exception as error:  # pragma: no cover - exercised only without dependency
        raise RuntimeError(
            "Appium Python client is not available. Install it with "
            "`python3 -m pip install -r requirements-mobile.txt`."
        ) from error
    return webdriver, UiAutomator2Options, AppiumBy


def create_driver(args: argparse.Namespace, trace: list[dict[str, Any]] | None = None) -> Any:
    webdriver, UiAutomator2Options, _ = import_appium()
    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.automation_name = "UiAutomator2"
    options.device_name = args.device or "Android"
    options.no_reset = True
    options.new_command_timeout = getattr(args, "new_command_timeout", 300)
    if getattr(args, "app_activity", ""):
        options.app_package = args.app_package
        options.app_activity = args.app_activity
    driver = webdriver.Remote(args.server, options=options)
    if trace is not None:
        trace.append({"at": utc_now(), "action": "driver_session_created"})
    if getattr(args, "app_package", ""):
        activate_app(driver, args.app_package, trace)
    return driver


def activate_app(driver: Any, app_package: str, trace: list[dict[str, Any]] | None = None) -> None:
    try:
        driver.activate_app(app_package)
        if trace is not None:
            trace.append({"at": utc_now(), "action": "activate_app", "package": app_package, "ok": True})
    except Exception as error:
        if trace is not None:
            trace.append(
                {
                    "at": utc_now(),
                    "action": "activate_app",
                    "package": app_package,
                    "ok": False,
                    "error": str(error),
                }
            )


def tap_point(driver: Any, x: int, y: int, trace: list[dict[str, Any]] | None = None, label: str = "tap") -> None:
    try:
        driver.execute_script("mobile: clickGesture", {"x": x, "y": y})
    except Exception:
        # Appium 3 servers support clickGesture; older local setups can fall back
        # to W3C pointer actions through tap coordinates when available.
        try:
            driver.tap([(x, y)])
        except Exception as error:
            if trace is not None:
                trace.append({"at": utc_now(), "action": label, "ok": False, "x": x, "y": y, "error": str(error)})
            raise
    if trace is not None:
        trace.append({"at": utc_now(), "action": label, "ok": True, "x": x, "y": y})


def scroll_screen(driver: Any, direction: str, trace: list[dict[str, Any]] | None = None) -> bool:
    size = driver.get_window_size()
    left = int(size["width"] * 0.08)
    top = int(size["height"] * 0.18)
    width = int(size["width"] * 0.84)
    height = int(size["height"] * 0.62)
    try:
        result = driver.execute_script(
            "mobile: scrollGesture",
            {"left": left, "top": top, "width": width, "height": height, "direction": direction, "percent": 0.75},
        )
        ok = bool(result)
    except Exception as error:
        if trace is not None:
            trace.append({"at": utc_now(), "action": "scroll", "direction": direction, "ok": False, "error": str(error)})
        return False
    if trace is not None:
        trace.append({"at": utc_now(), "action": "scroll", "direction": direction, "ok": ok})
    return ok


def save_screenshot(driver: Any, file: Path) -> bool:
    file.parent.mkdir(parents=True, exist_ok=True)
    try:
        data = driver.get_screenshot_as_png()
        file.write_bytes(data)
        return True
    except Exception:
        try:
            encoded = driver.get_screenshot_as_base64()
            file.write_bytes(base64.b64decode(encoded))
            return True
        except Exception:
            return False


def find_input_node(xml_text: str, preferred_resource_id: str = "") -> MobileNode | None:
    nodes = parse_xml_nodes(xml_text)
    if preferred_resource_id:
        for node in nodes:
            if node.resource_id == preferred_resource_id and node.enabled:
                return node
    scored: list[tuple[int, MobileNode]] = []
    for node in nodes:
        haystack = " ".join([node.text, node.content_desc, node.resource_id, node.class_name]).lower()
        score = 0
        if "edittext" in node.class_name.lower():
            score += 40
        if any(token in haystack for token in ["输入", "提问", "问问", "发消息", "message", "ask", "prompt", "input"]):
            score += 25
        if node.enabled:
            score += 10
        if node.bounds:
            _, top, _, bottom = node.bounds
            score += max(0, min(20, bottom // 100))
            if bottom > 900:
                score += 10
            if bottom - top >= 20:
                score += 5
        if score:
            scored.append((score, node))
    if not scored:
        return None
    return sorted(scored, key=lambda item: item[0], reverse=True)[0][1]


def find_send_node(xml_text: str, preferred_resource_id: str = "") -> MobileNode | None:
    nodes = parse_xml_nodes(xml_text)
    if preferred_resource_id:
        for node in nodes:
            if node.resource_id == preferred_resource_id and node.enabled:
                return node
    scored: list[tuple[int, MobileNode]] = []
    for node in nodes:
        haystack = " ".join([node.text, node.content_desc, node.resource_id]).lower()
        score = 0
        if any(token in haystack for token in ["发送", "提交", "send", "submit"]):
            score += 40
        if "send" in haystack or "publish" in haystack:
            score += 20
        if node.clickable:
            score += 10
        if node.enabled:
            score += 10
        if node.bounds:
            left, top, right, bottom = node.bounds
            if right - left <= 160 and bottom - top <= 160:
                score += 5
            if bottom > 800:
                score += 5
        if score:
            scored.append((score, node))
    if not scored:
        return None
    return sorted(scored, key=lambda item: item[0], reverse=True)[0][1]


def find_new_chat_node(xml_text: str, preferred_resource_id: str = "") -> MobileNode | None:
    nodes = parse_xml_nodes(xml_text)
    if preferred_resource_id:
        for node in nodes:
            if node.resource_id == preferred_resource_id and node.enabled and node.center:
                return node
    scored: list[tuple[int, MobileNode]] = []
    tokens = [
        "创建新对话",
        "新建对话",
        "新对话",
        "新建聊天",
        "新聊天",
        "新建会话",
        "新会话",
        "new chat",
        "new conversation",
    ]
    for node in nodes:
        haystack = " ".join([node.text, node.content_desc, node.resource_id]).lower()
        score = 0
        if any(token in haystack for token in tokens):
            score += 80
        if any(token in haystack for token in ["create", "plus", "add"]) and any(token in haystack for token in ["chat", "conversation", "dialog"]):
            score += 50
        if node.clickable:
            score += 10
        if node.enabled:
            score += 10
        if node.bounds:
            left, top, right, bottom = node.bounds
            if top < 360 and right > 850:
                score += 8
            if right - left <= 180 and bottom - top <= 180:
                score += 5
        if score >= 70 and node.center:
            scored.append((score, node))
    if not scored:
        return None
    return sorted(scored, key=lambda item: item[0], reverse=True)[0][1]


def ensure_fresh_chat(driver: Any, args: argparse.Namespace, trace: list[dict[str, Any]]) -> None:
    if not getattr(args, "fresh_chat", False):
        return

    def tap_new_chat_if_visible(stage: str) -> bool:
        source = driver.page_source
        node = find_new_chat_node(source, getattr(args, "new_chat_resource_id", ""))
        if not node or not node.center:
            trace.append({"at": utc_now(), "action": "fresh_chat_probe", "stage": stage, "ok": False})
            return False
        x, y = node.center
        tap_point(driver, x, y, trace, "tap_new_chat")
        time.sleep(getattr(args, "fresh_chat_wait_seconds", 1.2))
        source_after = driver.page_source
        has_input = find_input_node(source_after, getattr(args, "input_resource_id", "")) is not None
        trace.append(
            {
                "at": utc_now(),
                "action": "fresh_chat_opened",
                "stage": stage,
                "ok": bool(has_input),
                "resource_id": node.resource_id,
                "label": node.label,
            }
        )
        return True

    if tap_new_chat_if_visible("current_screen"):
        return

    for step in range(max(0, getattr(args, "fresh_chat_back_steps", 2))):
        try:
            driver.press_keycode(4)
            trace.append({"at": utc_now(), "action": "fresh_chat_back", "step": step + 1, "ok": True})
        except Exception as error:
            trace.append({"at": utc_now(), "action": "fresh_chat_back", "step": step + 1, "ok": False, "error": str(error)})
            break
        time.sleep(0.8)
        if tap_new_chat_if_visible(f"after_back_{step + 1}"):
            return

    message = "Unable to open a fresh Doubao chat before sending prompt."
    trace.append({"at": utc_now(), "action": "fresh_chat_failed", "error": message})
    if getattr(args, "require_fresh_chat", False):
        raise RuntimeError(message)


def send_prompt(driver: Any, prompt: str, args: argparse.Namespace, trace: list[dict[str, Any]]) -> None:
    _, _, AppiumBy = import_appium()
    source = driver.page_source
    input_node = find_input_node(source, getattr(args, "input_resource_id", ""))
    element = None
    if input_node and input_node.resource_id:
        try:
            element = driver.find_element(AppiumBy.ID, input_node.resource_id)
            element.click()
            trace.append({"at": utc_now(), "action": "click_input", "resource_id": input_node.resource_id, "ok": True})
        except Exception as error:
            trace.append({"at": utc_now(), "action": "click_input", "resource_id": input_node.resource_id, "ok": False, "error": str(error)})
            element = None
    if element is None and input_node and input_node.center:
        x, y = input_node.center
        tap_point(driver, x, y, trace, "tap_input")
    elif element is None:
        size = driver.get_window_size()
        tap_point(driver, size["width"] // 2, int(size["height"] * 0.88), trace, "tap_input_fallback")

    pasted = False
    try:
        driver.set_clipboard_text(prompt)
        time.sleep(0.2)
        driver.press_keycode(279)
        pasted = True
        trace.append({"at": utc_now(), "action": "paste_prompt", "ok": True, "chars": len(prompt)})
    except Exception as error:
        trace.append({"at": utc_now(), "action": "paste_prompt", "ok": False, "error": str(error)})
    if not pasted:
        try:
            target = element or driver.switch_to.active_element
            target.send_keys(prompt)
            trace.append({"at": utc_now(), "action": "send_keys_prompt", "ok": True, "chars": len(prompt)})
        except Exception as error:
            trace.append({"at": utc_now(), "action": "send_keys_prompt", "ok": False, "error": str(error)})
            raise RuntimeError("Unable to enter prompt through clipboard paste or send_keys.") from error

    time.sleep(0.5)
    source = driver.page_source
    send_node = find_send_node(source, getattr(args, "send_resource_id", ""))
    if send_node and send_node.center:
        x, y = send_node.center
        tap_point(driver, x, y, trace, "tap_send")
    else:
        try:
            driver.press_keycode(66)
            trace.append({"at": utc_now(), "action": "press_enter_to_send", "ok": True})
        except Exception as error:
            trace.append({"at": utc_now(), "action": "press_enter_to_send", "ok": False, "error": str(error)})
            raise RuntimeError("Unable to find or activate the send button.") from error


def wait_for_answer_stable(driver: Any, args: argparse.Namespace, trace: list[dict[str, Any]]) -> str:
    started = time.monotonic()
    last_signature = ""
    stable_since: float | None = None
    latest_source = ""
    while time.monotonic() - started <= args.timeout:
        latest_source = driver.page_source
        texts = visible_texts_from_xml(latest_source)
        visible_text = "\n".join(texts)
        signature = stable_hash(visible_text)
        generating = any(STOP_GENERATING_RE.search(text) for text in texts)
        if signature != last_signature:
            last_signature = signature
            stable_since = time.monotonic()
        stable_for = 0 if stable_since is None else time.monotonic() - stable_since
        trace.append(
            {
                "at": utc_now(),
                "action": "wait_answer",
                "signature": signature,
                "stable_for_seconds": round(stable_for, 2),
                "generating": generating,
            }
        )
        if not generating and stable_for >= args.stable_seconds:
            return latest_source
        time.sleep(args.poll_seconds)
    raise TimeoutError(f"Answer did not stabilize within {args.timeout} seconds.")


def collect_screens(driver: Any, args: argparse.Namespace, sample_id: str, artifact_dir: Path, trace: list[dict[str, Any]]) -> tuple[list[list[str]], list[str], list[str]]:
    screenshots: list[str] = []
    page_sources: list[str] = []
    screen_texts: list[list[str]] = []
    seen_signatures: set[str] = set()

    for index in range(args.max_scrolls + 1):
        source = driver.page_source
        texts = visible_texts_from_xml(source)
        signature = stable_hash("\n".join(texts))
        xml_file = artifact_dir / "xml" / sample_id / f"screen-{index + 1:02d}.xml"
        shot_file = artifact_dir / "screenshots" / sample_id / f"screen-{index + 1:02d}.png"
        xml_ref = os.path.relpath(xml_file, artifact_dir)
        shot_ref = os.path.relpath(shot_file, artifact_dir)
        write_text(xml_file, source)
        save_screenshot(driver, shot_file)
        page_sources.append(xml_ref)
        screenshots.append(shot_ref)
        screen_texts.append(texts)
        trace.append(
            {
                "at": utc_now(),
                "action": "capture_screen",
                "index": index + 1,
                "text_count": len(texts),
                "signature": signature,
                "screenshot": shot_ref,
                "page_source": xml_ref,
            }
        )
        if index >= args.max_scrolls:
            break
        if signature in seen_signatures:
            trace.append({"at": utc_now(), "action": "stop_scroll", "reason": "repeated_screen_signature"})
            break
        seen_signatures.add(signature)
        if not scroll_screen(driver, args.scroll_direction, trace):
            break
        time.sleep(0.8)
    return screen_texts, screenshots, page_sources


def capture_once(args: argparse.Namespace, sample_id: str = "capture") -> dict[str, Any]:
    trace: list[dict[str, Any]] = []
    started_at = utc_now()
    artifact_dir = Path(args.artifact_dir).resolve() if args.artifact_dir else Path.cwd().resolve()
    driver = None
    try:
        driver = create_driver(args, trace)
        time.sleep(args.launch_wait_seconds)
        ensure_fresh_chat(driver, args, trace)
        baseline_texts = set(visible_texts_from_xml(driver.page_source))
        trace.append({"at": utc_now(), "action": "baseline_captured", "text_count": len(baseline_texts)})
        send_prompt(driver, args.prompt, args, trace)
        wait_for_answer_stable(driver, args, trace)
        screen_texts, screenshots, page_sources = collect_screens(driver, args, sample_id, artifact_dir, trace)
        all_texts = [text for screen in screen_texts for text in screen]
        answer_text = merge_visible_texts(screen_texts, baseline_texts, args.prompt)
        references = collect_references_from_texts(all_texts + answer_text.splitlines())
        if args.recover_links and references.get("items"):
            recover_reference_links(driver, references, artifact_dir, sample_id, args.app_package, trace)
        try:
            search_materials = collect_search_materials(driver, args, sample_id, artifact_dir, answer_text, references, trace)
        except Exception as error:
            trace.append({"at": utc_now(), "action": "collect_search_materials_failed", "error": str(error)})
            search_materials = empty_search_materials(True, f"Search-material extraction failed: {error}")
        low_confidence_refs = [item for item in references["items"] if not item.get("url")]
        confidence = "high" if references["items"] and not low_confidence_refs else ("medium" if answer_text else "low")
        failure_reason = "" if answer_text else "no_answer_text_extracted"
        if references["items"] and low_confidence_refs:
            failure_reason = "some_references_without_url"
        record = {
            "ok": bool(answer_text),
            "collected_at": utc_now(),
            "engine": "doubao",
            "transport": "appium-uiautomator2-avd",
            "question": args.prompt,
            "options": {
                "device": args.device or None,
                "server": args.server,
                "app_package": args.app_package,
                "app_activity": args.app_activity or None,
                "timeout": args.timeout,
                "stable_seconds": args.stable_seconds,
                "poll_seconds": args.poll_seconds,
                "max_scrolls": args.max_scrolls,
                "scroll_direction": args.scroll_direction,
                "fresh_chat": bool(getattr(args, "fresh_chat", False)),
                "require_fresh_chat": bool(getattr(args, "require_fresh_chat", False)),
                "link_recovery": bool(args.recover_links),
                "search_materials": not bool(args.skip_search_materials),
                "material_link_recovery": bool(args.recover_material_links or args.recover_links),
                "started_at": started_at,
            },
            "page": {
                "title": "Doubao Android",
                "package": args.app_package,
                "activity": args.app_activity or None,
            },
            "answer": {"text": answer_text},
            "references": references,
            "mobile_search_materials": search_materials,
            "mobile": {
                "device": args.device or None,
                "app_package": args.app_package,
                "app_activity": args.app_activity or None,
                "server": args.server,
            },
            "artifacts": {
                "screenshots": screenshots,
                "page_sources": page_sources,
            },
            "extraction": {
                "char_count": len(answer_text),
                "line_count": len(answer_text.splitlines()) if answer_text else 0,
                "headings": extract_headings(answer_text),
                "reference_count": references["count"],
                "search_material_count": search_materials.get("count", 0),
                "cited_search_material_count": search_materials.get("cited_count", 0),
                "uncited_search_material_count": search_materials.get("uncited_count", 0),
                "target": getattr(args, "target", "") or getattr(args, "target_entity", "") or None,
                "target_mention_count": count_occurrences(answer_text, getattr(args, "target", "") or getattr(args, "target_entity", "")),
                "confidence": confidence,
                "failure_reason": failure_reason,
            },
            "confidence": confidence,
            "failure_reason": failure_reason,
            "action_trace": trace,
            "raw": {"visible_text_count": len(set(all_texts))},
        }
        return record
    except Exception as error:
        trace.append({"at": utc_now(), "action": "capture_failed", "error": str(error)})
        return {
            "ok": False,
            "collected_at": utc_now(),
            "engine": "doubao",
            "transport": "appium-uiautomator2-avd",
            "question": args.prompt,
            "options": {
                "device": args.device or None,
                "server": args.server,
                "app_package": args.app_package,
                "app_activity": args.app_activity or None,
                "started_at": started_at,
            },
            "page": {"title": "Doubao Android", "package": args.app_package, "activity": args.app_activity or None},
            "answer": {"text": ""},
            "references": {"requested": True, "count": 0, "items": [], "note": "Capture failed before reference extraction."},
            "mobile_search_materials": empty_search_materials(True, "Capture failed before search-material extraction."),
            "mobile": {"device": args.device or None, "app_package": args.app_package, "app_activity": args.app_activity or None, "server": args.server},
            "artifacts": {"screenshots": [], "page_sources": []},
            "extraction": {
                "char_count": 0,
                "line_count": 0,
                "headings": [],
                "reference_count": 0,
                "search_material_count": 0,
                "cited_search_material_count": 0,
                "uncited_search_material_count": 0,
                "target": getattr(args, "target", "") or getattr(args, "target_entity", "") or None,
                "target_mention_count": None,
                "confidence": "low",
                "failure_reason": str(error),
            },
            "confidence": "low",
            "failure_reason": str(error),
            "action_trace": trace,
            "raw": {},
        }
    finally:
        if driver is not None:
            try:
                driver.quit()
            except Exception:
                pass


def reusable_raw(existing: dict[str, Any], sample: dict[str, Any]) -> tuple[bool, str]:
    if not existing.get("ok"):
        return False, "existing raw result had ok=false"
    if clean_text(existing.get("question")) != clean_text(sample["question"]):
        return False, "existing raw result question does not match current plan"
    answer = clean_text(((existing.get("answer") or {}).get("text")))
    if not answer:
        return False, "existing raw result has no answer text"
    return True, ""


def safe_id(value: Any, fallback: str) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9._-]+", "-", str(value or "").strip()).strip("-")
    return (cleaned or fallback)[:80]


def timestamp_id() -> str:
    return dt.datetime.now(dt.UTC).strftime("%Y%m%dT%H%M%SZ")


def split_aliases(value: str) -> list[str]:
    return [item.strip() for item in re.split(r"[|,，;；\n\r\t]+", value or "") if item.strip()]


def normalize_entity_type(value: str) -> str:
    key = clean_text(value).lower()
    mapping = {
        "person": "person",
        "people": "person",
        "human": "person",
        "人": "person",
        "人物": "person",
        "人名": "person",
        "专家": "person",
        "company": "company",
        "brand": "company",
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
    }
    return mapping.get(key, value)


def read_questions(file: Path, global_repeat: int, global_target: str) -> list[dict[str, Any]]:
    raw = file.read_text(encoding="utf-8")
    trimmed = raw.strip()
    if trimmed.startswith("["):
        values = json.loads(trimmed)
    else:
        values = [line.strip() for line in raw.splitlines() if line.strip() and not line.strip().startswith("#")]
    if not isinstance(values, list) or not values:
        raise ValueError("questions must contain at least one question")
    questions: list[dict[str, Any]] = []
    for index, value in enumerate(values, start=1):
        if isinstance(value, str):
            questions.append(
                {
                    "id": f"q{index:02d}",
                    "index": index,
                    "question": value,
                    "repeat": global_repeat,
                    "target": global_target,
                }
            )
        elif isinstance(value, dict):
            question = clean_text(value.get("question") or value.get("prompt"))
            if not question:
                raise ValueError(f"question object at index {index} is missing question")
            questions.append(
                {
                    "id": safe_id(value.get("id") or value.get("key"), f"q{index:02d}"),
                    "index": index,
                    "question": question,
                    "repeat": int(value.get("repeat") or global_repeat),
                    "target": clean_text(value.get("target") or global_target),
                }
            )
        else:
            raise ValueError(f"unsupported question item at index {index}")
    return questions


def make_plan(questions: list[dict[str, Any]]) -> list[dict[str, Any]]:
    plan: list[dict[str, Any]] = []
    for item in questions:
        repeat = int(item["repeat"])
        if repeat < 1 or repeat > 50:
            raise ValueError(f"repeat for {item['id']} must be between 1 and 50")
        for repeat_index in range(1, repeat + 1):
            plan.append(
                {
                    "sample_id": f"{item['id']}-r{repeat_index:02d}",
                    "question_id": item["id"],
                    "question_index": item["index"],
                    "repeat_index": repeat_index,
                    "repeat_total": repeat,
                    "question": item["question"],
                    "target": item.get("target", ""),
                }
            )
    return plan


def delay_strategy(args: argparse.Namespace) -> dict[str, Any]:
    if args.delay_min_seconds is not None and args.delay_max_seconds is not None:
        return {
            "mode": "random",
            "min_seconds": args.delay_min_seconds,
            "max_seconds": args.delay_max_seconds,
            "min_minutes": args.delay_min_seconds / MINUTE_SECONDS,
            "max_minutes": args.delay_max_seconds / MINUTE_SECONDS,
        }
    return {"mode": "fixed", "delay_seconds": args.delay_seconds, "delay_minutes": args.delay_seconds / MINUTE_SECONDS}


def next_delay_seconds(args: argparse.Namespace) -> float:
    if args.delay_min_seconds is None or args.delay_max_seconds is None:
        return args.delay_seconds
    return random.uniform(args.delay_min_seconds, args.delay_max_seconds)


def summarize(samples: list[dict[str, Any]], plan: list[dict[str, Any]]) -> dict[str, Any]:
    completed = sum(1 for sample in samples if sample.get("status") in {"done", "failed"})
    ok = sum(1 for sample in samples if sample.get("ok"))
    failed = sum(1 for sample in samples if sample.get("status") == "failed")
    reference_count = 0
    search_material_count = 0
    cited_search_material_count = 0
    search_material_citation_count = 0
    answer_chars = 0
    for sample in samples:
        result = sample.get("result") or {}
        reference_count += len(((result.get("references") or {}).get("items") or []))
        materials = result.get("mobile_search_materials") or {}
        search_material_count += len(materials.get("items") or [])
        cited_search_material_count += int(materials.get("cited_count") or 0)
        search_material_citation_count += int(materials.get("total_citation_count") or 0)
        answer_chars += len(((result.get("answer") or {}).get("text") or ""))
    return {
        "planned_samples": len(plan),
        "completed_samples": completed,
        "ok_samples": ok,
        "failed_samples": failed,
        "valid_sample_rate": ok / len(plan) if plan else 0,
        "reference_count": reference_count,
        "search_material_count": search_material_count,
        "cited_search_material_count": cited_search_material_count,
        "search_material_citation_count": search_material_citation_count,
        "answer_chars": answer_chars,
    }


def run_batch_sample(args: argparse.Namespace, run_dir: Path, sample: dict[str, Any]) -> dict[str, Any]:
    raw_path = run_dir / "raw" / f"{sample['sample_id']}.json"
    log_path = run_dir / "logs" / f"{sample['sample_id']}.log"
    relative_raw = os.path.relpath(raw_path, run_dir)
    relative_log = os.path.relpath(log_path, run_dir)
    if args.resume and raw_path.exists():
        existing = read_json(raw_path)
        if existing:
            ok, reason = reusable_raw(existing, sample)
            if ok:
                append_text(log_path, f"[resume reused] {utc_now()} {relative_raw}\n")
                return {
                    **sample,
                    "ok": True,
                    "status": "done",
                    "reused": True,
                    "started_at": existing.get("collected_at"),
                    "finished_at": existing.get("collected_at"),
                    "duration_ms": 0,
                    "raw_path": relative_raw,
                    "log_path": relative_log,
                    "error": "",
                    "result": existing,
                }
            append_text(log_path, f"[resume skipped] {utc_now()} {reason}; rerunning sample.\n")
    sample_args = argparse.Namespace(**vars(args))
    sample_args.prompt = sample["question"]
    sample_args.target = sample.get("target", "") or args.target_entity
    sample_args.artifact_dir = str(run_dir)
    started = time.monotonic()
    started_at = utc_now()
    append_text(log_path, f"[capture] {started_at} {sample['sample_id']} {sample['question']}\n")
    result = capture_once(sample_args, sample["sample_id"])
    write_json(raw_path, result)
    for event in result.get("action_trace", []):
        append_text(log_path, json.dumps(event, ensure_ascii=False) + "\n")
    finished_at = utc_now()
    duration_ms = round((time.monotonic() - started) * 1000)
    ok = bool(result.get("ok"))
    return {
        **sample,
        "ok": ok,
        "status": "done" if ok else "failed",
        "started_at": started_at,
        "finished_at": finished_at,
        "duration_ms": duration_ms,
        "raw_path": relative_raw,
        "log_path": relative_log,
        "error": "" if ok else clean_text(result.get("failure_reason")),
        "result": result,
    }


def add_common_mobile_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--device", default="", help="ADB/Appium device name, such as emulator-5554.")
    parser.add_argument("--server", default=DEFAULT_SERVER, help=f"Appium server URL. Default: {DEFAULT_SERVER}.")
    parser.add_argument("--app-package", default=DEFAULT_APP_PACKAGE, help=f"Doubao Android package. Default: {DEFAULT_APP_PACKAGE}.")
    parser.add_argument("--app-activity", default="", help="Optional app activity. When omitted, the script activates the package after session creation.")
    parser.add_argument("--adb-path", default="", help="Optional adb executable path.")
    parser.add_argument("--new-command-timeout", type=int, default=300, help="Appium new command timeout in seconds.")


def add_runtime_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--timeout", type=int, default=300, help="Answer wait timeout in seconds.")
    parser.add_argument("--poll-seconds", type=float, default=2.0, help="Polling interval while waiting for a stable answer.")
    parser.add_argument("--stable-seconds", type=float, default=8.0, help="Visible UI must remain stable for this many seconds.")
    parser.add_argument("--launch-wait-seconds", type=float, default=2.0, help="Wait after app activation before interacting.")
    parser.add_argument("--max-scrolls", type=int, default=6, help="Maximum post-answer scroll captures.")
    parser.add_argument("--scroll-direction", choices=["up", "down"], default="down", help="Appium scrollGesture direction for collecting multi-screen text.")
    parser.add_argument("--input-resource-id", default="", help="Optional exact Android resource-id for the prompt input.")
    parser.add_argument("--send-resource-id", default="", help="Optional exact Android resource-id for the send button.")
    parser.add_argument("--fresh-chat", action="store_true", help="Open a fresh Doubao chat before each prompt when the app exposes a new-chat control.")
    parser.add_argument("--require-fresh-chat", action="store_true", help="Fail the sample if --fresh-chat cannot open a new chat.")
    parser.add_argument("--new-chat-resource-id", default="", help="Optional exact Android resource-id for the new-chat button.")
    parser.add_argument("--fresh-chat-back-steps", type=int, default=3, help="Back presses allowed while looking for the new-chat button.")
    parser.add_argument("--fresh-chat-wait-seconds", type=float, default=1.2, help="Wait after tapping the new-chat button.")
    parser.add_argument("--target", default="", help="Optional target term for mention counting.")
    parser.add_argument("--recover-links", action="store_true", help="Opt in to tapping visible reference nodes to recover URLs from clipboard or UI text.")
    parser.add_argument("--skip-search-materials", action="store_true", help="Skip the expanded `搜索/参考资料` material-list extraction.")
    parser.add_argument("--material-max-scrolls", type=int, default=8, help="Maximum scroll attempts while collecting expanded search materials.")
    parser.add_argument("--material-detail-wait-seconds", type=float, default=2.0, help="Wait after tapping a search material detail.")
    parser.add_argument("--recover-material-links", action="store_true", help="Tap expanded search material rows to recover detail URLs. `--recover-links` also enables this.")


def add_capture_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--prompt", required=True, default="", help="Prompt/question to send to Doubao.")
    parser.add_argument("--out", default="", help="Optional raw JSON output file.")
    parser.add_argument("--artifact-dir", default="", help="Directory for screenshots and XML. Defaults to the output file parent or current directory.")
    add_runtime_args(parser)


def validate_mobile_args(args: argparse.Namespace) -> None:
    if args.timeout < 30 or args.timeout > 7200:
        raise ValueError("--timeout must be between 30 and 7200 seconds")
    if args.poll_seconds <= 0:
        raise ValueError("--poll-seconds must be positive")
    if args.stable_seconds <= 0:
        raise ValueError("--stable-seconds must be positive")
    if args.max_scrolls < 0 or args.max_scrolls > 50:
        raise ValueError("--max-scrolls must be between 0 and 50")
    if args.material_max_scrolls < 0 or args.material_max_scrolls > 50:
        raise ValueError("--material-max-scrolls must be between 0 and 50")
    if args.material_detail_wait_seconds < 0:
        raise ValueError("--material-detail-wait-seconds must be non-negative")
    if args.fresh_chat_back_steps < 0 or args.fresh_chat_back_steps > 10:
        raise ValueError("--fresh-chat-back-steps must be between 0 and 10")
    if args.fresh_chat_wait_seconds < 0:
        raise ValueError("--fresh-chat-wait-seconds must be non-negative")
    if args.require_fresh_chat and not args.fresh_chat:
        raise ValueError("--require-fresh-chat requires --fresh-chat")


def command_preflight(args: argparse.Namespace) -> int:
    checks: list[dict[str, Any]] = []

    def add(key: str, label: str, status: str, detail: Any = "", fix: str = "") -> None:
        checks.append({"key": key, "label": label, "status": status, "detail": detail, "fix": fix})

    adb_path = args.adb_path or shutil.which("adb")
    add("adb", "ADB executable", "pass" if adb_path else "fail", adb_path or "adb not found", "Install Android SDK Platform-Tools and put adb on PATH, or pass --adb-path.")
    if adb_path:
        devices = run_command([adb_path, "devices"], timeout=args.timeout)
        add("adb_devices", "ADB devices", "pass" if devices["ok"] else "fail", devices["stdout"] or devices["stderr"], "Start an AVD or connect a USB-debuggable Android device.")
        if args.device:
            found = bool(re.search(rf"^{re.escape(args.device)}\s+device\b", devices.get("stdout", ""), re.M))
            add("target_device", "Target device", "pass" if found else "fail", args.device, "Verify `adb devices` and pass the connected device name.")
        package = run_command([adb_path, "-s", args.device, "shell", "pm", "path", args.app_package], timeout=args.timeout) if args.device else {"ok": False, "stdout": "skipped without --device", "stderr": ""}
        add("app_package", "Doubao package", "pass" if package["ok"] else "warn", package["stdout"] or package["stderr"], "Install the Doubao APK on the selected device, or pass --app-package.")

    status = appium_status(args.server, timeout=min(args.timeout, 10))
    add("appium_server", "Appium server", "pass" if status["ok"] else "fail", status.get("response") or status.get("error"), "Start Appium with `appium` and install the uiautomator2 driver.")

    try:
        import_appium()
        add("appium_python_client", "Appium Python client", "pass", "import ok")
    except RuntimeError as error:
        add("appium_python_client", "Appium Python client", "fail", str(error), "Run `python3 -m pip install -r requirements-mobile.txt`.")

    session_checks = {"screenshot": "skip", "page_source": "skip", "clipboard": "skip"}
    if status["ok"]:
        driver = None
        trace: list[dict[str, Any]] = []
        try:
            driver = create_driver(args, trace)
            source = driver.page_source
            session_checks["page_source"] = "pass" if clean_text(source) else "fail"
            try:
                driver.get_screenshot_as_png()
                session_checks["screenshot"] = "pass"
            except Exception:
                session_checks["screenshot"] = "fail"
            try:
                driver.set_clipboard_text("doubao-mobile-preflight")
                session_checks["clipboard"] = "pass"
            except Exception:
                session_checks["clipboard"] = "warn"
        except Exception as error:
            add("uiautomator2_session", "UiAutomator2 session", "fail", str(error), "Check Appium driver install, server URL, device name, and app package.")
        else:
            add("uiautomator2_session", "UiAutomator2 session", "pass", "session created")
        finally:
            if driver is not None:
                try:
                    driver.quit()
                except Exception:
                    pass
    for key, status_value in session_checks.items():
        add(key, key.replace("_", " ").title(), status_value, "")

    ok = all(item["status"] in {"pass", "skip", "warn"} for item in checks)
    output = {"ok": ok, "checks": checks}
    print(json.dumps(output, ensure_ascii=False, indent=2))
    return 0 if ok else 1


def command_capture(args: argparse.Namespace) -> int:
    validate_mobile_args(args)
    if not args.artifact_dir and args.out:
        args.artifact_dir = str(Path(args.out).resolve().parent)
    record = capture_once(args, "capture")
    if args.out:
        write_json(Path(args.out).resolve(), record)
    print(json.dumps(record, ensure_ascii=False, indent=2))
    return 0 if record.get("ok") else 1


def command_batch(args: argparse.Namespace) -> int:
    validate_mobile_args(args)
    if args.entity_type:
        args.entity_type = normalize_entity_type(args.entity_type)
        if args.entity_type not in {"person", "company", "product"}:
            raise ValueError("--entity-type must be person/company/product or 人/公司/产品")
    if args.target_entity and not args.entity_type:
        raise ValueError("--target-entity requires --entity-type")
    if args.repeat < 1 or args.repeat > 50:
        raise ValueError("--repeat must be between 1 and 50")
    if args.delay_min_seconds is not None or args.delay_max_seconds is not None:
        if args.delay_min_seconds is None or args.delay_max_seconds is None:
            raise ValueError("Random delay requires both minimum and maximum bounds.")
        if args.delay_min_seconds < 0 or args.delay_max_seconds < 0 or args.delay_min_seconds > args.delay_max_seconds:
            raise ValueError("Invalid random delay bounds.")
        if args.delay_max_seconds > MAX_DELAY_SECONDS:
            raise ValueError("Random delay maximum must be 24 hours or less.")

    questions = read_questions(Path(args.questions).resolve(), args.repeat, args.target_entity)
    plan = make_plan(questions)
    out_dir = Path(args.out_dir or Path("runs") / f"mobile-doubao-{timestamp_id()}").resolve()
    run_id = safe_id(out_dir.name, f"mobile-doubao-{timestamp_id()}")
    run = {
        "id": run_id,
        "started_at": utc_now(),
        "finished_at": None,
        "engine": "doubao",
        "transport": "appium-uiautomator2-avd",
        "dir": str(out_dir),
        "dry_run": args.dry_run,
    }
    dataset = {
        "schema_version": "yao-doubao-crawler/v1",
        "run": run,
        "input": {
            "question_count": len(questions),
            "global_repeat": args.repeat,
            "timeout": args.timeout,
            "reference_extraction": True,
            "target_entity": args.target_entity or None,
            "target_aliases": split_aliases(args.target_aliases),
            "entity_type": args.entity_type or None,
            "delay_strategy": delay_strategy(args),
            "mobile": {"device": args.device or None, "app_package": args.app_package, "app_activity": args.app_activity or None, "server": args.server},
            "questions": questions,
        },
        "plan": plan,
        "samples": [],
        "totals": summarize([], plan),
    }
    out_dir.mkdir(parents=True, exist_ok=True)
    write_json(out_dir / "doubao-crawl.json", dataset)
    if args.dry_run:
        dataset["run"]["finished_at"] = utc_now()
        write_json(out_dir / "doubao-crawl.json", dataset)
        print(json.dumps({"ok": True, "dry_run": True, "out_dir": str(out_dir), "samples": len(plan)}, ensure_ascii=False, indent=2))
        return 0

    for index, sample in enumerate(plan, start=1):
        print(f"[{index}/{len(plan)}] {sample['sample_id']}", file=sys.stderr)
        record = run_batch_sample(args, out_dir, sample)
        dataset["samples"].append(record)
        dataset["totals"] = summarize(dataset["samples"], plan)
        write_json(out_dir / "doubao-crawl.json", dataset)
        if index < len(plan) and not record.get("reused"):
            delay = next_delay_seconds(args)
            if delay > 0:
                append_text(out_dir / "batch.log", f"{utc_now()} [delay] waiting {round(delay, 2)} seconds\n")
                time.sleep(delay)
    dataset["run"]["finished_at"] = utc_now()
    dataset["totals"] = summarize(dataset["samples"], plan)
    write_json(out_dir / "doubao-crawl.json", dataset)
    print(json.dumps({"ok": True, "out_dir": str(out_dir), "dataset": str(out_dir / "doubao-crawl.json"), "totals": dataset["totals"]}, ensure_ascii=False, indent=2))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Capture Doubao Android UI evidence through Appium UiAutomator2.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    preflight = subparsers.add_parser("preflight", help="Check Android/Appium/Doubao mobile prerequisites.")
    add_common_mobile_args(preflight)
    preflight.add_argument("--timeout", type=int, default=30, help="Preflight command timeout in seconds.")
    preflight.set_defaults(func=command_preflight)

    capture = subparsers.add_parser("capture", help="Capture one Doubao Android answer.")
    add_common_mobile_args(capture)
    add_capture_args(capture)
    capture.set_defaults(func=command_capture)

    batch = subparsers.add_parser("batch", help="Run low-frequency repeated mobile captures.")
    add_common_mobile_args(batch)
    add_runtime_args(batch)
    batch.add_argument("--questions", required=True, help="Text file, JSON array of strings, or JSON array of objects.")
    batch.add_argument("--repeat", type=int, default=1, help="Global repeat count per question. Default: 1.")
    batch.add_argument("--target-entity", default="", help="Primary entity to diagnose.")
    batch.add_argument("--target-aliases", default="", help="Aliases separated by comma, pipe, semicolon, or newline.")
    batch.add_argument("--entity-type", default="", help="person/company/product or 人/公司/产品.")
    batch.add_argument("--out-dir", default="", help="Run output directory. Default: runs/mobile-doubao-<timestamp>.")
    batch.add_argument("--resume", action="store_true", help="Reuse valid raw JSON files.")
    batch.add_argument("--dry-run", action="store_true", help="Write the plan without connecting to Appium.")
    batch.add_argument("--delay-seconds", type=float, default=1.5, help="Fixed delay between samples.")
    batch.add_argument("--delay-min-seconds", type=float, default=None, help="Random delay lower bound in seconds.")
    batch.add_argument("--delay-max-seconds", type=float, default=None, help="Random delay upper bound in seconds.")
    batch.add_argument("--delay-min-minutes", type=float, default=None, help="Random delay lower bound in minutes.")
    batch.add_argument("--delay-max-minutes", type=float, default=None, help="Random delay upper bound in minutes.")
    batch.set_defaults(func=command_batch)

    return parser


def normalize_delay_args(args: argparse.Namespace) -> None:
    if hasattr(args, "delay_min_minutes") and args.delay_min_minutes is not None:
        args.delay_min_seconds = args.delay_min_minutes * MINUTE_SECONDS
    if hasattr(args, "delay_max_minutes") and args.delay_max_minutes is not None:
        args.delay_max_seconds = args.delay_max_minutes * MINUTE_SECONDS


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    normalize_delay_args(args)
    try:
        return int(args.func(args))
    except Exception as error:
        print(error, file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
