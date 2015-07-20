import os
import unittest

from datetime import datetime

from flask import current_app, g
from flask.ext.login import current_user
from flask.ext.sqlalchemy import SQLAlchemy

from blog import create_app
from blog.models import db, User, TextPost

class EssentialsTestCase(unittest.TestCase):
  def setUp(self):
    self.app = create_app('blog.configs.TestConfig', 'test')
    with self.app.app_context():
      db.create_all()
    self.client = self.app.test_client()

  def tearDown(self):
    with self.app.app_context():
      db.session.remove()
      db.drop_all()

  def test_app_exists(self):
    """Check that app was created"""
    self.assertFalse(current_app is None)

  def test_app_is_testing(self):
    """Make sure app is in testing mode"""
    self.assertTrue(current_app.config['TESTING'])
  
  def test_app_config(self):
    """Check app configuration"""
    self.assertEqual(current_app.config['UPLOAD_FOLDER'], 'test_uploads')


if __name__ == '__main__':
  unittest.main()
