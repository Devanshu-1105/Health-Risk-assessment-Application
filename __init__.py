from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'login' #type:ignore
login_manager.login_message_category ='info'

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "12345"
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///health_app.db'
    
    
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    
    from routes import main  # type: ignore
    app.register_blueprint(main)
  