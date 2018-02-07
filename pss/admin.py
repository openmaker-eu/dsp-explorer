from django.contrib import admin
from .models import Application


class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('les', 'project_name', 'created_at')
    search_fields = ('les', 'project_name')


admin.site.register(Application, ApplicationAdmin)
