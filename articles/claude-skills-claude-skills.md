---
author: 黃敬峰（AI峰哥）
date: '2026-03-08'
description: 一次搞懂 Claude Skills 是什麼、跟提示詞和 MCP 的差別。含從零建立 Skill 的 5 步驟指南、進階組合技玩法、企業培訓實戰經驗分享。
keywords:
- Claude Skills
- Skills是什麼
- Claude Skills教學
- Skills vs MCP
- AI技能包
slug: claude-skills-claude-skills
tags:
- ClaudeSkills
- AI教學
- Anthropic
- MCP
- AI工具
- AI生產力
title: Claude Skills 完整教學：Skills vs 提示詞 vs MCP 差在哪？含實戰操作指南｜2026
youtube_id: PV9K6CjZzIs
---

# Claude Skills 完整教學：Skills、提示詞、MCP 到底差在哪？（含實戰操作指南）

> 本文是 YouTube 影片「Claude Skills 是什麼？3分鐘搞懂 Skills、提示詞、MCP 的差別」的延伸閱讀版。
> 影片講了核心觀念，本文加上獨家實戰操作指南和進階應用場景。
> 影片版本：https://www.youtube.com/watch?v=PV9K6CjZzIs

---

## 影片重點回顧

Claude Skills 是 Anthropic 推出的一項功能，讓你可以把重複性的工作流程打包成「技能包」，AI 在需要的時候自動調用。它跟提示詞最大的差別是：提示詞關掉對話就忘了，Skills 永久可用。而且 Skills 不佔用上下文窗口，一次任務可以同時調用多個 Skills。

跟 MCP 的差別也很清楚：AI 是大腦、Skills 是操作手冊、MCP 是門禁卡。它們是搭配使用，不是互相競爭。

---

## 【獨家】Claude Skills 實戰操作指南：從零開始建立你的第一個 Skill

![A young man adjusts a video camera outdoors using a tripod and plaid cover.](images/claude-skills-practice-skill.jpg)
*Photo by [Hannah Nelson](https://www.pexels.com/@hannah-nelson-390257) on [Pexels](https://www.pexels.com/photo/photo-of-man-setting-up-dslr-camera-on-tripod-1038348/)*


影片裡講了 Skills 的概念，但你可能會問：「那我實際上要怎麼建立一個 Skill？」這裡給你一個完整的 step-by-step 指南。

### Step 1：找出你最常重複的工作

先不急著動手，花 5 分鐘想一下：你每週花最多時間在哪些重複性工作上？

常見的高價值 Skills 場景：
- 每週寫週報或會議紀錄
- 定期整理數據做分析報告
- 固定格式的客戶提案或簡報
- 社群貼文的撰寫和排版
- 程式碼的 review 和重構

### Step 2：定義 Skill 的核心要素

一個好的 Skill 至少要包含這四個要素：

| 要素 | 說明 | 範例 |
|------|------|------|
| 觸發條件 | 什麼時候該啟動這個 Skill | 「當用戶要求寫週報時」 |
| 輸入格式 | AI 需要什麼資訊 | 「本週完成的事項清單」 |
| 處理流程 | 具體的操作步驟 | 「分類→摘要→排版→檢查」 |
| 輸出標準 | 成品要長什麼樣 | 「300 字以內、含時間軸」 |

### Step 3：建立 Skill 資料夾結構

在 Claude 的設定中，一個 Skill 本質上就是一個資料夾，裡面可以放：

```
my-weekly-report-skill/
├── SKILL.md          ← 主要指令檔（必要）
├── template.md       ← 週報模板
├── examples/         ← 過去的好範例
│   ├── week1.md
│   └── week2.md
└── guidelines.md     ← 寫作風格指南
```

`SKILL.md` 是最重要的檔案，它告訴 AI 這個 Skill 的觸發條件、處理流程和輸出標準。

### Step 4：寫好 SKILL.md

這是你 Skill 的「大腦」，範例：

```markdown
# 週報撰寫 Skill

## 觸發條件

![Smartphone displaying weekly report chart alongside a smartwatch on a wooden surface.](images/report-weekly.jpg)
*Photo by [RDNE Stock project](https://www.pexels.com/@rdne) on [Pexels](https://www.pexels.com/photo/close-up-of-a-smartphone-and-a-smartwatch-7947966/)*

當用戶提到「寫週報」、「weekly report」、「本週報告」時觸發。

## 輸入
- 本週完成事項
- 下週計畫
- 遇到的問題（選填）

## 處理流程
1. 將完成事項按重要性排序
2. 每項用一句話摘要
3. 套用 template.md 格式
4. 檢查字數不超過 300 字

## 輸出格式
參考 template.md
```

### Step 5：測試和迭代

建好之後，實際跑幾次，看看 AI 的輸出是不是你要的。常見需要調整的地方：
- 觸發條件太廣（誤觸）或太窄（觸發不了）
- 輸出格式跟你想的不一樣
- 缺少某些步驟導致品質不穩定

---

## 【獨家】進階玩法：Skills 的組合技

![A tattooed videographer wearing an orange cap adjusts his camera equipment outdoors, preparing for a video shoot.](images/skills.jpg)
*Photo by [Kyle Loftus](https://www.pexels.com/@kyleloftusstudios) on [Pexels](https://www.pexels.com/photo/man-in-grey-crew-neck-t-shirt-and-yellow-hat-holding-black-dslr-camera-8755154/)*


影片提到一次任務可以調用多個 Skills，這在實際應用上有非常多可能性。

### 組合技 1：內容生產線

```
逐字稿 Skill → 文章改寫 Skill → SEO 優化 Skill → 社群貼文 Skill
```

一段播客錄音進去，出來的是完整的文章 + 10 篇社群貼文 + SEO 優化建議。

### 組合技 2：數據分析流水線

```
數據清理 Skill → 統計分析 Skill → 圖表生成 Skill → 報告撰寫 Skill
```

原始 CSV 丟進去，出來的是完整的分析報告含圖表。這就是為什麼有人說三四個小時的工作可以壓縮到十分鐘。

### 組合技 3：客戶提案自動化

```
需求分析 Skill → 方案設計 Skill → 簡報生成 Skill → 報價計算 Skill
```

客戶的需求描述進去，出來的是完整的提案簡報 + 報價單。

---

## 阿峰觀點

我帶過台積電、國泰金控、中華電信等超過 400 家企業做 AI 培訓，發現一個有趣的現象：大部分公司不是不想用 AI，而是用了之後覺得「效果不穩定」。

為什麼不穩定？因為每次都靠提示詞臨場發揮，結果就像請一個實習生，今天做得好，明天又退步了。

Skills 解決的就是這個問題。一旦你把流程標準化、打包成技能包，AI 的輸出就會變得穩定、可預測、可複製。

我認為 Skills 是目前被嚴重低估的 AI 功能。不只是 Claude，未來所有大型語言模型都會採用類似的概念。現在學會，等於提前卡位。

---

## 本文提到的資源

| 工具 | 連結 | 說明 |
|------|------|------|
| Claude | claude.ai | Anthropic 的 AI 助手，Skills 功能所在 |
| Claude Skills 官方倉庫 | Claude 設定頁面 → 視力技能 | Anthropic 官方開源的 Skills 合集 |

---

📌 企業 AI 培訓服務（服務過台積電、國泰金控、中華電信等 400+ 企業）
→ https://www.autolab.cloud

---

### 關於作者
黃敬峰（AI峰哥），企業 AI 實戰培訓專家，400+ 企業合作、10,000+ 學員。
核心心法：「會用、懂用、好用、每天用」
官網：https://www.autolab.cloud

---