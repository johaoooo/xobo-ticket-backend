import os
from pathlib import Path
from datetime import timedelta

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-xobo-ticket-secret-key-2024'
DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '.onrender.com']

# Jazzmin DOIT être AVANT django.contrib.admin
INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'rest_framework_simplejwt',
    'users',
    'stands',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'xoboticket.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'xoboticket.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'xobo_ticket',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'Africa/Porto-Novo'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CORS_ALLOWED_ORIGINS = ["http://localhost:5173", "http://localhost:5174"]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': ('rest_framework_simplejwt.authentication.JWTAuthentication',),
    'DEFAULT_PERMISSION_CLASSES': ['rest_framework.permissions.IsAuthenticated'],
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=7),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=30),
}

ADMIN_VALIDATION_PASSWORD = 'admin123'
AUTH_USER_MODEL = 'users.User'

# Email Configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'josephdehazounde@gmail.com'
EMAIL_HOST_PASSWORD = 'cwra avcv xlwi jcry'
DEFAULT_FROM_EMAIL = 'Xobo Ticket <josephdehazounde@gmail.com>'
FRONTEND_URL = 'http://localhost:5173'

# ============================================
# JAZZMIN CONFIGURATION - Admin Moderne
# ============================================

JAZZMIN_SETTINGS = {
    "site_title": "Xobo Ticket Admin",
    "site_header": "Xobo Ticket",
    "site_brand": "Xobo Ticket",
    "welcome_sign": "Bienvenue sur Xobo Ticket",
    "copyright": "Xobo Ticket",
    "search_model": "stands.Stand",
    
    "topmenu_links": [
        {"name": "Accueil", "url": "/admin/", "icon": "fas fa-home"},
        {"name": "Frontend", "url": "/", "icon": "fas fa-globe"},
        {"name": "API", "url": "/api/health/", "icon": "fas fa-plug"},
    ],
    
    "icons": {
        "auth.User": "fas fa-users",
        "users.User": "fas fa-user",
        "stands.Stand": "fas fa-store",
        "stands.Validation": "fas fa-check-circle",
        "auth.Group": "fas fa-users",
    },
    
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",
    
    "show_ui_builder": True,
    "changeform_format": "horizontal_tabs",
    "changeform_format_overrides": {},
}

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": "navbar-primary",
    "accent": "accent-primary",
    "navbar": "navbar-dark",
    "no_navbar_border": False,
    "navbar_fixed": True,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": True,
    "sidebar": "sidebar-dark-primary",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": False,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
    "theme": "darkly",
    "dark_mode_theme": "darkly",
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success"
    }
}

import dj_database_url
import os

_db_url = os.environ.get('DATABASE_URL')
if _db_url:
    DATABASES['default'] = dj_database_url.parse(_db_url, conn_max_age=600)

SECRET_KEY = os.environ.get('SECRET_KEY', SECRET_KEY)
DEBUG = os.environ.get('DEBUG', 'True') == 'True'
FRONTEND_URL = os.environ.get('FRONTEND_URL', FRONTEND_URL)
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', EMAIL_HOST_USER)
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', EMAIL_HOST_PASSWORD)
