from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
import psycopg2

db = SQLAlchemy()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'some-secret-key'
connection = psycopg2.connect(user="helmascaqbnjcy",
                                  password="d58ede02612842cf7f5f92ea352840187b8fe1217c2fffdae9b6acd7305a552b",
                                  host="ec2-34-233-115-14.compute-1.amazonaws.com",
                                  port="5432",
                                  database="dfumocahrfo52p")
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

with app.app_context():
    db.create_all()

if __name__ == "__main__":
        app.run()