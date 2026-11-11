#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
doc_cleaner.py — AI Clean Master 文档载体 (.docx / .md) 扫描与去 AI 味清理器

支持：
1. --scan: 扫描 Word (.docx) 或 Markdown (.md) 中的 AI 伪标签小字、空洞导语/结语、AI 黑话与 Emoji 噪音。
2. --apply: 删除指定的冗余段落，执行人味化文本改写并保留原文档标题样式与表格结构。
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


def scan_doc(file_path: str) -> dict:
    p = Path(file_path)
    ext = p.suffix.lower()
    items = []

    if ext == ".docx":
        from docx import Document
        doc = Document(str(p))
        for i, para in enumerate(doc.paragraphs):
            txt = para.text.strip()
            if not txt:
                continue
            b_words = [w for w in AI_BUZZWORDS if w in txt]
            has_emoji = bool(EMOJI_SLOP_RE.search(txt))
            if b_words or has_emoji or txt.startswith(("SECTION", "CORE INSIGHT", "本页核心洞察", "注：以上")):
                items.append({
                    "paragraph_index": i,
                    "style": para.style.name if para.style else "Normal",
                    "text": txt,
                    "buzzwords": b_words,
                    "has_emoji_slop": has_emoji,
                })
    else:
        lines = p.read_text(encoding="utf-8").splitlines()
        for i, line in enumerate(lines):
            txt = line.strip()
            if not txt:
                continue
            b_words = [w for w in AI_BUZZWORDS if w in txt]
            has_emoji = bool(EMOJI_SLOP_RE.search(txt))
            if b_words or has_emoji or re.search(r"(SECTION\s*0?\d+|CORE INSIGHT|仅供演示参考)", txt, re.I):
                items.append({
                    "line_index": i,
                    "text": txt,
                    "buzzwords": b_words,
                    "has_emoji_slop": has_emoji,
                })

    return {
        "file": str(p.resolve()),
        "format": ext,
        "flagged_count": len(items),
        "items": items,
    }


def apply_doc_plan(file_path: str, plan: dict, output_path: str) -> dict:
    p = Path(file_path)
    ext = p.suffix.lower()
    out_p = Path(output_path)
    out_p.parent.mkdir(parents=True, exist_ok=True)

    stats = {"deleted_items": 0, "rewritten_items": 0}

    if ext == ".docx":
        from docx import Document
        doc = Document(str(p))
        rw_map = {r["paragraph_index"]: r["new_text"] for r in plan.get("rewrites", [])}
        del_set = set(plan.get("delete_paragraph_indices", []))

        for idx, para in enumerate(doc.paragraphs):
            if idx in rw_map:
                if para.runs:
                    para.runs[0].text = rw_map[idx]
                    for r in para.runs[1:]:
                        r.text = ""
                else:
                    para.text = rw_map[idx]
                stats["rewritten_items"] += 1

        for idx in sorted(del_set, reverse=True):
            if 0 <= idx < len(doc.paragraphs):
                el = doc.paragraphs[idx]._element
                if el.getparent() is not None:
                    el.getparent().remove(el)
                    stats["deleted_items"] += 1

        doc.save(str(out_p))
    else:
        content = p.read_text(encoding="utf-8")
        for block in plan.get("remove_exact", []):
            if block in content:
                content = content.replace(block, "")
                stats["deleted_items"] += 1
        for rw in plan.get("rewrites", []):
            old_t = rw.get("old", "")
            new_t = rw.get("new", "")
            if old_t and old_t in content:
                content = content.replace(old_t, new_t)
                stats["rewritten_items"] += 1
        if plan.get("strip_emoji_slop", True):
            content = EMOJI_SLOP_RE.sub("", content)
        out_p.write_text(content, encoding="utf-8")

    stats["output_file"] = str(out_p.resolve())
    return stats


def main():
    parser = argparse.ArgumentParser(description="Scan and clean AI-slop in Word (.docx) and Markdown (.md) documents.")
    parser.add_argument("--scan", dest="scan_file", help="Path to .docx or .md to scan")
    parser.add_argument("--json", dest="json_out", help="Optional JSON output path")
    parser.add_argument("--apply", dest="plan_json", help="Path to JSON cleanup plan")
    parser.add_argument("input_file", nargs="?", help="Input document path when using --apply")
    parser.add_argument("-o", "--output", help="Output document path")
    args = parser.parse_args()

    if args.scan_file:
        rep = scan_doc(args.scan_file)
        if args.json_out:
            Path(args.json_out).write_text(json.dumps(rep, ensure_ascii=False, indent=2), encoding="utf-8")
        sys.stdout.buffer.write(json.dumps(rep, ensure_ascii=False, indent=2).encode("utf-8"))
        sys.stdout.buffer.write(b"\n")
        return

    if args.plan_json and args.input_file:
        in_p = Path(args.input_file)
        out_p = args.output or str(in_p.with_name(f"{in_p.stem}_cleaned{in_p.suffix}"))
        plan = json.loads(Path(args.plan_json).read_text(encoding="utf-8"))
        stats = apply_doc_plan(str(in_p), plan, out_p)
        sys.stdout.buffer.write(json.dumps(stats, ensure_ascii=False, indent=2).encode("utf-8"))
        sys.stdout.buffer.write(b"\n")
        return

    parser.print_help()


if __name__ == "__main__":
    main()
