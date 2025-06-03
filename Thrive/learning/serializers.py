from rest_framework import serializers
from .models import Guide, Webinar, Toolkit

class GuideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guide
        fields = '__all__'

class WebinarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Webinar
        fields = '__all__'

class ToolkitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Toolkit
        fields = '__all__'
