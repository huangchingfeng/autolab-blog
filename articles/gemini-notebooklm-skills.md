---
title: 萬卷之王：把 Gemini Gem 技能外掛到 NotebookLM 的終極玩法
slug: gemini-notebooklm-skills
date: "2026-03-09"
description: 教你把所有 Gemini Gem 的技能裝進 NotebookLM，一個筆記本搞定多步驟工作流。四步驟完整教學。
tags:
  - NotebookLM
  - Gemini
  - AI工具教學
  - Google AI
---

# 萬卷之王：把 Gemini Gem 技能外掛到 NotebookLM 的終極玩法

> 本文是社群貼文的完整延伸版。
> 社群版講了核心概念，本文加上獨家操作指南和進階技巧。

---

## 重點回顧

Gemini 的 Gem（自訂機器人）很好用，但有個致命缺點：左邊欄位只能釘選 5 個。如果你做了十幾個 Gem，每次找就要翻半天。而且做多步驟工作流的時候，要在不同 Gem 之間切換複製貼上，超級麻煩。

「萬卷之王」就是一個解決方案：把所有 Gem 的技能「外掛」到 NotebookLM，一個筆記本裝好幾個技能，用勾選切換，還能搭配你的資料一起運作。

---

## 【獨家】完整操作指南：四步驟把技能裝進 NotebookLM

![A minimalist workspace featuring a laptop, smartphone, and an apple on a clean white desk.](images/notebooklm.jpg)
*Photo by [karsten madsen](https://www.pexels.com/@morningtrain) on [Pexels](https://www.pexels.com/photo/macbook-pro-near-iphone-and-apple-fruit-18105/)*


### 步驟一：製作「生成技能的 Gem」

在 Gemini 左邊選單找到「Gem」，新增一個叫「對話機器人指令架構師」的 Gem。這個 Gem 的功能是：你告訴它你想要什麼機器人，它就幫你寫好完整的行為指示（提示詞）。

**使用方式**：
1. 打開 Gemini → 左邊選單 → Gem → 新增 Gem
2. 在「使用說明」貼上指令架構師的系統提示
3. 儲存

之後你只要對它說「幫我寫一個能生成一頁式漫畫的機器人」，它就會幫你產出完整的行為指示，包含版本號、角色設定、輸出格式等等。

### 步驟二：製作「生圖專用 Gem」

因為 NotebookLM 本身不能生成圖片，所以我們需要一個專門負責生圖的 Gem。這個 Gem 很簡單——你貼提示詞給它，它就直接生圖，不囉嗦。

**重點**：以後所有要生圖的需求，都統一透過這一個 Gem 處理。NotebookLM 負責產出圖片提示詞，生圖 Gem 負責執行。各司其職。

### 步驟三：設定 NotebookLM 自訂提示詞

這是最關鍵的一步。在 NotebookLM 右上角找到「設定筆記本」→「自訂提示詞」，貼上一段叫「動態指令解析與執行專家」的系統提示。

**這段提示做了什麼**：
- 自動偵測來源資料裡的行為指令（角色設定、操作指令、SOP）
- 將偵測到的指令內化為筆記本的運作邏輯
- 行為指令不會出現在輸出結果中
- 如果有多組指令，依據當下問題選擇最相關的

白話說：貼上這段提示之後，你的 NotebookLM 就變成一個「可以讀取並套用技能」的筆記本。

**每一本筆記本都可以這樣設定**，包括舊的筆記本。

### 步驟四：用 Google 文件存技能

把步驟一生成的行為指示，或你原本 Gem 的行為指示，存成 Google 文件。然後在 NotebookLM 左邊「新增來源」→「雲端硬碟」→ 選擇該文件 → 插入。

**為什麼用 Google 文件而不是直接貼文字**：
- Google 文件更新後，NotebookLM 按一下就能同步更新
- 貼文字的話，每次修改都要重新新增來源

一個 Google 文件 = 一個技能。要用哪個技能，就勾選哪個來源。

---

## 【獨家】進階技巧：把舊的生圖 Gem 轉成 NotebookLM 技能

![A colorful assortment of polished gemstones showcasing natural beauty and luster.](images/gem-notebooklm.jpg)
*Photo by [Markus Winkler](https://www.pexels.com/@markus-winkler-1430818) on [Pexels](https://www.pexels.com/photo/a-pile-of-colorful-stones-and-rocks-19902306/)*


如果你原本的 Gem 是直接生成圖片的（比如字母解謎、漫畫生成），要怎麼轉？

1. 把原本 Gem 的行為指示全部複製
2. 在 NotebookLM 裡勾選「指令架構師」技能
3. 把行為指示貼上，告訴它：「把最後的輸出規則改成輸出 YAML 格式的 AI 生成圖片提示詞」
4. 它會幫你在原版本基礎上修改（比如從 2.0 改成 2.1），保留原本邏輯

改好之後存成 Google 文件，新增為 NotebookLM 來源。以後要用這個技能時：
1. 勾選該技能 + 你的資料
2. NotebookLM 產出圖片提示詞
3. 到生圖 Gem 執行

### 多技能同時使用

你可以同時勾選兩個不衝突的技能。比如：
- 勾選「漫畫技能」+ 教材 PDF → 生成分鏡腳本
- 再勾選「字母解謎技能」→ 把關鍵字轉成解謎遊戲

如果對話開始跑掉，刪除對話記錄重新來。NotebookLM 有記憶效應，前面的對話會影響後面的結果。

### Google 生圖的小提醒

Google 目前的策略是：不管你選什麼模型，第一次都用 Imagen 2 生成（省資源）。如果不滿意，點「重做」選 Imagen Pro 才會用更好的模型。

---

<div style="background:#0F1D32;border:2px solid #00D4FF;border-radius:16px;padding:32px;margin:32px 0;text-align:center;">
<h2 style="color:#00D4FF;margin-top:0;border:none;display:block;font-size:24px;">免費下載：萬卷之王指令包</h2>
<p style="color:#C7C7CC;margin-bottom:20px;">影片裡的 3 組提示詞，複製貼上就能用。動態指令解析專家 + 指令架構師 Gem + 生圖專用 Gem。<br>填寫 Email 後立即寄到你的信箱。</p>
<div style="display:flex;justify-content:center;gap:16px;flex-wrap:wrap;margin-bottom:24px;">
<span style="background:rgba(0,212,255,.1);border:1px solid rgba(0,212,255,.25);border-radius:8px;padding:8px 16px;color:#C7C7CC;font-size:13px;">NotebookLM 自訂提示詞</span>
<span style="background:rgba(0,212,255,.1);border:1px solid rgba(0,212,255,.25);border-radius:8px;padding:8px 16px;color:#C7C7CC;font-size:13px;">指令架構師 Gem 提示詞</span>
<span style="background:rgba(0,212,255,.1);border:1px solid rgba(0,212,255,.25);border-radius:8px;padding:8px 16px;color:#C7C7CC;font-size:13px;">生圖專用 Gem 提示詞</span>
</div>
<div id="nblm-form-area">
<form id="nblm-lead-form" style="max-width:400px;margin:0 auto;" novalidate>
<input type="text" id="nblm-name" name="name" placeholder="你的姓名" required style="width:100%;padding:12px 16px;border-radius:8px;border:1px solid #253350;background:#0A1628;color:#FFF;font-size:15px;margin-bottom:10px;box-sizing:border-box;">
<input type="email" id="nblm-email" name="email" placeholder="你的 Email" required style="width:100%;padding:12px 16px;border-radius:8px;border:1px solid #253350;background:#0A1628;color:#FFF;font-size:15px;margin-bottom:14px;box-sizing:border-box;">
<button type="submit" id="nblm-submit-btn" style="width:100%;padding:14px;border:none;border-radius:8px;background:#00D4FF;color:#0A1628;font-size:16px;font-weight:700;cursor:pointer;">免費下載指令包</button>
<div id="nblm-error-msg" style="color:#FF6B35;font-size:13px;margin-top:8px;display:none;"></div>
<p style="color:#8B8FA3;font-size:11px;margin-top:10px;">我們重視你的隱私，不會寄送垃圾信。</p>
</form>
</div>
<div id="nblm-success-msg" style="display:none;">
<div style="font-size:48px;margin-bottom:12px;">&#10003;</div>
<h3 style="color:#00D4FF;margin-bottom:8px;">指令包已寄出！</h3>
<p style="color:#C7C7CC;margin-bottom:16px;">請到信箱查收（記得看一下垃圾信匣）</p>
<a href="https://blog.autolab.cloud/notebooklm-skills-download/notebooklm-skills-prompts.txt" download style="display:inline-block;padding:10px 24px;border-radius:8px;background:#00D4FF;color:#0A1628;font-weight:700;text-decoration:none;margin-bottom:10px;">下載萬卷之王指令包</a>
<br>
<a href="https://line.me/ti/g2/o6oRaGIHTzZ1nEofxnT9Rbv7_ZHAX-rylbJfKA?utm_source=invitation&utm_medium=link_copy&utm_campaign=default" target="_blank" style="display:inline-block;padding:10px 24px;border-radius:8px;background:rgba(0,212,255,.15);color:#00D4FF;font-weight:700;text-decoration:none;margin-top:8px;">加入 LINE 學員社群</a>
</div>
</div>

<script>
(function(){
  var WEBHOOK_URL='https://n8n.autolab.cloud/webhook/notebooklm-skills-lead';
  var form=document.getElementById('nblm-lead-form');
  if(!form)return;
  var btn=document.getElementById('nblm-submit-btn');
  var err=document.getElementById('nblm-error-msg');
  var area=document.getElementById('nblm-form-area');
  var ok=document.getElementById('nblm-success-msg');
  form.addEventListener('submit',async function(e){
    e.preventDefault();err.style.display='none';
    var n=document.getElementById('nblm-name').value.trim();
    var em=document.getElementById('nblm-email').value.trim();
    if(!n){err.textContent='請輸入姓名';err.style.display='block';return;}
    if(!em||!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(em)){err.textContent='請輸入正確的 Email';err.style.display='block';return;}
    btn.disabled=true;btn.textContent='處理中...';
    try{
      var r=await fetch(WEBHOOK_URL,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({name:n,email:em,source:'notebooklm-skills-article-inline',timestamp:new Date().toISOString()})});
      if(!r.ok)throw new Error('err');
      area.style.display='none';ok.style.display='block';
    }catch(x){err.textContent='發送失敗，請稍後再試';err.style.display='block';btn.disabled=false;btn.textContent='免費下載指令包';}
  });
})();
</script>

## 阿峰觀點

![A modern humanoid robot with digital face and luminescent screen, symbolizing innovation in technology.](images/artificial-intelligence-business.jpg)
*Photo by [Kindel Media](https://www.pexels.com/@kindelmedia) on [Pexels](https://www.pexels.com/photo/low-angle-shot-of-robot-8566526/)*


我帶過超過 400 家企業做 AI 培訓，最常被問的就是：「這些工具我一個一個都會用，但怎麼串在一起？」

萬卷之王就是一個絕佳範例：
- **NotebookLM** 負責處理資料和套用技能（遵照度最高）
- **Gem** 負責生圖（NotebookLM 做不到的事）
- **Google 文件** 負責存技能（同步更新）

每個工具各司其職，組合起來就是一個完整的工作流。

這個方法最大的價值不是省了幾分鐘，而是讓你的 AI 工作流程變得「可組合」。你可以不斷新增技能、分享技能，甚至跟同事交換技能。這才是真正的 AI 協作。

「你是機長，AI 是機組人員。」你不需要每個工具都精通，但你要知道什麼時候該派誰上場。

---

## 本文提到的資源

| 工具 | 連結 | 說明 |
|------|------|------|
| NotebookLM | https://notebooklm.google.com | Google AI 筆記本 |
| Gemini | https://gemini.google.com | Google AI 聊天 + Gem |
| 原始直播影片 | https://www.youtube.com/watch?v=CkAs29S4ZxY | 萬卷之王完整教學 |

---

企業想導入 AI？阿峰老師服務過台積電、國泰金控、中華電信等超過 400 家企業
→ https://www.autolab.cloud

---

### 關於作者
黃敬峰（AI峰哥），企業 AI 實戰培訓專家，400+ 企業合作、10,000+ 學員。
核心心法：「會用、懂用、好用、每天用」
官網：https://www.autolab.cloud
