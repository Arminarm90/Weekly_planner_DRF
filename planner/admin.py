from django.contrib import admin
from .models import Task, Day, Week

admin.site.register(Task)
admin.site.register(Day)
admin.site.register(Week)