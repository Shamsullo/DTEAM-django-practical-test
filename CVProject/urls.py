from django.contrib import admin
from django.urls import include, path

from CVProject.views import SettingsView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('audit/', include('audit.urls')),
    path('api/', include('main.api.urls'), name='api_cv'),
    path('settings/', SettingsView.as_view(), name='settings'),
]