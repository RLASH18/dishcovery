from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from authlib.integrations.flask_client import OAuth
from app.config import Config

db = SQLAlchemy()
oauth = OAuth()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    oauth.init_app(app)

    # Import models
    from app.models.user import User

    # Register OAuth providers
    from app.extensions import register_social
    register_social(app)

    # Register routes
    from app.routes.web import register_routes
    register_routes(app)

    return app