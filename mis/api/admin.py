from django.contrib import admin
from .models import Class, Department, Year, Shift, Teacher, TimingField, Period, Subject

# # Register your models here.

# admin.site.register(Book)

admin.site.register(Department)
admin.site.register(Year)
admin.site.register(Class)
admin.site.register(Shift)
admin.site.register(Teacher)
admin.site.register(TimingField)
admin.site.register(Period)
admin.site.register(Subject)

from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('email', 'role', 'is_staff', 'is_active',)
    list_filter = ('email', 'role', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('role', 'is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'role', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)

admin.site.register(User, CustomUserAdmin)




