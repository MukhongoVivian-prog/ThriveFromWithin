from rest_framework import serializers
from .models import WellnessProgram, WellnessEnrollment

class WellnessProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = WellnessProgram
        fields = '__all__'

class WellnessEnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = WellnessEnrollment
        fields = '__all__'
