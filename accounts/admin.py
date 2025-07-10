from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from django.contrib.admin import AdminSite


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + (
        ('Campi Personalizzati', {'fields': ('birth_date', 'organization')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)

class MyAdminSite(AdminSite):
    class Media:
        css = {
            'all': ('css/custom_admin.css',)
        }

admin.site = MyAdminSite()