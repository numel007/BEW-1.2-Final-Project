from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField, SelectField, SubmitField, TextAreaField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Length, ValidationError
from exercise_app.models import Category, Exercise

class ExerciseForm(FlaskForm):
    '''Exercise creation form'''
    name = StringField('Exercise Name', validators=[DataRequired(), Length(min=1, max=100)])
    description = StringField('Brief Description', validators=[DataRequired(), Length(min=1, max=300)])
    category = QuerySelectField('Category', query_factory=lambda: Category.query, allow_blank=False)
    submit = SubmitField('Submit')

class CategoryForm(FlaskForm):
    '''Category creation form'''
    name = StringField('Category Name', validators=[DataRequired(), Length(min=1, max=100)])
    submit = SubmitField('Submit')