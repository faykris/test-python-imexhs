from rest_framework import serializers
from .models import MedicalImageResult

class MedicalImageResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalImageResult
        fields = '__all__'