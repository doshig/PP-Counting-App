from django.conf.urls import url
from . import views
from .api import LABLogViewSet

from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'lablogs', LABLogViewSet)

urlpatterns = router.urls