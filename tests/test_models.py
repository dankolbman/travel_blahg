import pytest
from blog.models import db, User

create_user = False

@pytest.mark.usefixtures("testblog")
class TestModels:
  def test_user_save(self, testblog):
    """ Create and save a user """
    usr = User('Joe', 'abc123')
    db.session.add(usr)
    db.session.commit()

    user = User.query.filter_by(username='Joe').first()
    assert user is not None

  def test_user_password(self, testblog):
    """ Test password hashing and checking """
    usr = User('Joe', 'abc123')

    assert usr.username == 'Joe'
    assert usr.password != 'abc123'
    assert usr.check_password('abc123')
