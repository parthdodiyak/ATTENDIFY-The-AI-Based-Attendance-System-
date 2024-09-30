from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.utils import timezone 





# Create your models here.
class Student(AbstractBaseUser):
    enrollmentNumber= models.CharField(max_length=50,unique=True)
    department = models.CharField(max_length=100,blank=True, null=True)
    user_name = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=100)
    face_encoding = models.TextField()
    last_login = models.DateTimeField(auto_now=True)
    student_id = models.CharField(max_length=20, unique=True,null=True, blank=True)
    forgot_password_token = models.CharField(max_length=100, blank=True, null=True)
    
    
    

   


    def __str__(self):
        return self.user_name

class Faculty(AbstractBaseUser):
    user_name = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=128)
    department = models.CharField(max_length=100,blank=True, null=True)
    forgot_password_token = models.CharField(max_length=100, blank=True, null=True)
    last_login = models.DateTimeField(auto_now=True, null=True, blank=True )
    faculty_id = models.CharField(max_length=20, unique=True,null=True, blank=True)
    
    '''def save(self, *args, **kwargs):
        # Hash the password before saving
        if self.password:
            self.password = make_password(self.password)
        super().save(*args, **kwargs)'''

    def __str__(self):
        return self.user_name

class AttendanceRecord(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    enrollmentNumber = models.CharField(max_length=50,blank=True, null=True)
    timestamp = models.DateTimeField(default=timezone.now)
    attendance_date = models.DateField(default=timezone.now)  # Add this line
    semester = models.CharField(max_length=50,blank=True, null=True)  # New field for semester
    faculty_name = models.CharField(max_length=100,blank=True, null=True)  # New field for faculty name
    time_slot = models.CharField(max_length=50,blank=True, null=True)  # New field for time slot
    lecture_name = models.CharField(max_length=100,blank=True, null=True) 
    department = models.CharField(max_length=100,blank=True, null=True)

    def __str__(self):
        return f"{self.student.user_name} - {self.enrollmentNumber} - {self.timestamp}"
