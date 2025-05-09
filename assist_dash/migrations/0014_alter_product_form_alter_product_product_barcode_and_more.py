# Generated by Django 4.2.1 on 2023-07-10 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assist_dash', '0013_remove_order_stock_order_datetime_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='Form',
            field=models.CharField(choices=[('Tablet', 'Tablet'), ('Capsule', 'Capsule'), ('Liquid', 'Liquid'), ('Syrup', 'Syrup'), ('Topical Creams and Ointments', 'Topical Creams and Ointments'), ('Patches', 'Patches'), ('Inhalers and Nasal Sprays', 'Inhalers and Nasal Sprays'), ('Powder', 'Powder'), ('Drops', 'Drops'), ('Injectable', 'Injectable'), ('Effervescent Tablet', 'Effervescent Tablet'), ('-', '-')], default='-', max_length=50),
        ),
        migrations.AlterField(
            model_name='product',
            name='Product_Barcode',
            field=models.ImageField(blank=True, null=True, upload_to='barcodes/'),
        ),
        migrations.AlterField(
            model_name='product',
            name='Product_Category',
            field=models.CharField(choices=[('Supplement', 'Supplement'), ('Prescription Medication', 'Prescription Medication'), ('OTC Medication', 'OTC Medication'), ('Personal Care and Hygiene Products', 'Personal Care and Hygiene Products'), ('First Aid and Medical Supplies', 'First Aid and Medical Supplies'), ('Baby Care Products', 'Baby Care Products'), ('Mobility Aids', 'Mobility Aids'), ('Oral Health', 'Oral Health'), ('Eye and Ear Care', 'Eye and Ear Care'), ('Diagnostic Tests and Medical Devices', 'Diagnostic Tests and Medical Devices'), ('Others', 'Others')], default='Others', max_length=50),
        ),
        migrations.AlterField(
            model_name='sale',
            name='Sale_Method',
            field=models.CharField(choices=[('e-Wallet', 'e-Wallet'), ('Credit Card', 'Credit Card'), ('Debit Card', 'Debit Card'), ('Cash', 'Cash')], default='Cash', max_length=50),
        ),
    ]
