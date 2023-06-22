from django.urls import path,include
from admin_dash import views

urlpatterns = [
    #CREATE
    path('addbranch', views.addbranch, name="addbranch"),
    path('adduser', views.adduser, name="adduser"),

    #READ
    path('admindash', views.admindash, name="admindash" ),
    path('branches', views.branches, name="branches"),
    path('roles', views.roles, name="roles"),

    #UPDATE
    path('viewbranch/<branch_id>', views.viewbranch, name="viewbranch"),
    path('viewuser/<user_id>', views.viewuser, name="viewuser"),

    #DELETE
    path('deleteuser/<user_id>', views.deleteuser, name="deleteuser"),
    path('deletebranch/<branch_id>', views.deletebranch, name="deletebranch"),
]
