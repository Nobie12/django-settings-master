from .base import *
from .env import env

DEBUG = False
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=[])
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
            "handlers": ["file"],
        }
    }
}