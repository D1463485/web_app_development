from datetime import datetime
from . import db

class Recipe(db.Model):
    __tablename__ = 'recipes'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    instructions = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    ingredients = db.relationship('Ingredient', backref='recipe', lazy=True, cascade="all, delete-orphan")

    def to_dict(self):
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

    @classmethod
    def get_all(cls):
        return cls.query.order_by(cls.created_at.desc()).all()

    @classmethod
    def get_by_id(cls, recipe_id):
        return cls.query.get(recipe_id)

    def update(self, title=None, instructions=None, ingredients_data=None):
        if title:
            self.title = title
        if instructions:
            self.instructions = instructions
        
        if ingredients_data is not None:
            # 簡單的做法：刪除舊的食材，新增新的食材
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

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class Ingredient(db.Model):
    __tablename__ = 'ingredients'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id', ondelete='CASCADE'), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    quantity = db.Column(db.String(50), nullable=True)
    unit = db.Column(db.String(20), nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'recipe_id': self.recipe_id,
            'name': self.name,
            'quantity': self.quantity,
            'unit': self.unit
        }
