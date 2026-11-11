# CLAUDE.md — AI Clean Master (`ai-clean-master`)

This repository provides **`ai-clean-master`**, an all-carrier skill and Python toolkit for removing AI-generated micro-copy and decorative containers (连盒带字删除), visually promoting retained core content (智能字号提权), and rewriting buzzwords into authentic professional copy across **10 major industries** in **1:1 Chinese and English**.

Supported carriers: **PPTX** (`.pptx`/SVG), **Web** (`.html`/`.jsx`/`.tsx`/`.vue`), **Images** (`.png`/`.jpg`), and **Documents** (`.docx`/`.md`).

See [`SKILL.md`](./SKILL.md), [`AGENTS.md`](./AGENTS.md), and [`references/industry-playbooks-bilingual.md`](./references/industry-playbooks-bilingual.md) for full specifications.

---

## Quick Commands

### 1. 10-Industry & Bilingual Classification
- Programmatically classify industry context and language:
  ```bash
  python -c "from scripts.industry_classifier import detect_industry_and_language; import json; print(json.dumps(detect_industry_and_language('Your text here'), ensure_ascii=False, indent=2))"
  ```
- Verify protected footnote vs. fake disclaimer:
  ```bash
  python -c "from scripts.industry_classifier import is_protected_domain_footnote; print(is_protected_domain_footnote('FDA 510(k) cleared; n=120, p<0.01')); print(is_protected_domain_footnote('注：以上数据仅供演示参考'))"
  ```

### 2. Carrier Scanning & Cleaning
- **PPTX**:
  ```bash
  python scripts/pptx_inspector.py "<input.pptx>" --json "<scan.json>"
  python scripts/pptx_cleaner.py "<input.pptx>" "<plan.json>" -o "<output_cleaned.pptx>"
  ```
- **Web UI**:
  ```bash
  python scripts/web_cleaner.py --scan "<input.html>" --json "<scan.json>"
  python scripts/web_cleaner.py --apply "<plan.json>" "<input.html>" -o "<output_cleaned.html>"
  ```
- **Images/Posters**:
  ```bash
  python scripts/image_cleaner.py --scan "<input.png>"
  python scripts/image_cleaner.py --apply "<plan.json>" "<input.png>" -o "<output_cleaned.png>"
  ```
- **Documents (.docx / .md)**:
  ```bash
  python scripts/doc_cleaner.py --scan "<input.docx>" --json "<scan.json>"
  python scripts/doc_cleaner.py --apply "<plan.json>" "<input.docx>" -o "<output_cleaned.docx>"
  ```

### 3. Verification & Multi-Agent Installation
- Run complete 4-carrier smoke test suite:
  ```bash
  python scripts/test_smoke.py
  ```
- Install skill across all 8 supported AI agents (Antigravity, Claude Code, Codex, Cursor, WorkBuddy, Qoder, Trae, Doubao):
  ```bash
  python scripts/install_skill.py --agent all --scope global
  ```

---

## Core Operating Principles

1. **Mandatory 5-Stage Flow**: Scan & Classify $\rightarrow$ `grill-me` One-by-One Alignment $\rightarrow$ `Before → After` Confirmation Gate $\rightarrow$ Execute Cleanup & Typographic Promotion $\rightarrow$ Delivery.
2. **10-Industry Alignment**: Map tones and vocabulary to [`references/industry-playbooks-bilingual.md`](./references/industry-playbooks-bilingual.md) across all 10 industries in 1:1 Chinese and English.
3. **Statutory Footnote Guard**: Call `is_protected_domain_footnote`. Strictly protect clinical (`FDA`, `p < 0.05`), financial (`GAAP`, `EBITDA`, `10-K`), engineering (`ISO`, `GB/T`, `IEC`, `IEEE`), ESG (`Scope 1/2/3`, `tCO2e`), and academic citations. Never confuse them with fake AI demo disclaimers (`仅供演示参考`).
4. **Layout Promotion**: Strip container boxes (AutoShapes, pill `<span>` badges, shaded callouts). Promote headline font size (+2pt~+4pt / `text-lg font-bold`), add breathing room, and center vertically per [`references/layout-promotion-rules.md`](./references/layout-promotion-rules.md).
5. **Non-Destructive Guarantee**: Never overwrite the source file. Always write output to `<name>_cleaned.<ext>`.
