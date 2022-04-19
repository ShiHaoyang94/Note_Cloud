from django.contrib import admin

# Register your models here.
from user.models import User


class UserManager(admin.ModelAdmin):
    list_display = ['username','email','creatd_time','updated_time','is_active','password']
    list_display_links = ['username']
    readonly_fields = ['username','email','creatd_time','updated_time','password']
admin.site.register(User, UserManager)