from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users import models


@admin.register(models.User)
class UserConfig(UserAdmin):
    add_form_template = "admin/auth/user/add_form.html"
    search_fields = ('email', 'username', 'contact_no')
    list_filter = ('is_active','is_verified')
    list_display = ('username','email','first_name','last_name','is_active')

    fieldsets = (
        ('Personal Info', {'fields': ('first_name','last_name')}),
        ('Contact Info', {'fields': ('contact_no','email')}),
        ('Credentials', {'fields':('username','password')}),
        ('Status',{'fields':('is_active','is_verified','last_login')}),
    )

    add_fieldsets = (
        ('Personal Info',{'classes':('wide',),
        'fields':('first_name','last_name')}),
        ('Contact Info',{'classes':('wide',),
        'fields':('contact_no','email')}),
        ('Credentials',{'classes':('wide',),
        'fields':('username','password')}),
        ('Status',{'classes':('wide',),
        'fields':('is_active', 'is_verified')}),
    )
