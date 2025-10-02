# 🛠️ Django Settings Playground

A practice project to **master Django settings management** in 4 phases:

1.  How Django reads settings.
2.  Using `.env` for secrets (`django-environ`).
3.  Splitting settings into `base.py`, `dev.py`, `prod.py`.
4.  Advanced settings (logging, static/media, security).
* * *

## 🚀 Features

-   ✅ Clean `.env`\-based configuration.
-   ✅ Split settings for **dev** and **prod** environments.
-   ✅ Secure handling of **secrets & API keys**.
-   ✅ Built-in support for **Database, Email, Cache** with `django-environ`.
-   ✅ Logging & security best practices.
* * *

## 📂 Project Structure

``` bash
myproject/
├── manage.py
├── myproject/
│   ├── __init__.py
│   ├── settings/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── dev.py
│   │   └── prod.py
│   ├── urls.py
│   └── wsgi.py
├── .env
└── requirements.txt
```

* * *

## ⚙️ Installation

Clone the repo:

`git clone https://github.com/yourusername/django-settings-playground.git cd django-settings-playground`

Create and activate a virtual environment:

`python -m venv venv source venv/bin/activate    # macOS/Linux venv\Scripts\activate       # Windows`

Install dependencies:

`pip install -r requirements.txt`

* * *

## 🔑 Environment Variables

Create a `.env` file in the project root:

`# .env DEBUG=True SECRET_KEY=super-secret-key DATABASE_URL=postgres://user:pass@localhost:5432/mydb EMAIL_URL=smtp://user:password@smtp.gmail.com:587 CACHE_URL=redis://127.0.0.1:6379/1`

* * *

## 🖥️ Running the Project

### Development

`export DJANGO_SETTINGS_MODULE="myproject.settings.dev" python manage.py runserver`

### Production

`export DJANGO_SETTINGS_MODULE="myproject.settings.prod" python manage.py runserver 0.0.0.0:8000`

* * *

## 📒 Notes on the 4 Phases

1.  **Phase 1: Understanding settings**
    → How Django finds and loads settings.

2.  **Phase 2: Secure secrets with `.env`**
    → No more hardcoding API keys or passwords.

3.  **Phase 3: Split settings**
    → `base.py` for common configs, `dev.py` for local dev, `prod.py` for secure deployments.

4.  **Phase 4: Advanced config**
    → Logging, static/media files, email, caching, security settings.

* * *

## 🛡️ Best Practices

-   Add `.env` to `.gitignore`.
-   Keep `prod.py` strict (no `DEBUG=True`).
-   Use `django-environ` helpers for **DB, cache, email**.
-   Logs in dev → console, logs in prod → files/monitoring.
* * *

## 📚 References

-   [Django settings setup](https://youtu.be/O4IIBOGFyWI?si=ErjiQ8YGpOdj7fw5)

* * *

- To understand how to manage split settings I'd actually need to understand the following in order.
1. Understand Django Settings Basics
2. Learn Environment Variables & Security
3. Minimal Split Settings Setup
4. Add Security Practices
5. Then watch the thenewboston playlist for advanced modularization I guess.

- I will actually link another file for learning the 4 phases.
- Before moving on with the playlist (5th phase) and putting it into practice.


### Roadmap
- [Phase 1: Django Settings Basics](./Notes/phase-1_django-settings.md)
- [Phase 2: Env Vars & Security](./Notes/phase-2_env-vars-security.md)
- [Phase 3: Split Settings](./Notes/phase-3_split-settings.md)
- [Phase 4: Security Practices](./Notes/phase-4_security-practices.md)
- [Phase 5: Thenewboston Playlist] - I'll use another repo for this.


✍️ **Author:** Ken Aule
