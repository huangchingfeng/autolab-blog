#!/usr/bin/env python3
"""Autolab Blog Banner 圖片生成器

為所有文章生成統一風格的 1200x630 banner 圖片。
設計風格：大字置中、醒目、一眼看懂
用法：
  python3 generate_banners.py            # 全部重新生成
  python3 generate_banners.py --slug xxx # 只生成單篇
"""

import argparse
import os
import platform
import re
import shutil
import yaml
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

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

BANNER_W = 1200
BANNER_H = 630

# ============================================================
# 字體（動態偵測，支援 macOS + Linux）
# ============================================================

def _find_font(names, fallback=""):
    search_dirs = []
    if platform.system() == "Darwin":
        search_dirs = [Path.home() / "Library/Fonts", Path("/System/Library/Fonts"), Path("/Library/Fonts")]
    else:
        search_dirs = [Path("/usr/share/fonts"), Path("/usr/local/share/fonts"), Path.home() / ".fonts"]
    for name in names:
        for d in search_dirs:
            for p in d.rglob(name):
                return str(p)
    return fallback


FONT_CN_BOLD = _find_font(["NotoSansCJKtc-Bold.otf", "NotoSansCJK-Bold.ttc"])
FONT_CN_REGULAR = _find_font(["NotoSansCJKtc-Regular.otf", "NotoSansCJK-Regular.ttc"], FONT_CN_BOLD)
FONT_CN_MEDIUM = _find_font(["NotoSansCJKtc-Medium.otf", "NotoSansCJK-Medium.ttc"], FONT_CN_BOLD)


def _font(path, size):
    return ImageFont.truetype(path, size)


# ============================================================
# 智慧斷行（中英文混合，不切斷英文單詞）
# ============================================================

def _wrap_text_smart(text, font, max_width, max_lines=3):
    """智慧斷行：遇到英文單詞不切斷"""
    lines = []
    current = ""
    i = 0
    while i < len(text):
        ch = text[i]
        if ch.isascii() and (ch.isalnum() or ch in "-_."):
            word = ""
            while i < len(text) and text[i].isascii() and (text[i].isalnum() or text[i] in "-_."):
                word += text[i]
                i += 1
            test = current + word
            bbox = font.getbbox(test)
            if (bbox[2] - bbox[0]) > max_width and current.strip():
                lines.append(current.strip())
                current = word
            else:
                current = test
        else:
            test = current + ch
            bbox = font.getbbox(test)
            if (bbox[2] - bbox[0]) > max_width and current.strip():
                lines.append(current.strip())
                current = ch
            else:
                current = test
            i += 1

    if current.strip():
        lines.append(current.strip())

    if len(lines) > max_lines:
        lines = lines[:max_lines]
        last = lines[-1]
        if len(last) > 2:
            lines[-1] = last[:-1] + "…"

    return lines


def _text_width(draw, text, font):
    bbox = font.getbbox(text)
    return bbox[2] - bbox[0]


def _text_height(draw, text, font):
    bbox = font.getbbox(text)
    return bbox[3] - bbox[1]


# ============================================================
# 讀取文章 YAML front matter
# ============================================================

def parse_front_matter(md_path):
    content = Path(md_path).read_text(encoding="utf-8")
    match = re.match(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return None
    data = yaml.safe_load(match.group(1))
    return data


def get_all_articles(articles_dir):
    articles = []
    for md_file in sorted(Path(articles_dir).glob("*.md")):
        data = parse_front_matter(md_file)
        if data and "title" in data and "slug" in data:
            articles.append(data)
    return articles


# ============================================================
# Banner 生成 — 大字置中風格
# ============================================================

def generate_banner(title, tags, date_str, slug, description, output_dir):
    """生成單篇文章的 banner 圖片 (1200x630) — 大字置中風格"""
    img = Image.new("RGB", (BANNER_W, BANNER_H), DEEP_NAVY)
    draw = ImageDraw.Draw(img)

    # 1. 背景漸層
    for y in range(BANNER_H):
        ratio = y / BANNER_H
        r = int(DEEP_NAVY[0] * (1 - ratio * 0.3))
        g = int(DEEP_NAVY[1] * (1 - ratio * 0.3))
        b = int(DEEP_NAVY[2] * (1 - ratio * 0.3))
        draw.line([(0, y), (BANNER_W, y)], fill=(r, g, b))

    # 2. 微弱幾何裝飾（比之前更淡）
    overlay = Image.new("RGBA", (BANNER_W, BANNER_H), (0, 0, 0, 0))
    overlay_draw = ImageDraw.Draw(overlay)
    overlay_draw.ellipse(
        [(BANNER_W - 300, -100), (BANNER_W + 100, 300)],
        fill=(CYAN[0], CYAN[1], CYAN[2], 12)
    )
    overlay_draw.ellipse(
        [(-100, BANNER_H - 200), (200, BANNER_H + 100)],
        fill=(CYAN[0], CYAN[1], CYAN[2], 8)
    )
    img = img.convert("RGBA")
    img = Image.alpha_composite(img, overlay)
    img = img.convert("RGB")
    draw = ImageDraw.Draw(img)

    # 3. 計算整體垂直佈局（置中）
    # 結構：分類標籤 → 主標題（大字）→ 副標題/描述 → 底線

    # 分類標籤（第一個 tag）
    tag_label = tags[0] if tags else "AI 實戰"
    tag_font = _font(FONT_CN_BOLD, 18)

    # 主標題 — 動態字體大小（根據標題長度調整）
    title_clean = title.strip()
    if len(title_clean) <= 15:
        title_size = 72
        max_lines = 2
    elif len(title_clean) <= 25:
        title_size = 64
        max_lines = 2
    elif len(title_clean) <= 40:
        title_size = 56
        max_lines = 3
    else:
        title_size = 48
        max_lines = 3

    title_font = _font(FONT_CN_BOLD, title_size)
    line_height = int(title_size * 1.35)
    max_text_w = BANNER_W - 160  # 左右各留 80px

    title_lines = _wrap_text_smart(title_clean, title_font, max_text_w, max_lines=max_lines)

    # 副標題（description，限制在畫面寬度內）
    desc_font = _font(FONT_CN_REGULAR, 22)
    desc_max_w = BANNER_W - 200  # 左右各留 100px
    desc_text = ""
    if description:
        # 逐字計算，確保不超出寬度
        for ch in description:
            test = desc_text + ch
            tw = _text_width(draw, test + "…", desc_font)
            if tw > desc_max_w:
                desc_text += "…"
                break
            desc_text = test
        else:
            # 沒超出，不加省略號
            pass

    # 計算總高度來做垂直置中
    tag_h = 32
    gap_tag_title = 24
    title_block_h = len(title_lines) * line_height
    gap_title_desc = 28
    desc_h = 30 if desc_text else 0
    gap_desc_line = 30
    line_deco_h = 4

    total_h = tag_h + gap_tag_title + title_block_h + gap_title_desc + desc_h + gap_desc_line + line_deco_h
    start_y = (BANNER_H - total_h) // 2

    # 4. 繪製分類標籤 pill（置中）
    tag_tw = _text_width(draw, tag_label, tag_font)
    pill_w = tag_tw + 32
    pill_h = 32
    pill_x = (BANNER_W - pill_w) // 2
    pill_y = start_y

    # pill 背景（深色半透明效果）
    pill_bg = (20, 50, 65)
    draw.rounded_rectangle(
        [(pill_x, pill_y), (pill_x + pill_w, pill_y + pill_h)],
        radius=pill_h // 2,
        fill=pill_bg,
        outline=CYAN,
        width=2
    )
    draw.text(
        (pill_x + 16, pill_y + 5),
        tag_label,
        font=tag_font,
        fill=CYAN
    )

    # 5. 繪製主標題（大字 Bold，置中）
    title_y = pill_y + pill_h + gap_tag_title
    for line in title_lines:
        lw = _text_width(draw, line, title_font)
        lx = (BANNER_W - lw) // 2
        draw.text((lx, title_y), line, font=title_font, fill=WHITE)
        title_y += line_height

    # 6. 繪製副標題描述（CYAN 色，置中）
    if desc_text:
        desc_y = title_y + gap_title_desc
        dw = _text_width(draw, desc_text, desc_font)
        dx = (BANNER_W - dw) // 2
        draw.text((dx, desc_y), desc_text, font=desc_font, fill=CYAN)
        current_y = desc_y + desc_h
    else:
        current_y = title_y

    # 7. 底部 CYAN 短線裝飾（置中）
    line_w = 80
    line_y = current_y + gap_desc_line
    line_x = (BANNER_W - line_w) // 2
    draw.line([(line_x, line_y), (line_x + line_w, line_y)], fill=CYAN, width=4)

    # 8. 左下角品牌小字
    brand_font = _font(FONT_CN_REGULAR, 16)
    draw.text((40, BANNER_H - 50), "阿峰老師 Autolab", font=brand_font, fill=GRAY_400)

    # 9. 右下角日期
    if date_str:
        date_font = _font(FONT_CN_REGULAR, 16)
        date_display = str(date_str)
        date_w = _text_width(draw, date_display, date_font)
        draw.text(
            (BANNER_W - 40 - date_w, BANNER_H - 50),
            date_display,
            font=date_font,
            fill=GRAY_400
        )

    # 儲存 banner + thumbnail
    slug_dir = Path(output_dir) / slug
    slug_dir.mkdir(parents=True, exist_ok=True)

    banner_path = slug_dir / "banner.png"
    thumbnail_path = slug_dir / "thumbnail.png"

    img.save(str(banner_path), "PNG", quality=95)
    shutil.copy2(str(banner_path), str(thumbnail_path))

    return str(banner_path)


# ============================================================
# CLI
# ============================================================

def main():
    parser = argparse.ArgumentParser(description="生成部落格 banner 圖片")
    parser.add_argument("--slug", type=str, help="只生成指定 slug 的 banner")
    args = parser.parse_args()

    base_dir = Path(__file__).parent
    articles_dir = base_dir / "articles"
    blog_dir = base_dir / "blog"

    articles = get_all_articles(articles_dir)
    if not articles:
        print("找不到任何文章！")
        return

    if args.slug:
        articles = [a for a in articles if a.get("slug") == args.slug]
        if not articles:
            print(f"找不到 slug 為 '{args.slug}' 的文章")
            return

    print(f"準備生成 {len(articles)} 篇文章的 banner...\n")

    for i, article in enumerate(articles, 1):
        title = article.get("title", "無標題")
        tags = article.get("tags", [])
        date_str = article.get("date", "")
        slug = article.get("slug", "")
        description = article.get("description", "")

        print(f"[{i}/{len(articles)}] {slug}")
        print(f"  標題：{title[:50]}{'...' if len(title) > 50 else ''}")

        path = generate_banner(title, tags, date_str, slug, description, blog_dir)
        print(f"  完成：{path}")

    print(f"\n全部完成！共生成 {len(articles)} 張 banner。")


if __name__ == "__main__":
    main()
