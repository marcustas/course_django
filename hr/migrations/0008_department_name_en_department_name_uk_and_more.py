# Generated by Django 4.2.6 on 2023-11-13 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0007_alter_position_department'),
    ]

    operations = [
        migrations.AddField(
            model_name='department',
            name='name_en',
            field=models.CharField(max_length=200, null=True, verbose_name='Name'),
        ),
        migrations.AddField(
            model_name='department',
            name='name_uk',
            field=models.CharField(max_length=200, null=True, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='company',
            name='address',
            field=models.CharField(max_length=200, verbose_name='Address'),
        ),
        migrations.AlterField(
            model_name='company',
            name='email',
            field=models.EmailField(max_length=254, verbose_name='Email'),
        ),
        migrations.AlterField(
            model_name='company',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='company',
            name='tax_code',
            field=models.CharField(max_length=200, verbose_name='Tax code'),
        ),
        migrations.AlterField(
            model_name='department',
            name='name',
            field=models.CharField(max_length=200, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='position',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='Is active'),
        ),
        migrations.AlterField(
            model_name='position',
            name='is_manager',
            field=models.BooleanField(default=False, verbose_name='Is manager'),
        ),
        migrations.AlterField(
            model_name='position',
            name='monthly_rate',
            field=models.IntegerField(default=0, verbose_name='Monthly rate'),
        ),
    ]
