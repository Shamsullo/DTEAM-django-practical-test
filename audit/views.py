from django.views.generic import ListView
from .models import RequestLog


class RequestLogListView(ListView):
    model = RequestLog
    template_name = "audit/list_request_log.html"
    context_object_name = "logs"
    paginate_by = 10
    ordering = ["-timestamp"]
