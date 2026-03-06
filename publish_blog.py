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


def youtube_embed(youtube_id):
    """產生 YouTube banner（縮圖 + 播放按鈕，點擊跳 YouTube）"""
    if not youtube_id:
        return ""
    return f"""<a href="https://www.youtube.com/watch?v={youtube_id}" target="_blank" rel="noopener" class="yt-banner">
  <img src="https://img.youtube.com/vi/{youtube_id}/maxresdefault.jpg" alt="觀看 YouTube 影片" loading="lazy">
  <div class="yt-play">&#9654;</div>
</a>"""


def md_to_html(content):
    """Markdown → HTML"""
    return markdown.markdown(content, extensions=MD_EXTENSIONS,
                             extension_configs=MD_EXT_CONFIGS)


def build_json_ld(meta):
    """產生 Article JSON-LD 結構化資料"""
    return json.dumps({
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
        "datePublished": meta.get("date", ""),
        "dateModified": meta.get("date", ""),
        "image": meta.get("og_image", f"{SITE_URL}/static/og-default.png"),
        "mainEntityOfPage": f"{SITE_URL}/{meta.get('slug', '')}/",
        "keywords": ", ".join(meta.get("keywords", meta.get("tags", []))),
        "inLanguage": "zh-Hant-TW"
    }, ensure_ascii=False)


def render_article(meta, html_content):
    """套用文章頁模板"""
    tpl = (TEMPLATES_DIR / "article.html").read_text()
    slug = meta.get("slug", "untitled")
    og_image = meta.get("og_image", f"{SITE_URL}/static/og-default.png")
    tags_html = "".join(f'<span class="tag">{t}</span>' for t in meta.get("tags", []))
    yt_html = youtube_embed(meta.get("youtube_id"))
    json_ld = build_json_ld(meta)
    canonical = meta.get("canonical_url") or f"{SITE_URL}/{slug}/"

    # Featured image（優先 banner.png，fallback thumbnail.png）
    featured_html = ""
    banner_path = BLOG_DIR / slug / "banner.png"
    thumb_path = BLOG_DIR / slug / "thumbnail.png"
    if banner_path.exists():
        featured_html = f'<div class="featured-image-wrapper"><img src="banner.png" alt="{meta.get("title", "")}" class="featured-image" loading="lazy"></div>'
    elif thumb_path.exists():
        featured_html = f'<div class="featured-image-wrapper"><img src="thumbnail.png" alt="{meta.get("title", "")}" class="featured-image" loading="lazy"></div>'

    return Template(tpl).safe_substitute(
        title=meta.get("title", "Untitled"),
        description=meta.get("description", ""),
        keywords=", ".join(meta.get("keywords", meta.get("tags", []))),
        canonical=canonical,
        og_image=og_image,
        slug=slug,
        date=meta.get("date", ""),
        author=meta.get("author", "黃敬峰（AI峰哥）"),
        tags=tags_html,
        youtube=yt_html,
        featured_image=featured_html,
        content=html_content,
        json_ld=json_ld,
        site_url=SITE_URL,
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
            thumb = f'{SITE_URL}/{a["slug"]}/banner.png'
        elif a.get("has_thumb"):
            thumb = f'{SITE_URL}/{a["slug"]}/thumbnail.png'
        else:
            thumb = f"{SITE_URL}/static/og-default.png"
        tags_html = "".join(f'<span class="tag">{t}</span>' for t in a.get("tags", [])[:3])
        cards.append(f"""<a href="{SITE_URL}/{a['slug']}/" class="card">
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
    sorted_articles = sorted(all_articles, key=lambda a: a.get("date", ""), reverse=True)

    items = []
    for a in sorted_articles[:20]:  # 最新 20 篇
        pub_date = a.get("date", "")
        # 簡易日期轉換
        try:
            dt = datetime.datetime.strptime(pub_date, "%Y-%m-%d")
            rfc_date = dt.strftime("%a, %d %b %Y 00:00:00 +0800")
        except (ValueError, TypeError):
            rfc_date = today

        desc = a.get("description", "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        title = a.get("title", "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

        items.append(f"""    <item>
      <title>{title}</title>
      <link>{SITE_URL}/{a['slug']}/</link>
      <guid>{SITE_URL}/{a['slug']}/</guid>
      <pubDate>{rfc_date}</pubDate>
      <description>{desc}</description>
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
{chr(10).join(items)}
  </channel>
</rss>"""


def scan_articles():
    """掃描所有已發布文章的 meta（自動去重複 slug）"""
    all_meta = []
    seen_slugs = set()
    for md_file in sorted(ARTICLES_DIR.glob("*.md")):
        text = md_file.read_text()
        meta, _ = parse_front_matter(text)
        slug = meta.get("slug")
        if slug and slug not in seen_slugs:
            seen_slugs.add(slug)
            meta["has_banner"] = (BLOG_DIR / slug / "banner.png").exists()
            meta["has_thumb"] = (BLOG_DIR / slug / "thumbnail.png").exists()
            all_meta.append(meta)
        elif slug in seen_slugs:
            print(f"  [!] 跳過重複 slug: {slug} ({md_file.name})")
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

    # 轉換 HTML
    html_content = md_to_html(content)
    full_html = render_article(meta, html_content)

    # 建立輸出目錄
    out_dir = BLOG_DIR / slug
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "index.html").write_text(full_html)
    print(f"  HTML: blog/{slug}/index.html")

    # 複製 thumbnail
    if thumbnail_path and Path(thumbnail_path).exists():
        src = Path(thumbnail_path).resolve()
        dst = (out_dir / "thumbnail.png").resolve()
        if src != dst:
            shutil.copy2(thumbnail_path, out_dir / "thumbnail.png")
        print(f"  縮圖: blog/{slug}/thumbnail.png")

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

    # 產生 slug — 優先用 keywords，再用標題英文部分
    slug_source = ""
    if seo.get("keywords"):
        # 取前 3 個 keyword 組成 slug
        slug_source = " ".join(seo["keywords"][:3])
    if not slug_source:
        slug_source = title
    slug = re.sub(r'[^a-z0-9]+', '-', slug_source.lower())
    slug = re.sub(r'-+', '-', slug).strip('-')
    # 截斷到合理長度
    if len(slug) > 60:
        slug = slug[:60].rsplit('-', 1)[0]
    # fallback：如果 slug 太短或無英文
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
        "youtube_id": youtube_id or "",
        "author": "黃敬峰（AI峰哥）",
        "og_image": f"{SITE_URL}/{slug}/banner.png",
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
    os.chdir(HERE)
    subprocess.run(["git", "add", "."], check=True, capture_output=True)
    result = subprocess.run(
        ["git", "diff", "--cached", "--quiet"], capture_output=True
    )
    if result.returncode == 0:
        print("  [i] 沒有變更，跳過 git push")
        return
    subprocess.run(["git", "commit", "-m", message], check=True, capture_output=True)
    subprocess.run(["git", "push"], check=True, capture_output=True)
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
