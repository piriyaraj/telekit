"""
Django settings for telekit project.

Generated by 'django-admin startproject' using Django 4.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

import sys
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-*coo(8h)0sl4n*z2%n6b#dl^ka%2*34xupw-ufyvp*o^xr=(7m'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'django.contrib.sites',
    'blog',
    'user_profile',
    'extract',
    'robots',
    'django_cleanup.apps.CleanupConfig', #keep it last
]
SITE_ID = 1
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'telekit.urls'
blogTemp=os.path.abspath("templates/blog")
userTemp=os.path.abspath("templates/user_profile")
extractTemp=os.path.abspath("templates/extract")
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [blogTemp,userTemp,extractTemp],
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

WSGI_APPLICATION = 'telekit.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': str(BASE_DIR.parent / 'telekit.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static/"),
)

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")



MEDIA_ROOT= os.path.join(BASE_DIR, "media")
MEDIA_URL="/media/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'user_profile.User'


# rating setting 
STAR_RATINGS_ANONYMOUS = True
STAR_RATINGS_CLEARABLE = True
STAR_RATINGS_RERATE = False


# robots sitemaps

ROBOTS_SITEMAP_URLS = [
    'https://telekit.link/link-sitemap.xml',
    'https://telekit.link/country-sitemap.xml',
    'https://telekit.link/language-sitemap.xml',
    'https://telekit.link/category-sitemap.xml',
    'https://telekit.link/static-sitemap.xml',

]

ROBOTS_USE_HOST = False

STRIPE_PUBLISHABLE_KEY = 'pk_test_51JehUWSCPqL7xbscRVNAqTUUt7VuPMnf0j4Y5XdQRqHbjSULO66d5o5qCZpjd9ye2v6azZPn1FIB3jZU3SEtL9rB009BwIxNyQ'
STRIPE_SECRET_KEY = 'sk_test_51JehUWSCPqL7xbscWJOjv3bb5Iq1djgYmSZBX6AR2sYjnX5HWBeDjyGYMwmOIPTe5iUFd8lbrbiBe8YaUQY1SEXq00tjlz36zp'
STRIPE_ENDPOINT_SECRET = 'whsec_bKGXPKK6KRLufpbFLFfNHaPeO12pxh8G'