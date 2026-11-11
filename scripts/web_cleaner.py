#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
web_cleaner.py — AI Clean Master 网站 / 前端页面 (HTML / React / Vue / SVG) 扫描与去 AI 味清理器

支持：
1. --scan: 扫描 HTML/JSX/TSX/Vue/SVG 中的：
   - 发光小胶囊/伪英文状态徽章 (rounded-full / badge / uppercase tracking-wider + SECTION/AI-POWERED/SYSTEM ONLINE)
   - Bento 卡片内的 text-xs / 10px~12px 凑数解释小字
   - 页脚/底栏假大空 Slogan 与免责废话
   - ✨🚀💡⚡ 表情符号噪音与 AI 黑话
2. --apply: 根据 JSON 计划执行连盒移除 DOM/标签节点、清理 Emoji、替换人味文案，并对保留的核心标题做字号 class 提权 (如 text-base -> text-lg font-semibold)。
"""

import argparse
import json
import re
import sys
from pathlib import Path

AI_BUZZWORDS = [
    "赋能", "抓手", "闭环", "全链路", "多维度", "全方位", "深层次",
    "底层逻辑", "顶层设计", "范式转移", "生态体系", "协同共振", "组合拳",
    "颗粒度", "痛点剖析", "破局之道", "矩阵", "价值跃迁", "新生态",
    "delve", "testament", "tapestry", "paradigm shift", "synergy", "holistic",
    "empowering", "game-changer", "cutting-edge", "seamless", "leverage"
]

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
    r"<(?P<tag>p|span|div|small)\b(?P<attrs>[^>]*(?:text-xs|text-\[1[012]px\]|font-size:\s*1[012]px)[^>]*)>(?P<inner>[^<]{4,200})</(?P=tag)>",
    re.I,
)

FOOTER_SLOP_RE = re.compile(
    r"<(?P<tag>div|p|footer|span)\b(?P<attrs>[^>]*)>(?P<inner>[^<]*(?:本页核心洞察|仅供演示参考|具体以实际为准|构建全链路数字生态|Empowering the future)[^<]*)</(?P=tag)>",
    re.I,
)


def scan_web_file(file_path: str) -> dict:
    content = Path(file_path).read_text(encoding="utf-8")
    findings = []

    for m in BADGE_ELEMENT_RE.finditer(content):
        attrs = m.group("attrs")
        inner = m.group("inner").strip()
        if ("rounded-full" in attrs or "badge" in attrs.lower() or "tracking-" in attrs or "uppercase" in attrs) and (
            BADGE_TEXT_RE.search(inner) or EMOJI_SLOP_RE.search(inner)
        ):
            findings.append({
                "type": "kicker_pill_badge",
                "matched_html": m.group(0),
                "text": inner,
                "recommendation": "delete_node_with_box",
            })

    for m in SMALL_SUBTEXT_RE.finditer(content):
        inner = m.group("inner").strip()
        if any(w in inner for w in ["通过", "实现", "赋能", "闭环", "全链路", "多维", "助力", "仅供参考", "+99"]):
            findings.append({
                "type": "redundant_micro_text",
                "matched_html": m.group(0),
                "text": inner,
                "recommendation": "delete_and_promote_sibling_heading",
            })

    for m in FOOTER_SLOP_RE.finditer(content):
        findings.append({
            "type": "footer_slop",
            "matched_html": m.group(0),
            "text": m.group("inner").strip(),
            "recommendation": "delete_node_with_box",
        })

    buzzwords_found = [w for w in AI_BUZZWORDS if w in content]
    emojis_found = list(set(EMOJI_SLOP_RE.findall(content)))

    return {
        "file": str(Path(file_path).resolve()),
        "findings_count": len(findings),
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
    }

    # 1. 连盒移除指定的完整 HTML/JSX 节点或自动清理扫描出的胶囊框与底栏废话
    if plan.get("auto_remove_detected_badges", True):
        for item in scan_web_file(file_path)["findings"]:
            target_html = item["matched_html"]
            if target_html in content:
                content = content.replace(target_html, "")
                stats["removed_blocks"] += 1

    for block in plan.get("remove_exact", []):
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
