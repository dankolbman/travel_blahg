import os
import unittest

from datetime import datetime

from flask import current_app, g
from flask.ext.login import current_user
from flask.ext.sqlalchemy import SQLAlchemy

from blog import create_app
from blog.models import db, User, TextPost

username = 'John'
password = 'abc123'
email = 'john@test.com'

class TestCase(unittest.TestCase):
  def setUp(self):
    self.app = create_app('blog.configs.TestConfig')
    with self.app.app_context():
      db.create_all()
    self.client = self.app.test_client()

  def tearDown(self):
    with self.app.app_context():
      db.session.remove()
      db.drop_all()

  # Helper functions 
  def login(self, username, password):
    return self.client.post('/login', data=dict(
              username=username,
              password=password
          ), follow_redirects=True)

  def logout(self):
    return self.client.get('/logout', follow_redirects=True)

  def create_user(self, username, password, email):
    u = User(username, password, email)
    with self.app.app_context():
      db.session.add(u)
      db.session.commit()
    

  def test_user(self):
    """ User creation and authentication
    Create new user
    Add to database
    Login and out"""
    # Make a new user
    u = User(username, password, email)
    with self.app.app_context():
      # Add to db
      db.session.add(u)
      db.session.commit()
      # Test queries
      self.assertIsNotNone(User.query.filter_by(username=username).first())
      self.assertIsNotNone(User.query.filter_by(email=email).first())
    # Test password secturity
    self.assertNotEqual(u.password, password)
    self.assertTrue(u.check_password(password))

    # Try an incorrect log in
    rv = self.login(username, 'not_correct')
    self.assertIn(b'Invalid username or password', rv.data)
    # Try correct login
    rv = self.login(username, password)
    # Test if log in was succsessful
    self.assertEqual(rv.status_code, 200)
    self.assertIn(b"logged in", rv.data)

    # Try logout
    rv = self.logout()
    self.assertIn(b'You were logged out', rv.data)

  def test_text_post(self):
    """ Test post creation """
    # Make a user
    self.create_user(username, password, email)
    # Log the user in
    self.login(username, password)
    with self.app.app_context():
      uid = User.query.filter_by(username=username).first().id

    p = TextPost(author_id=uid,
                title='Test Post',
                timestamp=datetime.utcnow(),
                text='Lorem Ipsum Dolor Sit Amet',
                latitude=43.165556,
                longitude=-77.611389,
                loc='POINT({0} {1})'.format(43.165556,-77.611389))
    
    with self.app.app_context():
      db.session.add(p)
      db.session.commit()
      self.assertEqual(User.query.filter_by(username=username).first().submitted.count(),1)

if __name__ == '__main__':
  unittest.main()
