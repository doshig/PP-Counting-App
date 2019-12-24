from django.contrib import admin


from import_export.admin import ImportExportModelAdmin
from import_export import resources
import csv
from django.http import HttpResponse

from .models import CountLog, ResourceLog, Pipeline

class CountLogResource(resources.ModelResource):
    
    class Meta:
        model = CountLog
        fields = ('LotNo')  
        
class ResourceLogResource(resources.ModelResource):
    
    class Meta:
        model = ResourceLog
        fields = ('PortEntry', 'ResourceID',)
        
class PipelineResource(resources.ModelResource):
    
    class Meta:
        model = Pipeline
        fields = ('workOrder', 'opSequenceFrom', 'opSequenceTo',)
        
#class PipelineCountResource(resources.ModelResource):
#    
#    class Meta:
#        model = PipelineCount
#        fields = ('countNumber', 'quantity',)
        
class PipelineAdmin(ImportExportModelAdmin):
    
    resource_class = PipelineResource
    list_filter = ('workOrder',)
    list_display = ('workOrder', 'opSequenceFrom', 'opSequenceTo',)
    
#class PipelineCountAdmin(ImportExportModelAdmin):
#    
#    resource_class = PipelineCountResource
#    list_filter = ('countNumber',)
#    list_display = ('countNumber', 'quantity',)
        
class CountLogAdmin(ImportExportModelAdmin):
    
    resource_class = CountLogResource

    list_filter = ('EmployeName','DateCount','LotNo',)
    search_fields = ('LotNo',)
    list_display = ('LotNo','EmployeName','DateCount','MoveTo','Quantity','MissedClockOut',)
    actions = ["export_as_csv"]
    
    def export_as_csv(self, request, queryset):

        meta = self.model._meta
        field_names = [field.name for field in meta.fields]
    
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)
    
        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])
    
        return response


class ResourceLogAdmin(ImportExportModelAdmin):
    
    resource_class = ResourceLogResource
    
    list_filter = ('ResourceID', 'PortEntry',)
    search_fields = ('ResourceID', 'PortEntry') #searches both parts of model in one search bar
    list_display = ('PortEntry', 'ResourceID',) #Shows both in colum on admin page for entry
#    list_filter = ('PortEntry')
    



admin.site.register(CountLog, CountLogAdmin)
admin.site.register(ResourceLog, ResourceLogAdmin)
admin.site.register(Pipeline, PipelineAdmin)
#admin.site.register(PipelineCount, PipelineCountAdmin)