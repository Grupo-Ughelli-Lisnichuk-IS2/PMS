"""
WSGI config for PMS project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

import os
import sys

sys.path.append('/home/yolile/PMS/')
sys.path.append('/home/yolile/PMS/PMS/')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "PMS.settings")


import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
