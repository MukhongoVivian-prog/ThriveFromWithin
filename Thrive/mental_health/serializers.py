from rest_framework import serializers
from .models import MoodCheckIn, JournalEntry, WellnessProgram, ProgramEnrollment, TherapistSession

class MoodCheckInSerializer(serializers.ModelSerializer):
    class Meta:
        model = MoodCheckIn
        fields = '__all__'
        read_only_fields = ['user', 'created_at']


class JournalEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = JournalEntry
        fields = '__all__'
        read_only_fields = ['user', 'created_at']


class WellnessProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = WellnessProgram
        fields = '__all__'
        read_only_fields = ['created_by']


class ProgramEnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgramEnrollment
        fields = '__all__'
        read_only_fields = ['enrolled_at']


class TherapistSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TherapistSession
        fields = '__all__'
        read_only_fields = ['user']
