from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator #used to constrain age range
from admin_dash.models import Branch_Location

type_choices=(
    ("Low Stock","Low Stock"),
    ("Near Expiration", "Near Expiration"),
    ("Expired","Expired"),
    ("default","default"),
)

class Notification(models.Model):
    #using the built in django id as pk
    Notification_Type = models.CharField(max_length=25, choices=type_choices, default="default")
    Notification_Content = models.TextField(max_length=255)
    branch = models.ForeignKey(Branch_Location, on_delete=models.CASCADE, default = "1")

    def __str__(self):
        return self.Notification_Content