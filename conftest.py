import pytest
from app import create_app
from db import db
from models import RecipeModel
from datetime import datetime

@pytest.fixture(scope='module')
def app():
    app = create_app()
    app.config.from_object("test_config")
    
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture(scope='module')
def client(app):
    return app.test_client()

@pytest.fixture(scope='function')
def init_database(app):
    with app.app_context():
        db.drop_all()
        db.create_all()
        recipe1 = RecipeModel(
            id=1, title="Chicken Curry", making_time="45 min", serves="4 people", ingredients="onion, chicken, seasoning", cost=1000, created_at=datetime.strptime("2016-01-10 12:10:12", "%Y-%m-%d %H:%M:%S"), updated_at=datetime.strptime("2016-01-10 12:10:12", "%Y-%m-%d %H:%M:%S")
        )
        recipe2 = RecipeModel(
            id=2, title="Rice Omelette", making_time="30 min", serves="2 people", ingredients="onion, egg, seasoning, soy sauce", cost=700, created_at=datetime.strptime("2016-01-11 13:10:12", "%Y-%m-%d %H:%M:%S"), updated_at=datetime.strptime("2016-01-11 13:10:12", "%Y-%m-%d %H:%M:%S")
        )
        db.session.add(recipe1)
        db.session.add(recipe2)
        db.session.commit()
        yield db
        db.session.remove()
        db.drop_all()
