#!/usr/bin/env python3
"""Autolab Blog Banner Generator — 奧美品牌顧問級 v2
設計概念：「駕駛艙儀表板」— 深色空間裡的發光儀表板，傳遞掌控感、專業、精準。

v2 修正：
- 改用 W8 字體（W9 有缺字問題）
- 垂直置中佈局：內容不再擠在上方
- 底部品牌列加粗加大
"""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

# ============================================================
# 品牌色碼
# ============================================================
DEEP_NAVY = (10, 22, 40)
NAVY_2 = (15, 29, 50)
NAVY_3 = (21, 32, 53)
NAVY_4 = (27, 42, 69)
CYAN = (0, 212, 255)
WHITE = (255, 255, 255)
GRAY_200 = (199, 199, 204)
GRAY_300 = (142, 142, 147)
GRAY_400 = (99, 99, 102)
ACCENT_ORANGE = (255, 107, 53)

# 品牌 Badge 背景色（模擬 Cyan 12% on Deep Navy）
BADGE_BG = (12, 47, 70)

# ============================================================
# 字體
# ============================================================
FONT_CN_BLACK = "/Users/huangjingfeng/Library/Fonts/NotoSansCJKtc-Black.otf"
FONT_CN_BOLD = "/Users/huangjingfeng/Library/Fonts/NotoSansCJKtc-Bold.otf"
FONT_CN_MEDIUM = "/Users/huangjingfeng/Library/Fonts/NotoSansCJKtc-Medium.otf"
FONT_CN_REGULAR = "/Users/huangjingfeng/Library/Fonts/NotoSansCJKtc-Regular.otf"
FONT_EN = "/System/Library/Fonts/HelveticaNeue.ttc"

W = 1200
H = 630
MARGIN_X = 80
BRAND_BAR_H = 70  # 底部品牌列高度


def make_font(path, size, index=0):
    return ImageFont.truetype(path, size, index=index)


def draw_rounded_rect(draw, xy, radius, fill=None):
    """繪製圓角矩形"""
    x1, y1, x2, y2 = xy
    r = min(radius, (y2 - y1) // 2, (x2 - x1) // 2)
    draw.pieslice([x1, y1, x1 + 2*r, y1 + 2*r], 180, 270, fill=fill)
    draw.pieslice([x2 - 2*r, y1, x2, y1 + 2*r], 270, 360, fill=fill)
    draw.pieslice([x1, y2 - 2*r, x1 + 2*r, y2], 90, 180, fill=fill)
    draw.pieslice([x2 - 2*r, y2 - 2*r, x2, y2], 0, 90, fill=fill)
    draw.rectangle([x1 + r, y1, x2 - r, y2], fill=fill)
    draw.rectangle([x1, y1 + r, x2, y2 - r], fill=fill)


def draw_glow(img, cx, cy, radius, color, intensity=0.08):
    """繪製柔和光暈效果"""
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    steps = 50
    for i in range(steps, 0, -1):
        ratio = i / steps
        r = int(radius * ratio)
        alpha = int(255 * intensity * (1 - ratio))
        c = color + (alpha,)
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=c)
    img.paste(Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB"))


def wrap_text(text, font, max_width):
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


def generate_banner(title, subtitle, tags, slug, output_dir):
    """生成單張品牌 banner"""
    img = Image.new("RGB", (W, H), DEEP_NAVY)
    draw = ImageDraw.Draw(img)

    # === 背景光暈 ===
    draw_glow(img, W - 80, 60, 450, CYAN, intensity=0.035)
    draw_glow(img, 80, H - 80, 300, ACCENT_ORANGE, intensity=0.018)
    draw = ImageDraw.Draw(img)

    # === 計算佈局（垂直置中） ===
    title_font = make_font(FONT_CN_BLACK, 48)
    sub_font = make_font(FONT_CN_REGULAR, 20)
    tag_font = make_font(FONT_CN_MEDIUM, 14)
    max_text_w = W - MARGIN_X * 2

    title_lines = wrap_text(title, title_font, max_text_w)
    if len(title_lines) > 3:
        title_lines = title_lines[:3]
        title_lines[-1] = title_lines[-1][:-2] + "..."

    sub_lines = []
    if subtitle:
        sub_lines = wrap_text(subtitle, sub_font, max_text_w)[:2]

    # 計算內容總高度
    tag_block_h = 36  # tag badges 高度
    title_line_h = 64
    sub_line_h = 32
    gap_tag_title = 24
    gap_title_sub = 20

    content_h = tag_block_h + gap_tag_title
    content_h += len(title_lines) * title_line_h
    if sub_lines:
        content_h += gap_title_sub + len(sub_lines) * sub_line_h

    # 可用區域：頂部 40px ~ 底部品牌列上方 20px
    avail_top = 40
    avail_bottom = H - BRAND_BAR_H - 20
    avail_h = avail_bottom - avail_top

    # 垂直置中偏上（視覺重心偏上更舒服）
    start_y = avail_top + max(0, (avail_h - content_h) // 2 - 20)

    # === 頂部 Cyan 裝飾線 ===
    draw.line([(MARGIN_X, start_y), (MARGIN_X + 50, start_y)], fill=CYAN, width=3)

    # === Tag badges ===
    tag_x = MARGIN_X
    tag_y = start_y + 14
    for tag in (tags[:3] if tags else []):
        bbox = tag_font.getbbox(tag)
        tw = bbox[2] - bbox[0] + 24
        th = 28
        draw_rounded_rect(draw,
                          (tag_x, tag_y, tag_x + tw, tag_y + th),
                          radius=14,
                          fill=BADGE_BG)
        # 1px Cyan 邊框模擬
        draw.rounded_rectangle(
            [(tag_x, tag_y), (tag_x + tw, tag_y + th)],
            radius=14,
            outline=(0, 80, 100),
            width=1
        )
        draw.text((tag_x + 12, tag_y + 5), tag, font=tag_font, fill=CYAN)
        tag_x += tw + 10

    # === 標題 ===
    title_y = tag_y + tag_block_h + gap_tag_title - 14
    for line in title_lines:
        draw.text((MARGIN_X, title_y), line, font=title_font, fill=WHITE)
        title_y += title_line_h

    # === 副標題 ===
    if sub_lines:
        sub_y = title_y + gap_title_sub
        for line in sub_lines:
            draw.text((MARGIN_X, sub_y), line, font=sub_font, fill=GRAY_200)
            sub_y += sub_line_h

    # === 底部品牌列 ===
    bar_y = H - BRAND_BAR_H

    # 分隔線：左 1/3 Cyan 漸層 → 右 2/3 Navy
    for x in range(MARGIN_X, W - MARGIN_X):
        progress = (x - MARGIN_X) / (W - 2 * MARGIN_X)
        if progress < 0.25:
            # Cyan → 透明
            fade = 1.0 - (progress / 0.25)
            r = int(DEEP_NAVY[0] + (CYAN[0] - DEEP_NAVY[0]) * fade)
            g = int(DEEP_NAVY[1] + (CYAN[1] - DEEP_NAVY[1]) * fade)
            b = int(DEEP_NAVY[2] + (CYAN[2] - DEEP_NAVY[2]) * fade)
            draw.point((x, bar_y), fill=(r, g, b))
        else:
            draw.point((x, bar_y), fill=NAVY_3)

    # 品牌文字
    brand_cn = make_font(FONT_CN_BOLD, 16)
    brand_en = make_font(FONT_EN, 15, index=5)

    draw.text((MARGIN_X, bar_y + 20), "阿峰老師", font=brand_cn, fill=CYAN)

    pipe_x = MARGIN_X + 76
    draw.text((pipe_x, bar_y + 20), " |  autolab.cloud", font=brand_en, fill=GRAY_400)

    # 右下角 Wing Mark
    wx = W - MARGIN_X - 36
    wy = bar_y + 22
    # 左翼
    draw.polygon([(wx, wy + 14), (wx + 14, wy), (wx + 17, wy + 7)], fill=CYAN)
    # 右翼
    draw.polygon([(wx + 36, wy + 14), (wx + 22, wy), (wx + 19, wy + 7)], fill=CYAN)

    # === 右上角裝飾 L 形 ===
    dx = W - MARGIN_X
    dy = 50
    draw.line([(dx - 36, dy), (dx, dy)], fill=NAVY_4, width=2)
    draw.line([(dx, dy), (dx, dy + 36)], fill=NAVY_4, width=2)

    # === 左下角裝飾點陣（3x3 微點） ===
    dot_x0 = MARGIN_X
    dot_y0 = bar_y - 50
    for row in range(3):
        for col in range(3):
            dx = dot_x0 + col * 8
            dy = dot_y0 + row * 8
            draw.ellipse([dx, dy, dx + 3, dy + 3], fill=NAVY_4)

    # 保存
    output_path = Path(output_dir) / "thumbnail.png"
    img.save(str(output_path), "PNG", quality=95)
    print(f"  [OK] {slug}")
    return output_path


# ============================================================
# 文章資料
# ============================================================
BLOG_DIR = Path(__file__).parent / "blog"

ARTICLES = [
    {
        "slug": "vibe-coding-ai",
        "title": "Vibe Coding 入門指南：工具人時代結束，用 AI 協作解決真問題",
        "subtitle": "矽谷工程師被裁、公司錢拿去買 GPU。含 5 步驟入門實戰、台灣企業案例。",
        "tags": ["AI", "Vibe Coding", "AI趨勢"],
    },
    {
        "slug": "satya-nadella-ai-ceo-ai-ai",
        "title": "Satya Nadella 的 10 億美元 AI 豪賭",
        "subtitle": "3 個不確定性思維 + 阿峰老師獨家「降低門檻 + 提高天花板」實操模板",
        "tags": ["AI趨勢", "微軟CEO", "OpenAI"],
    },
    {
        "slug": "ai-block-2026-ai",
        "title": "AI 裁員潮來了？Block 砍 5000 人背後的真相",
        "subtitle": "三個關鍵觀察 + 獨家 5 步工作拆解法，教你找出不可取代區。",
        "tags": ["AI裁員", "AI安全", "職場AI"],
    },
    {
        "slug": "ai-block-claude",
        "title": "Claude 被封殺、Block 裁員一半：AI 時代職場生存指南",
        "subtitle": "AI 取代人力已不是預言，而是現在式。深度分析數據與各大廠立場。",
        "tags": ["AI", "AI裁員", "Anthropic"],
    },
    {
        "slug": "ai-new-business-rules",
        "title": "AI 時代創業不再靠資金，靠的是這六個步驟",
        "subtitle": "Daniel Priestley 的創業框架 + 台灣企業實戰觀察。真正稀缺的是決策勇氣。",
        "tags": ["AI創業", "創業框架", "企業培訓"],
    },
    {
        "slug": "notebooklm-ai",
        "title": "NotebookLM 逆向工程教學：3 步驟免費拆解百萬爆款影片",
        "subtitle": "用 Google NotebookLM 拆解影片結構，轉化為你的腳本藍圖。含完整提示詞。",
        "tags": ["NotebookLM", "AI工具", "內容創作"],
    },
    {
        "slug": "claude-code-10-real-products",
        "title": "10 個素人用 Claude Code 做出真實產品",
        "subtitle": "設計師、廣告導演、露營旅館老闆。非工程師背景，最快只花 4.5 小時上線。",
        "tags": ["Claude Code", "Vibe Coding", "實戰案例"],
    },
    {
        "slug": "article-2026-03-06",
        "title": "你的「三分鐘熱度」是 AI 時代最值錢的資產",
        "subtitle": "多元潛能、認知交集、Tutorial Hell — 3 步找到認知交集的操作指南。",
        "tags": ["AI", "多元潛能", "認知交集"],
    },
]


def main():
    print("=" * 55)
    print("  Autolab Blog Banner Generator v2")
    print("  Design: Ogilvy-grade Brand Consistency")
    print("=" * 55)

    for article in ARTICLES:
        slug = article["slug"]
        out_dir = BLOG_DIR / slug
        out_dir.mkdir(parents=True, exist_ok=True)
        generate_banner(
            title=article["title"],
            subtitle=article["subtitle"],
            tags=article["tags"],
            slug=slug,
            output_dir=out_dir,
        )

    print(f"\n  共生成 {len(ARTICLES)} 張品牌 Banner")
    print("=" * 55)


if __name__ == "__main__":
    main()
