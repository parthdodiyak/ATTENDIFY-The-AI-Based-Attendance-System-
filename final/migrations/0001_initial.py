# Generated by Django 5.0.1 on 2024-02-20 17:56

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Faculty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('password', models.CharField(max_length=128)),
                ('department', models.CharField(max_length=100)),
                ('forgot_password_token', models.CharField(blank=True, max_length=100, null=True)),
                ('last_login', models.DateTimeField(auto_now=True, null=True)),
                ('faculty_id', models.CharField(blank=True, default='some_default_value', max_length=20, null=True, unique=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('enrollmentNumber', models.CharField(max_length=50)),
                ('user_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('password', models.CharField(max_length=100)),
                ('face_encoding', models.TextField()),
                ('last_login', models.DateTimeField(auto_now=True)),
                ('student_id', models.CharField(blank=True, default='some_default_value', max_length=20, null=True, unique=True)),
                ('forgot_password_token', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AttendanceRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('attendance_date', models.DateField(default=django.utils.timezone.now)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='final.student')),
            ],
        ),
    ]
