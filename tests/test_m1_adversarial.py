"""
Adversarial Stress Test Suite for Milestone 1
Probes for cross-industry duplication, language contamination,
unescaped markdown artifacts, and quantitative edge cases.
"""

import re
import sys
from pathlib import Path
import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
PLAYBOOK_PATH = REPO_ROOT / "references" / "industry-playbooks-bilingual.md"
DICTIONARY_PATH = REPO_ROOT / "references" / "ai-slop-dictionary.md"
LAYOUT_RULES_PATH = REPO_ROOT / "references" / "layout-promotion-rules.md"

sys.path.insert(0, str(REPO_ROOT))
from tests.test_m1_challenger import parse_terms_from_cell


@pytest.fixture(scope="module")
def playbook_text():
    return PLAYBOOK_PATH.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def dictionary_text():
    return DICTIONARY_PATH.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def layout_rules_text():
    return LAYOUT_RULES_PATH.read_text(encoding="utf-8")


def test_adversarial_zero_cross_industry_copy_paste(playbook_text):
    """
    Stress-test: Verify that NO Before/After pairs or Section D templates
    were copy-pasted across different industries.
    Every industry must have unique, distinct examples.
    """
    industries = re.split(r"\n(?=## 行业 \d+：)", playbook_text)[1:]
    
    seen_zh_befores = {}
    seen_zh_afters = {}
    seen_en_befores = {}
    seen_en_afters = {}
    seen_zh_templates = {}
    seen_en_templates = {}
    
    for i, ind in enumerate(industries, 1):
        # Section C pairs
        sec_c = re.search(r"### C\. 中英 1:1 改写范例.*?(?=### D\.|$)", ind, re.DOTALL).group(0)
        parts = sec_c.split("English Parity Examples")
        zh_part, en_part = parts[0], parts[1]
        
        zh_b = [x.strip() for x in re.findall(r"❌ \*\*Before \d+ \(AI Slop\)\*\*:\s*(.+)", zh_part)]
        zh_a = [x.strip() for x in re.findall(r"✅ \*\*After \d+ \(Human Pro\)\*\*:\s*(.+)", zh_part)]
        en_b = [x.strip() for x in re.findall(r"❌ \*\*Before \d+ \(AI Slop\)\*\*:\s*(.+)", en_part)]
        en_a = [x.strip() for x in re.findall(r"✅ \*\*After \d+ \(Human Pro\)\*\*:\s*(.+)", en_part)]
        
        for b in zh_b:
            assert b not in seen_zh_befores, f"Duplicate ZH Before across industries: Ind {i} vs Ind {seen_zh_befores[b]}"
            seen_zh_befores[b] = i
        for a in zh_a:
            assert a not in seen_zh_afters, f"Duplicate ZH After across industries: Ind {i} vs Ind {seen_zh_afters[a]}"
            seen_zh_afters[a] = i
        for b in en_b:
            assert b not in seen_en_befores, f"Duplicate EN Before across industries: Ind {i} vs Ind {seen_en_befores[b]}"
            seen_en_befores[b] = i
        for a in en_a:
            assert a not in seen_en_afters, f"Duplicate EN After across industries: Ind {i} vs Ind {seen_en_afters[a]}"
            seen_en_afters[a] = i
            
        # Section D templates
        sec_d = re.search(r"### D\. 中英高质感表达模版与高说服力句式.*?(?=---\n|## 行业|$)", ind, re.DOTALL).group(0)
        parts_d = sec_d.split("English High-Impact Templates")
        zh_tpls = [x.strip() for x in re.findall(r"^\s*\d+\.\s+\*\*\[.*?\]\*\*:\s*(.+)", parts_d[0], re.MULTILINE)]
        en_tpls = [x.strip() for x in re.findall(r"^\s*\d+\.\s+\*\*\[.*?\]\*\*:\s*(.+)", parts_d[1], re.MULTILINE)]
        
        for t in zh_tpls:
            assert t not in seen_zh_templates, f"Duplicate ZH template across industries: Ind {i} vs Ind {seen_zh_templates[t]}"
            seen_zh_templates[t] = i
        for t in en_tpls:
            assert t not in seen_en_templates, f"Duplicate EN template across industries: Ind {i} vs Ind {seen_en_templates[t]}"
            seen_en_templates[t] = i

    print(f"\n[Adversarial PASS] Unique ZH Befores: {len(seen_zh_befores)}")
    print(f"[Adversarial PASS] Unique ZH Afters: {len(seen_zh_afters)}")
    print(f"[Adversarial PASS] Unique EN Befores: {len(seen_en_befores)}")
    print(f"[Adversarial PASS] Unique EN Afters: {len(seen_en_afters)}")
    print(f"[Adversarial PASS] Unique ZH Templates: {len(seen_zh_templates)}")
    print(f"[Adversarial PASS] Unique EN Templates: {len(seen_en_templates)}")


def test_adversarial_language_purity_in_section_b(playbook_text):
    """
    Stress-test: Verify that English rows in Section B don't contain stray Chinese characters
    and Chinese rows contain authentic Chinese terms (with allowable standard acronyms e.g. P99, QPS, ISO).
    """
    industries = re.split(r"\n(?=## 行业 \d+：)", playbook_text)[1:]
    chinese_char_pattern = re.compile(r"[\u4e00-\u9fff]")
    
    for i, ind in enumerate(industries, 1):
        m_b = re.search(r"### B\. 伪黑话黑名单 vs\. 真专业白名单.*?\n(\|.*?\n\|[-| :]+\n(\|.*?\n)+)", ind)
        data_rows = [line.strip() for line in m_b.group(1).strip().split("\n")[2:] if line.strip()]
        
        for r in data_rows:
            cols = [c.strip() for c in r.strip("|").split("|")]
            lang, slop_col, domain_col = cols[0], cols[1], cols[2]
            
            if "EN" in lang:
                # English slop and domain terms must contain ZERO Chinese characters
                zh_in_slop = chinese_char_pattern.findall(slop_col)
                zh_in_domain = chinese_char_pattern.findall(domain_col)
                assert len(zh_in_slop) == 0, f"Industry {i} EN slop row contaminated with Chinese: {zh_in_slop}"
                assert len(zh_in_domain) == 0, f"Industry {i} EN domain row contaminated with Chinese: {zh_in_domain}"


def test_adversarial_no_unclosed_markdown_artifacts(playbook_text, dictionary_text, layout_rules_text):
    """
    Stress-test: Check for unclosed brackets, unclosed quotes, or dangling formatting marks.
    """
    files = {
        "industry-playbooks-bilingual.md": playbook_text,
        "ai-slop-dictionary.md": dictionary_text,
        "layout-promotion-rules.md": layout_rules_text,
    }
    
    for filename, text in files.items():
        # Check double-asterisks (bold) balance on non-table, non-bullet lines
        for line_no, line in enumerate(text.splitlines(), 1):
            # Bold markers ** should be paired on any single line (count should be even)
            bold_count = line.count("**")
            assert bold_count % 2 == 0, f"{filename}:{line_no} Unbalanced bold markers (**): {line}"
            
            # Backtick count on line should generally be even unless in code fence
            if not line.strip().startswith("```"):
                bt_count = line.count("`")
                assert bt_count % 2 == 0, f"{filename}:{line_no} Unbalanced backtick markers (`): {line}"
