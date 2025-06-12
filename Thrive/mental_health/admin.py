from django.contrib import admin
from .models import TherapistSession,JournalEntry, ChatMessage

# Register your models here.
admin.site.register(TherapistSession)
admin.site.register(JournalEntry)
admin.site.register(ChatMessage)
