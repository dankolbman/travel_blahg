import os

from flask.ext.script import Manager, Server
from flask.ext.script.commands import ShowUrls, Clean

from blog import create_app
from blog.models import db, User

# Try to load an environment, or default to a development config
env = os.environ.get('BLOG_ENV', 'dev')
# Load the settings
app = create_app('blog.configs.{0}Config'.format( env.capitalize()), env=env)

manager = Manager(app)
manager.add_command("server", Server())
manager.add_command("show-urls", ShowUrls())
manager.add_command("clean", Clean())


@manager.command
def createuser(name, password):
  if User.query.filter_by(username=name).first() != None:
    print('User with name', name, 'already exists!')
    return
  user = User(name, password)
  db.session.add(user)
  db.session.commit()
  print('Added user', user.username)

@manager.command
def createdb():
  """ Initialize a db from models """
  db.create_all()

if __name__ == "__main__":
  manager.run()

