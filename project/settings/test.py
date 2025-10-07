from .base import *

DEBUG = env.bool("DEBUG", default=True)
ALLOWED_HOSTS = ["*"]
DATABASES = {
    'default': env.db("DATABASE_URL", default="sqlite:///db.sqlite3")
}
SECRET_KEY = env("SECRET_KEY")