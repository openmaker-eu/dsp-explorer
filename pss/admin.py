from django.contrib import admin
from .models import Application


class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('profile', 'les', 'project_name', 'created_at')
    search_fields = ('profile', 'les', 'project_name')

admin.site.register(Application, ApplicationAdmin)
