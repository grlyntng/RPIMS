# Generated by Django 4.2.1 on 2023-07-10 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='Notification_Type',
            field=models.CharField(choices=[('Low Stock', 'Low Stock'), ('Near Expiration', 'Near Expiration'), ('Expired', 'Expired'), ('default', 'default')], default='default', max_length=25),
        ),
    ]
