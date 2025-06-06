from django.contrib import admin
from .models import ChatRoom,Message,GroupSessionParticipant,GroupTherapySession

# Register your models here.
admin.site.register(ChatRoom)
admin.site.register(Message)
admin.site.register(GroupTherapySession)            
admin.site.register(GroupSessionParticipant)
