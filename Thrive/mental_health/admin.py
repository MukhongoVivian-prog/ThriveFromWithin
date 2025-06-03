from django.contrib import admin
from .models import WellnessProgram,TherapistSession, MoodCheckIn, JournalEntry, ProgramEnrollment

# Register your models here.
admin.site.register(WellnessProgram)
admin.site.register(TherapistSession)
admin.site.register(MoodCheckIn)
admin.site.register(JournalEntry)
admin.site.register(ProgramEnrollment)
