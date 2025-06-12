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
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Mail settings
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', True)
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    
    # AI settings
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
    OPENAI_ROUTER_API_KEY = os.environ.get('OPENAI_ROUTER_API_KEY', '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')
    
    # Zoom settings
    ZOOM_API_KEY = os.environ.get('ZOOM_API_KEY')
    ZOOM_API_SECRET = os.environ.get('ZOOM_API_SECRET')
    
    # Google Meet settings
    GOOGLE_MEET_API_KEY = 'AIzaSyDWVJ7jqy1uTXMDGYy1Y_f0cLm0AWxoS-Q'
    
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
