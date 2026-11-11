#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
image_cleaner.py — AI Clean Master 图片载体 (海报 / 信息图 / 截图式 PPT) 无痕去小字与人味大字重绘引擎

支持：
1. --scan <img_path>: 输出图片尺寸、色彩分布概览，供多模态视觉定位 bbox 使用。
2. --apply <plan.json> <img_path> -o <out.png>:
   针对每个 region (bbox: [x1, y1, x2, y2])：
   - 自动采样 bbox 外围像素环，智能采用双线性渐变插值或中位数纯色无痕抹除原有的 AI 小字及胶囊色块；
   - 若 action == "erase_and_redraw"，在擦除后的区域内自动探测系统中文字体（微软雅黑/思源黑体/黑体），
     将精炼提权后的人味大字自动换行并居中/左对齐高清绘制回原图。
"""

import argparse
import json
import sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

# Windows / macOS / Linux 常见高质感无衬线中文字体候选路径
CJK_FONT_CANDIDATES = [
    r"C:\Windows\Fonts\msyhbd.ttc",
    r"C:\Windows\Fonts\msyh.ttc",
    r"C:\Windows\Fonts\simhei.ttf",
    r"C:\Windows\Fonts\dengb.ttf",
    "/System/Library/Fonts/PingFang.ttc",
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc",
    "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
]


def load_cjk_font(font_size: int, bold: bool = True):
    candidates = CJK_FONT_CANDIDATES if bold else CJK_FONT_CANDIDATES[1:] + CJK_FONT_CANDIDATES[:1]
    for fp in candidates:
        if Path(fp).exists():
            try:
                return ImageFont.truetype(fp, size=int(font_size))
            except Exception:
                continue
    return ImageFont.load_default()


def smart_erase_region(img_arr: np.ndarray, bbox: list, pad: int = 4) -> tuple:
    """
    采样 bbox 外扩边框像素，平滑擦除矩形区域内的文字与胶囊背景块，返回修改后的数组及采样背景均值 RGB。
    """
    h, w, c = img_arr.shape
    x1, y1, x2, y2 = [int(round(v)) for v in bbox]
    x1, y1 = max(0, x1), max(0, y1)
    x2, y2 = min(w, x2), min(h, y2)
    if x2 <= x1 or y2 <= y1:
        return img_arr, (255, 255, 255)

    # 采样顶部、底部、左侧、右侧外围像素条
    top_strip = img_arr[max(0, y1 - pad):max(1, y1), x1:x2, :3]
    bot_strip = img_arr[min(h - 1, y2):min(h, y2 + pad), x1:x2, :3]
    left_strip = img_arr[y1:y2, max(0, x1 - pad):max(1, x1), :3]
    right_strip = img_arr[y1:y2, min(w - 1, x2):min(w, x2 + pad), :3]

    top_med = np.median(top_strip.reshape(-1, 3), axis=0) if top_strip.size else np.array([248, 249, 250])
    bot_med = np.median(bot_strip.reshape(-1, 3), axis=0) if bot_strip.size else top_med
    left_med = np.median(left_strip.reshape(-1, 3), axis=0) if left_strip.size else top_med
    right_med = np.median(right_strip.reshape(-1, 3), axis=0) if right_strip.size else left_med

    reg_h = y2 - y1
    reg_w = x2 - x1

    # 构造双线性平滑插值背景块（既适配纯色背景，也适配渐变背景）
    v_grad = np.linspace(0.0, 1.0, reg_h)[:, None, None]
    h_grad = np.linspace(0.0, 1.0, reg_w)[None, :, None]

    v_interp = (1.0 - v_grad) * top_med + v_grad * bot_med
    h_interp = (1.0 - h_grad) * left_med + h_grad * right_med
    patch = np.clip(0.5 * (v_interp + h_interp), 0, 255).astype(np.uint8)

    img_arr[y1:y2, x1:x2, :3] = patch
    avg_bg = tuple(int(v) for v in np.median(patch.reshape(-1, 3), axis=0))
    return img_arr, avg_bg


def wrap_text_lines(draw: ImageDraw.ImageDraw, text: str, font, max_width: int) -> list:
    """按像素宽度自动切分中英文混排文本行"""
    lines = []
    for raw_line in text.split("\n"):
        cur = ""
        for ch in raw_line:
            test = cur + ch
            bbox = draw.textbbox((0, 0), test, font=font)
            if (bbox[2] - bbox[0]) <= max_width or not cur:
                cur = test
            else:
                lines.append(cur)
                cur = ch
        if cur:
            lines.append(cur)
    return lines


def auto_contrast_text_color(bg_rgb: tuple) -> tuple:
    lum = 0.299 * bg_rgb[0] + 0.587 * bg_rgb[1] + 0.114 * bg_rgb[2]
    return (20, 24, 33) if lum > 145 else (248, 250, 252)


def apply_image_plan(img_path: str, plan: dict, output_path: str) -> dict:
    pil_img = Image.open(img_path).convert("RGBA")
    arr = np.array(pil_img)

    stats = {
        "erased_regions": 0,
        "redrawn_regions": 0,
    }

    bg_samples = {}
    for idx, reg in enumerate(plan.get("regions", [])):
        bbox = reg["bbox"]
        arr, avg_bg = smart_erase_region(arr, bbox, pad=reg.get("sample_pad", 4))
        bg_samples[idx] = avg_bg
        stats["erased_regions"] += 1

    cleaned_img = Image.fromarray(arr)
    draw = ImageDraw.Draw(cleaned_img)

    for idx, reg in enumerate(plan.get("regions", [])):
        if reg.get("action") != "erase_and_redraw" or not reg.get("text"):
            continue

        x1, y1, x2, y2 = [int(round(v)) for v in reg["bbox"]]
        box_w = max(20, x2 - x1)
        box_h = max(16, y2 - y1)
        font_size = int(reg.get("font_size") or max(18, min(int(box_h * 0.42), 48)))
        bold = bool(reg.get("bold", True))
        font = load_cjk_font(font_size, bold=bold)

        text_color = reg.get("text_color")
        if isinstance(text_color, list):
            text_color = tuple(text_color)
        elif not text_color:
            text_color = auto_contrast_text_color(bg_samples.get(idx, (255, 255, 255)))

        lines = wrap_text_lines(draw, reg["text"], font, int(box_w * 0.92))
        line_spacing = int(font_size * 0.3)
        line_heights = []
        line_widths = []
        for ln in lines:
            tb = draw.textbbox((0, 0), ln, font=font)
            line_widths.append(tb[2] - tb[0])
            line_heights.append(tb[3] - tb[1])

        total_text_h = sum(line_heights) + line_spacing * max(0, len(lines) - 1)
        align = reg.get("align", "center")
        cur_y = y1 + max(0, (box_h - total_text_h) // 2)

        for ln, lw, lh in zip(lines, line_widths, line_heights):
            if align == "left":
                cur_x = x1 + int(box_w * 0.04)
            else:
                cur_x = x1 + max(0, (box_w - lw) // 2)
            draw.text((cur_x, cur_y), ln, font=font, fill=text_color)
            cur_y += lh + line_spacing

        stats["redrawn_regions"] += 1

    out_p = Path(output_path)
    out_p.parent.mkdir(parents=True, exist_ok=True)
    if out_p.suffix.lower() in (".jpg", ".jpeg"):
        cleaned_img.convert("RGB").save(str(out_p), quality=95)
    else:
        cleaned_img.save(str(out_p))

    stats["output_file"] = str(out_p.resolve())
    return stats


def main():
    parser = argparse.ArgumentParser(description="Erase AI-slop small text/badges and redraw promoted human copy on raster images.")
    parser.add_argument("--scan", dest="scan_img", help="Inspect image dimensions and metadata")
    parser.add_argument("--apply", dest="plan_json", help="Path to JSON region cleanup plan")
    parser.add_argument("input_img", nargs="?", help="Input image path when using --apply")
    parser.add_argument("-o", "--output", help="Output image path")
    args = parser.parse_args()

    if args.scan_img:
        im = Image.open(args.scan_img)
        info = {
            "file": str(Path(args.scan_img).resolve()),
            "width": im.width,
            "height": im.height,
            "mode": im.mode,
            "format": im.format,
        }
        sys.stdout.buffer.write(json.dumps(info, ensure_ascii=False, indent=2).encode("utf-8"))
        sys.stdout.buffer.write(b"\n")
        return

    if args.plan_json and args.input_img:
        in_p = Path(args.input_img)
        out_p = args.output or str(in_p.with_name(f"{in_p.stem}_cleaned{in_p.suffix}"))
        plan = json.loads(Path(args.plan_json).read_text(encoding="utf-8"))
        stats = apply_image_plan(str(in_p), plan, out_p)
        sys.stdout.buffer.write(json.dumps(stats, ensure_ascii=False, indent=2).encode("utf-8"))
        sys.stdout.buffer.write(b"\n")
        return

    parser.print_help()


if __name__ == "__main__":
    main()
