# Generated by Django 5.0.1 on 2024-02-27 08:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('final', '0007_attendancerecord_faculty_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='enrollmentNumber',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
