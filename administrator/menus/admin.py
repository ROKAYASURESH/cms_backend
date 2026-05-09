# admin.py
from django.contrib import admin
from .models import Menu

@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ('title', 'parent', 'position', 'publish')
    list_filter = ('publish',)
    search_fields = ('title',)
    ordering = ('position',)
