# AGENTS.md — AI Clean Master (`ai-clean-master`)

This repository provides **`ai-clean-master`**, a cross-agent skill and Python toolkit for cleaning up AI-generated micro-copy ("AI-slop small text" / AI 味小字), removing decorative pill badges & footer disclaimers **box-and-text together** (连盒带字清除), visually promoting retained core copy (智能字号提权), and rewriting robotic buzzwords into authentic human language (人味化改写) across **PPTX (`.pptx`/SVG)**, **Images/Posters (`.png`/`.jpg`/`.webp`)**, **Websites (`.html`/`.jsx`/`.tsx`/`.vue`)**, and **Documents (`.docx`/`.md`)**.

## Mandatory Workflow

Whenever triggered, follow [`SKILL.md`](./SKILL.md) strictly:
1. **Stage 1 (Scan & Diagnose)**: Run the carrier-specific scanner in [`scripts/`](./scripts/) (`pptx_inspector.py`, `web_cleaner.py --scan`, `image_cleaner.py --scan`, or `doc_cleaner.py --scan`) and consult [`references/ai-slop-dictionary.md`](./references/ai-slop-dictionary.md).
2. **Stage 2 (`grill-me` One-by-One Alignment)**: Interview the user **one question at a time** (using `ask_question` / `AskUserQuestion` or numbered single-question prompt), always placing the `(Recommended)` option first.
3. **Stage 3 (Preview & Confirmation Gate)**: Output a `Before → After` comparison table showing box-and-text deletions, humanized rewrites, and font promotions. Wait for user confirmation before mutating files.
4. **Stage 4 (Execute Cleanup & Visual Promotion)**: Run `pptx_cleaner.py`, `web_cleaner.py --apply`, `image_cleaner.py --apply`, or `doc_cleaner.py --apply` following [`references/layout-promotion-rules.md`](./references/layout-promotion-rules.md). Always write to `<name>_cleaned.<ext>` (never overwrite original files).
5. **Stage 5 (Delivery Report)**: Present the output file link and cleanup statistics.
