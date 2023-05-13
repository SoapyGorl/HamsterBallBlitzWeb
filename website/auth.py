from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('UserName')
        password = request.form.get('password')
        user = User.query.filter_by(username = username).first()
        if user:
            if check_password_hash(user.password, password):
                flash('You are logged in', category = 'success')
                login_user(user, remember = True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password', category = 'error')
        else:
            flash('Username does not exist', category = 'error')
    return render_template("login.html", user = current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out')
    return redirect(url_for('views.home'))

@auth.route('/sign-up', methods = ['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        username = request.form.get('UserName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        user = User.query.filter_by(username = username).first()
        if user:
            flash('Username already exists', category = 'error')
        elif password1 != password2:
            flash('Passwords did not match', category = 'error')
        elif len(username) >= 150:
            flash('Username is too long', category = 'error')
        elif len(password1) >= 150:
            flash('Password is too long', category = 'error')
        else:
            new_user = User(username = username, password = generate_password_hash(password1, method = 'scrypt'))
            db.session.add(new_user)
            db.session.commit()
            flash('Account created!', category = 'success')
            user = User.query.filter_by(username = username).first()
            login_user(user, remember = True)
            return redirect(url_for('views.home'))
    return render_template("sign_up.html", user = current_user)