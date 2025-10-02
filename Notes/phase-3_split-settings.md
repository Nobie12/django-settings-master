
## The Core Problem

-   `settings.py` gets huge (databases, apps, middleware, email, logging, security, etc).
-   Different environments (dev, staging, prod) need different values.
-   Editing the same `settings.py` everywhere is error-prone.

👉 Solution: **Split settings into multiple files** (modular & environment-aware).

* * *

## Typical Structure

```bash
myproject/
├── manage.py
├── myproject/
│   ├── __init__.py
│   ├── settings/
│   │   ├── __init__.py
│   │   ├── base.py        # common settings
│   │   ├── dev.py         # development settings
│   │   ├── prod.py        # production settings
│   │   ├── staging.py     # optional
│   │   └── test.py        # for testing
│   ├── urls.py
│   └── wsgi.py

```

* * *

## The Idea

-   **`base.py`** → Contains settings common to all environments.
-   **`dev.py`** → Imports everything from `base.py` and overrides dev-only configs (e.g. `DEBUG=True`).
-   **`prod.py`** → Imports `base.py` and overrides prod configs (e.g. `DEBUG=False`, strong security).
-   **`__init__.py`** → Sometimes used to decide which settings file to load.
* * *

## Example

### `base.py`

```python
import environ
import os

env = environ.Env(DEBUG=(bool, False))
environ.Env.read_env()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = env("SECRET_KEY")
DEBUG = env("DEBUG")

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

DATABASES = {
    "default": env.db()
}

```

* * *

### `dev.py`

```python
from .base import *

DEBUG = True
ALLOWED_HOSTS = ["*"]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

```

* * *

### `prod.py`

```python
from .base import *

DEBUG = False
ALLOWED_HOSTS = ["mydomain.com"]

SECURE_SSL_REDIRECT = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True

```

* * *

## How Django Knows Which One to Use?

In `manage.py` and `wsgi.py`, Django looks for the `DJANGO_SETTINGS_MODULE` environment variable:

```python
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings.dev")
```

Or for production:

```bash
export DJANGO_SETTINGS_MODULE="myproject.settings.prod"
```

* * *

##  Analogy

Think of it like **different outfits for different occasions**:

-   `base.py` = Your underwear (always there).
-   `dev.py` = Your casual T-shirt (comfortable for coding).
-   `prod.py` = Your suit (strict & secure for real world).
* * *

✅ This keeps settings organized, safe, and environment-specific.