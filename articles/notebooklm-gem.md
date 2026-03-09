---
author: 黃敬峰（AI峰哥）
date: '2026-03-09'
description: NotebookLM 可以像手機裝外掛！把 Gem 的行為指示變成可勾選技能，一個筆記本搞定所有工作流。四步驟完整教學，含指令架構師、動態指令解析、實戰案例。
keywords:
- NotebookLM 技能
- 萬卷之王
- NotebookLM 教學
- Gem 外掛
- NotebookLM 自訂提示詞
slug: notebooklm-gem
tags:
- NotebookLM
- Gem
- AI教學
- Google
- 萬卷之王
title: NotebookLM 萬卷之王：一個筆記本裝無限技能，四步驟完整設定教學
youtube_id: I-7AvLSHJ5Q
---

# NotebookLM 萬卷之王：一個筆記本裝無限技能，四步驟完整教學

> 本文是 YouTube 影片「NotebookLM 萬卷之王：一個筆記本裝無限技能，告別 Gem 地獄！四步驟完整教學」的延伸閱讀版。
> 影片講了核心觀念，本文加上獨家分析和實務操作建議。
> 影片版本：https://www.youtube.com/watch?v=I-7AvLSHJ5Q

---

## 影片重點回顧

Google 的 NotebookLM 其實可以像手機一樣「裝外掛」。核心概念是把 Gemini Gem 的行為指示，變成 NotebookLM 的可勾選技能。只需要四個步驟：製作指令架構師 Gem、製作生圖專用 Gem、設定動態指令解析提示詞、新增技能文件。設定完成後，一個筆記本就能裝無限個技能，勾選即切換，告別 Gem 欄位不夠用的痛點。

---

## 【獨家】為什麼 NotebookLM 比 Gem 更適合當技能中心

![A colorful assortment of polished gemstones showcasing natural beauty and luster.](images/notebooklm-gem.jpg)
*Photo by [Markus Winkler](https://www.pexels.com/@markus-winkler-1430818) on [Pexels](https://www.pexels.com/photo/a-pile-of-colorful-stones-and-rocks-19902306/)*


### Gem 的根本限制

很多人把 Gem 當成萬能工具，做了十幾個不同功能的機器人。但用了一陣子之後，你一定會遇到兩個問題。

第一個是介面限制。Gemini 左邊的釘選欄位最多只有五個，但你可能做了十幾個 Gem。每次要找特定的 Gem 都要滑老半天，工作節奏完全被打斷。

第二個是更根本的問題：**遵照度**。Gem 在處理長文件、大量資料時，會開始摻雜自己的想法。你明明給了它一份 50 頁的 PDF，但它的回應裡會出現一些 PDF 裡根本沒有的內容。

### NotebookLM 的天然優勢

NotebookLM 的設計哲學完全不同。它的核心邏輯是：**只用你提供的資料來回應**。你餵它什麼，它就用什麼。不會亂加、不會腦補、不會跑題。

這個特性讓 NotebookLM 天生適合當「技能執行者」。因為技能的本質就是一套規則，你需要 AI 嚴格按照規則來執行，而不是自由發揮。

### 技能 vs Gem 的本質差異

| 面向 | Gem | NotebookLM 技能 |
|------|-----|-----------------|
| 數量限制 | 釘選 5 個，其他要翻找 | 無限，勾選即用 |
| 資料遵照度 | 中等，會摻雜自己的想法 | 高，完全依照你的資料 |
| 切換方式 | 開新對話、找 Gem | 勾選/取消勾選 |
| 技能更新 | 進入 Gem 編輯頁修改 | 更新 Google 文件自動同步 |
| 組合使用 | 不行，一次只能用一個 | 可以同時勾選多個技能 |

這就是為什麼「萬卷之王」不只是一個技巧，而是一個工作流的升級。

---

## 【獨家】四步驟深度拆解：每一步的眉角和注意事項

![A blue SIM card on a dark background with vibrant red and purple accents.](images/technology.jpg)
*Photo by [Pascal 📷](https://www.pexels.com/@userpascal) on [Pexels](https://www.pexels.com/photo/minimalist-blue-sim-card-with-bold-colors-33092906/)*


### Step 1：指令架構師 Gem — 被低估的超級工具

影片裡提到「機器人生機器人」，這不是噱頭，是真的很實用。

傳統做法是你自己寫 Gem 的行為指示。但行為指示要寫得好，需要考慮角色設定、輸出格式、視覺規範、邊界條件。大部分人寫出來的指示不夠完整，導致 Gem 的行為不穩定。

指令架構師的價值在於：你只需要用自然語言描述「我要一個什麼功能的機器人」，它就幫你產出一套結構完整的行為指示。

**實務建議：**
- 描述需求時越具體越好。不要說「幫我做一個寫文案的機器人」，要說「幫我做一個能把課程大綱轉換成 LinkedIn 貼文的機器人，每篇 300 字以內，用教練語氣」
- 產出的行為指示先在 Gem 裡測試幾輪，確認行為穩定後再存成技能
- 一個技能只做一件事，不要塞太多功能

### Step 2：生圖專用 Gem — 解決 NotebookLM 的最大短板

NotebookLM 不能直接生成圖片，這是目前最大的限制。但可以用「兩段式」策略繞過去：

1. 在 NotebookLM 裡用技能生成圖片的提示詞（比如 YAML 格式的描述）
2. 把提示詞貼到生圖專用 Gem，讓它直接出圖

這個生圖 Gem 的關鍵設計是「不囉嗦」。一般你跟 Gemini 說要生圖，它會先聊一堆。但這個 Gem 你貼提示詞，它就直接生，非常乾脆。

**進階技巧：**
- 在生圖 Gem 的行為指示裡加上「不要問問題，直接根據提示詞生成」
- 可以上傳角色設定圖，讓生成的圖片保持角色一致性
- 建議用 YAML 格式輸出提示詞，結構清楚不會漏資訊

### Step 3：動態指令解析專家 — 系統的靈魂

這是整個萬卷之王系統的核心。你在 NotebookLM 的「筆記本設定 → 自訂提示詞」裡，貼上一段特殊的提示詞。

這段提示詞的作用是告訴 NotebookLM 一個新規則：

> 如果你在來源資料裡偵測到行為指令、角色設定或操作指令的內容，就自動把它內化為自己的運作邏輯。

白話說，就是讓 NotebookLM 學會「讀技能、裝技能」。

**注意事項：**
- 自訂提示詞有字數限制，要精簡但完整
- 如果你發現回答開始走偏，清除對話紀錄重來（NotebookLM 有記憶效應）
- 不衝突的技能可以同時勾選使用

### Step 4：新增技能 — 兩種方式各有優缺

**方式一：用指令架構師在 NotebookLM 裡直接生成**
- 優點：快速，不用離開 NotebookLM
- 缺點：生成的內容在 NotebookLM 的對話裡，不方便後續管理

**方式二：存成 Google 文件加入來源**
- 優點：更新文件時 NotebookLM 自動同步，方便分享給團隊
- 缺點：多一個步驟

建議長期使用的技能用方式二，臨時測試用方式一。

---

## 阿峰觀點

![A modern humanoid robot with digital face and luminescent screen, symbolizing innovation in technology.](images/artificial-intelligence-business.jpg)
*Photo by [Kindel Media](https://www.pexels.com/@kindelmedia) on [Pexels](https://www.pexels.com/photo/low-angle-shot-of-robot-8566526/)*


我服務過超過 400 家企業，從台積電到傳統製造業，最常聽到的抱怨就是「AI 工具太多了，每個都要學」。

萬卷之王的價值不在於它有多炫，而在於它解決了一個真實的工作流問題：**如何在一個介面裡完成多種 AI 任務，而不用在不同工具之間跳來跳去**。

想做漫畫就裝漫畫技能，想做溝通就裝溝通技能，想做教學就裝教學技能。一個筆記本，搞定所有事。

這才是 AI 工具應該有的樣子：不是讓你學更多工具，而是讓你用更少的工具做更多的事。

---

## 本文提到的資源

| 工具 | 連結 | 說明 |
|------|------|------|
| NotebookLM | https://notebooklm.google.com | Google 的 AI 筆記工具 |
| Google Gemini | https://gemini.google.com | Google 的 AI 助手（Gem 功能） |

---

📌 企業 AI 培訓 — 阿峰老師服務過台積電、國泰金控、中華電信等超過 400 家企業
→ https://www.autolab.cloud

---

### 關於作者
黃敬峰（AI峰哥），企業 AI 實戰培訓專家，400+ 企業合作、10,000+ 學員。
核心心法：「會用、懂用、好用、每天用」
官網：https://www.autolab.cloud