#!/usr/bin/env python3
"""
為部落格文章的 h2 章節自動加入 Pexels 圖片。

用法：
  python3 add_article_images.py                  # 處理所有文章
  python3 add_article_images.py --slug ai-2026-ai # 處理單篇文章
  python3 add_article_images.py --dry-run         # 預覽模式（不下載）
"""

import os
import re
import sys
import time
import argparse
import requests
import unicodedata
from pathlib import Path

# ── 設定 ──────────────────────────────────────────────
PEXELS_API_KEY = "DLzQWvyf1dQxEkF27Z5TCptcZZH2x4uX1JaLusuoOGZWmT6q0TzRxmUl"
PEXELS_SEARCH_URL = "https://api.pexels.com/v1/search"
MAX_IMAGES_PER_ARTICLE = 3

BASE_DIR = Path(__file__).resolve().parent
ARTICLES_DIR = BASE_DIR / "articles"
BLOG_DIR = BASE_DIR / "blog"

# 要跳過的章節關鍵字（前言、結語等）
SKIP_SECTIONS = [
    "結語", "前言", "總結", "行動清單", "延伸閱讀",
    "FAQ", "常見問題", "資源連結", "影片重點回顧",
    "重點回顧", "小結", "結論", "參考資料", "附錄",
]

# 中文 → 英文關鍵字對照表
KEYWORD_MAP = {
    "AI": "artificial intelligence",
    "人工智慧": "artificial intelligence",
    "企業": "business",
    "培訓": "training",
    "職場": "workplace",
    "創業": "startup",
    "白領": "office worker",
    "程式": "programming",
    "工具": "tools",
    "簡報": "presentation",
    "影片": "video",
    "未來": "future",
    "數據": "data",
    "自動化": "automation",
    "機器人": "robot",
    "學習": "learning",
    "教學": "education",
    "寫作": "writing",
    "設計": "design",
    "音樂": "music",
    "語音": "voice",
    "瀏覽器": "browser",
    "搜尋": "search",
    "知識": "knowledge",
    "效率": "productivity",
    "投資": "investment",
    "股票": "stock market",
    "經濟": "economy",
    "失業": "unemployment",
    "危機": "crisis",
    "趨勢": "trend",
    "技術": "technology",
    "筆記": "notes",
    "會議": "meeting",
    "客戶": "client",
    "行銷": "marketing",
    "品牌": "brand",
    "電商": "ecommerce",
    "手機": "smartphone",
    "電腦": "computer",
    "鍵盤": "keyboard",
    "開發": "software development",
    "程式碼": "code",
    "團隊": "team",
    "管理": "management",
    "策略": "strategy",
    "商業": "business",
    "模式": "model",
    "平台": "platform",
    "生態": "ecosystem",
    "競爭": "competition",
    "優勢": "advantage",
    "轉型": "transformation",
    "創新": "innovation",
    "實戰": "practice",
    "案例": "case study",
    "分析": "analysis",
    "報告": "report",
    "規劃": "planning",
    "方法": "method",
}


def sanitize_filename(title: str) -> str:
    """將章節標題轉為安全的英文檔案名稱。"""
    # 移除 【獨家】 等標記
    title = re.sub(r"[【】「」『』《》〈〉（）\(\)\[\]#*]", "", title).strip()

    words = []

    # 按空白和標點拆分
    tokens = re.split(r"[\s：:,，、/\-—]+", title)
    for token in tokens:
        if not token:
            continue
        # 純英文/數字直接使用
        if re.match(r"^[a-zA-Z0-9]+$", token):
            words.append(token.lower())
            continue

        # 嘗試整個 token 在對照表中
        if token in KEYWORD_MAP:
            words.append(KEYWORD_MAP[token].replace(" ", "-"))
            continue

        # 混合 token（如 "400多家企業"）：先抽英文/數字，再逐子串匹配中文
        ascii_part = re.findall(r"[a-zA-Z0-9]+", token)
        for part in ascii_part:
            words.append(part.lower())

        # 抽取中文部分，用滑動窗口匹配對照表（優先長詞）
        chinese_only = re.sub(r"[a-zA-Z0-9]", "", token)
        i = 0
        while i < len(chinese_only):
            matched = False
            # 從最長的 key 開始嘗試
            for length in range(min(4, len(chinese_only) - i), 0, -1):
                substr = chinese_only[i:i + length]
                if substr in KEYWORD_MAP:
                    words.append(KEYWORD_MAP[substr].replace(" ", "-"))
                    i += length
                    matched = True
                    break
            if not matched:
                i += 1

    # 去重但保留順序
    seen = set()
    unique_words = []
    for w in words:
        if w not in seen:
            seen.add(w)
            unique_words.append(w)

    name = "-".join(unique_words[:5]) if unique_words else "section"
    # 清理多餘連字號
    name = re.sub(r"-+", "-", name).strip("-")
    return name[:60]  # 限制長度


def generate_search_query(title: str, first_paragraph: str) -> str:
    """根據章節標題和首段內容產生英文搜尋關鍵字（2-3 個字）。"""
    # 合併標題和首段
    text = title + " " + (first_paragraph or "")

    # 移除標記符號
    text = re.sub(r"[【】「」『』《》〈〉（）\(\)\[\]#*\-]", " ", text)

    # 收集英文關鍵字
    english_words = []

    # 1. 先找對照表中的中文關鍵字
    for zh, en in KEYWORD_MAP.items():
        if zh in text:
            for w in en.split():
                if w not in english_words:
                    english_words.append(w)

    # 2. 找文中已有的英文詞
    for word in re.findall(r"[A-Za-z]{3,}", text):
        w = word.lower()
        if w not in english_words and w not in ("the", "and", "for", "with", "this", "that", "from", "are", "was", "not", "but", "has", "had", "will"):
            english_words.append(w)

    # 取前 2-3 個關鍵字
    if not english_words:
        english_words = ["technology"]

    query = " ".join(english_words[:3])
    return query


def search_pexels(query: str) -> dict | None:
    """搜尋 Pexels 照片，回傳照片資訊或 None。"""
    headers = {"Authorization": PEXELS_API_KEY}
    params = {"query": query, "per_page": 1, "orientation": "landscape"}

    try:
        resp = requests.get(PEXELS_SEARCH_URL, headers=headers, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        if data.get("photos"):
            photo = data["photos"][0]
            return {
                "url": photo["src"]["medium"],
                "photographer": photo["photographer"],
                "photographer_url": photo["photographer_url"],
                "photo_url": photo["url"],
                "alt": photo.get("alt", query),
            }
    except requests.RequestException as e:
        print(f"  [錯誤] Pexels API 請求失敗: {e}")
    return None


def download_image(url: str, save_path: Path) -> bool:
    """下載圖片到指定路徑。"""
    try:
        save_path.parent.mkdir(parents=True, exist_ok=True)
        resp = requests.get(url, timeout=30)
        resp.raise_for_status()
        save_path.write_bytes(resp.content)
        return True
    except requests.RequestException as e:
        print(f"  [錯誤] 下載圖片失敗: {e}")
        return False


def has_image_nearby(lines: list[str], heading_idx: int) -> bool:
    """檢查 h2 標題後 3 行內是否已有圖片。"""
    for i in range(heading_idx + 1, min(heading_idx + 4, len(lines))):
        line = lines[i].strip()
        if re.match(r"!\[.*\]\(.*\)", line):
            return True
        # 遇到下一個標題就停止
        if line.startswith("## ") or line.startswith("# "):
            break
    return False


def should_skip_section(title: str) -> bool:
    """判斷是否應該跳過此章節（前言、結語等）。"""
    clean = re.sub(r"[【】「」『』]", "", title).strip()
    for keyword in SKIP_SECTIONS:
        if keyword in clean:
            return True
    return False


def find_h2_sections(lines: list[str]) -> list[dict]:
    """找出所有 h2 章節及其首段內容。"""
    sections = []
    for i, line in enumerate(lines):
        stripped = line.strip()
        if not stripped.startswith("## "):
            continue

        title = stripped[3:].strip()

        # 跳過不需要圖片的章節
        if should_skip_section(title):
            continue

        # 已有圖片則跳過
        if has_image_nearby(lines, i):
            continue

        # 收集首段（h2 後的第一段非空文字）
        first_para = ""
        for j in range(i + 1, min(i + 10, len(lines))):
            para_line = lines[j].strip()
            if not para_line or para_line == "---":
                continue
            if para_line.startswith("#"):
                break
            first_para = para_line
            break

        sections.append({
            "index": i,
            "title": title,
            "first_paragraph": first_para,
        })

    return sections


def process_article(article_path: Path, dry_run: bool = False) -> None:
    """處理單篇文章。"""
    content = article_path.read_text(encoding="utf-8")
    lines = content.split("\n")

    # 從 front matter 取 slug
    slug_match = re.search(r"^slug:\s*(.+)$", content, re.MULTILINE)
    if not slug_match:
        print(f"  [跳過] 找不到 slug: {article_path.name}")
        return
    slug = slug_match.group(1).strip()

    print(f"\n📄 處理文章: {article_path.name} (slug: {slug})")

    # 找出候選 h2 章節
    sections = find_h2_sections(lines)
    if not sections:
        print("  沒有需要加圖的章節")
        return

    # 限制最多處理 MAX_IMAGES_PER_ARTICLE 個章節
    # 優先選擇帶有【獨家】標記的，或排在文章中間的章節
    def section_priority(sec):
        title = sec["title"]
        score = 0
        if "獨家" in title:
            score += 10
        # 偏好文章中段的章節
        pos = sec["index"] / max(len(lines), 1)
        if 0.2 < pos < 0.8:
            score += 5
        return -score  # 負數因為 sorted 是升序

    sections = sorted(sections, key=section_priority)[:MAX_IMAGES_PER_ARTICLE]
    # 恢復原始順序（從後往前插入需要）
    sections = sorted(sections, key=lambda s: s["index"], reverse=True)

    images_dir = BLOG_DIR / slug / "images"
    images_added = 0

    for sec in sections:
        title = sec["title"]
        query = generate_search_query(title, sec["first_paragraph"])
        filename = sanitize_filename(title)
        # 若標題無法產生有意義的檔名，改用搜尋關鍵字
        if filename == "section":
            filename = re.sub(r"[^a-z0-9]+", "-", query.lower()).strip("-")[:40] or "section"
        filename += ".jpg"

        print(f"\n  ## {title}")
        print(f"     搜尋關鍵字: {query}")
        print(f"     圖片檔名: {filename}")

        if dry_run:
            print("     [預覽模式] 跳過下載")
            images_added += 1
            continue

        # 搜尋 Pexels
        photo = search_pexels(query)
        if not photo:
            print("     [跳過] 找不到合適的圖片")
            time.sleep(1)
            continue

        print(f"     攝影師: {photo['photographer']}")
        print(f"     圖片來源: {photo['photo_url']}")

        # 下載圖片
        save_path = images_dir / filename
        if not download_image(photo["url"], save_path):
            time.sleep(1)
            continue

        print(f"     已下載: {save_path}")

        # 在 h2 標題後插入圖片 markdown
        idx = sec["index"]
        alt_text = photo["alt"] if photo["alt"] else title
        image_md = (
            f"\n![{alt_text}](images/{filename})\n"
            f"*Photo by [{photo['photographer']}]({photo['photographer_url']}) "
            f"on [Pexels]({photo['photo_url']})*\n"
        )
        lines.insert(idx + 1, image_md)

        # 因為從後往前處理，不需要調整 index
        images_added += 1

        # 尊重 API 速率限制
        time.sleep(1)

    if images_added > 0 and not dry_run:
        # 寫回文章檔案
        new_content = "\n".join(lines)
        article_path.write_text(new_content, encoding="utf-8")
        print(f"\n  ✅ 已為 {slug} 加入 {images_added} 張圖片")
    elif dry_run:
        print(f"\n  [預覽] 將為 {slug} 加入 {images_added} 張圖片")


def main():
    parser = argparse.ArgumentParser(description="為部落格文章 h2 章節加入 Pexels 圖片")
    parser.add_argument("--slug", type=str, help="只處理指定 slug 的文章")
    parser.add_argument("--dry-run", action="store_true", help="預覽模式，不下載圖片")
    args = parser.parse_args()

    if not ARTICLES_DIR.exists():
        print(f"[錯誤] 找不到文章目錄: {ARTICLES_DIR}")
        sys.exit(1)

    # 收集要處理的文章
    articles = sorted(ARTICLES_DIR.glob("*.md"))
    if not articles:
        print("[錯誤] 文章目錄中沒有 .md 檔案")
        sys.exit(1)

    if args.slug:
        # 篩選指定 slug 的文章
        matched = []
        for a in articles:
            content = a.read_text(encoding="utf-8")
            slug_match = re.search(r"^slug:\s*(.+)$", content, re.MULTILINE)
            if slug_match and slug_match.group(1).strip() == args.slug:
                matched.append(a)
        if not matched:
            print(f"[錯誤] 找不到 slug 為 '{args.slug}' 的文章")
            sys.exit(1)
        articles = matched

    mode = "預覽模式" if args.dry_run else "執行模式"
    print(f"🔍 {mode} — 共 {len(articles)} 篇文章待處理")
    print(f"   每篇最多加 {MAX_IMAGES_PER_ARTICLE} 張圖片")

    for article in articles:
        process_article(article, dry_run=args.dry_run)

    print("\n🎉 全部完成！")


if __name__ == "__main__":
    main()
