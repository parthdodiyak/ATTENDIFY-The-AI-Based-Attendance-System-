# Generated by Django 5.0.1 on 2024-02-29 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('final', '0008_alter_student_enrollmentnumber'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='student',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
    ]
