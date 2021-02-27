from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from exercise_app.models import User, Category, Exercise
from exercise_app import bcrypt
from exercise_app.auth.forms import CreateAccountForm, LoginForm

from exercise_app import app, db

auth = Blueprint('auth', __name__)

# Routes

@auth.route('/signup', methods=['POST', 'GET'])
def signup():
    form = CreateAccountForm()

    if form.validate_on_submit():
        hash_pass = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        new_user = User(
            username = form.username.data,
            password = hash_pass
        )
        db.session.add(new_user)
        db.session.commit()

        flash('Account created successfully')
        return redirect(url_for('auth.login'))
    return render_template('signup.html', form=form)

@auth.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).one()
        login_user(user, remember=True)
        next_page = request.args.get('next')

        if next_page:
            return redirect(next_page)
        else:
            return redirect(url_for('main.homepage'))
    return render_template('login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.homepage'))