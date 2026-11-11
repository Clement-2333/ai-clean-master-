# 连盒清理与智能视觉提权规则 / Layout Box Cleaning & Typographic Promotion Rules (`layout-promotion-rules.md`)

本文档规定 `ai-clean-master` 在清理 AI 味小字后，如何**同步清除背后的装饰色块与容器框（连盒带字清理 / Paired Container Removal）**，以及如何**对保留的核心文字进行视觉提权与版面重平衡（Visual Promotion & Layout Rebalancing）**。
规则全面覆盖 **PPTX 演示文稿、图片/海报、网页前端（HTML/React/Vue/Tailwind）以及文档（Word .docx / Markdown）四大载体**，并对各载体中的**真实合规与学术工程角标容器建立绝对保护与专业排版准则**。

This document defines how `ai-clean-master` removes decorative containers and paired background shapes when cleaning AI micro-copy slop, and how it performs **typographic promotion and visual rebalancing** for retained core content across four carriers: **PPTX presentations, images/infographics, web UI (HTML/React/Vue/Tailwind), and documents (Word .docx / Markdown)**, while enforcing strict protection and clean restyling for legitimate domain footnotes.

---

## 一、PPT (`.pptx`) 连盒清理与字号提权规范 / PPTX Paired Shape Cleaning & Typographic Promotion

### 1. 配对背景框几何判定法则 (Geometric Paired Shape Detection)
在 AI 生成的 PPT（或由 SVG/HTML 转换出的 PPTX）中，顶部伪英文眉题（Kicker/Badge）或底部总结条（Footer）通常不是文本框自身的填充色，而是**文本框（TextBox）叠加浮动在一个独立的圆角矩形/矩形（AutoShape）之上**。如果只删除文本框，版面上会残留刺眼的空色块、空胶囊或空横条。

`pptx_inspector.py` 与 `pptx_cleaner.py` 采用以下严格的几何判定法则自动识别并绑定配对背景形状 `paired_bg_shape_id`：

1. **包围盒交叠比例 (Intersection over Area - $\text{IoA}$)**:
   - 设待清理小字文本框的包围盒为 $B_{text} = (x_1, y_1, x_2, y_2)$，候选背景形状包围盒为 $B_{bg} = (X_1, Y_1, X_2, Y_2)$。
   - 交集面积占文本框面积比例必须满足：
     $$\text{IoA} = \frac{\text{Area}(B_{text} \cap B_{bg})}{\text{Area}(B_{text})} \ge 0.75$$
2. **尺寸比例与唯一性约束 (Size Constraints & Solitary Guard)**:
   - 背景形状内部**严禁包含其他未被标记删除的正常正文或标题文本**。
   - 背景形状高度约束：$H_{bg} \le 2.8 \times H_{text}$ 且 $H_{bg} \le 1.2\text{ inch}$（确保仅匹配胶囊标签条、装饰横栏，坚决防止误删承载整个模块的 Bento 大卡片或全屏背景底层）。
3. **连盒删除执行机制 (Execution Contract)**:
   - 当小字文本框被确认删除时，其绑定的 `paired_bg_shape_id` 自动合并进 `delete_shape_ids`，在同一批次中从 Slide XML 树中彻底移除。

### 2. 卡片内删小字后的「智能视觉提权」公式 (Font Size Promotion Formulas)
当卡片内删除了 1~3 行同义反复的凑数解释小字（或删除了冗余副文本框），仅保留卡片主标题或核心论点短句时，必须对保留文本执行提权：

1. **阶梯式字号提权 (Step-wise Font Promotion)**:
   - 原核心文字字号 $S_{orig} \le 14\text{pt}$ $\rightarrow$ 提权 `+3pt ~ +4pt`（目标范围 `16pt ~ 18pt`）；
   - 原核心文字字号 $14\text{pt} < S_{orig} \le 18\text{pt}$ $\rightarrow$ 提权 `+2pt ~ +3pt`（目标范围 `18pt ~ 21pt`）；
   - 原核心文字字号 $S_{orig} > 18\text{pt}$ $\rightarrow$ 提权 `+1pt ~ +2pt`（最高上限为页面主标题字号减去 `4pt`）。
2. **字重增强与空间垂直居中 (Weight Enhancement & Centering)**:
   - 将保留的核心标题设为加粗（`font.bold = True`），字重建议 600~700。
   - 若删除的是同一文本框内的副段落，将文本框垂直锚定设为居中（`MSO_ANCHOR.MIDDLE`），或微调文本框 `top` 坐标下移 `0.10 ~ 0.20 inch`，使放大后的核心观点自然稳居卡片视觉中心。

### 3. PPTX 真实合规角标与尾注的保护与排版规范 (Footnote Guard & Clean Styling)
- **判定准则**: 调用 `industry_classifier.is_protected_domain_footnote(text)`。若包含国家/国际标准号（如 `GB/T`、`ISO`、`IEC`）、临床试验数据（如 `p < 0.01`、`95% CI`、`FDA 510(k)`）、审计口径（如 `Non-GAAP`、`EBITDA`、`SEC Form 10-K`）或真实学术引用，**严禁作为 AI 废话删除**。
- **剥离装饰，纯净排版 (Strip Container, Retain Clean Text)**:
  - 若真实角标文本框背后附带了 AI 风格的鲜艳胶囊框或高饱和度色块，**仅删除背景色块**，保留文字。
  - 真实角标排版参数：
    - 字号：`8pt ~ 9pt`；
    - 颜色：中性弱化灰色（浅色背景下使用 `#64748B` Slate 或 `#71717A` Zinc，深色背景下使用 `#94A3B8`）；
    - 位置：锚定于页面底部边缘（`top >= 90%` Slide Height），取消任何边框与投影，保持单倍行距。

---

## 二、图片载体（海报 / 信息图 / 截图式 PPT）清理与重绘规范 / Image Inpainting & Typography Redraw

针对 `.png` / `.jpg` / `.webp` 格式的位图，`image_cleaner.py` 提供像素级无痕清理与高质感字体原位重绘：

### 1. 无痕背景擦除算法 (Smart Background Erase Algorithms)
给定待清除的小字或胶囊框坐标 `bbox = [x1, y1, x2, y2]`：
- **外扩采样环 (Border Ring Sampling)**：在 `bbox` 外围取 `3px ~ 6px` 宽度的边界环，计算环内像素的 RGB 均值、中位数及颜色方差：
  1. **纯色或微噪点背景 (Solid / Low-Variance Background)**:
     - 取采样环的 RGB 中位数（Median Color）填充整个 `bbox` 区域；
     - 对边界向外扩展 2 像素进行高斯羽化过渡，彻底消除原胶囊框抗锯齿边缘留下的脏痕。
  2. **线性渐变背景 (Linear / Bilinear Gradient Background)**:
     - 分别采样 `bbox` 左、右或上、下边界的中位数色值，使用双线性插值（Bilinear Gradient Fill）平滑渲染渐变色，精确复原底图光影过渡。
  3. **复杂纹理底图 (Complex Texture Background)**:
     - 调用 `cv2.inpaint`（Navier-Stokes 或 Telea 算法，半球半径 3px）执行结构化纹理修补。

### 2. 擦除模式分流 (Erase Modes & Redraw Contract)
- **仅删除模式 (`action: "erase_only"`)**:
  - 适用于：顶部伪英文胶囊（如 `SECTION 01`）、底部假大空免责声明、装饰性假数据角标、浮动 Emoji。
  - 执行：执行无痕擦除后直接保留纯净底图，释放留白空间。
- **擦除并提权重绘模式 (`action: "erase_and_redraw"`)**:
  - 适用于：卡片内「空洞黑话标题 + 凑数小字」合并重塑场景。
  - 执行步骤：
    1. 计算「原标题 + 原小字」的合并外接矩形并完整擦除；
    2. 探测系统高质量无衬线字体（优先加载 `Microsoft YaHei UI Bold`、`PingFang SC Semibold`、`Source Han Sans / 思源黑体` 或 `Inter`）；
    3. 以前景对比度优先原则自动计算字体颜色（深底用 `#FFFFFF` / `#F8FAFC`，浅底用 `#0F172A` / `#1E293B`）；
    4. 字号相比原副标题小字提升 **35% ~ 60%**，在原区域内自动折行并垂直居中绘制精炼后的人味专业文案。

### 3. 图片内真实角标与版权/标准保护 (Image Legitimate Footnote Protection)
- 在对图片进行 OCR 区域检测与清洗分析时，凡命中 `is_protected_domain_footnote` 的文本区域（如图片下方的 `Source: Bloomberg`、`GB/T 1804-m`、`© 2026 Studio`），**其边界框一律排除在擦除掩码（Erase Mask）之外**，坚决避免擦除真实数据源和法律版权声明。

---

## 三、网站与前端页面（HTML / React / Vue / Tailwind）降噪与提权规范 / Web UI De-Slop & Semantic Promotion

### 1. 连盒剥离 AI 伪徽章 (Pill Badge & Kicker Removal)
- **匹配特征**: 带有胶囊外观的装饰容器，如 `<span class="inline-flex items-center rounded-full px-3 py-1 text-xs ...">✨ Next-Gen AI</span>` 或 `<div class="badge badge-outline ...">`。
- **处理规则**: **彻底移除整个外层容器 DOM 节点**（而非仅仅清空内部文字），防止页面上留下空的药丸形状或奇怪的边框占位。

### 2. Bento 卡片减负与主张提权 (Bento Card Elevation)
- **删除冗余副段落**: 匹配卡片内部仅用于同义反复的解释文本（如 `<p class="text-xs text-slate-400 dark:text-slate-500 mt-2">...</p>`），直接删除其 `<p>` 节点。
- **标题样式阶梯提权**:
  - `text-sm font-medium` $\rightarrow$ 提权至 `text-base font-semibold leading-normal`；
  - `text-base font-normal` $\rightarrow$ 提权至 `text-lg font-bold leading-snug tracking-tight text-slate-900 dark:text-slate-100`；
  - `text-lg` $\rightarrow$ 提权至 `text-xl font-bold`。
- **内边距与呼吸感调整**: 适当放大卡片内边距（如 `p-4` $\rightarrow$ `p-5 md:p-6`），使卡片在精炼内容下依然视觉饱满，杜绝 AI 模板常有的逼仄感。

### 3. 清理视觉塑料感与光污染 (Eliminating Plastic Aesthetics & Slop Glow)
- **清除 Emoji 噪音**: 移除按钮、卡片标题前堆砌的 `✨`、`🚀`、`💡`、`⚡`、`🔥`。
- **移除虚假光效**: 剔除 AI 网页模板滥用的廉价渐变光晕（如 `bg-gradient-to-r from-purple-500 to-pink-500 blur-xl opacity-30`）以及伪装成终端状态栏的无意义底部栏（如 `<div class="status-bar">SYSTEM ONLINE // LATENCY 12MS</div>`）。

### 4. 网页真实角标与合规声明的保护与语义化排版 (Web Semantic Footnotes)
- **保护语义标签与合规类名**: 严禁无差别删除 `<small>`、`<footer>`、`<aside>` 内部或带有 `.footnote`、`.citation`、`.legal-disclaimer` 类名的合法内容。
- **去胶囊化与纯净排版 (De-pill & Clean Typography)**:
  - 若合规角标被套上了彩色药丸胶囊类，将其类名清洗为标准的语义化文本：
    ```html
    <!-- 优化前 (AI 塑料风) -->
    <span class="inline-block rounded-full bg-indigo-50 border border-indigo-200 px-3 py-1 text-xs text-indigo-700">
      * 注：依据 ISO 14064-1 标准核算，Scope 1+2 经第三方独立审计
    </span>

    <!-- 优化后 (纯净专业排版) -->
    <p class="text-xs text-slate-500 dark:text-slate-400 mt-4 pt-2 border-t border-slate-100 dark:border-slate-800 leading-relaxed">
      * 注：依据 ISO 14064-1 标准核算，Scope 1+2 经第三方独立审计
    </p>
    ```

---

## 四、文档载体（Word .docx / Markdown）脱壳清理与提权规范 / Document (.docx / .md) Normalization & Promotion

针对长文档、立项报告、学术论文、竞标方案及周报，`doc_cleaner.py` 严格遵循以下排版与脱壳准则：

### 1. 带框引用与提示框脱壳清理 (Callout Box & Admonition Cleaning)
AI 生成 Markdown 或 Word 文档时，极度依赖彩色提示框（Callout / Admonition Box，如 `> [!NOTE]`、`> 💡 核心赋能` 或 Word 中带浅紫/浅蓝底纹的单单元格表格）来承载正确的废话。
- **处理规则**:
  1. **废话同义反复框 $\rightarrow$ 彻底拆解脱壳 (Dissolve Container)**:
     - 若提示框内仅是对正文段落用黑话重新总结（如 `💡 核心洞察：通过全链路协同打造价值闭环...`），直接将提示框的外层表格底纹或引用标记 `>` 剥除；
     - 提炼其中唯一的事实短句融入上下文正文，删掉其余空洞套话。
  2. **高价值论点框 $\rightarrow$ 人味化金句排版 (Promote to Elegant Pull-Quote)**:
     - 严禁使用刺眼的荧光色底纹（如浅粉、鲜绿、高饱和紫）；
     - 采用专业出版物常用的极简左侧单边线排版（见下文第 3 点）。

### 2. 标题层级脱壳与语义提权规范 (Heading Hierarchy Normalization)
AI 生成的文档标题通常充斥着胶囊前缀、方括号伪英文编号与 Emoji：
- **前缀脱壳清洗**:
  - `❌ # [SECTION 01 · STRATEGIC OVERVIEW] 数字化转型战略与赋能路径` $\rightarrow$ `✅ # 数字化转型战略与实施路径`
  - `❌ ## ✨ 【核心闭环】多维协同机制` $\rightarrow$ `✅ ## 多维协同机制`
  - `❌ ### 03 // 落地抓手剖析` $\rightarrow$ `✅ ### 关键执行步骤`
- **Word (`.docx`) 样式等级映射**:
  - `Heading 1`（一级标题）：`18pt ~ 22pt`，加粗，中文字体优先选择思源黑体/黑体，英文字体优先选择 Arial/Helvetica，段前 12pt，段后 6pt。
  - `Heading 2`（二级标题）：`15pt ~ 16pt`，加粗，段前 9pt，段后 4pt。
  - `Heading 3`（三级标题）：`13pt ~ 14pt`，半粗，段前 6pt，段后 2pt。
  - `Body Text`（正文）：`10.5pt ~ 11pt`（五号/小四），行间距固定值 `1.25 ~ 1.35` 倍或 `16pt ~ 20pt`。
- **Markdown 语法规范**:
  - 强制遵循严格的 `#` 至 `###` 递进语义层级，杜绝跳级（如 H1 直接接 H3）。

### 3. 重点金句与高亮区块排版 (Pull-Quote & Highlight Box Styling)
当需要强调关键结论、核心参数或客户原声时，采用克制、高级的版式语言：
- **Word (.docx) 规范**:
  - 移除四周封闭边框与花哨渐变底纹；
  - 仅保留**左侧单条实线边框**（宽度 `2.25pt ~ 3.0pt`，颜色采用低饱和中性深色 `#475569` Slate 或品牌主色 `#2563EB` Navy Blue）；
  - 左侧缩进 `0.5 cm`，背景填充极淡中性灰（`#F8FAFC` 或 `#F1F5F9`）；
  - 文字字号与正文相同（`10.5pt`）或微增至 `11pt`，字重设为半粗或微倾斜。
- **Markdown 规范**:
  - 统一转换为标准 Markdown 引用语法 `>`，首句加粗核心论断：
    ```markdown
    > **实测分选节拍达到 0.2 秒/件**：相比传统人工肉眼挑选，单台设备每日可替代 4 名质检人员，且漏检率控制在 0.3% 以内。
    ```

### 4. 文档原生角标与尾注保护规范 (Document Native Footnote & Citation Preservation)
- **Word 原生脚注/尾注保护**:
  - 严禁篡改或删除文档底层的 `w:footnote`、`w:endnote` XML 节点及其在正文中的引用锚点 `w:footnoteReference`。
  - 确保脚注文字继承正规格式：`9pt`（小五号）宋体 / Times New Roman，单倍行距，顶部保留标准 1/3 页面宽度的脚注分隔线。
- **Markdown 脚注保护**:
  - 严格保护正文中的 `[^1]`、`[^2]` 引用标记与文末的 `[^1]: ISO 9001:2015 质量管理体系认证要求...` 真实定义段落。
  - 杜绝因正则盲目匹配“注：”、“数据来源”而误删文末参考文献。

---

## 五、各载体真假小字与角标处理决策速查表 / Carrier Decision Matrix

| 载体 (Carrier) | 待处理元素类型 | 判定条件 | 处置动作 (Action) | 排版与提权要求 (Styling & Promotion) |
|---|---|---|---|---|
| **PPTX** | 顶部伪英文胶囊标签 | 位于页面/卡片顶部，套有 AutoShape 背景框 | 连盒带字彻底删除 (`delete_shape_ids`) | 页面顶部留白，无需补位 |
| **PPTX** | 卡片内凑数解释小字 | 与卡片标题同义反复，无新增参数 | 仅删除小字段落或副文本框 | 卡片主标题提权 `+2~+4pt`，字重加粗，垂直居中 |
| **PPTX** | 真实标准/法规角标 | 命中 `is_protected_domain_footnote` | **绝对保留文字**，若有背景胶囊则仅拆除背景色块 | 移至页底，字号 `8~9pt`，颜色弱化为 `#64748B` |
| **Image** | 胶囊标签 / 假微数据 | 位于外沿或卡片角标，无实际物理意义 | 无痕擦除 (`erase_only`) | 采样边界环中位数/双线性渐变填充，平滑羽化 |
| **Image** | 黑话卡片标题 + 凑数小字 | 包含核心业务但被黑话与小字包裹 | 擦除并提权重绘 (`erase_and_redraw`) | 提权 35%~60% 字号，选用系统黑体，垂直居中重绘 |
| **Image** | 真实版权与标准声明 | 命中 `is_protected_domain_footnote` | **排除在擦除掩码外** | 完整保留原始图像像素，严禁涂抹 |
| **Web UI** | 伪徽章 / 假状态标签 | `<span class="rounded-full ...">` | 完整删除外层 DOM 节点 | 消除多余外边距与内边距 |
| **Web UI** | Bento 卡片副文本 | 同义反复的 `<p class="text-xs ...">` | 移除 `<p>` 节点 | 主标题提权至 `text-lg font-bold`，卡片 `p-6` |
| **Web UI** | 真实学术/合规角标 | `<small>`, `<footer>`, `.footnote` 等 | **保留语义节点**，清除花哨药丸边框 | 赋予 `text-xs text-slate-500 mt-4 border-t pt-2` |
| **Doc (.docx)** | 彩色同义反复提示框 | 浅色底纹单单元格表格，内容为总结套话 | 脱壳解构表格，融入正文 | 恢复正文常规段落样式，删除重复总结句 |
| **Doc (.docx)** | 重点数据金句 | 包含核心量化参数或重要结论 | 转换为单边线 Pull-Quote | 左侧 2.5pt 浅灰实线，背景 `#F8FAFC`，字号 10.5pt |
| **Doc / MD** | 原生脚注与学术引用 | `w:footnote`, Markdown `[^n]` | **完整保留数据结构** | Word 统一 9pt 宋体/Times，MD 规范锚点连接 |
