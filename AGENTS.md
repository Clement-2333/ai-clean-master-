# AGENTS.md — AI Clean Master (`ai-clean-master`)

This repository provides **`ai-clean-master`**, a cross-agent skill and Python engine for cleaning up AI-generated micro-copy ("AI-slop small text" / AI 味小字), removing decorative pill badges & footer disclaimers **box-and-text together** (连盒带字清除), visually promoting retained core copy (智能字号提权), and rewriting robotic buzzwords into authentic human language (人味化改写) across **10 major industries** with **1:1 Chinese and English parity**.

Supported carriers:
- **PPTX** (`.pptx` / SVG): Paired AutoShape container deletion ($\text{IoA} \ge 0.75$, $H \le 2.8\times$), +2pt~+4pt bold font promotion, vertical centering.
- **Web UI** (`.html` / `.jsx` / `.tsx` / `.vue` / Tailwind): Outer pill badge DOM removal, redundant subtext deletion, headline class promotion (`text-base` $\rightarrow$ `text-lg font-bold`), emoji and slop glow purging.
- **Images/Posters** (`.png` / `.jpg` / `.webp`): Median border ring inpainting, bilinear gradient fill, high-contrast CJK bold redraw (+35%~60% font size), footnote erase-mask exclusion.
- **Documents** (`.docx` / `.md`): Colored callout box unboxing, heading prefix stripping, pull-quote single-border styling, native footnote preservation (`w:footnote`, `[^1]`).

---

## Mandatory 5-Stage Workflow

Whenever triggered, follow [`SKILL.md`](./SKILL.md) strictly:

### 1. Stage 1 (Scan & Automated Industry Classification)
- Automatically classify the industry context and primary language (`zh`, `en`, `bilingual`) using `scripts/industry_classifier.py`:
  - 10 Industry IDs: `tech_saas_ai`, `industrial_manufacturing`, `education_academia`, `finance_consulting`, `healthcare_biotech`, `retail_marketing`, `public_gov_smartcity`, `architecture_design`, `energy_sustainability_agtech`, `media_gaming_hospitality`.
- Run the carrier-specific scanner:
  - PPTX: `python scripts/pptx_inspector.py "<input.pptx>"`
  - Web: `python scripts/web_cleaner.py --scan "<input>"`
  - Image: `python scripts/image_cleaner.py --scan "<input>"`
  - Docs: `python scripts/doc_cleaner.py --scan "<input>"`

### 2. Stage 2 (`Grill-Me` One-by-One Alignment)
Interview the user **one question at a time** (using IDE interaction tools `ask_question`/`AskUserQuestion` or numbered single-question prompts), always placing the `(Recommended)` option first:
- **Q1 (Industry & Tone)**: Recommend the auto-detected industry from [`references/industry-playbooks-bilingual.md`](./references/industry-playbooks-bilingual.md) as Option 1 (`1. (Recommended: Auto-detected) ...`), and provide the 10-industry selection list.
- **Q2 (Cleanup Aggressiveness)**: `1. (Recommended) Full box-and-text removal + typographic promotion (连盒全清 + 核心大字提权)`; `2. Moderate cleanup`.
- **Q3 (Footnote & Real Data Guard)**: Enforce the Statutory Footnote Protection Iron Rule.

### 3. Stage 3 (Preview & Confirmation Gate)
Output a structured `Before → After` comparison table displaying deletions, humanized rewrites, protected footnotes, and font promotions. **Wait for explicit user confirmation before mutating files.**

### 4. Stage 4 (Execute Cleanup & Visual Promotion)
Execute the plan using `pptx_cleaner.py`, `web_cleaner.py --apply`, `image_cleaner.py --apply`, or `doc_cleaner.py --apply` following [`references/layout-promotion-rules.md`](./references/layout-promotion-rules.md).
- **Non-Destructive Output Contract**: Always write to `<name>_cleaned.<ext>` — never overwrite original files.

### 5. Stage 5 (Delivery Report)
Present the output file link and summary statistics (boxes removed, buzzwords rewritten, footnotes preserved, font promotions applied).

---

## Statutory Footnote Protection Iron Rule
Call `is_protected_domain_footnote(text)` from `scripts/industry_classifier.py` before classifying any footer or micro-copy:
- **🛡️ ABSOLUTE RETENTION (Never Delete)**:
  - Clinical / Medical: `p < 0.05`, `95% CI`, `n=120`, `FDA 510(k)`, `NMPA`, `国械注准`, `国药准字`, `Phase I-IV`.
  - Financial / Audit: `Non-GAAP`, `GAAP`, `EBITDA`, `SEC Form 10-K`, `CAGR`, `bps`, `经审计`.
  - Engineering / Standards: `ISO 9001/14064`, `GB/T`, `IEC`, `IEEE`, `ASTM`, `P99 latency`, `SLA 99.95%`.
  - ESG / Sustainability: `Scope 1/2/3`, `tCO2e`, `LCOE`, `carbon footprint`.
  - Academic / IP: `arXiv`, peer-reviewed citations, `UE5`, `4K@60fps`, `Copyright ©`.
  *(Action: Strip decorative pill background containers, retain clean text, restyle to 8~9pt Slate `#64748B` at page bottom).*
- **🗑️ MANDATORY DELETION (Delete Box & Text)**:
  - Generic AI placeholders: `仅供演示参考`, `for demonstration purposes only`, `虚拟数据`, `AI-generated placeholder`.

---

## Key Reference Index
- [`SKILL.md`](./SKILL.md) — Main entry point & 5-stage orchestration protocol.
- [`references/industry-playbooks-bilingual.md`](./references/industry-playbooks-bilingual.md) — 10-industry bilingual slop blacklists, authentic domain whitelists, and rewrite templates.
- [`references/ai-slop-dictionary.md`](./references/ai-slop-dictionary.md) — High-frequency Chinese and English AI buzzwords.
- [`references/layout-promotion-rules.md`](./references/layout-promotion-rules.md) — Container box removal, typographic promotion, and carrier decision matrices.
- [`scripts/industry_classifier.py`](./scripts/industry_classifier.py) — 10-industry bilingual classifier and footnote guard.
