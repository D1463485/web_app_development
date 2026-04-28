from flask import Blueprint, render_template, request, redirect, url_for, flash

recipe_bp = Blueprint('recipes', __name__)

@recipe_bp.route('/')
@recipe_bp.route('/recipes')
def index():
    """
    食譜列表 (首頁)
    - 輸入: URL 查詢參數 ?q=keyword (可選)
    - 處理邏輯: 根據關鍵字搜尋食譜，或取得全部食譜
    - 輸出: 渲染 recipes/index.html
    """
    pass

@recipe_bp.route('/recipes/new', methods=['GET', 'POST'])
def create_recipe():
    """
    新增食譜頁面與建立食譜邏輯
    - GET: 準備空資料，渲染 recipes/form.html
    - POST: 接收表單資料，寫入 DB，成功後重導向至首頁
    """
    pass

@recipe_bp.route('/recipes/<int:recipe_id>')
def recipe_detail(recipe_id):
    """
    食譜詳情
    - 輸入: recipe_id
    - 處理邏輯: 根據 ID 取得單一食譜資料
    - 輸出: 渲染 recipes/detail.html (找不到時回傳 404)
    """
    pass

@recipe_bp.route('/recipes/<int:recipe_id>/edit', methods=['GET', 'POST'])
def edit_recipe(recipe_id):
    """
    編輯食譜頁面與更新邏輯
    - GET: 根據 ID 取得資料，渲染 recipes/form.html
    - POST: 接收修改後的表單資料，更新 DB，成功後重導向至詳情頁
    """
    pass

@recipe_bp.route('/recipes/<int:recipe_id>/delete', methods=['POST'])
def delete_recipe(recipe_id):
    """
    刪除食譜
    - 輸入: recipe_id
    - 處理邏輯: 根據 ID 刪除資料庫中的該筆紀錄
    - 輸出: 成功後重導向至首頁
    """
    pass
