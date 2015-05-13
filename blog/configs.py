class Config(object):
  SECRET_KEY = 'G00DB33F'

class ProdConfig(Config):
  SQLALCHEMY_DATABASE_URI = 'sqlite:///../database.db'

  CACHE_TYPE = 'simple'

class DevConfig(Config):
  DEBUG = True
  DEBUG_TB_INTERCEPT_REDIRECTS = False

  SQLALCHEMY_DATABASE_URI = 'sqlite:///../dev_database.db'

  CACHE_TYPE = 'null'

class TestConfig(Config):
  DEBUG = True
  DEBUG_TB_INTERCEPT_REDIRECTS = False

  import tempfile
  db_file = tempfile.NamedTemporaryFile()
  SQLALCHEMY_DATABASE_URI = 'sqlite:///' + db_file.name
  SQLALCHEMY_ECHO = True

  CACHE_TYPE = 'null'
  WTF_CSRF_ENABLED = False

