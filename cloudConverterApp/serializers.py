from rest_framework import serializers
from .models import ConvertModel

class ConverterSerializer(serializers.ModelSerializer):
    class Meta:
        model= ConvertModel
        fields  = '__all__'