from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

if settings.DEBUG:
    urlpatterns = [
        path("admin/", admin.site.urls),
        path("api/", include("projects.urls")),
        path("api/", include("contacts.urls")),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    urlpatterns = [
        path("admin/", admin.site.urls),
        path("api/", include("projects.urls")),
        path("api/", include("contacts.urls")),
    ]
