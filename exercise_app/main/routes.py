from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from datetime import date, datetime
from exercise_app.models import Category, Exercise, User
from exercise_app.main.forms import ExerciseForm, CategoryForm
from exercise_app import bcrypt
from exercise_app import app, db

main = Blueprint('main', __name__)

# Routes

@main.route('/')
def homepage():
    all_categories = Category.query.all()
    all_exercises = Exercise.query.all()

    return render_template('homepage.html', all_categories=all_categories, all_exercises=all_exercises)

@main.route('/create_category', methods=['POST', 'GET'])
def create_category():
    form = CategoryForm()

    if form.validate_on_submit():
        new_category = Category(
            name = form.name.data
        )
        db.session.add(new_category)
        db.session.commit()

        flash('New category was added')
        return redirect(url_for('main.category_detail', category_id=new_category.id))
    return render_template('/create_category.html', form=form)

@main.route('/category/<category_id>', methods=['POST', 'GET'])
def category_detail(category_id):
    category = Category.query.filter_by(id=category_id).one()
    form = CategoryForm(obj=category)

    if form.validate_on_submit():
        category.name = form.name.data

        db.session.commit()
        flash('Category name updated')
        return redirect(url_for('main.category_detail', category_id=category_id))
    return render_template('category_detail.html', category=category, form=form)