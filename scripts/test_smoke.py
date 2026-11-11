#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_smoke.py — AI Clean Master 四大载体全链路自动化冒烟测试
测试范围：
1. PPTX (.pptx): 扫描配对胶囊背景框/底栏 + 连盒带字删除 + 段内凑数小字清理 + 核心文字人味改写与字号提权
2. Web (.html): 扫描并连盒移除 rounded-full 伪徽章、text-xs 凑数小字、Emoji 噪音 + 提权核心标题 class
3. Image (.png): 像素级无痕背景采样抹除顶部伪英文胶囊 + 原位放大重绘人味中文标题
4. Document (.docx & .md): 扫描黑话与冗余段落并执行人味化清理
"""

import json
import shutil
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.util import Inches, Pt

from doc_cleaner import apply_doc_plan, scan_doc
from image_cleaner import apply_image_plan
from pptx_cleaner import apply_pptx_plan
from pptx_inspector import inspect_pptx
from web_cleaner import apply_web_plan, scan_web_file


def test_pptx_pipeline(tmp_dir: Path):
    print("▶ [1/4] 测试 PPTX 扫描、连盒删除与视觉提权引擎...")
    pptx_in = tmp_dir / "sample_ai_slop.pptx"
    pptx_out = tmp_dir / "sample_ai_slop_cleaned.pptx"

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(blank_layout)

    # 1. 顶部装饰胶囊框 (AutoShape) + 伪英文小字 (TextBox)
    pill_bg = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.45), Inches(3.6), Inches(0.42)
    )
    pill_bg.fill.solid()
    pill_bg.fill.fore_color.rgb = RGBColor(224, 231, 255)

    kicker_tb = slide.shapes.add_textbox(Inches(0.85), Inches(0.48), Inches(3.5), Inches(0.36))
    p_kicker = kicker_tb.text_frame.paragraphs[0]
    p_kicker.text = "SECTION 01 · STRATEGIC OVERVIEW"
    p_kicker.font.size = Pt(10)

    # 2. 卡片大背景框 (不应被误判为小胶囊框) + 卡片内部含主标题与凑数解释小字的文本框
    card_bg = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5), Inches(5.5), Inches(3.2)
    )
    card_bg.fill.solid()
    card_bg.fill.fore_color.rgb = RGBColor(248, 250, 252)

    card_tb = slide.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(5.0), Inches(2.4))
    tf = card_tb.text_frame
    p_title = tf.paragraphs[0]
    p_title.text = "多维感知赋能智慧分选闭环"
    p_title.font.size = Pt(16)

    p_sub = tf.add_paragraph()
    p_sub.text = "通过引入全链路高效视觉算法抓手，全方位实现多维度果蔬分选效率的闭环提升。"
    p_sub.font.size = Pt(10.5)

    # 3. 底部横条底栏 (AutoShape) + 免责/假大空总结小字
    footer_bg = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(6.5), Inches(11.7), Inches(0.55)
    )
    footer_bg.fill.solid()
    footer_bg.fill.fore_color.rgb = RGBColor(30, 41, 59)

    footer_tb = slide.shapes.add_textbox(Inches(0.9), Inches(6.55), Inches(11.5), Inches(0.45))
    p_footer = footer_tb.text_frame.paragraphs[0]
    p_footer.text = "本页核心洞察：以数字化顶层设计赋能全链路生态闭环（注：以上数据仅供演示参考）"
    p_footer.font.size = Pt(10)

    prs.save(str(pptx_in))

    # 运行扫描器
    report = inspect_pptx(str(pptx_in))
    assert report["summary"]["total_flagged_shapes"] == 3, f"Expected 3 flagged shapes, got {report}"
    assert report["summary"]["total_paired_bg_shapes"] == 2, f"Expected 2 paired bg shapes, got {report}"

    # 构造清理与提权计划
    delete_ids = []
    for sp_info in report["slides"][0]["text_shapes"]:
        if "kicker_badge" in sp_info["issues"] or "footer_slop" in sp_info["issues"]:
            delete_ids.append(sp_info["shape_id"])
            if sp_info["paired_bg_shape_id"]:
                delete_ids.append(sp_info["paired_bg_shape_id"])

    plan = {
        "slides": [
            {
                "slide_index": 1,
                "delete_shape_ids": delete_ids,
                "delete_paragraphs": [
                    {"shape_id": card_tb.shape_id, "paragraph_indices": [1]}
                ],
                "rewrites": [
                    {
                        "shape_id": card_tb.shape_id,
                        "paragraph_index": 0,
                        "new_text": "双目相机 + 轻量模型，0.2 秒挑出瑕疵果",
                        "promote_pt": 4.0,
                        "vertical_center": True,
                    }
                ],
            }
        ]
    }

    stats = apply_pptx_plan(str(pptx_in), plan, str(pptx_out))
    assert stats["deleted_shapes"] == 4, f"Expected 4 shapes deleted (2 text + 2 bg), got {stats}"
    assert stats["deleted_paragraphs"] == 1
    assert stats["promoted_paragraphs"] == 1

    # 重新打开验证清洗后的 PPTX
    prs_after = Presentation(str(pptx_out))
    remaining_shapes = list(prs_after.slides[0].shapes)
    assert len(remaining_shapes) == 2, f"Expected only card_bg and card_tb left, got {len(remaining_shapes)}"
    cleaned_tb = [s for s in remaining_shapes if s.has_text_frame and s.text_frame.text.strip()][0]
    assert cleaned_tb.text_frame.text.strip() == "双目相机 + 轻量模型，0.2 秒挑出瑕疵果"
    assert round(cleaned_tb.text_frame.paragraphs[0].font.size.pt, 1) == 20.0
    print("  ✅ PPTX 引擎测试通过（连盒删除 2 组胶囊/底栏 + 剔除凑数小字 + 主标题提权至 20pt）")


def test_web_pipeline(tmp_dir: Path):
    print("▶ [2/4] 测试网站/前端 (HTML) 扫描与去 AI 味提权引擎...")
    html_in = tmp_dir / "sample_landing.html"
    html_out = tmp_dir / "sample_landing_cleaned.html"

    html_in.write_text(
        """<!DOCTYPE html>
<html>
<body>
  <section class="hero">
    <span class="rounded-full bg-indigo-500/10 px-3 py-1 text-xs uppercase tracking-wider">✨ SECTION 01 · AI-POWERED ECOSYSTEM</span>
    <h2 class="text-base font-medium">🚀 多维协同赋能智能硬件实训闭环</h2>
    <p class="text-xs text-slate-400">通过全链路数字化抓手，全方位赋能学生实现从底层逻辑到顶层设计的范式转移。</p>
  </section>
  <footer>
    <p class="text-xs">本页核心洞察：构建全链路数字生态（注：数据仅供演示参考）</p>
  </footer>
</body>
</html>""",
        encoding="utf-8",
    )

    scan_res = scan_web_file(str(html_in))
    assert scan_res["findings_count"] >= 3, f"Expected >=3 findings, got {scan_res}"

    web_plan = {
        "auto_remove_detected_badges": True,
        "strip_emoji_slop": True,
        "rewrites": [
            {
                "old": "多维协同赋能智能硬件实训闭环",
                "new": "从画电路板到写 PLC 程序，全程自己动手做通",
            }
        ],
        "class_promotions": [
            {
                "old": "text-base font-medium",
                "new": "text-xl font-bold leading-snug",
            }
        ],
    }

    stats = apply_web_plan(str(html_in), web_plan, str(html_out))
    cleaned_html = html_out.read_text(encoding="utf-8")
    assert "SECTION 01" not in cleaned_html
    assert "仅供演示参考" not in cleaned_html
    assert "text-xl font-bold leading-snug" in cleaned_html
    assert "从画电路板到写 PLC 程序" in cleaned_html
    assert "✨" not in cleaned_html and "🚀" not in cleaned_html
    print(f"  ✅ Web 引擎测试通过：{stats}")


def test_image_pipeline(tmp_dir: Path):
    print("▶ [3/4] 测试图片载体 (海报/信息图 PNG) 无痕擦除小字与原位大字重绘引擎...")
    img_in = tmp_dir / "sample_poster.png"
    img_out = tmp_dir / "sample_poster_cleaned.png"

    # 创建一张 800x450 的模拟 AI 信息图：带顶部深蓝胶囊框和中间浅白卡片
    im = Image.new("RGB", (800, 450), color=(244, 246, 250))
    draw = ImageDraw.Draw(im)
    # 顶部伪英文胶囊色块 (x: 60..320, y: 30..68)
    draw.rounded_rectangle([60, 30, 320, 68], radius=16, fill=(79, 70, 229))
    draw.text((80, 42), "SECTION 01 // CORE INSIGHT", fill=(255, 255, 255))
    # 卡片框 (x: 60..740, y: 110..340)
    draw.rounded_rectangle([60, 110, 740, 340], radius=18, fill=(255, 255, 255))
    draw.text((90, 150), "AI Slop Heading + Redundant small text...", fill=(60, 60, 60))
    im.save(str(img_in))

    img_plan = {
        "regions": [
            {
                "bbox": [56, 26, 326, 72],
                "action": "erase_only",
            },
            {
                "bbox": [80, 130, 720, 320],
                "action": "erase_and_redraw",
                "text": "双目视觉 0.2 秒识别单果瑕疵，比人工挑果快 4 倍",
                "font_size": 26,
                "align": "center",
            },
        ]
    }

    stats = apply_image_plan(str(img_in), img_plan, str(img_out))
    assert stats["erased_regions"] == 2
    assert stats["redrawn_regions"] == 1
    assert img_out.exists()

    # 验证顶部紫色胶囊框已被擦除为接近背景浅灰 (244, 246, 250)
    out_im = Image.open(str(img_out)).convert("RGB")
    px = out_im.getpixel((180, 48))
    assert px[0] > 230 and px[1] > 230 and px[2] > 235, f"Expected pill erased to light background, got {px}"
    print(f"  ✅ Image 引擎测试通过：{stats}")


def test_doc_pipeline(tmp_dir: Path):
    print("▶ [4/4] 测试文档载体 (.docx / .md) 扫描与人味化清理引擎...")
    md_in = tmp_dir / "sample_notes.md"
    md_out = tmp_dir / "sample_notes_cleaned.md"

    md_in.write_text(
        "# ✨ 项目方案汇报\n\n"
        "> SECTION 01 · STRATEGIC OVERVIEW\n\n"
        "本项目基于深度学习底层逻辑，通过全链路视觉抓手实现果蔬分选闭环。\n\n"
        "注：以上数据仅供演示参考，具体以实际为准。\n",
        encoding="utf-8",
    )

    rep = scan_doc(str(md_in))
    assert rep["flagged_count"] >= 3

    doc_plan = {
        "strip_emoji_slop": True,
        "remove_exact": [
            "> SECTION 01 · STRATEGIC OVERVIEW\n\n",
            "注：以上数据仅供演示参考，具体以实际为准。\n",
        ],
        "rewrites": [
            {
                "old": "本项目基于深度学习底层逻辑，通过全链路视觉抓手实现果蔬分选闭环。",
                "new": "我们用双目相机配合轻量化模型，实现了从拍照识别到气吹分拣的全自动流水线。",
            }
        ],
    }

    stats = apply_doc_plan(str(md_in), doc_plan, str(md_out))
    cleaned_md = md_out.read_text(encoding="utf-8")
    assert "SECTION 01" not in cleaned_md
    assert "仅供演示参考" not in cleaned_md
    assert "双目相机配合轻量化模型" in cleaned_md

    # 同时测试 .docx 扫描与清理
    try:
        from docx import Document
        docx_in = tmp_dir / "sample_report.docx"
        docx_out = tmp_dir / "sample_report_cleaned.docx"
        doc = Document()
        doc.add_heading("项目实施方案", level=1)
        doc.add_paragraph("SECTION 01 · STRATEGIC OVERVIEW")
        doc.add_paragraph("通过全链路数字化抓手赋能闭环管理。")
        doc.save(str(docx_in))

        d_rep = scan_doc(str(docx_in))
        assert d_rep["flagged_count"] == 2
        d_plan = {
            "delete_paragraph_indices": [1],
            "rewrites": [
                {"paragraph_index": 2, "new_text": "我们用一套自动化脚本把原本 3 天的统计缩短到了 10 分钟。"}
            ],
        }
        d_stats = apply_doc_plan(str(docx_in), d_plan, str(docx_out))
        assert d_stats["deleted_items"] == 1
        assert d_stats["rewritten_items"] == 1
    except ImportError:
        pass

    print(f"  ✅ Doc (.md & .docx) 引擎测试通过：{stats}")


def main():
    tmp_dir = Path(tempfile.mkdtemp(prefix="ai_clean_master_test_"))
    try:
        test_pptx_pipeline(tmp_dir)
        test_web_pipeline(tmp_dir)
        test_image_pipeline(tmp_dir)
        test_doc_pipeline(tmp_dir)
        print("\n🎉 ALL 4 CARRIER SMOKE TESTS PASSED SUCCESSFULLY!")
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)


if __name__ == "__main__":
    main()
