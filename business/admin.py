from django.contrib import admin

from business import models as BModel


@admin.register(BModel.OrgType)
class OrgTypeConfig(admin.ModelAdmin):
    list_display = ['entity','doc','verified','pending']

    def verified(self, instance):
        return BModel.Org.objects.filter(type=instance, is_verified=True).count()
    
    def pending(self, instance):
        return BModel.Org.objects.filter(type=instance, is_verified=False).count()
    

class OrgEmpAdmin(admin.TabularInline):
    model = BModel.OrgEmp
    extra = 0

@admin.register(BModel.Org)
class OrgConfig(admin.ModelAdmin):
    list_display = ['name','reg_no','type','is_active','is_verified','msg']
    list_filter = ['type','is_active','is_verified']
    search_fields = ['name','reg_no']
    raw_id_fields = ['type']
    inlines = [OrgEmpAdmin]
