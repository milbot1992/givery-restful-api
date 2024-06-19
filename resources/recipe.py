from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import RecipeModel
from schemas import RecipeSchema, RecipeUpdateSchema

blp = Blueprint("Recipes", "recipes", description="Operations on recipes")

@blp.route("/recipes/<int:recipe_id>")
class Recipe(MethodView):
    @blp.response(200, RecipeSchema)
    def get(self, recipe_id):
        recipe = RecipeModel.query.get_or_404(recipe_id)
        return recipe

    def delete(self, recipe_id):
        recipe = RecipeModel.query.get_or_404(recipe_id)
        db.session.delete(recipe)
        db.session.commit()
        return {"message": "Recipe deleted."}, 200

    @blp.arguments(RecipeUpdateSchema)
    @blp.response(200, RecipeSchema)
    def patch(self, recipe_data, recipe_id):
        recipe = RecipeModel.query.get_or_404(recipe_id)
        
        for key, value in recipe_data.items():
            setattr(recipe, key, value)

        db.session.commit()
        return recipe

@blp.route("/recipes")
class RecipeList(MethodView):
    @blp.response(200, RecipeSchema(many=True))
    def get(self):
        return RecipeModel.query.all()

    @blp.arguments(RecipeSchema)
    @blp.response(201, RecipeSchema)
    def post(self, recipe_data):
        recipe = RecipeModel(**recipe_data)
        try:
            db.session.add(recipe)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the recipe.")
        return recipe
