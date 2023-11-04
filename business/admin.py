from django.contrib import admin

from business import models as BModel


@admin.register(BModel.OrgDocType)
class OrgDocTypeConfig(admin.ModelAdmin):
    list_display = ['doc','doc_no','is_doc']


@admin.register(BModel.OrgType)
class OrgTypeConfig(admin.ModelAdmin):
    list_display = ['entity','doc_type','verified','pending']

    def verified(self, instance):
        return BModel.Org.objects.filter(type=instance, is_verified=True).count()
    
    def pending(self, instance):
        return BModel.Org.objects.filter(type=instance, is_verified=False).count()
    

class OrgEmpAdmin(admin.TabularInline):
    model = BModel.OrgEmp
    extra = 0
    fields = ['user','join_date','is_manager']

class OrgDocAdmin(admin.TabularInline):
    model = BModel.OrgDoc
    extra = 0


@admin.register(BModel.Org)
class OrgConfig(admin.ModelAdmin):
    list_display = ['name','type',]
    list_filter = ['type','is_active','is_verified']
    search_fields = ['name',]
    raw_id_fields = ['type']
    inlines = [OrgEmpAdmin,OrgDocAdmin]
