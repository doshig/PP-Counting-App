from rest_framework import serializers

from .models import LABLog



class LABLogSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = LABLog
        fields = '__all__'
