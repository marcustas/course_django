from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0002_position_is_active'),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('address', models.CharField(max_length=512)),
                ('email', models.EmailField(max_length=254)),
                ('tax_code', models.CharField(max_length=256)),
            ],
        ),
    ]