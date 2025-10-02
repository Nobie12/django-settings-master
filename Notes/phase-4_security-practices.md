

## Advanced Django Settings

### 🔹 1. **Logging**

Instead of debugging with `print()`, use Django’s logging system.

```python
# base.py
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {"class": "logging.StreamHandler"},
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
}

```

📌 Why?

- In **dev**, logs show in console.
    
- In **prod**, logs can be sent to files, services, or monitoring tools.
    

---

### 🔹 2. **Static & Media Files**

Django needs two folders:

- **Static files** (CSS, JS, images for your site).
    
- **Media files** (user uploads: profile pics, docs).

```python
# base.py
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

```

📌 In **production**, you usually serve these via Nginx, AWS S3, or Cloudflare.

---

### 🔹 3. **Security Settings (Prod)**

Only in `prod.py`:

```python
# prod.py
SECURE_SSL_REDIRECT = True       # Force HTTPS
SESSION_COOKIE_SECURE = True     # Cookies only sent over HTTPS
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000   # Enforce HTTPS for 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

```

📌 Why?

- Protects against attacks like **cookie theft** & **downgrade to HTTP**.
    

---

### 🔹 4. **Allowed Hosts & CORS**

```python
# prod.py
ALLOWED_HOSTS = ["mydomain.com"]

# If using APIs with frontend:
CORS_ALLOWED_ORIGINS = [
    "https://myfrontend.com",
]

```

📌 Prevents strangers from hijacking your app on other domains.

---

## 🔹 5. **Multiple Environments with `.env`**

Instead of hardcoding DB or email values in each settings file:

```env
# .env (prod)
DEBUG=False
SECRET_KEY=super-secret
DATABASE_URL=postgres://user:pass@db:5432/proddb
EMAIL_URL=smtp://user:pass@mailserver.com:587
CACHE_URL=redis://cache:6379/1

```

Then `base.py` stays clean:

```python
DEBUG = env("DEBUG")
SECRET_KEY = env("SECRET_KEY")
DATABASES = {"default": env.db()}
EMAIL_CONFIG = env.email_url("EMAIL_URL")
vars().update(EMAIL_CONFIG)
CACHES = {"default": env.cache()}

```

---

## 🔹 6. **Best Practices**

- ✅ Keep `base.py` minimal — just the foundation.
    
- ✅ Never commit `.env` to GitHub (add to `.gitignore`).
    
- ✅ Use strong security defaults in `prod.py`.
    
- ✅ Log errors in production, but don’t expose them to users.
    
- ✅ Centralize secrets in `.env` → one file controls everything.