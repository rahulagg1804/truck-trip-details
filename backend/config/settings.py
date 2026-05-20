import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv("SECRET_KEY", "dev-insecure-change-in-production")
DEBUG = os.getenv("DEBUG", "True").lower() in ("true", "1", "yes")
ALLOWED_HOSTS = [
    h.strip()
    for h in os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")
    if h.strip()
]

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.staticfiles",
    "corsheaders",
    "rest_framework",
    "trips",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.common.CommonMiddleware",
]

ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"

DATABASES = {}

CORS_ALLOWED_ORIGINS = [
    o.strip()
    for o in os.getenv(
        "CORS_ALLOWED_ORIGINS",
        "http://localhost:5173,http://127.0.0.1:5173,http://localhost:3000",
    ).split(",")
    if o.strip()
]
CORS_ALLOW_ALL_ORIGINS = os.getenv("CORS_ALLOW_ALL_ORIGINS", "").lower() in (
    "true",
    "1",
    "yes",
)

if not CORS_ALLOW_ALL_ORIGINS and not CORS_ALLOWED_ORIGINS and DEBUG:
    CORS_ALLOW_ALL_ORIGINS = True

REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": ["rest_framework.renderers.JSONRenderer"],
    "DEFAULT_AUTHENTICATION_CLASSES": [],
    "DEFAULT_PERMISSION_CLASSES": [],
}

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"

GEOCODING_ENABLED = os.getenv("GEOCODING_ENABLED", "True").lower() in ("true", "1", "yes")
ORS_API_KEY = os.getenv("ORS_API_KEY", "")
AVERAGE_SPEED_MPH = float(os.getenv("AVERAGE_SPEED_MPH", "55"))
FUEL_INTERVAL_MILES = int(os.getenv("FUEL_INTERVAL_MILES", "1000"))
PICKUP_DROPOFF_HOURS = float(os.getenv("PICKUP_DROPOFF_HOURS", "1"))
CYCLE_LIMIT_HOURS = float(os.getenv("CYCLE_LIMIT_HOURS", "70"))
CYCLE_DAYS = int(os.getenv("CYCLE_DAYS", "8"))
