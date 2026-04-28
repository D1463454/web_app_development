from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
import app.models.recipe as recipe_model

# 建立 Blueprint 以便未來管理
recipe_bp = Blueprint('recipes', __name__)

@recipe_bp.route('/')
@recipe_bp.route('/recipes')
def index():
    """
    【首頁 (食譜列表)】
    """
    recipes = recipe_model.get_all()
    return render_template('recipes/index.html', recipes=recipes)

@recipe_bp.route('/recipes/search', methods=['GET'])
def search():
    """
    【搜尋食譜】
    """
    q = request.args.get('q', '').strip()
    if not q:
        return redirect(url_for('recipes.index'))
        
    recipes = recipe_model.search_by_keyword(q)
    return render_template('recipes/index.html', recipes=recipes, search_query=q)

@recipe_bp.route('/recipes/recommend', methods=['GET'])
def recommend():
    """
    【依照食材推薦】
    """
    ingredients = request.args.get('ingredients', '').strip()
    if not ingredients:
        flash('請輸入要推薦的食材關鍵字', 'warning')
        return redirect(url_for('recipes.index'))
        
    # 將輸入字串依逗號分隔成列表
    ingredients_list = [i.strip() for i in ingredients.split(',') if i.strip()]
    recipes = recipe_model.recommend_by_ingredients(ingredients_list)
    return render_template('recipes/index.html', recipes=recipes, recommend_ingredients=ingredients)

@recipe_bp.route('/recipes/new', methods=['GET'])
def new_recipe():
    """
    【新增食譜頁面】
    """
    return render_template('recipes/new.html')

@recipe_bp.route('/recipes', methods=['POST'])
def create_recipe():
    """
    【建立食譜】
    """
    name = request.form.get('name', '').strip()
    ingredients = request.form.get('ingredients', '').strip()
    steps = request.form.get('steps', '').strip()
    image_url = request.form.get('image_url', '').strip()
    
    # 基礎驗證
    if not name or not ingredients or not steps:
        flash('「名稱」、「食材」與「步驟」皆為必填欄位！', 'danger')
        # 將填寫的資料帶回表單，避免使用者重打
        return render_template('recipes/new.html', name=name, ingredients=ingredients, steps=steps, image_url=image_url)
        
    data = {
        'name': name,
        'ingredients': ingredients,
        'steps': steps,
        'image_url': image_url
    }
    
    new_id = recipe_model.create(data)
    if new_id:
        flash('食譜新增成功！', 'success')
        return redirect(url_for('recipes.index'))
    else:
        flash('新增食譜時發生錯誤，請稍後再試。', 'danger')
        return render_template('recipes/new.html', name=name, ingredients=ingredients, steps=steps, image_url=image_url)

@recipe_bp.route('/recipes/<int:id>', methods=['GET'])
def recipe_detail(id):
    """
    【食譜詳細頁面】
    """
    recipe = recipe_model.get_by_id(id)
    if not recipe:
        abort(404)
    return render_template('recipes/detail.html', recipe=recipe)

@recipe_bp.route('/recipes/<int:id>/edit', methods=['GET'])
def edit_recipe(id):
    """
    【編輯食譜頁面】
    """
    recipe = recipe_model.get_by_id(id)
    if not recipe:
        abort(404)
    return render_template('recipes/edit.html', recipe=recipe)

@recipe_bp.route('/recipes/<int:id>/edit', methods=['POST'])
def update_recipe(id):
    """
    【更新食譜】
    """
    # 先確認食譜是否存在
    recipe = recipe_model.get_by_id(id)
    if not recipe:
        abort(404)
        
    name = request.form.get('name', '').strip()
    ingredients = request.form.get('ingredients', '').strip()
    steps = request.form.get('steps', '').strip()
    image_url = request.form.get('image_url', '').strip()
    
    if not name or not ingredients or not steps:
        flash('「名稱」、「食材」與「步驟」皆為必填欄位！', 'danger')
        # 構造一個臨時的 dict 讓表單保留未通過驗證的修改內容
        temp_recipe = {'id': id, 'name': name, 'ingredients': ingredients, 'steps': steps, 'image_url': image_url}
        return render_template('recipes/edit.html', recipe=temp_recipe)
        
    data = {
        'name': name,
        'ingredients': ingredients,
        'steps': steps,
        'image_url': image_url
    }
    
    success = recipe_model.update(id, data)
    if success:
        flash('食譜更新成功！', 'success')
        return redirect(url_for('recipes.recipe_detail', id=id))
    else:
        flash('更新食譜時發生內部錯誤。', 'danger')
        temp_recipe = {'id': id, 'name': name, 'ingredients': ingredients, 'steps': steps, 'image_url': image_url}
        return render_template('recipes/edit.html', recipe=temp_recipe)

@recipe_bp.route('/recipes/<int:id>/delete', methods=['POST'])
def delete_recipe(id):
    """
    【刪除食譜】
    """
    recipe = recipe_model.get_by_id(id)
    if not recipe:
        abort(404)
        
    success = recipe_model.delete(id)
    if success:
        flash('食譜已刪除！', 'success')
    else:
        flash('刪除食譜時發生錯誤。', 'danger')
        
    return redirect(url_for('recipes.index'))
