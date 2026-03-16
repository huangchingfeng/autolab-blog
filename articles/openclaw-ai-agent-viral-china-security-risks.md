---
title: "AI龍蝦暴紅真相：OpenClaw千人排隊裝AI，背後12%惡意技能你知道嗎？"
slug: "openclaw-ai-agent-viral-china-security-risks"
date: "2026-03-16"
description: "中國深圳騰訊總部外千人排隊安裝OpenClaw AI Agent，「養龍蝦」現象席捲中國職場。但技能市集ClawHub有335個惡意包、CVSS 8.8高危漏洞，台灣企業該如何看待這波AI Agent浪潮？"
tags: [AI Agent, OpenClaw, 資安, 企業AI, AI趨勢]
author: "黃敬峰（AI峰哥）"
---

> 本文是社群貼文的完整延伸版。
> 社群版講了核心現象，這裡加上獨家深度分析：AI Agent的資安框架、台灣企業的導入策略、以及阿峰老師的實戰觀察。

---

## 重點回顧

2026年3月，深圳騰訊總部外千人排隊安裝「龍蝦」AI工具OpenClaw。中國AI採用率58%（美國25%），5.15億生成式AI用戶，讓AI Agent的普及速度遠超預期。但技能市集ClawHub有335個惡意包（佔12%）、主要漏洞CVSS 8.8，促使中國政府下令國企全面禁裝。

---

## 【獨家】從「養龍蝦」看AI Agent的本質變革

「養龍蝦」這個詞，比大多數 AI 術語都更精準地描述了 AI Agent 的本質。

OpenClaw 的 logo 是紅色龍蝦，中國用戶把使用和訓練它的過程稱作「養龍蝦」。但仔細想想，「養」這個字非常關鍵——它帶出了三個重要的隱喻：

**第一，主動培育，不是被動使用。**
傳統 AI 工具（聊天機器人）是你主動問、它被動答。AI Agent 是你設定目標，它主動去完成。OpenClaw 可以自主執行終端指令、讀寫電腦檔案、瀏覽網頁、收發 email、管理行事曆——這不是聊天，是代理。

**第二，需要照顧和管理。**
養的東西你要負責。你要告訴它能去哪裡、不能去哪裡、可以碰什麼資料、不可以做什麼決定。這是 AI Agent 跟 ChatGPT 最大的差異：聊天機器人你不喜歡就關掉，AI Agent 在你不注意的時候還在跑。

**第三，邊界不清的後果很嚴重。**
養了不管的龍蝦，才是最危險的。這也正好是 ClawHub 惡意技能包事件的本質——用戶只看到「這個技能很好用」，沒有看到後台正在運行的是鍵盤記錄程式。

### 跟傳統 RPA 的差異

台灣企業可能對 RPA（機器人流程自動化）比較熟悉。AI Agent 跟 RPA 的差異在哪裡？

| 維度 | RPA | AI Agent |
|------|-----|---------|
| 執行邏輯 | 固定腳本、規則明確 | 動態推理、自行規劃步驟 |
| 例外處理 | 遇到例外就停下來報錯 | 嘗試找出替代方案 |
| 設定門檻 | 需要技術團隊建構流程 | 用自然語言描述任務即可 |
| 風險性質 | 流程錯誤（已知） | 行為不可預測（未知） |
| 典型工具 | UiPath、Automation Anywhere | OpenClaw、Claude Code |

AI Agent 的優勢在於彈性和自主性，但這兩個優勢也同時是它的風險來源。

---

## 【獨家】資安漏洞全解析：你需要了解的細節

非凡財經新聞的報導提到資安隱憂，但沒有深入細節。讓我把這件事說清楚。

### CVE-2026-25253：點一下就沉船的漏洞

這個漏洞的 CVSS 評分是 8.8——在資安評級中屬於「高危」（High），僅次於最高等級的「嚴重」（Critical，9.0+）。

具體的攻擊面包含：
- **一鍵遠端程式碼執行（RCE）**：攻擊者透過精心設計的請求，可以在你的電腦上執行任意程式碼
- **命令注入漏洞**：惡意指令可以被注入到 OpenClaw 的執行環境中
- **Prompt Injection 攻擊**：透過網頁內容或文件，欺騙 AI Agent 執行非預期的操作

這些漏洞的危險性在於：你不需要做任何「錯誤的事情」，只要 OpenClaw 瀏覽到一個惡意網頁，攻擊者就有機會入侵你的電腦。

### 技能市集的供應鏈攻擊

335 個惡意技能包、佔 ClawHub 整體 12% 的比例，這個數字讓我想到一個比喻：如果你去超市買東西，12% 的商品是假貨，你還敢買嗎？

這種攻擊方式叫做「供應鏈攻擊」（Supply Chain Attack）——不是直接攻擊你，而是污染你信任的來源。

惡意技能包的設計非常精心：
- 文件寫得完整專業，看起來跟正常技能沒有差別
- 功能本身可能真的有用，但同時在後台執行惡意操作
- 安裝的惡意軟體包含 keylogger（記錄你所有的鍵盤輸入）和 Atomic Stealer（竊取密碼和加密貨幣錢包）

台灣企業最常問我的問題是「我們公司 IT 有防火牆，應該沒問題吧？」答案是：防火牆擋不住你自己裝的東西。

### 135,000 個公開暴露的實例

全球有超過 135,000 個 OpenClaw 實例暴露在公開網路上，其中超過 15,000 個直接存在遠端程式碼執行漏洞。這代表攻擊者可以在不需要任何社交工程的情況下，直接掃描網路並入侵未設定好的 OpenClaw 實例。

---

## 【獨家】台灣企業的 AI Agent 導入框架

面對這波 AI Agent 浪潮，我給台灣企業的建議不是「先等等看」，而是「用正確的框架進場」。

在我帶過的 400+ 家企業培訓中，凡是成功導入 AI 工具的組織，都有一個共同特點：他們在工具選型之前，先想清楚了邊界。

### 三層邊界框架

**第一層：任務邊界**

哪些任務適合交給 AI Agent 自主執行？判斷標準：
- 流程步驟清楚、規則明確（✅ 適合）
- 需要人類判斷、有主觀成分（❌ 不適合）
- 錯誤可以輕易發現和修正（✅ 適合）
- 錯誤代價高、難以回復（❌ 不適合）

例如：整理會議記錄的格式（✅）、審核合約條款（❌）。

**第二層：資料存取邊界**

AI Agent 能接觸到哪些資料和系統？建議的設定原則：
- 最小權限原則：只給它完成任務所需的最小存取範圍
- 敏感資料隔離：財務、人事、客戶個資不開放 AI Agent 直接讀取
- 操作日誌：所有 AI Agent 的操作都要有記錄，方便事後稽核

**第三層：工具選型邊界**

開源版 vs 企業版的選擇標準：

| 情境 | 建議選擇 |
|------|---------|
| 個人實驗、學習用途 | 開源版（接受風險） |
| 小型團隊、非敏感任務 | 開源版 + 嚴格設定 |
| 中大型企業、有敏感資料 | 企業版（騰訊WorkBuddy等） |
| 政府、金融、醫療 | 企業版 + 私有部署 |

### 企業版 AI Agent 的現況

各大廠商已在搶這個市場：
- **騰訊 WorkBuddy**：企業版 OpenClaw，內建資安控管
- **ByteDance ArkClaw**：雲端即用型，降低自架風險
- **Zhipu AutoClaw**：中文優先的企業 AI Agent 平台

台灣市場目前還沒有本土的企業級 AI Agent 平台，但 Microsoft Copilot Studio 和 Salesforce AgentForce 已在提供類似的企業版服務，值得關注。

---

## 阿峰觀點

這件事讓我想到一個問題：為什麼 AI Agent 在中國的普及速度這麼快？

不是因為中國人特別敢冒險。是因為他們面對的工作壓力，讓「任何能幫我做事的工具」都值得冒險嘗試。

台灣職場文化相對保守，這在某種程度上減慢了 AI 採用速度，但也讓我們有機會「看清楚再進場」。中國的案例是一個非常珍貴的活教材——它讓我們知道 AI Agent 能做到什麼、市場的接受度有多高，也讓我們提早看到資安風險的真實形態。

「問題不在你，問題在工具」——這是我常說的一句話。

但這句話的完整版是：問題不在你，問題在你選的工具和你設定的邊界。工具再強，邊界沒設好，風險就是你的。

AI 時代，動手做的人才有未來。但動手之前，先把框架想清楚。

---

## 本文提到的資源

| 資源 | 連結 | 說明 |
|------|------|------|
| OpenClaw 官方文件 | openagenthq.io | 開源 AI Agent 平台 |
| CVE-2026-25253 | nvd.nist.gov | 漏洞資料庫記錄 |
| 企業 AI 培訓 | autolab.cloud | 阿峰老師企業培訓服務 |

---

如果你的公司想導入 AI Agent，又想避開這些資安陷阱，歡迎到官網聯繫我。
服務過超過 400 家企業，我們可以一起找到適合你組織的框架。

→ [https://www.autolab.cloud](https://www.autolab.cloud)

---

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

---

### 關於作者
黃敬峰（AI峰哥），企業 AI 實戰培訓專家，服務超過 400 家企業、10,000+ 學員。
核心心法：「會用、懂用、好用、每天用」
官網：https://www.autolab.cloud

---

**SEO:**
- Meta Title：AI龍蝦OpenClaw暴紅真相：千人排隊裝AI，12%技能惡意你知道嗎？
- Meta Description：中國千人排隊裝AI Agent「龍蝦」OpenClaw，但技能市集12%是惡意包，主要漏洞CVSS 8.8。台灣企業如何看待AI Agent浪潮？阿峰老師完整解析。
- Tags: AI Agent, OpenClaw, 資安, 企業AI導入, AI趨勢2026
- Target Keywords: OpenClaw AI Agent, AI龍蝦, AI Agent資安, 企業AI Agent導入, ClawHub惡意技能
