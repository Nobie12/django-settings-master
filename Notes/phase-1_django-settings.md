
## Concepts
- What are settings?
- How Django reads settings (priority, settings object).
- Key settings (DEBUG, SECRET_KEY, ALLOWED_HOSTS, DATABASES, etc.).
- Best practices: configuration vs logic, don’t hardcode secrets.

### What I have learnt

- So settings is actually what configures the whole Django Installation.
- It starts with the `DJANGO_SETTINGS_MODULE` environment variable which tells django which file to use for settings.
- This is explicitly set inside the `manage.py` file. Sth like this:
``` bash
	os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
```
- when the server is running in development u don't need to explicitly set the `DJANGO_SETTINGS_MODULE` because it is inside the manage.py file. But in deployed state the file is not even used files like the wsg or the asg are used instead or the `DJANGO_SETTINGS_MODULE` can be passed explicitly  using other methods.
- **You shouldn’t alter settings in your applications at runtime. For example, don’t do this in a view:**
```bash
from django.conf import settings

settings.DEBUG = True  # Don't do this!
```
- Because a settings file contains sensitive information, such as the database password, you should make every attempt to limit access to it. For example, change its file permissions so that only you and your web server’s user can read it. This is especially important in a shared-hosting environment.

##### Key settings explained (what they _do_, common pitfalls, and examples)

###### `DEBUG`

- Purpose: Developer mode — shows detailed error pages, extra checks and auto-reloader.
    
- Pitfall: **Never** run with `DEBUG = True` in production — it leaks stack traces, secrets and can reveal application internals. The Django deployment checklist explicitly warns about this. [Django Project](https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/?utm_source=chatgpt.com)
    
- Example:
```python
# development
DEBUG = True

# production
DEBUG = False
```

###### `SECRET_KEY`

- Purpose: cryptographic signing (sessions, CSRF tokens, password reset tokens, signed cookies). Must be unique & secret. If attackers know it they can forge tokens. [Django Project](https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/?utm_source=chatgpt.com)
    
- Pitfall: regenerating it at runtime (on each process start) will invalidate existing sessions and signed tokens; committing it to VCS leaks everything. [FreeCodeCamp+1](https://www.freecodecamp.org/news/how-to-change-your-django-secret-key-without-breaking-your-app/?utm_source=chatgpt.com)
    
- How to manage:
    
    - Generate once (e.g. `django.core.management.utils.get_random_secret_key()`) and store in environment/secret manager. [Stack Overflow](https://stackoverflow.com/questions/54498123/django-secret-key-generation?utm_source=chatgpt.com)
        
    - Load in `settings.py` from env:

```python
import os
SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]   # raise if missing (fail fast)
```

###### `ALLOWED_HOSTS`

- Purpose: protects against malformed Host headers (Host header attacks / DNS rebinding). It must list valid hostnames your site serves, e.g. `["example.com", "api.example.com"]`. If `DEBUG=False` and ALLOWED_HOSTS not properly set, Django will refuse requests. [Django Project+1](https://docs.djangoproject.com/en/5.2/topics/settings/?utm_source=chatgpt.com)
    
- Example:
```python
ALLOWED_HOSTS = ["myapp.example.com", "api.example.com"]
# or for a single dev machine:
ALLOWED_HOSTS = ["localhost", "127.0.0.1"]
```

###### `DATABASES`

- Purpose: connection config for each DB connection; usually a `default` dict containing `ENGINE`, `NAME`, `USER`, `PASSWORD`, `HOST`, `PORT`, etc. See Django DB docs for engines and advanced options. [Django Project+1](https://docs.djangoproject.com/en/5.2/ref/settings/?utm_source=chatgpt.com)
    
- Tip: avoid placing DB username/password directly in repo — load via env or DB URL helper libs (see below).
    

Example (Postgres):

```python
DATABASES = {
  "default": {
    "ENGINE": "django.db.backends.postgresql",
    "NAME": "mydb",
    "USER": "myuser",
    "PASSWORD": os.environ.get("DB_PASSWORD"),
    "HOST": "127.0.0.1",
    "PORT": "5432",
  }
}

```
### A few other quick keys you’ll hit often

- `INSTALLED_APPS` — list of enabled apps (order matters for migrations/signals).
    
- `MIDDLEWARE` — request/response processing chain; order is very important.
    
- `TEMPLATES` — Django template engine list & options.
    
- `STATIC_URL`, `STATIC_ROOT`, `MEDIA_URL`, `MEDIA_ROOT` — static/media file locations & serving rules.  
    All these are documented in the settings reference. [Django Project](https://docs.djangoproject.com/en/5.2/ref/settings/?utm_source=chatgpt.com)
    

---

# Best practices — configuration vs logic (practical checklist + examples)

**Principles (short & opinionated):**

1. **Config only in settings. No business logic.** Settings = _a list of knobs and values_, not code that performs work or database reads. If you find yourself doing heavy computation or DB queries in settings, move that into an app initialization function or service. Reading settings at import time leads to fragile apps. (Opinion: keep settings _tiny_ and declarative.) [adamj.eu+1](https://adamj.eu/tech/2022/11/24/django-settings-patterns-to-avoid/?utm_source=chatgpt.com)
    
2. **12-Factor: treat config as environment.** Put per-instance secrets/config in environment variables (or a cloud secret store). This makes containers and deployments predictable and safe. Use libraries like `django-environ` or `python-decouple` to parse env vars and `.env` files for local dev. [12factor.net+1](https://12factor.net/config?utm_source=chatgpt.com)
    
3. **Split settings by environment.** `settings/base.py`, `settings/development.py`, `settings/production.py` (or use `django-split-settings`/`django-configurations` if you like). Then pick which module via `DJANGO_SETTINGS_MODULE` (preferred) or `--settings`. Opinion: I prefer a small `base.py` + `dev.py` and `prod.py` that import `base.py` and override only what's needed. [Simple is Better Than Complex+1](https://simpleisbetterthancomplex.com/tips/2017/07/03/django-tip-20-working-with-multiple-settings-modules.html?utm_source=chatgpt.com)
    
4. **Never commit secrets.** Add `.env` / private config to `.gitignore`. Commit a `.env.example` or `.env.dist` listing required keys for dev. Use CI/CD secret mechanisms or cloud secret managers for production keys. [django-environ.readthedocs.io](https://django-environ.readthedocs.io/en/latest/quickstart.html?utm_source=chatgpt.com)
    
5. **Fail fast for missing config.** Use code that raises if a required env var is missing (e.g. `os.environ['DJANGO_SECRET_KEY']` or `decouple.config('SECRET_KEY')`) so you don’t silently run with insecure defaults.
    

**Concrete code examples**

Load secret + DB safely (recommended pattern):

```python
# settings/base.py
import os
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")
if not SECRET_KEY:
    raise RuntimeError("DJANGO_SECRET_KEY missing - do not run without it")

DATABASES = {
    "default": {
        "ENGINE": os.environ.get("DB_ENGINE", "django.db.backends.postgresql"),
        "NAME": os.environ.get("DB_NAME"),
        "USER": os.environ.get("DB_USER"),
        "PASSWORD": os.environ.get("DB_PASSWORD"),
        "HOST": os.environ.get("DB_HOST", "127.0.0.1"),
        "PORT": os.environ.get("DB_PORT", "5432"),
    }
}
```

Using `django-environ` (cleaner):

```python
import environ
env = environ.Env(DEBUG=(bool, False))
env.read_env()  # loads .env into environ (dev only)

SECRET_KEY = env("DJANGO_SECRET_KEY")
DATABASES = {"default": env.db()}  # reads DATABASE_URL-style string
DEBUG = env("DEBUG")
```

(Use `.env.dist` committed to repo to document keys; keep `.env` out of VCS.) [django-environ.readthedocs.io](https://django-environ.readthedocs.io/en/latest/quickstart.html?utm_source=chatgpt.com)

**What _not_ to do**

- Don’t query the DB or import models in settings. The ORM and models may not be ready; this causes import-time exceptions. [Google Groups](https://groups.google.com/g/django-developers/c/7JwWatLfP44/?utm_source=chatgpt.com)
    
- Don’t generate a random `SECRET_KEY` each startup in production — that invalidates sessions and tokens. Generate once and store it securely. [FreeCodeCamp](https://www.freecodecamp.org/news/how-to-change-your-django-secret-key-without-breaking-your-app/?utm_source=chatgpt.com)
    

---

##### Short production checklist (copy/paste)

- `DEBUG = False`. Confirm it. [Django Project](https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/?utm_source=chatgpt.com)
    
- `SECRET_KEY` is set from env/secret manager; not in VCS, not regenerated on each start. [Stack Overflow](https://stackoverflow.com/questions/54498123/django-secret-key-generation?utm_source=chatgpt.com)
    
- `ALLOWED_HOSTS` contains your domain(s). [Django Project](https://docs.djangoproject.com/en/5.2/topics/settings/?utm_source=chatgpt.com)
    
- DB credentials in env / secret store; use connection pooling if needed. [Django Project](https://docs.djangoproject.com/en/5.2/ref/settings/?utm_source=chatgpt.com)
    
- Static files served by a proper webserver (Nginx, CDN) — don’t rely on `runserver`.
    
- Use TLS/HTTPS and set secure cookie flags (SESSION_COOKIE_SECURE, CSRF_COOKIE_SECURE).
    
- Add system monitoring / logging / error reporting (Sentry, CloudWatch etc.).
    

---

### My quick opinionated recommendations (so you can act)

1. Convert `settings.py` to a `settings/` package with `base.py`, `development.py`, `production.py`. Keep `base.py` minimal. (Opinion: makes life easier.) [Simple is Better Than Complex](https://simpleisbetterthancomplex.com/tips/2017/07/03/django-tip-20-working-with-multiple-settings-modules.html?utm_source=chatgpt.com)
    
2. Use `DJANGO_SETTINGS_MODULE` in your container/host to point to the production file; _do not_ rely on branching logic in `__init__` unless you document it. [Django Project](https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/?utm_source=chatgpt.com)
    
3. Use `django-environ` or `python-decouple` for reading env vars. Keep a `.env.dist`. [django-environ.readthedocs.io](https://django-environ.readthedocs.io/?utm_source=chatgpt.com)
    
4. Store production secrets in a proper secret manager (AWS Secrets Manager / GCP Secret Manager / Azure Key Vault) and inject them into the environment at deploy time (or use service integrations). (This follows 12-factor.) [12factor.net](https://12factor.net/config?utm_source=chatgpt.com)

