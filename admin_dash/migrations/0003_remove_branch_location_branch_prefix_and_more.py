# Generated by Django 4.2.1 on 2023-06-14 15:25

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_dash', '0002_alter_branch_location_branch_name_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='branch_location',
            name='Branch_prefix',
        ),
        migrations.AddField(
            model_name='branch_location',
            name='Branch_phonenumber',
            field=models.IntegerField(default=1, validators=[django.core.validators.MaxValueValidator(6000000000000), django.core.validators.MinValueValidator(6000000000)]),
        ),
    ]
