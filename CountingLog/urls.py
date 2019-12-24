from django.conf.urls import url
from . import views
from .api import CountLogViewSet, PipelineViewSet, OpenPipelineViewSet, LastCountViewSet

from rest_framework.routers import DefaultRouter

##06/07/19 Add lastcount url 

router = DefaultRouter()
router.register(r'countlogs', CountLogViewSet)
router.register(r'pipelines', PipelineViewSet)
router.register(r'openpipelines', OpenPipelineViewSet)
router.register(r'lastcount', LastCountViewSet)

urlpatterns = router.urls