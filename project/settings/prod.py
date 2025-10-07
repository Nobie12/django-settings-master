from .base import *
from .env import env

DEBUG = False
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=[])
SECRET_KEY = env("SECRET_KEY")