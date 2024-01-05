from django.contrib import admin
from .models import tarea

class tareaAdmin(admin.ModelAdmin):
    readonly_fields = ("created", )

# Register your models here.
admin.site.register(tarea, tareaAdmin)