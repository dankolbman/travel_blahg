from datetime import datetime

from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import UserMixin, AnonymousUserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model, UserMixin):
  __tablename__ = "user"
  id = db.Column(db.Integer(), primary_key=True)
  username = db.Column(db.String(32))
  password = db.Column(db.String())
  email = db.Column(db.String())

  submitted = db.relationship('Post', backref='author', lazy='dynamic')

  def __init__(self, username, password, email):
    self.username = username
    self.email = email
    self.set_password(password)

  def set_password(self, password):
    self.password = generate_password_hash(password)

  def check_password(self, value):
    return check_password_hash(self.password, value)

  def is_authenticated(self):
    if isinstance(self, AnonymousUserMixin):
        return False
    else:
        return True

  def is_active(self):
    return True

  def is_anonymous(self):
    if isinstance(self, AnonymousUserMixin):
        return True
    else:
        return False

  def get_id(self):
    return self.id

  def __repr__(self):
    return '<User %r>' % self.username

class Post(db.Model):
  """ A post containing location data """
  __tablename__ = "post"
  id = db.Column(db.Integer, primary_key=True)
  post_type = db.Column(db.String(32), nullable=False)
  title = db.Column(db.String(256), nullable=False)
  timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow(), nullable=False)
  latitude = db.Column(db.Float, default=43.165556, nullable=False)
  longitude = db.Column(db.Float, default=-77.611389, nullable=False)
  author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
  __mapper_args__ = {'polymorphic_on': post_type }

  def get_id(self):
    return self.id

  def get_location(self):
    return self.latitude, self.longitude

  def __repr__(self):
    return '<Post {0}>'.format(self.title)

class TextPost(Post):
  """ A blog post """
  __mapper_args__ = {'polymorphic_identity': 'text'}
  text = db.Column(db.Text)

class ImagePost(Post):
  """ An image post """
  __mapper_args__ = {'polymorphic_identity': 'image'}
  image_path = db.Column(db.Text)
  caption = db.Column(db.String(512))
