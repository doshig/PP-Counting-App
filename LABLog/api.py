from rest_framework.viewsets import ModelViewSet
from .serializers import LABLogSerializer
from .models import LABLog



class LABLogViewSet(ModelViewSet):
    
    queryset = LABLog.objects.all()
    serializer_class = LABLogSerializer

