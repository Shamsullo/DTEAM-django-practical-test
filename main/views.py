from django.db.models import Prefetch
from django.views.generic import DetailView
from django.views.generic import ListView

from .models import CV, Contact, Project, Skill


class CVListView(ListView):
    model = CV
    template_name = 'main/cv_list.html'
    context_object_name = 'cvs'

    def get_queryset(self):
        return CV.objects.prefetch_related(
            Prefetch('skills', queryset=Skill.objects.all()),
            Prefetch('projects',
                     queryset=Project.objects.order_by('-start_date')),
            Prefetch('contacts',
                     queryset=Contact.objects.filter(is_primary=True))
        )


class CVDetailView(DetailView):
    model = CV
    template_name = 'main/cv_detail.html'
    context_object_name = 'cv'

    def get_queryset(self):
        return CV.objects.prefetch_related(
            Prefetch('skills', queryset=Skill.objects.all()),
            Prefetch('projects',
                     queryset=Project.objects.order_by('-start_date')),
            Prefetch('contacts', queryset=Contact.objects.all())
        )