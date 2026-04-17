---
title: "Claude Opus 4.7 + 1M Context 實戰｜阿峰老師的 Session 管理升級指南"
slug: claude-opus-4-7-session-management
date: "2026-04-17"
description: "Anthropic 發布 Opus 4.7 + Claude Code 工程師親口教 1M Context Session 管理。每天用 Claude Code 跑企業培訓的阿峰老師，整理升級後立刻要做的 5 件事——含 100+ Skills 用戶的實戰經驗。"
tags: [Claude Opus 4.7, Claude Code, Session管理, AI工具, 阿峰老師]
keywords: [Claude Opus 4.7, Claude Code, 1M Context, Session 管理, Context Rot, AI 培訓]
author: "黃敬峰（AI峰哥）"
---

4 月 16 日 Anthropic 發了 Opus 4.7，同一個禮拜，Anthropic 工程師 Thariq 發了一篇推文，講 Claude Code 在 1M context 下該怎麼管理 session。

兩件事看起來分開，其實是同一件事的兩個面向。

過去一年，我每天用 Claude Code 跑企業培訓的所有後勤工作——課程設計、客戶提案、簡報製作、影片產線、部落格發文。我的 CLAUDE.md 寫了上千行、Skills 累積到 100 多個、開一個對話起手就吃掉 30-50k token。

這篇我把 Opus 4.7 升級重點 + Thariq 的 Session 管理心法，再加上我自己用 Claude Code 跑企業 AI 顧問業務的實戰經驗，整理成「升級後該做的 5 件事」。

如果你也在每天用 Claude Code 工作（不只是寫程式），這篇就是寫給你的。

## Opus 4.7 升級重點：三句話講完

**第一句：程式能力大躍進。**

SWE-bench Pro 從 53.4% 跳到 64.3%。意思是過去要工程師緊盯的程式工作，現在可以放手交給 AI 跑。

**第二句：多了一檔 xhigh 思考模式。**

原本只有低、中、高、最大四檔，現在中間多了一檔「extra high」。Claude Code 預設直接拉到這檔，等於你不用手動切，就能拿到 Anthropic 認為最划算的品質。

**第三句：視覺辨識升 3 倍。**

能處理的圖片解析度從 1568 像素拉到 2576 像素，token 上限從 1600 拉到 4784。處理截圖、簡報、技術圖表會明顯更準。

但有兩個壞消息要先講清楚：

- **Token 用量會增加 0~35%**：同一篇文章，可能從吃 1000 token 變成 1350 token。月費會上升。
- **指令遵循變嚴格**：以前 Opus 4.6 會自動腦補、寬鬆詮釋你的模糊指令，4.7 直接照字面執行。意思是你過去寫的 prompt 可能會出現預期外的結果，要重新檢查。

## Claude Code 1M Context 的五個分岔點

![Close-up of colorful coding text on a dark computer screen, representing software development.](images/claude-code-1m-context.jpg)
*Photo by [Markus Spiske](https://www.pexels.com/@markusspiske) on [Pexels](https://www.pexels.com/photo/coding-script-965345/)*


Anthropic 工程師 Thariq 在推文裡點出一個重要觀念：每次 Claude 跑完一個任務、你正準備輸入下一個訊息，都是一個分岔點。你有五個選項：

| 動作 | 適用情境 |
|------|---------|
| **Continue** 繼續對話 | 同一個任務的延伸 |
| **Rewind**（esc esc） | 上一個方向走錯，回到某個訊息重新走 |
| **Clear** 開新 session | 切換到新任務 |
| **Compact** 壓縮上下文 | 接近 context 上限、要繼續同一任務 |
| **Subagent** 子代理 | 知道接下來會產生大量你不需要的中間輸出 |

最自然的反應是 Continue，但其他四個才是高手會用的。

### 為什麼 Rewind 比「再試一次」好

舉例：Claude 讀了 5 個檔案、試了某個方法、結果不對。

直覺反應：「不對，改用另一種方法」。
更好的做法：esc esc 回到讀檔之後那一輪，重新給指令：「不要用 A 方法，因為 foo module 沒開那個介面，直接走 B」。

差別在哪？前者把錯誤路徑的 token 全部留在 context 裡（污染 + 浪費）。後者把錯誤路徑砍掉，只留下你學到的結論。

### Compact 不是萬靈丹

Compact 是讓 Claude 自己摘要對話、用摘要取代歷史。它有三個風險：

- 你不知道 Claude 會留什麼、丟什麼
- 自動 compact 通常在 context 將滿時觸發，模型那時是「最不聰明」的狀態（因為 context rot）
- 如果你下個訊息切到別的任務，但 compact 摘要只留了本次任務的東西，新任務需要的資訊就沒了

Thariq 的建議：寧可主動 `/clear` + 自己寫一份 brief（「我們在改 auth middleware，限制是 X，重要檔案是 A 和 B」），也不要被動讓 Claude 幫你 compact。

### Context Rot 在 300-400k 開始

Anthropic 內部觀測：1M context 模型大約在 300-400k token 左右開始出現「context rot」——注意力被太多 token 稀釋、舊的不相關內容開始干擾當前任務，模型表現會下降。

這是個值得記住的數字。如果你的 session 已經跑到這個量，該考慮 clear 或 compact 了。

## 【獨家】100+ Skills 用戶的真實處境：我每天這樣用 Claude Code

![Close-up view of HTML and CSS code displayed on a computer screen, ideal for programming and technology themes.](images/100-skills-claude-code.jpg)
*Photo by [Bibek ghosh](https://www.pexels.com/@bibekghosh) on [Pexels](https://www.pexels.com/photo/data-on-a-computer-screen-14553720/)*


我講一下我自己的處境，因為這跟一般工程師不一樣。

我是企業培訓講師、不是工程師。我用 Claude Code 跑：

- **課程設計**：`/course-designer`、`/course-proposal`
- **客戶管理**：`/client-manager` 串 100+ 家企業客戶資料
- **內容產線**：`/yt-factory`、`/post-factory`、`/blog-factory`
- **教材製作**：`/course-pptx`、`/course-materials`
- **行政自動化**：`/email-writer`、`/gov-form-filler`、`/invoice-organizer`

我的 `~/.claude/CLAUDE.md` 寫了 8 大 GATE 規則 + 5 條 anti-slack 偵測，加上 100 多個 Skills 隨時待命。每開一個對話，光是把這些規則和 skills 載入 context，起手就吃 30-50k token。

這代表什麼？**升級到 Opus 4.7 之後，我每個對話的成本會明顯上升。**

但我不打算降級。原因有三個：

**1. xhigh 模式對我的長任務有幫助**

例如 `/yt-factory` 一條龍跑下去動輒 200k token，xhigh 多花的 token 換來的品質提升，划算。

**2. 指令遵循變嚴格反而對我有利**

我的 GATE 規則寫得越嚴格、Skills description 越精準，AI 越聽話。Opus 4.6 時代偶爾會「腦補」忽略我的規則，4.7 不會。

**3. 視覺升級對 `/course-materials` 是大幫助**

我經常要讀客戶傳來的截圖、政府表格掃描檔、簡報照片，4.7 的解析度提升會直接反映在辨識準確度上。

但我也立刻做了三件事，避免帳單失控：

- 把 `/system-maintenance` 設定成每次對話開始自動跑（背景檢查 CLAUDE.md 行數、Skills 數、Permission 規則數）
- 把長對話切到分支：每個獨立任務開新 session，不要在同一個對話裡跨任務
- 把重型任務（`/yt-factory`、`/course-pptx`）明確要求 spawn subagent

## 【獨家】升級後立刻要做的 5 件事

![Close-up of colorful coding text on a dark computer screen, representing software development.](images/5.jpg)
*Photo by [Markus Spiske](https://www.pexels.com/@markusspiske) on [Pexels](https://www.pexels.com/photo/coding-script-965345/)*


如果你跟我一樣每天重度用 Claude Code，這 5 件事建議今天就做：

### 1. 重新檢查你的 CLAUDE.md 規則

Opus 4.7 指令遵循變嚴格，意思是你以前寫得模糊、靠 AI 腦補的規則，現在會「照字面跑」。

重點檢查：

- 「不要做 X」是否寫清楚 X 的範圍？
- 「優先用 A」是否定義了什麼情況下用 A？
- 觸發條件（trigger）是否精準到不會誤觸？

我這次重看自己的 CLAUDE.md，把好幾條 GATE 規則加上 `not-triggered` 條件，避免被 AI 誤判要執行。

### 2. 把「再試一次」改成 esc esc rewind

這是我從 Thariq 推文學到、立刻改變的習慣。

以前 AI 跑錯了，我習慣繼續打字「不對，改用 X 方法」。現在我直接 esc esc 回到錯誤之前那一輪，重新給指令。

長遠來看，這個習慣每個月可能省下相當多的 token 成本（也就是錢）。

### 3. 切任務時用 /clear，不要用 /compact

特別是當你的對話已經很長、又要切到完全不同的任務時，不要圖方便用 compact，那會讓你進入下一個任務時帶著一份模糊的摘要包袱。

直接 `/clear` 開新對話，自己花 1 分鐘寫一份 brief：「我接下來要做 X，限制是 Y，相關檔案在 Z」。這份 brief 對 AI 來說，比 compact 出來的摘要更乾淨、更精準。

### 4. 重型任務明確要求 spawn subagent

不要等 Claude 自己決定要不要派子代理。如果你知道接下來的任務會：

- 讀很多檔案
- 跑很多次工具呼叫
- 產生大量你不需要再用的中間輸出

那就明確說：「派一個 subagent 去處理 X，只給我最後結論」。

我現在跑 `/yt-factory` 都會明確寫：「Phase 3 的雙語字幕翻譯派 subagent 處理，主對話只要結果」。

### 5. 監控你的 session token 用量

300-400k 是 context rot 的危險線。1M 的上限給你更多空間，但**「能裝得下」不等於「裝了還聰明」**。

養成一個習慣：每跑完一個大段落，問自己「這個對話接下來還需要多少？」。如果答案是「另一個獨立的事」，就 clear。

## 結語：引擎再好，不會開車一樣會撞牆

模型升級和工具更新一直在發生，但「怎麼用」才是長期決定產出品質的關鍵。

Opus 4.7 給了你更強的引擎，但 Session 管理才是你的駕駛技術。

我這篇想講的核心觀念：**AI 工具不是越強越好，是越會用越好**。

這也是我做企業 AI 培訓這幾年下來最深的體會：每一家企業導入 AI 失敗的原因，從來不是「工具不夠強」，而是「沒人教大家怎麼用」。

如果你的公司也在面對「買了 AI 工具但用不起來」的處境，歡迎跟我聊聊。

---

> **想用 AI 解決真問題？** 加入阿峰老師的 AI 實戰社群，一起從觀念到落地。
>
> - LINE 社群：https://reurl.cc/GGlLNx
> - 企業培訓諮詢：ai@autolab.cloud
> - 官網：https://www.autolab.cloud
