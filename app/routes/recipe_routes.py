from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.recipe import Recipe

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
    q = request.args.get('q', '').strip()
    try:
        if q:
            # 簡單搜尋：標題包含關鍵字
            recipes = Recipe.query.filter(Recipe.title.ilike(f'%{q}%')).order_by(Recipe.created_at.desc()).all()
        else:
            recipes = Recipe.get_all()
    except Exception as e:
        flash(f'載入食譜列表失敗: {str(e)}', 'danger')
        recipes = []
        
    return render_template('recipes/index.html', recipes=recipes, q=q)

@recipe_bp.route('/recipes/new', methods=['GET', 'POST'])
def create_recipe():
    """
    新增食譜頁面與建立食譜邏輯
    - GET: 準備空資料，渲染 recipes/form.html
    - POST: 接收表單資料，寫入 DB，成功後重導向至首頁
    """
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        instructions = request.form.get('instructions', '').strip()
        
        # 基本驗證
        if not title or not instructions:
            flash('名稱與料理步驟為必填欄位', 'danger')
            return render_template('recipes/form.html', action=url_for('recipes.create_recipe'))
            
        # 解析材料 (假設前端送來的 name='ingredient_name[]', 'ingredient_qty[]', 'ingredient_unit[]')
        ingredient_names = request.form.getlist('ingredient_name[]')
        ingredient_qtys = request.form.getlist('ingredient_qty[]')
        ingredient_units = request.form.getlist('ingredient_unit[]')
        
        ingredients_data = []
        for i in range(len(ingredient_names)):
            name = ingredient_names[i].strip()
            if name: # 材料名稱有填寫才加入
                qty = ingredient_qtys[i].strip() if i < len(ingredient_qtys) else ''
                unit = ingredient_units[i].strip() if i < len(ingredient_units) else ''
                ingredients_data.append({'name': name, 'quantity': qty, 'unit': unit})
                
        try:
            Recipe.create(title=title, instructions=instructions, ingredients_data=ingredients_data)
            flash('食譜新增成功！', 'success')
            return redirect(url_for('recipes.index'))
        except Exception as e:
            flash(f'新增失敗: {str(e)}', 'danger')
            return render_template('recipes/form.html', action=url_for('recipes.create_recipe'), title=title, instructions=instructions)

    # GET 請求
    return render_template('recipes/form.html', action=url_for('recipes.create_recipe'))

@recipe_bp.route('/recipes/<int:recipe_id>')
def recipe_detail(recipe_id):
    """
    食譜詳情
    - 輸入: recipe_id
    - 處理邏輯: 根據 ID 取得單一食譜資料
    - 輸出: 渲染 recipes/detail.html (找不到時回傳 404)
    """
    try:
        recipe = Recipe.get_by_id(recipe_id)
        if not recipe:
            flash('找不到該食譜', 'warning')
            return redirect(url_for('recipes.index'))
        return render_template('recipes/detail.html', recipe=recipe)
    except Exception as e:
        flash(f'載入食譜失敗: {str(e)}', 'danger')
        return redirect(url_for('recipes.index'))

@recipe_bp.route('/recipes/<int:recipe_id>/edit', methods=['GET', 'POST'])
def edit_recipe(recipe_id):
    """
    編輯食譜頁面與更新邏輯
    - GET: 根據 ID 取得資料，渲染 recipes/form.html
    - POST: 接收修改後的表單資料，更新 DB，成功後重導向至詳情頁
    """
    try:
        recipe = Recipe.get_by_id(recipe_id)
        if not recipe:
            flash('找不到該食譜', 'warning')
            return redirect(url_for('recipes.index'))
            
        if request.method == 'POST':
            title = request.form.get('title', '').strip()
            instructions = request.form.get('instructions', '').strip()
            
            if not title or not instructions:
                flash('名稱與料理步驟為必填欄位', 'danger')
                return render_template('recipes/form.html', action=url_for('recipes.edit_recipe', recipe_id=recipe.id), recipe=recipe)
                
            ingredient_names = request.form.getlist('ingredient_name[]')
            ingredient_qtys = request.form.getlist('ingredient_qty[]')
            ingredient_units = request.form.getlist('ingredient_unit[]')
            
            ingredients_data = []
            for i in range(len(ingredient_names)):
                name = ingredient_names[i].strip()
                if name:
                    qty = ingredient_qtys[i].strip() if i < len(ingredient_qtys) else ''
                    unit = ingredient_units[i].strip() if i < len(ingredient_units) else ''
                    ingredients_data.append({'name': name, 'quantity': qty, 'unit': unit})
                    
            recipe.update(title=title, instructions=instructions, ingredients_data=ingredients_data)
            flash('食譜更新成功！', 'success')
            return redirect(url_for('recipes.recipe_detail', recipe_id=recipe.id))
            
        # GET 請求
        return render_template('recipes/form.html', action=url_for('recipes.edit_recipe', recipe_id=recipe.id), recipe=recipe)
        
    except Exception as e:
        flash(f'發生錯誤: {str(e)}', 'danger')
        return redirect(url_for('recipes.index'))

@recipe_bp.route('/recipes/<int:recipe_id>/delete', methods=['POST'])
def delete_recipe(recipe_id):
    """
    刪除食譜
    - 輸入: recipe_id
    - 處理邏輯: 根據 ID 刪除資料庫中的該筆紀錄
    - 輸出: 成功後重導向至首頁
    """
    try:
        recipe = Recipe.get_by_id(recipe_id)
        if recipe:
            recipe.delete()
            flash('食譜已刪除', 'success')
        else:
            flash('找不到該食譜', 'warning')
    except Exception as e:
        flash(f'刪除失敗: {str(e)}', 'danger')
        
    return redirect(url_for('recipes.index'))
