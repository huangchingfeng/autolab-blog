---
title: 讓 AI 記住你的工作方式：Claude Skill 實戰指南
slug: claude-skill-guide
date: "2026-03-10"
description: 你花在教 AI 怎麼配合你的時間，可能比 AI 幫你省的時間還多。Anthropic 官方 33 頁 Skills 指南的中文深度解讀，加上阿峰老師的企業導入建議。
tags:
  - Claude
  - AI工具
  - Skill
  - 自動化
---

# 讓 AI 記住你的工作方式：Claude Skill 實戰指南

> 本文是社群貼文的完整延伸版。
> 社群版講了核心觀念，本文加上完整的運作原理和企業導入建議。

---

## 重點回顧

你有沒有算過，每次跟 AI 合作時花多少時間在「重新解釋同樣的事」？報告格式、寫作語氣、公司規範、個人偏好——這些溝通成本加起來，可能比 AI 幫你省的時間還多。

Anthropic 出了一份 33 頁的 Skills 建構指南，解決的就是這個問題。Skill 讓你花二十分鐘把規則設定好，之後每次使用就省十倍時間。本文整理了裡面的核心邏輯，加上我在企業培訓裡的實戰觀察。

---

## 【獨家】為什麼「長 Prompt」解決不了這個問題

![A modern workspace with AI technology and digital screens.](images/ai-workspace.jpg)
*Photo by [Lukas](https://www.pexels.com/@goumbik) on [Pexels](https://www.pexels.com/photo/person-holding-silver-laptop-computer-577210/)*


很多人的第一反應是：「那我把常用的 Prompt 存起來不就好了？」

我試過。存了一兩百個 Prompt 在筆記軟體裡。用了三個月後發現三個問題。

**第一，找不到。** 存了太多之後，光是搜尋正確的 Prompt 就要花時間。有時候找到了才發現上次改過但忘記存。

**第二，改不動。** Prompt 是一大段文字，改一個地方怕影響其他地方。沒有版本管理，不知道哪個版本是最新的。

**第三，分享不了。** 你的 Prompt 只有你會用。團隊其他人不知道你的 Prompt 在哪、怎麼用、什麼時候用。

Skill 解決了這三個問題。它不是一段文字，是一個有結構的資料夾。

### Skill 的資料夾長什麼樣

```
monthly-report/
├── SKILL.md          ← 核心說明（唯一必要的檔案）
├── scripts/          ← 自動化腳本（可選）
├── references/       ← 延伸參考（可選）
└── assets/           ← 模板、範本（可選）
```

SKILL.md 裡面分兩層。最上面是一張「標籤卡」，告訴 Claude 什麼時候該用這個 Skill、它做什麼。下面才是詳細的工作指令。

這個設計很聰明。Claude 會先掃過所有 Skill 的標籤卡，只有判斷「這個跟現在的任務有關」才會往下讀詳細指令。就像你不會把整本員工手冊塞給新人——先給一頁懶人包，需要時再翻對應章節。

### 為什麼分層這麼重要

AI 的「思考空間」是有限的。如果同時載入十個 Skill，每個都是五千字的完整指令，Claude 的表現反而會下降。

分層讓 Claude 把注意力放在真正需要的地方。標籤卡只佔幾百字，不管掛載多少個 Skill 都不會拖慢速度。

---

## 【獨家】企業導入 Skill 的三個階段

![A team collaborating on technology projects with data visualization.](images/team-collaboration.jpg)
*Photo by [fauxels](https://www.pexels.com/@fauxels) on [Pexels](https://www.pexels.com/photo/photo-of-people-using-laptops-3184357/)*


我在企業培訓裡帶過超過 400 家企業，觀察到一個規律：AI 工具用得最好的團隊，不是技術最強的，而是最懂得「標準化」的。

### 階段一：個人版（1-2 週）

先讓團隊裡的 AI 愛好者各自建自己的 Skill。每個人挑一件每天都在重複做的事，花二十分鐘建出第一版。

常見的起點：
- 每週報告生成
- Email 回覆模板
- 會議紀錄整理
- 客戶提案初稿

這個階段的目標不是做出完美的 Skill，而是讓大家體驗「設定一次就不用再重複溝通」的感覺。一旦體驗過，就回不去了。

### 階段二：團隊版（1-2 個月）

個人版跑順之後，開始做團隊共用的 Skill。這時候需要的是「把最好的做法提煉出來」。

舉個例子。假設業務團隊有五個人，每個人都有自己寫客戶提案的方式。找出成交率最高的那位，把他的寫法變成 Skill。以後五個人都用同一個 Skill，品質就拉到同一個水準。

這個階段要注意的是：Skill 之間不能打架。如果你同時有「客戶提案 Skill」和「Email 回覆 Skill」，兩者的指令不能矛盾。比如一個說「語氣要正式」，另一個說「語氣要口語」，Claude 會很困惑。

### 階段三：組織版（持續迭代）

當 Skill 覆蓋了主要工作場景後，重點轉向監控和迭代。哪些 Skill 用得最頻繁？哪些一直沒人用？用了之後品質真的有提升嗎？

這就跟管理其他工具一樣——不是建完就結束，而是持續觀察、調整、優化。

---

## 【獨家】常見的三個坑和怎麼避開

![A professional developer working on code and documentation.](images/developer-coding.jpg)
*Photo by [Pixabay](https://www.pexels.com/@pixabay) on [Pexels](https://www.pexels.com/photo/blur-close-up-code-computer-546819/)*


### 坑一：Skill 做太大

最常見的錯誤。想把一個 Skill 做成萬能瑞士刀，結果指令太長、太複雜，Claude 反而搞不清楚該做什麼。

**解法**：一個 Skill 只解決一個問題。如果你發現 SKILL.md 超過五千字，就該拆成兩個。

### 坑二：標籤寫太模糊

標籤卡如果寫「幫助處理工作」，Claude 完全不知道什麼時候該用。要寫具體的觸發詞。

**好的寫法**：「生成月度業務報告。使用者說『月報』『業績報告』或『上個月的數據』時啟用。」

**壞的寫法**：「協助數據分析相關工作。」

### 坑三：建完就不管

很多人花時間建了 Skill，用了兩次就放著。三個月後發現根本不符合現在的需求了。

**解法**：每個月花十分鐘回顧一次。哪些 Skill 還在用？用的時候有沒有需要手動修正的地方？有的話就更新。

---

## 阿峰觀點

![A modern humanoid robot with digital face, symbolizing AI innovation.](images/ai-robot.jpg)
*Photo by [Tara Winstead](https://www.pexels.com/@tara-winstead) on [Pexels](https://www.pexels.com/photo/robot-pointing-on-a-wall-8386440/)*


我一直跟學員說：「你是機長，AI 是機組人員。」

但一個好的機長，不會每次起飛前都從頭跟機組人員解釋飛行流程。他會確保每個人都有標準作業程序，熟悉了之後只需要簡短的指令就能完美配合。

Skill 就是你跟 AI 之間的標準作業程序。

我自己建了幾十個 Skill，覆蓋課程設計、客戶管理、內容產出各種場景。最大的體會是：建 Skill 的過程本身就很有價值。因為你必須把自己的工作流程想清楚、寫下來。很多時候你會發現「原來我一直在做多餘的步驟」或「原來這個環節可以更精簡」。

所以 Skill 不只是 AI 工具，它也是逼你梳理工作流程的方法。

如果你只記住一件事，記住這個：找一件你每天都在重複跟 AI 說的事，花二十分鐘把它變成 Skill。不用等到完美。能持續進化的工具，比做完就放著的值錢一百倍。

---

## 本文提到的資源

| 工具/資源 | 連結 | 說明 |
|------|------|------|
| Claude.ai | https://claude.ai | Anthropic AI 對話平台 |
| Claude Code | https://docs.anthropic.com/en/docs/claude-code | Claude 開發工具 |
| skill-creator | Claude.ai 內建 | 快速建立 Skill 的官方工具 |

---

企業想導入 AI？阿峰老師服務過超過 400 家企業。
→ https://www.autolab.cloud

---

### 關於作者
黃敬峰（AI峰哥），企業 AI 實戰培訓專家，400+ 企業合作、10,000+ 學員。
核心心法：「會用、懂用、好用、每天用」
官網：https://www.autolab.cloud
