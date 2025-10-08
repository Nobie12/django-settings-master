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
            "formatter": "verbose"
        },
        "logtail": {
            "class": "logtail.LogtailHandler",
            "source_token": env("BETTERSTACK_SOURCE_TOKEN"),
            "host": "https://" + env("BETTERSTACK_INGESTING_HOST"),
            "formatter": "verbose"
        }
    },

    "loggers": {
        "logging_test": {
            "level": env("DJANGO_LOG_LEVEL"),
            "handlers": ["file", "console", "logtail"],
        },
        "logging_test.views": {
            "level": "INFO",
            "handlers": ["logtail", "console"],
            "propagate": False
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