from django.contrib import admin
from django.urls import path,include
from final import views
from django.contrib.auth import views as auth_views
from .views import generate_attendance_pdf


urlpatterns = [
    path('', views.index,name='home'),
    path('student/', views.student, name='student'),
    path('contact/', views.contact_view, name='contact'),
    path('faculty/',views.faculty,name='faculty_registration'),
    path('register/',views.register_user,name='register'),
    path('signin/',views.signin,name='signin'),
    path('attendance/',views.attendance,name='attendance'),
    path('change_pass/',views.change_pass,name='change_pass'),
    path('forgot_pass/',views.forgot_pass,name='forgot_pass'),
    path('reset_password/<str:uidb64>/<str:token>/', views.change_pass, name='reset_password'),
    path('secreate/', views.secreate, name='secrate'),
    path('faculty_sign/', views.faculty_sign, name='faculty_sign'),
    path('take_attendance/', views.take_attendance, name='take_attendance'),
    path('faculty_view/', views.faculty_view, name='faculty_view'),
    path('succesful/', views.succesful, name='succesful'),
    path('change_pass1/',views.change_pass1,name='change_pass1'),
    path('forgot_pass1/',views.forgot_pass1,name='forgot_pass1'),
    path('reset_password1/<str:uidb64>/<str:token>/', views.change_pass1, name='reset_password1'),
    path('take_attendance',views.take_attendance,name='take_attendance'),
    path('option',views.option,name='option'),
    path('fdetail',views.fdetail,name='fdetail'),
    path('civil',views.civil,name='civil'),
    path('it',views.it,name='it'),
    path('electrical',views.electrical,name='electrical'),
    path('mechanical',views.mechanical,name='mechanical'),
    path('view_attendance/', views.view_attendance, name='view_attendance'),
    path('generate_attendance_pdf/', generate_attendance_pdf, name='generate_attendance_pdf'),

    


    
    

   

]