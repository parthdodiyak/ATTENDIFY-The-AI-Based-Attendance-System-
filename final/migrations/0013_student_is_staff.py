# Generated by Django 5.0.1 on 2024-03-01 05:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('final', '0012_remove_student_is_active_remove_student_is_staff'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
    ]
