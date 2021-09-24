from django.conf.urls import include
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from mysite_apk import settings

urlpatterns = [
    path('lord-of-the-faults/', admin.site.urls),
    path('', include('apk.urls')),
    path('auth/', include('django.contrib.auth.urls')),
]


if settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL,
        document_root=settings.STATIC_ROOT
    )
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
