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
            "filename": env("DJANGO_LOG_FILE"),
            "level": env("DJANGO_LOG_LEVEL"),
            "formatter": "verbose"
        },
        "console": {
            "class": "logging.StreamHandler",
            "level": env("DJANGO_LOG_LEVEL"),
            "formatter": "simple"
        }
    },

    "loggers": {
        "": {
            "level": env("DJANGO_LOG_LEVEL"),
            "handlers": ["file", "console"],
        }
    },

    "formatters": {
        "simple": {
            "format": "{asctime}: {levelname} {message}",
            "style": "{"
        },
        "verbose": {
            "format": "{name} {levelname} {asctime} {module} {process:d} {thread:d} {message}",
            "style": "{",
        }

    }
}