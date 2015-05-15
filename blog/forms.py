from flask_wtf import Form
from wtforms import TextField, TextAreaField, FloatField, PasswordField
from wtforms import validators

from .models import User

class LoginForm(Form):
  username = TextField(u'Username', validators=[validators.required()])
  password = PasswordField(u'Password', validators=[validators.required()])

  def validate(self):
    check_validate = super(LoginForm, self).validate()

    # Make sure the input was clean
    if not check_validate:
      return False

    user = User.query.filter_by(username=self.username.data).first()
    if not user:
      self.username.errors.append('Invalid username or password')
      return False
    elif not user.check_password(self.password.data):
      self.username.errors.append('Invalid username or password')
      return False
    return True

class CreatePostForm(Form):
  title = TextField(u'Title', validators=[validators.required(), validators.length(max=256)])
  body = TextAreaField(u'Content', validators=[validators.required()])

  latitude = FloatField(u'Latitude')
  longitude = FloatField(u'Longitude')

  def validate(self):
    check_validate = super(CreatePostForm, self).validate()

    # Make sure the input was clean
    if not check_validate:
      return False

    return True
