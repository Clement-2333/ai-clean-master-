#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
install_skill.py — Cross-Agent One-Click Installer for AI Clean Master (ai-clean-master)
跨平台主流 AI Agent 技能一键安装与适配脚本

Supported AI Agents / 支持的主流工具:
- antigravity : Google Antigravity (~/.gemini/config/skills/ai-clean-master | .agents/skills/ai-clean-master)
- claude      : Anthropic Claude Code (~/.claude/skills/ai-clean-master | .claude/skills/ai-clean-master)
- codex       : OpenAI Codex (~/.codex/skills/ai-clean-master | .agents/skills/ai-clean-master)
- cursor      : Cursor IDE (~/.cursor/skills/ai-clean-master | .cursor/rules/ai-clean-master.mdc)
- workbuddy   : Tencent WorkBuddy (~/.workbuddy/skills/ai-clean-master | .workbuddy/skills/ai-clean-master)
- qoder       : Alibaba Qoder (~/.qoder/skills/ai-clean-master | .qoder/skills/ai-clean-master)
- trae        : ByteDance Trae (~/.trae/skills/ai-clean-master | .trae/skills/ai-clean-master)
- doubao      : Doubao Workspace / 豆包工作台 (Generates ready-to-upload zip & prompt bundle)
"""

import argparse
import shutil
import sys
import zipfile
from pathlib import Path

SKILL_NAME = "ai-clean-master"
REPO_ROOT = Path(__file__).resolve().parent.parent

CORE_FILES = [
    "SKILL.md",
    "README.md",
    "README_EN.md",
    "LICENSE",
    "references",
    "scripts",
]

GLOBAL_AGENT_PATHS = {
    "antigravity": Path.home() / ".gemini" / "config" / "skills" / SKILL_NAME,
    "claude": Path.home() / ".claude" / "skills" / SKILL_NAME,
    "codex": Path.home() / ".codex" / "skills" / SKILL_NAME,
    "cursor": Path.home() / ".cursor" / "skills" / SKILL_NAME,
    "workbuddy": Path.home() / ".workbuddy" / "skills" / SKILL_NAME,
    "qoder": Path.home() / ".qoder" / "skills" / SKILL_NAME,
    "trae": Path.home() / ".trae" / "skills" / SKILL_NAME,
}

WORKSPACE_AGENT_PATHS = {
    "antigravity": Path(".agents") / "skills" / SKILL_NAME,
    "claude": Path(".claude") / "skills" / SKILL_NAME,
    "codex": Path(".agents") / "skills" / SKILL_NAME,
    "cursor": Path(".cursor") / "skills" / SKILL_NAME,
    "workbuddy": Path(".workbuddy") / "skills" / SKILL_NAME,
    "qoder": Path(".qoder") / "skills" / SKILL_NAME,
    "trae": Path(".trae") / "skills" / SKILL_NAME,
}


def copy_skill_tree(dest: Path):
    dest.mkdir(parents=True, exist_ok=True)
    for item_name in CORE_FILES:
        src = REPO_ROOT / item_name
        if not src.exists():
            continue
        dst = dest / item_name
        if src.is_dir():
            if dst.exists():
                shutil.rmtree(dst)
            shutil.copytree(src, dst, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        else:
            shutil.copy2(src, dst)


def install_workspace_rules(agent: str, workspace_root: Path):
    """为 Cursor / Trae / Qoder 同步生成工作区规则入口文件"""
    if agent == "cursor":
        mdc_src = REPO_ROOT / "adapters" / "cursor" / "ai-clean-master.mdc"
        if mdc_src.exists():
            mdc_dst = workspace_root / ".cursor" / "rules" / "ai-clean-master.mdc"
            mdc_dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(mdc_src, mdc_dst)
            print(f"  + Installed Cursor rule: {mdc_dst}")
    elif agent in ("trae", "qoder"):
        rule_src = REPO_ROOT / "adapters" / "trae-qoder-workbuddy" / "ai-clean-master-rule.md"
        if rule_src.exists():
            rule_dst = workspace_root / f".{agent}" / "rules" / "ai-clean-master.md"
            rule_dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(rule_src, rule_dst)
            print(f"  + Installed {agent.capitalize()} rule: {rule_dst}")


def build_doubao_bundle(out_dir: Path):
    out_dir.mkdir(parents=True, exist_ok=True)
    zip_path = out_dir / "ai-clean-master-skill-bundle.zip"
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for item_name in CORE_FILES + ["adapters"]:
            src = REPO_ROOT / item_name
            if not src.exists():
                continue
            if src.is_file():
                zf.write(src, f"{SKILL_NAME}/{item_name}")
            else:
                for sub in src.rglob("*"):
                    if sub.is_file() and "__pycache__" not in sub.parts:
                        rel = sub.relative_to(REPO_ROOT)
                        zf.write(sub, f"{SKILL_NAME}/{rel.as_posix()}")
    print(f"✓ Built Doubao Workspace / Universal Skill Bundle: {zip_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Install ai-clean-master across Antigravity, Claude Code, Codex, Cursor, WorkBuddy, Qoder, Trae, and Doubao."
    )
    parser.add_argument(
        "--agent",
        default="all",
        help="Comma-separated agent names: all,antigravity,claude,codex,cursor,workbuddy,qoder,trae,doubao (default: all)",
    )
    parser.add_argument(
        "--scope",
        choices=["global", "workspace"],
        default="global",
        help="Install into user global config (~/.<agent>/skills) or target workspace (default: global)",
    )
    parser.add_argument(
        "--workspace-dir",
        default=".",
        help="Target workspace directory when --scope=workspace",
    )
    args = parser.parse_args()

    requested = [a.strip().lower() for a in args.agent.split(",") if a.strip()]
    if "all" in requested:
        agents = list(GLOBAL_AGENT_PATHS.keys()) + ["doubao"]
    else:
        agents = requested

    ws_root = Path(args.workspace_dir).resolve()

    for ag in agents:
        if ag == "doubao":
            build_doubao_bundle(REPO_ROOT / "dist")
            continue

        if args.scope == "global":
            target = GLOBAL_AGENT_PATHS.get(ag)
            if not target:
                print(f"! Unknown agent '{ag}', skipping.")
                continue
            copy_skill_tree(target)
            print(f"✓ [{ag}] Installed globally -> {target}")
        else:
            rel_target = WORKSPACE_AGENT_PATHS.get(ag)
            if not rel_target:
                print(f"! Unknown agent '{ag}', skipping.")
                continue
            target = ws_root / rel_target
            copy_skill_tree(target)
            install_workspace_rules(ag, ws_root)
            print(f"✓ [{ag}] Installed to workspace -> {target}")


if __name__ == "__main__":
    main()
