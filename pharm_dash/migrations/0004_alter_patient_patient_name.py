# Generated by Django 4.2.1 on 2023-06-05 08:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pharm_dash', '0003_alter_patient_patient_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='Patient_Name',
            field=models.CharField(max_length=100),
        ),
    ]
