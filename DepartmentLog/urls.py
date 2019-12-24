from django.conf.urls import url
from . import views
from .api import DepartmentLogViewSet, DepartmentUserViewSet

from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'deptlogs', DepartmentLogViewSet)
router.register(r'deptlogusers', DepartmentUserViewSet)

urlpatterns = router.urls