from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0002_company_employee_phone_number_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='position',
            name='job_description',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]