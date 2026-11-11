"""
Empirical Challenger Test Suite for Milestone 1
Validates references/industry-playbooks-bilingual.md,
references/ai-slop-dictionary.md, and references/layout-promotion-rules.md
against all quantitative and qualitative criteria.
"""

import os
import re
import sys
from pathlib import Path
import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
PLAYBOOK_PATH = REPO_ROOT / "references" / "industry-playbooks-bilingual.md"
DICTIONARY_PATH = REPO_ROOT / "references" / "ai-slop-dictionary.md"
LAYOUT_RULES_PATH = REPO_ROOT / "references" / "layout-promotion-rules.md"

sys.path.insert(0, str(REPO_ROOT))
from scripts.industry_classifier import is_protected_domain_footnote


@pytest.fixture(scope="module")
def playbook_text():
    assert PLAYBOOK_PATH.exists(), f"Missing file: {PLAYBOOK_PATH}"
    return PLAYBOOK_PATH.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def dictionary_text():
    assert DICTIONARY_PATH.exists(), f"Missing file: {DICTIONARY_PATH}"
    return DICTIONARY_PATH.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def layout_rules_text():
    assert LAYOUT_RULES_PATH.exists(), f"Missing file: {LAYOUT_RULES_PATH}"
    return LAYOUT_RULES_PATH.read_text(encoding="utf-8")


# ============================================================================
# 1. 10-Industry Playbook Structure & Completeness
# ============================================================================

def test_industry_playbook_headers(playbook_text):
    """Verify exactly 10 industry headers exist and match expected numbering."""
    industry_matches = re.findall(r"^## 行业 (\d+)：(.*)", playbook_text, re.MULTILINE)
    assert len(industry_matches) == 10, f"Expected 10 industries, found {len(industry_matches)}"
    
    industry_nums = [int(m[0]) for m in industry_matches]
    assert industry_nums == list(range(1, 11)), f"Industry numbering mismatch: {industry_nums}"
    
    expected_keywords = [
        ("科技", "Technology"),
        ("智能制造", "Industrial"),
        ("教育", "Education"),
        ("金融", "Finance"),
        ("医疗健康", "Healthcare"),
        ("消费零售", "Retail"),
        ("政务公共事业", "Public Sector"),
        ("建筑地产", "Architecture"),
        ("新能源", "Clean Energy"),
        ("文娱传媒", "Media"),
    ]
    for idx, (zh_kw, en_kw) in enumerate(expected_keywords):
        header_text = industry_matches[idx][1]
        assert zh_kw in header_text, f"Industry {idx+1} header missing '{zh_kw}': {header_text}"
        assert en_kw in header_text, f"Industry {idx+1} header missing '{en_kw}': {header_text}"


def test_industry_sections_presence(playbook_text):
    """Verify each of the 10 industries contains standardized Sections A, B, C, D."""
    industries = re.split(r"\n(?=## 行业 \d+：)", playbook_text)[1:]
    assert len(industries) == 10, f"Expected 10 split industry blocks, found {len(industries)}"
    
    for i, ind in enumerate(industries, 1):
        assert re.search(r"### A\. 小字清理与真角标保护边界", ind), f"Industry {i} missing Section A"
        assert re.search(r"### B\. 伪黑话黑名单 vs\. 真专业白名单", ind), f"Industry {i} missing Section B"
        assert re.search(r"### C\. 中英 1:1 改写范例", ind), f"Industry {i} missing Section C"
        assert re.search(r"### D\. 中英高质感表达模版与高说服力句式", ind), f"Industry {i} missing Section D"


# ============================================================================
# 2. Section A: Micro-Copy Delete List & Protected Standards
# ============================================================================

def test_section_a_delete_and_protected_lists(playbook_text):
    """Verify Section A in every industry defines banned micro-copy and statutory standards."""
    industries = re.split(r"\n(?=## 行业 \d+：)", playbook_text)[1:]
    
    for i, ind in enumerate(industries, 1):
        sec_a = re.search(r"### A\. 小字清理与真角标保护边界.*?(?=### B\.|$)", ind, re.DOTALL).group(0)
        
        # Check deletion list items
        assert "必删 AI 小字与胶囊" in sec_a, f"Industry {i} Section A missing delete list"
        assert "ZH" in sec_a and "EN" in sec_a, f"Industry {i} Section A delete list missing bilingual division"
        
        # Check protected standards section
        assert re.search(r"-\s+\*\*🛡️\s*严禁误删的真实[^*]+\*\*:", sec_a), f"Industry {i} Section A missing protected standards header"
        assert re.search(r"-\s+\*\*(?:法定|行业标准|国家标准)[^*]*\*\*:", sec_a), f"Industry {i} Section A missing statutory standard basis bullet"
        assert re.search(r"-\s+\*\*真实双语示例[^*]*\*\*:", sec_a), f"Industry {i} Section A missing protected examples bullet"
        
        # Check at least 4 protected examples per industry
        example_lines = [line.strip() for line in sec_a.splitlines() if re.match(r"^\s*\d+\.\s+`\*", line)]
        assert len(example_lines) >= 4, f"Industry {i} Section A has {len(example_lines)} protected examples, expected >= 4"


# ============================================================================
# 3. Section B: Slop vs. Authentic Domain Terms Quantitative Thresholds
# ============================================================================

def parse_terms_from_cell(cell_str: str, lang: str):
    """Accurately parse slop and domain terms from table cell."""
    cell_clean = cell_str.strip()
    if "中文" in lang:
        # Split by Chinese and English commas/enumeration marks
        parts = re.split(r"[、，,]", cell_clean)
        terms = [p.strip().strip("`") for p in parts if p.strip()]
    else:
        # English: backticks preferred, or fallback to comma split
        bt_terms = re.findall(r"`([^`]+)`", cell_clean)
        if bt_terms:
            terms = bt_terms
        else:
            terms = [p.strip() for p in cell_clean.split(",") if p.strip()]
    return terms


def test_section_b_term_counts(playbook_text):
    """
    Assert quantitative requirements for Section B:
    - Exactly 2 rows per industry (ZH and EN)
    - In EVERY row:
      - Slop terms >= 15 (target: 15~20)
      - Authentic domain terms >= 20 (target: 20~25)
    - No duplicate terms within the same row
    """
    industries = re.split(r"\n(?=## 行业 \d+：)", playbook_text)[1:]
    total_rows = 0
    
    for i, ind in enumerate(industries, 1):
        m_b = re.search(r"### B\. 伪黑话黑名单 vs\. 真专业白名单.*?\n(\|.*?\n\|[-| :]+\n(\|.*?\n)+)", ind)
        assert m_b, f"Industry {i}: Section B table not found"
        
        table_lines = [line.strip() for line in m_b.group(1).strip().split("\n") if line.strip()]
        assert len(table_lines) >= 3, f"Industry {i}: Section B table must have header, separator, and data rows"
        
        data_rows = table_lines[2:]
        assert len(data_rows) == 2, f"Industry {i}: Section B table expected 2 rows (ZH and EN), got {len(data_rows)}"
        
        for r in data_rows:
            total_rows += 1
            cols = [c.strip() for c in r.strip("|").split("|")]
            assert len(cols) == 3, f"Industry {i}: Row has {len(cols)} columns, expected 3: {r}"
            
            lang, slop_col, domain_col = cols[0], cols[1], cols[2]
            slop_terms = parse_terms_from_cell(slop_col, lang)
            domain_terms = parse_terms_from_cell(domain_col, lang)
            
            # Assert counts
            assert len(slop_terms) >= 15, (
                f"Industry {i} ({lang}): slop terms count {len(slop_terms)} < 15. Terms: {slop_terms}"
            )
            assert len(domain_terms) >= 20, (
                f"Industry {i} ({lang}): domain terms count {len(domain_terms)} < 20. Terms: {domain_terms}"
            )
            
            # Assert uniqueness (no duplicate terms within the row)
            slop_set = set(t.lower() for t in slop_terms)
            assert len(slop_set) == len(slop_terms), (
                f"Industry {i} ({lang}): duplicate slop terms detected! Total={len(slop_terms)}, Unique={len(slop_set)}"
            )
            domain_set = set(t.lower() for t in domain_terms)
            assert len(domain_set) == len(domain_terms), (
                f"Industry {i} ({lang}): duplicate domain terms detected! Total={len(domain_terms)}, Unique={len(domain_set)}"
            )

    assert total_rows == 20, f"Expected 20 Section B table rows across 10 industries, got {total_rows}"


# ============================================================================
# 4. Section C: Before -> After Pairs
# ============================================================================

def test_section_c_pairs_count_and_substance(playbook_text):
    """
    Verify Before -> After pairs in Section C:
    - >= 2 pairs per language per industry (2 ZH + 2 EN = 4 per industry = 40 total)
    - Before and After are distinct and nontrivial
    """
    industries = re.split(r"\n(?=## 行业 \d+：)", playbook_text)[1:]
    
    total_zh_before = 0
    total_zh_after = 0
    total_en_before = 0
    total_en_after = 0
    
    for i, ind in enumerate(industries, 1):
        sec_c = re.search(r"### C\. 中英 1:1 改写范例.*?(?=### D\.|$)", ind, re.DOTALL).group(0)
        
        # Split into ZH and EN subsections
        assert "中文对照范例" in sec_c, f"Industry {i} Section C missing Chinese pairs subsection"
        assert "English Parity Examples" in sec_c, f"Industry {i} Section C missing English pairs subsection"
        
        zh_part = sec_c.split("English Parity Examples")[0]
        en_part = sec_c.split("English Parity Examples")[1]
        
        # Chinese pairs
        zh_befores = re.findall(r"❌ \*\*Before \d+ \(AI Slop\)\*\*:\s*(.+)", zh_part)
        zh_afters = re.findall(r"✅ \*\*After \d+ \(Human Pro\)\*\*:\s*(.+)", zh_part)
        
        assert len(zh_befores) >= 2, f"Industry {i} has {len(zh_befores)} ZH Before items (expected >= 2)"
        assert len(zh_afters) >= 2, f"Industry {i} has {len(zh_afters)} ZH After items (expected >= 2)"
        assert len(zh_befores) == len(zh_afters), f"Industry {i} ZH Before/After mismatch"
        
        total_zh_before += len(zh_befores)
        total_zh_after += len(zh_afters)
        
        # English pairs
        en_befores = re.findall(r"❌ \*\*Before \d+ \(AI Slop\)\*\*:\s*(.+)", en_part)
        en_afters = re.findall(r"✅ \*\*After \d+ \(Human Pro\)\*\*:\s*(.+)", en_part)
        
        assert len(en_befores) >= 2, f"Industry {i} has {len(en_befores)} EN Before items (expected >= 2)"
        assert len(en_afters) >= 2, f"Industry {i} has {len(en_afters)} EN After items (expected >= 2)"
        assert len(en_befores) == len(en_afters), f"Industry {i} EN Before/After mismatch"
        
        total_en_before += len(en_befores)
        total_en_after += len(en_afters)
        
        # Verify substantive rewriting (Before != After and nontrivial length)
        for b, a in zip(zh_befores, zh_afters):
            assert len(b.strip()) > 10, f"Industry {i} ZH Before too short: {b}"
            assert len(a.strip()) > 10, f"Industry {i} ZH After too short: {a}"
            assert b.strip() != a.strip(), f"Industry {i} ZH Before equals After: {b}"
            
        for b, a in zip(en_befores, en_afters):
            assert len(b.strip()) > 10, f"Industry {i} EN Before too short: {b}"
            assert len(a.strip()) > 10, f"Industry {i} EN After too short: {a}"
            assert b.strip() != a.strip(), f"Industry {i} EN Before equals After: {b}"

    assert total_zh_before >= 20, f"Total ZH Before pairs {total_zh_before} < 20"
    assert total_zh_after >= 20, f"Total ZH After pairs {total_zh_after} < 20"
    assert total_en_before >= 20, f"Total EN Before pairs {total_en_before} < 20"
    assert total_en_after >= 20, f"Total EN After pairs {total_en_after} < 20"
    assert (total_zh_before + total_en_before) == 40, f"Total pairs {total_zh_before + total_en_before} != 40"


# ============================================================================
# 5. Section D: Sentence Templates & High-Impact Patterns
# ============================================================================

def test_section_d_sentence_templates(playbook_text):
    """
    Verify Section D templates:
    - >= 4-5 templates for ZH per industry
    - >= 4-5 templates for EN per industry
    - Total = 100 templates (50 ZH + 50 EN across 10 industries)
    - Templates must contain slot brackets e.g. [ ] indicating fillable patterns
    """
    industries = re.split(r"\n(?=## 行业 \d+：)", playbook_text)[1:]
    
    total_zh_templates = 0
    total_en_templates = 0
    
    for i, ind in enumerate(industries, 1):
        sec_d = re.search(r"### D\. 中英高质感表达模版与高说服力句式.*?(?=---\n|## 行业|$)", ind, re.DOTALL).group(0)
        
        assert "中文表达模版与高说服力句式" in sec_d, f"Industry {i} Section D missing Chinese templates header"
        assert "English High-Impact Templates" in sec_d, f"Industry {i} Section D missing English templates header"
        
        parts = sec_d.split("English High-Impact Templates")
        zh_part = parts[0]
        en_part = parts[1]
        
        zh_tpls = re.findall(r"^\s*\d+\.\s+\*\*\[.*?\]\*\*:\s*(.+)", zh_part, re.MULTILINE)
        en_tpls = re.findall(r"^\s*\d+\.\s+\*\*\[.*?\]\*\*:\s*(.+)", en_part, re.MULTILINE)
        
        assert len(zh_tpls) >= 5, f"Industry {i} ZH templates count {len(zh_tpls)} < 5"
        assert len(en_tpls) >= 5, f"Industry {i} EN templates count {len(en_tpls)} < 5"
        
        # Verify placeholders exist in templates
        for tpl in zh_tpls:
            assert "[" in tpl and "]" in tpl, f"Industry {i} ZH template lacks bracketed slots: {tpl}"
        for tpl in en_tpls:
            assert "[" in tpl and "]" in tpl, f"Industry {i} EN template lacks bracketed slots: {tpl}"
            
        total_zh_templates += len(zh_tpls)
        total_en_templates += len(en_tpls)
        
    assert total_zh_templates == 50, f"Total ZH templates {total_zh_templates} != 50"
    assert total_en_templates == 50, f"Total EN templates {total_en_templates} != 50"
    assert (total_zh_templates + total_en_templates) == 100, f"Total templates {total_zh_templates + total_en_templates} != 100"


# ============================================================================
# 6. ai-slop-dictionary.md Verification
# ============================================================================

def test_ai_slop_dictionary_structure_and_parity(dictionary_text):
    """
    Verify ai-slop-dictionary.md:
    - Cross-reference banner to industry-playbooks-bilingual.md
    - 4 categories in Section 1 with protected footnote boundaries
    - Section 2 unified bilingual buzzword tables
    - Section 3 covers 4 scenarios with BOTH ZH and EN Before->After pairs
    """
    # 1. Cross-reference
    assert "industry-playbooks-bilingual.md" in dictionary_text, "Missing cross-reference to industry-playbooks-bilingual.md"
    
    # 2. Section 1: 4 categories
    assert re.search(r"## 一、四大类「AI 味小字」", dictionary_text), "Missing Section 1"
    assert "1. 顶部 / 卡片伪英文与八股眉题" in dictionary_text
    assert "2. 卡片内同义反复的凑数解释小字" in dictionary_text
    assert "3. 页脚 / 底栏的假大空总结与免责废话 vs. 严禁误删的真合规角标" in dictionary_text
    assert "4. 伪造微数据 / 假角标与表情噪音" in dictionary_text
    
    # Protected footnote references
    assert "is_protected_domain_footnote" in dictionary_text
    for std in ["ISO", "GB/T", "FDA 510(k)", "p < 0.01", "Non-GAAP", "SEC Form 10-K", "Scope 1/2/3", "tCO2e"]:
        assert std in dictionary_text, f"Dictionary Section 1 missing standard code: {std}"
        
    # 3. Section 2: Unified Blacklist
    assert re.search(r"## 二、统一「去 AI 黑话」底线词表", dictionary_text), "Missing Section 2"
    assert "赋能" in dictionary_text and "抓手" in dictionary_text and "闭环" in dictionary_text
    assert "Empower" in dictionary_text and "Delve into" in dictionary_text and "Holistic ecosystem" in dictionary_text
    
    # 4. Section 3: 4 Scenarios with 1:1 Parity
    assert re.search(r"## 三、四大场景自适应「人味语感」改写指南", dictionary_text), "Missing Section 3"
    
    expected_scenarios = [
        "场景 1：竞赛路演 / 创客答辩风",
        "场景 2：工科实训 / 技术工程风",
        "场景 3：课堂教学 / 班会演讲风",
        "场景 4：干练商务 / 日常工作汇报风",
    ]
    for sc in expected_scenarios:
        assert sc in dictionary_text, f"Missing scenario: {sc}"
        
    # Verify each scenario has both Chinese and English pairs
    scenario_blocks = re.split(r"### 场景 \d+：", dictionary_text)[1:]
    assert len(scenario_blocks) == 4, f"Expected 4 scenario blocks, found {len(scenario_blocks)}"
    
    for i, sc_block in enumerate(scenario_blocks, 1):
        assert "中文对照范例" in sc_block, f"Scenario {i} missing Chinese pair header"
        assert "English Parity Example" in sc_block, f"Scenario {i} missing English pair header"
        
        # Verify Before and After items exist in both
        zh_part = sc_block.split("English Parity Example")[0]
        en_part = sc_block.split("English Parity Example")[1]
        
        assert "Before" in zh_part and "After" in zh_part, f"Scenario {i} ZH pair incomplete"
        assert "Before" in en_part and "After" in en_part, f"Scenario {i} EN pair incomplete"


# ============================================================================
# 7. layout-promotion-rules.md Verification
# ============================================================================

def test_layout_promotion_rules_structure_and_scope(layout_rules_text):
    """
    Verify layout-promotion-rules.md:
    - Bilingual descriptions and annotations
    - Section I: PPTX rules (IoA >= 0.75, font promotion formulas, footnote guard)
    - Section II: Image rules (sampling ring, erase_only, erase_and_redraw, footnote protection)
    - Section III: Web UI rules (pill badge removal, bento elevation, emoji clean, footnote preservation)
    - Section IV: Document (.docx / .md) normalization and promotion
    - Section V: Carrier Decision Matrix
    """
    assert "## 一、PPT (`.pptx`) 连盒清理与字号提权规范" in layout_rules_text
    assert "## 二、图片载体（海报 / 信息图 / 截图式 PPT）清理与重绘规范" in layout_rules_text
    assert "## 三、网站与前端页面（HTML / React / Vue / Tailwind）降噪与提权规范" in layout_rules_text
    assert "## 四、文档载体（Word .docx / Markdown）脱壳清理与提权规范" in layout_rules_text
    assert "## 五、各载体真假小字与角标处理决策速查表" in layout_rules_text
    
    # Section I checks
    assert "0.75" in layout_rules_text or "IoA" in layout_rules_text
    assert "paired_bg_shape_id" in layout_rules_text
    assert "delete_shape_ids" in layout_rules_text
    assert "is_protected_domain_footnote" in layout_rules_text
    
    # Section II checks
    assert "bbox" in layout_rules_text
    assert "erase_only" in layout_rules_text
    assert "erase_and_redraw" in layout_rules_text
    
    # Section III checks
    assert "rounded-full" in layout_rules_text
    assert "leading-snug" in layout_rules_text or "text-lg font-bold" in layout_rules_text
    
    # Section IV checks (Document)
    assert "Callout Box" in layout_rules_text or "Admonition" in layout_rules_text
    assert "Heading Hierarchy" in layout_rules_text or "标题层级" in layout_rules_text
    assert "Pull-Quote" in layout_rules_text or "重点金句" in layout_rules_text
    assert "w:footnote" in layout_rules_text or "Markdown 脚注" in layout_rules_text
    
    # Section V checks (Matrix)
    matrix_match = re.search(r"## 五、各载体真假小字与角标处理决策速查表.*?(\|[^\n]+\n\|[-| :]+\n(?:\|[^\n]+\n?)+)", layout_rules_text, re.DOTALL)
    assert matrix_match, "Section V table not found"
    matrix_rows = [line for line in matrix_match.group(1).strip().split("\n")[2:] if line.strip()]
    assert len(matrix_rows) >= 10, f"Carrier Decision Matrix has {len(matrix_rows)} rows, expected >= 10"


# ============================================================================
# 8. Markdown Formatting, Alignment & Syntax Integrity
# ============================================================================

def test_markdown_tables_column_alignment(playbook_text, dictionary_text, layout_rules_text):
    """
    Verify every markdown table in all 3 reference files has:
    - Consistent column count across header, separator, and data rows
    - No empty trailing lines or misaligned pipes
    """
    files = {
        "industry-playbooks-bilingual.md": playbook_text,
        "ai-slop-dictionary.md": dictionary_text,
        "layout-promotion-rules.md": layout_rules_text,
    }
    
    for filename, text in files.items():
        lines = text.splitlines()
        in_table = False
        table_rows = []
        
        for line_no, line in enumerate(lines, 1):
            stripped = line.strip()
            if stripped.startswith("|") and stripped.endswith("|"):
                in_table = True
                table_rows.append((line_no, stripped))
            else:
                if in_table and len(table_rows) >= 2:
                    # Validate collected table
                    expected_cols = len(table_rows[0][1].split("|")) - 2
                    for r_no, r_text in table_rows:
                        cols = len(r_text.split("|")) - 2
                        assert cols == expected_cols, (
                            f"{filename}:{r_no} Table column mismatch! Expected {expected_cols}, got {cols}. Row: {r_text}"
                        )
                    table_rows = []
                    in_table = False
                elif in_table:
                    table_rows = []
                    in_table = False
                    
        # If file ends with table
        if in_table and len(table_rows) >= 2:
            expected_cols = len(table_rows[0][1].split("|")) - 2
            for r_no, r_text in table_rows:
                cols = len(r_text.split("|")) - 2
                assert cols == expected_cols, (
                    f"{filename}:{r_no} Table column mismatch! Expected {expected_cols}, got {cols}."
                )


def test_markdown_links_and_fences(playbook_text, dictionary_text, layout_rules_text):
    """
    Verify markdown link targets and code block fences:
    - All local markdown links target existing files
    - All code blocks (```) are properly paired/closed
    """
    files = {
        "industry-playbooks-bilingual.md": (PLAYBOOK_PATH, playbook_text),
        "ai-slop-dictionary.md": (DICTIONARY_PATH, dictionary_text),
        "layout-promotion-rules.md": (LAYOUT_RULES_PATH, layout_rules_text),
    }
    
    for filename, (filepath, text) in files.items():
        # Check code fence balance
        fence_count = len(re.findall(r"^```", text, re.MULTILINE))
        assert fence_count % 2 == 0, f"{filename} has unbalanced code fences (count={fence_count})"
        
        # Check relative markdown links
        links = re.findall(r"\[([^\]]+)\]\(([^)]+)\)", text)
        for link_text, target in links:
            if target.startswith("http://") or target.startswith("https://") or target.startswith("#"):
                continue
            # Strip anchors e.g. ./file.md#anchor
            target_path_clean = target.split("#")[0]
            if not target_path_clean:
                continue
            resolved = (filepath.parent / target_path_clean).resolve()
            assert resolved.exists(), f"{filename} contains broken link: [{link_text}]({target}) -> {resolved}"


# ============================================================================
# 9. Protected Footnote Classification Integration Tests
# ============================================================================

def test_protected_domain_footnotes_accuracy():
    """
    Empirical test: feed authentic footnotes from Industry Playbooks Section A
    into scripts.industry_classifier.is_protected_domain_footnote() to verify
    they are correctly recognized as protected (True).
    Also verify fake AI footers are rejected (False).
    """
    authentic_samples = [
        # Industry 1 (Tech / SaaS / AI) - arXiv standard
        "* 算法来源：自研微调模型权重及开源对齐数据集详见 arXiv:2405.12345v2 [cs.CL]",
        # Industry 2 (Manufacturing & Engineering) - GB/T, ISO, IEC, PLC
        "* 零件加工公差严格按 GB/T 1184-K 与 GB/T 1804-m 级执行，关键轴承位配合公差控制在 H7/js6",
        "* Machining tolerances comply with ISO 2768-mK; critical bearing fits held to ISO H7/js6.",
        "* 安全控制回路符合 ISO 13849-1 Cat.4 PLe 认证要求，急停响应时间 < 20ms",
        "* Controller: Siemens S7-1500 CPU 1516-3 PN/DP communicating over Profinet with 1.0ms isochronous bus cycle.",
        # Industry 3 (Education & Academia) - NSFC
        "* 基金资助：国家自然科学基金重点项目（项目批准号：62332001）",
        # Industry 4 (Finance & FinTech) - Non-GAAP, SEC 10-K, EBITDA
        "* 财务指标口径依据 Non-GAAP 准则调整，剔除股权激励与一次性资产重组损益（完整调节表详见 SEC Form 10-K 附注 14）",
        "* Financial metrics adjusted per Non-GAAP measures; EBITDA excludes share-based compensation per SEC Form 10-K Note 14.",
        # Industry 5 (Healthcare & Biotech) - RCT, p < 0.001, FDA 510(k), NMPA, CE Mark
        "* 临床试验终点依据 RECIST 1.1 标准判定，双盲随机对照（RCT, n=428），无进展生存期风险比 HR=0.62 (95% CI [0.49, 0.78], p < 0.001)",
        "* Primary endpoint per RECIST 1.1 in double-blind RCT (n=428); progression-free survival HR=0.62 (95% CI [0.49, 0.78], p < 0.001).",
        "* 医疗器械注册备案：符合国家药监局《第三类医疗器械注册审查指导原则》，国械注准 2025xxxxxxx",
        "* Regulatory compliance: FDA 510(k) cleared under Premarket Notification K241890; CE Mark per MDR (EU) 2017/745.",
        # Industry 8 (Architecture & Design) - GB 50016
        "* 消防设计严格遵照《建筑设计防火规范》(GB 50016-2014, 2018年版) 第 5.4.10 条执行",
        # Industry 9 (Clean Energy & ESG) - ISO 14064, Scope 1/2, tCO2e
        "* 温室气体核算依据 ISO 14064-1:2018 标准，范围一与范围二排放经通标技术 (SGS) 第三方独立鉴证，碳减排量共计 14,250 tCO2e",
        "* Carbon accounting complies with ISO 14064-1:2018; Scope 1 and Scope 2 verified by independent third-party auditor SGS (14,250 tCO2e reduced).",
    ]
    
    fake_ai_samples = [
        "注：以上数据仅为演示参考，具体以实际运行为准",
        "Generated by AI for layout demonstration purposes only.",
        "本页核心洞察：通过全链路协同实现高质量发展的闭环",
        "Key Takeaway: Empowering seamless digital transformation across all touchpoints",
        "SYSTEM STATUS: ONLINE | LATENCY 12MS",
        "+99.8% AI SYNERGY",
        "仅供内部交流参考，版权所有未经授权不得扩散",
    ]
    
    for sample in authentic_samples:
        is_prot = is_protected_domain_footnote(sample)
        assert is_prot is True, f"Failed to protect authentic footnote: {sample}"
        
    for sample in fake_ai_samples:
        is_prot = is_protected_domain_footnote(sample)
        assert is_prot is False, f"False positive! Fake AI sample was protected: {sample}"


def test_carrier_smoke_suite():
    """Verify that carrier smoke test suite runs without errors."""
    import subprocess
    cmd = [sys.executable, str(REPO_ROOT / "scripts" / "test_smoke.py")]
    res = subprocess.run(cmd, capture_output=True, text=True, cwd=str(REPO_ROOT))
    assert res.returncode == 0, f"Smoke test failed:\n{res.stdout}\n{res.stderr}"
    assert "ALL 4 CARRIER SMOKE TESTS PASSED SUCCESSFULLY" in res.stdout
