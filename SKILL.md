---
name: ai-clean-master
description: >-
  全载体「去 AI 味」与「小字连盒清理 + 视觉提权 + 人味化改写」大师技能 (All-Carrier AI-Slop Cleaner &
  Humanizer Skill for PPTX, Images/Posters, Web UI, and Docs). 支持 10 大主流行业中英双语 1:1 对等去 AI 味与真实合规角标保护
  (10 Major Industries Bilingual De-Slop & Statutory Footnote Guard). 支持 PPT (.pptx / SVG)、
  图片 (AI 海报 / 信息图 / 截图式 PPT)、网站前端 (HTML / React / Vue / Tailwind) 以及
  文档 (Word .docx / Markdown)。具备基于 `scripts/industry_classifier.py` 的自动化行业与语种识别、
  各行业专业术语白名单保护、假小字连盒清除、核心文字阶梯式字号提权与真人母语语感自适应改写。
  当用户要求清理 AI 生成内容中「AI 味很重的小字」（如顶部伪英文胶囊标签、卡片内同义反复的凑数小字、底栏假大空免责/总结、
  伪造微数据角标、满屏 ✨🚀 表情与廉价光污染），或希望消除「赋能/抓手/闭环/全链路/delve/synergy/paradigm shift」等中英文黑话八股时触发。
  Use this skill whenever the user wants to de-slop, humanize, or clean up AI-generated presentations (.pptx),
  infographics/posters (.png/.jpg), websites (.html/.tsx/.vue), or documents (.docx/.md) across 10 major industries
  with 1:1 Chinese/English parity by removing decorative pill badges, redundant micro-copy, footer disclaimers,
  and AI buzzwords while strictly protecting statutory footnotes and promoting core typography.
metadata:
  version: "1.2.0"
  license: "MIT"
  repository: "https://github.com/Clement-2333/ai-clean-master-"
  supported_industries: 10
  bilingual_parity: true
  supported_carriers:
    - "PPTX (.pptx / SVG)"
    - "Images (.png / .jpg / .webp)"
    - "Web UI (.html / .jsx / .tsx / .vue / Tailwind)"
    - "Docs (.docx / .md / text)"
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
   - **页脚/底栏的假大空总结与假免责废话（Footer Slop & Disclaimers）**：如 `本页核心洞察：构建全链路数字化闭环`、`Key Takeaway: Empowering seamless digital transformation`、`注：以上数据仅供演示参考`、AI 水印或网页假命令行状态栏。
   - **伪造的装饰性微数据/角标与符号噪音（Fake Metrics & Emoji Slop）**：无真实出处的 `+99.8%`、`INDEX-A`、`STEP 01 //`，以及满屏滥用的 `✨🚀💡⚡` 表情和廉价紫青霓虹发光。
2. **语言表述上的「中英文 AI 黑话与八股腔」（Linguistic AI Buzzwords）**：
   - **中文高频黑话**：「赋能、抓手、闭环、全链路、多维度、全方位、底层逻辑、顶层设计、生态体系、范式转移、协同共振、颗粒度、组合拳」及四字机械排比。
   - **英文高频黑话（English AI Slop）**：`delve into`, `testament to`, `rich tapestry`, `seamless integration`, `paradigm shift`, `holistic ecosystem`, `empower`, `leverage`, `cutting-edge`, `game-changer`, `unlock the full potential`。

**本技能五大铁律 / Five Iron Rules**：
- **铁律一：连盒带字一起清（Box-and-Text Removal）**：删除装饰性小字时，必须将其背后的胶囊框（Pill/Badge）、底栏条（Footer Bar）一并移除，绝不留下空色块。
- **铁律二：智能视觉提权（Smart Visual Promotion）**：删掉卡片内的凑数小字后，自动放大保留的核心观点字号（如 PPT `+2pt~+4pt`、网页 `text-base -> text-lg font-bold`）、放宽行距或垂直居中，防止版面空洞。
- **铁律三：人味化自适应改写（Adaptive Humanization）**：统一砍掉中英文黑话八股，根据 10 大行业手册（[`references/industry-playbooks-bilingual.md`](references/industry-playbooks-bilingual.md)）改写成「真人母语从业者自然说出口的专业行话」。
- **铁律四：真实合规角标绝对保护（Statutory Footnote Guard）**：调用 `scripts/industry_classifier.py` 判定，严禁误删法定、临床统计（`p < 0.05`、`95% CI`、`FDA 510(k)`）、财务审计（`GAAP`、`EBITDA`、`10-K`）、工程国家标准（`ISO`、`GB/T`、`IEC`）与绿色双碳（`Scope 1-3`、`tCO2e`）真实角标。若套有药丸框，仅剥离彩色底色，纯文本保留并弱化为底部标准排版。
- **铁律五：绝不覆盖原文件（Non-Destructive Output）**：所有修改一律输出为 `*_cleaned.<ext>` 新文件。

---

## 2. 跨平台五步工作流（融合自动分类、`grill-me` 追问与用户确认门禁）

保留包含本文件的目录绝对路径为 `SKILL_DIR`。每次调用脚本时，将 `${SKILL_DIR}` 展开为真实绝对路径。

### Stage 1：行业与语种自动识别与载体病灶扫描（Scan & Diagnose）

#### 1.1 行业与语种自动识别与真实角标预检 (Pre-Scan: Industry & Footnote Guard)
在执行载体扫描时，各引擎自动调用 `scripts/industry_classifier.py`（或在纯文本/代码场景直接调用）：
```bash
python -c "import sys; sys.path.insert(0, '${SKILL_DIR}'); from scripts.industry_classifier import detect_industry_and_language; import json; print(json.dumps(detect_industry_and_language('''<text_sample>'''), ensure_ascii=False, indent=2))"
```
- **输出参数包含**：
  - `industry_id`：10 大行业标识符之一（`tech_saas_ai`, `industrial_manufacturing`, `education_academia`, `finance_consulting`, `healthcare_biotech`, `retail_marketing`, `public_gov_smartcity`, `architecture_design`, `energy_sustainability_agtech`, `media_gaming_hospitality`）。
  - `confidence`：匹配置信度（`high`, `medium`, `default`）。
  - `language`：语言标识（`zh`, `en`, `bilingual`）。
  - `recommended_tone_zh` / `recommended_tone_en`：推荐的人味改写语感。
  - `matched_keywords_zh` / `matched_keywords_en`：识别命中的行业真实专业词汇。
- **真实角标判定契约**：
  `is_protected_domain_footnote(text)` 严格过滤假演示废话（`仅供演示参考`, `for illustrative purposes only`），绝对放行合规标准（`ISO`, `GB/T`, `IEC`, `IEEE`, `FDA 510(k)`, `NMPA`, `GAAP`, `Scope 1-3`, `arXiv`）。

#### 1.2 载体专属扫描执行
根据目标文件类型调用对应扫描引擎（支持通过 `--industry <id>` 显式指定行业）：

| 载体类型 (Carrier) | 适用扩展名 (Extensions) | 扫描命令 (Scan Command) |
|---|---|---|
| **PPT 演示文稿** | `.pptx` | `python "${SKILL_DIR}/scripts/pptx_inspector.py" "<input.pptx>" --industry <id> --json "<scan.json>"` |
| **网站 / 前端页面** | `.html`, `.jsx`, `.tsx`, `.vue`, `.svg` | `python "${SKILL_DIR}/scripts/web_cleaner.py" --scan "<input_file>" --json "<scan.json>"` |
| **图片 / 海报 / 信息图** | `.png`, `.jpg`, `.jpeg`, `.webp` | `python "${SKILL_DIR}/scripts/image_cleaner.py" --scan "<input_img>"` 并结合多模态视觉能力定位图中所有小字、胶囊标签、凑数副文案的像素坐标 `bbox` |
| **文档 / 大纲 / 讲稿** | `.docx`, `.md`, 纯文本 | `python "${SKILL_DIR}/scripts/doc_cleaner.py" --scan "<input_doc>" --json "<scan.json>"` |

> [!NOTE]
> - 在 Windows 下若 `python3` 触发 WindowsApps 存根（退出码 9009），请统一使用 `python`。
> - 若在豆包工作台（Doubao Workspace）等纯云端对话环境且无本地 Python 容器，直接对照 [`references/industry-playbooks-bilingual.md`](references/industry-playbooks-bilingual.md) 与 [`references/ai-slop-dictionary.md`](references/ai-slop-dictionary.md) 执行结构化诊断与重写。

---

### Stage 2：`Grill-Me` 逐题交互式追问对齐（One-by-One Decision Interview）

扫描完成后，**严禁直接修改文件**。必须进入 `grill-me` 访谈模式，沿着决策树**每次只问一个问题**，且**每道题必须把最推荐的选项放在第一位并标注 `(Recommended)`**：
- **跨 Agent 工具调用适配**：
  - 在 **Antigravity / Claude Code / Cursor / Trae / Qoder / WorkBuddy** 等支持结构化提问工具（如 `ask_question` 或 `AskUserQuestion`）的宿主中，优先调用该工具向用户发起单题选择。
  - 在 **Codex CLI / 豆包工作台** 等无弹窗选择工具的环境中，在对话框中用清晰的编号列表（`1. (Recommended) ...`）每次只抛出一道题，等待用户回复编号或意见后再问下一题。

按顺序消解以下决策分支（若用户在初始指令中已明确指定某项，可跳过该题）：

1. **Q1 — 目标行业与「人味语感」档位（Target Industry & Domain Tone）**：
   - **动态首推机制**：根据 Stage 1 自动识别结果，将最高置信度的行业设为第一项并标注 `(Recommended)`。
   - **10 大行业映射表（全部对照 [`references/industry-playbooks-bilingual.md`](references/industry-playbooks-bilingual.md) 专属规范）**：
     1. **科技 / SaaS / 人工智能 (Technology, SaaS & AI)**：极客实测与架构干货风（突出 P99 延迟、吞吐量、显存占用、成本降幅与真实部署指标）
     2. **智能制造 / 工业工程 / 自动化 (Industrial, Manufacturing & Engineering)**：硬核工科与现场实操风（动词 + 硬件/PLC/执行机构 + 重复定位精度、节拍与一次良品率）
     3. **教育 / 学术科研 / 高校竞赛 (Education, Academia & Campus Competitions)**：高校创客答辩与严谨学术风（消融实验对比、统计显著性 p 值、BOM 物料成本与真实样机实测）
     4. **金融 / 投资 / 财税与商业咨询 (Finance, VC, FinTech & Consulting)**：投行与咨询结论先行风（一页一结论，ARR、NDR、毛利基点 bps、回本周期与 GAAP/Non-GAAP 合规）
     5. **医疗健康 / 生物医药与临床科研 (Healthcare, Biotech & MedTech)**：严谨临床医学与循证风（入组样本量 n、双盲对照、敏感度/特异度、FDA 510(k)/NMPA 注册合规）
     6. **消费零售 / 电商增长与品牌营销 (Retail, E-Commerce & Brand Marketing)**：实战增长与主理人直白风（转化率、复购率、客单价、动销率与真实测评原声）
     7. **政务公共事业 / 国企央企与智慧城市 (Public Sector, GovTech & Smart City)**：务实政务与为民服务风（彻底清除洋气伪英文胶囊标签，突出办事时限压缩、一网通办、便民覆盖率）
     8. **建筑地产 / 空间营造与工业设计 (Architecture, Real Estate & Industrial Design)**：实体质感与工程造物风（真实材料工艺、阳极氧化、倒角壁厚、采光动线与容积率）
     9. **新能源 / 碳中和 / 现代农业与环保 (Clean Energy, ESG, Sustainability & AgTech)**：绿色实效与田间实测风（度电成本 LCOE、减排吨数 tCO2e、节水比例与亩产增幅）
     10. **文娱传媒 / 游戏动漫 / 文旅与创意内容 (Media, Gaming, Cultural IP & Hospitality)**：玩家/游客真实体验风（完播率、次留率、60fps 帧率、互动玩法与单日客流打卡）
   - **细分场景修饰（Sub-Scenario Overlay）**：可在所选行业内指定路演答辩 (Pitch)、工程技术 (Engineering)、教学培训 (Teaching) 或高管汇报 (Executive) 视角。
2. **Q2 — 小字与装饰色块的清理激进度（Cleanup Aggressiveness）**：
   - `(Recommended) 连盒全清 + 核心字号提权 (Full Box-and-Text Cleanup + Font Promotion)`：删除所有顶部伪英文/八股小胶囊（连同背景框）、底栏免责废话、卡片内同义反复的凑数小字，并将保留的核心观点字号放大居中。
   - `温和清理 (Moderate Cleanup)`：仅删除明显的伪英文角标、页脚免责废话与 `✨🚀` 表情，保留卡片内的副标题结构但将其改写为精炼人话。
3. **Q3 — 真实合规角标保护与图片修复模式确认（Footnote Guard & Image Mode）**：
   - **法定与真实角标绝对保护**：确认符合 `is_protected_domain_footnote` 的声明（如 `* FDA 510(k) Cleared, p < 0.01`、`* ISO 9001:2015 / GB/T 1804-m`、`* Non-GAAP EBITDA`、`* Scope 1-3 tCO2e`）保留，仅剥离药丸色块。
   - **虚假免责彻底删除**：确认 `注：以上数据仅供演示参考`、`for illustrative purposes only` 等假免责连盒彻底删除。
   - 若目标是**图片（`.png`/`.jpg`）**，询问采用 `(Recommended) 原图像素级无痕擦除小字 + 原位重绘人味大字`，还是 `重构为可编辑的 HTML/SVG/PPTX 图层`。

---

### Stage 3：输出「删减 + 人味改写 + 视觉提权」对照表与确认门禁

完成 `grill-me` 对齐后，阅读 [`references/layout-promotion-rules.md`](references/layout-promotion-rules.md)、[`references/industry-playbooks-bilingual.md`](references/industry-playbooks-bilingual.md) 与 [`references/ai-slop-dictionary.md`](references/ai-slop-dictionary.md)，向用户输出直观的 **逐页/逐区域 `Before → After` 对照预览表**：

```markdown
### 📋 AI Clean Master 清理与改写预览 (Cleanup & Humanization Preview)

| 页码/区域 | 动作类型 | 原内容（AI 味病灶） | 处理后（人味化 & 视觉提权） |
|---|---|---|---|
| P1 顶部 | `🗑️ 连盒删除` | `[胶囊框 #4] SECTION 01 · STRATEGIC OVERVIEW` | *连同浅蓝胶囊背景框一并移除，保留通透留白* |
| P1 卡片1 | `✂️ 删小字 + 🔼 提权` | 标题：`多维赋能分选体系`<br>小字(10pt)：`通过全链路视觉感知赋能高效农业分选闭环` | 标题改写并提权至 **20pt 居中**：<br>**`双目视觉 0.2 秒识别单果瑕疵`**（删掉下方凑数小字） |
| P1 底部 | `🛡️ 合规角标保护` | `[药丸框 #9] * FDA 510(k) Cleared, p < 0.01, n=120` | *剥离药丸背景框，文字保留并规范为底部 8.5pt Slate 弱化显示* |
| P2 引文 | `📦 文档脱壳提权` | 灰色全包围提示框：`> 核心指标：构建数字化全栈底座` | *溶解全包围色块，提权为左侧 2.5pt 单实线单侧引用块并重写人话* |
```

- **四大载体视觉提权规范（详见 [`references/layout-promotion-rules.md`](references/layout-promotion-rules.md)）**：
  - **PPTX**：几何判定成对背景框（$\text{IoA} \ge 0.75$, $H_{bg} \le 2.8 \times H_{text}$）连盒清除，保留文字阶梯提权 `+2pt ~ +4pt`，段落垂直居中。
  - **Images**：边界环采样双线性插值无痕抹除，原位重绘 `+35% ~ +60%` 高对比度思源黑体大字，法定角标排除于擦除蒙版之外。
  - **Web UI**：移除 `<span class="rounded-full">` 徽章 DOM，移除冗余 `text-xs` 小字，标题类名提权为 `text-lg font-bold leading-snug`，规范保留语义化 `<small>`/`<footer>`。
  - **Docs (.docx / .md)**：脱壳全包围底纹提示框，提权为左单实线优雅引言块（Word 2.5pt 单边框，Markdown `> **核心参数**`），标题层级规范化，保护原生脚注（`w:footnote`, `[^1]`）。
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
2. **清洗战果统计**：连盒清除的小字/胶囊框/底栏数量、砍掉的中英文 AI 黑话数量、保护的法定与合规角标数量、完成视觉字号提权与人味化改写的核心观点数量。

---

## 3. 参考文档与脚本索引 / References & Scripts

- [`references/industry-playbooks-bilingual.md`](references/industry-playbooks-bilingual.md)：10 大行业中英双语去 AI 味与专业人味改写手册（覆盖 10 大行业小字边界、真实合规标准、黑白名单词表、1:1 中英改写对照范例与高说服力句式模版）。
- [`references/layout-promotion-rules.md`](references/layout-promotion-rules.md)：四大载体（PPTX、图片、网页、文档）连盒清理几何判定、智能视觉提权与真实合规角标排版规范。
- [`references/ai-slop-dictionary.md`](references/ai-slop-dictionary.md)：中英文 AI 味小字特征库、黑话禁用词表、四大场景人味改写字典与 10 大行业速查链接。
- [`scripts/industry_classifier.py`](scripts/industry_classifier.py)：10 大行业与中英双语自动识别、黑话检测、真实合规角标保护与术语白名单暴露引擎。
- [`scripts/pptx_inspector.py`](scripts/pptx_inspector.py) & [`scripts/pptx_cleaner.py`](scripts/pptx_cleaner.py)：`.pptx` 扫描、配对背景盒删除、法定角标保护与清理提权引擎。
- [`scripts/web_cleaner.py`](scripts/web_cleaner.py)：HTML / React / Vue / SVG DOM 胶囊扫描、合规角标保留与降噪提权引擎。
- [`scripts/image_cleaner.py`](scripts/image_cleaner.py)：海报与信息图像素级无痕擦除小字、法定角标保护与大字重绘引擎。
- [`scripts/doc_cleaner.py`](scripts/doc_cleaner.py)：Word (`.docx`) 与 Markdown (`.md`) 提示框脱壳、原生脚注保留与去 AI 味清理引擎。
- [`scripts/install_skill.py`](scripts/install_skill.py)：跨平台主流 AI Agent 一键安装与适配脚本。
