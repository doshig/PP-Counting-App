from rest_framework.viewsets import ModelViewSet
from .serializers import DepartmentLogSerializer, DepartmentUserSerializer
from .models import DepartmentLog, DepartmentLogUsers



class DepartmentLogViewSet(ModelViewSet):
    
    queryset = DepartmentLog.objects.all()
    serializer_class = DepartmentLogSerializer
    
class DepartmentUserViewSet(ModelViewSet):
    queryset = DepartmentLogUsers.objects.filter(userActive = True)
    serializer_class = DepartmentUserSerializer

