from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()

# Redirect users to login if not authenticated
login_manager.login_view = "auth.login"
login_manager.login_message_category = "info"
