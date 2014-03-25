#encoding:utf-8
# Identificando la ruta del proyecto


"""
Django settings for PMS project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""
ADMINS =(
 ('Yohanna Lisnichuk', 'yolile_3000@hotmail.com'),
 ('Victor Ughelli', 'viktor992@hotmail.com')
)


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
TEMPLATE_DIRS = (
 os.path.join('/home/yolile/PMS/templates','templates'),
)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'v*4hk*e9ck06&nf=w!cez$=^f4&aauz9qh%vz015ix5^clc#ly'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []
#MEDIA_URL = 'http://localhost:90/media/'
#STATIC_URL = 'http://localhost:90/static/'


# Application definition

INSTALLED_APPS = (
 'django.contrib.auth',
 'django.contrib.contenttypes',
 'django.contrib.sessions',
 'django.contrib.sites',
 'django.contrib.messages',
 'django.contrib.staticfiles',
 'django.contrib.admin',
 'django.contrib.admindocs',
 'principal',
)


MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'PMS.urls'

WSGI_APPLICATION = 'PMS.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
 'default': {
 'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add ‘postgresql_psycopg2’, ‘mysql’, ‘sqlite3’ or ‘oracle’.
 'NAME': 'PMS_db', # Or path to database file if using sqlite3.
 'USER': 'yolile', # Not used with sqlite3.
 'PASSWORD': '123', # Not used with sqlite3.
 'HOST': 'localhost', # Set to empty string for localhost. Not used with sqlite3.
 'PORT': '', # Set to empty string for default. Not used with sqlite3.
 }
}


# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'es-PY'

TIME_ZONE = 'America/Asuncion'

USE_I18N = True

USE_L10N = True

USE_TZ = True

SITE_ID = 1
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'