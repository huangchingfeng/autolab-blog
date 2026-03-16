---
title: "Claude Code /btw 指令完整解析：問一下就好，不消耗 context window"
slug: claude-code-btw-feature
date: "2026-03-16"
description: "Claude Code 2.1.72 新推出 /btw 旁問功能，讓你在工作流中插問一個問題，不進入對話歷史、不消耗 context window，可減少約 50% token 消耗。本文完整說明使用方式、限制與場景。"
tags: [Claude Code, AI工具, 開發工具, token優化]
author: "黃敬峰（AI峰哥）"
---

> 本文是社群貼文的完整延伸版。
> 社群版講了核心概念，這裡加上完整使用指南、場景分析與阿峰老師的實戰觀點。

---

## 重點回顧

Claude Code 2.1.72 在 2026 年 3 月 10 日推出 `/btw` 指令（By The Way）。這個指令讓你在進行中的工作任務旁邊「順便問一個問題」——答案顯示在浮層視窗，不進入對話歷史，不消耗 context window，關掉就消失。

持續使用 `/btw` 可以減少約 50% 的 token 消耗，是目前 Claude Code 裡最直接的省錢手段之一。

---

## 【獨家】/btw 的技術設計：為什麼能做到不消耗 context？

![Abstract digital art featuring futuristic geometric patterns with vibrant neon lighting.](images/btw-technology-design-context.jpg)
*Photo by [Pachon in Motion](https://www.pexels.com/@pachon-in-motion-426015731) on [Pexels](https://www.pexels.com/photo/a-computer-generated-image-of-a-futuristic-room-18419508/)*


### 一般問問題會發生什麼？

當你在 Claude Code 的對話框裡直接輸入一個問題，這條訊息會被加進「對話歷史」（conversation history），Claude 在處理每一個後續請求時，都需要把整段歷史記憶載入進來。

這代表什麼？

**你問的問題愈多，context 愈長，每次請求的 token 就愈多，費用就愈高。** 就算是一個「那個函式叫什麼名字」這種五秒鐘能解決的問題，問完之後它就永遠留在你的 context 裡了。

### /btw 的設計邏輯

`/btw` 採用「側鏈」（side-chain context）設計。

它創建一個完全獨立的臨時 context，跟主要工作任務的對話歷史完全隔離。Claude 看得到你的主任務 context（所以它能回答跟目前工作相關的問題），但它的回答不會回寫進主任務的歷史記錄。

你關掉浮層視窗，這個側鏈就消失了。什麼都沒留下。

### 另一個關鍵限制：沒有工具呼叫權限

`/btw` 的請求沒有工具呼叫（tool call）權限。這是故意的設計，也是它能做到低 token 消耗的另一個原因。

沒有工具呼叫權限意味著：
- 不能執行程式碼
- 不能讀取或編輯檔案
- 不能呼叫外部 API
- 只能回答基於現有知識和 context 的問題

這個限制讓 `/btw` 的每次請求都是輕量的——沒有工具呼叫的 overhead，純粹是知識查詢。

---

## 【獨家】什麼時候該用 /btw，什麼時候不該用？

![A soothing abstract blurred gradient background with warm tones.](images/btw.jpg)
*Photo by [Juan Pablo Serrano](https://www.pexels.com/@juanpphotoandvideo) on [Pexels](https://www.pexels.com/photo/blurry-image-of-a-brownish-background-1242348/)*


這是實際使用時最需要判斷的地方。

### 適合用 /btw 的場景

**查詢型問題（最適合）**

這是 `/btw` 的甜蜜點。你正在做一件事，需要查一個資訊，查完繼續做：

- `/btw` Python 的 `datetime.strptime` 格式字串怎麼寫？
- `/btw` 我們剛才討論的那個 API endpoint 路徑是什麼？
- `/btw` ES2022 有沒有 `at()` 方法？
- `/btw` PostgreSQL 的 `JSONB` 跟 `JSON` 差在哪？

這類問題有幾個共同特點：一句話能說清楚、答案是固定知識或 context 裡已有的資訊、問完不需要 Claude 採取任何行動。

**確認型問題**

你在實作某個功能，想再確認一下某個細節：

- `/btw` 這個函式我之前是不是說過要用 async？
- `/btw` 我們的 API key 是放在 `.env` 還是 `config.json`？

### 不適合用 /btw 的場景

**影響任務方向的決策型問題**

如果你的問題的答案會改變接下來的工作方向，就不適合用 `/btw`：

- ❌ `/btw` 你覺得這個架構設計有沒有問題？

  這種問題你需要 Claude 的答案留在 context 裡，讓它影響後續的實作決策。

**複雜的多輪除錯**

- ❌ `/btw` 這個 bug 怎麼追？

  這種問題需要 Claude 看完錯誤訊息、提問、看你的回覆、再提問，整個過程都需要保存在對話歷史。

**你希望 Claude 日後還能引用的重要資訊**

- ❌ `/btw` 我們的目標用戶是誰？

  如果你希望 Claude 在接下來的工作中都記得這個資訊，就把它說進主要對話裡，不要用 `/btw`。

---

## 【獨家】Token 省了 50%——實際意味著什麼？

![Image of Bitcoin tokens on a Weekly LocalBitcoins volume report paper.](images/token-50.jpg)
*Photo by [RDNE Stock project](https://www.pexels.com/@rdne) on [Pexels](https://www.pexels.com/photo/silver-and-golden-bitcoin-tokens-scattered-over-a-finance-report-8370771/)*


「省 50% token 消耗」聽起來是個行銷說詞，但背後有實際的使用邏輯。

這個數字的前提是：**在需要頻繁問小問題的工作任務中**。

如果你今天在用 Claude Code 做一個複雜的 refactor，過程中可能問了 20 個問題。如果其中 10 個是「查一個語法」「確認一個函式名」這類純查詢問題，以前你會把這 10 個問題全問進主對話，造成 context 快速膨脹。

現在這 10 個問題全用 `/btw`，主對話 context 只剩 10 個真正影響任務的訊息。context 短了一半，每次請求的 token 自然省了大約一半。

對於重度使用 Claude Code 的開發者來說，這不只是費用問題，還有一個更重要的影響：**context 太長時，Claude 的回應品質會下降**。較短的 context 讓 Claude 更能專注在當前任務的關鍵資訊，而不是在一大堆舊訊息裡撈重點。

---

## 阿峰觀點

帶過超過 400 家企業做 AI 培訓，我發現一個很普遍的行為模式，在工程師族群裡特別明顯：

他們不敢問「小問題」。

不是不需要知道，而是覺得「這種事應該自己查，不值得問 AI」「每問一次又多一點 context，有點浪費」。

結果就是，他們花了更多時間自己查，反而比直接問 AI 慢。而且查到了，還得把答案套回工作情境——這個整合步驟本來可以讓 Claude 幫你做。

這不是他們的問題，這是工具的設計帶給他們的心理負擔。

`/btw` 的意義不只是省錢，而是讓工程師有心理安全感去問那些「以前覺得不值得問」的問題。

問題不在你，問題在工具。

工具現在修好了，你就該放手問。

---

## 如何開始使用

升級到 Claude Code 2.1.72 或以上版本，直接使用：

```
/btw [你的問題]
```

不需要任何設定，升級即用。

---

## 本文提到的資源

| 工具 | 說明 |
|------|------|
| Claude Code | Anthropic 的 AI 程式碼開發工具 |
| /btw 指令 | Claude Code 2.1.72 新功能，旁問不消耗 context |

---

如果你的公司也想讓工程師團隊更有效率地使用 AI 工具，歡迎到官網聯繫我。
阿峰老師 → https://www.autolab.cloud

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

### 關於作者
黃敬峰（AI峰哥），企業 AI 實戰培訓專家，400+ 企業合作、10,000+ 學員。
核心心法：「會用、懂用、好用、每天用」
官網：https://www.autolab.cloud
