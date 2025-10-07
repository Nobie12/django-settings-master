import environ
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent
env = environ.Env()

# Take environment variables from .env file
environ.Env.read_env(BASE_DIR / ".env")
