from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()

def create_app(config_class=Config):
    """Factory per creare l'applicazione Flask"""
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)

    # Importa le routes e registrale sull'app
    from app import routes
    routes.register_routes(app)

    with app.app_context():
        from app import models
        db.create_all()

    return app
