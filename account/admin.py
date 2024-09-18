from django.contrib import admin
from .models import User, InstituteProfile, StudentProfile, FreelanceProfile

admin.site.register(User)
admin.site.register(InstituteProfile)
admin.site.register(StudentProfile)
admin.site.register(FreelanceProfile)
