from flask import Flask
from flask_smorest import Api
from db import db
import models
from resources.recipe import blp as RecipeBlueprint
from resources.utils import insert_initial_data
from flask_migrate import Migrate

def create_app(db_url=None):
    app = Flask(__name__)
    app.config["API_TITLE"] = "Stores REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or "sqlite:///data.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["PROPAGATE_EXCEPTIONS"] = True

    db.init_app(app)
    migrate = Migrate(app, db)
    api = Api(app)

    with app.app_context():
        try:
            db.create_all()
            insert_initial_data()
        except Exception as e:
            print(f"Error during table creation or data insertion: {e}")

    api.register_blueprint(RecipeBlueprint)

    return app

app = create_app()
