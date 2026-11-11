"""
Milestone 3 Bilingual Parity & Structural Stress Test Suite
Challenger 2 Empirical Verification:
1. Row-by-Row 10-Industry Parity: README.md vs README_EN.md vs references/industry-playbooks-bilingual.md
2. Mermaid Structural Validation: Syntax, Node Symmetry, Edge Symmetry, Label Parity
3. Carrier Engines Section 4 Parity: Subsections 0-4, CLI flags, explanations, code blocks
4. Statutory Footnotes Protection Empirical Verification
5. Execution of Documented Code Snippets
"""

import os
import sys
import re
import json
import pytest

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

README_ZH = os.path.join(REPO_ROOT, "README.md")
README_EN = os.path.join(REPO_ROOT, "README_EN.md")
PLAYBOOKS = os.path.join(REPO_ROOT, "references", "industry-playbooks-bilingual.md")

EXPECTED_INDUSTRIES = [
    "tech_saas_ai",
    "industrial_manufacturing",
    "education_academia",
    "finance_consulting",
    "healthcare_biotech",
    "retail_marketing",
    "public_gov_smartcity",
    "architecture_design",
    "energy_sustainability_agtech",
    "media_gaming_hospitality"
]


def parse_markdown_table(file_path: str, header_marker: str):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    idx = content.find(header_marker)
    assert idx != -1, f"Marker '{header_marker}' not found in {file_path}"
    sub = content[idx:]

    table_lines = []
    in_table = False
    for line in sub.splitlines():
        line = line.strip()
        if line.startswith("|") and line.endswith("|"):
            table_lines.append(line)
            in_table = True
        elif in_table:
            break

    assert len(table_lines) >= 3, f"Table too short in {file_path}: {len(table_lines)} lines"
    headers = [c.strip() for c in table_lines[0].strip("|").split("|")]
    rows = []
    for line in table_lines[2:]:
        cols = [c.strip() for c in line.strip("|").split("|")]
        rows.append(cols)

    return headers, rows


def extract_mermaid_block(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    match = re.search(r"```mermaid\s*\n(.*?)\n```", content, re.DOTALL)
    assert match is not None, f"Mermaid block not found in {file_path}"
    return match.group(1).strip()


# =========================================================================
# Part 1: 10-Industry Tables Row-by-Row 1:1 Parity
# =========================================================================

def test_10_industries_row_by_row_parity():
    """Verify that all 10 industries exist in exact order and match across README.md, README_EN.md, and playbooks."""
    zh_headers, zh_rows = parse_markdown_table(README_ZH, "## 五、10 大行业中英双语专业词库与合规防护矩阵")
    en_headers, en_rows = parse_markdown_table(README_EN, "## 5. 10 Major Industries Bilingual Matrix & Statutory Guard")

    assert len(zh_rows) == 10, f"Expected 10 rows in README.md, got {len(zh_rows)}"
    assert len(en_rows) == 10, f"Expected 10 rows in README_EN.md, got {len(en_rows)}"
    assert len(zh_headers) == 4, f"Expected 4 columns in README.md, got {len(zh_headers)}"
    assert len(en_headers) == 4, f"Expected 4 columns in README_EN.md, got {len(en_headers)}"

    # Check industry classifier knowledge base
    import scripts.industry_classifier as ic
    supported = ic.get_supported_industries()
    assert supported == EXPECTED_INDUSTRIES, f"Classifier supported industries mismatch: {supported}"

    with open(PLAYBOOKS, "r", encoding="utf-8") as f:
        playbooks_content = f.read()

    playbook_industries = re.findall(r"## 行业 \d+：([^\n]+)", playbooks_content)
    assert len(playbook_industries) == 10, f"Playbook should define 10 industries, found {len(playbook_industries)}"

    # Expected statutory and regulatory anchors per industry
    industry_statutory_anchors = {
        0: {"zh": ["ISO/IEC 27001", "SOC2", "RFC 7519", "IEEE 802.3", "arXiv", "SLA"],
            "en": ["ISO/IEC 27001", "SOC2", "RFC 7519", "IEEE 802.3", "arXiv", "SLA"]},
        1: {"zh": ["GB/T", "ISO 13849-1", "IEC 61131-3", "CE"],
            "en": ["ISO 2768", "ISO 13849-1", "IEC 61131-3", "CE"]},
        2: {"zh": ["自然科学基金", "重点研发计划", "NeurIPS", "p < 0.01"],
            "en": ["NSF", "NeurIPS", "p < 0.01"]},
        3: {"zh": ["GAAP", "Non-GAAP", "SEC Form", "10-K", "10-Q"],
            "en": ["GAAP", "Non-GAAP", "SEC Form", "10-K", "10-Q"]},
        4: {"zh": ["NMPA", "FDA", "510(k)", "PMA", "IRB", "95% CI", "p < 0.001"],
            "en": ["FDA", "510(k)", "PMA", "NMPA", "IRB", "95% CI", "p < 0.001"]},
        5: {"zh": ["广告法", "GB/T", "POS"],
            "en": ["FTC", "16 CFR", "POS"]},
        6: {"zh": ["条例", "GB/T 20988", "等保三级"],
            "en": ["APA", "NIST", "FedRAMP", "Section 508"]},
        7: {"zh": ["GB 50096", "GB 50016", "LEED", "BIM"],
            "en": ["IBC", "LEED", "WELL", "ASHRAE", "BIM"]},
        8: {"zh": ["ISO 14064", "GHG Protocol", "GB/T 19964"],
            "en": ["ISO 14064", "GHG Protocol", "Scope", "IEEE 1547"]},
        9: {"zh": ["版号", "DCI-P3", "© 2026"],
            "en": ["ESRB", "PEGI", "DCI-P3", "© 2026"]}
    }

    for i in range(10):
        expected_id = EXPECTED_INDUSTRIES[i]
        zh_row = zh_rows[i]
        en_row = en_rows[i]

        # Col 0: Industry ID & Name
        assert expected_id in zh_row[0], f"Row {i+1} in README.md missing '{expected_id}': {zh_row[0]}"
        assert expected_id in en_row[0], f"Row {i+1} in README_EN.md missing '{expected_id}': {en_row[0]}"

        # Col 1: Banned Buzzwords
        zh_slop = zh_row[1]
        en_slop = en_row[1]
        assert len(zh_slop) > 10, f"Row {i+1} ZH slop column is suspiciously short: {zh_slop}"
        assert len(en_slop) > 10, f"Row {i+1} EN slop column is suspiciously short: {en_slop}"

        # Col 2: Authentic Domain Terms
        zh_domain = zh_row[2]
        en_domain = en_row[2]
        assert len(zh_domain) > 10, f"Row {i+1} ZH domain column is suspiciously short: {zh_domain}"
        assert len(en_domain) > 10, f"Row {i+1} EN domain column is suspiciously short: {en_domain}"

        # Col 3: Statutory Standards
        zh_stat = zh_row[3]
        en_stat = en_row[3]
        assert len(zh_stat) > 10, f"Row {i+1} ZH statutory column is suspiciously short: {zh_stat}"
        assert len(en_stat) > 10, f"Row {i+1} EN statutory column is suspiciously short: {en_stat}"

        # Verify statutory anchors
        anchors = industry_statutory_anchors[i]
        zh_matched = [a for a in anchors["zh"] if a in zh_stat]
        en_matched = [a for a in anchors["en"] if a in en_stat]
        assert len(zh_matched) >= 1, f"Row {i+1} ZH statutory missing expected anchors: {zh_stat}"
        assert len(en_matched) >= 1, f"Row {i+1} EN statutory missing expected anchors: {en_stat}"


# =========================================================================
# Part 2: Mermaid Structural Validation & Parity
# =========================================================================

def parse_mermaid_flowchart(mermaid_code: str):
    """Parses a simple Mermaid flowchart TD to extract node ids, node shapes, and edges."""
    lines = [l.strip() for l in mermaid_code.splitlines() if l.strip()]
    assert lines[0] == "flowchart TD", f"Mermaid graph must start with 'flowchart TD', got '{lines[0]}'"

    nodes = {}
    edges = []

    for line in lines[1:]:
        # 1. Match node definitions like: A["text"] or B{"text"} or B1["text"]
        node_defs = re.findall(r'(\b[A-Za-z0-9_]+)\s*([\[\{])(["\']?.*?["\']?)[\]\}]', line)
        for nid, shape_open, label in node_defs:
            shape_type = "diamond" if shape_open == "{" else "rect"
            nodes[nid] = (shape_type, label)

        # 2. To cleanly extract edges, simplify the line by replacing node definitions with just node IDs
        # e.g., A["text"] -> A, B{"text"} -> B
        simplified = re.sub(r'(\b[A-Za-z0-9_]+)\s*[\[\{].*?[\]\}]', r'\1', line)

        # Match edges: X --> Y or X -- "label" --> Y
        edge_match = re.search(r'([A-Za-z0-9_& ]+)\s*(?:--\s*("[^"]*")\s*)?-->\s*([A-Za-z0-9_]+)', simplified)
        if edge_match:
            src_group = edge_match.group(1).strip()
            cond_label = edge_match.group(2)
            dst = edge_match.group(3).strip()
            srcs = [s.strip() for s in src_group.split("&")]
            for s in srcs:
                edges.append((s, dst, cond_label.strip('"') if cond_label else None))

    return nodes, edges


def test_mermaid_syntax_and_symmetry():
    """Verify that both Chinese and English Mermaid flowcharts are syntactically valid and 1:1 symmetric."""
    zh_mermaid = extract_mermaid_block(README_ZH)
    en_mermaid = extract_mermaid_block(README_EN)

    zh_nodes, zh_edges = parse_mermaid_flowchart(zh_mermaid)
    en_nodes, en_edges = parse_mermaid_flowchart(en_mermaid)

    expected_nodes = {"A", "B", "B1", "B2", "B3", "B4", "CLAS", "C", "D", "E", "F"}

    # 1. Node symmetry
    assert set(zh_nodes.keys()) == expected_nodes, f"ZH nodes mismatch: {set(zh_nodes.keys())}"
    assert set(en_nodes.keys()) == expected_nodes, f"EN nodes mismatch: {set(en_nodes.keys())}"

    # 2. Node shape symmetry
    for nid in expected_nodes:
        zh_shape, _ = zh_nodes[nid]
        en_shape, _ = en_nodes[nid]
        assert zh_shape == en_shape, f"Node {nid} shape mismatch: ZH is {zh_shape}, EN is {en_shape}"

    # 3. Decision node B must be a diamond in both
    assert zh_nodes["B"][0] == "diamond", "Node B in ZH must be diamond"
    assert en_nodes["B"][0] == "diamond", "Node B in EN must be diamond"

    # 4. Edge symmetry
    zh_edge_set = set(zh_edges)
    en_edge_set = set(en_edges)

    assert zh_edge_set == en_edge_set, f"Edge mismatch between ZH and EN:\nZH only: {zh_edge_set - en_edge_set}\nEN only: {en_edge_set - zh_edge_set}"

    # 5. Verify all carrier branches exist
    carrier_labels = {
        ("B", "B1"): ".pptx / SVG",
        ("B", "B2"): ".png / .jpg / .webp",
        ("B", "B3"): ".html / .jsx / .tsx / .vue",
        ("B", "B4"): ".docx / .md"
    }
    for (src, dst), expected_label in carrier_labels.items():
        assert (src, dst, expected_label) in zh_edges, f"Missing branch ({src} -> {dst}) with label '{expected_label}' in ZH"
        assert (src, dst, expected_label) in en_edges, f"Missing branch ({src} -> {dst}) with label '{expected_label}' in EN"

    # 6. Verify fan-in to CLAS and pipeline stages
    for b_node in ["B1", "B2", "B3", "B4"]:
        assert (b_node, "CLAS", None) in zh_edges
        assert (b_node, "CLAS", None) in en_edges

    pipeline = [("A", "B"), ("CLAS", "C"), ("C", "D"), ("D", "E"), ("E", "F")]
    for src, dst in pipeline:
        assert (src, dst, None) in zh_edges
        assert (src, dst, None) in en_edges


# =========================================================================
# Part 3: Carrier Engines Section 4 Parity
# =========================================================================

def extract_section_subsections(file_path: str, section_marker: str):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    idx = content.find(section_marker)
    assert idx != -1, f"Marker '{section_marker}' not found in {file_path}"
    sub = content[idx:]
    # Stop at next ## section
    end_idx = sub.find("\n## ")
    if end_idx != -1:
        sub = sub[:end_idx]

    # Split by ### N.
    subsections = re.findall(r"### (\d+)\.\s+([^\n]+)\n(.*?)(?=\n### \d+\.|\Z)", sub, re.DOTALL)
    result = {}
    for num, title, body in subsections:
        result[int(num)] = {
            "title": title.strip(),
            "body": body.strip(),
            "code_blocks": re.findall(r"```(?:bash|python)?\s*\n(.*?)\n```", body, re.DOTALL)
        }
    return result


def test_carrier_engines_section_parity():
    """Verify Section 4 parity between README.md and README_EN.md across subsections 0-4."""
    zh_subsections = extract_section_subsections(README_ZH, "## 四、四大载体专属清理引擎与自动化识别流程")
    en_subsections = extract_section_subsections(README_EN, "## 4. Four Carrier-Specific Engines & Automated Classification")

    expected_indices = [0, 1, 2, 3, 4]
    assert list(zh_subsections.keys()) == expected_indices, f"ZH subsection numbers mismatch: {list(zh_subsections.keys())}"
    assert list(en_subsections.keys()) == expected_indices, f"EN subsection numbers mismatch: {list(en_subsections.keys())}"

    # Subsection 0: Classifier
    for subs, lang in [(zh_subsections, "ZH"), (en_subsections, "EN")]:
        codes = subs[0]["code_blocks"]
        assert len(codes) >= 1, f"Missing code block in {lang} subsection 0"
        combined_code = "\n".join(codes)
        assert "detect_industry_and_language" in combined_code
        assert "is_protected_domain_footnote" in combined_code
        assert "industry_classifier.py" in subs[0]["title"]

    # Subsection 1: PPTX
    for subs, lang in [(zh_subsections, "ZH"), (en_subsections, "EN")]:
        codes = subs[1]["code_blocks"]
        assert len(codes) >= 1, f"Missing code block in {lang} subsection 1"
        combined_code = "\n".join(codes)
        assert "pptx_inspector.py" in combined_code
        assert "pptx_cleaner.py" in combined_code
        assert "--industry" in combined_code
        assert "--json" in combined_code
        assert "-o" in combined_code

    # Subsection 2: Web
    for subs, lang in [(zh_subsections, "ZH"), (en_subsections, "EN")]:
        codes = subs[2]["code_blocks"]
        assert len(codes) >= 1, f"Missing code block in {lang} subsection 2"
        combined_code = "\n".join(codes)
        assert "web_cleaner.py" in combined_code
        assert "--scan" in combined_code
        assert "--apply" in combined_code
        assert "-o" in combined_code

    # Subsection 3: Image
    for subs, lang in [(zh_subsections, "ZH"), (en_subsections, "EN")]:
        codes = subs[3]["code_blocks"]
        assert len(codes) >= 1, f"Missing code block in {lang} subsection 3"
        combined_code = "\n".join(codes)
        assert "image_cleaner.py" in combined_code
        assert "--apply" in combined_code
        assert "-o" in combined_code

    # Subsection 4: Doc
    for subs, lang in [(zh_subsections, "ZH"), (en_subsections, "EN")]:
        codes = subs[4]["code_blocks"]
        assert len(codes) >= 1, f"Missing code block in {lang} subsection 4"
        combined_code = "\n".join(codes)
        assert "doc_cleaner.py" in combined_code
        assert "--scan" in combined_code
        assert "--apply" in combined_code
        assert "-o" in combined_code


# =========================================================================
# Part 4: Statutory Footnotes Protection Empirical Verification
# =========================================================================

def test_statutory_footnotes_protection():
    """Verify that authentic statutory footnotes across all domains are recognized as protected."""
    import scripts.industry_classifier as ic

    authentic_samples = [
        "* FDA 510(k) Cleared, p < 0.01, n=120",
        "* Non-GAAP EBITDA per SEC Form 10-K",
        "* ISO 9001:2015 and GB/T 1804-m",
        "* Scope 1+2 emissions: 42.5 tCO2e, LCOE $0.038",
        "* arXiv:2405.12345 [cs.CL]",
        "* 测试环境：P99 延迟 < 18ms",
        "* 国械注准 20243401234 号，临床试验 n=1,280",
        "* 经审计财务报表：CAGR 34%，YoY +28%",
        "* © 2026 Studio Inc. All rights reserved. 4K@60fps"
    ]
    for auth in authentic_samples:
        assert ic.is_protected_domain_footnote(auth) is True, f"Authentic footnote falsely classified as slop: {auth}"

    fake_samples = [
        "* 注：以上数据仅供演示参考，实际以交付为准。",
        "* Note: Data generated for illustrative layout purposes only.",
        "* 仅供演示参考：EBITDA 提升 20%",
        "* Disclaimer: All metrics shown are placeholders.",
        "Key Takeaway: Empowering digital transformation.",
        "本页核心洞察：通过多维抓手实现全链路闭环"
    ]
    for fake in fake_samples:
        assert ic.is_protected_domain_footnote(fake) is False, f"Fake disclaimer incorrectly marked protected: {fake}"


# =========================================================================
# Part 5: Empirical Execution of README Code Snippets
# =========================================================================

def test_readme_code_snippets_execution():
    """Verify that Python one-liners documented in README.md Section 4.0 run cleanly."""
    import scripts.industry_classifier as ic

    # Snippet 1: detect_industry_and_language
    res = ic.detect_industry_and_language('P99 latency sub-20ms under high QPS load with zero-copy Kafka buffer')
    assert res["language"] == "en"
    assert res["industry_id"] == "tech_saas_ai"
    assert "latency" in res["matched_domain_terms"] or "zero-copy" in res["matched_domain_terms"]

    # Snippet 2: is_protected_domain_footnote
    is_prot = ic.is_protected_domain_footnote('* SOC2 Type II Certified (FY2025); P99 latency < 18ms')
    assert is_prot is True
