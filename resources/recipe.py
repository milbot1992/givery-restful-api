from flask.views import MethodView
from flask_smorest import Blueprint
from werkzeug.exceptions import NotFound
from sqlalchemy.orm.exc import NoResultFound

from db import db
from models import RecipeModel
from schemas import RecipeSchema, RecipeUpdateSchema, RecipeResponseSchema, RecipeListResponseSchema, RecipePostResponseSchema

blp = Blueprint("Recipes", "recipes", description="Operations on recipes")

@blp.route("/recipes/<int:recipe_id>")
class Recipe(MethodView):
    @blp.response(200, RecipeResponseSchema)
    def get(self, recipe_id):
        """
        Retrieve a recipe by its ID.
        If the recipe is found, return its details.
        """
        recipe = RecipeModel.query.get_or_404(recipe_id)
        return {
            "message": "Recipe details by id",
            "recipe": [recipe]
        }

    @blp.response(200, RecipeResponseSchema)
    def delete(self, recipe_id):
        """
        Delete a recipe by its ID.
        If the recipe is not found, return an error message.
        """
        try:
            recipe = RecipeModel.query.get_or_404(recipe_id)
        except NotFound:
            return {"message": "No recipe found"}, 400
        db.session.delete(recipe)
        db.session.commit()
        return {"message": "Recipe successfully removed!"}, 200

    @blp.arguments(RecipeUpdateSchema)
    @blp.response(200, RecipeResponseSchema)
    def patch(self, recipe_data, recipe_id):
        """
        Update an existing recipe by its ID with the provided data.
        If the recipe is not found, an error message is returned.
        """
        print("recipe id:", recipe_id)
        try:
            recipe = RecipeModel.query.filter_by(id=recipe_id).one()
        except NoResultFound:
            return {"message": "No recipe found with the provided ID"}, 400
        
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
        """
        Retrieve all recipes.
        Return a list of all recipes in the database.
        """
        recipes = RecipeModel.query.all()
        return {
            "recipes": recipes
        }

    @blp.arguments(RecipeSchema)
    @blp.response(200, RecipePostResponseSchema)
    def post(self, recipe_data):
        """
        Create a new recipe with the provided data.
        Return a success message if the recipe is created successfully.
        """
        recipe = RecipeModel(**recipe_data)
        db.session.add(recipe)
        db.session.commit()
        return {
            "message": "Recipe successfully created!",
            "recipe": [recipe]
        }

@blp.errorhandler(422)
def recipe_post_error(e):
    """
    Handle validation errors for recipe creation.
    Return a custom error message with required fields.
    """
    return {
        "message": "Recipe creation failed!",
        "required": "title, making_time, serves, ingredients, cost"
    }, 400