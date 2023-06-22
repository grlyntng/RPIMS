from .models import Supplier, Order_Stock,Product
from django.forms import ModelForm
from .widgets import DatePickerInput

class addsupplierform(ModelForm):
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


class placeorderform(ModelForm):
    class Meta:
        model = Order_Stock
        fields = (
            "Order_Quantity",
            "Order_Name",
            "Order_Total",
            "Order_Date", #use widget
            "Order_Status",
            "supplier",
            "branch",
        )

        widgets = {
            "Order_Date" : DatePickerInput(),
        }

class addproductform(ModelForm):
    class Meta:
        model = Product
        fields = (
            "Product_Name",
            "Brand",
            "Product_Price",
            "Unit_Dose",
            "Product_Barcode",
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
            "Product_Barcode":"BARCODE",
            "Product_Category": "CATEGORY",
            "Form":"FORM",
            "Product_Quantity":"QUANTITY",
            "Product_Expirydate":"EXPIRATION DATE",
            "branch":"BRANCH",
        }

        widgets = {
            "Product_Expirydate" : DatePickerInput(),
        }