"""
Django settings for ll_project project.

"""

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# MEDIA
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'   # meglio così

# CKEditor configs (immutato)
CKEDITOR_5_CONFIGS = {
    'title': {
        'toolbar': ['bold', 'italic', 'underline'],
        'height': '50px',
        'placeholder': 'Scrivi il titolo...',
        'htmlSupport': {
            'allow': [{'name': '*', 'attributes': True, 'classes': True, 'styles': True}]
        },
        'enter': 'soft',
    },
    'description': {
        'toolbar': ['bold', 'italic', 'underline', 'link', 'bulletedList', 'numberedList'],
        'height': '200px',
        'placeholder': 'Scrivi la descrizione...',
        'htmlSupport': {
            'allow': [{'name': '*', 'attributes': True, 'classes': True, 'styles': True}]
        },
        'enter': 'soft',
    },
    'details': {
        'toolbar': ['bold', 'italic', 'underline', 'link', 'bulletedList', 'numberedList'],
        'height': '200px',
        'placeholder': 'Scrivi la descrizione...',
        'htmlSupport': {
            'allow': [{'name': '*', 'attributes': True, 'classes': True, 'styles': True}]
        },
        'enter': 'soft',
    }
}

# ===========================
# 🔐 SECURITY
# ===========================

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")

DEBUG = os.environ.get("DJANGO_DEBUG", "False") == "True"

ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS", "").split(",")

CSRF_TRUSTED_ORIGINS = os.environ.get("DJANGO_CSRF_TRUSTED_ORIGINS", "").split(",")

# ===========================
# 🔧 APPS
# ===========================

INSTALLED_APPS = [
    'margherita_poli',
    'accounts',

    'django_bootstrap5',
    'django_ckeditor_5',
    'imagekit',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

LANGUAGES = [
    ('it', 'Italiano'),
    ('en', 'English'),
]

MIDDLEWARE = [
    'django.middleware.locale.LocaleMiddleware',

    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'll_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
            ],
        },
    },
]

WSGI_APPLICATION = 'll_project.wsgi.application'


# ===========================
# 🗂️ DATABASE (PostgreSQL)
# ===========================

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get("DB_NAME"),
        'USER': os.environ.get("DB_USER"),
        'PASSWORD': os.environ.get("DB_PASSWORD"),
        'HOST': os.environ.get("DB_HOST"),
        'PORT': os.environ.get("DB_PORT", "5432"),
    }
}


# ===========================
# 🔐 PASSWORD VALIDATION
# ===========================

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'it-IT'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# ===========================
# 📁 STATIC FILES
# ===========================

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'static'


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ===========================
# 📧 EMAIL (via variabili ambiente)
# ===========================

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.environ.get("EMAIL_HOST")
EMAIL_PORT = os.environ.get("EMAIL_PORT")
EMAIL_USE_TLS = os.environ.get("EMAIL_USE_TLS") == "True"
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER


# ===========================
# 💳 STRIPE
# ===========================

STRIPE_SECRET_KEY = os.environ.get("STRIPE_SECRET_KEY")
STRIPE_PUBLIC_KEY = os.environ.get("STRIPE_PUBLIC_KEY")

