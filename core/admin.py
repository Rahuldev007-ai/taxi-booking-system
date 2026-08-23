from django.contrib import admin
from .models import AdminUser,User
# Register your models here.

admin.site.register(AdminUser)
admin.site.register(User)