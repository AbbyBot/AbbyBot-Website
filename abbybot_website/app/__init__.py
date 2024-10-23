# app/__init__.py

from flask import Flask
from app.routes.main import main_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    
    # Register Blueprints
    app.register_blueprint(main_bp)
    
    return app
