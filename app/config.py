"""Flask configuration."""
from os import environ, path
from dotenv import load_dotenv
from datetime import timedelta
from sys import platform


basedir = path.abspath(path.dirname(__file__))
if platform.startswith('dar'):
    load_dotenv(path.join(basedir, 'mac.env'))
else:
    load_dotenv(path.join(basedir, '.env'))

load_dotenv()

__all__ = ['Config']

class Config:
    """Set Flask config variables."""

    FLASK_ENV = environ.get('FLASK_ENV')
    SECRET_KEY = environ.get('SECRET_KEY')
    WEBSITE_NAME = environ.get("WEBSITE_NAME")
    WEBSITE_EMAIL = environ.get("WEBSITE_EMAIL")
    WEBSITE_LOGO = environ.get("WEBSITE_LOGO")
    HOMEPAGE_ABOUT = environ.get("HOMEPAGE_ABOUT")
    
    ALLOWED_EXTENSIONS = {'tif', 'fits', 'png'}
    STATIC_FOLDER = 'static'
    IMAGE_FOLDER = 'static/images'
    TEMPLATES_FOLDER = 'templates'
    ADDRESS = environ.get('ADDRESS')
    DB_PASSWORD = environ.get("DB_PASSWORD")
    MODEL_RETRAIN_SPAN = 4
    # Database
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://'+environ.get('MYSQL_ROOT_USER')+':'+environ.get('MYSQL_ROOT_PASSWORD')+'@'+environ.get('HOST')+':'+environ.get('DB_PORT')+'/'+environ.get('DB')
    # Adding binds
    SQLALCHEMY_BINDS = {
                        'keycloak': 'mysql+pymysql://'+environ.get('MYSQL_ROOT_USER')+':'+environ.get('MYSQL_ROOT_PASSWORD')+'@'+environ.get('HOST')+':'+environ.get('DB_PORT')+'/'+environ.get('OAUTH_DB')
                        }
    JWT_SECRETE_KEY = environ.get('JWT_SECRETE_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_ENGINE_OPTIONS = {
                                 'pool_size' : 10,
                                 'pool_recycle':120,
                                 'pool_pre_ping': True,
                                 'max_overflow': 5
                                 }

    #Session related config
    SESSION_PERMANENT = True
    SESSION_TYPE = "filesystem"
    PERMANENT_SESSION_LIFETIME = timedelta(hours=5)

    #Database gone away fix
    SQLALCHEMY_POOL_PRE_PING =True

    # OAUTH config + DB
    KEYCLOAK_BASE_URL = environ.get('KEYCLOAK_HOST_URL')
    OAUTH2_CLIENT_ID = environ.get('KC_REALM_CLIENT')
    OAUTH2_CLIENT_SECRET = environ.get('OAUTH_SECRET')
    OAUTH2_ISSUER = environ.get('KC_SOURCE_URL') + 'realms/' + environ.get('KC_REALM')
    OAUTH2_META_URL = environ.get('KC_SOURCE_URL') + 'realms/' + environ.get('KC_REALM')+ '/.well-known/openid-configuration'
    SQLALCHEMY_KC_DATABASE_URI = 'mysql+pymysql://'+environ.get('MYSQL_ROOT_USER')+':'+environ.get('MYSQL_ROOT_PASSWORD')+'@'+environ.get('HOST')+':'+environ.get('DB_PORT')+'/'+environ.get('OAUTH_DB')

    if FLASK_ENV == 'production':
        OAUTH2_TOKEN_URL = environ.get('KC_SOURCE_URL') + 'realms/' + environ.get('KC_REALM')+ '/protocol/openid-connect/token'
        OAUTH2_AUTH_URL = environ.get('KC_SOURCE_URL') + 'realms/' + environ.get('KC_REALM')+ '/protocol/openid-connect/auth'
        OAUTH2_REVOKE_URL =  environ.get('KC_SOURCE_URL') + 'realms/' + environ.get('KC_REALM')+ '/protocol/openid-connect/logout?'
    elif FLASK_ENV == 'development':
        OAUTH2_TOKEN_URL = 'http://localhost:8080' + '/realms/' + environ.get('KC_REALM')+ '/protocol/openid-connect/token'
        OAUTH2_AUTH_URL = 'http://localhost:8080' + '/realms/' + environ.get('KC_REALM')+ '/protocol/openid-connect/auth'
        OAUTH2_REVOKE_URL =  'http://localhost:8080' + '/realms/' + environ.get('KC_REALM')+ '/protocol/openid-connect/logout?'

    OAUTH_API_CLIENT = environ.get('ADMIN_CLIENT_ID')
    OAUTH_API_SECRET = environ.get('ADMIN_CLIENT_SECRET')

    CELERY_URL = environ.get('CELERY_REDIS_URL')
