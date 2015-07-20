import os

COV = None
if os.environ.get('FLASK_COVERAGE'):
  import coverage
  COV = coverage.coverage(branch=True, include='app/*')
  COV.start()

from flask.ext.script import Manager, Server
from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.script.commands import ShowUrls, Clean

from blog import create_app
from blog.models import db, User

# Try to load an environment, or default to a development config
env = os.environ.get('BLOG_ENV', 'dev')
# Load the settings
app = create_app('blog.configs.{0}Config'.format( env.capitalize()), env=env)
print('Using config {0}'.format(env))

migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command("server", Server())
manager.add_command("show-urls", ShowUrls())
manager.add_command("clean", Clean())
manager.add_command('db', MigrateCommand)

@manager.command
def createuser(name, password, email):
  if User.query.filter_by(username=name).first() != None:
    print('User with name', name, 'already exists!')
    return
  user = User(name, password, email)
  db.session.add(user)
  db.session.commit()
  print('Added user', user.username)

@manager.command
def createdb():
  """ Initialize a db from models """
  db.create_all()

@manager.command
def test(coverage=False):
  """Run the unit tests."""
  import unittest
  tests = unittest.TestLoader().discover('tests')
  unittest.TextTestRunner(verbosity=2).run(tests)
  if COV:
    COV.stop()
    COV.save()
    print('Coverage Summary:')
    COV.report()
    basedir = os.path.abspath(os.path.dirname(__file__))
    covdir = os.path.join(basedir, 'tmp/coverage')
    COV.html_report(directory=covdir)
    print('HTML version: file://%s/index.html' % covdir)
    COV.erase()

if __name__ == "__main__":
  manager.run()

