from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_login import (
    UserMixin,
    login_user,
    LoginManager,
    current_user,
    logout_user,
    login_required,
)
import pymysql



login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = "login"
login_manager.login_message_category = "info"

db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()


def create_app():
    app = Flask(__name__)

    app.secret_key = 'secret-key'
    # app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://hocjseczzxrzkz:11f9f8ae1a833f1bc24c96fadf05b42424665dd8157c2ad9d58d8ccbbb3652c7@ec2-34-231-63-30.compute-1.amazonaws.com:5432/d4hvpctm1e1un4"
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    pymysql.install_as_MySQLdb()
    login_manager.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    
    
    return app
