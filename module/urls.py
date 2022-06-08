from django.conf.urls import handler400, handler404, handler500, include
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from .views import index_page

from module import settings

handler404 = 'service_pages.views.page_not_found'  # noqa
handler500 = 'service_pages.views.server_error'  # noqa
handler400 = 'service_pages.views.bad_request'  # noqa

urlpatterns = [
    path('', index_page),
    path('module-admin/', admin.site.urls),
    path('apk/', include('apk.urls')),
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
