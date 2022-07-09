from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user


# # # from flask_mysqldb import MySQL
# # # import MySQLdb.cursors
# # # import re

from flask_sqlalchemy import SQLAlchemy

auth = Blueprint('auth', __name__)

# Change this to your secret key (can be anything)
# app.secret_key = 'your secret key'

# # # Enter database connection details below
# # # app.config['MYSQL_HOST'] = 'localhost'
# # # app.config['MYSQL_USER'] = 'root'
# # # app.config['MYSQL_PASSWORD'] = ''
# # # app.config['MYSQL_DB'] = 'loginwebsite'

# Intialize MySQL
# # # mysql = MySQL(app)

# # # @app.route("/",methods=['GET', 'POST'])
# # # def reroute():
# # #     return redirect((url_for('login')))
    
# # # #add routes here
# # # @app.route('/login/', methods=['GET', 'POST'])
# # # def login():
# # #     msg = ''
# # #     if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
# # #         # Create variables for easy access
# # #         username = request.form['username']
# # #         password = request.form['password']
# # #         cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
# # #         cursor.execute('SELECT * FROM user WHERE username = %s AND password = %s', (username, password))
# # #         # Fetch one record and return result
# # #         user = cursor.fetchone()
# # #         if user:
# # #             # Create session data, we can access this data in other routes
# # #             session['loggedin'] = True
# # #             session['username'] = user['username']
# # #             # Redirect to home page
# # #             return redirect(url_for('home'))
# # #         else:
# # #             # Account doesnt exist or username/password incorrect
# # #             msg = 'Incorrect username/password!'
# # #     return render_template('login.html', msg='')

# # # @app.route('/login/signup', methods=['GET', 'POST'])
# # # def signup():
# # #     # Output message if something goes wrong...
# # #     msg = ''
# # #     # Check if "username", "password" and "email" POST requests exist (user submitted form)
# # #     if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
# # #         # Create variables for easy access
# # #         username = request.form['username']
# # #         password = request.form['password']
# # #         email = request.form['email']
# # #         # Check if account exists using MySQL
# # #         cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
# # #         cursor.execute('SELECT * FROM user WHERE username = %s', (username,))
# # #         user = cursor.fetchone()
# # #         # If account exists show error and validation checks
# # #         if user:
# # #             msg = 'Account already exists!'
# # #         elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
# # #             msg = 'Invalid email address!'
# # #         elif not re.match(r'[A-Za-z0-9]+', username):
# # #             msg = 'Username must contain only characters and numbers!'
# # #         elif not username or not password or not email:
# # #             msg = 'Please fill out the form!'
# # #         else:
# # #             # Account doesnt exists and the form data is valid, now insert new account into accounts table
# # #             cursor.execute('INSERT INTO user VALUES (%s, %s, %s)', (username, password, email,))
# # #             mysql.connection.commit()
# # #             msg = 'You have successfully signed up!'
# # #             return redirect(url_for('home'))
# # #     elif request.method == 'POST':
# # #         # Form is empty... (no POST data)
# # #         msg = 'Please fill out the form!'
# # #     # Show registration form with message (if any)
# # #     return render_template('signup.html', msg=msg)

# # # @app.route('/login/logout')
# # # def logout():
# # #     # Remove session data, this will log the user out
# # #    session.pop('loggedin', None)
# # #    session.pop('username', None)
# # #    # Redirect to login page
# # #    return redirect(url_for('login'))

# # # @app.route('/login/home')
# # # def home():
# # #     # Check if user is loggedin
# # #     if 'loggedin' in session:
# # #         # User is loggedin show them the home page
# # #         return render_template('index.html', username=session['username'])
# # #     # User is not loggedin redirect to login page
# # #     return redirect(url_for('login'))

# # # @app.route('/login/profile', methods=['GET'])
# # # def profile():
# # #     # Check if user is loggedin
# # #     if 'loggedin' in session:
# # #         # We need all the account info for the user so we can display it on the profile page
# # #         cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
# # #         cursor.execute('SELECT * FROM user WHERE username = %s', (session['username'],))
# # #         user = cursor.fetchone()
# # #         # Show the profile page with account info
# # #         return render_template('profile.html', user=user)
# # #     # User is not loggedin redirect to login page
# # #     return redirect(url_for('login'))


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                msg = 'Incorrect Credentials, try again.'
                return render_template("login.html", user=current_user, msg = msg)
        else:
            msg = 'Incorrect Credentials, try again.'
            return render_template("login.html", user=current_user, msg = msg)

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    msg = ''
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            msg = 'Email already exists.'
            return render_template("signup.html", user=current_user, msg = msg)
        elif len(username) < 2:
            msg = 'First name must be greater than 1 character.'
            return render_template("signup.html", user=current_user, msg = msg)
        elif len(password) < 8:
            msg = 'Password must be at least 8 characters.'
            return render_template("signup.html", user=current_user, msg = msg)
        else:
            new_user = User(email=email, username=username, password=generate_password_hash(
                password, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            return redirect(url_for('views.home'))

    return render_template("signup.html", user=current_user)

