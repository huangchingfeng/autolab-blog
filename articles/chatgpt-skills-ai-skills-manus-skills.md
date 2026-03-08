---
author: 黃敬峰（AI峰哥）
date: '2026-03-08'
description: ChatGPT 悄悄上線 Skills 功能，讓你幫 AI 設定固定工作流程。本文完整解析 Skills 操作指南、Manus 匯入教學，以及企業如何用
  Skills 解決 AI 產出不穩定的問題。
keywords:
- ChatGPT Skills
- AI Skills
- Manus Skills 匯入
- 企業AI導入
- AI工作流程
slug: chatgpt-skills-ai-skills-manus-skills
tags:
- AI
- ChatGPT
- Skills
- Manus
- 企業AI
title: ChatGPT Skills 正式登場！比 GPT 5.4 更值得注意的新功能
youtube_id: ''
---

# ChatGPT Skills 正式登場：為什麼這比 GPT 5.4 更值得你注意？

> 本文是社群貼文的完整延伸版。
> 社群版講了核心觀念，本文加上獨家深度分析和操作指南。

---

## 重點回顧

OpenAI 上週推出了 Instant 5.3 和 GPT 5.4 兩個新模型，但真正值得注意的是 ChatGPT 悄悄在設定頁面上線的「Skills」功能。Skills 讓你幫 AI 設定固定工作流程，每次執行都照著走，解決了企業用 AI 最大的痛點：產出不穩定。目前 ChatGPT 的 Skills 功能還在早期階段，Manus 在這方面更成熟，但 OpenAI 的更新速度極快，追上只是時間問題。

---

## 【獨家】Skills 完整操作指南：從建立到匯入

### 什麼是 Skills？

簡單講，Skills 就是你幫 AI 設定的一套「標準作業流程」。你把規則寫好，AI 每次執行就自動遵守，不需要你每次重新說明。

舉個例子：我建了一個「社群貼文撰寫」的 Skill，裡面規定了：
- 專有名詞（Elon Musk、Google）一律保留英文，不翻譯
- 每個段落不超過三行
- 結尾必須有行動呼籲（CTA）
- 附上正確示範和錯誤示範供 AI 參考

每次我說「幫我寫一篇 Facebook 貼文」，AI 就自動套用這些規則，品質穩定、風格一致。

### 在 ChatGPT 哪裡找到 Skills？

目前 Skills 功能只在 ChatGPT 桌面版（chatgpt.com）看得到：

1. 點擊左下角「設定」
2. 找到「Skills」選項
3. 目前只有一個預設 Skill：**Skills Creator**

Skills Creator 是一個「幫你建立 Skill 的 Skill」。你打字告訴它你想要什麼功能，它就幫你生成完整的 Skill，包含 Reference（參考資料）和 Script（執行腳本）兩個資料夾。

### 從 Manus 匯入 Skills（Step-by-Step）

如果你已經在 Manus 上建了 Skills，可以直接匯入 ChatGPT：

1. **進入 Manus** → 左下角點「Skills」
2. **選擇要匯出的 Skill** → 點進去
3. **點右下角三點** → 選「下載」→ 存成 ZIP 檔到桌面
4. **回到 ChatGPT** → 設定 → Skills → 右上角「New Skill」
5. **上傳剛才的 ZIP 檔**
6. 看到**綠色勾勾**表示匯入成功

注意：如果格式出問題（沒有綠色勾勾），回到 Manus 調整 Skill 的結構再重新匯出。

### 使用 Skill 的方式

在 ChatGPT 對話框輸入 `/`（斜線），就會跳出你所有的 Skills 列表，選擇對應的 Skill 即可。

### 目前的限制

我實測發現一個問題：**ChatGPT 目前無法自動判斷什麼時候該使用哪個 Skill**。

測試方式：開新對話，不刻意選 Skill，直接說「幫我寫一篇 Facebook 貼文」。結果 ChatGPT 完全沒有自動套用我上傳的社群貼文 Skill。

相比之下，Manus 在自動判斷方面做得更好，而且有更多預設 Skills 可以直接使用。

---

## 【獨家】企業 AI 導入的關鍵：為什麼 Skills 是必備的？

### 企業用 AI 的最大痛點

我帶過台積電、國泰金控、中華電信等超過 400 家企業做 AI 培訓，最常聽到的問題永遠是同一個：

**「AI 產出品質不穩定，每次結果都不一樣，怎麼辦？」**

你叫 AI 寫一封客戶信，這次正式、下次口語。你叫它整理報告，這次有圖表、下次純文字。在個人使用還好，但在企業裡面，這種不確定性是災難。

行銷部門不能每次發貼文都靠運氣。客服部門不能每次回覆客戶都語氣不同。品管部門不能每次檢查報告都格式不一。

### Skills 如何解決這個問題

Skills 的核心價值就是**標準化**。你把以下東西寫進 Skill：

- **品牌規範**：用色、語氣、禁用詞
- **寫作風格**：段落長度、標題格式、CTA 模板
- **審核標準**：必須包含的元素、品質檢查清單
- **參考範例**：正確示範和錯誤示範

AI 每次執行時都會自動遵守這些規則，輸出品質自然就穩定了。

### 進階應用：Skills + API 串接

Skills 搭配 Connectors（API 串接），威力更大：

- **有 API 的系統**：AI 可以直接進入你公司的 CRM、ERP、專案管理工具操作
- **沒有 API 的系統**：AI 可以控制瀏覽器，自動完成登入、點擊、填表等操作

想像一下：行銷部門建了一個「週報發布」的 Skill，每週五下午 AI 自動從 Google Analytics 抓數據、生成週報、上傳到 Notion、發通知到 Slack。全程不需要人介入。

這就是 Skills 的終極形態：**不是讓 AI 聊天，是讓 AI 執行任務。**

---

## 阿峰觀點

我自己的判斷是這樣的：AI 的使用方式正在經歷一次典範轉移。

**過去**：每次跟 AI 對話都從零開始，效果靠運氣。
**現在**：用 Skills 設定好流程，啟動對應的 Skill 執行任務，效果穩定。
**未來**：每個部門都有自己的 Skill 庫，AI 成為真正的「數位同事」。

懂得設計好的 Skills，等於幫公司建立了一套 AI 可以反覆執行的標準作業流程。這不是給人看的 SOP，是給 AI 跑的 SOP。

我常跟學員說：「你是機長，AI 是機組人員。」而 Skills，就是你寫給機組人員的操作手冊。手冊寫得越好，飛行越穩。

目前 ChatGPT 的 Skills 功能還在早期，但 OpenAI 每隔 2-3 天就更新一次的速度，我相信很快就會追上 Manus。現在開始學習設計 Skills，等到功能成熟時，你就能領先同事一大步。

---

## 本文提到的資源

| 工具 | 連結 | 說明 |
|------|------|------|
| ChatGPT | https://chatgpt.com | OpenAI 的 AI 對話工具，已支援 Skills |
| Manus | https://manus.im | 支援 Skills 的 AI 工具，可匯出 ZIP 到 ChatGPT |

---

如果你是老闆或 HR，想帶團隊導入 AI，歡迎到官網聯繫阿峰老師。
→ https://www.autolab.cloud

加入 LINE 社群，跟我們一起玩 AI：
→ https://reurl.cc/GGlLNx

---

### 關於作者
黃敬峰（AI峰哥），企業 AI 實戰培訓專家，400+ 企業合作、10,000+ 學員。
核心心法：「會用、懂用、好用、每天用」
官網：https://www.autolab.cloud

---