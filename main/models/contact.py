from django.db import models

from .cv import CV


class Contact(models.Model):
    """Contact information"""
    TYPE_CHOICES = [
        ('EMAIL', 'Email'),
        ('PHONE', 'Phone'),
        ('LINKEDIN', 'LinkedIn'),
        ('GITHUB', 'GitHub'),
        ('WEBSITE', 'Website'),
        ('OTHER', 'Other'),
    ]

    cv = models.ForeignKey(CV, on_delete=models.CASCADE,
                           related_name='contacts')
    contact_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    value = models.CharField(max_length=255)
    is_primary = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['cv', 'contact_type', 'is_primary'],
                name='unique_primary_contact_type'
            )
        ]

    def __str__(self):
        return f"{self.get_contact_type_display()}: {self.value}"
