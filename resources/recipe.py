from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import RecipeModel
from schemas import RecipeSchema, RecipeUpdateSchema, RecipeResponseSchema, RecipeListResponseSchema

blp = Blueprint("Recipes", "recipes", description="Operations on recipes")

@blp.route("/recipes/<int:recipe_id>")
class Recipe(MethodView):
    @blp.response(200, RecipeResponseSchema)
    def get(self, recipe_id):
        recipe = RecipeModel.query.get_or_404(recipe_id)
        return {
            "message": "Recipe retrieved successfully.",
            "recipe": recipe
        }

    @blp.response(200, RecipeResponseSchema)
    def delete(self, recipe_id):
        recipe = RecipeModel.query.get_or_404(recipe_id)
        db.session.delete(recipe)
        db.session.commit()
        return {"message": "Recipe deleted successfully."}

    @blp.arguments(RecipeUpdateSchema)
    @blp.response(200, RecipeResponseSchema)
    def patch(self, recipe_data, recipe_id):
        recipe = RecipeModel.query.get_or_404(recipe_id)
        
        for key, value in recipe_data.items():
            setattr(recipe, key, value)

        db.session.commit()
        return {
            "message": "Recipe updated successfully.",
            "recipe": recipe
        }

@blp.route("/recipes")
class RecipeList(MethodView):
    @blp.response(200, RecipeListResponseSchema)
    def get(self):
        return {
            "message": "Recipes retrieved successfully.",
            "recipes": RecipeModel.query.all()
        }

    @blp.arguments(RecipeSchema)
    @blp.response(201, RecipeResponseSchema)
    def post(self, recipe_data):
        recipe = RecipeModel(**recipe_data)
        try:
            db.session.add(recipe)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the recipe.")
        return {
            "message": "Recipe created successfully.",
            "recipe": recipe
        }
