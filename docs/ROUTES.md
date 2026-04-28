# 路由設計文件 (ROUTES)

根據 PRD 與 FLOWCHART 的設計要求，本文件定義食譜收藏系統所有的 Flask 路由、HTTP 方法、處理邏輯及對應的 Jinja2 模板。

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| :--- | :--- | :--- | :--- | :--- |
| 首頁 (食譜列表) | GET | `/` 或 `/recipes` | `templates/recipes/index.html` | 顯示所有已收藏的食譜列表 |
| 搜尋食譜 | GET | `/recipes/search` | `templates/recipes/index.html` | 透過 Query Parameter（如 `?q=關鍵字`）搜尋食譜名稱 |
| 依照食材推薦 | GET | `/recipes/recommend` | `templates/recipes/index.html` | 輸入手上食材，系統推薦符合的食譜 |
| 新增食譜頁面 | GET | `/recipes/new` | `templates/recipes/new.html` | 顯示填寫食譜內容的 HTML 表單 |
| 建立食譜 | POST | `/recipes` | — | 接收表單資料並儲存至資料庫，成功後重導向至首頁 |
| 食譜詳細頁面 | GET | `/recipes/<int:id>` | `templates/recipes/detail.html` | 顯示特定食譜的完整資訊 |
| 編輯食譜頁面 | GET | `/recipes/<int:id>/edit` | `templates/recipes/edit.html` | 顯示帶有原有資料的表單，供使用者修改 |
| 更新食譜 | POST | `/recipes/<int:id>/edit` | — | 接收修改後的表單資料並更新 DB，成功後重導向至詳細頁面 |
| 刪除食譜 | POST | `/recipes/<int:id>/delete` | — | 刪除特定的食譜，成功後重導向至首頁 |

## 2. 每個路由的詳細說明

### 首頁 (食譜列表)
- **URL**: `/` 或 `/recipes`
- **HTTP 方法**: GET
- **輸入**: 無
- **處理邏輯**: 呼叫 `Recipe` Model 取得所有食譜清單，按時間排序。
- **輸出**: 渲染 `templates/recipes/index.html`。
- **錯誤處理**: 無。

### 搜尋食譜
- **URL**: `/recipes/search`
- **HTTP 方法**: GET
- **輸入**: URL 參數 `q` (例如 `/recipes/search?q=雞肉`)
- **處理邏輯**: 呼叫 Model 進行資料庫模糊查詢（對 `name` 欄位進行 `LIKE %關鍵字%` 比對）。
- **輸出**: 渲染 `templates/recipes/index.html`，並傳入搜尋結果與關鍵字。
- **錯誤處理**: 若未提供搜尋關鍵字，則顯示所有清單。

### 依照食材推薦
- **URL**: `/recipes/recommend`
- **HTTP 方法**: GET
- **輸入**: URL 參數 `ingredients` (例如 `/recipes/recommend?ingredients=雞肉,洋蔥`)
- **處理邏輯**: 呼叫 Model，針對 `ingredients` 欄位進行比對，找出包含這些食材的食譜。
- **輸出**: 渲染 `templates/recipes/index.html`，並標示為推薦結果。
- **錯誤處理**: 若未提供食材，提示使用者輸入。

### 新增食譜頁面
- **URL**: `/recipes/new`
- **HTTP 方法**: GET
- **輸入**: 無
- **處理邏輯**: 無特殊邏輯，僅需顯示表單。
- **輸出**: 渲染 `templates/recipes/new.html`。
- **錯誤處理**: 無。

### 建立食譜
- **URL**: `/recipes`
- **HTTP 方法**: POST
- **輸入**: 表單欄位 (`name`, `ingredients`, `steps`)
- **處理邏輯**: 驗證必填欄位。若驗證成功，呼叫 Model 將資料寫入資料庫。
- **輸出**: 成功後 `redirect('/')` 重導向至首頁。
- **錯誤處理**: 若必填欄位缺失，重新渲染 `templates/recipes/new.html` 並顯示錯誤訊息。

### 食譜詳細頁面
- **URL**: `/recipes/<int:id>`
- **HTTP 方法**: GET
- **輸入**: URL 路徑變數 `id`
- **處理邏輯**: 呼叫 Model 查詢指定 `id` 的食譜資料。
- **輸出**: 渲染 `templates/recipes/detail.html`。
- **錯誤處理**: 若查無指定 ID 的資料，返回 404 Not Found 畫面。

### 編輯食譜頁面
- **URL**: `/recipes/<int:id>/edit`
- **HTTP 方法**: GET
- **輸入**: URL 路徑變數 `id`
- **處理邏輯**: 呼叫 Model 查詢指定 `id` 的食譜資料，用於預填表單。
- **輸出**: 渲染 `templates/recipes/edit.html`。
- **錯誤處理**: 若查無指定 ID，返回 404 畫面。

### 更新食譜
- **URL**: `/recipes/<int:id>/edit`
- **HTTP 方法**: POST
- **輸入**: URL 路徑變數 `id`，以及表單欄位 (`name`, `ingredients`, `steps`)
- **處理邏輯**: 驗證必填資料後，呼叫 Model 更新指定 `id` 的紀錄。
- **輸出**: 成功後 `redirect('/recipes/<id>')` 重導向至詳細頁面。
- **錯誤處理**: 若查無 ID 返回 404；若驗證失敗，重新渲染編輯頁面並提示錯誤。

### 刪除食譜
- **URL**: `/recipes/<int:id>/delete`
- **HTTP 方法**: POST
- **輸入**: URL 路徑變數 `id`
- **處理邏輯**: 呼叫 Model 刪除對應資料。
- **輸出**: 成功後 `redirect('/')` 重導向至首頁。
- **錯誤處理**: 若查無指定 ID 返回 404。

## 3. Jinja2 模板清單

所有模板放置於 `app/templates/` 內，統一繼承 `base.html`：

- `base.html`: 基礎佈局（包含 Header, Footer, 導覽列與共用的靜態資源引用）。
- `recipes/index.html`: 食譜列表頁（兼具首頁、搜尋結果與推薦結果顯示用途）。
- `recipes/detail.html`: 單筆食譜詳細內容頁，包含編輯與刪除的按鈕。
- `recipes/new.html`: 新增食譜表單頁。
- `recipes/edit.html`: 編輯食譜表單頁。

## 4. 路由骨架程式碼

路由的實作骨架已建立於 `app/routes/recipes.py`，裡面包含所有的 `@app.route` 定義與函式 docstring。
