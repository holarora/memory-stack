from django.contrib import admin
from .models import Task

# Register your models here.


class TaskAdmin(admin.ModelAdmin):
    readonly_fields = ("slug",)
    list_filter = (
        "taskName",
        "duedate",
    )
    list_display = (
        "taskName",
        "duedate",
    )


admin.site.register(Task, TaskAdmin)
