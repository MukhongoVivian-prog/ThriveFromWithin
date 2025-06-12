from rest_framework import serializers
from .models import ChatMessage, JournalEntry,TherapistSession

# class MoodCheckInSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = MoodCheckIn
#         fields = '__all__'
#         read_only_fields = ['user', 'created_at']


class JournalEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = JournalEntry
        fields = '__all__'
        read_only_fields = ['user', 'created_at']


# class WellnessProgramSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = WellnessProgram
#         fields = '__all__'
#         read_only_fields = ['created_by']


# class ProgramEnrollmentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ProgramEnrollment
#         fields = '__all__'
#         read_only_fields = ['enrolled_at']


class TherapistSessionSerializer(serializers.ModelSerializer):
    chat = serializers.SerializerMethodField()

    class Meta:
        model = TherapistSession
        fields = ['chat','id']

    def get_chat(self,obj):
        data = []
        messages = ChatMessage.objects.filter(session=obj)
        is_therapist = self.context.get('is_therapist', None)

        for message in messages:
            if is_therapist is None:
                date = message.date
                day = date.date().strftime("%A")
                time = date.time().strftime("%H:%M") 

                data.append({
                    "date":date,
                    "therapist":f"{message.therapist.first_name} {message.therapist.last_name}",
                    "reciever":"me",
                    "message":message.message,
                    "id":message.id,
                    "day":day,
                    "time":time
                })
            else:
                data.append({
                    "date":date,
                    "therapist":"me",
                    "from":f"{message.user.first_name} {message.user.last_name}",
                    "message":message.message,
                    "id":message.id,
                    "day":day,
                    "time":time
                })
        return data
