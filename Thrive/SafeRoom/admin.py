from django.contrib import admin
from .models import Meditation,BreathingExercise, MotivationalQuote, PrivateJournalEntry

# Register your models here.
admin.site.register(Meditation)
admin.site.register(BreathingExercise)
admin.site.register(MotivationalQuote)
admin.site.register(PrivateJournalEntry)
