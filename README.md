# Discord 炸群機器人
## 📌 專案簡介 (Project Overview)
本專案為 Discord Bot 的安全性概念驗證 (PoC) 工具，旨在展示當機器人獲得高權限（如 `Administrator`）時，Discord API 可能產生的破壞性機制。透過模擬自動化炸群與資源清空行為，協助伺服器管理員與資安人員評估潛在安全風險、驗證權限控管漏洞以及測試 API Rate Limit 防禦力。

**模擬測試行為範疇：**
* **頻道與身分組管理**：批次刪除與動態無限建立頻道/身分組測試。
* **成員管理機制**：模擬高頻率大規模封鎖 (Ban) 與剔除操作。
* **Webhook 與訊息廣播**：測試大量 Markdown 訊息與 Webhook 推播對 Event Loop 與伺服器頻寬的衝擊。

## ⚠️ 免責聲明與使用條款 (Disclaimer)
* **教育與研究用途**：本程式僅供資安技術研究、學術討論與授權之安全性測試。
* **法律責任**：使用者需完全承擔因不當使用所衍生之法律責任、帳號懲處（如 Discord Ban）與伺服器損失，開發團隊概不負責。使用者需自行承擔一切法律、帳號與平台風險。
* **合規性要求**：請嚴格遵守 [Discord Terms of Service](https://discord.com/terms) 與 [Developer Terms](https://discord.com/developers/docs/legal)，絕對禁止用於未經授權的目標伺服器。

## ⚙️ 技術架構與環境需求 (Technical Requirements)
### 運行環境
* **Python**: `3.8+`
* **主要依賴庫**：`discord.py`

### 必備套件安裝
```bash
pip install discord.py
```
## 🚀 快速開始 (Getting Started)
### 1. 取得 Bot Token 與設定權限
1. 開啟 [Discord Developer Portal](https://discord.com/developers/applications)。
2. 建立應用程式並新增 Bot。
3. 於 **Privileged Gateway Intents** 區塊開啟：
* `MESSAGE CONTENT INTENT`
* `SERVER MEMBERS INTENT`

4. 複製 Bot Token。
### 2. 配置動態檔案與執行
程式啟動時會自動於根目錄下建立預設組態檔：
* `channels.txt`：定義欲建立的頻道名稱清單。
* `messages.txt`：定義廣播發送的 Markdown 訊息內容。
在主程式中貼入 Token 後執行：

```bash
python full_nuke.py
```

## 👨‍💻 專案資訊 (Project Info)
* **開發與發布**：N.L. / YX International Strategy
* **授權條款**：MIT License
