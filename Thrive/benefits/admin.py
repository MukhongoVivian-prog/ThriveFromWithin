from django.contrib import admin
from .models import Benefit, BenefitCategory

# Register your models here.
admin.site.register(Benefit)
admin.site.register(BenefitCategory)