from django.contrib import admin
from .models import User,Profil,Avatar
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _

class UserAdmin(BaseUserAdmin):
    list_display = ('email','last_name','first_name', 'is_staff','is_active',)
    list_filter = ('is_staff', 'is_active','groups')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name','avatar')}),
        ('Important dates', {'fields': ('last_login',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name','last_name','avatar','password1', 'password2','is_staff','is_superuser',),
        }),
    )
    
    ordering = ('is_active',)
    search_fields = ('email', 'first_name','last_name')

admin.site.register(User,UserAdmin)
admin.site.register(Profil,)
admin.site.register(Avatar,)
