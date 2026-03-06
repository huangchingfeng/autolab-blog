#!/usr/bin/env python3
"""Autolab Blog Banner Generator v4 — Pexels 背景版

設計概念：高品質 Pexels 照片背景 + 深色漸層遮罩 + 品牌文字覆蓋
尺寸：1200×630（OG Image / Twitter Card）

v4 更新：
- ARTICLES 從 articles/ 動態掃描，不再寫死
- _draw_text_with_stroke 改用 PIL 內建 stroke_width（效能提升 ~40x）
- .env 改用 python-dotenv
"""

import os
import shutil
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

import yaml

# broll_engine 路徑（共用 Pexels API + 字體工具）
BROLL_DIR = Path(__file__).parent.parent.parent / "04-內容行銷(Marketing)" / "11-youtube-broll(YouTube影片B-Roll)"
sys.path.insert(0, str(BROLL_DIR))

# ============================================================
# 品牌色碼
# ============================================================
DEEP_NAVY = (10, 22, 40)
CYAN = (0, 212, 255)
WHITE = (255, 255, 255)
GRAY_300 = (142, 142, 147)
ACCENT_ORANGE = (255, 107, 53)

W = 1200
H = 630
MARGIN_X = 60

# ============================================================
# 字體（動態偵測，支援 macOS + Linux）
# ============================================================
import platform

def _find_font(names, fallback=""):
    """在常見路徑中搜尋字體"""
    search_dirs = []
    if platform.system() == "Darwin":
        search_dirs = [
            Path.home() / "Library/Fonts",
            Path("/System/Library/Fonts"),
            Path("/Library/Fonts"),
        ]
    else:
        search_dirs = [
            Path("/usr/share/fonts"),
            Path("/usr/local/share/fonts"),
            Path.home() / ".fonts",
        ]
    for name in names:
        for d in search_dirs:
            for p in d.rglob(name):
                return str(p)
    return fallback

FONT_CN_BOLD = _find_font(["NotoSansCJKtc-Bold.otf", "NotoSansCJK-Bold.ttc"])
FONT_CN_BLACK = _find_font(["NotoSansCJKtc-Black.otf", "NotoSansCJK-Black.ttc"], FONT_CN_BOLD)
FONT_CN_MEDIUM = _find_font(["NotoSansCJKtc-Medium.otf", "NotoSansCJK-Medium.ttc"], FONT_CN_BOLD)
FONT_CN_REGULAR = _find_font(["NotoSansCJKtc-Regular.otf", "NotoSansCJK-Regular.ttc"], FONT_CN_BOLD)
FONT_EN = _find_font(["HelveticaNeue.ttc", "Helvetica.ttc", "DejaVuSans.ttf", "Arial.ttf"])

# Tag → Pexels 搜尋關鍵字映射
TAG_TO_QUERY = {
    "AI": "artificial intelligence",
    "AI趨勢": "technology future",
    "AI裁員": "office corporate",
    "AI創業": "startup entrepreneur",
    "AI安全": "cybersecurity",
    "Claude": "artificial intelligence robot",
    "Claude Code": "programming code",
    "Vibe Coding": "software developer coding",
    "職場AI": "business office modern",
    "企業培訓": "corporate training workshop",
    "NotebookLM": "digital notebook technology",
    "AI工具": "technology tools",
    "內容創作": "creative content digital",
    "多元潛能": "creative person diverse",
    "認知交集": "brain creativity",
    "實戰案例": "success business",
    "創業框架": "startup planning",
    "創業": "startup entrepreneur",
    "微軟CEO": "microsoft technology",
    "OpenAI": "artificial intelligence research",
    "Anthropic": "artificial intelligence research",
    "投資": "finance investment chart",
    "AI寫作": "writing creative digital",
    "Cursor": "programming code ide",
    "n8n": "automation workflow technology",
    "自動化": "automation digital workflow",
    "提示詞": "artificial intelligence chat",
    "商業模式": "business strategy planning",
    "Gemini": "artificial intelligence google",
    "ChatGPT": "artificial intelligence chatbot",
    "SatyaNadella": "microsoft technology ceo",
    "JackDorsey": "technology entrepreneur",
    "DarioAmodei": "artificial intelligence research",
    "AI實戰": "technology office modern",
    "AI職場": "office workplace future",
    "Block": "fintech payment technology",
}


def _make_font(path, size, index=0):
    return ImageFont.truetype(path, size, index=index)


def _wrap_text(text, font, max_width):
    """智慧斷行"""
    lines = []
    current = ""
    for ch in text:
        test = current + ch
        bbox = font.getbbox(test)
        tw = bbox[2] - bbox[0]
        if tw > max_width and current:
            lines.append(current.strip())
            current = ch
        else:
            current += ch
    if current.strip():
        lines.append(current.strip())
    return lines


def _draw_text_with_stroke(draw, pos, text, font, fill, stroke_width=2, stroke_fill=(0, 0, 0)):
    """繪製帶描邊的文字（使用 PIL 內建 stroke 參數）"""
    x, y = pos
    draw.text((x, y), text, font=font, fill=fill,
              stroke_width=stroke_width, stroke_fill=stroke_fill)


def _tags_to_query(tags):
    """從文章 tags 推導 Pexels 搜尋關鍵字"""
    if not tags:
        return "technology modern"
    for tag in tags:
        if tag in TAG_TO_QUERY:
            return TAG_TO_QUERY[tag]
    return "technology modern"


def _load_pexels_bg(query, cache_dir, slug):
    """下載 Pexels 照片作為 banner 背景"""
    cache_dir = Path(cache_dir)
    cache_dir.mkdir(parents=True, exist_ok=True)
    cache_path = cache_dir / f"{slug}_bg.jpg"

    try:
        from broll_engine.pexels import pexels_photo
        result = pexels_photo(query, str(cache_path), size="large2x", orientation="landscape")
        if result:
            return Image.open(result).convert("RGB")
    except Exception as e:
        print(f"    Pexels 下載失敗: {e}")

    return None


def _create_gradient_bg():
    """Fallback：CVI 漸層背景"""
    img = Image.new("RGB", (W, H), DEEP_NAVY)
    draw = ImageDraw.Draw(img)
    for y in range(H):
        ratio = y / H
        r = int(DEEP_NAVY[0] + (20 - DEEP_NAVY[0]) * ratio * 0.3)
        g = int(DEEP_NAVY[1] + (35 - DEEP_NAVY[1]) * ratio * 0.3)
        b = int(DEEP_NAVY[2] + (60 - DEEP_NAVY[2]) * ratio * 0.3)
        draw.line([(0, y), (W, y)], fill=(r, g, b))
    return img


def generate_banner(title, tags=None, pexels_query="", subtitle="",
                    slug="banner", output_path="banner.png", cache_dir="/tmp/pexels-blog-cache"):
    """生成 Pexels 背景版品牌 banner（1200×630）

    Args:
        title: 文章標題
        tags: 文章標籤列表
        pexels_query: 自訂 Pexels 搜尋詞（空字串=從 tags 推導）
        subtitle: 副標題（可選）
        slug: 文章 slug（用於快取）
        output_path: 輸出路徑
        cache_dir: Pexels 快取目錄
    """
    # 1. 背景：Pexels 照片 or CVI 漸層
    query = pexels_query or _tags_to_query(tags)
    bg_img = _load_pexels_bg(query, cache_dir, slug)
    has_photo = bg_img is not None

    if bg_img:
        # 裁切到 1200×630 並模糊化
        bg_img = bg_img.resize((max(W, int(bg_img.width * H / bg_img.height)),
                                max(H, int(bg_img.height * W / bg_img.width))),
                               Image.LANCZOS)
        # 居中裁切
        left = (bg_img.width - W) // 2
        top = (bg_img.height - H) // 2
        bg_img = bg_img.crop((left, top, left + W, top + H))
        # 微模糊讓文字更清晰
        bg_img = bg_img.filter(ImageFilter.GaussianBlur(radius=2))
        img = bg_img
    else:
        img = _create_gradient_bg()

    # 2. 深色漸層遮罩（從上到下加深）
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    overlay_draw = ImageDraw.Draw(overlay)
    if has_photo:
        for y in range(H):
            ratio = y / H
            alpha = int(100 + 115 * ratio)
            overlay_draw.line([(0, y), (W, y)], fill=(DEEP_NAVY[0], DEEP_NAVY[1], DEEP_NAVY[2], alpha))
    img = img.convert("RGBA")
    img = Image.alpha_composite(img, overlay)
    img = img.convert("RGB")
    draw = ImageDraw.Draw(img)

    # 3. 文字佈局
    title_font = _make_font(FONT_CN_BLACK, 52)
    sub_font = _make_font(FONT_CN_REGULAR, 20)
    tag_font = _make_font(FONT_CN_MEDIUM, 14)
    brand_font = _make_font(FONT_CN_BOLD, 15)
    brand_en = _make_font(FONT_EN, 14, index=5)
    max_text_w = W - MARGIN_X * 2

    title_lines = _wrap_text(title, title_font, max_text_w)
    if len(title_lines) > 3:
        title_lines = title_lines[:3]
        title_lines[-1] = title_lines[-1][:-2] + "..."

    # 4. 從底部向上佈局 — 品牌條
    bar_y = H - 50
    bar_overlay = Image.new("RGBA", (W, 50), (DEEP_NAVY[0], DEEP_NAVY[1], DEEP_NAVY[2], 180))
    img_rgba = img.convert("RGBA")
    img_rgba.paste(bar_overlay, (0, bar_y), bar_overlay)
    img = img_rgba.convert("RGB")
    draw = ImageDraw.Draw(img)

    draw.text((MARGIN_X, bar_y + 15), "阿峰老師", font=brand_font, fill=CYAN)
    draw.text((MARGIN_X + 70, bar_y + 16), " |  blog.autolab.cloud", font=brand_en, fill=GRAY_300)

    # 5. 標題（底部對齊品牌條上方）
    title_line_h = 68
    title_block_h = len(title_lines) * title_line_h
    title_start_y = bar_y - title_block_h - 20

    # 副標題
    sub_lines = []
    if subtitle:
        sub_lines = _wrap_text(subtitle, sub_font, max_text_w)[:2]
    if sub_lines:
        title_start_y -= (len(sub_lines) * 30 + 12)

    for i, line in enumerate(title_lines):
        y = title_start_y + i * title_line_h
        _draw_text_with_stroke(draw, (MARGIN_X, y), line, title_font, WHITE,
                               stroke_width=3, stroke_fill=(0, 0, 0))

    # 副標題
    if sub_lines:
        sub_y = title_start_y + title_block_h + 8
        for line in sub_lines:
            _draw_text_with_stroke(draw, (MARGIN_X, sub_y), line, sub_font, (220, 220, 225),
                                   stroke_width=1, stroke_fill=(0, 0, 0))
            sub_y += 30

    # 6. Tags（標題上方）
    if tags:
        tag_y = title_start_y - 44
        tag_x = MARGIN_X
        for tag in tags[:3]:
            bbox = tag_font.getbbox(tag)
            tw = bbox[2] - bbox[0] + 20
            th = 26
            tag_bg = Image.new("RGBA", (tw, th), (0, 0, 0, 0))
            tag_draw = ImageDraw.Draw(tag_bg)
            tag_draw.rounded_rectangle([(0, 0), (tw - 1, th - 1)], radius=13,
                                       fill=(255, 255, 255, 40))
            tag_draw.rounded_rectangle([(0, 0), (tw - 1, th - 1)], radius=13,
                                       outline=(CYAN[0], CYAN[1], CYAN[2], 120), width=1)
            img_rgba = img.convert("RGBA")
            img_rgba.paste(tag_bg, (tag_x, tag_y), tag_bg)
            img = img_rgba.convert("RGB")
            draw = ImageDraw.Draw(img)
            draw.text((tag_x + 10, tag_y + 4), tag, font=tag_font, fill=CYAN)
            tag_x += tw + 8

    # 7. 頂部 Cyan 裝飾線
    top_y = min(tag_y - 20 if tags else title_start_y - 20, 40)
    draw.line([(MARGIN_X, top_y), (MARGIN_X + 50, top_y)], fill=CYAN, width=3)

    # 儲存
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(str(output_path), "PNG", optimize=True)
    print(f"  [OK] banner → {output_path.name}")
    return str(output_path)


# ============================================================
# 動態掃描 articles/ 取得文章清單
# ============================================================
HERE = Path(__file__).parent.resolve()
ARTICLES_DIR = HERE / "articles"
BLOG_DIR = HERE / "blog"


def scan_articles_for_banners():
    """從 articles/ 動態掃描文章 meta（不再寫死清單）"""
    articles = []
    for md_file in sorted(ARTICLES_DIR.glob("*.md")):
        text = md_file.read_text()
        if not text.startswith("---"):
            continue
        parts = text.split("---", 2)
        if len(parts) < 3:
            continue
        meta = yaml.safe_load(parts[1]) or {}
        slug = meta.get("slug")
        if not slug:
            continue
        articles.append({
            "slug": slug,
            "title": meta.get("title", slug),
            "subtitle": meta.get("description", ""),
            "tags": meta.get("tags", []),
        })
    return articles


def main():
    """載入 .env 並批次生成全部 banner"""
    # 載入 Pexels API Key（優先用 python-dotenv，fallback 手動解析）
    try:
        from dotenv import load_dotenv
        env_path = BROLL_DIR / ".env"
        if env_path.exists():
            load_dotenv(env_path)
    except ImportError:
        env_path = BROLL_DIR / ".env"
        if env_path.exists():
            for line in open(env_path):
                line = line.strip()
                if "=" in line and not line.startswith("#"):
                    k, v = line.split("=", 1)
                    os.environ[k.strip()] = v.strip().strip("'\"")

    # 動態掃描文章
    articles = scan_articles_for_banners()

    print("=" * 55)
    print("  Autolab Blog Banner Generator v4")
    print(f"  掃描到 {len(articles)} 篇文章")
    print("=" * 55)

    for article in articles:
        slug = article["slug"]
        out_dir = BLOG_DIR / slug
        out_dir.mkdir(parents=True, exist_ok=True)
        generate_banner(
            title=article["title"],
            subtitle=article.get("subtitle", ""),
            tags=article["tags"],
            slug=slug,
            output_path=str(out_dir / "banner.png"),
        )
        # 同時生成 thumbnail.png（向後相容）
        banner_path = out_dir / "banner.png"
        if banner_path.exists():
            shutil.copy2(str(banner_path), str(out_dir / "thumbnail.png"))

    print(f"\n  共生成 {len(articles)} 張品牌 Banner")
    print("=" * 55)


if __name__ == "__main__":
    main()
