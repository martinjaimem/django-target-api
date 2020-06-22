from django.contrib import admin
from applications.users.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'date_joined', 'last_login')
    fieldsets = [
        (None, { 'fields': ['name', 'email', 'password', 'gender', ] }),
        ('Advanced information', { 'fields': ['is_staff', 'is_superuser', 'is_active', ] }),
    ]
    search_fields = ['email', 'name']

admin.site.register(User, UserAdmin)
