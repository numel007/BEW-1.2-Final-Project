import os
import unittest
from exercise_app import app, db, bcrypt
from exercise_app.models import Exercise, Category, User

def create_user():
    '''Create user. username=test_user, password=securepassword'''

    new_user = User(username='test_user', password=bcrypt.generate_password_hash('securepassword').decode('utf-8'))
    db.session.add(new_user)
    db.session.commit()

def login(client, username, password):

    post_data={
        'username' : username,
        'password' : password
    }

    return client.post('/login', data=post_data, follow_redirects=True)

def logout(client):

    return client.get('/logout', follow_redirects=True)

def create_category():
    '''Create category with name arms'''

    new_cat = Category(name='Arms')
    db.session.add(new_cat)
    db.session.commit()

def create_exercise():
    """Name: bicep curls, Description: 'Every day is arm day', Category: 'Arms'"""

    create_category()
    category = Category.query.filter_by(name='Arms').one()
    new_exer = Exercise(name='bicep curls', description='Every day is arm day.', category=category)
    db.session.add(new_exer)
    db.session.commit()

# Tests

class MainTests(unittest.TestCase):

    def setUp(self):

        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        db.drop_all()
        db.create_all()

    def test_create_category(self):

        create_user()
        login(self.app, 'test_user', 'securepassword')

        post_data = {
            'name' : 'Rear Deltoids'
        }
        self.app.post('/create_category', data=post_data)

        new_cat = Category.query.filter_by(name='Rear Deltoids').one()
        self.assertIsNotNone(new_cat)
        self.assertEqual(new_cat.name, 'Rear Deltoids')

    def test_create_exercise(self):

        create_user()
        login(self.app, 'test_user', 'securepassword')
        create_category()

        arms_cat = Category.query.filter_by(name='Arms').one()

        post_data = {
            'name' : 'wrist curls',
            'description' : 'Curls for the wrists',
            'category' : arms_cat.id
        }
        self.app.post('/create_exercise', data=post_data)

        new_exer = Exercise.query.filter_by(name='wrist curls').one()

        # arms_cat is expired after commit, re-query it for comparison
        arms_cat = Category.query.filter_by(name='Arms').one()

        self.assertIsNotNone(new_exer)
        self.assertEqual(new_exer.name, 'wrist curls')
        self.assertEqual(new_exer.description, 'Curls for the wrists')
        self.assertEqual(new_exer.category.name, arms_cat.name)

    def test_create_user(self):

        post_data = {
            'username' : 'exotic_muffins',
            'password' : 'buygme'
        }
        self.app.post('/signup', data=post_data)

        new_user = User.query.filter_by(username='exotic_muffins').one()

        self.assertIsNotNone(new_user)

    def test_login_user(self):

        create_user()

        post_data = {
            'username' : 'test_user',
            'password' : 'securepassword'
        }
        page = self.app.post('/login', data=post_data, follow_redirects=True)
        page_content = page.get_data(as_text=True)
        self.assertIn('test_user', page_content)

    def test_invalid_login(self):

        create_user()

        post_data = {
            'username' : 'test_user2',
            'password' : 'securepassword'
        }
        page = self.app.post('/login', data=post_data, follow_redirects=True)
        page_content = page.get_data(as_text=True)
        self.assertIn('error', page_content)

    def test_favorite_exercise(self):

        create_user()
        login(self.app, 'test_user', 'securepassword')

        create_exercise()

        post_data = {
            'favorite_exercises' : 1
        }
        self.app.post('/favorite/1', data=post_data)
        user = User.query.filter_by(username='test_user').one()

        self.assertIsNotNone(user.favorite_exercises)
        self.assertEqual(user.favorite_exercises[0].name, 'bicep curls')

    def test_logout_user(self):

        create_user()
        login(self.app, 'test_user', 'securepassword')
        page = logout(self.app)

        page_content = page.get_data(as_text=True)
        self.assertNotIn('test_user', page_content)