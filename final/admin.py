from django.contrib import admin

# Register your models here.
from final.models import Student
from final.models import Faculty
from final.models import AttendanceRecord

admin.site.register(Student)
admin.site.register(Faculty)
admin.site.register(AttendanceRecord)





