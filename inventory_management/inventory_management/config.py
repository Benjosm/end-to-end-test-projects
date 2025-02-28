import os
from datetime import timedelta

class Config:
    """Base configuration."""
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-key-not-secure")
    DATABASE_URI = os.environ.get("DATABASE_URI", "sqlite:///inventory.db")
    JWT_EXPIRATION = timedelta(hours=1)
    ITEMS_PER_PAGE = 20
    NOTIFICATION_ENABLED = False

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    TESTING = False

class TestingConfig(Config):
    """Testing configuration."""
    DEBUG = True
    TESTING = True
    DATABASE_URI = "sqlite:///:memory:"

class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    TESTING = False
    NOTIFICATION_ENABLED = True
    
    # Security headers
    SECURE_HEADERS = {
        "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
        "X-Content-Type-Options": "nosniff",
        "X-Frame-Options": "SAMEORIGIN",
        "X-XSS-Protection": "1; mode=block",
    }
