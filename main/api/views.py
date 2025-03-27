from rest_framework import viewsets

from main.api.serializers import (
    CVDetailSerializer, CVSerializer,
    ContactSerializer,
    ProjectSerializer, SkillSerializer
)
from main.models import CV, Contact, Project, Skill


class CVViewSet(viewsets.ModelViewSet):
    queryset = CV.objects.all()
    serializer_class = CVSerializer

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CVDetailSerializer
        return CVSerializer



class ContactViewSet(viewsets.ModelViewSet):
    serializer_class = ContactSerializer

    def get_queryset(self):
        return Contact.objects.filter(cv_id=self.kwargs['cv_pk'])


class SkillViewSet(viewsets.ModelViewSet):
    serializer_class = SkillSerializer

    def get_queryset(self):
        return Skill.objects.filter(cv_id=self.kwargs['cv_pk'])


class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer

    def get_queryset(self):
        return Project.objects.filter(cv_id=self.kwargs['cv_pk'])
