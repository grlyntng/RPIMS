from django.urls import path,include
from users import views

urlpatterns = [
    path('', views.login_user, name="login_user"),
    path('logout_user', views.logout_user, name="logout" ),

]
