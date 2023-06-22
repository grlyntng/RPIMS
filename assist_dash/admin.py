from django.contrib import admin

# Register your models here.
from .models import Supplier
admin.site.register(Supplier)

from .models import Product
admin.site.register(Product)

from .models import Order_Stock
admin.site.register(Order_Stock)

from .models import Sale
admin.site.register(Sale)

from .models import Sale_Detail
admin.site.register(Sale_Detail)