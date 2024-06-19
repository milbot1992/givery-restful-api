from db import db
from models import RecipeModel
from datetime import datetime

def insert_initial_data():
    # Check if there are any existing recipes
    if RecipeModel.query.count() > 0:
        return

    recipes = [
        {
            "id": 1,
            "title": "Chicken Curry",
            "making_time": "45 min",
            "serves": "4 people",
            "ingredients": "onion, chicken, seasoning",
            "cost": 1000,
            "created_at": datetime.strptime("2016-01-10 12:10:12", "%Y-%m-%d %H:%M:%S"),
            "updated_at": datetime.strptime("2016-01-10 12:10:12", "%Y-%m-%d %H:%M:%S"),
        },
        {
            "id": 2,
            "title": "Rice Omelette",
            "making_time": "30 min",
            "serves": "2 people",
            "ingredients": "onion, egg, seasoning, soy sauce",
            "cost": 700,
            "created_at": datetime.strptime("2016-01-11 13:10:12", "%Y-%m-%d %H:%M:%S"),
            "updated_at": datetime.strptime("2016-01-11 13:10:12", "%Y-%m-%d %H:%M:%S"),
        },
    ]

    for recipe_data in recipes:
        recipe = RecipeModel(**recipe_data)
        db.session.add(recipe)
    
    db.session.commit()
