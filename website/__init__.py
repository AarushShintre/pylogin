from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

DB_NAME = "database.db"

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'some-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://helmascaqbnjcy:d58ede02612842cf7f5f92ea352840187b8fe1217c2fffdae9b6acd7305a552b@ec2-34-233-115-14.compute-1.amazonaws.com:5432/dfumocahrfo52p'
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


