"""
Django settings for devProject project.
"""

from pathlib import Path
import os
from dotenv import load_dotenv

# ======================
# BASE DIR
# ======================
BASE_DIR = Path(__file__).resolve().parent.parent

# ======================
# .env 読み込み
# ======================
load_dotenv(BASE_DIR / ".env")

# ======================
# セキュリティ設定
# ======================
SECRET_KEY = os.environ.get("SECRET_KEY", "django-insecure-temp-key")
DEBUG = os.environ.get("DEBUG", "False") == "True"

if DEBUG:
    ALLOWED_HOSTS = [
        "127.0.0.1",
        "localhost",
    ]
else:
    ALLOWED_HOSTS = [
        "testproject-ptxu.onrender.com",
    ]



# ======================
# Application definition
# ======================
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # DRF
    "rest_framework",

    # Django アプリ
    "testApp",
    "main",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# ======================
# Debug Toolbar（DEBUG=True のときのみ）
# ======================
if DEBUG:
    INSTALLED_APPS += ["debug_toolbar"]
    MIDDLEWARE.insert(
        2, "debug_toolbar.middleware.DebugToolbarMiddleware"
    )

ROOT_URLCONF = "devProject.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "devProject.wsgi.application"


# ======================
# Database
# ======================
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# ======================
# Password validation
# ======================
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# ======================
# Internationalization
# ======================
LANGUAGE_CODE = "ja"
TIME_ZONE = "Asia/Tokyo"
USE_I18N = True
USE_TZ = True


# ======================
# Static files
# ======================
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"


# ======================
# Default primary key field type
# ======================
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# ======================
# 認証関連
# ======================
LOGIN_URL = "/login/"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"


# ======================
# Debug Toolbar
# ======================
INTERNAL_IPS = [
    "127.0.0.1",
]
