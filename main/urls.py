from django.urls import path
from .views import CVDetailPDFView, CVListView, CVDetailView

urlpatterns = [
    path('', CVListView.as_view(), name='cv_list'),
    path('cv/<int:pk>/', CVDetailView.as_view(), name='cv_detail'),
    path('cv/<int:pk>/pdf/', CVDetailPDFView.as_view(), name='cv_pdf'),
]