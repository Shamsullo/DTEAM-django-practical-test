from django.db.models import Prefetch
from django.http import HttpResponseServerError
from django.views.generic import ListView, DetailView
from django_weasyprint import WeasyTemplateResponseMixin
from django.http import JsonResponse
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError
from django.views.generic.detail import BaseDetailView
from .tasks import send_cv_pdf_email


from .models import CV, Contact, Project, Skill


class CVListView(ListView):
    model = CV
    template_name = "main/cv_list.html"
    context_object_name = "cvs"

    def get_queryset(self):
        return CV.objects.prefetch_related(
            Prefetch("skills", queryset=Skill.objects.all()),
            Prefetch(
                "projects", queryset=Project.objects.order_by("-start_date")
            ),
            Prefetch(
                "contacts", queryset=Contact.objects.filter(is_primary=True)
            ),
        )


class CVDetailView(DetailView):
    model = CV
    template_name = "main/cv_detail.html"
    context_object_name = "cv"

    def get_queryset(self):
        return CV.objects.prefetch_related(
            Prefetch("skills", queryset=Skill.objects.all()),
            Prefetch(
                "projects", queryset=Project.objects.order_by("-start_date")
            ),
            Prefetch("contacts", queryset=Contact.objects.all()),
        )


class CVDetailPDFView(WeasyTemplateResponseMixin, DetailView):
    model = CV
    template_name = "main/cv_pdf.html"
    pdf_filename = "cv_{pk}.pdf"

    def get_pdf_filename(self):
        return (
            f"cv_{self.object.first_name}_{self.object.last_name}.pdf".lower()
        )

    def get_queryset(self):
        return CV.objects.prefetch_related(
            Prefetch("skills", queryset=Skill.objects.all()),
            Prefetch(
                "projects", queryset=Project.objects.order_by("-start_date")
            ),
            Prefetch("contacts", queryset=Contact.objects.all()),
        )

    def get(self, request, *args, **kwargs):
        try:
            return super().get(request, *args, **kwargs)
        except Exception as e:
            return HttpResponseServerError(f"Error generating PDF: {str(e)}")


class SendCVEmailAjaxView(BaseDetailView):
    model = CV

    def validate_email(self, email):
        validator = EmailValidator()
        try:
            validator(email)
            return True
        except ValidationError:
            return False

    def post(self, request, *args, **kwargs):
        email = request.POST.get("email")

        if not email:
            return JsonResponse(
                {"error": "Email address is required"}, status=400
            )

        if not self.validate_email(email):
            return JsonResponse({"error": "Invalid email address"}, status=400)

        try:
            cv = self.get_object()
            task = send_cv_pdf_email.delay(cv.pk, email)

            return JsonResponse(
                {"message": "Email will be sent shortly", "task_id": task.id}
            )

        except Exception as e:
            return JsonResponse(
                {"error": f"Failed to queue email task: {str(e)}"}, status=500
            )
