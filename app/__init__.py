from flask import Flask

from app.database import init_db
from app.routes import register_routes
from config import Config


def create_app(test_config=None):
    app = Flask(__name__, template_folder="../templates", static_folder="../static")
    app.config.from_object(Config)

    if test_config:
        app.config.update(test_config)

    if app.config.get("DATABASE") == ":memory:":
        app.config["DATABASE_URL"] = ":memory:"

    init_db(app.config["DATABASE_URL"])
    register_routes(app)
    return app
