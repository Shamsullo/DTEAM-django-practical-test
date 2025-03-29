from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from CVProject.views import SettingsView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('audit/', include('audit.urls')),
    path('api/', include('main.api.urls'), name='api_cv'),
    path('settings/', SettingsView.as_view(), name='settings'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
