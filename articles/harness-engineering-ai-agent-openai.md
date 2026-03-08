---
author: 黃敬峰（AI峰哥）
date: '2026-03-09'
description: OpenAI 發表 Harness Engineering 研究，AI Agent 五個月從零寫出百萬行程式碼。拆解三大核心教訓、台灣企業實務對照，以及如何在你的工作中應用駕馭工程思維。
keywords:
- 駕馭工程
- Harness Engineering
- AI Agent 寫程式
- OpenAI 實驗
- AI 取代工程師
slug: harness-engineering-ai-agent-openai
tags:
- AI
- OpenAI
- HarnessEngineering
- 駕馭工程
- AIAgent
- 軟體開發
title: OpenAI 駕馭工程：AI Agent 五個月零手寫百萬行程式碼，軟體開發典範轉移
youtube_id: yvJYy-Pzz7o
---

# OpenAI 駕馭工程實驗：AI Agent 五個月零手寫，從零打造百萬行程式碼軟體

> 本文是 YouTube 影片「OpenAI 實驗震撼：五個月零手寫，AI Agent 從零寫出百萬行程式碼！駕馭工程時代來了」的延伸閱讀版。
> 影片講了核心觀念，本文加上獨家分析和實務操作建議。
> 影片版本：https://www.youtube.com/watch?v=yvJYy-Pzz7o

---

## 影片重點回顧

OpenAI 發表了「Harness Engineering（駕馭工程）」研究，他們從 2025 年 8 月開始，讓 AI Agent 從一個空的程式碼倉庫，五個月寫出超過一百萬行程式碼，打造出一個完整的軟體產品。整個過程中，沒有任何一個人類工程師手寫過任何一行程式碼——包含產品程式、測試、CI/CD、內部文件，全部由 Agent 完成。

---

## 【獨家】駕馭工程的三大核心教訓與台灣企業的實務對照

![Abstract blurred motion of people walking indoors, depicting urban life and busy routines.](images/business.jpg)
*Photo by [RPA studio](https://www.pexels.com/@octocat) on [Pexels](https://www.pexels.com/photo/blurred-silhouettes-of-commuters-indoors-33289065/)*


### 1. 指令架構：先給地圖，不給百科全書

OpenAI 在實驗初期踩了一個很典型的坑：他們把所有規則都塞進一個巨大的 `agents.md` 檔案裡，結果 Agent 讀不完就隨便抓重點，很多規則被忽略。

後來他們把 `agents.md` 縮減到只有一兩百行，變成一個「目錄」。Agent 需要深入了解某個主題時，再自己去讀對應的詳細文件。

**台灣企業實務對照：**

我服務過超過 400 家企業，從台積電、國泰金控到傳統製造業，最常看到的問題就是「一次塞太多」。不管是 Prompt 還是 SOP 文件，大家習慣把所有東西寫在一起。

正確的做法：
- **主文件只放架構和目錄**，不超過 200 行
- **細節放在子文件**，讓 AI 按需求自己去讀
- **每個子文件聚焦單一主題**，不要混合

這個原則不只適用於 AI Agent 開發，也適用於你每天在用的 ChatGPT 或 Claude。你的 Prompt 越簡潔清楚，AI 的回應品質就越高。

### 2. 瓶頸翻轉：從「確認再放行」到「先做再修正」

實驗中期最震撼的發現：最大的瓶頸不是 AI，是人類。

人類工程師花在審核程式碼和 QA 測試的時間，反而拖慢了 Agent 的開發進度。於是他們把大部分程式碼審核也交給另一個 Agent，因為「修正錯誤的成本很低，但等待的成本很高」。

**這對企業流程意味著什麼？**

傳統企業的審核流程通常是：做完 → 主管審核 → 修改 → 再審核 → 通過。一個簡單的文件可能要來回三四次。

但如果你導入 AI 輔助，實作速度會快十倍以上。這時候「等待審核」就變成最大的浪費。

建議的新流程：
1. **AI 快速產出初稿**（幾分鐘）
2. **另一個 AI 做初步審核**（品質檢查、格式確認）
3. **人類只做最終決策**（方向判斷、品牌調性）

這樣既保留了人類的判斷力，又不讓人類的速度成為瓶頸。

### 3. 端到端自動化：Agent 已經能完成工程師的完整工作流程

到實驗後期，Agent 已經可以自己看到 Bug、研究解法、寫修正程式碼、開 PR、回覆 Code Review 評論，甚至自己把 PR 合併。

這代表什麼？工程師過去十年的標準工作流程——接到 Bug、分析需求、規劃方案、實作、Code Review、Merge——全部可以被 Agent 端到端完成。

**但這不代表工程師失業。** 這代表工程師的角色從「執行者」變成「架構師」。你不再需要自己寫每一行程式碼，但你需要：
- 定義系統架構
- 設定 Agent 的邊界和規則
- 確保 AI 產出符合品質標準
- 做架構層級的關鍵決策

---

## 【獨家】如何在你的工作中應用「駕馭工程」思維

![A blue SIM card on a dark background with vibrant red and purple accents.](images/technology.jpg)
*Photo by [Pascal 📷](https://www.pexels.com/@userpascal) on [Pexels](https://www.pexels.com/photo/minimalist-blue-sim-card-with-bold-colors-33092906/)*


不管你是不是工程師，「駕馭工程」的核心思維都可以應用在日常工作中。

### Step 1：盤點你的工作流程

列出你每天做的事情，標記哪些是「執行性工作」（重複、有規則、可以標準化），哪些是「決策性工作」（需要判斷、創意、人際互動）。

### Step 2：把執行性工作交給 AI

- 寫報告 → ChatGPT / Claude 初稿 + 你審核
- 數據分析 → AI 跑分析 + 你做決策
- Email 回覆 → AI 草稿 + 你確認語氣
- 會議紀錄 → AI 轉錄 + 你補充重點

### Step 3：建立你的「agents.md」

寫一份你的工作規則文件，告訴 AI 你的偏好、標準、常用格式。這份文件就是你的「駕馭」工具，讓 AI 在你設定的範圍內高效運作。

### Step 4：持續迭代

跟 OpenAI 的實驗一樣，你的規則會不斷修正。遇到 AI 做不好的事情，不是重試一次，而是去想「我的指令缺少什麼？」然後更新你的規則文件。

---

## 阿峰觀點

![Abstract illustration of AI with silhouette head full of eyes, symbolizing observation and technology.](images/artificial-intelligence.jpg)
*Photo by [Tara Winstead](https://www.pexels.com/@tara-winstead) on [Pexels](https://www.pexels.com/photo/an-artificial-intelligence-illustration-on-the-wall-8849295/)*


我常說：「你是機長，AI 是機組人員。」

機長不需要自己推餐車、自己檢查引擎。但機長要知道飛機的整體狀態，要做關鍵決策。

很多人擔心「認知外包」——過度使用 AI 會讓思考能力下降。但我實際深度使用這些工具之後，發現我的認知反而是上升的。AI 看到我以前沒看到的東西，提出我沒想過的設計方式。透過深度協作，我花更多時間在思考架構和策略。

會思考的人，有了 AI 之後會思考得更好。不思考的人，有沒有 AI 都一樣不思考。

2026 年的現在，手寫程式碼還是主流。但五年後回頭看，手寫程式碼可能就像現在看手抄報告一樣，是一門古老的技藝。

---

## 本文提到的資源

| 工具 | 連結 | 說明 |
|------|------|------|
| OpenAI | https://openai.com | Harness Engineering 研究發表方 |
| Claude AI | https://claude.ai | Anthropic 的 AI 助手 |
| ChatGPT | https://chatgpt.com | OpenAI 的 AI 助手 |

---

📌 企業 AI 培訓 — 阿峰老師服務過台積電、國泰金控、中華電信等超過 400 家企業
→ https://www.autolab.cloud

---

### 關於作者
黃敬峰（AI峰哥），企業 AI 實戰培訓專家，400+ 企業合作、10,000+ 學員。
核心心法：「會用、懂用、好用、每天用」
官網：https://www.autolab.cloud