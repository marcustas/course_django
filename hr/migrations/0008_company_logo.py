# Generated by Django 4.2.6 on 2023-11-11 20:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0007_employee_avatar_employee_cv_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='logo',
            field=models.ImageField(blank=True, null=True, upload_to='logo/'),
        ),
    ]