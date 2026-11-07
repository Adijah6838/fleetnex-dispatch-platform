import os
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    """Base configuration class."""
    SECRET_KEY = os.environ.get("SECRET_KEY", "fleetnex-dev-secret-key")
    
    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'fleetnex.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_SORT_KEYS = False

    # JWT Configuration
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "fleetnex-jwt-secret-key")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)