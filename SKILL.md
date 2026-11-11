---
name: ai-clean-master
description: >-
  全载体「去 AI 味」与「小字连盒清理 + 视觉提权 + 人味化改写」大师技能 (All-Carrier AI-Slop Cleaner &
  Humanizer Skill for PPTX, Images/Posters, Web UI, and Docs). 支持 PPT (.pptx / SVG)、
  图片 (AI 海报 / 信息图 / 截图式 PPT)、网站前端 (HTML / React / Vue / Tailwind) 以及
  文档 (Word .docx / Markdown)。当用户要求清理 AI 生成内容中「AI 味很重的小字」（如顶部伪英文胶囊标签、
  卡片内同义反复的凑数小字、底栏假大空免责/总结、伪造微数据角标、满屏 ✨🚀 表情与廉价光污染），
  或希望消除「赋能/抓手/闭环/全链路/delve/synergy/paradigm shift」等中英文黑话八股、优化表述使其更有「人味感」时触发。
  Use this skill whenever the user wants to de-slop, humanize, or clean up AI-generated presentations (.pptx),
  infographics/posters (.png/.jpg), websites (.html/.tsx/.vue), or documents (.docx/.md) by removing decorative
  pill badges, redundant micro-copy, footer disclaimers, and AI buzzwords while promoting core typography.
metadata:
  version: "1.1.0"
  license: "MIT"
  repository: "https://github.com/Clement-2333/ai-clean-master-"
  supported_agents:
    - "Google Antigravity"
    - "Claude Code"
    - "OpenAI Codex"
    - "Cursor"
    - "Tencent WorkBuddy"
    - "Alibaba Qoder"
    - "ByteDance Trae"
    - "Doubao Workspace (豆包工作台)"
---

# AI Clean Master（全载体去 AI 味小字清理与人味化大师）

## 1. 核心使命 / Core Mission

AI 生成的 PPT、海报信息图、网站页面和文档往往带有强烈的「机器流水线塑料感（AI Slop）」，主要集中在两大病灶：

1. **视觉与排版上的「AI 味小字及廉价装饰框」（Visual & Micro-Copy Slop）**：
   - **顶部/卡片伪英文与八股眉题（Kickers & Pill Badges）**：如 `SECTION 01 · STRATEGIC OVERVIEW`、`CORE INSIGHT`、`✨ Next-Gen AI Platform`、`SYSTEM ONLINE`、`核心赋能模块`，通常还套着一个圆角胶囊框（Pill/Badge）或发光边框。
   - **卡片内同义反复的凑数解释小字（Redundant Micro-Copy）**：大标题已经写明「识别速度提升 3 倍」，下面还硬塞两行 `10pt` / `text-xs` 的废话「通过引入高效算法机制，实现了识别处理速度的显著提升」。
   - **页脚/底栏的假大空总结与免责废话（Footer Slop & Disclaimers）**：如 `本页核心洞察：构建全链路数字化闭环`、`Key Takeaway: Empowering seamless digital transformation`、`注：以上数据仅供演示参考`、AI 水印或网页假命令行状态栏。
   - **伪造的装饰性微数据/角标与符号噪音（Fake Metrics & Emoji Slop）**：无真实出处的 `+99.8%`、`INDEX-A`、`STEP 01 //`，以及满屏滥用的 `✨🚀💡⚡` 表情和廉价紫青霓虹发光。
2. **语言表述上的「中英文 AI 黑话与八股腔」（Linguistic AI Buzzwords）**：
   - **中文高频黑话**：「赋能、抓手、闭环、全链路、多维度、底层逻辑、顶层设计、生态体系、范式转移、协同共振、颗粒度、组合拳」及四字机械排比。
   - **英文高频黑话（English AI Slop）**：`delve into`, `testament to`, `rich tapestry`, `seamless integration`, `paradigm shift`, `holistic ecosystem`, `empower`, `leverage`, `cutting-edge`, `game-changer`, `unlock the full potential`。

**本技能四大铁律 / Four Iron Rules**：
- **连盒带字一起清（Box-and-Text Removal）**：删除装饰性小字时，必须将其背后的胶囊框（Pill/Badge）、底栏条（Footer Bar）一并移除，绝不留下空色块。
- **智能视觉提权（Smart Visual Promotion）**：删掉卡片内的凑数小字后，自动放大保留的核心观点字号（如 PPT `+2pt~+4pt`、网页 `text-base -> text-lg font-semibold`）、放宽行距或垂直居中，防止版面空洞。
- **人味化自适应改写（Adaptive Humanization）**：统一砍掉中英文黑话八股，并根据目标场景（竞赛路演、工科答辩、教学课堂、干练商务）改写成「真人上台能自然说出口的话」。
- **绝不覆盖原文件（Non-Destructive Output）**：所有修改一律输出为 `*_cleaned.<ext>` 新文件。

---

## 2. 跨平台五步工作流（融合 `grill-me` 追问与用户确认门禁）

保留包含本文件的目录绝对路径为 `SKILL_DIR`。每次调用脚本时，将 `${SKILL_DIR}` 展开为真实绝对路径。

### Stage 1：载体识别与 AI 味病灶扫描（Scan & Diagnose）

根据用户提供的目标文件或代码类型，调用对应的专属扫描引擎（识别准则详见 [`references/ai-slop-dictionary.md`](references/ai-slop-dictionary.md)）：

| 载体类型 (Carrier) | 适用扩展名 (Extensions) | 扫描命令 (Scan Command) |
|---|---|---|
| **PPT 演示文稿** | `.pptx` | `python "${SKILL_DIR}/scripts/pptx_inspector.py" "<input.pptx>" --json "<scan.json>"` |
| **网站 / 前端页面** | `.html`, `.jsx`, `.tsx`, `.vue`, `.svg` | `python "${SKILL_DIR}/scripts/web_cleaner.py" --scan "<input_file>" --json "<scan.json>"` |
| **图片 / 海报 / 信息图** | `.png`, `.jpg`, `.jpeg`, `.webp` | `python "${SKILL_DIR}/scripts/image_cleaner.py" --scan "<input_img>"` 并结合多模态视觉能力定位图中所有小字、胶囊标签、凑数副文案的像素坐标 `bbox` |
| **文档 / 大纲 / 讲稿** | `.docx`, `.md`, 纯文本 | `python "${SKILL_DIR}/scripts/doc_cleaner.py" --scan "<input_doc>" --json "<scan.json>"` |

> [!NOTE]
> - 在 Windows 下若 `python3` 触发 WindowsApps 存根（退出码 9009），请统一使用 `python`。
> - 若在豆包工作台（Doubao Workspace）等纯云端对话环境且无本地 Python 容器，直接对照 [`references/ai-slop-dictionary.md`](references/ai-slop-dictionary.md) 执行结构化诊断与代码/文案重写。

---

### Stage 2：`Grill-Me` 逐题交互式追问对齐（One-by-One Decision Interview）

扫描完成后，**严禁直接修改文件**。必须进入 `grill-me` 访谈模式，沿着决策树**每次只问一个问题**，且**每道题必须把最推荐的选项放在第一位并标注 `(Recommended)`**：
- **跨 Agent 工具调用适配**：
  - 在 **Antigravity / Claude Code / Cursor / Trae / Qoder / WorkBuddy** 等支持结构化提问工具（如 `ask_question` 或 `AskUserQuestion`）的宿主中，优先调用该工具向用户发起单题选择。
  - 在 **Codex CLI / 豆包工作台** 等无弹窗选择工具的环境中，在对话框中用清晰的编号列表（`1. (Recommended) ...`）每次只抛出一道题，等待用户回复编号或意见后再问下一题。

按顺序消解以下决策分支（若用户在初始指令中已明确指定某项，可跳过该题）：

1. **Q1 — 目标场景与「人味语感」档位（Tone & Scenario）**：
   - 自动根据扫描内容把最匹配的风格放在第一项并标 `(Recommended)`：
     - **竞赛路演 / 创客答辩风 (Pitch & Competition)**：突出真实痛点、「我们自己动手做了什么」与实测效果（拒绝空谈生态与赋能）。
     - **工科实训 / 技术工程风 (Engineering & Technical)**：动词开头 + 具体硬件/算法/参数 + 量化结果，客观干练。
     - **课堂教学 / 班会演讲风 (Teaching & Speech)**：带第一/第二人称主语（「咱们看」「大家常遇到」 / `"Let's look at..."`），短句口语化。
     - **干练商务 / 日常汇报风 (Crisp Business)**：结论先行（一页一句人话结论），用事实和具体动作代替四字形容词。
2. **Q2 — 小字与装饰色块的清理激进度（Cleanup Aggressiveness）**：
   - `(Recommended) 连盒全清 + 核心字号提权 (Full Box-and-Text Cleanup + Font Promotion)`：删除所有顶部伪英文/八股小胶囊（连同背景框）、底栏免责废话、卡片内同义反复的凑数小字，并将保留的核心观点字号放大居中。
   - `温和清理 (Moderate Cleanup)`：仅删除明显的伪英文角标、页脚免责废话与 `✨🚀` 表情，保留卡片内的副标题结构但将其改写为精炼人话。
3. **Q3 — 疑似真实数据角标或图片修复模式确认（Borderline Data / Image Mode）**：
   - 若扫描发现带具体数字的小字/角标（如 `+38.5%`、`N=120`），单列一题请用户确认哪些是**真实业务数据（需保留并提权）**、哪些是**AI 编造的装饰微数据（需连盒删除）**。
   - 若目标是**图片（`.png`/`.jpg`）**，询问采用 `(Recommended) 原图像素级无痕擦除小字 + 原位重绘人味大字`，还是 `重构为可编辑的 HTML/SVG/PPTX 图层`。

---

### Stage 3：输出「删减 + 人味改写 + 视觉提权」对照表与确认门禁

完成 `grill-me` 对齐后，阅读 [`references/layout-promotion-rules.md`](references/layout-promotion-rules.md) 与 [`references/ai-slop-dictionary.md`](references/ai-slop-dictionary.md)，向用户输出直观的 **逐页/逐区域 `Before → After` 对照预览表**：

```markdown
### 📋 AI Clean Master 清理与改写预览 (Cleanup & Humanization Preview)

| 页码/区域 | 动作类型 | 原内容（AI 味病灶） | 处理后（人味化 & 视觉提权） |
|---|---|---|---|
| P1 顶部 | `🗑️ 连盒删除` | `[胶囊框 #4] SECTION 01 · STRATEGIC OVERVIEW` | *连同浅蓝胶囊背景框一并移除* |
| P1 卡片1 | `✂️ 删小字 + 🔼 提权` | 标题：`多维赋能分选体系`<br>小字(10pt)：`通过全链路视觉感知赋能高效农业分选闭环` | 标题改写并提权至 **20pt 居中**：<br>**`双目视觉 0.2 秒识别单果瑕疵`**（删掉下方凑数小字） |
| P1 底部 | `🗑️ 连盒删除` | `[底栏条 #9] 本页核心洞察：实现高质量发展的抓手` | *连同底部深灰横条一并移除* |
```

- **确认门禁（Confirmation Gate）**：展示预览表后，请用户确认是否执行（或提出微调意见）。**只有当用户明确确认（或在最初请求中已明确声明“不用确认直接出一键结果”）时，才可进入 Stage 4**。

---

### Stage 4：执行连盒清理、人味改写与智能视觉提权（Execute Cleanup & Promotion）

根据确认后的方案，调用对应载体的清理引擎生成 `*_cleaned.<ext>` 新文件：

#### 路线 A：PPT 演示文稿 (`.pptx`)
编写 JSON 计划文件并运行：
```bash
python "${SKILL_DIR}/scripts/pptx_cleaner.py" "<input.pptx>" "<plan.json>" -o "<input_cleaned.pptx>"
```
`plan.json` 结构示例：
```json
{
  "slides": [
    {
      "slide_index": 1,
      "delete_shape_ids": [4, 5, 9, 10],
      "delete_paragraphs": [
        {"shape_id": 7, "paragraph_indices": [1, 2]}
      ],
      "rewrites": [
        {
          "shape_id": 7,
          "paragraph_index": 0,
          "new_text": "双目视觉 0.2 秒识别单果瑕疵",
          "promote_pt": 3.0,
          "vertical_center": true
        }
      ]
    }
  ]
}
```

#### 路线 B：网站与前端页面 (`.html` / `.jsx` / `.tsx` / `.vue` / `.svg`)
编写 `<web_plan.json>` 并运行：
```bash
python "${SKILL_DIR}/scripts/web_cleaner.py" --apply "<web_plan.json>" "<input.html>" -o "<input_cleaned.html>"
```

#### 路线 C：图片 / 海报 / 信息图 (`.png` / `.jpg` / `.webp`)
编写区域擦除与重绘配置 `<img_plan.json>`（定义每个区域的 `bbox: [x1, y1, x2, y2]`、`action: "erase_only" | "erase_and_redraw"`、`text`、`font_size`），运行：
```bash
python "${SKILL_DIR}/scripts/image_cleaner.py" --apply "<img_plan.json>" "<input.png>" -o "<input_cleaned.png>"
```

#### 路线 D：文档与富文本 (`.docx` / `.md`)
编写 `<doc_plan.json>` 并运行：
```bash
python "${SKILL_DIR}/scripts/doc_cleaner.py" --apply "<doc_plan.json>" "<input.docx>" -o "<input_cleaned.docx>"
```

---

### Stage 5：交付结果与清洗报告（Delivery & Summary Report）

验证生成的 `*_cleaned.*` 文件存在且无格式损坏，向用户输出精炼交付报告：
1. **新文件路径**；
2. **清洗战果统计**：连盒清除的小字/胶囊框/底栏数量、砍掉的中英文 AI 黑话数量、完成视觉字号提权与人味化改写的核心观点数量。

---

## 3. 参考文档与脚本索引 / References & Scripts

- [`references/ai-slop-dictionary.md`](references/ai-slop-dictionary.md)：中英文 AI 味小字特征库、黑话禁用词表、四大场景人味改写字典。
- [`references/layout-promotion-rules.md`](references/layout-promotion-rules.md)：PPT/图片/网页连盒清理几何判定与字号提权规范。
- [`scripts/pptx_inspector.py`](scripts/pptx_inspector.py) & [`scripts/pptx_cleaner.py`](scripts/pptx_cleaner.py)：`.pptx` 扫描与清理提权引擎。
- [`scripts/web_cleaner.py`](scripts/web_cleaner.py)：HTML / React / Vue / SVG 扫描与降噪提权引擎。
- [`scripts/image_cleaner.py`](scripts/image_cleaner.py)：海报与信息图像素级无痕擦除小字与大字重绘引擎。
- [`scripts/doc_cleaner.py`](scripts/doc_cleaner.py)：Word (`.docx`) 与 Markdown (`.md`) 去 AI 味清理引擎。
- [`scripts/install_skill.py`](scripts/install_skill.py)：跨平台主流 AI Agent 一键安装与适配脚本。
