from django.contrib import admin
from .models import User, Task

admin.site.register(Task)
admin.site.register(User)
