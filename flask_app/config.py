# config.py
import os
class BaseConfig:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///local.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "jwt-dev-secret")
    WTF_CSRF_ENABLED = False

class DevConfig(BaseConfig):
    DEBUG = True

class TestConfig(BaseConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"

class ProdConfig(BaseConfig):
    DEBUG = False

def get_config(name=None):
    name = name or os.getenv("FLASK_ENV", "dev")
    return {"dev": DevConfig, "test": TestConfig, "prod": ProdConfig}.get(name, DevConfig)
