from flask_wtf import Form
from wtforms import TextField, PasswordField
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
