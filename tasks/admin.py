from django.contrib import admin
from .models import Task

# Register your models here.
class TaskAdmin(admin.ModelAdmin):
  readonly_fields = ('fecha_creacion','fecha_completada')

admin.site.register(Task, TaskAdmin)