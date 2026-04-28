# 路由設計 (Route Design) - 食譜收藏夾

本文件基於 PRD、系統架構與資料庫設計，規劃了食譜收藏夾的所有 Flask 路由、HTTP 方法以及對應的 Jinja2 模板。

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| :--- | :--- | :--- | :--- | :--- |
| 食譜列表 (首頁) | GET | `/` 或 `/recipes` | `templates/recipes/index.html` | 顯示所有食譜，支援搜尋 |
| 新增食譜頁面 | GET | `/recipes/new` | `templates/recipes/form.html` | 顯示新增表單 |
| 建立食譜 | POST | `/recipes/new` | — | 接收表單，存入 DB，重導向至首頁 |
| 食譜詳情 | GET | `/recipes/<int:recipe_id>` | `templates/recipes/detail.html` | 顯示單筆食譜內容與材料 |
| 編輯食譜頁面 | GET | `/recipes/<int:recipe_id>/edit` | `templates/recipes/form.html` | 顯示帶有原資料的表單 |
| 更新食譜 | POST | `/recipes/<int:recipe_id>/edit` | — | 接收表單，更新 DB，重導向至詳情頁 |
| 刪除食譜 | POST | `/recipes/<int:recipe_id>/delete`| — | 刪除資料庫紀錄，重導向至首頁 |

## 2. 每個路由的詳細說明

### 2.1 食譜列表 (首頁)
- **URL**: `GET /` 或 `GET /recipes`
- **輸入**: URL 查詢參數 `?q=keyword` (可選，用於搜尋)
- **處理邏輯**: 若有 `q` 參數，呼叫 `Recipe.query.filter` 搜尋標題；否則呼叫 `Recipe.get_all()` 取得全部食譜。
- **輸出**: 渲染 `recipes/index.html`，傳遞 `recipes` 列表與目前的 `q`。
- **錯誤處理**: 無特定錯誤，若無資料顯示空狀態提示。

### 2.2 新增食譜頁面
- **URL**: `GET /recipes/new`
- **輸入**: 無
- **處理邏輯**: 準備空資料供模板使用。
- **輸出**: 渲染 `recipes/form.html`。
- **錯誤處理**: 無。

### 2.3 建立食譜
- **URL**: `POST /recipes/new`
- **輸入**: 表單資料 `title`, `instructions`, `ingredients[]` (名稱、數量、單位陣列)。
- **處理邏輯**: 驗證必填欄位 (title, instructions)。呼叫 `Recipe.create()` 寫入資料庫。
- **輸出**: 成功後 HTTP 302 重導向至 `/`。
- **錯誤處理**: 若驗證失敗，重新渲染 `recipes/form.html` 並顯示錯誤訊息。

### 2.4 食譜詳情
- **URL**: `GET /recipes/<int:recipe_id>`
- **輸入**: URL 參數 `recipe_id`
- **處理邏輯**: 呼叫 `Recipe.get_by_id(recipe_id)`。
- **輸出**: 渲染 `recipes/detail.html`，傳遞 `recipe` 物件。
- **錯誤處理**: 若找不到對應 ID，回傳 404 頁面。

### 2.5 編輯食譜頁面
- **URL**: `GET /recipes/<int:recipe_id>/edit`
- **輸入**: URL 參數 `recipe_id`
- **處理邏輯**: 呼叫 `Recipe.get_by_id(recipe_id)` 取得現有資料。
- **輸出**: 渲染 `recipes/form.html`，傳遞 `recipe` 物件。
- **錯誤處理**: 若找不到對應 ID，回傳 404 頁面。

### 2.6 更新食譜
- **URL**: `POST /recipes/<int:recipe_id>/edit`
- **輸入**: URL 參數 `recipe_id`，表單資料 `title`, `instructions`, `ingredients[]`。
- **處理邏輯**: 取得現有 Recipe，呼叫 `recipe.update()` 更新資料。
- **輸出**: 成功後 HTTP 302 重導向至 `/recipes/<recipe_id>`。
- **錯誤處理**: 若驗證失敗，重新渲染 `recipes/form.html` 並顯示錯誤訊息；若找不到 ID 則回傳 404。

### 2.7 刪除食譜
- **URL**: `POST /recipes/<int:recipe_id>/delete`
- **輸入**: URL 參數 `recipe_id`
- **處理邏輯**: 呼叫 `Recipe.get_by_id()` 取得物件後執行 `recipe.delete()`。
- **輸出**: 成功後 HTTP 302 重導向至 `/`。
- **錯誤處理**: 若找不到 ID 則回傳 404。

## 3. Jinja2 模板清單

所有模板將放置於 `app/templates/` 目錄下：

- `base.html`: 所有頁面的共用基礎模板 (Header, Footer, CSS/JS 引入)。
- `recipes/index.html`: 首頁，繼承 `base.html`，顯示搜尋列與食譜卡片列表。
- `recipes/detail.html`: 食譜詳情頁，繼承 `base.html`，顯示完整作法與材料清單。
- `recipes/form.html`: 新增與編輯共用的表單頁面，繼承 `base.html`，使用 Jinja2 判斷是新增還是編輯模式來改變按鈕文字與 Action 網址。

## 4. 路由骨架程式碼
已於 `app/routes/recipe_routes.py` 建立 Blueprint 路由骨架，定義了各個函式與註解，供後續實作邏輯。
