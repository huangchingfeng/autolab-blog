#!/usr/bin/env python3
"""Autolab Blog 文章內圖片生成器

兩種圖片類型：
A. 資訊圖表（PIL 生成，CVI 品牌風格）— key_points_card, comparison_card, quote_card, steps_card
B. Pexels 配圖（下載 + 品牌化處理）— section_image

所有圖片寬度 1200px，深色品牌風格。
"""

import os
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# broll_engine 路徑（共用 Pexels API）
BROLL_DIR = Path(__file__).parent.parent.parent / "04-內容行銷(Marketing)" / "11-youtube-broll(YouTube影片B-Roll)"
sys.path.insert(0, str(BROLL_DIR))

# ============================================================
# 品牌色碼
# ============================================================
DEEP_NAVY = (10, 22, 40)
CARD_BG = (15, 29, 50)
CYAN = (0, 212, 255)
WHITE = (255, 255, 255)
GRAY_200 = (199, 199, 204)
GRAY_400 = (99, 99, 102)
ACCENT_ORANGE = (255, 107, 53)

IMG_W = 1200
PADDING = 60

# ============================================================
# 字體
# ============================================================
FONT_CN_BOLD = "/Users/huangjingfeng/Library/Fonts/NotoSansCJKtc-Bold.otf"
FONT_CN_REGULAR = "/Users/huangjingfeng/Library/Fonts/NotoSansCJKtc-Regular.otf"
FONT_CN_MEDIUM = "/Users/huangjingfeng/Library/Fonts/NotoSansCJKtc-Medium.otf"


def _font(path, size):
    return ImageFont.truetype(path, size)


def _wrap_text(text, font, max_width):
    """智慧斷行"""
    lines = []
    current = ""
    for ch in text:
        test = current + ch
        bbox = font.getbbox(test)
        if (bbox[2] - bbox[0]) > max_width and current:
            lines.append(current.strip())
            current = ch
        else:
            current += ch
    if current.strip():
        lines.append(current.strip())
    return lines


def _brand_footer(draw, y, width):
    """底部品牌小字"""
    font = _font(FONT_CN_REGULAR, 14)
    text = "阿峰老師 | autolab.cloud"
    draw.text((PADDING, y), text, font=font, fill=GRAY_400)
    return y + 30


# ============================================================
# A. 資訊圖表
# ============================================================

def generate_key_points_card(title, points, output_path, width=IMG_W):
    """重點摘要卡片

    Args:
        title: 卡片標題
        points: 要點列表 ["重點一", "重點二", ...]
        output_path: 輸出路徑
    """
    title_font = _font(FONT_CN_BOLD, 32)
    point_font = _font(FONT_CN_REGULAR, 24)
    max_text_w = width - PADDING * 2 - 40  # 留空間給圓點

    # 計算高度
    title_lines = _wrap_text(title, title_font, width - PADDING * 2)
    point_lines_list = [_wrap_text(p, point_font, max_text_w) for p in points]

    h = PADDING  # 頂部
    h += len(title_lines) * 44 + 20  # 標題
    h += 4  # cyan 分隔線
    h += 24  # 間距
    for pl in point_lines_list:
        h += len(pl) * 36 + 16  # 每個要點
    h += 20  # 底部間距
    h += 40  # 品牌 footer
    h += PADDING  # 底部

    # 繪製
    img = Image.new("RGB", (width, h), DEEP_NAVY)
    draw = ImageDraw.Draw(img)

    # 卡片背景（圓角）
    draw.rounded_rectangle(
        [(PADDING - 20, PADDING - 20), (width - PADDING + 20, h - PADDING + 10)],
        radius=16, fill=CARD_BG
    )

    # Cyan 上邊框
    draw.rounded_rectangle(
        [(PADDING - 20, PADDING - 20), (width - PADDING + 20, PADDING - 16)],
        radius=16, fill=CYAN
    )

    y = PADDING

    # 標題
    for line in title_lines:
        draw.text((PADDING, y), line, font=title_font, fill=WHITE)
        y += 44
    y += 12

    # Cyan 分隔線
    draw.line([(PADDING, y), (PADDING + 80, y)], fill=CYAN, width=3)
    y += 24

    # 要點
    for i, (point, lines) in enumerate(zip(points, point_lines_list)):
        # Cyan 圓點
        dot_y = y + 10
        draw.ellipse([(PADDING + 4, dot_y), (PADDING + 16, dot_y + 12)], fill=CYAN)
        # 文字
        for j, line in enumerate(lines):
            draw.text((PADDING + 32, y), line, font=point_font, fill=GRAY_200)
            y += 36
        y += 16

    y += 4
    _brand_footer(draw, y, width)

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    img.save(output_path, "PNG", quality=95)
    return output_path


def generate_comparison_card(title, left_label, right_label,
                             left_items, right_items, output_path, width=IMG_W):
    """左右對比卡片（Before/After）"""
    title_font = _font(FONT_CN_BOLD, 30)
    label_font = _font(FONT_CN_BOLD, 24)
    item_font = _font(FONT_CN_REGULAR, 22)

    n_items = max(len(left_items), len(right_items))
    h = PADDING + 50 + 50 + n_items * 42 + 60 + PADDING

    img = Image.new("RGB", (width, h), DEEP_NAVY)
    draw = ImageDraw.Draw(img)

    # 卡片背景
    draw.rounded_rectangle(
        [(PADDING - 20, PADDING - 20), (width - PADDING + 20, h - PADDING + 10)],
        radius=16, fill=CARD_BG
    )

    y = PADDING

    # 標題
    draw.text((PADDING, y), title, font=title_font, fill=WHITE)
    y += 50

    # 中線
    mid_x = width // 2

    # 左右標籤
    draw.text((PADDING + 20, y), left_label, font=label_font, fill=ACCENT_ORANGE)
    draw.text((mid_x + 20, y), right_label, font=label_font, fill=CYAN)
    y += 44

    # 分隔線
    draw.line([(mid_x, y - 10), (mid_x, h - PADDING - 30)], fill=GRAY_400, width=1)

    # 項目
    for i in range(n_items):
        if i < len(left_items):
            draw.text((PADDING + 20, y), f"• {left_items[i]}", font=item_font, fill=GRAY_200)
        if i < len(right_items):
            draw.text((mid_x + 20, y), f"• {right_items[i]}", font=item_font, fill=GRAY_200)
        y += 42

    y += 10
    _brand_footer(draw, y, width)

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    img.save(output_path, "PNG", quality=95)
    return output_path


def generate_quote_card(quote, author, output_path, width=IMG_W):
    """金句卡片"""
    quote_font = _font(FONT_CN_BOLD, 36)
    author_font = _font(FONT_CN_REGULAR, 20)
    max_w = width - PADDING * 2 - 40

    quote_lines = _wrap_text(quote, quote_font, max_w)
    h = PADDING + 30 + len(quote_lines) * 52 + 30 + 30 + 50 + PADDING

    img = Image.new("RGB", (width, h), DEEP_NAVY)
    draw = ImageDraw.Draw(img)

    # 卡片背景
    draw.rounded_rectangle(
        [(PADDING - 20, PADDING - 20), (width - PADDING + 20, h - PADDING + 10)],
        radius=16, fill=CARD_BG
    )

    y = PADDING

    # 大引號裝飾
    big_quote_font = _font(FONT_CN_BOLD, 72)
    draw.text((PADDING, y - 10), "“", font=big_quote_font, fill=CYAN)
    y += 40

    # 引言文字
    for line in quote_lines:
        draw.text((PADDING + 20, y), line, font=quote_font, fill=WHITE)
        y += 52
    y += 20

    # 作者
    draw.text((PADDING + 20, y), f"— {author}", font=author_font, fill=CYAN)
    y += 40

    _brand_footer(draw, y, width)

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    img.save(output_path, "PNG", quality=95)
    return output_path


def generate_steps_card(title, steps, output_path, width=IMG_W):
    """流程步驟卡片

    Args:
        steps: [("步驟標題", "說明"), ...]
    """
    title_font = _font(FONT_CN_BOLD, 30)
    step_title_font = _font(FONT_CN_BOLD, 24)
    step_desc_font = _font(FONT_CN_REGULAR, 20)

    h = PADDING + 50 + len(steps) * 80 + 50 + PADDING

    img = Image.new("RGB", (width, h), DEEP_NAVY)
    draw = ImageDraw.Draw(img)

    draw.rounded_rectangle(
        [(PADDING - 20, PADDING - 20), (width - PADDING + 20, h - PADDING + 10)],
        radius=16, fill=CARD_BG
    )

    y = PADDING
    draw.text((PADDING, y), title, font=title_font, fill=WHITE)
    y += 50

    for i, (step_title, step_desc) in enumerate(steps):
        # 數字圓圈
        cx = PADDING + 20
        cy = y + 12
        draw.ellipse([(cx - 14, cy - 14), (cx + 14, cy + 14)], fill=CYAN)
        num_font = _font(FONT_CN_BOLD, 18)
        draw.text((cx - 5, cy - 11), str(i + 1), font=num_font, fill=DEEP_NAVY)

        # 步驟標題 + 說明
        draw.text((PADDING + 50, y), step_title, font=step_title_font, fill=WHITE)
        y += 34
        draw.text((PADDING + 50, y), step_desc, font=step_desc_font, fill=GRAY_200)
        y += 42

        # 連接線（最後一步不畫）
        if i < len(steps) - 1:
            draw.line([(cx, cy + 14), (cx, cy + 52)], fill=CYAN, width=2)

    y += 10
    _brand_footer(draw, y, width)

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    img.save(output_path, "PNG", quality=95)
    return output_path


# ============================================================
# B. Pexels 配圖
# ============================================================

def generate_section_image(query, caption, output_path, width=IMG_W, height=675):
    """Pexels 配圖 + 品牌化處理

    Args:
        query: Pexels 搜尋關鍵字
        caption: 底部字幕
        output_path: 輸出路徑
    """
    try:
        from broll_engine.pexels import pexels_photo
    except ImportError:
        print("    無法 import pexels_photo，跳過配圖生成")
        return ""

    # 下載照片
    cache_path = str(Path(output_path).parent / f"_pexels_{Path(output_path).stem}.jpg")
    photo_path = pexels_photo(query, cache_path, size="large2x", orientation="landscape")

    if not photo_path:
        return ""

    # 載入並裁切到目標尺寸
    img = Image.open(photo_path).convert("RGB")
    img = img.resize((max(width, int(img.width * height / img.height)),
                       max(height, int(img.height * width / img.width))),
                      Image.LANCZOS)
    left = (img.width - width) // 2
    top = (img.height - height) // 2
    img = img.crop((left, top, left + width, top + height))

    # 底部漸層遮罩
    overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    overlay_draw = ImageDraw.Draw(overlay)
    for y in range(height - 120, height):
        ratio = (y - (height - 120)) / 120
        alpha = int(180 * ratio)
        overlay_draw.line([(0, y), (width, y)], fill=(0, 0, 0, alpha))

    img = img.convert("RGBA")
    img = Image.alpha_composite(img, overlay)

    # 底部字幕
    if caption:
        draw = ImageDraw.Draw(img)
        caption_font = _font(FONT_CN_REGULAR, 18)
        draw.text((24, height - 40), caption, font=caption_font, fill=(255, 255, 255, 220))

    img = img.convert("RGB")

    # 圓角裁切
    mask = Image.new("L", (width, height), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.rounded_rectangle([(0, 0), (width - 1, height - 1)], radius=16, fill=255)
    result = Image.new("RGB", (width, height), DEEP_NAVY)
    result.paste(img, mask=mask)

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    result.save(output_path, "PNG", quality=95)

    # 清理快取照片
    if os.path.exists(cache_path):
        os.remove(cache_path)

    return output_path


# ============================================================
# CLI 測試
# ============================================================
if __name__ == "__main__":
    out_dir = "/tmp/blog-article-images-test"
    os.makedirs(out_dir, exist_ok=True)

    print("測試 key_points_card...")
    generate_key_points_card(
        title="AI 時代職場生存的三大關鍵",
        points=[
            "學會用 AI 工具不是選擇，是生存條件",
            "不可取代區 = 你的判斷力 + AI 執行力",
            "持續學習的速度 > 你目前的技術深度",
        ],
        output_path=f"{out_dir}/key_points.png",
    )

    print("測試 comparison_card...")
    generate_comparison_card(
        title="AI 改變的不是人，是工作方式",
        left_label="以前",
        right_label="現在",
        left_items=["手動整理報表", "寫 Email 花 30 分鐘", "一個人做研究"],
        right_items=["AI 自動分析", "AI 5 分鐘搞定", "AI 協作加速 10x"],
        output_path=f"{out_dir}/comparison.png",
    )

    print("測試 quote_card...")
    generate_quote_card(
        quote="你是機長，AI 是機組人員。你決定目的地，AI 幫你安全抵達。",
        author="阿峰老師",
        output_path=f"{out_dir}/quote.png",
    )

    print("測試 steps_card...")
    generate_steps_card(
        title="5 步工作拆解法",
        steps=[
            ("盤點工作內容", "列出你每週做的所有任務"),
            ("標記 AI 可替代項目", "哪些是重複性、規則明確的？"),
            ("找出判斷力密集區", "需要經驗、直覺、人際的工作"),
            ("設計人機協作流程", "AI 做初稿，你做最終決策"),
            ("持續迭代優化", "每週回顧一次，持續調整"),
        ],
        output_path=f"{out_dir}/steps.png",
    )

    print(f"\n測試完成！圖片在 {out_dir}/")
