# app/__init__.py

from flask import Flask
from flask_mail import Mail
from dotenv import load_dotenv
import os

# Load dotenv variables
load_dotenv()

# Flask-Mail instance
mail = Mail()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    
    # Flask-Mail configuration
    app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
    app.config['MAIL_PORT'] = os.getenv('MAIL_PORT')
    app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS') == 'True'
    app.config['MAIL_USE_SSL'] = os.getenv('MAIL_USE_SSL') == 'True'
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
    app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')

    # Initialize Flask-Mail
    mail.init_app(app)
    
    # Register Blueprints
    from app.routes.main import main_bp
    from app.routes.abbybot_privileges import abbybot_privileges_bp
    from app.routes.wishlist import wishlist_bp
    from app.routes.wip import wip_bp
    from app.routes.dashboard import dashboard_bp
    from app.routes.socials import socials_bp
    from app.routes.status import status_bp
    from app.routes.status_data import status_data_bp
    from app.routes.bot_policies import bot_policies_bp
    from app.routes.user_responsibilities import user_responsibilities_bp

    from app.routes.handlers.error_handlers import error_handlers_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(abbybot_privileges_bp)
    app.register_blueprint(wishlist_bp)
    app.register_blueprint(wip_bp)
    app.register_blueprint(error_handlers_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(socials_bp)
    app.register_blueprint(status_bp)
    app.register_blueprint(status_data_bp)
    app.register_blueprint(bot_policies_bp)
    app.register_blueprint(user_responsibilities_bp)
    
    return app
