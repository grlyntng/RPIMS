from django.contrib.auth.models import AbstractUser
from django.db import models

from admin_dash.models import Branch_Location
 
# User class
# AbstractUser class inherits the User class and is used to add additional fields required for your User 
# in the database itself. So, it changes the schema of the database.
role_choices = (
    ("ADMIN", "Admin"),
    ("PHARMACIST", "Pharmacist"),
    ("ASSISTANT", "Assistant"),
)

class User(AbstractUser): 
    role = models.CharField(max_length=20, choices=role_choices, default="Assistant",editable=True)
    branch = models.ForeignKey(Branch_Location, on_delete=models.CASCADE, default = "1")

    def __str__(self):
        return self.username
    