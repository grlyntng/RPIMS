from django.urls import path
from reports import views

urlpatterns = [
    
    path('pharmacistreports', views.pharmacistreports, name="pharmacistreports"),
    path('salesreports', views.salesreports, name="salesreports"),
    path('suppliersreports', views.supplierreports, name="supplierreports"),
    path('inventoryreports', views.inventoryreports, name="inventoryreports"),

    path('adminreports', views.adminreports, name="adminreports"),
    path('admininventoryreports', views.admininventoryreports, name="admininventoryreports"),
    path('adminsalesreports', views.adminsalesreports, name="adminsalesreports"),
    path('adminsuppliersreports', views.adminsupplierreports, name="adminsupplierreports"),

]
