"""Module for all global constants to import across the app"""

# Python Third Party Imports
from config import Config

# Local Library Imports
from classxlib.file import merge_directory

# GLOBAL VARIABLES
STATIC_FOLDER = Config.STATIC_FOLDER
IMAGE_FOLDER = Config.IMAGE_FOLDER
FLASK_ENV = Config.FLASK_ENV

# SET ADMIN DIRECTORIES
ADMIN_UPLOAD_FOLDER = IMAGE_FOLDER

# USER UPLOAD FOLDER
USER_UPLOAD_FOLDER = merge_directory(IMAGE_FOLDER, 'user_images')