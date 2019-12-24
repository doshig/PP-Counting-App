from rest_framework import serializers

from .models import CountLog, Pipeline



class CountLogSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CountLog
        fields = '__all__'
        
class PipelineSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Pipeline
        fields = '__all__'
