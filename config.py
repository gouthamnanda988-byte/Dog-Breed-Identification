"""
Configuration file for Dog Breed Identification Project
"""

import os
from dotenv import load_dotenv

# Base directory of the project
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Load environment variables from .env file (override=True ensures latest values take precedence)
load_dotenv(os.path.join(BASE_DIR, '.env'), override=True)

# Flask settings
SECRET_KEY = os.getenv('SECRET_KEY', 'dog-breed-project-secret-key')
DEBUG = os.getenv('FLASK_DEBUG', 'True').lower() in ('true', '1', 't')

# Folder paths
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'images', 'uploads')
MODEL_FOLDER = os.path.join(BASE_DIR, 'model')
DATASET_FOLDER = os.path.join(BASE_DIR, 'dataset')
DATABASE_FOLDER = os.path.join(BASE_DIR, 'database')

# Allowed image extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# MySQL Database Configuration (dynamically retrieved from environment)
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = int(os.getenv('DB_PORT', 3306))
DB_USER = os.getenv('DB_USER', 'root')
DB_PASSWORD = os.getenv('DB_PASSWORD', '')
DB_NAME = os.getenv('DB_NAME', 'dog_breed_db')


def get_db_config():
    """
    Return the freshest database connection parameters from environment.
    Ensures that any changes to .env are reflected immediately.
    """
    load_dotenv(os.path.join(BASE_DIR, '.env'), override=True)
    return {
        'host': os.getenv('DB_HOST', 'localhost'),
        'port': int(os.getenv('DB_PORT', 3306)),
        'user': os.getenv('DB_USER', 'root'),
        'password': os.getenv('DB_PASSWORD', ''),
        'database': os.getenv('DB_NAME', 'dog_breed_db')
    }
