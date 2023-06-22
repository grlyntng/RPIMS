from django.db import models
from admin_dash.models import Branch_Location
from assist_dash.models import Order_Stock
# Create your models here.


class Appointment(models.Model):
    #using the built in django id as pk
    app_detail = models.TextField(max_length=255, editable = True)
    datetime_start = models.DateTimeField(null=True)
    datetime_end = models.DateTimeField(null=True)
    branch = models.ForeignKey(Branch_Location, on_delete=models.CASCADE, default = "1")
    order = models.ForeignKey(Order_Stock, on_delete=models.CASCADE, default = "1")
    def __str__(self):
        return self.app_detail
    