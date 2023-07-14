from django.shortcuts import render
from .models import Notification
from .utils import check_notifications
# Create your views here.
from django.shortcuts import render, HttpResponse, HttpResponseRedirect, redirect
from django.template import loader
from django.contrib import messages 

from assist_dash.models import Sale_Detail,Product,Sale

def adminnotification(request):
    check_notifications()
    notifications = Notification.objects.all()
    items_sold_today = adminget_items_sold_today()
    products_in_inventory = adminget_products_in_inventory()
    return render(request, 'notifications/adminnotification.html', {
        'notifications': notifications,
        'items_sold_today': items_sold_today,
        'products_in_inventory': products_in_inventory
    })

def pharmacistnotification(request):
    check_notifications()
    notifications = Notification.objects.all()
    user_branch = request.user.branch  # Assuming the branch information is stored in the user object
    items_sold_today = get_items_sold_today(user_branch)
    products_in_inventory = get_products_in_inventory(user_branch)
    return render(request, 'notifications/pharmacistnotification.html', {
        'notifications': notifications,
        'items_sold_today': items_sold_today,
        'products_in_inventory': products_in_inventory
    })


def assistantnotification(request):
    check_notifications()
    notifications = Notification.objects.all()
    user_branch = request.user.branch  # Assuming the branch information is stored in the user object
    items_sold_today = get_items_sold_today(user_branch)
    products_in_inventory = get_products_in_inventory(user_branch)
    return render(request, 'notifications/assistantnotification.html', {
        'notifications': notifications,
        'items_sold_today': items_sold_today,
        'products_in_inventory': products_in_inventory
    })

from django.db.models import Sum
from datetime import date

def get_items_sold_today(user_branch):
    today = date.today()
    items_sold = Sale_Detail.objects.filter(
        sale__Sale_Date=today,
        branch=user_branch
    ).aggregate(total_quantity=Sum('Item_Quantity'))
    return items_sold['total_quantity'] if items_sold['total_quantity'] else 0

def get_products_in_inventory(user_branch):
    products_in_inventory = Product.objects.filter(branch=user_branch).aggregate(total_quantity=Sum('Product_Quantity'))
    return products_in_inventory['total_quantity'] if products_in_inventory['total_quantity'] else 0


def adminget_items_sold_today():
    today = date.today()
    items_sold = Sale_Detail.objects.filter(sale__Sale_Date=today).aggregate(total_quantity=Sum('Item_Quantity'))
    return items_sold['total_quantity'] if items_sold['total_quantity'] else 0

def adminget_products_in_inventory():
    products_in_inventory = Product.objects.aggregate(total_quantity=Sum('Product_Quantity'))
    return products_in_inventory['total_quantity'] if products_in_inventory['total_quantity'] else 0