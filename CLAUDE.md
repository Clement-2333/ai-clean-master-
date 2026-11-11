# CLAUDE.md — AI Clean Master (`ai-clean-master`)

See [`SKILL.md`](./SKILL.md) and [`AGENTS.md`](./AGENTS.md) for the complete 5-stage `ai-clean-master` workflow (Scan → `grill-me` One-by-One Alignment → Before/After Confirmation Gate → Box-and-Text Cleanup & Visual Promotion → Delivery).

## Quick Commands
- Run full smoke tests across PPTX, Web, Image, and Docs:
  ```bash
  python scripts/test_smoke.py
  ```
- Install across all supported AI agents (Claude Code, Codex, Antigravity, Cursor, WorkBuddy, Qoder, Trae, Doubao):
  ```bash
  python scripts/install_skill.py --agent all --scope global
  ```
