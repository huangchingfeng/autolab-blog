---
title: "Claude Code Agent Teams 完全指南：從 Sub-agent 到多 AI 協作的架構升級"
slug: claude-code-agent-teams-guide
date: 2026-03-17
category: AI工具教學
---

# Claude Code Agent Teams 完全指南：從 Sub-agent 到多 AI 協作的架構升級

> 本文是 YouTube 影片「Claude Code Agent Teams 實戰！一個人管多個 AI Agent 的終極教學」的延伸閱讀版。
> 影片講了核心觀念和故事背景，本文加上完整的部署步驟和深度架構分析。
> 影片版本：https://www.youtube.com/watch?v=kfefDSYE0Rg

---

## 影片重點回顧

Claude Code 的 Agent Teams 功能在 2026 年 2 月 5 日正式上線，但其實 [Anthropic](https://www.anthropic.com) 早在幾個月前就把它寫進了 Claude Code 的 binary 裡，只是用 guard function 鎖住，對外不開放。

2026 年 1 月 24 日，開發者 Mike Kelly 用 `strings` 指令把 binary 拆開，發現了內部代號「Swarms」的 TeammateTool，有 13 個完整操作，全寫好了。消息傳出，社群沸騰，兩週後 Anthropic 正式發布。

核心概念：一個 session 當 Team Lead，指揮多個 Teammate，每個 Teammate 有獨立 context window，**而且 Teammate 之間可以直接溝通**——這是跟 sub-agent 最大的差別。

啟用方式：Claude Code v2.1.32+，設定環境變數 `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`。

---

## 【獨家】Agent Teams vs Sub-agent：架構層面的本質差異

很多人以為 Agent Teams 只是「更多 sub-agent」，其實不對。

<!-- wp:html -->
<table style="width:100%;border-collapse:collapse;margin:1.5em 0;font-size:0.95em;">
<thead><tr style="background:#00D4FF;color:#0A1628;">
  <th style="padding:12px 16px;text-align:left;font-weight:700;">比較維度</th>
  <th style="padding:12px 16px;text-align:left;font-weight:700;">Sub-agent 模式</th>
  <th style="padding:12px 16px;text-align:left;font-weight:700;">Agent Teams</th>
</tr></thead>
<tbody>
<tr style="background:#f8f9fa;border-bottom:1px solid #e9ecef;">
  <td style="padding:10px 16px;font-weight:600;">溝通路徑</td>
  <td style="padding:10px 16px;">所有訊息必須經過主 Agent</td>
  <td style="padding:10px 16px;">Teammate 之間可直接溝通</td>
</tr>
<tr style="background:#ffffff;border-bottom:1px solid #e9ecef;">
  <td style="padding:10px 16px;font-weight:600;">Context Window</td>
  <td style="padding:10px 16px;">共用主 Agent 的 context</td>
  <td style="padding:10px 16px;">每個 Teammate 獨立 context</td>
</tr>
<tr style="background:#f8f9fa;border-bottom:1px solid #e9ecef;">
  <td style="padding:10px 16px;font-weight:600;">並行能力</td>
  <td style="padding:10px 16px;">偽並行（主 Agent 排程）</td>
  <td style="padding:10px 16px;">真並行（各自同時執行）</td>
</tr>
<tr style="background:#ffffff;border-bottom:1px solid #e9ecef;">
  <td style="padding:10px 16px;font-weight:600;">瓶頸所在</td>
  <td style="padding:10px 16px;">主 Agent 是流量瓶頸</td>
  <td style="padding:10px 16px;">Team Lead 只做策略決策</td>
</tr>
<tr style="background:#f8f9fa;border-bottom:1px solid #e9ecef;">
  <td style="padding:10px 16px;font-weight:600;">適合任務規模</td>
  <td style="padding:10px 16px;">中小型（單一線性流程）</td>
  <td style="padding:10px 16px;">大型（多任務並行，相互依賴）</td>
</tr>
<tr style="background:#ffffff;">
  <td style="padding:10px 16px;font-weight:600;">除錯難度</td>
  <td style="padding:10px 16px;">集中在主 Agent，容易追蹤</td>
  <td style="padding:10px 16px;">分散但透明（inbox 可直接查看）</td>
</tr>
</tbody></table>
<!-- /wp:html -->

**簡單說**：sub-agent 是「老闆一個人管所有業務」；Agent Teams 是「老闆只做策略，各部門主管直接協調」。

後者在任務規模擴大後效率差距是指數級的。

---

## 【獨家】Agent Teams 完整部署步驟

這是我查過官方文件後整理的實際操作步驟，比官方文件更有條理。

### 第一步：確認環境

```bash
# 確認 Claude Code 版本
claude --version
# 需要 v2.1.32 或更新

# 如果版本不夠，更新
npm update -g @anthropic-ai/claude-code
```

### 第二步：啟用 Agent Teams

在你的 `~/.claude/settings.json` 加上：

```json
{
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
  }
}
```

或者每次執行前設定環境變數：

```bash
export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1
claude
```

### 第三步：設定顯示模式

Agent Teams 支援三種顯示模式：

- **`auto`（預設）**：在 tmux session 裡自動開分割畫面，否則用 in-process 模式
- **`in-process`**：所有 Teammate 在同一個 terminal，用 Shift+Down 切換
- **`split`**：強制分割畫面（需要 tmux 或 iTerm2）

如果你用 tmux，直接進 tmux 再開 claude 就好。如果用 iTerm2，需要先啟用 Python API：

```
iTerm2 → Preferences → General → Magic → Enable Python API
```

### 第四步：啟動 Team Lead

直接開啟 claude，然後用以下方式說明你的任務：

```
我需要你組建一個 Agent Teams 來重構這個代碼庫：
- Frontend Teammate：負責 React 組件（src/components/）
- Backend Teammate：負責 API 路由（src/api/）
- Test Teammate：負責測試（src/__tests__/）

請分派任務後開始執行。
```

Claude Code 會自動：
1. 啟動對應數量的 Teammate session
2. 建立 `~/.claude/teams/[team-name]/` 目錄
3. 為每個 Teammate 建立 inbox 檔案
4. 分派任務並開始執行

### 第五步：監控執行狀態

在 tmux 分割畫面下，你能同時看到：
- Team Lead 的總體進度
- 各個 Teammate 的執行狀態
- Teammate 之間的 inbox 訊息

如果某個 Teammate 卡住了，直接在它的視窗下指令。如果想查看所有 Agent 在溝通什麼：

```bash
cat ~/.claude/teams/[team-name]/inbox/teammate-1.json
```

---

## 【獨家】什麼任務最適合用 Agent Teams？

不是所有任務都值得開 Agent Teams。根據官方文件和我的觀察，以下場景效益最明顯：

**✅ 高度適合：**
- **大型代碼庫重構**：前端 + 後端 + 測試可以完全並行
- **多服務同時開發**：微服務架構下各服務獨立開發
- **文件生成 + 審查**：一個 Agent 寫，另一個同步審查和改進
- **多語言翻譯**：同時處理多個語言版本

**⚠️ 注意事項：**
- **Token 成本是線性倍數**：3 個 Teammate = 至少 3 倍 token 消耗
- **目前不支援 session 恢復**：中斷後 in-process 模式的 Teammate 無法繼續
- **VS Code terminal 不支援分割畫面**：建議用外部 terminal

**❌ 不適合：**
- 簡單的單一任務（成本不划算）
- 嚴格線性依賴的工作流（A 必須等 B 完成才能開始）

---

## 阿峰觀點

我帶過超過 400 家企業做 AI 培訓，最近最常聽到工程師說：「我用 Claude 做小任務很快，但遇到大型專案還是很頭大。」

Agent Teams 加上 Claude Opus 4.6 的 [context compaction](https://docs.anthropic.com/en/docs/claude-code/memory)（自動壓縮舊對話，讓長時間 session 不斷線），這個組合直接解決了那個「大型專案很頭大」的問題。

但我想說一個更根本的東西：**這不只是工具的升級，是角色的升級。**

以前工程師的工作主要是「執行」——寫程式、改 bug、跑測試。現在開始出現一種新能力：**指揮 AI 團隊**——決定架構方向、分派任務、監控結果、做最後判斷。

會寫程式的工程師越來越多（AI 也會），但會指揮 AI 團隊的工程師還很少。

那個問我「一個人管五個 AI agent，是我在工作還是他們在工作」的工程師，我後來跟他說：你的工作性質已經在改變了，而且是往更有價值的方向改變。

問題不在你能不能寫程式。問題在你能不能做指揮官。

---

## 本文提到的資源

<!-- wp:html -->
<table style="width:100%;border-collapse:collapse;margin:1.5em 0;font-size:0.95em;">
<thead><tr style="background:#00D4FF;color:#0A1628;">
  <th style="padding:12px 16px;text-align:left;font-weight:700;">資源</th>
  <th style="padding:12px 16px;text-align:left;font-weight:700;">連結</th>
  <th style="padding:12px 16px;text-align:left;font-weight:700;">說明</th>
</tr></thead>
<tbody>
<tr style="background:#f8f9fa;border-bottom:1px solid #e9ecef;">
  <td style="padding:10px 16px;">Anthropic 官方文件</td>
  <td style="padding:10px 16px;"><a href="https://code.claude.com/docs/en/agent-teams" style="color:#00D4FF;">code.claude.com</a></td>
  <td style="padding:10px 16px;">Agent Teams 官方指南</td>
</tr>
<tr style="background:#ffffff;border-bottom:1px solid #e9ecef;">
  <td style="padding:10px 16px;">社群發現文章</td>
  <td style="padding:10px 16px;"><a href="https://paddo.dev/blog/claude-code-hidden-swarm/" style="color:#00D4FF;">paddo.dev</a></td>
  <td style="padding:10px 16px;">Mike Kelly 如何在 binary 裡挖出 Swarms</td>
</tr>
<tr style="background:#f8f9fa;">
  <td style="padding:10px 16px;">Claude Code 下載</td>
  <td style="padding:10px 16px;"><a href="https://code.claude.com" style="color:#00D4FF;">code.claude.com</a></td>
  <td style="padding:10px 16px;">官方 CLI，需要 API Key</td>
</tr>
</tbody></table>
<!-- /wp:html -->

---

<!-- wp:html -->
<div style="background:linear-gradient(135deg, #0A1628 0%, #1a2a4a 100%);padding:28px;border-radius:12px;margin:2em 0;border-left:4px solid #00D4FF;">
  <p style="font-weight:700;font-size:1.2em;margin:0 0 8px 0;color:#fff;">📬 訂閱阿峰老師的 AI 實戰電子報</p>
  <p style="color:#ccc;margin:0 0 16px 0;font-size:0.95em;">每週精選 AI 工具技巧、產業趨勢、實戰案例，直送你的信箱。</p>
  <form action="https://formsubmit.co/ai@autolab.cloud" method="POST" style="display:flex;gap:8px;flex-wrap:wrap;">
    <input type="hidden" name="_subject" value="新訂閱：AI 實戰電子報">
    <input type="hidden" name="_template" value="table">
    <input type="hidden" name="_next" value="https://blog.autolab.cloud/?subscribed=1">
    <input type="hidden" name="_captcha" value="false">
    <input type="email" name="email" placeholder="輸入你的 Email" required style="flex:1;min-width:200px;padding:12px 16px;border:2px solid #00D4FF;border-radius:6px;background:#fff;font-size:1em;outline:none;">
    <button type="submit" style="background:#00D4FF;color:#0A1628;padding:12px 24px;border:none;border-radius:6px;font-weight:700;font-size:1em;cursor:pointer;white-space:nowrap;">免費訂閱 →</button>
  </form>
</div>
<!-- /wp:html -->

如果你的公司想導入 AI，讓團隊真正用起來，歡迎到 **[autolab.cloud](https://www.autolab.cloud)** 聯繫阿峰老師。

---

<!-- wp:html -->
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
<!-- /wp:html -->

---

### 關於作者
黃敬峰（AI峰哥），企業 AI 實戰培訓專家，400+ 企業合作、10,000+ 學員。
核心心法：「會用、懂用、好用、每天用」
官網：https://www.autolab.cloud

SEO:
- Meta Title：Claude Code Agent Teams 完全指南：多 AI 協作架構升級
- Meta Description：Claude Code Agent Teams 讓一個 Team Lead 指揮多個 Teammate 並行執行，Teammate 之間可直接溝通。本文包含完整部署步驟、架構比較表、最適合場景分析。
- Tags：#ClaudeCode #AgentTeams #AI #工程師 #多代理
- Target Keywords：Claude Code Agent Teams, Claude Code 多 Agent, AI Agent 協作, Team Lead Teammate, Claude Code 教學
