# 流程圖文件 (FLOWCHART)

根據產品需求文件 (PRD) 所描述的需求，以下是系統的使用者流程圖、系統序列圖，以及功能清單對照表。

> **注意：** 系統目前似乎尚未建立 `docs/ARCHITECTURE.md`，但我已根據 PRD 記載的技術限制（Flask + Jinja2 + SQLite）來繪製系統序列圖與推斷架構。

## 1. 使用者流程圖（User Flow）

描述使用者進入食譜收藏系統後的各種操作路徑。

```mermaid
flowchart LR
    A([使用者開啟網頁]) --> B[首頁 - 食譜列表]
    
    B --> C{要執行什麼操作？}
    
    C -->|搜尋食譜| D[輸入關鍵字並送出]
    D --> B
    
    C -->|食材推薦| E[輸入現有食材並送出]
    E --> B
    
    C -->|新增食譜| F[進入新增食譜頁面]
    F -->|填寫完成並送出| F_Submit[新增成功]
    F_Submit --> B
    
    C -->|查看詳細| G[進入食譜詳細頁面]
    
    G --> H{要執行什麼額外操作？}
    
    H -->|編輯食譜| I[進入編輯食譜頁面]
    I -->|修改完成並送出| I_Submit[編輯成功]
    I_Submit --> G
    
    H -->|刪除食譜| J[點擊刪除按鈕]
    J --> B
```

## 2. 系統序列圖（Sequence Diagram）

以下以**「新增食譜」**為例，描述從使用者操作到資料存入資料庫的完整流程。

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 使用者瀏覽器
    participant Flask as Flask Route/Controller
    participant DB as SQLite (Model)
    
    User->>Browser: 在新增食譜頁面填寫表單並送出
    Browser->>Flask: POST /recipes
    Flask->>Flask: 驗證接收到的資料 (名稱、食材、步驟)
    Flask->>DB: INSERT INTO recipes (新增食譜紀錄)
    DB-->>Flask: 回傳存檔成功確認
    Flask-->>Browser: HTTP 302 重導向到首頁 (食譜列表)
    Browser->>User: 看到剛新增的食譜出現在列表中
```

## 3. 功能清單對照表

列出每個主要功能對應的 URL 路徑與 HTTP 方法。

| 功能 | URL 路徑 | HTTP 方法 | 說明 |
| :--- | :--- | :--- | :--- |
| **首頁 (食譜列表)** | `/` 或 `/recipes` | GET | 顯示所有已收藏的食譜列表 |
| **搜尋食譜** | `/recipes/search` | GET | 透過 Query Parameter（如 `?q=關鍵字`）搜尋食譜名稱 |
| **依照食材推薦** | `/recipes/recommend` | GET | 輸入手上食材，系統推薦符合的食譜 |
| **新增食譜 (表單)** | `/recipes/new` | GET | 顯示填寫食譜內容的 HTML 表單 |
| **新增食譜 (送出)** | `/recipes` | POST | 接收表單資料並儲存至資料庫 |
| **食譜詳細頁面** | `/recipes/<id>` | GET | 顯示特定食譜的完整資訊（食材、步驟等） |
| **編輯食譜 (表單)** | `/recipes/<id>/edit` | GET | 顯示帶有原有資料的表單，供使用者修改 |
| **編輯食譜 (送出)** | `/recipes/<id>/edit` | POST | 接收修改後的表單資料並更新至資料庫 |
| **刪除食譜** | `/recipes/<id>/delete` | POST | 刪除特定的食譜（使用 POST 避免 GET 造成的誤刪風險）|
