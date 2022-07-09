from flask import Blueprint, redirect, render_template, url_for
from flask_login import login_required, current_user
from . import db

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def load():
    return redirect(url_for('views.home'))

@views.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    return render_template("index.html", username=current_user.username)

@views.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    return render_template("profile.html")



