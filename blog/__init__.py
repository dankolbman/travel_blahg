from flask import Flask
from flaskext.markdown import Markdown

from blog.models import db
from blog.views.main import main
from blog.views.user import user
from blog.views.api import api

from blog.extensions import cache, debug_toolbar, login_manager


def create_app(config, env="prod"):
    """
    Application factory
      config - the config object
      env - name of environment to load
    """

    app = Flask(__name__)

    app.config.from_object(config)
    app.config['ENV'] = env

    # Flask cache init
    cache.init_app(app)

    # Markdown
    md = Markdown(app)

    # initialize the debug tool bar
    debug_toolbar.init_app(app)

    # initialize SQLAlchemy
    db.init_app(app)

    login_manager.init_app(app)

    # register our blueprints
    app.register_blueprint(main)
    app.register_blueprint(user, url_prefix='/user')
    app.register_blueprint(api, url_prefix='/api')

    return app

