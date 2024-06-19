from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.exceptions import NotFound
from marshmallow import ValidationError

from db import db
from models import RecipeModel
from schemas import RecipeSchema, RecipeUpdateSchema, RecipeResponseSchema, RecipeListResponseSchema

blp = Blueprint("Recipes", "recipes", description="Operations on recipes")

@blp.route("/recipes/<int:recipe_id>")
class Recipe(MethodView):
    @blp.response(200, RecipeResponseSchema)
    def get(self, recipe_id):
        if recipe_id is None:
            recipe_id = 1
        recipe = RecipeModel.query.get_or_404(recipe_id)
        return {
            "message": "Recipe details by id",
            "recipe": [recipe]
        }

    @blp.response(200, RecipeResponseSchema)
    def delete(self, recipe_id):
        try:
            recipe = RecipeModel.query.get_or_404(recipe_id)
        except NotFound:
            return {"message": "No recipe found"}, 404
        db.session.delete(recipe)
        db.session.commit()
        return {"message": "Recipe successfully removed!"}, 200

    @blp.arguments(RecipeUpdateSchema)
    @blp.response(200, RecipeResponseSchema)
    def patch(self, recipe_data, recipe_id):
        if recipe_id is None:
            recipe_id = 1
        recipe = RecipeModel.query.get_or_404(recipe_id)
        
        for key, value in recipe_data.items():
            setattr(recipe, key, value)

        db.session.commit()
        return {
            "message": "Recipe successfully updated!",
            "recipe": [recipe]
        }

@blp.route("/recipes")
class RecipeList(MethodView):
    @blp.response(200, RecipeListResponseSchema)
    def get(self):
        return {
            "recipes": RecipeModel.query.all()
        }

    @blp.arguments(RecipeSchema)
    @blp.response(200, RecipeResponseSchema)
    def post(self, recipe_data):
        required_fields = ['title', 'making_time', 'serves', 'ingredients', 'cost']
        
        missing_fields = [field for field in required_fields if field not in recipe_data]
        if missing_fields:
            return {
                "message": "Recipe creation failed!",
                "required": required_fields
            }, 422
        
        recipe = RecipeModel(**recipe_data)
        
        try:
            db.session.add(recipe)
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback() 
            return {
                "message": "Recipe creation failed!",
                "required": required_fields
            }, 500
        
        return {
            "message": "Recipe successfully created!",
            "recipe": [recipe]
        }
    
@blp.errorhandler(422)
def recipe_post_error(e):
    return {
        "message": "Recipe creation failed!",
        "required": "title, making_time, serves, ingredients, cost"
        }