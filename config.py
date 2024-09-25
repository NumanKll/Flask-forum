from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message = "Lütfen Giriş Yapın"

class Config:
    SECRET_KEY="111111111111"
    SQLALCHEMY_DATABASE_URI = 'sqlite:///db.db'