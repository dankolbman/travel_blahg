from blog import create_app

class TestConfig:
  def test_prod_config(self):
    ''' Tests production config '''
    app = create_app('blog.configs.ProdConfig', env='prod')

    assert app.config['CACHE_TYPE'] == 'simple'

  def test_dev_config(self):
    ''' Tests development config '''
    app = create_app('blog.configs.DevConfig', env='dev')

    assert app.config['DEBUG'] is True
    assert app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] is False
    assert app.config['SQLALCHEMY_DATABASE_URI'] == 'sqlite:///../dev_database.db'
    assert app.config['CACHE_TYPE'] == 'null'

  def test_test_config(self):
    ''' Tests test config '''
    app = create_app('blog.configs.TestConfig', env='dev')

    assert app.config['DEBUG'] is True
    assert app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] is False
    assert app.config['SQLALCHEMY_ECHO'] is True
    assert app.config['CACHE_TYPE'] == 'null'
    assert app.config['WTF_CSRF_ENABLED'] is False

