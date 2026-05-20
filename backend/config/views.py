import mimetypes
from pathlib import Path

from django.conf import settings
from django.http import FileResponse, Http404

FRONTEND_DIST = Path(settings.BASE_DIR).parent / "frontend" / "dist"
ASSETS_DIR = FRONTEND_DIST / "assets"


def serve_spa(request):
    index = FRONTEND_DIST / "index.html"
    if not index.exists():
        raise Http404("Frontend not built. Run: cd frontend && npm run build")
    return FileResponse(index.open("rb"), content_type="text/html")


def serve_frontend_asset(request, path):
    target = ASSETS_DIR / path
    if not target.is_file():
        raise Http404()
    content_type, _ = mimetypes.guess_type(str(target))
    return FileResponse(target.open("rb"), content_type=content_type or "application/octet-stream")
