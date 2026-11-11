<div align="center">

# 🧹 AI Clean Master (`ai-clean-master`)

**All-Carrier AI-Slop Micro-Copy Cleaner, Box-and-Text Remover, Visual Promoter & Copy Humanizer Skill**  
*Works across **PPTX (`.pptx` / SVG)** · **Images (Posters / Infographics / Slide Captures)** · **Web UI (HTML / React / Vue / Tailwind)** · **Documents (`.docx` / Markdown)***

[**简体中文**](./README.md) | [**English**](./README_EN.md)

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Carriers](https://img.shields.io/badge/Carriers-PPTX_%7C_Image_%7C_Web_%7C_Docx-success.svg)](#4-four-carrier-specific-engines)
[![Agents](https://img.shields.io/badge/Agents-Claude_Code_%7C_Codex_%7C_Antigravity_%7C_Cursor_%7C_WorkBuddy_%7C_Qoder_%7C_Trae_%7C_Doubao-orange.svg)](#3-multi-agent-installation--adaptation-guide)

</div>

---

## 1. Why `ai-clean-master`?

Whether you generate **PowerPoint decks (`.pptx`)**, **infographic posters (`.png`/`.jpg`)**, **landing pages / web prototypes (`.html`/`.tsx`/`.vue`)**, or **Word/Markdown documents** with AI, the output almost always suffers from unmistakable **"AI Slop"**:

1. **Cluttered, Zero-Information "AI Micro-Copy" & Decorative Pill Boxes**:
   - **Pseudo-English Kickers & Pill Badges**: Every heading has a glowing pill badge above it (`SECTION 01 · STRATEGIC OVERVIEW`, `✨ Next-Gen AI Platform`, `CORE INSIGHT`, `SYSTEM ONLINE`, `01 // FEATURE MATRIX`);
   - **Redundant Card Subtext**: A card title already states `"3x Faster Defect Detection"`, yet AI pads the bottom of the card with two lines of `10pt` / `text-xs` filler repeating the exact same idea in passive voice;
   - **Fake Footer Takeaways & Disclaimers**: Bottom banners stuffed with `"Key Takeaway: Empowering end-to-end digital transformation"` or `"Note: Data shown is for demonstration purposes only"`;
   - **Fabricated Micro-Metrics & Emoji Spam**: Ungrounded `+99.8% EFFICIENCY` corner tags and endless `✨🚀💡⚡` emojis.
2. **Robotic Buzzwords (Chinese & English)**:
   - English clichés: `delve into`, `testament to`, `rich tapestry`, `paradigm shift`, `holistic ecosystem`, `synergy`, `empowering`, `cutting-edge`, `game-changer`.
   - Chinese clichés: `赋能 (empower)`, `抓手 (lever)`, `闭环 (closed-loop)`, `全链路 (full-link)`, `底层逻辑 (underlying logic)`, `顶层设计 (top-level design)`.
3. **Text-Only Deletion Breaks Layouts**:
   - Simply deleting text leaves ugly empty colored pill shapes and footer bars floating on your slide or poster, and leaves cards looking half-empty.

---

## 2. Core Capabilities

- 🗑️ **Box-and-Text Removal (连盒带字一起清)**  
  Automatically pairs decorative micro-copy with its underlying background shape (`paired_bg_shape_id` via bounding-box IoA in `.pptx`, DOM badge wrappers in HTML/JSX, or border-ring pixel sampling in raster images) and deletes **both the text and its decorative box**.
- 🔼 **Smart Visual Promotion (智能视觉提权)**  
  After stripping redundant subtext inside a card, automatically promotes the remaining core point's font size (e.g., `+2pt to +4pt` in PPTX, `text-base → text-lg font-semibold` in Tailwind/CSS) and vertically centers it so the layout feels bold and balanced.
- 🗣️ **Bilingual De-Buzzword Baseline + Adaptive Human Tone (人味化改写)**  
  Replaces robotic buzzwords with natural, spoken-style copy tailored to 4 scenarios: **Pitch / Competition**, **Engineering / Technical Review**, **Classroom / Speech**, and **Crisp Business Report**.
- 🤝 **Built-in `grill-me` One-by-One Alignment & Confirmation Gate**  
  Interviews you **one question at a time** (with a `(Recommended)` first option) to align on tone, cleanup aggressiveness, and borderline real metrics, then presents a `Before → After` preview table for approval before outputting `<name>_cleaned.<ext>` (never overwrites original files).

---

## 3. Multi-Agent Installation & Adaptation Guide

### 0. Clone & Install Dependencies

```bash
# Via GitHub CLI
gh repo clone Clement-2333/ai-clean-master-
# Or via Git
git clone https://github.com/Clement-2333/ai-clean-master-.git
cd ai-clean-master-

# Install Python dependencies
pip install python-pptx python-docx Pillow numpy
```

### 1. One-Click Cross-Agent Installer (Recommended)

Use [`scripts/install_skill.py`](./scripts/install_skill.py) to install `ai-clean-master` across all mainstream AI coding agents in one command:

```bash
# Install globally for all supported AI agents + build Doubao Workspace zip bundle
python scripts/install_skill.py --agent all --scope global

# Install for specific agents (comma-separated)
python scripts/install_skill.py --agent antigravity,claude,codex,cursor,workbuddy,qoder,trae,doubao --scope global

# Install into a specific project workspace (auto-generates .cursor/rules, .trae/rules, .qoder/rules)
python scripts/install_skill.py --agent all --scope workspace --workspace-dir /path/to/your/project
```

### 2. Supported AI Agents Matrix

| AI Agent Tool | Global Skill Path | Workspace Path & Rule Adapter |
|---|---|---|
| **Google Antigravity** | `~/.gemini/config/skills/ai-clean-master` | `<project>/.agents/skills/ai-clean-master` |
| **Claude Code** | `~/.claude/skills/ai-clean-master` | `<project>/.claude/skills/ai-clean-master` + [`CLAUDE.md`](./CLAUDE.md) |
| **OpenAI Codex** | `~/.codex/skills/ai-clean-master` | `<project>/.agents/skills/ai-clean-master` + [`AGENTS.md`](./AGENTS.md) |
| **Cursor** | `~/.cursor/skills/ai-clean-master` | `<project>/.cursor/rules/ai-clean-master.mdc` ([`adapters/cursor/ai-clean-master.mdc`](./adapters/cursor/ai-clean-master.mdc)) |
| **Tencent WorkBuddy** | `~/.workbuddy/skills/ai-clean-master` | `<project>/.workbuddy/skills/ai-clean-master` or `<project>/.agents/skills/ai-clean-master` |
| **Alibaba Qoder** | `~/.qoder/skills/ai-clean-master` | `<project>/.qoder/skills/ai-clean-master` + `<project>/.qoder/rules/ai-clean-master.md` |
| **ByteDance Trae** | `~/.trae/skills/ai-clean-master` | `<project>/.trae/skills/ai-clean-master` + `<project>/.trae/rules/ai-clean-master.md` |
| **Doubao Workspace (豆包工作台)** | Upload `dist/ai-clean-master-skill-bundle.zip` | Prompt & Sandbox Guide: [`adapters/doubao-workspace/doubao-skill-prompt.md`](./adapters/doubao-workspace/doubao-skill-prompt.md) |

---

## 4. Four Carrier-Specific Engines

### 1. PowerPoint Engine (`pptx_inspector.py` + `pptx_cleaner.py`)
```bash
# Scan a .pptx file for AI-slop micro-copy, buzzwords, and paired pill/footer background shapes
python scripts/pptx_inspector.py deck.pptx --json scan.json

# Apply box-and-text removal, sub-paragraph pruning, run-preserving rewrites, and font promotion
python scripts/pptx_cleaner.py deck.pptx plan.json -o deck_cleaned.pptx
```

### 2. Web & Frontend Engine (`web_cleaner.py`)
```bash
# Scan HTML/React/Vue/SVG for rounded-full badges, text-xs filler, and emoji spam
python scripts/web_cleaner.py --scan landing.html

# Apply DOM node removal, copy humanization, and typography class promotion
python scripts/web_cleaner.py --apply web_plan.json landing.html -o landing_cleaned.html
```

### 3. Raster Image / Poster Engine (`image_cleaner.py`)
```bash
# Erase baked-in pill badges/micro-copy via smart border-ring gradient interpolation & redraw promoted copy
python scripts/image_cleaner.py --apply img_plan.json poster.png -o poster_cleaned.png
```

### 4. Document Engine (`doc_cleaner.py`)
```bash
# Scan and clean Word (.docx) and Markdown (.md) files while preserving headings and tables
python scripts/doc_cleaner.py --scan report.docx
python scripts/doc_cleaner.py --apply doc_plan.json report.docx -o report_cleaned.docx
```

---

## 5. Verification

Run the self-contained 4-carrier smoke test suite:

```bash
python scripts/test_smoke.py
```

---

## 📄 License

Released under the [MIT License](LICENSE).
