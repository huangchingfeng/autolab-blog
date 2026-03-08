#!/usr/bin/env python3
"""Autolab Blog — 一鍵發布腳本
用法：
  python3 publish_blog.py article.md                     # 發布單篇
  python3 publish_blog.py --from-yt blog-article.md      # 從 YT Factory 發布
  python3 publish_blog.py --rebuild                       # 重建全站
  python3 publish_blog.py --newsletter article.md         # 發布 + 寄電子報（未來）
"""
import argparse
import datetime
import html
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
from string import Template

import markdown
import yaml

# ============================================================
# 路徑
# ============================================================
HERE = Path(__file__).parent.resolve()
ARTICLES_DIR = HERE / "articles"
BLOG_DIR = HERE / "blog"
TEMPLATES_DIR = HERE / "templates"
STATIC_DIR = HERE / "static"
SITE_URL = "https://blog.autolab.cloud"

# ============================================================
# Markdown 設定
# ============================================================
MD_EXTENSIONS = [
    "tables", "fenced_code", "codehilite", "toc",
    "pymdownx.tasklist", "pymdownx.magiclink",
]
MD_EXT_CONFIGS = {
    "codehilite": {"css_class": "highlight", "guess_lang": False},
}


def parse_front_matter(text):
    """解析 YAML front matter，回傳 (meta_dict, content_str)"""
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            meta = yaml.safe_load(parts[1]) or {}
            content = parts[2].strip()
            return meta, content
    return {}, text


def extract_seo_from_article(text):
    """從 blog-article.md 底部的 SEO 區塊提取 meta"""
    meta = {}
    # Meta Title
    m = re.search(r"Meta Title[：:]\s*(.+)", text)
    if m:
        meta["title"] = m.group(1).strip()
    # Meta Description
    m = re.search(r"Meta Description[：:]\s*(.+)", text)
    if m:
        meta["description"] = m.group(1).strip()
    # Tags
    m = re.search(r"Tags[：:]\s*(.+)", text)
    if m:
        tags_str = m.group(1).strip()
        meta["tags"] = [t.strip().lstrip("#") for t in re.split(r"[,、\s]+#?", tags_str) if t.strip().lstrip("#")]
    # Target Keywords
    m = re.search(r"Target Keywords[：:]\s*(.+)", text)
    if m:
        meta["keywords"] = [k.strip() for k in m.group(1).split(",")]
    return meta


def normalize_youtube_id(raw_id):
    """從 YouTube URL 或 ID 中提取 11 字元 ID"""
    if not raw_id:
        return ""
    m = re.search(r'(?:v=|youtu\.be/|embed/)([a-zA-Z0-9_-]{11})', raw_id)
    if m:
        return m.group(1)
    # 已經是純 ID
    if re.match(r'^[a-zA-Z0-9_-]{11}$', raw_id.strip()):
        return raw_id.strip()
    return raw_id.strip()


def youtube_embed(youtube_id, title=""):
    """產生 YouTube banner（縮圖 + 播放按鈕，點擊跳 YouTube）"""
    if not youtube_id:
        return ""
    vid = normalize_youtube_id(youtube_id)
    alt_text = html.escape(f"觀看影片：{title}") if title else "觀看 YouTube 影片"
    aria = html.escape(f"在 YouTube 觀看：{title}") if title else "在 YouTube 觀看影片"
    return f"""<a href="https://www.youtube.com/watch?v={vid}" target="_blank" rel="noopener" class="yt-banner" aria-label="{aria}">
  <img src="https://img.youtube.com/vi/{vid}/maxresdefault.jpg"
       onerror="this.src='https://img.youtube.com/vi/{vid}/hqdefault.jpg'"
       alt="{alt_text}" loading="lazy" width="1280" height="720">
  <div class="yt-play" role="img" aria-hidden="true">&#9654;</div>
</a>"""


def md_to_html(content):
    """Markdown → HTML"""
    return markdown.markdown(content, extensions=MD_EXTENSIONS,
                             extension_configs=MD_EXT_CONFIGS)


def _iso_date(date_str):
    """將日期轉為 ISO 8601 含時區格式"""
    d = str(date_str) if date_str else ""
    if re.match(r'^\d{4}-\d{2}-\d{2}$', d):
        return f"{d}T00:00:00+08:00"
    return d


def build_json_ld(meta):
    """產生 Article JSON-LD 結構化資料（含 VideoObject）"""
    date_iso = _iso_date(meta.get("date", ""))
    updated_iso = _iso_date(meta.get("updated", meta.get("date", "")))

    ld = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": meta.get("title", ""),
        "description": meta.get("description", ""),
        "author": {
            "@type": "Person",
            "name": meta.get("author", "黃敬峰（AI峰哥）"),
            "url": "https://www.autolab.cloud"
        },
        "publisher": {
            "@type": "Organization",
            "name": "Autolab",
            "url": "https://www.autolab.cloud",
            "logo": {
                "@type": "ImageObject",
                "url": f"{SITE_URL}/static/og-default.png"
            }
        },
        "datePublished": date_iso,
        "dateModified": updated_iso,
        "image": meta.get("og_image", f"{SITE_URL}/static/og-default.png"),
        "mainEntityOfPage": f"{SITE_URL}/{meta.get('slug', '')}/",
        "keywords": ", ".join(meta.get("keywords", meta.get("tags", []))),
        "inLanguage": "zh-Hant-TW"
    }

    # VideoObject（YouTube 影片 Rich Result）
    yt_id = meta.get("youtube_id", "")
    if yt_id:
        vid = normalize_youtube_id(yt_id)
        ld["video"] = {
            "@type": "VideoObject",
            "name": meta.get("title", ""),
            "description": meta.get("description", ""),
            "thumbnailUrl": f"https://img.youtube.com/vi/{vid}/maxresdefault.jpg",
            "uploadDate": date_iso,
            "embedUrl": f"https://www.youtube.com/embed/{vid}",
            "url": f"https://www.youtube.com/watch?v={vid}"
        }

    return json.dumps(ld, ensure_ascii=False)


def build_breadcrumb(meta):
    """產生麵包屑 HTML 和 JSON-LD"""
    title = html.escape(meta.get("title", ""))
    slug = meta.get("slug", "")

    breadcrumb_html = (
        f'<a href="{SITE_URL}/">Blog</a>'
        f'<span class="sep">›</span>'
        f'<span class="current">{title}</span>'
    )

    breadcrumb_ld = json.dumps({
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": 1,
                "name": "Blog",
                "item": f"{SITE_URL}/"
            },
            {
                "@type": "ListItem",
                "position": 2,
                "name": meta.get("title", ""),
                "item": f"{SITE_URL}/{slug}/"
            }
        ]
    }, ensure_ascii=False)

    return breadcrumb_html, breadcrumb_ld


def build_article_tags_meta(tags):
    """產生 article:tag Open Graph meta tags"""
    return "\n  ".join(
        f'<meta property="article:tag" content="{html.escape(str(t))}">'
        for t in tags
    )


def build_related_articles(current_meta, all_articles):
    """找出最相關的 3 篇文章（基於標籤匹配 + 日期）"""
    current_slug = current_meta.get("slug", "")
    current_tags = set(current_meta.get("tags", []))

    if not all_articles:
        return ""

    # 計算相關度（共同標籤數）
    scored = []
    for a in all_articles:
        if a.get("slug") == current_slug:
            continue
        common = len(current_tags & set(a.get("tags", [])))
        scored.append((common, str(a.get("date", "")), a))

    # 排序：先按共同標籤數降序，再按日期降序
    scored.sort(key=lambda x: (x[0], x[1]), reverse=True)
    related = [item[2] for item in scored[:3]]

    if not related:
        return ""

    cards_html = []
    for a in related:
        slug = a.get("slug", "")
        if a.get("has_banner"):
            thumb = f'../{slug}/banner.png'
        elif a.get("has_thumb"):
            thumb = f'../{slug}/thumbnail.png'
        else:
            thumb = "../static/og-default.png"

        title = html.escape(str(a.get("title", "")))
        cards_html.append(f'''<a href="{SITE_URL}/{slug}/" class="related-card">
  <img class="related-card-thumb" src="{thumb}" alt="{title}" loading="lazy">
  <div class="related-card-body">
    <div class="related-card-date">{a.get("date", "")}</div>
    <div class="related-card-title">{title}</div>
  </div>
</a>''')

    return f'''<section class="related-section">
  <h2>你可能也想看</h2>
  <div class="related-grid">
    {"".join(cards_html)}
  </div>
</section>'''


def build_article_nav(current_meta, all_articles):
    """產生上一篇/下一篇導航"""
    current_slug = current_meta.get("slug", "")
    sorted_articles = sorted(all_articles, key=lambda a: str(a.get("date", "")), reverse=True)

    idx = None
    for i, a in enumerate(sorted_articles):
        if a.get("slug") == current_slug:
            idx = i
            break

    if idx is None:
        return ""

    parts = []
    # 上一篇（較新的 = idx - 1）
    if idx > 0:
        prev = sorted_articles[idx - 1]
        prev_title = html.escape(str(prev.get("title", "")))
        parts.append(f'''<a href="{SITE_URL}/{prev["slug"]}/" class="prev">
  <div class="nav-label">← 上一篇</div>
  <div class="nav-title">{prev_title}</div>
</a>''')
    else:
        parts.append('<div></div>')

    # 下一篇（較舊的 = idx + 1）
    if idx < len(sorted_articles) - 1:
        next_a = sorted_articles[idx + 1]
        next_title = html.escape(str(next_a.get("title", "")))
        parts.append(f'''<a href="{SITE_URL}/{next_a["slug"]}/" class="next">
  <div class="nav-label">下一篇 →</div>
  <div class="nav-title">{next_title}</div>
</a>''')
    else:
        parts.append('<div></div>')

    return f'''<nav class="article-nav">
  {"".join(parts)}
</nav>'''


def render_article(meta, html_content, all_articles=None):
    """套用文章頁模板"""
    tpl = (TEMPLATES_DIR / "article.html").read_text()
    slug = meta.get("slug", "untitled")
    title = meta.get("title", "Untitled")
    title_escaped = html.escape(title)

    # og_image fallback：banner → thumbnail → og-default
    og_image = f"{SITE_URL}/static/og-default.png"
    banner_path = BLOG_DIR / slug / "banner.png"
    thumb_path = BLOG_DIR / slug / "thumbnail.png"
    if banner_path.exists():
        og_image = f"{SITE_URL}/{slug}/banner.png"
    elif thumb_path.exists():
        og_image = f"{SITE_URL}/{slug}/thumbnail.png"
    elif meta.get("og_image"):
        og_image = meta["og_image"]

    tags_html = "".join(f'<span class="tag">{html.escape(str(t))}</span>' for t in meta.get("tags", []))
    yt_html = youtube_embed(meta.get("youtube_id"), title)
    json_ld = build_json_ld({**meta, "og_image": og_image})
    canonical = meta.get("canonical_url") or f"{SITE_URL}/{slug}/"
    date_iso = _iso_date(meta.get("date", ""))

    # Featured image（優先 banner.png，fallback thumbnail.png）
    featured_html = ""
    if banner_path.exists():
        featured_html = f'<div class="featured-image-wrapper"><img src="banner.png" alt="{title_escaped}" class="featured-image" loading="lazy" width="780" height="438"></div>'
    elif thumb_path.exists():
        featured_html = f'<div class="featured-image-wrapper"><img src="thumbnail.png" alt="{title_escaped}" class="featured-image" loading="lazy" width="780" height="438"></div>'

    # 麵包屑
    breadcrumb_html, breadcrumb_ld = build_breadcrumb(meta)

    # article:tag meta
    article_tags_meta = build_article_tags_meta(meta.get("tags", []))

    # 相關文章 & 導航（需要 all_articles）
    related_html = ""
    nav_html = ""
    if all_articles:
        related_html = build_related_articles(meta, all_articles)
        nav_html = build_article_nav(meta, all_articles)

    # 逃逸 content 中的 $ 符號，避免 Template 誤解析
    safe_content = html_content.replace("$", "$$")

    return Template(tpl).safe_substitute(
        title=title_escaped,
        description=html.escape(meta.get("description", "")),
        keywords=", ".join(meta.get("keywords", meta.get("tags", []))),
        canonical=canonical,
        og_image=og_image,
        og_image_width="1200",
        og_image_height="630",
        slug=slug,
        date=str(meta.get("date", "")),
        date_iso=date_iso,
        author=meta.get("author", "黃敬峰（AI峰哥）"),
        tags=tags_html,
        youtube=yt_html,
        featured_image=featured_html,
        content=safe_content,
        json_ld=json_ld,
        site_url=SITE_URL,
        breadcrumb_html=breadcrumb_html,
        breadcrumb_ld=breadcrumb_ld,
        article_tags_meta=article_tags_meta,
        related_articles=related_html.replace("$", "$$"),
        article_nav=nav_html.replace("$", "$$"),
    )


def render_index(all_articles):
    """產生首頁 HTML"""
    tpl = (TEMPLATES_DIR / "index.html").read_text()
    # 按日期倒序
    sorted_articles = sorted(all_articles, key=lambda a: a.get("date", ""), reverse=True)

    cards = []
    for a in sorted_articles:
        # 優先用 banner.png（Pexels 背景版），fallback thumbnail.png
        if a.get("has_banner"):
            thumb = f'{a["slug"]}/banner.png'
        elif a.get("has_thumb"):
            thumb = f'{a["slug"]}/thumbnail.png'
        else:
            thumb = "static/og-default.png"
        tags_html = "".join(f'<span class="tag">{t}</span>' for t in a.get("tags", [])[:3])
        cards.append(f"""<a href="{a['slug']}/" class="card">
  <img class="card-thumb" src="{thumb}" alt="{a.get('title', '')}" loading="lazy">
  <div class="card-body">
    <div class="card-date">{a.get('date', '')}</div>
    <div class="card-title">{a.get('title', '')}</div>
    <div class="card-desc">{a.get('description', '')}</div>
    <div class="card-tags">{tags_html}</div>
  </div>
</a>""")

    return Template(tpl).safe_substitute(
        cards="\n".join(cards),
        site_url=SITE_URL,
        count=len(sorted_articles),
        article_count=len(sorted_articles),
    )


def generate_sitemap(all_articles):
    """產生 sitemap.xml"""
    today = datetime.date.today().isoformat()
    urls = [f"""  <url>
    <loc>{SITE_URL}/</loc>
    <lastmod>{today}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>1.0</priority>
  </url>"""]

    for a in all_articles:
        urls.append(f"""  <url>
    <loc>{SITE_URL}/{a['slug']}/</loc>
    <lastmod>{a.get('date', today)}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>""")

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{chr(10).join(urls)}
</urlset>"""


def generate_rss(all_articles):
    """產生 RSS 2.0 feed"""
    today = datetime.date.today().strftime("%a, %d %b %Y 00:00:00 +0800")
    sorted_articles = sorted(all_articles, key=lambda a: str(a.get("date", "")), reverse=True)

    items = []
    for a in sorted_articles[:20]:
        pub_date = str(a.get("date", ""))
        try:
            dt = datetime.datetime.strptime(pub_date, "%Y-%m-%d")
            rfc_date = dt.strftime("%a, %d %b %Y 00:00:00 +0800")
        except (ValueError, TypeError):
            rfc_date = today

        desc = html.escape(str(a.get("description", "")))
        title = html.escape(str(a.get("title", "")))
        # 分類標籤
        categories = "".join(f"\n      <category>{html.escape(str(t))}</category>" for t in a.get("tags", []))

        items.append(f"""    <item>
      <title>{title}</title>
      <link>{SITE_URL}/{a['slug']}/</link>
      <guid>{SITE_URL}/{a['slug']}/</guid>
      <pubDate>{rfc_date}</pubDate>
      <author>ai@autolab.cloud (黃敬峰)</author>
      <description>{desc}</description>{categories}
    </item>""")

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>阿峰老師 AI 實戰部落格</title>
    <link>{SITE_URL}/</link>
    <description>企業 AI 培訓、Vibe Coding、AI 工具教學，從觀念到落地。</description>
    <language>zh-TW</language>
    <lastBuildDate>{today}</lastBuildDate>
    <atom:link href="{SITE_URL}/feed.xml" rel="self" type="application/rss+xml"/>
    <image>
      <url>{SITE_URL}/static/og-default.png</url>
      <title>阿峰老師 AI 實戰部落格</title>
      <link>{SITE_URL}/</link>
    </image>
{chr(10).join(items)}
  </channel>
</rss>"""


def scan_articles():
    """掃描所有已發布文章的 meta（自動去重複 slug，按日期排序保留最新）"""
    all_meta = []
    seen_slugs = set()
    # 先蒐集所有文章，再按日期倒序（同 slug 保留最新的）
    candidates = []
    for md_file in ARTICLES_DIR.glob("*.md"):
        text = md_file.read_text()
        meta, _ = parse_front_matter(text)
        slug = meta.get("slug")
        if slug:
            meta["_src"] = md_file.name
            candidates.append(meta)
    # 按日期倒序排列
    candidates.sort(key=lambda a: str(a.get("date", "")), reverse=True)
    for meta in candidates:
        slug = meta["slug"]
        if slug not in seen_slugs:
            seen_slugs.add(slug)
            meta["has_banner"] = (BLOG_DIR / slug / "banner.png").exists()
            meta["has_thumb"] = (BLOG_DIR / slug / "thumbnail.png").exists()
            all_meta.append(meta)
        else:
            print(f"  [!] 跳過重複 slug: {slug} ({meta.get('_src', '')})")
    return all_meta


def publish_article(md_path, thumbnail_path=None):
    """發布單篇文章"""
    md_path = Path(md_path).resolve()
    text = md_path.read_text()
    meta, content = parse_front_matter(text)

    if not meta.get("slug"):
        print("  [!] 缺少 slug，無法發布")
        return None

    slug = meta["slug"]
    print(f"  文章: {meta.get('title', slug)}")
    print(f"  Slug: {slug}")

    # 建立輸出目錄（先建立，才能複製 thumbnail）
    out_dir = BLOG_DIR / slug
    out_dir.mkdir(parents=True, exist_ok=True)

    # 複製 thumbnail（必須在 render_article 之前，否則 featured image 偵測失敗）
    if thumbnail_path and Path(thumbnail_path).exists():
        src = Path(thumbnail_path).resolve()
        dst = (out_dir / "thumbnail.png").resolve()
        if src != dst:
            shutil.copy2(thumbnail_path, out_dir / "thumbnail.png")
        print(f"  縮圖: blog/{slug}/thumbnail.png")

    # 轉換 HTML（此時 thumbnail 已就位，featured image 偵測正確）
    html_content = md_to_html(content)
    # 掃描所有文章用於 related/nav
    all_articles = scan_articles()
    full_html = render_article(meta, html_content, all_articles)
    (out_dir / "index.html").write_text(full_html)
    print(f"  HTML: blog/{slug}/index.html")

    # 複製到 articles/ 備份
    dest = ARTICLES_DIR / f"{slug}.md"
    if md_path.resolve() != dest.resolve():
        shutil.copy2(md_path, dest)

    return meta


def publish_from_yt(md_path, youtube_id=None, thumbnail_path=None):
    """從 YT Factory 的 blog-article.md 發布"""
    md_path = Path(md_path).resolve()
    text = md_path.read_text()

    # 提取 SEO meta
    seo = extract_seo_from_article(text)
    title = seo.get("title", "Untitled")

    # 清理文章內容（移除底部 SEO 區塊）
    content = re.split(r'\n\s*SEO:\s*\n', text)[0].strip()

    # 產生 slug — 只取純英文/數字 keywords
    slug_source = ""
    if seo.get("keywords"):
        # 過濾出有英文字母的 keywords
        en_keywords = [k for k in seo["keywords"] if re.search(r'[a-zA-Z]', k)]
        if en_keywords:
            slug_source = " ".join(en_keywords[:3])
    if not slug_source:
        # 從標題中提取英文部分
        en_parts = re.findall(r'[a-zA-Z][a-zA-Z0-9]*', title)
        if en_parts:
            slug_source = " ".join(en_parts[:5])
    slug = re.sub(r'[^a-z0-9]+', '-', slug_source.lower()) if slug_source else ""
    slug = re.sub(r'-+', '-', slug).strip('-')
    # 去除重複的連續相同詞（如 ai-ai-ai → ai）
    parts = slug.split('-')
    deduped = [parts[0]] if parts else []
    for p in parts[1:]:
        if p != deduped[-1]:
            deduped.append(p)
    slug = '-'.join(deduped)
    # 截斷到合理長度
    if len(slug) > 60:
        slug = slug[:60].rsplit('-', 1)[0]
    # fallback
    if len(slug) < 5 or not any(c.isalpha() for c in slug):
        slug = f"article-{datetime.date.today().isoformat()}"

    today = datetime.date.today().isoformat()

    # 建立 front matter
    front_matter = {
        "title": seo.get("title", title),
        "description": seo.get("description", ""),
        "date": today,
        "tags": seo.get("tags", []),
        "keywords": seo.get("keywords", []),
        "slug": slug,
        "youtube_id": normalize_youtube_id(youtube_id) if youtube_id else "",
        "author": "黃敬峰（AI峰哥）",
    }

    # 組合完整 markdown
    fm_yaml = yaml.dump(front_matter, allow_unicode=True, default_flow_style=False)
    full_md = f"---\n{fm_yaml}---\n\n{content}"

    # 存到 articles/
    dest = ARTICLES_DIR / f"{slug}.md"
    dest.write_text(full_md)
    print(f"  Front matter 已生成")

    return publish_article(dest, thumbnail_path)


def rebuild_site():
    """重建首頁 + sitemap"""
    all_articles = scan_articles()

    # 複製 static 到 blog/
    blog_static = BLOG_DIR / "static"
    if blog_static.exists():
        shutil.rmtree(blog_static)
    shutil.copytree(STATIC_DIR, blog_static)

    # 重建所有文章頁（加入相關文章和導航）
    print(f"  重建文章頁（相關文章 + 導航）...")
    for meta in all_articles:
        slug = meta.get("slug", "")
        md_file = ARTICLES_DIR / f"{slug}.md"
        if md_file.exists():
            text = md_file.read_text()
            _, content = parse_front_matter(text)
            html_content = md_to_html(content)
            full_html = render_article(meta, html_content, all_articles)
            out_dir = BLOG_DIR / slug
            out_dir.mkdir(parents=True, exist_ok=True)
            (out_dir / "index.html").write_text(full_html)
    print(f"  已重建 {len(all_articles)} 篇文章頁")

    # 生成首頁
    index_html = render_index(all_articles)
    (BLOG_DIR / "index.html").write_text(index_html)
    print(f"  首頁: blog/index.html（{len(all_articles)} 篇文章）")

    # 生成 sitemap
    sitemap = generate_sitemap(all_articles)
    (BLOG_DIR / "sitemap.xml").write_text(sitemap)
    print(f"  Sitemap: blog/sitemap.xml")

    # RSS feed
    rss = generate_rss(all_articles)
    (BLOG_DIR / "feed.xml").write_text(rss)
    print(f"  RSS: blog/feed.xml")

    # robots.txt
    (BLOG_DIR / "robots.txt").write_text(
        f"User-agent: *\nAllow: /\nSitemap: {SITE_URL}/sitemap.xml\n"
    )

    # CNAME（GitHub Pages 自訂網域，必須保護）
    cname_path = BLOG_DIR / "CNAME"
    if not cname_path.exists():
        cname_path.write_text("blog.autolab.cloud")
        print("  CNAME: blog.autolab.cloud（自動重建）")

    return all_articles


def git_deploy(message="publish blog article"):
    """Git add + commit + push"""
    def _git(*cmd):
        try:
            return subprocess.run(
                ["git", *cmd], cwd=HERE, check=True,
                capture_output=True, text=True
            )
        except subprocess.CalledProcessError as e:
            print(f"  [!] git {' '.join(cmd)} 失敗:")
            if e.stderr:
                print(f"      {e.stderr.strip()}")
            raise
    _git("add", ".")
    result = subprocess.run(
        ["git", "diff", "--cached", "--quiet"], cwd=HERE, capture_output=True
    )
    if result.returncode == 0:
        print("  [i] 沒有變更，跳過 git push")
        return
    _git("commit", "-m", message)
    _git("push")
    print("  Git: commit + push 完成")


def main():
    parser = argparse.ArgumentParser(description="Autolab Blog 發布腳本")
    parser.add_argument("article", nargs="?", help="Markdown 文章路徑")
    parser.add_argument("--from-yt", metavar="MD", help="從 YT Factory blog-article.md 發布")
    parser.add_argument("--youtube-id", help="YouTube 影片 ID")
    parser.add_argument("--thumbnail", help="縮圖路徑")
    parser.add_argument("--rebuild", action="store_true", help="重建全站")
    parser.add_argument("--no-push", action="store_true", help="不自動 git push")
    parser.add_argument("--newsletter", action="store_true", help="同時寄送電子報（未來功能）")
    args = parser.parse_args()

    print("=" * 55)
    print("  Autolab Blog 發布系統")
    print("=" * 55)

    meta = None

    if args.from_yt:
        print(f"\n[1/3] 從 YT Factory 發布...")
        meta = publish_from_yt(args.from_yt, args.youtube_id, args.thumbnail)
    elif args.article:
        print(f"\n[1/3] 發布文章...")
        meta = publish_article(args.article, args.thumbnail)
    elif not args.rebuild:
        parser.print_help()
        return

    print(f"\n[2/3] 重建全站...")
    all_articles = rebuild_site()

    if not args.no_push:
        print(f"\n[3/3] 部署...")
        title = meta.get("title", "update") if meta else "rebuild site"
        git_deploy(f"blog: {title}")

    slug = meta.get("slug", "") if meta else ""
    url = f"{SITE_URL}/{slug}/" if slug else SITE_URL

    print(f"\n{'=' * 55}")
    print(f"  發布完成！")
    print(f"  文章數: {len(all_articles)}")
    if slug:
        print(f"  網址: {url}")
    print(f"  首頁: {SITE_URL}/")
    print(f"  Sitemap: {SITE_URL}/sitemap.xml")
    print(f"{'=' * 55}")

    if args.newsletter:
        print("\n  [i] 電子報功能開發中，敬請期待！")
        # TODO: 未來串接電子報 API（Resend / SendGrid / Mailchimp）
        # 流程：讀取文章 → 套用電子報模板 → 呼叫 API 發送

    return url


if __name__ == "__main__":
    main()
