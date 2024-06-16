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




