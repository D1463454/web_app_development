from flask import Blueprint, render_template, request, redirect, url_for, flash, abort

# 建立 Blueprint 以便未來管理
recipe_bp = Blueprint('recipes', __name__)

@recipe_bp.route('/')
@recipe_bp.route('/recipes')
def index():
    """
    【首頁 (食譜列表)】
    - HTTP 方法: GET
    - 處理邏輯: 呼叫 Recipe Model 取得所有食譜清單，按時間排序。
    - 輸出: 渲染 templates/recipes/index.html
    """
    pass

@recipe_bp.route('/recipes/search', methods=['GET'])
def search():
    """
    【搜尋食譜】
    - HTTP 方法: GET
    - 處理邏輯: 取得 URL 參數 'q'，呼叫 Model 進行模糊查詢。
    - 輸出: 渲染 templates/recipes/index.html 並帶入結果。
    """
    pass

@recipe_bp.route('/recipes/recommend', methods=['GET'])
def recommend():
    """
    【依照食材推薦】
    - HTTP 方法: GET
    - 處理邏輯: 取得 URL 參數 'ingredients'，呼叫 Model 找出包含這些食材的食譜。
    - 輸出: 渲染 templates/recipes/index.html 並標示推薦結果。
    """
    pass

@recipe_bp.route('/recipes/new', methods=['GET'])
def new_recipe():
    """
    【新增食譜頁面】
    - HTTP 方法: GET
    - 處理邏輯: 僅顯示新增表單。
    - 輸出: 渲染 templates/recipes/new.html
    """
    pass

@recipe_bp.route('/recipes', methods=['POST'])
def create_recipe():
    """
    【建立食譜】
    - HTTP 方法: POST
    - 處理邏輯: 接收表單資料 (name, ingredients, steps)，驗證必填，寫入資料庫。
    - 輸出: 成功重導向至首頁，失敗重新渲染表單並顯示錯誤。
    """
    pass

@recipe_bp.route('/recipes/<int:id>', methods=['GET'])
def recipe_detail(id):
    """
    【食譜詳細頁面】
    - HTTP 方法: GET
    - 處理邏輯: 呼叫 Model 查詢指定 id 的食譜資料。
    - 輸出: 渲染 templates/recipes/detail.html。找不到則 404。
    """
    pass

@recipe_bp.route('/recipes/<int:id>/edit', methods=['GET'])
def edit_recipe(id):
    """
    【編輯食譜頁面】
    - HTTP 方法: GET
    - 處理邏輯: 呼叫 Model 查詢指定 id 的食譜資料，預填於表單中。
    - 輸出: 渲染 templates/recipes/edit.html。找不到則 404。
    """
    pass

@recipe_bp.route('/recipes/<int:id>/edit', methods=['POST'])
def update_recipe(id):
    """
    【更新食譜】
    - HTTP 方法: POST
    - 處理邏輯: 接收修改後的表單資料，更新 DB 中該 id 的紀錄。
    - 輸出: 成功重導向至詳細頁面。失敗顯示錯誤。
    """
    pass

@recipe_bp.route('/recipes/<int:id>/delete', methods=['POST'])
def delete_recipe(id):
    """
    【刪除食譜】
    - HTTP 方法: POST
    - 處理邏輯: 呼叫 Model 刪除對應 id 的資料。
    - 輸出: 成功重導向至首頁。找不到則 404。
    """
    pass
