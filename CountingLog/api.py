from rest_framework.viewsets import ModelViewSet
from .serializers import CountLogSerializer, PipelineSerializer
from .models import CountLog, Pipeline


##06/07/19 Add Last Count View Set to show last counted job in Count.html page 

class CountLogViewSet(ModelViewSet):
    
    queryset = CountLog.objects.all()
    serializer_class = CountLogSerializer
    
'''
This code is to get the most recent work order very quickly
'''
class LastCountViewSet(ModelViewSet):

#    queryset = CountLog.objects.all().order_by('-id')[1]
#    second_to_last = CountLog.objects.all().order_by('-id')[0]
#    print("second2last: ", second_to_last) ##Testing only

#    queryset = CountLog.objects.filter(id=second_to_last)
#    queryset = CountLog.objects.last()
#    queryset = CountLog.objects.all()
#    queryset = CountLog.objects.order_by('-id')
#    queryset = CountLog.objects.order_by('-id')[0]
#    queryset = CountLog.objects.all()[:1]
    queryset = CountLog.objects.order_by('-id')[:1] ##Get 


#    queryset = CountLog.objects.order_by('-id').last()
#    print("queryset1: ", queryset)
    
    serializer_class = CountLogSerializer

    
class OpenPipelineViewSet(ModelViewSet):
    queryset = Pipeline.objects.exclude(pipelineClosed = True)  
    serializer_class = PipelineSerializer
    
class PipelineViewSet(ModelViewSet):
    
    #Returns newest first on top, descending to oldest last
#    queryset = Pipeline.objects.all().order_by('-dateCreated')
    queryset = Pipeline.objects.all()
    serializer_class = PipelineSerializer

