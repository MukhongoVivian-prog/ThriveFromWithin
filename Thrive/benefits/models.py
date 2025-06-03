from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class BenefitCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Benefit(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    country = models.CharField(max_length=100)
    company_name = models.CharField(max_length=255)
    category = models.ForeignKey(BenefitCategory, on_delete=models.SET_NULL, null=True, related_name='benefits')
    available_to_employees = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.company_name} ({self.country})"
