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


FONT_CN_BLACK = _find_font(["NotoSansCJKtc-Black.otf", "NotoSansCJK-Black.ttc"])
FONT_CN_BOLD = _find_font(["NotoSansCJKtc-Bold.otf", "NotoSansCJK-Bold.ttc"], FONT_CN_BLACK)
FONT_CN_REGULAR = _find_font(["NotoSansCJKtc-Regular.otf", "NotoSansCJK-Regular.ttc"], FONT_CN_BOLD)
FONT_CN_MEDIUM = _find_font(["NotoSansCJKtc-Medium.otf", "NotoSansCJK-Medium.ttc"], FONT_CN_BOLD)
# 標題用最粗的 Black，沒有 Black 就 fallback 到 Bold
FONT_TITLE = FONT_CN_BLACK or FONT_CN_BOLD


def _font(path, size):
    return ImageFont.truetype(path, size)


# ============================================================
# 智慧斷行（中英文混合，不切斷英文單詞）
# ============================================================

def _wrap_text_smart(text, font, max_width, max_lines=3):
    """智慧斷行：遇到英文單詞不切斷，自動消除孤行"""
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

    # 消除孤行（orphan）：最後一行少於 6 字時，從倒數第二行末尾移字過去
    if len(lines) >= 2:
        last = lines[-1]
        if len(last) < 6 and len(lines[-2]) > 6:
            # 計算需要從倒數第二行移多少字，讓最後一行至少 6 字
            move_count = 6 - len(last)
            prev = lines[-2]
            new_prev = prev[:-move_count].strip()
            new_last = prev[-move_count:] + last
            # 驗證移完後最後一行不超寬
            bbox_last = font.getbbox(new_last)
            if (bbox_last[2] - bbox_last[0]) <= max_width and len(new_prev) >= 4:
                lines[-2] = new_prev
                lines[-1] = new_last

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
    """生成單篇文章的 banner 圖片 (1200x630) — 極簡大字風格

    設計理念（奧美風格）：
    一張 Banner 只說一件事。背景給氣氛，標題給衝擊，品牌色給記憶點。
    只保留 3 個元素：標題文字 + 左側色帶 + 底部微光。
    """
    # 1. 純色深底背景
    img = Image.new("RGB", (BANNER_W, BANNER_H), DEEP_NAVY)
    draw = ImageDraw.Draw(img)

    # 2. 底部 Cyan 微光漸層（極淡，營造高級感）
    overlay = Image.new("RGBA", (BANNER_W, BANNER_H), (0, 0, 0, 0))
    overlay_draw = ImageDraw.Draw(overlay)
    glow_start_y = 480
    for y in range(glow_start_y, BANNER_H):
        ratio = (y - glow_start_y) / (BANNER_H - glow_start_y)
        alpha = int(20 * ratio)  # 最濃也只有 alpha=20，極克制
        overlay_draw.line([(0, y), (BANNER_W, y)],
                          fill=(CYAN[0], CYAN[1], CYAN[2], alpha))
    img = img.convert("RGBA")
    img = Image.alpha_composite(img, overlay)
    img = img.convert("RGB")
    draw = ImageDraw.Draw(img)

    # 3. 左側品牌色帶（5px 寬，全高，品牌識別錨點）
    draw.rectangle([(48, 0), (53, BANNER_H)], fill=CYAN)

    # 4. 標題 — 動態字級，一眼看完
    title_clean = title.strip()
    max_text_w = 1080  # 左右各留 60px
    max_block_h = 500  # 文字區塊最大高度（上下各留 65px）

    # 字級候選列表（固定 3 行，字盡量大）
    size_candidates = [
        (96, 3),   # 大字 3 行
        (88, 3),   # 大字 3 行
        (80, 3),   # 中大字 3 行
        (72, 3),   # 中字 3 行
        (64, 3),   # 中字 3 行
        (56, 3),   # 小字 3 行
        (48, 3),   # 最小 3 行
    ]

    title_font = None
    title_lines = None
    title_size = 56
    line_height = 78

    for size, max_lines in size_candidates:
        test_font = _font(FONT_TITLE, size)
        test_lh = int(size * 1.4)
        test_lines = _wrap_text_smart(title_clean, test_font, max_text_w, max_lines=max_lines + 1)

        # 檢查：是否在 max_lines 行內塞得下（沒被截斷）
        if len(test_lines) <= max_lines:
            block_h = len(test_lines) * test_lh
            if block_h <= max_block_h:
                title_font = test_font
                title_lines = test_lines
                title_size = size
                line_height = test_lh
                break

    # 最終 fallback
    if title_font is None:
        title_size = 48
        title_font = _font(FONT_TITLE, title_size)
        line_height = int(title_size * 1.4)
        title_lines = _wrap_text_smart(title_clean, title_font, max_text_w, max_lines=4)

    # 垂直視覺居中（光學中心比數學中心略低）
    title_block_h = len(title_lines) * line_height
    block_center_y = BANNER_H // 2 + 10  # 光學中心微偏下
    block_top = block_center_y - title_block_h // 2

    # 繪製標題（水平置中，白色大字）
    for i, line in enumerate(title_lines):
        line_center_y = block_top + i * line_height + line_height // 2
        draw.text((BANNER_W // 2, line_center_y), line,
                  font=title_font, fill=WHITE, anchor="mm")

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
