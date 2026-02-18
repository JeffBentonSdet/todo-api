"""Application configuration. Defines configuration classes for different environments (development, testing, production)."""

import os


class Config:
    """Base configuration."""

    SECRET_KEY = os.environ.get("SECRET_KEY", "change-me-in-production")
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    """Development configuration."""

    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", "sqlite:///todo_dev.db"
    )


class TestingConfig(Config):
    """Testing configuration."""

    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"


configs = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "default": DevelopmentConfig,
}
