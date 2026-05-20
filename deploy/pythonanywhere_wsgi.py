# Copy this into PythonAnywhere → Web → WSGI configuration file
# Replace YOUR_USERNAME with your PythonAnywhere username

import os
import sys

path = "/home/YOUR_USERNAME/truck-trip-details/backend"
if path not in sys.path:
    sys.path.insert(0, path)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
os.environ["DEBUG"] = "false"
os.environ["ALLOWED_HOSTS"] = "YOUR_USERNAME.pythonanywhere.com"
os.environ["CORS_ALLOWED_ORIGINS"] = "https://rahulagg1804.github.io"
os.environ["GEOCODING_ENABLED"] = "true"

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
