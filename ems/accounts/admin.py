from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + (
        ('Campi Personalizzati', {'fields': ('birth_date', 'organization')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)