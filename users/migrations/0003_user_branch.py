# Generated by Django 4.2.1 on 2023-06-03 16:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('admin_dash', '0002_alter_branch_location_branch_name_and_more'),
        ('users', '0002_alter_user_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='branch',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, to='admin_dash.branch_location'),
        ),
    ]
