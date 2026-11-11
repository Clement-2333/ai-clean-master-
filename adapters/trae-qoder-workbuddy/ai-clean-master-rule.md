# AI Clean Master (`ai-clean-master`) — Trae / Qoder / WorkBuddy 规则与技能适配器

> 适用工具：**字节跳动 Trae** (`.trae/rules/` | `.trae/skills/`)、**阿里 Qoder** (`.qoder/rules/` | `.qoder/skills/`)、**腾讯 WorkBuddy** (`.workbuddy/skills/` | `.agents/skills/`)

## 触发场景 (When to Use)
当用户要求对 **PPT (`.pptx`/SVG)**、**图片 (AI 海报/信息图/截图 PPT)**、**网站前端 (HTML/React/Vue)** 或 **文档 (`.docx`/Markdown)** 执行以下任一操作时激活：
- 清理「AI 味很重的小字」（顶部伪英文眉题胶囊 `SECTION 01`、卡片内同义反复的凑数小字、底部假大空总结/免责废话、编造的 `+99%` 微数据角标、`✨🚀` 表情堆砌）；
- 消除「赋能、抓手、闭环、全链路、底层逻辑、delve、synergy、paradigm shift」等中英文 AI 黑话，按照 10 大行业人味化手册改写为真实母语从业者文案；
- 连盒带字删除装饰色块，保护真实行业合规角标，并对保留的核心文字进行字号放大提权。

---

## 核心参考知识库 (Mandatory References)
- **技能主编排规范**: `SKILL.md`
- **10 大行业中英双语去黑话手册**: `references/industry-playbooks-bilingual.md`
- **中英双语 AI 黑话词典**: `references/ai-slop-dictionary.md`
- **连盒清理与视觉提权规则**: `references/layout-promotion-rules.md`
- **行业分类与合规保护引擎**: `scripts/industry_classifier.py`

---

## 标准五步执行流 (5-Stage Execution Workflow)

### Stage 1：自动扫描病灶与 10 大行业识别 (Scan & Diagnose)
1. **自动识别行业与语言**:
   - 各载体扫描器自动调用 `industry_classifier.py`，识别文本主语言（`zh` / `en` / `bilingual`）与所属 10 大行业之一：
     - `tech_saas_ai` (科技/SaaS/AI) | `industrial_manufacturing` (智能制造/工业) | `education_academia` (教育/科研/竞赛)
     - `finance_consulting` (金融/投资/咨询) | `healthcare_biotech` (医疗健康/生物) | `retail_marketing` (消费零售/电商)
     - `public_gov_smartcity` (政务/智慧城市) | `architecture_design` (建筑/工业设计) | `energy_sustainability_agtech` (新能源/双碳/农业)
     - `media_gaming_hospitality` (文娱传媒/游戏)
2. **载体专属扫描**:
   - PPTX：`python scripts/pptx_inspector.py "<input.pptx>"`
   - 网页/前端：`python scripts/web_cleaner.py --scan "<input>"`
   - 海报/图片：`python scripts/image_cleaner.py --scan "<input>"` 并结合视觉定位小字与胶囊框坐标 `bbox`
   - 文档：`python scripts/doc_cleaner.py --scan "<input>"`

### Stage 2：`Grill-Me` 逐题追问对齐（每次只问一题，首项必标 `(Recommended)`）
扫描完成后，**严禁直接修改文件**。在 Trae / Qoder / WorkBuddy 中，优先调用用户交互工具（如 `ask_question` / `AskUserQuestion`）或在对话中每次只抛出一题：
1. **Q1 — 目标行业与「人味语感」档位 (10 Major Industries)**:
   - 自动将 Stage 1 识别出的行业作为首项推荐：
     - `1. (Recommended: 自动识别) <命中行业名称> — <推荐人味语感>`
   - 列出 10 大行业完整选项供用户选择或调整（映射至 `references/industry-playbooks-bilingual.md`）。
2. **Q2 — 小字与胶囊背景框清理激进度 (Cleanup Aggressiveness)**:
   - `1. (Recommended) 连盒全清 + 核心大字视觉提权 (Full Box-and-Text Cleanup + Typographic Promotion)`：连盒删除伪英文眉题胶囊、底栏总结条与卡片内凑数小字，卡片主标题字号放大 `+2~+4pt`（网页 `text-lg font-bold`）并居中。
   - `2. 温和清理 (Moderate Cleanup)`：仅删除外层胶囊与底栏免责，卡片内凑数小字改写为人话但保留结构。
3. **Q3 — 真实行业合规角标保护与数据核对 (Footnote Guard)**:
   - **绝对保护真角标**: 严格保护符合 `is_protected_domain_footnote` 的医疗临床（`p < 0.05`, `95% CI`, `FDA 510(k)`, `NMPA`）、金融财报（`GAAP`, `EBITDA`, `10-K`, `bps`）、国家/国际标准（`ISO`, `GB/T`, `IEC`, `IEEE`）、双碳（`Scope 1/2/3`, `tCO2e`）及学术引用（`arXiv`）。若带有彩色胶囊底纹，仅剥离胶囊底色，纯文字保留并弱化为底部 8~9pt。
   - **坚决连盒删除假免责**: `仅供演示参考`、`for demonstration purposes only`、`虚拟数据` 连盒带字彻底清除。
   - 若输入为图片，确认 `原图像素级无痕擦除 + 原位大字重绘` 还是 `重构为可编辑图层`。

### Stage 3：`Before → After` 修改预览与确认门禁 (Confirmation Gate)
输出逐页/逐模块修改对照表，经用户确认后再执行修改：

| 载体与位置 | 元素类型 | 处置动作 | 优化前 (AI Slop) | 优化后 (人味表达与版式重平衡) |
|---|---|---|---|---|
| PPTX 第 1 页顶部 | 伪英文眉题 | 连盒删除 | `[SECTION 01 · 架构全景]` (胶囊框) | *(彻底移除胶囊背景框与小字，留白)* |
| PPTX 第 1 页卡片 | 标题 + 凑数小字 | 提权 + 人味改写 | 多维感知赋能智慧分选闭环 (16pt) + 凑数小字 (10pt) | **双目相机 0.2 秒识别单果瑕疵，分拣效率提升 4 倍** (20pt 加粗居中) |
| Web UI 卡片 | 药丸徽章 | DOM 节点删除 | `<span class="rounded-full ...">✨ Next-Gen</span>` | *(彻底移除 span 节点，消除空边框)* |

### Stage 4：连盒清理与视觉提权执行 (Non-Destructive Execution)
调用对应脚本并遵循 `references/layout-promotion-rules.md`：
- **PPTX**: 依据几何判定法则（$\text{IoA} \ge 0.75$, $H \le 2.8\times$）成对删除背景框，主标题提权 `+2~+4pt`。
- **Web UI**: 移除 badge DOM，移除冗余 `<p>`，标题类名提权为 `text-lg font-bold leading-snug`。
- **图片**: 边界环采样无痕抹除，原位重绘高质量思源黑体/YaHei 大字，保护真实角标区域。
- **文档**: 脱壳彩色提示框，标题去括号编号，保护原生脚注（`w:footnote`, `[^1]`）。
- **文件输出铁律**: 一律输出为 `<name>_cleaned.<ext>`，绝不覆盖原文件。

### Stage 5：输出清洗统计报告 (Delivery Report)
汇总连盒清除的小字/色块数、替换的黑话数、保护的合规声明数与字号提权项，输出最终交付物。
