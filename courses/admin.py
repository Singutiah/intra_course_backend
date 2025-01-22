from django.contrib import admin


from .models import Course, College, Department, School
# Register your models here.
admin.site.register(Course)
admin.site.register(College)
admin.site.register(Department)
admin.site.register(School)
