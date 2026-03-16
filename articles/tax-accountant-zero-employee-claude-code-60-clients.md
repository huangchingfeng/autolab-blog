---
title: "員工 0 人的稅務師，靠 Claude Code 一人服務 60 家公司：不是工程師，也能做到的 AI 自動化框架"
slug: "tax-accountant-zero-employee-claude-code-60-clients"
date: "2026-03-16"
description: "日本稅務師畠山謙人如何用 Claude Code 以 0 名員工服務 60 家客戶，每年省下 600 萬台幣人事費？完整拆解他的系統設計、CLAUDE.md 業務手冊、兩階段判斷機制，以及非工程師如何複製這套框架。"
tags: [Claude Code, AI自動化, 一人公司, 稅務, 非工程師]
author: "黃敬峰（AI峰哥）"
---

> 本文是社群貼文的完整延伸版。
> 社群版講了核心觀念，本文加上獨家深度分析和可操作框架。

---

## 重點回顧

日本稅務師畠山謙人，以 0 名員工服務 60 家顧問客戶，每年省下相當於 600 萬台幣的人事費。他的核心工具是 Claude Code。他不是工程師，程式碼全部讓 Claude 寫。關鍵在於：他把十幾年累積的稅務判斷力，翻成了 AI 能執行的語言。

---

## 【獨家】這件事為什麼值得台灣企業認真看？

我在企業培訓現場最常被老闆問的問題，大概可以分成兩類：

第一類：「AI 可以幫我做什麼？」
第二類：「我要給它什麼，它才能幫我做？」

大多數老闆問的是第一類。懂的人問的是第二類。

畠山謙人的案例，完整示範了第二類思維長什麼樣。

稅務師行業的業界標準，是每 10 家客戶配 1 名工作人員。60 家公司，照這個算法要養 6 個人。光人事成本，每年超過 3,000 萬日圓，換算台幣大概 600 萬。

他現在的人事費是零。

這不是因為他找到了什麼神奇的 AI 工具。是因為他做了一件很多企業沒有做的事：**把工作的規則說清楚，然後交給 AI 執行。**

台灣企業導入 AI 失敗的最大原因，我觀察下來幾乎都是同一個：把「工具導入」跟「工作流程重設計」搞混了。買了工具、裝了系統，但沒有人說清楚「這件工作的規則是什麼」。AI 不知道邊界在哪裡，要嘛跑錯，要嘛根本跑不起來。

畠山的案例提供了一個清晰的答案：**你需要先是個好的業務設計者，才能成為好的 AI 使用者。**

---

## 【獨家】他的完整系統拆解

### 指揮塔架構

他用 Claude Code 作為整個事務所的「指揮塔」，串連了以下系統：

- **freee**（雲端會計軟體）：交易資料的主要輸入端
- **Gmail MCP**：批量草擬提醒郵件，一次搞定沒交月報的客戶
- **Google 日曆 MCP**：列出會議清單、自動產生準備工作
- **Notion MCP**：讀取會議記錄 → 生成下次議程、管理待辦
- **Slack MCP**：TODO 與 bot 管理

這幾個工具串在一起的效果是：**稅務師八成的日常工作（他稱之為「轉記」——把 A 的資料移到 B），幾乎歸零。**

### 核心自動化：每晚 21 點的記帳流程

這是整個系統最核心的部分。

每晚 21 點，系統自動開始處理 60 家公司的分錄。整個流程 30-50 分鐘跑完。原本要 5 小時的工作，縮短到不到 1 小時，而且他不需要人坐在電腦旁邊。早上起來，前一天的帳已經全部處理好了。

130 張發票的處理，手工輸入要一整天。現在 15 分鐘轉成可匯入格式。

每個月省 24 小時，一年省 300 小時。這是他實際記錄下來的數字，不是估計。

### 兩階段科目判定（成本控制的關鍵）

這個設計很聰明，值得單獨拆解。

**第一階段：關鍵字辭典比對**
自己建的關鍵字辭典，14 個科目類別 × 超過 100 個關鍵字。遇到能比對到的交易，直接自動歸類——快、準確率高、不花 API 成本。

**第二階段：Claude API 備援**
只有關鍵字比對失敗的交易，才進入 Claude API 處理。同時設定信賴度門檻——低於門檻的，不自動分類，標記為待人工複核。

這個設計的核心邏輯是：**AI 是替補，不是主角。** 讓規則先跑，規則跑不過的才請 AI 出場。成本控制好，品質也不因為省錢就妥協。

很多台灣企業導入 AI 的思維是「把所有事情都丟給 AI 判斷」，結果要嘛成本爆表，要嘛出錯率高到不敢用。畠山的兩階段設計給了一個更務實的參考框架。

### 排除規則設計（最容易被忽略的部分）

他設計了 7 種排除規則，明確指定哪些交易類型**不進自動化流程**：

- 借款償還
- 社會保險
- 薪資
- 投資相關
- 其他高風險科目

這些全部要人工複核。

為什麼這很重要？因為這些科目一旦分錯，後果非常嚴重——稅務申報錯誤、財報失真、法律風險。

他說的話我覺得非常值得所有企業主聽進去：

**「重要的是知道應該自動化什麼。能做出這個判斷的，只有每天在現場親手操作的你。」**

這不是謙虛，這是事實。AI 不知道你的工作邊界在哪裡，只有你知道。

---

## 【獨家】CLAUDE.md：把業務規則翻成 AI 的語言

這是我覺得畠山案例中，最值得台灣企業借鑑的部分。

CLAUDE.md 是一個設定檔，讓 Claude Code 知道「這個專案的規矩是什麼」。工程師通常用來寫開發規範，但他用來寫的是整間事務所的業務規則。

他寫進去的內容包括：

**分錄分類規則**
- 餐飲費 1 萬日圓以下 → 會議費
- 餐飲費 1 萬日圓以上 → 交際費
- 海外 SaaS 訂閱費 → 通訊費

**安全政策**
- API 金鑰絕對不輸出
- 個人編號絕對不輸出
- 60 家公司資料以 company_id 完全分離，A 公司和 B 公司的資料在設計上不可能混入

**判斷邊界**
- 符合過去模式的交易 → AI 可自動處理
- 新出現的交易模式 → 先標記、不亂分類、等人工確認

這等於是把一個資深員工腦袋裡的 SOP，翻成 AI 讀得懂、能執行的格式。

他說：「跟人不同，AI 不會因為重複教同一件事不耐煩，也不會忘記。」

這點非常關鍵。你把規則教 AI 一次，它就會用那個規則幫你跑到天荒地老。人會忘、會累、會搞混，AI 不會。

### 如何開始寫你的 CLAUDE.md？

如果你想把這個概念用在自己的工作上，以下是一個起始框架：

**Step 1：列出你工作中「最重複、最有規律」的 10 件事**
這些通常是最適合自動化的候選項目。

**Step 2：對每一件事，寫下「判斷規則」**
格式很簡單：「如果 [條件]，就 [做什麼]」。例如：「如果客戶回覆的 email 包含『確認』，就更新 CRM 狀態為已確認。」

**Step 3：列出「排除清單」**
哪些事情絕對不能自動化？金錢相關、客戶關係敏感、法律合規要求的——全部列進去。

**Step 4：把 Step 2 和 Step 3 的內容，整理成一份文件**
告訴 Claude Code：「這是我的工作規則，請照這個跑。」

這就是你的 CLAUDE.md 的原型。

---

## 【獨家】為什麼懂業務的人用 AI 效果反而更好？

這個問題很多人覺得反直覺，但背後有清楚的邏輯。

工程師用 AI，做出的是技術上很厲害的東西——效能好、架構漂亮、可擴充性強。

稅務師用 AI，做出的是實務上正確的東西——分類準確、符合法規、不需要回頭重改。

**後者其實更難，因為它需要的是花了十幾年才累積起來的行業判斷力。**

Claude Code 可以把任何人說的需求翻成程式碼，但它沒有辦法自己知道「這個情境應該怎麼判」。知道這件事的人，是每天在現場做這份工作的你。

這就是為什麼畠山說：「正因為不是工程師，Claude Code 才能發揮作用。」——他不是在謙虛，他是在說一個事實。他的行業 know-how 是 AI 系統能正確運作的基礎。

我在台灣帶企業 AI 培訓的時候，觀察到同樣的現象：**能把自己的工作拆解清楚的人，AI 工具在他們手上的效果就是比其他人好。** 這不是技術問題，是業務理解的問題。

---

## 阿峰觀點

看完畠山的案例，我腦子裡一直在想一件事：

台灣有多少人，現在手上的工作，其實已經可以用這套方式大幅自動化了——只是還沒有人幫他們說清楚「怎麼開始」？

我帶過超過 400 家企業的 AI 培訓，每次看到這類案例都更確定一件事：

AI 工具的門檻已經低到不需要工程師背景了。現在的門檻是：你能不能說清楚你的工作規則？

「AI 沒變聰明，是環境變好了。」現在的工具，讓不寫程式的人也能把自己的行業知識翻成系統能執行的語言。

畠山的系統，我覺得最值得複製的核心不是技術，而是態度：**他花了時間把工作想清楚，然後才去找工具。**

這個順序對了，工具才有用。順序搞反，再好的工具也跑不起來。

---

## 本文提到的資源

<!-- wp:html -->
<table style="width:100%;border-collapse:collapse;margin:1.5em 0;">
<thead>
<tr style="background:#00D4FF;color:#fff;">
<th style="padding:10px 16px;text-align:left;font-weight:bold;">工具</th>
<th style="padding:10px 16px;text-align:left;">說明</th>
</tr>
</thead>
<tbody>
<tr style="background:#f8f9fa;">
<td style="padding:10px 16px;font-weight:bold;border:1px solid #e0e0e0;">Claude Code</td>
<td style="padding:10px 16px;border:1px solid #e0e0e0;">Anthropic 開發的 AI 編程助手，可透過對話指揮自動化工作流程</td>
</tr>
<tr>
<td style="padding:10px 16px;font-weight:bold;border:1px solid #e0e0e0;">freee（フリー）</td>
<td style="padding:10px 16px;border:1px solid #e0e0e0;">日本主流雲端會計軟體，提供 MCP 接口</td>
</tr>
<tr style="background:#f8f9fa;">
<td style="padding:10px 16px;font-weight:bold;border:1px solid #e0e0e0;">CLAUDE.md</td>
<td style="padding:10px 16px;border:1px solid #e0e0e0;">Claude Code 的專案設定檔，用來定義業務規則、安全政策、判斷邊界</td>
</tr>
<tr>
<td style="padding:10px 16px;font-weight:bold;border:1px solid #e0e0e0;">MCP（Model Context Protocol）</td>
<td style="padding:10px 16px;border:1px solid #e0e0e0;">讓 AI 與外部系統（Gmail、日曆、Notion 等）直接串接的通訊協議</td>
</tr>
</tbody>
</table>
<!-- /wp:html -->

---

如果你的公司也想走這條路，我的企業 AI 培訓服務可以幫助你的團隊從「聽過 AI」變成「每天用 AI」。

👉 企業培訓洽詢：https://www.autolab.cloud

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

📎 資料來源：畠山謙人（@kandmybike）— X 長文，AI 稅理士事務所一人管 60 家公司實錄（2026-03）
