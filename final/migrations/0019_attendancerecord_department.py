# Generated by Django 5.0.1 on 2024-03-06 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('final', '0018_student_department'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendancerecord',
            name='department',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
