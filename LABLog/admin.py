from django.contrib import admin


from import_export.admin import ImportExportModelAdmin
from import_export import resources

from django.http import HttpResponse


from .models import LABLog

class LABLogResource(resources.ModelResource):
    
    class Meta:
        model = LABLog
        fields = ('LotNo')  
        
class LABLogAdmin(ImportExportModelAdmin):
    
    resource_class = LABLogResource

    list_filter = ('LotNo',)
    search_fields = ('LotNo',)
    list_display = ('LotNo', 'VisualNotClosed','Notes','OpNumOpen',)


admin.site.register(LABLog, LABLogAdmin)