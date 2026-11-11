#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_smoke.py — AI Clean Master 全链路自动化冒烟与行业/角标硬核断言测试套件
测试范围：
1. 10 大行业中英双语识别器 (industry_classifier) 精度与白名单曝光
2. 真实法定/临床/金融/工程/学术/ESG 角标保护 vs. 虚假 AI 演示免责剔除
3. PPTX (.pptx): 扫描配对胶囊框 + 连盒删除 + 凑数小字清理 + 核心文案提权 + 真实合规角标防御性保护
4. Web (.html): 扫描并连盒移除 rounded-full 伪徽章、text-xs 凑数小字、Emoji 噪音 + 提权 class + 真实角标保护
5. Image (.png): 像素级无痕背景擦除伪英文胶囊 + 原位放大重绘人味标题 + 真实角标跳过擦除保护
6. Document (.docx & .md): 扫描黑话与冗余段落 + 人味化清理 + 真实角标防御性保护
"""

import json
import shutil
import sys
import tempfile
from pathlib import Path

# Ensure scripts directory is on sys.path
SCRIPTS_DIR = Path(__file__).resolve().parent
# If running inside .agents/teamwork/..., locate the real scripts/ dir
if "scripts" != SCRIPTS_DIR.name:
    for p in SCRIPTS_DIR.parents:
        if (p / "scripts").exists():
            SCRIPTS_DIR = p / "scripts"
            break
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from PIL import Image, ImageDraw
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.util import Inches, Pt

from doc_cleaner import apply_doc_plan, scan_doc
from image_cleaner import apply_image_plan
from industry_classifier import (
    INDUSTRY_PROFILES,
    detect_buzzwords_bilingual,
    detect_industry_and_language,
    get_all_whitelists,
    get_industry_profile,
    get_industry_whitelist,
    get_protected_footnote_patterns,
    get_supported_industries,
    is_protected_domain_footnote,
    is_redundant_subtext_bilingual,
    is_whitelisted_domain_term,
)
from pptx_cleaner import apply_pptx_plan
from pptx_inspector import inspect_pptx
from web_cleaner import apply_web_plan, scan_web_file


# ============================================================================
# 1. 10 大行业中英双语分类器识别与术语白名单测试
# ============================================================================

def test_industry_classifier_bilingual_10_industries():
    print("▶ [1/6] 测试 10 大行业中英双语自动识别器与专业白名单 API...")

    # 1. 验证 10 大行业支持完整性与 API 契约
    supported = get_supported_industries()
    assert len(supported) == 10, f"Expected 10 supported industries, got {len(supported)}"
    expected_industries = [
        "tech_saas_ai",
        "industrial_manufacturing",
        "education_academia",
        "finance_consulting",
        "healthcare_biotech",
        "retail_marketing",
        "public_gov_smartcity",
        "architecture_design",
        "energy_sustainability_agtech",
        "media_gaming_hospitality",
    ]
    for ind_id in expected_industries:
        assert ind_id in supported, f"Missing industry ID: {ind_id}"
        prof = get_industry_profile(ind_id)
        assert prof["id"] == ind_id
        assert len(prof["keywords_zh"]) >= 15
        assert len(prof["keywords_en"]) >= 15
        wl_zh = get_industry_whitelist(ind_id, lang="zh")
        wl_en = get_industry_whitelist(ind_id, lang="en")
        assert len(wl_zh) >= 15
        assert len(wl_en) >= 15

    # 验证全局白名单字典映射
    all_wl = get_all_whitelists()
    assert len(all_wl) == 10

    # 2. 真实中文业务语料 10 大行业分类识别断言
    samples_zh = {
        "tech_saas_ai": "我们对大模型进行了FP8量化推理基准测试，微服务架构下P99延迟稳定在18ms，吞吐量提升了3倍。",
        "industrial_manufacturing": "产线机械手由西门子PLC控制，伺服电机驱动气缸执行分选，工位重复定位精度达到正负0.02mm，良品率提升至99.4%。",
        "education_academia": "本课题在高校创新实验室开展了消融实验，对照组与实验组样本的显著性检验表明教学实训台有效降低了样机物料清单成本。",
        "finance_consulting": "公司最新财报显示GAAP净利润与自由现金流表现强劲，由于回本周期缩短与高净留存率，毛利率提升了450个基点。",
        "healthcare_biotech": "该临床试验在三甲医院完成多中心患者入组，双盲对照筛查结果显示诊断试剂的敏感度达98.2%，特异度达99.1%，无严重不良反应。",
        "retail_marketing": "本季度电商直播大促期间，门店全渠道客单价与转化率显著提升，爆款SKU动销率加快，复购率较去年翻倍。",
        "public_gov_smartcity": "市政推进基层社区一网通办便民工程，压缩行政审批时限，最多跑一次事项办结率达98.5%，营商环境大幅优化。",
        "architecture_design": "该园区建筑规划的容积率与窗墙比经过精细采光模拟，外立面采用阳极氧化铝合金与大倒角结构，得房率达88%。",
        "energy_sustainability_agtech": "分布式光伏电站与储能微电网协同运行，度电成本持续下降；现代农业大棚采用水肥一体化与滴灌技术，每亩作物减排成效显著。",
        "media_gaming_hospitality": "新上线动作游戏在UE5引擎加持下实现60帧率稳定战斗，次留与完播率表现优异，文旅景区实景互动带动单日客流破万。",
    }

    for exp_id, text in samples_zh.items():
        res = detect_industry_and_language(text)
        assert res["industry_id"] == exp_id, f"ZH Mismatch: expected {exp_id}, got {res['industry_id']} for '{text}'"
        assert res["language"] == "zh"
        assert res["confidence"] in ("high", "medium")
        assert len(res["matched_domain_terms"]) >= 2

    # 3. 真实英文业务语料 10 大行业分类识别断言
    samples_en = {
        "tech_saas_ai": "Our cloud-native microservice architecture optimized LLM inference latency down to 15ms, achieving 3x throughput in benchmark tests.",
        "industrial_manufacturing": "The automated conveyor assembly line uses PLC interlock controls and servo actuators to cut cycle time and boost first pass yield to 99.2%.",
        "education_academia": "Our university laboratory conducted an ablation study with a rigorous control group, proving prototype efficacy with statistically significant results.",
        "finance_consulting": "Our latest audit confirmed strong EBITDA margins and free cash flow, with CAC payback dropping to 8 months and net dollar retention reaching 124%.",
        "healthcare_biotech": "In this multi-center clinical oncology trial, patient biomarker screening achieved high sensitivity and specificity with zero adverse events.",
        "retail_marketing": "During the holiday campaign, our omnichannel ecommerce storefront improved ROAS, raised average order value (AOV), and doubled repeat purchase rates.",
        "public_gov_smartcity": "The municipal smart city governance platform streamlined civic transit permits and e-government public service delivery across city agencies.",
        "architecture_design": "The architectural facade incorporates anodized unibody panels, an optimized window-to-wall ratio, and passive daylight cross-ventilation.",
        "energy_sustainability_agtech": "Integrating solar photovoltaic panels and battery storage reduced the LCOE while precision drip irrigation increased crop yield per acre.",
        "media_gaming_hospitality": "Our Unreal Engine action title maintains a solid 60fps frame rate during intense gameplay, driving 42% D1 player retention.",
    }

    for exp_id, text in samples_en.items():
        res = detect_industry_and_language(text)
        assert res["industry_id"] == exp_id, f"EN Mismatch: expected {exp_id}, got {res['industry_id']} for '{text}'"
        assert res["language"] == "en"
        assert res["confidence"] in ("high", "medium")
        assert len(res["matched_domain_terms"]) >= 2

    # 4. 专业白名单保护函数 is_whitelisted_domain_term 校验
    assert is_whitelisted_domain_term("P99 latency", "tech_saas_ai") is True
    assert is_whitelisted_domain_term("PLC", "industrial_manufacturing") is True
    assert is_whitelisted_domain_term("消融实验", "education_academia") is True
    assert is_whitelisted_domain_term("EBITDA", "finance_consulting") is True
    assert is_whitelisted_domain_term("敏感度", "healthcare_biotech") is True
    assert is_whitelisted_domain_term("ROAS", "retail_marketing") is True
    assert is_whitelisted_domain_term("一网通办", "public_gov_smartcity") is True
    assert is_whitelisted_domain_term("容积率", "architecture_design") is True
    assert is_whitelisted_domain_term("LCOE", "energy_sustainability_agtech") is True
    assert is_whitelisted_domain_term("帧率", "media_gaming_hospitality") is True

    # 验证黑话检测函数 detect_buzzwords_bilingual
    slop_zh = "通过全栈赋能与生态共振，实现闭环与颠覆性范式转移"
    hits_zh = detect_buzzwords_bilingual(slop_zh)
    assert len(hits_zh) >= 3

    slop_en = "We delve into next-gen holistic synergies to seamlessly empower enterprise transformation"
    hits_en = detect_buzzwords_bilingual(slop_en)
    assert "delve" in hits_en
    assert "seamlessly" in hits_en
    assert "empower" in hits_en

    print("  ✅ 10 大行业中英双语分类器识别率 100% (20/20)，白名单与黑话检测校验通过！")


# ============================================================================
# 2. 真实行业法定/合规角标保护 vs. 假大空 AI 免责剔除硬核断言
# ============================================================================

def test_statutory_footnote_protection_vs_fake_disclaimers():
    print("▶ [2/6] 测试真实法定/临床/金融/工程/学术/ESG 角标保护 vs. 虚假 AI 免责剔除...")

    # 真实角标库 (涵盖 FDA, NMPA, GAAP, Non-GAAP, 10-K, ISO, GB/T, IEC, Scope 1/2/3, IEEE, arXiv, 版权)
    genuine_statutory_footnotes = [
        # 医疗/临床/生物统计
        "* 临床试验数据基于三甲医院 320 例双盲对照入组患者 (p < 0.01, 95% CI: [0.82, 0.94])",
        "* FDA 510(k) cleared device (K231456); For Investigational Use Only outside designated indications.",
        "* 本品经国家药品监督管理局批准 (国械注准 20243400123)，适应症范围详见说明书。",
        "* Clinical Trial NCT04812345: Phase III study evaluating progression-free survival (mPFS = 14.2 months).",
        "* In vitro assay showed IC50 = 12.4 nM against target biomarker; n = 450 per cohort.",
        "* 获得国家药品监督管理局 NMPA 创新医疗器械特别审查资格批准。",

        # 金融/审计/证券合规
        "* Non-GAAP Financial Measures: Adjusted EBITDA excludes stock-based compensation and acquisition expenses.",
        "* 财务数据经独立第三方会计师事务所审计，符合中国企业会计准则及 SEC Form 10-K 披露规范。",
        "* Past performance is not indicative of future results. CAGR calculated from FY2021 to FY2025.",
        "* 数据来源：Wind 资讯与公司 2025Q3 未经审计季度财报，统计口径包含海外全资子公司。",
        "* Net Dollar Retention (NDR) reached 126% YoY; gross margin expanded 320 bps under GAAP.",
        "* Unaudited interim condensed consolidated financial statements for Q3 2025.",

        # 工业/工程/国际标准/ESG/学术论文
        "* 零件机械加工公差严格按 GB/T 1804-m 级执行，电气控制系统符合 ISO 13849-1 Cat.4 PLe 安全认证。",
        "* Automated logic compliant with IEC 61131-3 standard; PLC cycle time measured at 1.0ms on S7-1500.",
        "* 温室气体减排核算依据 GHG Protocol Scope 1、Scope 2 与 Scope 3 统计（经第三方核证减排 14,200 tCO2e）。",
        "* Levelized Cost of Electricity (LCOE) calculated at $0.028/kWh; battery cycle life > 6,000 cycles.",
        "* Architecture details and ablation metrics published in arXiv:2405.12345v2 [cs.CL]; IEEE 802.3.",
        "* 本研究受国家自然科学基金 (No. 62172001) 资助，消融实验测试环境详见附录表格。",

        # 文娱传媒与版权声明
        "* Copyright © 2026 Studio Inc. All rights reserved. 4K@60fps real-time gameplay captured on UE5.",
        "* © 2025 品牌所有，未经许可禁止商业转载或非遗授权二次开发。",
    ]

    for fn in genuine_statutory_footnotes:
        assert is_protected_domain_footnote(fn) is True, f"Genuine footnote falsely rejected: {fn}"

    # 虚假 AI 演示免责与凑数占位小字 (必须返回 False)
    fake_ai_disclaimers = [
        "注：以上数据仅供演示参考，具体以实际业务情况为准。",
        "本页核心洞察：以数字化顶层设计赋能全链路生态闭环（注：数据仅供演示参考）",
        "Note: Data and metrics are generated for demonstration purposes only.",
        "For illustrative purposes only; sample layout created by AI.",
        "Disclaimer: Fictitious data used for display purposes.",
        "本图表为排版展示使用，不构成任何真实投资建议。",
        "Mock numbers generated by AI for testing purposes.",
        "Dummy text and placeholder layout generated for demonstration.",
        "Generated by AI placeholder - for illustrative purposes only.",
        "仅供演示参考，请以官方最终发布口径为准。",
    ]

    for fake in fake_ai_disclaimers:
        assert is_protected_domain_footnote(fake) is False, f"Fake disclaimer falsely protected: {fake}"

    # 验证底层正则对象曝光
    patterns = get_protected_footnote_patterns()
    assert len(patterns) >= 4

    print(f"  ✅ 真实合规角标 100% 保护 ({len(genuine_statutory_footnotes)}/{len(genuine_statutory_footnotes)})，虚假 AI 免责 100% 剔除 ({len(fake_ai_disclaimers)}/{len(fake_ai_disclaimers)})！")


# ============================================================================
# 3. PPTX 引擎自动化测试 (含连盒清理、字号提权与真实角标防护)
# ============================================================================

def test_pptx_pipeline(tmp_dir: Path):
    print("▶ [3/6] 测试 PPTX 扫描、连盒删除、视觉提权与真实角标防护引擎...")
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

    # 2. 卡片大背景框 + 卡片内部文本框
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

    # 3. 底部横条底栏 + 虚假免责/假大空总结小字
    footer_bg = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(6.0), Inches(11.7), Inches(0.55)
    )
    footer_bg.fill.solid()
    footer_bg.fill.fore_color.rgb = RGBColor(30, 41, 59)

    footer_tb = slide.shapes.add_textbox(Inches(0.9), Inches(6.05), Inches(11.5), Inches(0.45))
    p_footer = footer_tb.text_frame.paragraphs[0]
    p_footer.text = "本页核心洞察：以数字化顶层设计赋能全链路生态闭环（注：以上数据仅供演示参考）"
    p_footer.font.size = Pt(10)

    # 4. 真实临床/法规保护角标 (严禁被判定为 footer_slop 或被误删)
    protected_tb = slide.shapes.add_textbox(Inches(0.9), Inches(6.8), Inches(11.5), Inches(0.45))
    p_prot = protected_tb.text_frame.paragraphs[0]
    p_prot.text = "* 临床试验基于三甲医院 320 例双盲入组患者 (p < 0.01, 95% CI: [0.82, 0.94]); 符合 FDA 510(k) 申报规范。"
    p_prot.font.size = Pt(9)

    prs.save(str(pptx_in))

    # 运行扫描器
    report = inspect_pptx(str(pptx_in))
    assert report["summary"]["total_flagged_shapes"] == 3, f"Expected 3 flagged shapes (excluding protected footnote), got {report}"
    assert report["summary"]["total_paired_bg_shapes"] == 2, f"Expected 2 paired bg shapes, got {report}"

    # 验证真实角标文本框未被标记为任何病灶
    prot_sp_info = [s for s in report["slides"][0]["text_shapes"] if s["shape_id"] == protected_tb.shape_id][0]
    assert len(prot_sp_info["issues"]) == 0, f"Protected footnote shape must have 0 issues, got {prot_sp_info['issues']}"

    # 构造清理与提权计划，故意在 delete_shape_ids 中混入 protected_tb.shape_id 检验防御机制
    delete_ids = [protected_tb.shape_id]
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
    assert stats["protected_footnotes_preserved"] >= 1, f"Expected protected footnote preserved, got {stats}"

    # 重新打开验证清洗后的 PPTX
    prs_after = Presentation(str(pptx_out))
    remaining_shapes = list(prs_after.slides[0].shapes)
    assert len(remaining_shapes) == 3, f"Expected 3 shapes left (card_bg, card_tb, protected_tb), got {len(remaining_shapes)}"

    # 校验提权标题与受保护角标内容
    texts = [s.text_frame.text.strip() for s in remaining_shapes if s.has_text_frame and s.text_frame.text.strip()]
    assert "双目相机 + 轻量模型，0.2 秒挑出瑕疵果" in texts
    assert any("FDA 510(k)" in t for t in texts)
    print("  ✅ PPTX 引擎测试通过（连盒删除 2 组胶囊/底栏 + 剔除凑数小字 + 主标题提权至 20pt + 真实角标防御性存活）")


# ============================================================================
# 4. Web 前端引擎自动化测试 (含伪徽章连盒剥离、样式提权与真实角标防护)
# ============================================================================

def test_web_pipeline(tmp_dir: Path):
    print("▶ [4/6] 测试网站/前端 (HTML) 扫描、去 AI 味提权与真实角标防护引擎...")
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
    <p class="text-xs text-slate-400">* 电气控制回路符合 ISO 13849-1 Cat.4 PLe 安全认证标准，急停响应时间 < 20ms。</p>
  </section>
  <footer>
    <p class="text-xs">本页核心洞察：构建全链路数字生态（注：数据仅供演示参考）</p>
    <p class="text-xs text-slate-500">* Non-GAAP Measures: Adjusted EBITDA excludes stock-based compensation; SEC Form 10-K.</p>
  </footer>
</body>
</html>""",
        encoding="utf-8",
    )

    scan_res = scan_web_file(str(html_in))
    assert scan_res["findings_count"] >= 3, f"Expected >=3 findings, got {scan_res}"
    assert len(scan_res["protected_footnotes"]) >= 2, f"Expected >= 2 protected footnotes in scan, got {scan_res['protected_footnotes']}"

    web_plan = {
        "auto_remove_detected_badges": True,
        "strip_emoji_slop": True,
        "remove_exact": [
            '<p class="text-xs text-slate-400">* 电气控制回路符合 ISO 13849-1 Cat.4 PLe 安全认证标准，急停响应时间 < 20ms。</p>'
        ],
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
    # 验证受保护真实角标完整存活
    assert "ISO 13849-1 Cat.4 PLe" in cleaned_html
    assert "Non-GAAP Measures" in cleaned_html
    assert stats["protected_footnotes_preserved"] >= 1
    print(f"  ✅ Web 引擎测试通过（连盒删除徽章 + 样式提权 + 真实角标防御存活）：{stats}")


# ============================================================================
# 5. Image 引擎自动化测试 (含背景采样擦除、大字重绘与真实角标跳过保护)
# ============================================================================

def test_image_pipeline(tmp_dir: Path):
    print("▶ [5/6] 测试图片载体 (海报 PNG) 无痕擦除小字、原位大字重绘与真实角标保护引擎...")
    img_in = tmp_dir / "sample_poster.png"
    img_out = tmp_dir / "sample_poster_cleaned.png"

    # 创建 800x450 的模拟 AI 信息图
    im = Image.new("RGB", (800, 450), color=(244, 246, 250))
    draw = ImageDraw.Draw(im)
    # 顶部伪英文胶囊色块 (x: 60..320, y: 30..68)
    draw.rounded_rectangle([60, 30, 320, 68], radius=16, fill=(79, 70, 229))
    draw.text((80, 42), "SECTION 01 // CORE INSIGHT", fill=(255, 255, 255))
    # 卡片框 (x: 60..740, y: 110..340)
    draw.rounded_rectangle([60, 110, 740, 340], radius=18, fill=(255, 255, 255))
    draw.text((90, 150), "AI Slop Heading + Redundant small text...", fill=(60, 60, 60))
    # 真实数据来源标注 (x: 60..740, y: 380..410)
    draw.text((70, 390), "* Source: Wind Data & Unaudited 2025Q3 Report, CAGR = 24.5%", fill=(100, 100, 100))
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
            {
                "bbox": [60, 380, 740, 420],
                "text": "* Source: Wind Data & Unaudited 2025Q3 Report, CAGR = 24.5%",
                "action": "erase_only",  # 故意传入 erase_only，验证引擎自动识别真角标并防御性保留
            },
        ]
    }

    stats = apply_image_plan(str(img_in), img_plan, str(img_out))
    assert stats["erased_regions"] == 2
    assert stats["redrawn_regions"] == 1
    assert stats["preserved_regions"] == 1, f"Expected 1 preserved region, got {stats}"
    assert img_out.exists()

    # 验证顶部紫色胶囊框已被擦除为接近背景浅灰 (244, 246, 250)
    out_im = Image.open(str(img_out)).convert("RGB")
    px = out_im.getpixel((180, 48))
    assert px[0] > 230 and px[1] > 230 and px[2] > 235, f"Expected pill erased to light background, got {px}"
    print(f"  ✅ Image 引擎测试通过（无痕擦除 + 原位重绘 + 真实角标跳过保护）：{stats}")


# ============================================================================
# 6. Document 引擎自动化测试 (含 DOCX/MD 扫描清理与真实角标防护)
# ============================================================================

def test_doc_pipeline(tmp_dir: Path):
    print("▶ [6/6] 测试文档载体 (.docx / .md) 扫描、人味化清理与真实角标防护引擎...")
    md_in = tmp_dir / "sample_notes.md"
    md_out = tmp_dir / "sample_notes_cleaned.md"

    md_in.write_text(
        "# ✨ 项目方案汇报\n\n"
        "> SECTION 01 · STRATEGIC OVERVIEW\n\n"
        "本项目基于深度学习底层逻辑，通过全链路视觉抓手实现果蔬分选闭环。\n\n"
        "* 依据 GHG Protocol 审计，2025 年度实现 Scope 1 与 Scope 2 减排 14,200 tCO2e。\n\n"
        "注：以上数据仅供演示参考，具体以实际业务情况为准。\n",
        encoding="utf-8",
    )

    rep = scan_doc(str(md_in))
    assert rep["flagged_count"] >= 3
    assert len(rep["protected_footnotes"]) >= 1, f"Expected protected footnote in scan, got {rep['protected_footnotes']}"

    doc_plan = {
        "strip_emoji_slop": True,
        "remove_exact": [
            "> SECTION 01 · STRATEGIC OVERVIEW\n\n",
            "* 依据 GHG Protocol 审计，2025 年度实现 Scope 1 与 Scope 2 减排 14,200 tCO2e。\n\n",  # 故意放入试图删除
            "注：以上数据仅供演示参考，具体以实际业务情况为准。\n",
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
    # 验证真实角标防御性存活
    assert "Scope 1 与 Scope 2 减排" in cleaned_md
    assert stats["protected_footnotes_preserved"] >= 1

    # 同时测试 .docx 扫描与清理
    try:
        from docx import Document
        docx_in = tmp_dir / "sample_report.docx"
        docx_out = tmp_dir / "sample_report_cleaned.docx"
        doc = Document()
        doc.add_heading("项目实施方案", level=1)
        doc.add_paragraph("SECTION 01 · STRATEGIC OVERVIEW")
        doc.add_paragraph("通过全链路数字化抓手赋能闭环管理。")
        doc.add_paragraph("* 加工公差执行 GB/T 1804-m 级，电气回路符合 ISO 13849-1 Cat.4 PLe 认证。")
        doc.save(str(docx_in))

        d_rep = scan_doc(str(docx_in))
        assert d_rep["flagged_count"] == 2
        assert len(d_rep["protected_footnotes"]) == 1

        d_plan = {
            "delete_paragraph_indices": [1, 3],  # 试图连同索引 3 的真实角标一起删除
            "rewrites": [
                {"paragraph_index": 2, "new_text": "我们用一套自动化脚本把原本 3 天的统计缩短到了 10 分钟。"}
            ],
        }
        d_stats = apply_doc_plan(str(docx_in), d_plan, str(docx_out))
        assert d_stats["deleted_items"] == 1  # 索引 3 受保护，实际仅删除 1 项
        assert d_stats["rewritten_items"] == 1
        assert d_stats["protected_footnotes_preserved"] >= 1

        doc_after = Document(str(docx_out))
        doc_texts = [p.text for p in doc_after.paragraphs if p.text]
        assert any("GB/T 1804-m" in t for t in doc_texts)
    except ImportError:
        pass

    print(f"  ✅ Doc (.md & .docx) 引擎测试通过（黑话改写 + 真实角标防御存活）：{stats}")


# ============================================================================
# 主执行入口
# ============================================================================

def main():
    tmp_dir = Path(tempfile.mkdtemp(prefix="ai_clean_master_test_"))
    try:
        test_industry_classifier_bilingual_10_industries()
        test_statutory_footnote_protection_vs_fake_disclaimers()
        test_pptx_pipeline(tmp_dir)
        test_web_pipeline(tmp_dir)
        test_image_pipeline(tmp_dir)
        test_doc_pipeline(tmp_dir)
        print("\n🎉 ALL 4 CARRIER SMOKE TESTS PASSED SUCCESSFULLY!")
        print("=" * 70)
        print("🎉 ALL 6 TEST SUITES (CLASSIFIER, FOOTNOTES, PPTX, WEB, IMAGE, DOC) PASSED!")
        print("=" * 70)
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)


if __name__ == "__main__":
    main()
