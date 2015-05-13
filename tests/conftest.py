import pytest

from blog import create_app
from blog.models import db, User

@pytest.fixture
def testblog(request):
  ''' Creates a test blog fixture to use in testing '''
  app = create_app('blog.configs.TestConfig', env='dev')
  client = app.test_client()

  db.app = app
  db.create_all()

  def teardown():
    db.session.remove()
    db.drop_all()

  request.addfinalizer(teardown)

  return client
