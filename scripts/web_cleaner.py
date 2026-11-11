#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
web_cleaner.py — AI Clean Master 网站 / 前端页面 (HTML / React / Vue / SVG) 扫描与去 AI 味清理器

支持：
1. --scan: 扫描 HTML/JSX/TSX/Vue/SVG 中的：
   - 发光小胶囊/伪英文状态徽章 (rounded-full / badge / uppercase tracking-wider + SECTION/AI-POWERED/SYSTEM ONLINE)
   - Bento 卡片内的 text-xs / 10px~12px 凑数解释小字 (严格保护受认证的合规/真实数据角标)
   - 页脚/底栏假大空 Slogan 与免责废话
   - ✨🚀💡⚡ 表情符号噪音与 AI 黑话
   - 10 大行业与双语自动识别及合规角标保护 (protected_footnotes)
2. --apply: 根据 JSON 计划执行连盒移除 DOM/标签节点、清理 Emoji、替换人味文案，并对保留的核心标题做字号 class 提权。
"""

import argparse
import json
import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Robust 3-tier import fallback for industry_classifier
# ---------------------------------------------------------------------------
try:
    from scripts.industry_classifier import (
        is_protected_domain_footnote,
        detect_buzzwords_bilingual,
        detect_industry_and_language,
        is_redundant_subtext_bilingual,
    )
except (ImportError, ModuleNotFoundError):
    try:
        from industry_classifier import (
            is_protected_domain_footnote,
            detect_buzzwords_bilingual,
            detect_industry_and_language,
            is_redundant_subtext_bilingual,
        )
    except (ImportError, ModuleNotFoundError):
        _script_dir = Path(__file__).resolve().parent
        if str(_script_dir) not in sys.path:
            sys.path.insert(0, str(_script_dir))
        _parent_dir = _script_dir.parent
        if str(_parent_dir) not in sys.path:
            sys.path.insert(0, str(_parent_dir))
        from industry_classifier import (
            is_protected_domain_footnote,
            detect_buzzwords_bilingual,
            detect_industry_and_language,
            is_redundant_subtext_bilingual,
        )

EMOJI_SLOP_RE = re.compile(r"[✨🚀💡⚡🔥🎯🌐💎]+\s*")

# 匹配典型的单行 HTML/JSX 胶囊徽章或微标签节点
BADGE_ELEMENT_RE = re.compile(
    r"<(?P<tag>span|div|p|small)\b(?P<attrs>[^>]*)>(?P<inner>[^<]{1,90})</(?P=tag)>",
    re.I,
)

BADGE_TEXT_RE = re.compile(
    r"(SECTION\s*0?\d+|PART\s*0?\d+|CORE INSIGHT|STRATEGIC|AI-POWERED|NEXT-GEN|SYSTEM\s+ONLINE|0\d\s*//|核心赋能|战略顶层|多维感知|全链路)",
    re.I,
)

SMALL_SUBTEXT_RE = re.compile(
    r"<(?P<tag>p|span|div|small)\b(?P<attrs>[^>]*(?:text-xs|text-\[1[012]px\]|font-size:\s*1[012]px)[^>]*)>(?P<inner>(?:(?!</(?P=tag)>).){4,300})</(?P=tag)>",
    re.I | re.DOTALL,
)

FOOTER_SLOP_RE = re.compile(
    r"<(?P<tag>div|p|footer|span)\b(?P<attrs>[^>]*)>(?P<inner>[^<]*(?:本页核心洞察|仅供演示参考|具体以实际为准|构建全链路数字生态|Empowering the future)[^<]*)</(?P=tag)>",
    re.I,
)


def scan_web_file(file_path: str) -> dict:
    content = Path(file_path).read_text(encoding="utf-8")
    findings = []
    protected_footnotes = []

    # 1. 行业与双语自动识别
    ind_info = detect_industry_and_language(content)

    # 2. 扫描徽章/胶囊
    for m in BADGE_ELEMENT_RE.finditer(content):
        attrs = m.group("attrs")
        inner = m.group("inner").strip()
        is_badge_style = ("rounded-full" in attrs or "badge" in attrs.lower() or "tracking-" in attrs or "uppercase" in attrs)
        if is_badge_style:
            if is_protected_domain_footnote(inner):
                protected_footnotes.append({
                    "type": "kicker_badge",
                    "matched_html": m.group(0),
                    "text": inner,
                    "reason": "protected_compliance_or_standard",
                })
                continue

            if BADGE_TEXT_RE.search(inner) or EMOJI_SLOP_RE.search(inner):
                findings.append({
                    "type": "kicker_pill_badge",
                    "matched_html": m.group(0),
                    "text": inner,
                    "recommendation": "delete_node_with_box",
                })

    # 3. 扫描凑数小字并做真合规/真角标保护
    for m in SMALL_SUBTEXT_RE.finditer(content):
        inner = m.group("inner").strip()
        if is_protected_domain_footnote(inner):
            if not any(pf["matched_html"] == m.group(0) for pf in protected_footnotes):
                protected_footnotes.append({
                    "type": "redundant_micro_text",
                    "matched_html": m.group(0),
                    "text": inner,
                    "reason": "protected_domain_footnote",
                })
            continue

        if any(w in inner for w in ["通过", "实现", "赋能", "闭环", "全链路", "多维", "助力", "仅供参考", "+99"]) or is_redundant_subtext_bilingual(inner):
            findings.append({
                "type": "redundant_micro_text",
                "matched_html": m.group(0),
                "text": inner,
                "recommendation": "delete_and_promote_sibling_heading",
            })

    # 4. 扫描页脚废话并保护真实披露声明
    for m in FOOTER_SLOP_RE.finditer(content):
        inner = m.group("inner").strip()
        if is_protected_domain_footnote(inner):
            if not any(pf["matched_html"] == m.group(0) for pf in protected_footnotes):
                protected_footnotes.append({
                    "type": "footer_slop",
                    "matched_html": m.group(0),
                    "text": inner,
                    "reason": "protected_domain_footnote",
                })
            continue

        findings.append({
            "type": "footer_slop",
            "matched_html": m.group(0),
            "text": inner,
            "recommendation": "delete_node_with_box",
        })

    # 5. 全文双语黑话与 Emoji 噪音检测
    buzzwords_found = detect_buzzwords_bilingual(content)
    emojis_found = list(set(EMOJI_SLOP_RE.findall(content)))

    return {
        "file": str(Path(file_path).resolve()),
        "language": ind_info.get("language", "zh"),
        "industry_id": ind_info.get("industry_id", "tech_saas_ai"),
        "industry_name_zh": ind_info.get("industry_name_zh", ""),
        "industry_name_en": ind_info.get("industry_name_en", ""),
        "confidence": ind_info.get("confidence", "default"),
        "findings_count": len(findings),
        "protected_footnotes_count": len(protected_footnotes),
        "protected_footnotes": protected_footnotes,
        "buzzwords": buzzwords_found,
        "emoji_slop": [e.strip() for e in emojis_found if e.strip()],
        "findings": findings,
    }


def apply_web_plan(file_path: str, plan: dict, output_path: str) -> dict:
    content = Path(file_path).read_text(encoding="utf-8")
    stats = {
        "removed_blocks": 0,
        "rewritten_snippets": 0,
        "promoted_classes": 0,
        "stripped_emojis": 0,
        "protected_footnotes_preserved": 0,
    }

    # 1. 连盒移除指定的完整 HTML/JSX 节点或自动清理扫描出的胶囊框与底栏废话
    if plan.get("auto_remove_detected_badges", True):
        for item in scan_web_file(file_path)["findings"]:
            target_html = item["matched_html"]
            # 严格防止误删已认定的保护角标
            if is_protected_domain_footnote(item.get("text", "")):
                stats["protected_footnotes_preserved"] += 1
                continue
            if target_html in content:
                content = content.replace(target_html, "")
                stats["removed_blocks"] += 1

    for block in plan.get("remove_exact", []):
        if is_protected_domain_footnote(block) and not plan.get("force_remove_protected", False):
            stats["protected_footnotes_preserved"] += 1
            continue
        if block in content:
            content = content.replace(block, "")
            stats["removed_blocks"] += 1

    # 2. 执行人味化文案与标签替换
    for rw in plan.get("rewrites", []):
        old_val = rw["old"]
        new_val = rw["new"]
        if old_val in content:
            content = content.replace(old_val, new_val)
            stats["rewritten_snippets"] += 1

    # 3. 执行样式提权替换 (如卡片主标题从 text-base 提权为 text-lg font-semibold)
    for promo in plan.get("class_promotions", []):
        old_cls = promo["old"]
        new_cls = promo["new"]
        if old_cls in content:
            content = content.replace(old_cls, new_cls)
            stats["promoted_classes"] += 1

    # 4. 剥离 AI 强迫症 Emoji 噪音
    if plan.get("strip_emoji_slop", True):
        matches = EMOJI_SLOP_RE.findall(content)
        if matches:
            stats["stripped_emojis"] = len(matches)
            content = EMOJI_SLOP_RE.sub("", content)

    # 清理多余空行
    content = re.sub(r"\n{3,}", "\n\n", content)

    out_p = Path(output_path)
    out_p.parent.mkdir(parents=True, exist_ok=True)
    out_p.write_text(content, encoding="utf-8")
    stats["output_file"] = str(out_p.resolve())
    return stats


def main():
    parser = argparse.ArgumentParser(description="Scan and clean AI-slop badges, micro-text, and buzzwords in HTML/React/Vue/SVG files.")
    parser.add_argument("--scan", dest="scan_file", help="Scan target web/frontend file")
    parser.add_argument("--json", dest="json_out", help="Write scan result to JSON file")
    parser.add_argument("--apply", dest="plan_json", help="Apply cleanup plan JSON")
    parser.add_argument("input_file", nargs="?", help="Input file when using --apply")
    parser.add_argument("-o", "--output", help="Output file path")
    args = parser.parse_args()

    if args.scan_file:
        rep = scan_web_file(args.scan_file)
        if args.json_out:
            Path(args.json_out).write_text(json.dumps(rep, ensure_ascii=False, indent=2), encoding="utf-8")
        sys.stdout.buffer.write(json.dumps(rep, ensure_ascii=False, indent=2).encode("utf-8"))
        sys.stdout.buffer.write(b"\n")
        return

    if args.plan_json and args.input_file:
        in_p = Path(args.input_file)
        out_p = args.output or str(in_p.with_name(f"{in_p.stem}_cleaned{in_p.suffix}"))
        plan = json.loads(Path(args.plan_json).read_text(encoding="utf-8"))
        stats = apply_web_plan(str(in_p), plan, out_p)
        sys.stdout.buffer.write(json.dumps(stats, ensure_ascii=False, indent=2).encode("utf-8"))
        sys.stdout.buffer.write(b"\n")
        return

    parser.print_help()


if __name__ == "__main__":
    main()
