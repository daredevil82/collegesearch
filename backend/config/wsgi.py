"""
WSGI config for collegesearch project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application


from config.settings._base import set_settings_module, get_secret
set_settings_module(get_secret('django_settings_module'))
application = get_wsgi_application()
