import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    INIT_KEY = os.environ.get('INIT_KEY') or 'dev-init-key'
    
    # Database configuration
    if os.environ.get('DATABASE_URL'):
        # Handle Render's PostgreSQL URL
        if os.environ.get('DATABASE_URL').startswith("postgres://"):
            SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL').replace("postgres://", "postgresql://", 1)
        else:
            SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    else:
        SQLALCHEMY_DATABASE_URI = 'sqlite:///aurarecovery.db'
    
    # Ensure we're using the correct database name
    if 'postgresql://' in SQLALCHEMY_DATABASE_URI:
        # Extract the base URL without the database name
        base_url = SQLALCHEMY_DATABASE_URI.rsplit('/', 1)[0]
        # Add the specific database name
        SQLALCHEMY_DATABASE_URI = f"{base_url}/aurarecovery_db_uhop"
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Mail settings
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', True)
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    
    # AI settings
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
    
    # Zoom settings
    ZOOM_API_KEY = os.environ.get('ZOOM_API_KEY')
    ZOOM_API_SECRET = os.environ.get('ZOOM_API_SECRET')
    
    # Google Meet settings
    GOOGLE_MEET_API_KEY = os.environ.get('GOOGLE_MEET_API_KEY')
    
    # Security settings
    SESSION_COOKIE_SECURE = os.environ.get('FLASK_ENV') == 'production'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Application settings
    ITEMS_PER_PAGE = 20
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file upload

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
