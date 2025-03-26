from django.db import models

from .cv import CV


class Skill(models.Model):
    """Skills with proficiency levels"""
    PROFICIENCY_CHOICES = [
        ('BEG', 'Beginner'),
        ('INT', 'Intermediate'),
        ('ADV', 'Advanced'),
        ('EXP', 'Expert'),
    ]

    cv = models.ForeignKey(CV, on_delete=models.CASCADE, related_name='skills')
    name = models.CharField(max_length=100)
    proficiency = models.CharField(
        max_length=3,
        choices=PROFICIENCY_CHOICES,
        default='INT'
    )

    def __str__(self):
        return f"{self.name} - {self.get_proficiency_display()}"

