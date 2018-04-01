import os


class Config(object):
  APP_NAME = 'Blog'
  SECRET_KEY = 'G00DB33F'
  ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

  LARGE_IMAGE = '968'
  MED_IMAGE = '512'
  SMALL_IMAGE = '128'

  PG_HOST = os.environ.get('PG_HOST', 'localhost')
  PG_PORT = os.environ.get('PG_PORT', 5432)
  PG_NAME = os.environ.get('PG_NAME', 'dev')
  PG_USER = os.environ.get('PG_USER', 'postgres')
  PG_PASS = os.environ.get('PG_PASS', 'pass')
  SQLALCHEMY_DATABASE_URI = 'postgres://{}:{}@{}:{}/{}'.format(
                                PG_USER, PG_PASS, PG_HOST, PG_PORT, PG_NAME)

class ProdConfig(Config):
  DEBUG = False
  TESTING = False


  UPLOAD_FOLDER = 'uploads'
  CACHE_TYPE = 'simple'

class DevConfig(Config):
  DEBUG = True
  DEBUG_TB_INTERCEPT_REDIRECTS = False
  TESTING = False
  UPLOAD_FOLDER = 'dev_uploads'

  #SQLALCHEMY_DATABASE_URI = 'sqlite:///../dev_database.db'
  SQLALCHEMY_DATABASE_URI = "postgresql:///blog_dev"

  CACHE_TYPE = 'null'

class TestConfig(Config):
  DEBUG = False
  DEBUG_TB_INTERCEPT_REDIRECTS = False
  TESTING = True
  UPLOAD_FOLDER = 'test_uploads'

  import tempfile
  db_file = tempfile.NamedTemporaryFile()
  SQLALCHEMY_DATABASE_URI = 'postgresql:///blog_test'
  #SQLALCHEMY_ECHO = True

  CACHE_TYPE = 'null'
  WTF_CSRF_ENABLED = False

