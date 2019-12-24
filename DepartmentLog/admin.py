from django.contrib import admin


from import_export.admin import ImportExportModelAdmin
from import_export import resources

from django.http import HttpResponse


from .models import DepartmentLog, DepartmentLogUsers

class DepartmentLogResource(resources.ModelResource):
    
    class Meta:
        model = DepartmentLog
        fields = ('LotNo')  
        
class DepartmentLogAdmin(ImportExportModelAdmin):
    
    resource_class = DepartmentLogResource

    list_filter = ('Date','EmployeName','Department','WrongLocation',)
    search_fields = ('LotNo',)
    list_display = ('LotNo', 'Date','EmployeName','Department','WrongLocation',)


class DepartmentLogUsersResource(resources.ModelResource):
    
    class Meta:
        model = DepartmentLogUsers
        fields = ('listNumber', 'userName','userActive',)  
        
class DepartmentLogUsersAdmin(ImportExportModelAdmin):
    
    resource_class = DepartmentLogUsersResource

    list_filter = ('listNumber', 'userName','userActive',) 
    search_fields = ('listNumber',)
    list_display = ('listNumber', 'userName','userActive',) 



admin.site.register(DepartmentLogUsers, DepartmentLogUsersAdmin)
admin.site.register(DepartmentLog, DepartmentLogAdmin)