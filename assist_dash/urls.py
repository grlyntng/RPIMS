from django.urls import path
from assist_dash import views

urlpatterns = [
    path('assistdash', views.assistdash, name="assistdash"),
    path('suppliers', views.suppliers, name="suppliers"),
    path('searchsupplier', views.searchsupplier, name="searchsupplier"),
    path('addsupplier', views.addsupplier, name="addsupplier"),
    path('editsupplier/<supplier_id>', views.editsupplier, name="editsupplier"),

    path('orders', views.orders, name="orders"),
    path('placeorder', views.placeorder, name="placeorder"),
    path('searchorder/', views.searchorder, name="searchorder"),
    path('vieworder/<id>', views.vieworder, name="vieworder"),


    path('inventory', views.inventory, name="inventory"),
    path('addproduct', views.addproduct, name="addproduct"),
    path('searchproduct', views.searchproduct, name="searchproduct"),

    path('checkout/', views.checkout, name="checkout"),
    path('order_confirmation/<int:sale_id>/', views.order_confirmation, name='order_confirmation'),
]


