from django.db import models
from admin_dash.models import Branch_Location
from assist_dash.models import Order_Stock
# Create your models here.


class Appointment(models.Model):
    #using the built in django id as pk
    app_detail = models.TextField(max_length=255, editable = True)
    date = models.DateField(null=True)
    time_start = models.TimeField(null=True)
    branch = models.ForeignKey(Branch_Location, on_delete=models.CASCADE, default = "1")
   
    def __str__(self):
        return self.app_detail
    