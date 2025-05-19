# flaskr/__init__.py

# Python Standard Library Imports
import os

# Python Third Party Imports
from celery import Celery
# This has to be created here to avoid circular imports
celery = Celery('tasks', broker=os.environ.get('CELERY_REDIS_URL'))
from flask import Flask
from flask_session import Session

# Local Library Imports
from . import database
from . import oauth
from .public import PUBLIC
from .auth import AUTH
from .dashboard import DASHBOARD
from .research_field import RESEARCH_FIELD
from .original_image import ORIGINAL_IMAGE
from .crop_image import CROP_IMAGE
from .segment_image import SEGMENT_IMAGE
from .label import LABEL
from .user import USER
from .error import ERROR

from classxlib.database import DatabaseService


def create_app():
    # create and configure the app
    app = Flask(__name__,
                template_folder='../templates',
                static_folder='../static')
    app.config.from_object('config.Config')

    app.jinja_env.autoescape = False

    app.jinja_env.globals['WEBSITE_NAME'] = app.config['WEBSITE_NAME']
    app.jinja_env.globals['WEBSITE_EMAIL'] = app.config['WEBSITE_EMAIL']
    app.jinja_env.globals['WEBSITE_LOGO'] = app.config['WEBSITE_LOGO']
    app.jinja_env.globals['HOMEPAGE_ABOUT'] = app.config['HOMEPAGE_ABOUT']
    
    # App session setup
    app_session = Session()
    app_session.init_app(app)
    app.database_service = DatabaseService(app.config['SQLALCHEMY_DATABASE_URI'])

    # Initializing the database
    database.init_app(app)

    # Initalizing the OAuth App
    oauth.init_app(app)

    # Registering the Blueprint APIs
    app.register_blueprint(PUBLIC)
    app.register_blueprint(AUTH)
    app.register_blueprint(DASHBOARD)
    app.register_blueprint(RESEARCH_FIELD)
    app.register_blueprint(ORIGINAL_IMAGE)
    app.register_blueprint(CROP_IMAGE)
    app.register_blueprint(SEGMENT_IMAGE)
    app.register_blueprint(LABEL)
    app.register_blueprint(USER)
    app.register_blueprint(ERROR)

    return app
