from django.db import models
from django.core.validators import URLValidator

from .cv import CV


class Project(models.Model):
    """Projects worked on"""

    cv = models.ForeignKey(
        CV, on_delete=models.CASCADE, related_name="projects"
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    url = models.URLField(blank=True, validators=[URLValidator()])

    def __str__(self):
        return self.title
