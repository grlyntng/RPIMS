from django.db import models
from admin_dash.models import Branch_Location
from django.core.validators import MaxValueValidator, MinValueValidator
from .barcode_utils import generate_ean13_barcode
status_choices=(
    ("In Progress","In Progress"),
    ("Completed","Completed"),
    ("Cancelled","Cancelled"),
)

category_choices=(
    ("Supplement","Supplement"),
    ("Prescription Medication","Prescription Medication"),
    ("OTC Medication","OTC Medication"),
    ("Personal Care and Hygiene Products","Personal Care and Hygiene Products"),
    ("First Aid and Medical Supplies","First Aid and Medical Supplies"),
    ("Baby Care Products","Baby Care Products"),
    ("Mobility Aids","Mobility Aids"),
    ("Oral Health", "Oral Health"),
    ("Eye and Ear Care", "Eye and Ear Care"),
    ("Diagnostic Tests and Medical Devices","Diagnostic Tests and Medical Devices"),
    ("Others","Others"),
)


form_choices = (
    ("Tablet","Tablet"),
    ("Capsule","Capsule"),
    ("Liquid","Liquid"),
    ("Syrup","Syrup"),
    ("Lozenge","Lozenge"),
    ("Topical Creams and Ointments","Topical Creams and Ointments"),
    ("Patches","Patches"),
    ("Inhalers and Nasal Sprays","Inhalers and Nasal Sprays"),
    ("Powder","Powder"),
    ("Drops","Drops"),
    ("Injectable","Injectable"),
    ("Effervescent Tablet","Effervescent Tablet"),
    ("-","-"),
)

method_choices = (
    ("e-Wallet","e-Wallet"),
    ("Credit Card","Credit Card"),
    ("Debit Card","Debit Card"),
    ("Cash","Cash"),
)


# Create your models here.
class Supplier(models.Model):
    #using the built in django id as pk
    Supplier_Name = models.CharField(max_length=100)
    Supplier_Rating = models.DecimalField(max_digits=2, decimal_places=1,default = 1, validators=[MaxValueValidator(5), MinValueValidator(1)])
    Supplier_Description = models.TextField(max_length=255)
    Supplier_Phone =  models.IntegerField(default = 1, validators=[MaxValueValidator(6000000000000), MinValueValidator(6000000000)])
    Supplier_Email = models.EmailField(max_length=255)
    branch = models.ForeignKey(Branch_Location, on_delete=models.CASCADE, default = "1")

    def __str__(self):
        return self.Supplier_Name
    
class Product(models.Model):
    #using the built in django id as pk
    Product_Category = models.CharField(max_length=50, choices=category_choices,default="Others")
    Product_Name = models.CharField(max_length=100)
    Product_Expirydate = models.DateField(null=True)
    Product_Barcode = models.CharField(max_length=13)
    Product_Price = models.DecimalField(max_digits=1000, decimal_places=2,default = 1, validators=[ MinValueValidator(1)])
    Product_Quantity = models.IntegerField(default=1,validators=[ MinValueValidator(1)])
    Unit_Dose = models.CharField(max_length=50)
    Brand = models.CharField(max_length=100) 
    Form = models.CharField(max_length=50, choices=form_choices,default="-")
    branch = models.ForeignKey(Branch_Location, on_delete=models.CASCADE, default = "1")

    def __str__(self):
        return f'{self.Product_Name}'


class Order_Stock(models.Model):
    #using the built in django id as pk
    Order_Quantity = models.IntegerField(default = 1, validators=[MaxValueValidator(1000), MinValueValidator(1)])
    Order_Name = models.TextField(max_length=50)
    Order_Total = models.DecimalField(max_digits=1000, decimal_places=2,default = 1, validators=[ MinValueValidator(1)])
    Order_Date = models.DateField(null=True)
    Order_Time = models.TimeField(null=True)
    Order_Status = models.CharField(max_length=50, choices=status_choices,default="In Progress")
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE,default="1")
    branch = models.ForeignKey(Branch_Location, on_delete=models.CASCADE, default = "1")

    def __str__(self):
        return self.Order_Name
    

class Sale(models.Model):
    #using the built in django id as pk
    Sale_total = models.DecimalField(max_digits=1000, decimal_places=2,default = 1, validators=[ MinValueValidator(1)])
    Sale_Date = models.DateField(null=True)
    Sale_Method = models.CharField(max_length=50, choices=method_choices,default="Cash")
    branch = models.ForeignKey(Branch_Location, on_delete=models.CASCADE, default = "1")

    def __str__(self):
        return f'{self.Sale_Date}-{self.id}'
    

class Sale_Detail(models.Model):
    #using the built in django id as pk
    Item_Quantity = models.IntegerField(default=1)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, default = "1")
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, default = "1")
    branch = models.ForeignKey(Branch_Location, on_delete=models.CASCADE, default = "1")

    def __str__(self):
        return f'{self.branch}-{self.id}'