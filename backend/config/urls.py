from django.urls import include, path, re_path

from trips.views import health

from .views import serve_frontend_asset, serve_spa

urlpatterns = [
    path("health/", health),
    path("api/", include("trips.urls")),
    path("assets/<path:path>", serve_frontend_asset),
    re_path(r"^.*$", serve_spa),
]
