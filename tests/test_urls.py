import pytest

create_user = True

@pytest.mark.usefixtures("testblog")
class TestURLs:
  def test_home(self, testblog):
    """ Tests if the home page loads """
    rv = testblog.get('/')
    assert rv.status_code == 200

  def test_login(self, testblog):
    """ Tests if the login page loads """
    rv = testblog.get('/login')
    assert rv.status_code == 200

  def test_logout(self, testblog):
    """ Test logout page
      This should redirect us to the index
    """
    rv = testblog.get('/logout')
    assert rv.status_code == 302

