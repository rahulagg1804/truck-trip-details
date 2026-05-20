from django.urls import include, path, re_path

from .views import serve_frontend_asset, serve_spa

urlpatterns = [
    path("api/", include("trips.urls")),
    path("assets/<path:path>", serve_frontend_asset),
    re_path(r"^.*$", serve_spa),
]
