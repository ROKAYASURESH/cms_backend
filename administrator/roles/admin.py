# admin.py
from django.contrib import admin
from .models import Roles

@admin.register(Roles)
class Rolesadmin(admin.ModelAdmin):
    list_display = ('role_name', 'descriptions', 'isRole')
    list_filter = ('role_name',)
    search_fields = ('id',)
    ordering = ('role_name',)