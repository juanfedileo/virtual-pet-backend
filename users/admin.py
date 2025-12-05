
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    # 1. Agregamos los campos a la vista de "Lista" (la tabla de usuarios)
    list_display = (
        'username', 'email', 'first_name', 'last_name', 
        'role', 'is_staff', 'notification_channels'
    )

    # 2. Agregamos los campos al formulario de "Edición"
    # UserAdmin.fieldsets es la configuración por defecto. Le sumamos un bloque extra.
    fieldsets = UserAdmin.fieldsets + (
        ('Información Extra de VirtualPet', {
            'fields': ('role', 'address', 'phone', 'notification_channels'),
        }),
    )

    # 3. También al formulario de "Crear Usuario"
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {
            'classes': ('wide',),
            'fields': ('role', 'address', 'phone', 'notification_channels'),
        }),
    )

# Registramos el modelo con nuestra configuración personalizada
admin.site.register(User, CustomUserAdmin)

# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
# from .models import User

# @admin.register(User)
# class CustomUserAdmin(UserAdmin):
#     model = User
#     list_display = ('username', 'email', 'role', 'is_staff', 'is_active')
#     list_filter = ('role', 'is_staff', 'is_active')
#     fieldsets = (
#         (None, {'fields': ('username', 'password')}),
#         ('Personal info', {'fields': ('email',)}),
#         ('Roles', {'fields': ('role',)}),
#         ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
#         ('Important dates', {'fields': ('last_login', 'date_joined')}),
#     )
