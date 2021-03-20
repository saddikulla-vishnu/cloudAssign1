"""
WSGI config for cloudAssign1 project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from dotenv import load_dotenv

print(load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cloudAssign1.settings')

application = get_wsgi_application()
