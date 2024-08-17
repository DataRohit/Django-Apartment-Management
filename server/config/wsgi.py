# Imports
import os
import sys
from pathlib import Path

import environ
from django.core.wsgi import get_wsgi_application

# Initialize environment variables
env = environ.Env()


# Resolve the base directory of the project
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent


# Add the project directory to the Python path
sys.path.append(str(BASE_DIR / "apps"))


# Set the Django settings module to use for the application
os.environ.setdefault("DJANGO_SETTINGS_MODULE", env("DJANGO_SETTINGS_MODULE"))


# Get the WSGI application for the Django project
application = get_wsgi_application()
