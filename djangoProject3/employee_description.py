from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0003_company'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='phone_number',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='position',
            name='job_description',
            field=models.TextField(default='do your best'),
        ),
    ]