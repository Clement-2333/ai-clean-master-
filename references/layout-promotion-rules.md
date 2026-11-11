# 连盒清理与智能视觉提权规则 (`layout-promotion-rules.md`)

本文档规定 `ai-clean-master` 在清理掉 AI 味小字后，如何**同步清除背后的装饰色块（连盒带字清理）**，以及如何**对保留的核心文字进行视觉提权（Visual Promotion）**，确保修改后的 PPT、图片或网页版面干净、饱满、不空洞。

---

## 一、PPT (`.pptx`) 连盒清理与字号提权规范

### 1. 配对背景框（胶囊框 / 底栏条）几何判定法则
在 AI 生成的 PPT（或由 SVG/HTML 转出的 PPTX）中，顶部眉题小字（Kicker/Badge）或底部总结小字（Footer）往往不是借用 Shape 自带的 `fill`，而是**文字框（TextBox）浮在一个独立的圆角矩形/矩形（AutoShape）之上**。
如果只删除文本框，幻灯片上会留下一个突兀的空胶囊色块或空底栏！

`pptx_inspector.py` 与 `pptx_cleaner.py` 采用以下几何判定准则自动识别并绑定 `paired_bg_shape_id`：
1. **包围盒包含/高重叠（Containment / Overlap）**：
   - 设小字文本框包围盒为 $B_{text} = (x_1, y_1, x_2, y_2)$，候选背景图形包围盒为 $B_{bg} = (X_1, Y_1, X_2, Y_2)$。
   - 交集面积占文本框面积比例：$\text{IoA} = \frac{\text{Area}(B_{text} \cap B_{bg})}{\text{Area}(B_{text})} \ge 0.75$。
2. **尺寸比例约束（防误删大卡片或全屏背景）**：
   - 背景图形本身**不能包含其他非删除的正常文本形状**；
   - 背景图形高度 $H_{bg} \le 2.8 \times H_{text}$ 且 $H_{bg} \le 1.2\text{ inch}$（即属于小胶囊框、小标签条或底栏横条，绝不能是承载正文的整张大卡片或全屏背景图）。
3. **连盒删除执行**：
   - 当某小字文本框被列入删除清单时，其绑定的 `paired_bg_shape_id` 默认一并加入 `delete_shape_ids`，从 Slide XML 树中彻底移除。

### 2. 卡片内删小字后的「智能视觉提权」公式
当卡片内删掉了 1~3 行凑数解释小字（或删除了卡片内的副文本框）后，只剩下卡片主标题/核心短句时：
1. **字号提权（Font Size Promotion）**：
   - 原核心文字字号 $S_{orig} \le 14\text{pt}$ $\rightarrow$ 提权 `+3pt ~ +4pt`（目标 `16pt ~ 18pt`）；
   - 原核心文字字号 $14\text{pt} < S_{orig} \le 18\text{pt}$ $\rightarrow$ 提权 `+2pt ~ +3pt`（目标 `18pt ~ 21pt`）；
   - 原核心文字字号 $S_{orig} > 18\text{pt}$ $\rightarrow$ 提权 `+1pt ~ +2pt`（最高不超过页面主标题字号减去 `4pt`）。
2. **字重与空间重平衡**：
   - 若删除的是同一文本框内的副段落（`delete_paragraphs`），将文本框的垂直对齐属性设为居中（`MSO_ANCHOR.MIDDLE`），或微调文本框 `top` 下移 `0.1 ~ 0.2 inch`，让放大后的核心观点稳居卡片视觉中心。

---

## 二、图片载体（海报 / 信息图 / 截图式 PPT）清理与重绘规范

针对 `.png` / `.jpg` / `.webp` 格式的 AI 生成图片，`image_cleaner.py` 提供像素级无痕清理与提权重绘：

### 1. 无痕背景擦除算法（Smart Background Erase）
给定待清除的小字或胶囊框区域 `bbox = [x1, y1, x2, y2]`：
- **外扩采样环（Border Ring Sampling）**：取 `bbox` 外围 `3px ~ 6px` 的像素环，计算颜色方差与梯度分布：
  - **纯色/微噪点背景**：取采样环的 RGB 中位数（Median Color）填充整个 `bbox`（对外扩 2px 做羽化过渡，彻底盖住原胶囊框边缘抗锯齿噪点）。
  - **线性渐变背景**：分别取 `bbox` 左/右或上/下边缘的中位数颜色，按双线性插值（Bilinear Gradient Fill）平滑填充，还原原图渐变过渡。
  - **复杂纹理背景**：若环境安装了 `opencv-python`，自动调用 `cv2.inpaint`（Telea 算法）进行纹理修复。

### 2. 原位人味大字重绘（Promoted Typography Redraw）
- **仅删除（`action: "erase_only"`）**：适用于顶部伪英文胶囊（`SECTION 01`）、底部免责小字、伪数据角标。擦除后直接还原为干净背景。
- **擦除并提权重绘（`action: "erase_and_redraw"`）**：适用于卡片内「黑话标题 + 凑数小字」合二为一的区域：
  1. 将整个「原黑话标题 + 原凑数小字」的总包围盒一并擦除干净；
  2. 在该总区域内，使用系统高质感无衬线中文字体（自动探测 `微软雅黑 Bold / Microsoft YaHei UI`、`思源黑体`、`黑体`），以比原小字大 **30%~60%** 的字号自动换行并垂直居中绘制精炼后的人味文案。

---

## 三、网站与前端页面（HTML / React / Vue / Tailwind）降噪与提权规范

1. **连盒剥离 AI 伪徽章（Pill Badge Removal）**：
   - 匹配包含伪英文/状态套话的 `<span class="... rounded-full ...">` 或 `<div class="... badge ...">` 节点，直接移除整个外层标签节点（而非仅清空内部文字）。
2. **Bento 卡片减负与核心观点提权**：
   - 移除卡片内仅作同义反复的 `<p class="text-xs text-slate-400 ...">` 或 `<p class="text-sm text-gray-500 ...">` 节点；
   - 将卡片内保留的核心标题/结论从 `text-base` 升级为 `text-lg font-semibold leading-snug`（或从 `text-lg` 升级为 `text-xl font-bold`），增加卡片内边距（如 `p-5` $\rightarrow$ `p-6`），让卡片靠精炼有力的文字本身撑起视觉质感。
3. **清除视觉塑料感**：
   - 自动清理文案中堆砌的 `✨🚀💡⚡🔥` 等 AI 强迫症 Emoji；
   - 移除包裹小字的无意义霓虹发光边框或底部假命令行状态栏。
