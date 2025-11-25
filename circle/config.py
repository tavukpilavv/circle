import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///circle.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "dev-secret")
    ENV = os.getenv("FLASK_ENV", "development")
    TESTING = ENV == "testing"
    CACHE_TYPE = os.getenv("CACHE_TYPE", "SimpleCache")
    CACHE_REDIS_URL = os.getenv("REDIS_URL")
    RATE_LIMITS = os.getenv("RATE_LIMITS", "200/day;50/hour")
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*")
    SECURITY_HEADERS = {
        "Content-Security-Policy": "default-src 'self'",
        "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
    }
    MAX_PER_PAGE = int(os.getenv("MAX_PER_PAGE", 50))
    DEFAULT_PER_PAGE = int(os.getenv("DEFAULT_PER_PAGE", 20))


def get_config():
    return Config()
