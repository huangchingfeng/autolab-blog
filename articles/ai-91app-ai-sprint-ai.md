---
author: 黃敬峰（AI峰哥）
date: '2026-03-09'
description: 91APP 有 30+ 個開發團隊全面導入 AI，產品長分享職稱邊界消失、Sprint 估點數失去意義的實戰觀察。阿峰老師獨家分析自動化工具的典範翻轉和
  Agent UX 設計。
keywords:
- 企業AI導入
- 91APP AI
- Sprint AI
- Agent UX設計
- AI組織創新
slug: ai-91app-ai-sprint-ai
tags:
- AI
- 企業AI導入
- 91APP
- Sprint
- AgentUX
- 組織創新
title: AI 時代組織怎麼跑？91APP 三十幾個團隊的實戰經驗拆解｜阿峰老師
youtube_id: baZp2vDyuFI
---

# AI 時代組織怎麼跑？91APP 三十幾個團隊的實戰經驗完整拆解

> 本文是 YouTube 影片「91APP 產品長揭露：AI 讓職業邊界消失，Sprint 估點數也沒用了」的延伸閱讀版。
> 影片講了核心觀念，本文加上獨家分析和操作指南。
> 影片版本：https://www.youtube.com/watch?v=baZp2vDyuFI

---

## 影片重點回顧

91APP 有三十幾個開發團隊，全面導入 AI 三年。產品長 Happy 和前 iCHEF 共同創辦人 Spencer 分享了最前線的觀察：職稱邊界正在模糊化、Sprint 方法論被 AI 衝擊、Agent UX 不是聊天機器人，而是融入流程的隱形助手。更大膽的判斷是——未來軟體要服務 Agent，不再是服務人。

---

## 【獨家】自動化工具的典範翻轉：從 N8N 到 LLM-first

![Close-up view of a robotic arm equipped with a video camera, showcasing modern technology.](images/automation-tools-n8n-llm-first.jpg)
*Photo by [Pavel Danilyuk](https://www.pexels.com/@pavel-danilyuk) on [Pexels](https://www.pexels.com/photo/a-video-camera-on-a-stand-8438976/)*


影片中 Spencer 提到 N8N 的星星數在過去半年暴跌，這背後的邏輯值得深入分析。

過去三年，自動化工具經歷了三個階段：

**階段一：Rule-based 自動化（2020-2023）**
N8N、Zapier、Make 這類工具的核心邏輯是「你設定規則，軟體執行」。你得手動拉節點、設觸發條件、一個一個串接。語言模型只是其中一個步驟，被「封印」在有限的規則框架裡。

**階段二：LLM + Rule-based 混合（2023-2024）**
開始有人把 ChatGPT API 塞進 N8N 的節點裡，讓 AI 在某些步驟做判斷。但整體架構還是 Rule-based，AI 只是一個更聰明的「節點」。

**階段三：LLM-first 架構（2025-現在）**
Spencer 在影片中描述的方向：以語言模型為基礎，在上面疊控制。你用自然語言描述任務，AI 自動去技能組裡找工具、自動組合工作流。規則不再是框架，而是控制手段。

這個翻轉的核心洞察是：以前是「有限集合上放無限可能」（等於封印），現在是「無限可能上加有限控制」（等於釋放）。

我帶企業做 AI 培訓時，最常遇到的誤區就是第二階段的思維：把 AI 當工具塞進現有流程。但真正的突破在第三階段——讓 AI 重新定義流程本身。

---

## 【獨家】Sprint 方法論的 AI 衝擊：五個正在發生的改變

![A modern humanoid robot with digital face and luminescent screen, symbolizing innovation in technology.](images/sprint-method-ai.jpg)
*Photo by [Kindel Media](https://www.pexels.com/@kindelmedia) on [Pexels](https://www.pexels.com/photo/low-angle-shot-of-robot-8566526/)*


影片中 Happy 提到 Sprint 估點數失去意義，但他沒有展開的是，整個敏捷開發框架正在被根本性地挑戰。根據我服務超過四百家企業的觀察，以下五個改變正在發生：

**1. 估點數 → 估方向**
以前一個 Ticket 估 3 天，AI 出現後可能 1 天就完成。重點不再是「多久」，而是「做不做」和「做到什麼程度」。

**2. 角色固定 → 能力流動**
Happy 的觀察最精準：PO 可以寫程式、RD 可以做產品決策。Sprint 原本就有「任何人可以撿別人的工作」的原則，以前做不到，現在 AI 讓它成真了。

**3. Sprint Review → 持續驗證**
以前要等一個 Sprint 結束才 Review，現在 Vibe Coding 可以在幾小時內做出 Prototype，直接拿給客戶看。驗證週期從兩週變成一天。

**4. Backlog 管理 → 機會爆炸**
Happy 說「題目收不完」——員工瘋狂提案，用 AI 快速做出 POC 證明可行性。以前的問題是「資源不夠」，現在的問題是「機會太多，怎麼選」。

**5. 團隊規模 → 重新定義**
如果一個人加 AI 可以做以前三個人的工作，團隊還需要 7-15 人嗎？91APP 目前沒有裁員，而是讓團隊做更多事。但長期來看，最佳團隊規模一定會改變。

---

## 阿峰觀點

![A modern humanoid robot with digital face and luminescent screen, symbolizing innovation in technology.](images/artificial-intelligence-business.jpg)
*Photo by [Kindel Media](https://www.pexels.com/@kindelmedia) on [Pexels](https://www.pexels.com/photo/low-angle-shot-of-robot-8566526/)*


聽完 Happy 和 Spencer 的分享，我最大的感觸是：台灣其實有很多企業已經走在 AI 導入的最前線，只是大家不太講。

91APP 的做法有幾個值得學的地方：

第一，**從上到下全力支持**。不是喊口號，是直接發錢訂閱 AI 工具。每人每月二十塊美金，看起來不多，但代表的是「你去用，公司買單」的態度。

第二，**不急著收斂**。三十幾個團隊各自探索不同的 AI 工作方式，讓大家互相分享。這需要管理層的耐心和信任。

第三，**務實面對失敗**。對話式 Agent 客戶不買單？那就換方向，做融入流程的隱形 AI。不是「AI 不行」，是「這個用法不對」。

你是機長，AI 是機組人員。不要被職稱限住你的可能性。

---

## 本文提到的資源

| 工具 | 連結 | 說明 |
|------|------|------|
| 91APP | https://www.91app.com | 台灣零售科技 SaaS 平台 |
| 塞掐 Side Chat | https://www.youtube.com/watch?v=8QSNNvM7yEU | 原始訪談完整版 |

---

## 影片中提到的資源

- Cursor — AI 程式編輯器
- Claude Code — Anthropic 的 CLI 開發工具
- N8N — 開源自動化工具
- Open Claw（龍蝦）— 開源 AI Agent 平台
- Lublia — Spencer 的開源 AI 工作流工具

---

📌 企業 AI 培訓服務
→ https://www.autolab.cloud

---

### 關於作者
黃敬峰（AI峰哥），企業 AI 實戰培訓專家，400+ 企業合作、10,000+ 學員。
核心心法：「會用、懂用、好用、每天用」
官網：https://www.autolab.cloud