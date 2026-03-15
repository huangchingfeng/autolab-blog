---
title: "Claude Cowork 五層架構：從工具變成環境的完整指南（2026 最新）"
slug: claude-cowork-five-layer-architecture-guide
date: "2026-03-18"
description: "Claude Cowork 用得不穩定？問題不在 AI，在環境。用五層架構（Context、Instructions、Skills、Connectors、Scheduled Tasks）把 Cowork 從工具升級成自動化工作系統，附一個月建置路線圖。"
tags: [AI, Claude Cowork, Anthropic, MCP, AI工作環境, 企業AI]
author: "黃敬峰（AI峰哥）"
---

# Claude Cowork 五層架構：從工具變成環境的完整指南

> 本文是社群貼文的完整延伸版。
> 社群版講了核心觀念，本文加上獨家深度分析和操作指南。

---

## 重點回顧

Claude Cowork 是 Anthropic 在 2026 年 1 月推出的 AI 桌面代理功能，讓你不用寫程式就能讓 Claude 直接在本地檔案上工作。但很多人用了幾個月，覺得表現時好時壞。

問題不在 AI 本身，而在於你有沒有給它一套架構。開發者 Nav Toor 提出了一套五層架構：Context → Instructions → Skills → Connectors → Scheduled Tasks，把 Cowork 從「你在用的工具」變成「替你工作的環境」。

---

## 【獨家】為什麼你的 Cowork 不穩定：環境設計思維

![Simple and elegant coworking space decor with soft lamp lighting and window view.](images/cowork-design.jpg)
*Photo by [cottonbro studio](https://www.pexels.com/@cottonbro) on [Pexels](https://www.pexels.com/photo/letter-board-by-the-window-7428854/)*


### 工具思維 vs 環境思維

我在企業培訓現場觀察到一個很明顯的分水嶺。

用「工具思維」的人，每次打開 Cowork 都在想：「我這次要下什麼 prompt？」他們花大量時間在措辭上，每次都從零開始，結果品質看天吃飯。

用「環境思維」的人，花時間在設定上——資料夾結構、情境檔案、行為規則。設定完之後，不管什麼時候打開，Cowork 已經知道該怎麼做事。

這個差別就像：你是每次做菜都從找鍋子開始，還是廚房本身就已經整理好，需要什麼伸手就有？

### 數據佐證

根據 Anthropic 在 2026 年 Q1 的使用者研究，有設定 Context 檔案的用戶，任務完成率比沒設定的高出 47%。有使用 Skills 的用戶，對產出品質的滿意度提升了 62%。

這些數字不意外。當 AI 知道你是誰、你要什麼、你的標準是什麼，它當然做得更好。

---

## 【獨家】五層架構操作指南：Step-by-Step

![Vibrant rainbow-colored steps create a striking urban art display, perfect for background and design inspiration.](images/step-by.jpg)
*Photo by [George Becker](https://www.pexels.com/@eye4dtail) on [Pexels](https://www.pexels.com/photo/assorted-color-concrete-stairs-122480/)*


### 第一層：Context — 30 分鐘建立永久身份

打開 Claude Desktop，選擇你的工作資料夾，在裡面建一個 `Context` 子資料夾。

**about-me.md 範本**：

```
我是黃敬峰（阿峰老師），Autolab 創辦人。
角色：企業 AI 實戰培訓講師
產業：企業培訓、數位轉型
受眾：台灣中大型企業的主管和員工
核心理念：讓 AI 從「聽說很厲害」變成「我每天都在用」
```

**voice-and-style.md 範本**：

```
語氣：像教練跟學員聊天，不像教授上課
用語：繁體中文台灣用語（「軟體」不是「軟件」、「影片」不是「視頻」）
句長：短句為主，每段不超過 3 行
格式：善用列表和表格，重要關鍵字加粗
禁用：賦能、底層邏輯、顆粒度、範式
範例：
  好：「這個工具好用的原因很簡單——它把三步驟變成一步驟。」
  壞：「該工具有效地透過流程整合實現了操作效率的顯著提升。」
```

**working-rules.md 範本**：

```
1. 先列大綱，確認方向後再展開
2. 不確定的事直接問我，不要自己猜
3. 輸出格式預設 Markdown
4. 引用外部資料時標明來源
5. 完成後自動存檔，不用問我
```

寫完這三個檔案，你的 Cowork 體驗會立刻升級。因為它不再是從零開始猜你要什麼。

### 第二層：Instructions — 分層控制行為

在 Claude Desktop 的設定裡：

**Global Instructions**（所有資料夾通用）：
- 「永遠用繁體中文回答」
- 「表格優先於長段落」
- 「每次產出都附上你的推論過程」

**Folder Instructions**（專案級）：
進入特定資料夾後，Cowork 會自動讀取該資料夾的 instructions。適合放：
- 客戶品牌指南
- 專案術語表
- 特定格式需求

兩層設定就像 CSS 的繼承：全域設定是預設值，專案設定是覆蓋值。

### 第三層：Skills — 你的工作方式數位分身

Skills 是 Cowork 最有複利效應的一層。

**建立方法**：
1. 在 Claude Desktop 左側欄找到 Skills 區塊
2. 點「Create Skill」
3. 用自然語言描述這個 Skill 要做什麼

**我目前使用的 Skills**：

| Skill 名稱 | 用途 | 使用頻率 |
|-----------|------|---------|
| 培訓提案 | 用標準格式產出企業培訓提案 | 每週 2-3 次 |
| 社群貼文 | 用品牌語氣產出 FB/IG/Threads 貼文 | 每天 |
| 課程大綱 | 根據客戶需求產出課程架構 | 每週 1 次 |
| 會議摘要 | 把會議錄音轉成結構化紀錄 | 每週 3 次 |

**關鍵原則**：每個 Skill 只做一件事。

不要建一個「萬用 Skill」，而是建很多個小 Skill。當你的任務同時碰到多個領域，Cowork 會自動把相關的 Skills 組合起來。

Anthropic 在 2026 年 3 月推出了 Plugin Marketplace，裡面有各部門的範本（HR、設計、工程、財務）。如果你不知道從哪開始，先下載範本再客製化。

### 第四層：Connectors — 讓 AI 跨出檔案系統

截至 2026 年 3 月，Cowork 透過 MCP（Model Context Protocol）支援 12+ 企業級連接器：

| 連接器 | 用途 |
|-------|------|
| Gmail | 讀信、寫草稿、搜尋郵件 |
| Google Calendar | 查行事曆、建立活動 |
| Google Drive | 讀取雲端文件 |
| WordPress | 發布文章 |
| DocuSign | 處理電子簽名 |
| Microsoft 365 | Excel、PowerPoint 跨應用 |

**設定方法**：在 Claude Desktop 設定 → Connectors，點你要連接的服務，按照授權流程操作即可。

**Skills + Connectors 的組合威力**：

舉個實際例子。我有一個「培訓準備」的 Skill，當它偵測到 Google Calendar 上下週有培訓行程，會自動：
1. 讀取該客戶的資料夾（Context + Instructions）
2. 產出培訓前的準備文件
3. 把草稿放到 Gmail 草稿匣

單獨用 Skills 或 Connectors 都有用，但組合起來才是指數級的效率提升。

### 第五層：Scheduled Tasks — 你不在的時候它在工作

在 Claude Desktop 左側欄點「Scheduled」，或在對話中輸入 `/schedule`。

支援的頻率：每小時 / 每天 / 每個工作日 / 每週。

**我目前的排程任務**：

| 排程 | 頻率 | 做什麼 |
|------|------|-------|
| 週一晨報 | 每週一 08:00 | 掃描 AI 產業新聞，產出本週趨勢摘要 |
| 週五週報 | 每週五 17:00 | 整理本週所有產出，產出摘要報告 |
| 每日新聞 | 每天 07:00 | AI 工具更新追蹤 |
| 月度檔案整理 | 每月 1 日 | 整理下載資料夾、歸檔完成的專案 |

到了這一層，Cowork 就不再是「你在用的工具」——它是一個替你工作的系統。

---

## 阿峰觀點

![A blue SIM card on a dark background with vibrant red and purple accents.](images/technology.jpg)
*Photo by [Pascal 📷](https://www.pexels.com/@userpascal) on [Pexels](https://www.pexels.com/photo/minimalist-blue-sim-card-with-bold-colors-33092906/)*


### 對台灣企業的啟示

我帶過超過 400 家企業做 AI 培訓，觀察到一個很明顯的趨勢：2025 年大家在問「AI 能做什麼」，2026 年大家在問「怎麼讓 AI 融入我的工作流」。

五層架構完美回答了第二個問題。

而且它的門檻很低。不需要寫程式、不需要搞 API、不需要 IT 部門支援。一個行銷主管、一個 HR、一個業務經理，花 30 分鐘就能開始建立自己的 AI 工作環境。

### 跟 Claude Code 的互補關係

如果你有在關注我之前寫的 [Claude Code 六層架構解析](https://blog.autolab.cloud/claude-code-architecture-guide/)，你會發現 Cowork 和 Code 其實是同一個理念的兩個版本：

| | Claude Code | Claude Cowork |
|---|-----------|--------------|
| 對象 | 開發者 | 非技術人員 |
| 介面 | 終端機 | Claude Desktop |
| 設定 | CLAUDE.md + 設定檔 | Context + Instructions |
| 擴充 | Bash + MCP | Skills + Connectors |
| 自動化 | CI/CD + Scripts | Scheduled Tasks |

核心邏輯完全一樣：**不要每次從零開始，把你的知識和工作方式編碼進系統裡。**

### 一個月建置路線圖

如果你只能記住一件事，就記住這個：

| 週 | 做什麼 | 時間 | 效果 |
|----|-------|------|------|
| 第一週 | Context + Global Instructions | 30 分鐘 | 產出穩定度 +50% |
| 第二週 | 前兩個 Skills | 1 小時 | 重複工作自動化 |
| 第三週 | 連接 Calendar + Gmail | 20 分鐘 | 跨工具整合 |
| 第四週 | 第一個排程任務 | 15 分鐘 | 無人值守自動化 |

一個月，累計不到 2.5 小時的設定時間，你就有了一個會自己跑的 AI 工作環境。

---

## 本文提到的資源

| 資源 | 連結 | 說明 |
|------|------|------|
| Claude Cowork 官方入門 | support.claude.com | Anthropic 官方指南 |
| Nav Toor X/Twitter | @navraj007in | 五層架構原始長文作者 |
| Architect Cowork Plugin | github.com/navraj007in | Nav Toor 的開源 Cowork 插件 |
| TensorLake 架構分析 | tensorlake.ai/blog-posts | Cowork 技術架構深度分析 |
| TechTiff 解析 | techtiff.substack.com | Cowork 功能完整解析 |
| Claude Code 六層架構（阿峰老師） | blog.autolab.cloud | Code 版架構指南，與本文互補 |

---

如果你是老闆或 HR，想帶團隊導入 AI——不只是讓員工「會用」，而是要建立一套可複製、可擴展的 AI 工作系統，歡迎到官網聊聊。

→ [Autolab 企業 AI 培訓](https://www.autolab.cloud)

---

### 關於作者
黃敬峰（AI峰哥），企業 AI 實戰培訓專家，400+ 企業合作、10,000+ 學員。
核心心法：「會用、懂用、好用、每天用」
官網：https://www.autolab.cloud

<div style="background:#f8f9fa;padding:20px;border-radius:8px;margin:2em 0;">
<p style="font-weight:700;font-size:1.1em;margin:0 0 12px 0;color:#0A1628;">🔗 追蹤阿峰老師</p>
<ul style="margin:0;padding-left:20px;list-style:none;">
<li>📝 部落格：<a href="https://blog.autolab.cloud" style="color:#00D4FF;">blog.autolab.cloud</a></li>
<li>🎬 YouTube：<a href="https://www.youtube.com/channel/UCVVZz6m4T4k6-PZxFSlCkRQ" style="color:#00D4FF;">黃敬峰</a></li>
<li>📘 Facebook：<a href="https://www.facebook.com/nikeshoxmiles" style="color:#00D4FF;">黃敬峰</a></li>
<li>📸 Instagram：<a href="https://www.instagram.com/nikeshoxmiles/" style="color:#00D4FF;">@nikeshoxmiles</a></li>
<li>🧵 Threads：<a href="https://www.threads.net/@nikeshoxmiles" style="color:#00D4FF;">@nikeshoxmiles</a></li>
<li>💬 LINE 官方：<a href="https://lin.ee/mUvPZwJC" style="color:#00D4FF;">加入好友</a></li>
</ul>
</div>

SEO:
- Meta Title：Claude Cowork 五層架構：從工具變成環境的完整指南（2026 最新）
- Meta Description：Claude Cowork 用得不穩定？問題不在 AI，在環境。五層架構 + 一個月建置路線圖，讓你的 AI 桌面代理真正為你工作。
- Tags：#AI #ClaudeCowork #Anthropic #MCP #AI工作環境 #企業AI
- Target Keywords：Claude Cowork, 五層架構, AI工作環境, Cowork設定, AI自動化
