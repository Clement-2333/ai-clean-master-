# AI Clean Master (`ai-clean-master`) — Trae / Qoder / WorkBuddy 规则与技能适配器

> 适用工具：**字节跳动 Trae** (`.trae/rules/` | `.trae/skills/`)、**阿里 Qoder** (`.qoder/rules/` | `.qoder/skills/`)、**腾讯 WorkBuddy** (`.workbuddy/skills/` | `.agents/skills/`)

## 触发场景 (When to Use)
当用户要求对 **PPT (`.pptx`/SVG)**、**图片 (AI 海报/信息图/截图 PPT)**、**网站前端 (HTML/React/Vue)** 或 **文档 (`.docx`/Markdown)** 执行以下任一操作时激活：
- 清理「AI 味很重的小字」（顶部伪英文眉题胶囊 `SECTION 01`、卡片内同义反复的凑数小字、底部假大空总结/免责废话、编造的 `+99%` 微数据角标、`✨🚀` 表情堆砌）；
- 消除「赋能、抓手、闭环、全链路、底层逻辑、delve、synergy、paradigm shift」等中英文 AI 黑话，将文案改写得更有人味感；
- 连盒带字删除装饰色块，并对保留的核心文字进行字号放大提权。

## 标准五步执行流 (5-Stage Execution Workflow)

1. **Stage 1：自动扫描病灶**
   - PPTX：`python scripts/pptx_inspector.py "<input.pptx>"`
   - 网页/前端：`python scripts/web_cleaner.py --scan "<input>"`
   - 海报/图片：`python scripts/image_cleaner.py --scan "<input>"` 并结合视觉识别定位小字与胶囊框坐标 `bbox`
   - 文档：`python scripts/doc_cleaner.py --scan "<input>"`
2. **Stage 2：`grill-me` 逐题追问对齐（每次只问一题，首项必标 `(Recommended)`）**
   - Q1：确认目标受众与人味语感档位（竞赛路演风 / 工科技术风 / 课堂演讲风 / 干练商务风）；
   - Q2：确认小字与胶囊背景框清理激进度（默认推荐：连盒全清 + 核心观点字号提权）；
   - Q3：确认疑似真实业务数据角标的去留（或图片原位无痕重绘 vs. 转可编辑图层）。
3. **Stage 3：`Before → After` 修改预览与确认门禁**
   - 输出清晰的逐页/逐模块删减、改写与字号提权对照表，经用户确认后再执行修改。
4. **Stage 4：连盒清理与视觉提权执行**
   - 调用 `pptx_cleaner.py` / `web_cleaner.py` / `image_cleaner.py` / `doc_cleaner.py` 输出 `*_cleaned.<ext>` 新文件（绝不覆盖原文件）。
5. **Stage 5：输出清洗统计报告**
   - 汇总连盒清除的小字/色块数、替换的黑话数与字号提权项。
