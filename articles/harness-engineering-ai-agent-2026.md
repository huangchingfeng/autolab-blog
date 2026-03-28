---
title: "Harness Engineering：為什麼你的 AI Agent Demo 很強、上線就爛？2026 年 AI 工程最重要的觀念轉變"
slug: "harness-engineering-ai-agent-2026"
date: "2026-03-28"
description: "從 Prompt Engineering 到 Context Engineering 到 Harness Engineering，2026 年 AI 工程的典範轉移。OpenAI 三人團隊靠環境設計產出百萬行程式碼，完美解釋為什麼 agent demo 很強、實際用就爛。"
tags: [AI, Harness Engineering, AI Agent, 企業AI]
author: "黃敬峰（AI峰哥）"
seo_title: "Harness Engineering 完整解析：2026 年 AI Agent 從 Demo 到上線的關鍵"
seo_description: "什麼是 Harness Engineering？為什麼 78% 企業的 AI Agent 死在上線那天？從 OpenAI Codex 團隊的實戰案例，解析 2026 年 AI 工程最重要的觀念轉變。"
focus_keyphrase: "Harness Engineering"
---

# Harness Engineering：為什麼你的 AI Agent Demo 很強、上線就爛？

> 社群版講了核心觀念，本文加上獨家深度分析和操作指南。
> 想了解什麼是 Harness Engineering、為什麼它在 2026 年突然成為最重要的 AI 工程概念，這篇文章幫你拆解清楚。

---

## 重點回顧

AI 工程在三年內經歷了三次典範轉移：2024 年是 Prompt Engineering（雕琢文字），2025 年是 Context Engineering（餵對資訊），2026 年則是 Harness Engineering（設計環境）。OpenAI 內部一個三人工程團隊，透過設計完整的 harness 基礎設施，讓 Codex agent 在五個月內產出約一百萬行程式碼，零手寫。這說明了一件事：AI 的效能瓶頸不在模型，在環境。

---

## 【獨家】從馬具到 AI 基礎設施：Harness 到底是什麼？

Harness 這個字直譯是「馬具」——套在馬身上，讓馬能拉車、能轉彎、能停下來的那套裝備。如果把 AI agent 想像成一匹非常強壯的馬，那問題從來不是馬不夠壯，而是你有沒有幫牠裝上好的馬具。

在 AI 的語境裡，Harness 就是包圍在 agent 外面的整套基礎設施。它包含四個核心層面：

### 1. 工具存取（Tool Access）

Agent 可以用什麼工具？可以讀取哪些檔案？可以呼叫哪些 API？這些不是隨便開放的，而是像公司 IT 部門一樣，有明確的權限管理。OpenAI 的做法是寫大量的 AGENTS.md 檔案——不是給人看的文件，而是給 agent 看的「規則書」，裡面清楚定義了什麼能做、什麼不能做。

### 2. 安全護欄（Guardrails）

Agent 不能碰的東西，用系統去硬性限制，不是用 prompt 去「拜託」它。具體做法包括：

- **靜態檢查**：用 linter、type checker 等工具自動攔截不合規的程式碼
- **動態審計**：用另一個 LLM 當稽核員，檢查 agent 的輸出是否符合規範
- **行為邊界**：限制 agent 可以執行的指令範圍，例如禁止直接修改 production 資料庫

這跟我在企業培訓時常強調的觀念一樣：你不能只靠「請同仁注意資安」這種公告，你需要系統層面的防護。

### 3. 回饋迴路（Feedback Loops）

這是 Harness 最有力量的部分。Agent 做完一個步驟後，不是直接往下走，而是：

- 自動跑單元測試
- 自動做 code review
- 失敗了自動修正，再跑一次
- 直到通過所有檢查才進入下一步

研究數據顯示：光是在每個步驟之間加入一道「驗證迴路」，任務完成率就能從 83% 提升到 96%。不換模型、不改 prompt，只是多一道品質關卡。

### 4. 可觀察性（Observability）

人類需要看得到 agent 在做什麼。監控儀表板、日誌記錄、異常告警——這些不是「有更好」，是「沒有就會出事」。

OpenAI 團隊甚至設計了「熵值管理」機制：派專門的「清理 agent」定期巡邏程式碼庫，找出文件過時、命名不一致、規則被違反的地方，自動修正。就像辦公室有專人定期整理文件歸檔一樣。

---

## 【獨家】為什麼 Agent Demo 超強、上線就爛？完整拆解

這是 2026 年最困擾企業的問題。數據很殘酷：

- **78% 的企業**已經有 AI agent 試點專案
- 但只有**不到 15%** 成功部署到正式環境
- **89% 的失敗**可以歸結為五個環境問題

這五個問題分別是：

### 問題一：跟舊系統整合太複雜

大部分企業不是從零開始建系統，而是有一堆已經跑了十幾年的 ERP、CRM、內部系統。Agent 要跟這些系統溝通，需要的不只是 API 串接，還有資料格式轉換、錯誤處理、權限協調。

### 問題二：大量處理時品質不穩

Demo 的時候只跑 10 筆資料，品質當然好。正式環境一天跑 10,000 筆，各種邊界案例就冒出來了。沒有 harness 裡的驗證迴路，品質根本守不住。

### 問題三：缺乏監控工具

Agent 出錯了，你知道嗎？如果沒有可觀察性層，很多時候 agent 在那邊安靜地犯錯，你到月底對帳才發現。

### 問題四：組織內沒人負責

AI agent 歸 IT 管還是業務管？出問題找誰？很多企業連這個都沒想清楚就上線了。

### 問題五：領域訓練資料不夠

Agent 需要理解你的業務邏輯，但你的內部文件可能不夠完整、不夠結構化，agent 根本抓不到重點。

注意，這五個原因**沒有一個**是「模型太笨」。全部都是環境問題。

我帶過超過 400 家企業做 AI 培訓，看到一個很明顯的模式：大家花 80% 的精力在選模型、調 prompt，卻只花 20% 在設計 AI 的工作環境。比例應該反過來。

---

## 【獨家】企業導入 AI Agent 的 Harness 設計清單

如果你是老闆或 IT 主管，想讓 AI agent 真正上線而不只是做 demo，這是我建議的檢查清單：

**基礎層（必做）**：
- [ ] 寫好給 agent 看的規則文件（不是給人看的 SOP）
- [ ] 定義工具存取權限——哪些 API 可以用、哪些資料可以讀
- [ ] 設定行為邊界——什麼事不能做，用系統限制不是用文字叮嚀
- [ ] 建立基本的日誌記錄和錯誤告警

**進階層（上線前必做）**：
- [ ] 在每個步驟之間加入驗證迴路
- [ ] 設計自動測試流程——agent 的輸出要能自動被檢驗
- [ ] 建立監控儀表板——你要隨時看得到 agent 在做什麼
- [ ] 指定 agent 的負責人——出問題找誰要很清楚

**長期維護（上線後必做）**：
- [ ] 定期審查 agent 的輸出品質
- [ ] 更新規則文件（業務邏輯會變，文件要跟著變）
- [ ] 清理過時的設定和資料
- [ ] 收集使用者回饋，持續優化 harness

---

## 阿峰觀點

我在 2024 年花很多時間教企業寫好 prompt。2025 年開始教 RAG 和 context 設計。2026 年，我越來越常被問到的問題不是「怎麼問 AI」，而是「怎麼讓 AI 在我們公司穩定運作」。

答案就是 Harness Engineering。

LangChain 的實驗最能說明問題：在 Terminal Bench 2.0 評測上，他們不換模型、不改 prompt，只調整 harness 設計，效能就從 52.8% 跳到 66.5%，排名從 30 名外衝進前 5。Stripe 內部的 AI agent 每週合併超過 1,000 個 PR，秘密也不是用了什麼神奇模型，是設計了一套穩定的工作環境。

這告訴我們一件事：**模型是零件，Harness 才是產品。**

模型可以換。OpenAI 出新版你就升級。但你花三個月設計的那套文件系統、檢查機制、回饋迴路、監控儀表板——這才是真正的護城河。

「AI 沒變聰明，是環境變好了。」

下次有人問你該用 ChatGPT 還是 Claude 還是 Gemini，你可以反問一句：你的 AI 有一套好的工作環境嗎？

---

## 本文提到的資源

| 資源 | 說明 |
|------|------|
| OpenAI: Harness Engineering | OpenAI 官方部落格文章，描述 Codex 團隊如何用 harness 產出百萬行程式碼 |
| Cen Runzhe: From Prompt to Harness Engineering | Medium 文章，系統梳理三代 AI 工程演變 |
| LangChain Terminal Bench 2.0 | 證明只改 harness 就能大幅提升 agent 效能的評測 |
| Martin Fowler: Harness Engineering | 技術大師對 Harness Engineering 的深度分析 |

---

如果你是老闆或 HR，想帶團隊導入 AI，歡迎到官網聯繫阿峰老師。
→ https://www.autolab.cloud

加入 LINE 社群跟我們一起玩 AI：
→ https://reurl.cc/GGlLNx

---

### 關於作者
黃敬峰（AI峰哥），企業 AI 實戰培訓專家，400+ 企業合作、10,000+ 學員。
核心心法：「會用、懂用、好用、每天用」
官網：https://www.autolab.cloud
