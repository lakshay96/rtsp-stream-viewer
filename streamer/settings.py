import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-change-me'  # Use a real secret in production
DEBUG = True

ALLOWED_HOSTS = ['*']  # Allow all for simplicity (restrict in production)

CSRF_TRUSTED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:3002",  
]

# Installed apps, including Channels and our streams app
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'channels',         # Django Channels for WebSockets
    'streams',          # Our streaming app
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'streamer.urls'

# Templates (not heavily used in this project, but required by Django)
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

WSGI_APPLICATION = 'streamer.wsgi.application'
ASGI_APPLICATION = 'streamer.asgi.application'

# Channel layers configuration
# Using in-memory channel layer for development (not suitable for multi-process)
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer'
    }
}
# (In production, use Redis: e.g., channels_redis with Redis URL&#8203;:contentReference[oaicite:8]{index=8})

# Database (not used for stream data, can be default SQLite)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Static files (needed if we had any, e.g., for admin interface)
STATIC_URL = 'static/'
