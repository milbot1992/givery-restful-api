import pytest
from db import db
from models import RecipeModel

def test_post_recipe(client):
    response = client.post("/recipes", json={
        "title": "Chicken Curry",
        "making_time": "45 min",
        "serves": "4 people",
        "ingredients": "onion, chicken, seasoning",
        "cost": 1000
    })
    assert response.status_code == 200
    assert response.json["title"] == "Chicken Curry"

def test_get_all_recipes(client, init_database):
    response = client.get("/recipes")
    assert response.status_code == 200
    assert len(response.json) == 2

def test_get_recipe(client, init_database):
    response = client.get("/recipes/1")
    assert response.status_code == 200
    assert response.json["title"] == "Chicken Curry"

def test_patch_recipe(client, init_database):
    response = client.patch("/recipes/1", json={
        "title": "Spicy Chicken Curry"
    })
    assert response.status_code == 200
    assert response.json["title"] == "Spicy Chicken Curry"

def test_delete_recipe(client, init_database):
    response = client.delete("/recipes/1")
    assert response.status_code == 200
    assert response.json["message"] == "Recipe successfully removed!"
    response = client.get("/recipes/1")
    assert response.status_code == 404
