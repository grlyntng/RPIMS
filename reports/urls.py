from django.urls import path
from reports import views

urlpatterns = [
    path('adminreports', views.adminreports, name="adminreports"),
    path('pharmacistreports', views.pharmacistreports, name="pharmacistreports"),
    path('salesreports', views.salesreports, name="salesreports"),
    path('suppliersreports', views.supplierreports, name="supplierreports"),
    path('inventoryreports', views.inventoryreports, name="inventoryreports"),

]
