from django.contrib import admin

# Register your models here.
from users.models import User, UserVerificationCode


class UserAdminModel(admin.ModelAdmin):
    list_display = ['username', 'email']

admin.site.register(User, UserAdminModel)