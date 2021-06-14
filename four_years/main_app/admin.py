from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
from .forms import *


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User

    list_display = ('email', 'is_staff', 'is_active',)
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
        ('Personal information', {'fields': ['first_name', 'last_name', 'patronymic', 'date_of_birth', 'series_passport', 'number_passport', 'school']}),

    )

    search_fields = ('email',)
    ordering = ('email',)


admin.site.register(ApplicationForm)
admin.site.register(Choice)
admin.site.register(Address)
admin.site.register(User, CustomUserAdmin)
