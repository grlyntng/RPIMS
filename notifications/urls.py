from django.urls import path
from notifications import views

urlpatterns = [
    path('adminnotification', views.adminnotification,name="adminnotification" ),
    path('pharmacistnotification', views.pharmacistnotification,name="pharmacistnotification" ),
    path('assistantnotification', views.assistantnotification,name="assistantnotification" ),
]
