from flask_wtf import Form
from wtforms import TextField, TextAreaField, FloatField, PasswordField, FileField
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

class EditProfileForm(Form):
  username = TextField(u'Username')
  email = TextField(u'Email', validators=[validators.email()])
  password = PasswordField(u'Password', validators=\
            [validators.EqualTo('password2', message='Passwords must match.'),\
            validators.length(6,64)])
  password2 = PasswordField(u'Password Verify')
  api_key = TextField(u'API Key')

  def validate(self):
    check_validate = super(EditProfileForm, self).validate()

    # Make sure the input was clean
    if not check_validate:
      return False

    return True

class CreatePostForm(Form):
  title = TextField(u'Title', validators=[validators.required(), validators.length(max=256)])
  text = TextAreaField(u'Content', validators=[validators.required()])

  latitude = FloatField(u'Latitude', validators=[validators.required()])
  longitude = FloatField(u'Longitude', validators=[validators.required()])

  def validate(self):
    check_validate = super(CreatePostForm, self).validate()

    # Make sure the input was clean
    if not check_validate:
      return False

    return True

class CreateImageForm(Form):
  title = TextField(u'Title', validators=[validators.required(), validators.length(max=256)])
  image = FileField(u'Image', validators=[validators.required()])
  caption = TextAreaField(u'Caption', validators=[validators.required(), validators.length(max=512)])

  latitude = FloatField(u'Latitude')
  longitude = FloatField(u'Longitude')

  def validate(self):
    check_validate = super(CreateImageForm, self).validate()

    # Make sure the input was clean
    if not check_validate:
      return False

    return True
