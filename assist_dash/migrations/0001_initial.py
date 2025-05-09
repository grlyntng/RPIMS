# Generated by Django 4.2.1 on 2023-06-05 11:57

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('admin_dash', '0002_alter_branch_location_branch_name_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Supplier_Name', models.CharField(max_length=100)),
                ('Supplier_Rating', models.DecimalField(decimal_places=2, default=1, max_digits=3, validators=[django.core.validators.MaxValueValidator(5), django.core.validators.MinValueValidator(1)])),
                ('Supplier_Description', models.TextField(max_length=255)),
                ('Supplier_Phone', models.IntegerField(default=1, validators=[django.core.validators.MaxValueValidator(6000000000000), django.core.validators.MinValueValidator(6000000000)])),
                ('branch', models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, to='admin_dash.branch_location')),
            ],
        ),
    ]
