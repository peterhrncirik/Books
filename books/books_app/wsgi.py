"""
WSGI config for books_app project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'books_app.settings')

application = get_wsgi_application()

# import os
# import sys
# sys.path.append('/opt/bitnami/projects/books_app')
# os.environ.setdefault("PYTHON_EGG_CACHE", "/opt/bitnami/projects/books_app/books_app")
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "books_app.settings")
# from django.core.wsgi import get_wsgi_application
# application = get_wsgi_application()
