#!/usr/bin/env python3
"""Autolab Blog Banner 圖片生成器

為所有文章生成統一風格的 1200x630 banner 圖片。
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
PADDING = 60

# ============================================================
# 字體（動態偵測，支援 macOS + Linux）— 複製自 generate_article_images.py
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
        # 偵測英文單詞（含數字、連字號、底線、點）
        if ch.isascii() and (ch.isalnum() or ch in "-_."):
            word = ""
            while i < len(text) and text[i].isascii() and (text[i].isalnum() or text[i] in "-_."):
                word += text[i]
                i += 1
            # 測試加上整個單詞後是否超寬
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

    # 限制最多 max_lines 行
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        last = lines[-1]
        if len(last) > 2:
            lines[-1] = last[:-1] + "…"

    return lines


# ============================================================
# 讀取文章 YAML front matter
# ============================================================

def parse_front_matter(md_path):
    """解析 Markdown 檔案的 YAML front matter"""
    content = Path(md_path).read_text(encoding="utf-8")
    match = re.match(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return None
    data = yaml.safe_load(match.group(1))
    return data


def get_all_articles(articles_dir):
    """取得所有文章的 front matter"""
    articles = []
    for md_file in sorted(Path(articles_dir).glob("*.md")):
        data = parse_front_matter(md_file)
        if data and "title" in data and "slug" in data:
            articles.append(data)
    return articles


# ============================================================
# Banner 生成
# ============================================================

def generate_banner(title, tags, date_str, slug, output_dir):
    """生成單篇文章的 banner 圖片 (1200x630)"""
    img = Image.new("RGB", (BANNER_W, BANNER_H), DEEP_NAVY)
    draw = ImageDraw.Draw(img)

    # 1. 背景漸層（從 DEEP_NAVY 到更深的顏色）
    for y in range(BANNER_H):
        ratio = y / BANNER_H
        r = int(DEEP_NAVY[0] * (1 - ratio * 0.4))
        g = int(DEEP_NAVY[1] * (1 - ratio * 0.4))
        b = int(DEEP_NAVY[2] * (1 - ratio * 0.4))
        draw.line([(0, y), (BANNER_W, y)], fill=(r, g, b))

    # 2. 右上角半透明大圓（幾何裝飾）
    overlay = Image.new("RGBA", (BANNER_W, BANNER_H), (0, 0, 0, 0))
    overlay_draw = ImageDraw.Draw(overlay)
    circle_r = 220
    cx, cy = BANNER_W - 80, -40
    overlay_draw.ellipse(
        [(cx - circle_r, cy - circle_r), (cx + circle_r, cy + circle_r)],
        fill=(CYAN[0], CYAN[1], CYAN[2], 18)
    )
    # 第二個較小的圓，增加層次感
    circle_r2 = 120
    cx2, cy2 = BANNER_W - 160, 60
    overlay_draw.ellipse(
        [(cx2 - circle_r2, cy2 - circle_r2), (cx2 + circle_r2, cy2 + circle_r2)],
        fill=(CYAN[0], CYAN[1], CYAN[2], 12)
    )
    img = img.convert("RGBA")
    img = Image.alpha_composite(img, overlay)
    img = img.convert("RGB")
    draw = ImageDraw.Draw(img)

    # 3. 頂部品牌小字
    brand_font = _font(FONT_CN_REGULAR, 14)
    draw.text((PADDING, 50), "阿峰老師 AI 實戰部落格", font=brand_font, fill=GRAY_400)

    # 4. 文章標題（Bold 42px, 自動斷行，最多 3 行）
    title_font = _font(FONT_CN_BOLD, 42)
    max_text_w = BANNER_W - PADDING * 2 - 100  # 右邊留空間給裝飾
    title_lines = _wrap_text_smart(title, title_font, max_text_w, max_lines=3)

    title_y = 110
    line_height = 60
    for line in title_lines:
        draw.text((PADDING, title_y), line, font=title_font, fill=WHITE)
        title_y += line_height

    # 5. 標題下方：前 3 個 tags（pill 形狀，CYAN 邊框+文字）
    tag_font = _font(FONT_CN_REGULAR, 22)
    tag_y = title_y + 30
    tag_x = PADDING
    display_tags = (tags or [])[:3]

    for tag in display_tags:
        bbox = tag_font.getbbox(tag)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        pill_w = tw + 28
        pill_h = th + 18

        # pill 外框
        draw.rounded_rectangle(
            [(tag_x, tag_y), (tag_x + pill_w, tag_y + pill_h)],
            radius=pill_h // 2,
            outline=CYAN,
            width=2
        )
        # pill 文字（置中）
        text_x = tag_x + 14
        text_y = tag_y + 7
        draw.text((text_x, text_y), tag, font=tag_font, fill=CYAN)
        tag_x += pill_w + 16

    # 6. 右下角日期
    date_font = _font(FONT_CN_REGULAR, 18)
    date_display = str(date_str) if date_str else ""
    if date_display:
        date_bbox = date_font.getbbox(date_display)
        date_w = date_bbox[2] - date_bbox[0]
        draw.text(
            (BANNER_W - PADDING - date_w, BANNER_H - 60),
            date_display,
            font=date_font,
            fill=GRAY_400
        )

    # 7. 底部 CYAN 細線裝飾（寬 120px, 3px 高）
    line_y = BANNER_H - 30
    draw.line([(PADDING, line_y), (PADDING + 120, line_y)], fill=CYAN, width=3)

    # 儲存 banner + thumbnail（兩者相同）
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

        print(f"[{i}/{len(articles)}] {slug}")
        print(f"  標題：{title[:50]}{'...' if len(title) > 50 else ''}")

        path = generate_banner(title, tags, date_str, slug, blog_dir)
        print(f"  完成：{path}")

    print(f"\n全部完成！共生成 {len(articles)} 張 banner。")


if __name__ == "__main__":
    main()
