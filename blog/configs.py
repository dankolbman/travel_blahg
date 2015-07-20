class Config(object):
  APP_NAME = 'Blog'
  SECRET_KEY = 'G00DB33F'
  ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

  LARGE_IMAGE = '968'
  MED_IMAGE = '512'
  SMALL_IMAGE = '128'


class ProdConfig(Config):
  DEBUG = False
  TEST = False
  SQLALCHEMY_DATABASE_URI = "postgresql:///blog"

  UPLOAD_FOLDER = 'uploads'
  CACHE_TYPE = 'simple'

class DevConfig(Config):
  DEBUG = True
  DEBUG_TB_INTERCEPT_REDIRECTS = False
  TEST = False
  UPLOAD_FOLDER = 'dev_uploads'

  #SQLALCHEMY_DATABASE_URI = 'sqlite:///../dev_database.db'
  SQLALCHEMY_DATABASE_URI = "postgresql:///blog_dev"

  CACHE_TYPE = 'null'

class TestConfig(Config):
  DEBUG = False
  DEBUG_TB_INTERCEPT_REDIRECTS = False
  TEST = True
  UPLOAD_FOLDER = 'test_uploads'

  import tempfile
  db_file = tempfile.NamedTemporaryFile()
  SQLALCHEMY_DATABASE_URI = 'postgresql:///blog_test'
  #SQLALCHEMY_ECHO = True

  CACHE_TYPE = 'null'
  WTF_CSRF_ENABLED = False

