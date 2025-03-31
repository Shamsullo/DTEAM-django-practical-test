from django.db import models
from django.conf import settings


class RequestLog(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    method = models.CharField(max_length=10)
    path = models.CharField(max_length=255)
    query_string = models.TextField(blank=True, null=True)
    remote_addr = models.GenericIPAddressField(null=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    status_code = models.IntegerField(null=True)
    response_time = models.FloatField(
        null=True, help_text="Response time in seconds"
    )
    user_agent = models.TextField(blank=True, null=True)
    referer = models.URLField(max_length=500, blank=True, null=True)
    request_body = models.TextField(blank=True, null=True)
    content_type = models.CharField(max_length=100, blank=True, null=True)
    session_key = models.CharField(max_length=40, blank=True, null=True)
    headers = models.JSONField(default=dict, blank=True)
    host = models.CharField(max_length=255, blank=True, null=True)
    is_secure = models.BooleanField(default=False)
    is_ajax = models.BooleanField(default=False)
    encoding = models.CharField(max_length=64, blank=True, null=True)

    class Meta:
        ordering = ["-timestamp"]
        indexes = [
            models.Index(fields=["-timestamp"]),
            models.Index(fields=["user"]),
            models.Index(fields=["method"]),
            models.Index(fields=["status_code"]),
        ]

    def __str__(self):
        return f"{self.timestamp} - {self.method} {self.path} ({self.status_code})"
