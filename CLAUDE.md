# Autolab Blog — 部落格系統

> 阿峰老師的 AI 實戰部落格，純靜態 HTML 部署在 GitHub Pages。

## 基本資訊

| 項目 | 值 |
|------|-----|
| 網址 | https://blog.autolab.cloud |
| GitHub Repo | https://github.com/huangchingfeng/autolab-blog |
| 部署方式 | GitHub Pages + GitHub Actions（push main → 自動部署） |
| DNS | GoDaddy CNAME `blog` → `huangchingfeng.github.io` |
| HTTPS | Let's Encrypt，已強制 |

## 技術棧

- **Python 3** — 發布腳本（`publish_blog.py`）
- **Markdown + YAML** — 文章格式（front matter + 內容）
- **Jinja-style Template** — `string.Template` 套用 HTML 模板
- **依賴**：`markdown`, `pyyaml`, `pymdown-extensions`, `Pygments`

## 目錄結構

```
.
├── publish_blog.py        # 一鍵發布腳本
├── articles/              # Markdown 原始檔（含 YAML front matter）
├── templates/
│   ├── article.html       # 文章模板（SEO 完整）
│   └── index.html         # 首頁模板（卡片列表）
├── static/
│   ├── style.css          # 品牌風格 CSS
│   └── og-default.png     # 預設 OG 圖片
├── blog/                  # 輸出目錄（部署到 GitHub Pages）
│   ├── index.html
│   ├── CNAME
│   ├── sitemap.xml
│   ├── robots.txt
│   └── [slug]/index.html  # 各文章
└── .github/workflows/
    └── deploy.yml         # GitHub Actions 自動部署
```

## 常用指令

```bash
# 發布單篇文章
python3 publish_blog.py article.md

# 從 YT Factory 發布（自動提取 SEO meta）
python3 publish_blog.py --from-yt blog-article.md --youtube-id VIDEO_ID --thumbnail thumb.png

# 重建全站（首頁 + sitemap）
python3 publish_blog.py --rebuild

# 不自動 git push（本地預覽）
python3 publish_blog.py article.md --no-push
```

## SEO 功能

- Open Graph + Twitter Card meta tags
- JSON-LD 結構化資料（Article schema）
- Canonical URL
- sitemap.xml + robots.txt
- YouTube 影片自動嵌入

## 與 YT Factory 整合

YT Factory Phase 9 會自動呼叫 `publish_blog.py --from-yt`，將 Phase 8 產出的 blog-article.md 發布到此部落格。
