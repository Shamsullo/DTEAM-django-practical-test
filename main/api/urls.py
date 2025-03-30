from django.urls import include, path
from rest_framework_nested import routers

from main.api.views import (
    CVViewSet,
    ContactViewSet,
    ProjectViewSet,
    SkillViewSet,
)

router = routers.DefaultRouter()
router.register(r"cvs", CVViewSet)

cv_router = routers.NestedDefaultRouter(router, r"cvs", lookup="cv")
cv_router.register(r"contacts", ContactViewSet, basename="cv-contacts")
cv_router.register(r"skills", SkillViewSet, basename="cv-skills")
cv_router.register(r"projects", ProjectViewSet, basename="cv-projects")

urlpatterns = [
    path("", include(router.urls)),
    path("", include(cv_router.urls)),
]
