from django.db import models


class CV(models.Model):
    """Main CV model containing personal information"""

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    bio = models.TextField(help_text="Professional summary")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "CV"
        verbose_name_plural = "CVs"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.first_name} {self.last_name}'s CV"
