from .base import *
from .env import env

DEBUG = env.bool("DEBUG", default=True)
ALLOWED_HOSTS = ["*"]
DATABASES = {
    'default': env.db("DATABASE_URL", default="sqlite:///db.sqlite3")
}
SECRET_KEY = env("SECRET_KEY")

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "file": {
            "class": "logging.FileHandler",
            "filename": "app.log",
            "level": "DEBUG"
        },
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG"
        }
    },

    "loggers": {
        "": {
            "level": "DEBUG",
            "handlers": ["console", "file"],
        }
    }
}