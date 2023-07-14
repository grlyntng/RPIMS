from .models import Supplier, Order_Stock,Product
from django.forms import ModelForm
from .widgets import DatePickerInput,TimePickerInput
from django import forms


class addsupplierform(ModelForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['branch'].initial = user.branch #auto branch option to current branch
        for field in self.fields.values():
            field.help_text = ''
            
    class Meta:
        model = Supplier
        fields = (
            "Supplier_Name",
            "Supplier_Rating",
            "Supplier_Description",
            "Supplier_Phone",
            "Supplier_Email",
            "branch",
        )


class editorderform(ModelForm):
    
    class Meta:
        model = Order_Stock
        fields = (
            'Order_Status',
        )
        labels = {
            'Order_Status':'STATUS',
        }

class editsupplierform(ModelForm):
    def __init__(self, *args, **kwargs):
        super(editsupplierform, self).__init__(*args, **kwargs)

        for fieldname in ['Supplier_Email','Supplier_Rating','Supplier_Description','Supplier_Phone']:
            self.fields[fieldname].help_text = None

    class Meta:
        model = Supplier
        fields = (
            "Supplier_Rating",
            "Supplier_Description",
            "Supplier_Phone",
            "Supplier_Email",
        )


class placeorderform(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['branch'].initial = user.branch #auto branch option to current branch
        for field in self.fields.values():
            field.help_text = ''

    class Meta:
        model = Order_Stock
        fields = (
            "Order_Quantity",
            "Order_Name",
            "Order_Total",
            "Order_Date",
            "Order_Time",
            "supplier",
            "branch",
        )

        widgets = {
            "Order_Date" : DatePickerInput(),
            "Order_Time" : TimePickerInput(),
        }

from .barcode_utils import generate_ean13_barcode
from random import randint

class addproductform(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['branch'].initial = user.branch #auto branch option to current branch
        for field in self.fields.values():
            field.help_text = ''

    def generate_unique_barcode(self):
        while True:
            Product_Barcode= str(randint(1000000000000, 9999999999999))
            if not Product.objects.filter(Product_Barcode=Product_Barcode).exists():
                return Product_Barcode
    def save(self, commit=True):
        product = super().save(commit=False)
        product.Product_Barcode = self.generate_unique_barcode()
        
        if commit:
            product.save()

        # Generate and save the barcode image
        output_path = f"static/barcodes/{product.Product_Barcode}"
        generate_ean13_barcode(product.Product_Barcode, output_path)
        product.save()
        return product

    class Meta:
        model = Product
        fields = (
            "Product_Name",
            "Brand",
            "Product_Price",
            "Unit_Dose",
            "Product_Category",
            "Form",
            "Product_Quantity",
            "Product_Expirydate",
            "branch",
        )

        labels = {
            "Product_Name":"NAME",
            "Brand": "BRAND",
            "Product_Price" : "PRICE",
            "Unit_Dose": "UNIT DOSE",
            "Product_Category": "CATEGORY",
            "Form":"FORM",
            "Product_Quantity":"QUANTITY",
            "Product_Expirydate":"EXPIRATION DATE",
            "branch":"BRANCH",
        }

        widgets = {
            "Product_Expirydate" : DatePickerInput(),
        }