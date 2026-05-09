from django.contrib import admin

from .models import SetPermission

@admin.register(SetPermission)
class SetPermissionAdmin(admin.ModelAdmin):
    list_display = ('role', 'menu', 'permission_type', 'has_permission')
    list_filter = ('role', 'menu')
    search_fields = ('role__role_name', 'menu__title')
    ordering = ('role__role_name', 'menu__title')