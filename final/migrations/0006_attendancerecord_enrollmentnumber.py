# Generated by Django 5.0.1 on 2024-02-21 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('final', '0005_alter_student_student_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendancerecord',
            name='enrollmentNumber',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
