from django.contrib import admin
from .models import Users, Tasks, Projects, Description

admin.site.register(Users)
admin.site.register(Tasks)
admin.site.register(Projects)
admin.site.register(Description)

# Register your models here.
