# Generated by Django 4.2.6 on 2023-10-12 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='position',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]