"""Isolated SQLite settings for the legacy inventory regression tests.

Run from the repository root:
    python manage.py test inventory --settings=EcoFlux.test_settings
These settings do not read a deployment .env or connect to a live database.
"""
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = "isolated-legacy-test-settings-only"
DEBUG = False
ALLOWED_HOSTS = ["testserver", "localhost"]
INSTALLED_APPS = [
    "django.contrib.auth", "django.contrib.contenttypes", "django.contrib.sessions",
    "django.contrib.messages", "django.contrib.staticfiles", "crispy_forms", "inventory",
]
MIDDLEWARE = [
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
]
DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}}
ROOT_URLCONF = "inventory.urls"
TEMPLATES = [{
    "BACKEND": "django.template.backends.django.DjangoTemplates",
    "DIRS": [BASE_DIR / "templates"], "APP_DIRS": True,
    "OPTIONS": {"context_processors": [
        "django.contrib.auth.context_processors.auth",
        "django.contrib.messages.context_processors.messages",
        "django.template.context_processors.request",
    ]},
}]
STATIC_URL = "/static/"
MEDIA_URL = "/media/"
PHOTO_UPLOAD_SUBDIR = "photos"
DOCUMENT_UPLOAD_SUBDIR = "documents"
MEDIA_THUMBNAIL_SUBDIR = "thumbnails"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
USE_TZ = True
TIME_ZONE = "UTC"
LOGIN_URL = "/accounts/login/"
GIT_VERSION = "test"
