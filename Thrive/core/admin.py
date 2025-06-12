from django.contrib import admin
from .models import User, Company,Material, Scene, Sound

# Register your models here.
admin.site.register(User)
admin.site.register(Company)
admin.site.register(Material)

admin.site.register(Scene)
admin.site.register(Sound)