#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pptx_cleaner.py — AI Clean Master PPTX 连盒带字清理、人味化改写与智能视觉提权执行器

支持操作：
1. delete_shape_ids: 连盒带字删除指定文本框及其配对的背景胶囊框/底栏条
2. delete_paragraphs: 删除卡片文本框内同义反复的凑数小字段落
3. rewrites: 保样式替换核心文案，并支持字号提权 (promote_pt / target_pt) 与垂直居中 (vertical_center)
"""

import argparse
import json
import sys
from pathlib import Path
from pptx import Presentation
from pptx.enum.text import MSO_ANCHOR
from pptx.util import Pt


def iter_shapes_recursive(shapes):
    for sp in list(shapes):
        yield sp
        if sp.shape_type == 6 and hasattr(sp, "shapes"):
            yield from iter_shapes_recursive(sp.shapes)


def remove_shape_xml(shape):
    """从幻灯片 XML 树中安全移除形状节点"""
    el = shape._element
    parent = el.getparent()
    if parent is not None:
        parent.remove(el)
        return True
    return False


def remove_paragraph_xml(paragraph):
    """从 TextFrame 中移除指定段落 XML 节点"""
    p_el = paragraph._p
    parent = p_el.getparent()
    if parent is not None:
        parent.remove(p_el)
        return True
    return False


def replace_paragraph_text_preserve_style(paragraph, new_text: str, promote_pt: float = 0.0, target_pt: float = None):
    """替换段落文本并保留第一个非空 Run 的字体、颜色与加粗样式，同时按需提权字号"""
    runs = list(paragraph.runs)
    base_pt = None
    if paragraph.font and paragraph.font.size:
        base_pt = paragraph.font.size.pt
    for r in runs:
        if r.font and r.font.size and base_pt is None:
            base_pt = r.font.size.pt

    if runs:
        runs[0].text = new_text
        for extra_run in runs[1:]:
            extra_run.text = ""
        target_run = runs[0]
    else:
        target_run = paragraph.add_run()
        target_run.text = new_text

    final_pt = None
    if target_pt is not None:
        final_pt = float(target_pt)
    elif promote_pt:
        final_pt = (base_pt or 16.0) + float(promote_pt)

    if final_pt is not None:
        target_run.font.size = Pt(final_pt)
        if paragraph.font:
            paragraph.font.size = Pt(final_pt)


def apply_pptx_plan(input_pptx: str, plan: dict, output_pptx: str) -> dict:
    prs = Presentation(input_pptx)
    stats = {
        "deleted_shapes": 0,
        "deleted_paragraphs": 0,
        "rewritten_paragraphs": 0,
        "promoted_paragraphs": 0,
    }

    slide_plans = {sp["slide_index"]: sp for sp in plan.get("slides", [])}

    for idx, slide in enumerate(prs.slides, start=1):
        s_plan = slide_plans.get(idx)
        if not s_plan:
            continue

        shape_map = {sp.shape_id: sp for sp in iter_shapes_recursive(slide.shapes)}

        # 1. 执行段内凑数小字删除 (从后往前删，避免索引偏移)
        for dp in s_plan.get("delete_paragraphs", []):
            sp = shape_map.get(dp["shape_id"])
            if sp is None or not getattr(sp, "has_text_frame", False):
                continue
            paras = list(sp.text_frame.paragraphs)
            for p_idx in sorted(dp.get("paragraph_indices", []), reverse=True):
                if 0 <= p_idx < len(paras) and len(sp.text_frame.paragraphs) > 1:
                    if remove_paragraph_xml(paras[p_idx]):
                        stats["deleted_paragraphs"] += 1

        # 2. 执行人味化文案改写与字号视觉提权
        for rw in s_plan.get("rewrites", []):
            sp = shape_map.get(rw["shape_id"])
            if sp is None or not getattr(sp, "has_text_frame", False):
                continue
            paras = list(sp.text_frame.paragraphs)
            p_idx = rw.get("paragraph_index", 0)
            if 0 <= p_idx < len(paras):
                promote_pt = rw.get("promote_pt", 0.0)
                target_pt = rw.get("target_pt", None)
                replace_paragraph_text_preserve_style(
                    paras[p_idx],
                    rw["new_text"],
                    promote_pt=promote_pt,
                    target_pt=target_pt,
                )
                stats["rewritten_paragraphs"] += 1
                if promote_pt or target_pt:
                    stats["promoted_paragraphs"] += 1
            if rw.get("vertical_center"):
                sp.text_frame.vertical_anchor = MSO_ANCHOR.MIDDLE

        # 3. 执行连盒带字删除 (小字文本框 + 配对胶囊框/底栏条)
        for del_id in s_plan.get("delete_shape_ids", []):
            sp = shape_map.get(del_id)
            if sp is not None and remove_shape_xml(sp):
                stats["deleted_shapes"] += 1

    out_path = Path(output_pptx)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    prs.save(str(out_path))
    stats["output_file"] = str(out_path.resolve())
    return stats


def main():
    parser = argparse.ArgumentParser(description="Clean AI-slop small text, remove paired pill/footer shapes, and promote core text in a PPTX file.")
    parser.add_argument("input_pptx", help="Input .pptx file path")
    parser.add_argument("plan_json", help="Path to JSON cleanup plan")
    parser.add_argument("-o", "--output", help="Output .pptx file path (defaults to <input>_cleaned.pptx)")
    args = parser.parse_args()

    in_path = Path(args.input_pptx)
    out_path = args.output or str(in_path.with_name(f"{in_path.stem}_cleaned{in_path.suffix}"))
    plan = json.loads(Path(args.plan_json).read_text(encoding="utf-8"))

    stats = apply_pptx_plan(str(in_path), plan, out_path)
    sys.stdout.buffer.write(json.dumps(stats, ensure_ascii=False, indent=2).encode("utf-8"))
    sys.stdout.buffer.write(b"\n")


if __name__ == "__main__":
    main()
