from celery import shared_task
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from weasyprint import HTML
import tempfile
from .models import CV


@shared_task
def send_cv_pdf_email(cv_id, email):
    try:
        # Get the CV object
        cv = CV.objects.prefetch_related(
            "skills", "projects", "contacts", "education"
        ).get(pk=cv_id)

        # Render the PDF template
        html_string = render_to_string("main/cv_pdf.html", {"cv": cv})

        # Create a temporary file to store the PDF
        with tempfile.NamedTemporaryFile(
            suffix=".pdf", delete=False
        ) as tmp_file:
            # Generate PDF
            HTML(string=html_string).write_pdf(tmp_file.name)

            # Create email
            email_subject = f"CV - {cv.first_name} {cv.last_name}"
            email_body = f"Please find attached the CV for {cv.first_name} {cv.last_name}."

            # Create EmailMessage object
            email_message = EmailMessage(
                subject=email_subject,
                body=email_body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[email],
            )

            # Attach the PDF
            with open(tmp_file.name, "rb") as pdf_file:
                email_message.attach(
                    f"cv_{cv.first_name}_{cv.last_name}.pdf".lower(),
                    pdf_file.read(),
                    "application/pdf",
                )

            # Send email
            email_message.send(fail_silently=False)

        return True

    except CV.DoesNotExist:
        raise Exception("CV not found")
    except Exception as e:
        raise Exception(f"Failed to send email: {str(e)}")
