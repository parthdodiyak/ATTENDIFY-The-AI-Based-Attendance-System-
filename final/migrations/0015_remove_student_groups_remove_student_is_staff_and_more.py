# Generated by Django 5.0.1 on 2024-03-01 05:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('final', '0014_student_groups_student_is_superuser_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='groups',
        ),
        migrations.RemoveField(
            model_name='student',
            name='is_staff',
        ),
        migrations.RemoveField(
            model_name='student',
            name='is_superuser',
        ),
        migrations.RemoveField(
            model_name='student',
            name='user_permissions',
        ),
    ]
