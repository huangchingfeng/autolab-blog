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
    """產生 YouTube 嵌入 HTML"""
    if not youtube_id:
        return ""
    return f"""<div class="yt-embed"><div class="yt-wrapper">
<iframe src="https://www.youtube.com/embed/{youtube_id}"
  title="YouTube video" loading="lazy"
  allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
  allowfullscreen></iframe>
</div></div>"""


def md_to_html(content):
    """Markdown → HTML，自動將 YouTube 連結轉嵌入"""
    # 轉換 YouTube 連結為嵌入（行內）
    content = re.sub(
        r'(?:https?://)?(?:www\.)?youtube\.com/watch\?v=([a-zA-Z0-9_-]+)',
        r'<div class="yt-embed"><div class="yt-wrapper"><iframe src="https://www.youtube.com/embed/\1" title="YouTube" loading="lazy" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe></div></div>',
        content
    )
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
        thumb = f'{SITE_URL}/{a["slug"]}/thumbnail.png' if a.get("has_thumb") else f"{SITE_URL}/static/og-default.png"
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


def scan_articles():
    """掃描所有已發布文章的 meta"""
    all_meta = []
    for md_file in sorted(ARTICLES_DIR.glob("*.md")):
        text = md_file.read_text()
        meta, _ = parse_front_matter(text)
        if meta.get("slug"):
            meta["has_thumb"] = (BLOG_DIR / meta["slug"] / "thumbnail.png").exists()
            all_meta.append(meta)
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
        "og_image": f"{SITE_URL}/{slug}/thumbnail.png" if thumbnail_path else "",
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

    # robots.txt
    (BLOG_DIR / "robots.txt").write_text(
        f"User-agent: *\nAllow: /\nSitemap: {SITE_URL}/sitemap.xml\n"
    )

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
