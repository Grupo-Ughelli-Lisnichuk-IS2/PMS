#encoding:utf-8

"""
Django settings for PMS project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
#MEDIA_URL = 'http://localhost:90/media/'
#STATIC_URL = 'http://localhost:90/static/'

import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
RUTA_PROYECTO = os.path.dirname(os.path.realpath(__file__))
TEMPLATE_DIRS = (
    os.path.join(BASE_DIR,'templates'),
)
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(BASE_DIR,'static'),
)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'rg9k*_m^js+8797s0-3yl_v8yu2iq((op%+aj7u5dyw$s2lg^u'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'usuarios',
    'fases',
    'proyectos',
    'tiposDeItem',
    'items'
)


DELETE_MESSAGE = 50

MESSAGE_TAGS = {
    DELETE_MESSAGE : 'deleted',
}

TEMPLATE_CONTEXT_PROCESSORS = {
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.request',  
    'django.contrib.messages.context_processors.messages',
}

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
 'USER': 'postgres', # Not used with sqlite3.
 'PASSWORD': '123456', # Not used with sqlite3.
 'HOST': 'localhost', # Set to empty string for localhost. Not used with sqlite3.
 'PORT': '5432', # Set to empty string for default. Not used with sqlite3.
 }
}

#Configuraciones de urls de login

INDEX_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
LOGIN_REDIRECT_URL = '/principal'
LOGIN_URL='/login/'

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'es-PY'

TIME_ZONE = 'America/Asuncion'

USE_I18N = True

USE_L10N = True

USE_TZ = True

SITE_ID = 1
STATIC_URL = '/static/'

SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_AGE = 1800

MEDIA_ROOT = '/home/yolile/archivosPMS/'
