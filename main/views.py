from django.db.models import Prefetch
from django.views.generic import ListView, DetailView
# from django_weasyprint import WeasyTemplateResponseMixin
# from django.http import HttpResponseServerError

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


class CVDetailPDFView(DetailView):
    pass
# class CVDetailPDFView(WeasyTemplateResponseMixin, DetailView):
#     model = CV
#     template_name = 'main/cv_pdf.html'
#     pdf_filename = 'cv_{pk}.pdf'
#
#     def get_pdf_filename(self):
#         return f'cv_{self.object.first_name}_{self.object.last_name}.pdf'.lower()
#
#     def get_queryset(self):
#         return CV.objects.prefetch_related(
#             Prefetch('skills', queryset=Skill.objects.all()),
#             Prefetch('projects',
#                      queryset=Project.objects.order_by('-start_date')),
#             Prefetch('contacts', queryset=Contact.objects.all())
#         )
#
#     def get(self, request, *args, **kwargs):
#         try:
#             return super().get(request, *args, **kwargs)
#         except Exception as e:
#             return HttpResponseServerError(f"Error generating PDF: {str(e)}")
