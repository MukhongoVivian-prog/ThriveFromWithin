from rest_framework import serializers
from .models import Meditation, BreathingExercise, MotivationalQuote, PrivateJournalEntry

class MeditationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meditation
        fields = '__all__'

class BreathingExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = BreathingExercise
        fields = '__all__'

class MotivationalQuoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = MotivationalQuote
        fields = '__all__'

class PrivateJournalEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = PrivateJournalEntry
        fields = '__all__'
        read_only_fields = ['user', 'created_at']
