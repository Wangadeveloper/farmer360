from flask import Flask,render_template
from app.extensions import db, bcrypt, login_manager
import os

from dotenv import load_dotenv
load_dotenv()


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object("config.Config")

    # Ensure upload folder exists
    os.makedirs(app.config.get("UPLOAD_FOLDER", "uploads"), exist_ok=True)

    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    # Register blueprints
    from app.blueprints.auth import auth_bp
    from app.blueprints.disease import disease_bp
    from app.blueprints.records import records_bp
    from app.blueprints.finance import finance_bp
    from app.blueprints.chemicals import chemicals_bp
    from app.blueprints.stories import stories_bp

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(disease_bp, url_prefix="/disease")
    app.register_blueprint(records_bp, url_prefix="/records")
    app.register_blueprint(finance_bp, url_prefix="/finance")
    app.register_blueprint(chemicals_bp, url_prefix="/chemicals")
    app.register_blueprint(stories_bp, url_prefix="/stories")

    # Import models so they’re registered before db.create_all()
    from app import models  

    with app.app_context():
        db.create_all()

    @login_manager.user_loader
    def load_user(user_id):
        from app.models import User
        return User.query.get(int(user_id))
    
    @app.route("/")
    def home():
        return render_template("home.html")

    return app
