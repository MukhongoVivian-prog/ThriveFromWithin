from rest_framework import serializers
from .models import Benefit, BenefitCategory

class BenefitCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BenefitCategory
        fields = '__all__'

class BenefitSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Benefit
        fields = '__all__'
