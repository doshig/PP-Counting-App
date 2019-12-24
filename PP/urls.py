"""SFA URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('Homepage.urls')),
    url(r'^CountingLog/', include('CountingLog.urls')),
    url(r'^CountingLog/count/', TemplateView.as_view(template_name="CountingLog/Count.html"),name="count log"),
    url(r'^DepartmentLog/', include('DepartmentLog.urls')),
    url(r'^DepartmentLog/deptlog/', TemplateView.as_view(template_name="DepartmentLog/Deptlog.html"),name="dept log"),
    url(r'^Reportview/errorjob/', TemplateView.as_view(template_name="Reportview/ErrorJob.html"),name="error job"),
    url(r'^Reportview/joblocation/', TemplateView.as_view(template_name="Reportview/JobLocation.html"),name="job location"),
    url(r'^LABLog/', include('LABLog.urls')),
    url(r'^LABLog/Labcheck/', TemplateView.as_view(template_name="LABLog/LabCheck.html"),name="lab check"),
    url(r'^LABLog/Labview/', TemplateView.as_view(template_name="LABLog/LabView.html"),name="lab view"),
    url(r'^CountingLog/countpipeline/', TemplateView.as_view(template_name="CountingLog/CountPipeline.html"),name="pipeline"),
    url(r'^Reportview/PipelineReport/', TemplateView.as_view(template_name="Reportview/PipelineReport.html"),name="reportpipeline"),
    url(r'^CountingLog/countsix/', TemplateView.as_view(template_name="CountingLog/CountSix.html"),name="holdcount"),
    url(r'^DepartmentLog/deptlogsix/', TemplateView.as_view(template_name="DepartmentLog/DeptlogSix.html"),name="deptlogsix"),


    
]
