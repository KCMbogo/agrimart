from django.contrib import admin
from userauths.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_superuser', 'last_login')

admin.site.register(User, UserAdmin)
