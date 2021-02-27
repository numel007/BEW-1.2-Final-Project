from exercise_app import db
from sqlalchemy.orm import backref
from flask_login import UserMixin

class Exercise(db.Model):
    '''Exercise model'''
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80), nullable = False)
    description = db.Column(db.String(300), nullable = False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable = False)
    category = db.relationship('Category', back_populates='exercises')
    favorited_by = db.relationship('User', secondary='favorite_exercises_table', back_populates='favorite_exercises')

    def __str__(self):
        return f'{self.name}'

class Category(db.Model):
    '''Category model'''
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80), nullable = False)
    exercises = db.relationship('Exercise', back_populates='category')

    def __str__(self):
        return f'{self.name}'

class User(UserMixin, db.Model):
    '''User model'''
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    favorite_exercises = db.relationship('Exercise', secondary='favorite_exercises_table', back_populates='favorited_by')

    def __str__(self):
        return f'{self.username}'
        
favorite_user_exercises = db.Table('favorite_exercises_table', 
    db.Column('exercise_id', db.Integer, db.ForeignKey('exercise.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
)