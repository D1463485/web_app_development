from datetime import datetime
from . import db

class Recipe(db.Model):
    """
    食譜資料表模型 (Recipe)
    """
    __tablename__ = 'recipes'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    instructions = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    ingredients = db.relationship('Ingredient', backref='recipe', lazy=True, cascade="all, delete-orphan")

    def to_dict(self):
        """將物件轉換為字典格式"""
        return {
            'id': self.id,
            'title': self.title,
            'instructions': self.instructions,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'ingredients': [i.to_dict() for i in self.ingredients]
        }

    @classmethod
    def create(cls, title, instructions, ingredients_data=None):
        """
        新增一筆食譜與對應的材料紀錄
        :param title: 食譜名稱
        :param instructions: 料理步驟
        :param ingredients_data: 材料清單 (dict 的 list，包含 name, quantity, unit)
        :return: 成功時回傳建立的 recipe 物件，失敗時拋出 Exception
        """
        try:
            recipe = cls(title=title, instructions=instructions)
            if ingredients_data:
                for item in ingredients_data:
                    ingredient = Ingredient(
                        name=item.get('name'),
                        quantity=item.get('quantity'),
                        unit=item.get('unit')
                    )
                    recipe.ingredients.append(ingredient)
            db.session.add(recipe)
            db.session.commit()
            return recipe
        except Exception as e:
            db.session.rollback()
            raise Exception(f"建立食譜失敗: {str(e)}")

    @classmethod
    def get_all(cls):
        """
        取得所有食譜，依建立時間降序排列
        :return: 食譜物件列表
        """
        try:
            return cls.query.order_by(cls.created_at.desc()).all()
        except Exception as e:
            raise Exception(f"查詢食譜列表失敗: {str(e)}")

    @classmethod
    def get_by_id(cls, recipe_id):
        """
        根據 ID 取得單筆食譜
        :param recipe_id: 食譜 ID
        :return: 食譜物件或 None
        """
        try:
            return cls.query.get(recipe_id)
        except Exception as e:
            raise Exception(f"查詢單筆食譜失敗: {str(e)}")

    def update(self, title=None, instructions=None, ingredients_data=None):
        """
        更新食譜與對應的材料
        :param title: 新的食譜名稱 (可選)
        :param instructions: 新的料理步驟 (可選)
        :param ingredients_data: 新的材料清單 (會完全替換舊的)
        :return: 更新後的 recipe 物件
        """
        try:
            if title:
                self.title = title
            if instructions:
                self.instructions = instructions
            
            if ingredients_data is not None:
                # 刪除舊的食材，新增新的食材
                for old_ing in self.ingredients:
                    db.session.delete(old_ing)
                
                for item in ingredients_data:
                    ingredient = Ingredient(
                        name=item.get('name'),
                        quantity=item.get('quantity'),
                        unit=item.get('unit')
                    )
                    self.ingredients.append(ingredient)
                    
            db.session.commit()
            return self
        except Exception as e:
            db.session.rollback()
            raise Exception(f"更新食譜失敗: {str(e)}")

    def delete(self):
        """
        刪除此食譜 (關聯的材料也會因 cascade 一併刪除)
        """
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise Exception(f"刪除食譜失敗: {str(e)}")

class Ingredient(db.Model):
    """
    材料資料表模型 (Ingredient)
    """
    __tablename__ = 'ingredients'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id', ondelete='CASCADE'), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    quantity = db.Column(db.String(50), nullable=True)
    unit = db.Column(db.String(20), nullable=True)

    def to_dict(self):
        """將物件轉換為字典格式"""
        return {
            'id': self.id,
            'recipe_id': self.recipe_id,
            'name': self.name,
            'quantity': self.quantity,
            'unit': self.unit
        }
