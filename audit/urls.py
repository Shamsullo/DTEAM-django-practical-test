from django.urls import path
from audit.views import RequestLogListView

urlpatterns = [
    path('logs/', RequestLogListView.as_view(), name='request_logs'),
]