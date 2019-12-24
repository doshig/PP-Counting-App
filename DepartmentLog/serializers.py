from rest_framework import serializers

from .models import DepartmentLog, DepartmentLogUsers



class DepartmentLogSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = DepartmentLog
        fields = '__all__'
        
        
class DepartmentUserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = DepartmentLogUsers
        fields = '__all__'
