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
    exercises_in_cat = category.exercises
    form = CategoryForm(obj=category)

    if form.validate_on_submit():
        category.name = form.name.data

        db.session.commit()
        flash('Category name updated')
        return redirect(url_for('main.category_detail', category_id=category_id))
    return render_template('category_detail.html', category=category, form=form, exercises=exercises_in_cat)

@main.route('/create_exercise', methods=['POST', 'GET'])
def create_exercise():
    form = ExerciseForm()

    if form.validate_on_submit():
        new_exercise = Exercise(
            name = form.name.data,
            description = form.description.data,
            category = form.category.data
        )
        db.session.add(new_exercise)
        db.session.commit()

        flash('New exercise added')
        return redirect(url_for('main.exercise_detail', exercise_id=new_exercise.id))
    return render_template('create_exercise.html', form=form)

@main.route('/exercise/<exercise_id>', methods=['POST', 'GET'])
def exercise_detail(exercise_id):
    exercise = Exercise.query.filter_by(id=exercise_id).one()
    form = ExerciseForm(obj=exercise)

    if form.validate_on_submit():
        exercise.name = form.name.data
        exercise.description = form.description.data
        exercise.category = form.category.data

        db.session.commit()
        flash('Exercise updated')
        return redirect(url_for('main.exercise_detail', exercise_id=exercise_id))
    return render_template('exercise_detail.html', exercise=exercise, form=form)

@main.route('/profile/<username>')
@login_required
def profile(username):
    user = User.query.filter_by(username=username).one()
    return render_template('profile.html', user=user)

@main.route('/favorite/<exercise_id>', methods=['POST'])
def favorite(exercise_id):
    exercise = Exercise.query.filter_by(id=exercise_id).one()
    if exercise in current_user.favorite_exercises:
        flash(f'{exercise.name} already in your favorites.')
    else:
        current_user.favorite_exercises.append(exercise)
        db.session.add(current_user)
        db.session.commit()
        flash(f'{exercise.name} added to your favorites.')
    return redirect(url_for('main.exercise_detail', exercise_id=exercise_id))

@main.route('/unfavorite/<exercise_id>', methods=['POST'])
def unfavorite(exercise_id):
    exercise = Exercise.query.filter_by(id=exercise_id).one()
    if exercise not in current_user.favorite_exercises:
        flash(f'{exercise.name} not in your favorites. Add it first.')
    else:
        current_user.favorite_exercises.remove(exercise)
        db.session.add(current_user)
        db.session.commit()
        flash(f'{exercise.name} removed from your favorites.')
    return redirect(url_for('main.exercise_detail', exercise_id=exercise_id))