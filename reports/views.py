from django.shortcuts import render, HttpResponse, HttpResponseRedirect, redirect
from django.template import loader
from django.contrib import messages 
from admin_dash.models import Branch_Location

#import models to be used in analytics and reports
from assist_dash.models import Product,Supplier,Order_Stock,Sale,Sale_Detail
from .wastereport_utils import *
from django.db.models import Sum
from datetime import datetime, timedelta
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

from datetime import datetime
from django.db.models import Sum, F, Avg
from django.db.models.functions import Coalesce
from django.db.models import DecimalField
from decimal import Decimal, ROUND_HALF_UP
from django.db import models
from django.db.models import  Sum
from datetime import date, timedelta
from django.db.models import Count, Case, When


def adminreports(request): #waste reports
    report_type = request.GET.get('report_type', 'daily')
    branch = request.GET.get('branch', 'all')

    if branch == 'all':
        # Generate the waste report for all branches
        waste_report, wasted_inventory_value = generate_waste_report(report_type)
    else:
        # Retrieve the branch based on the branch name
        branch_obj = Branch_Location.objects.get(Branch_Name=branch)

        # Generate the waste report for a specific branch
        waste_report, wasted_inventory_value = generate_waste_report1(report_type, branch_obj)

    # Filter the waste report based on the selected report type
    if report_type == 'daily':
        waste_report = filter_daily_report(waste_report)
    elif report_type == 'monthly':
        waste_report = filter_monthly_report(waste_report)
    elif report_type == 'annual':
        waste_report = filter_annual_report(waste_report)

    mybranches = Branch_Location.objects.all()

    context = {
        'waste_report': waste_report,
        'wasted_inventory_value': wasted_inventory_value,
        'report_type': report_type,
        'mybranches': mybranches,
        'branch_selected': branch,  # Pass the selected branch to the template
    }
    return render(request, 'reports/admin-reports.html', context)

def pharmacistreports(request): #waste reports
    report_type = request.GET.get('report_type', 'daily')

    user_branch = request.user.branch

    # Generate the waste report
    waste_report, wasted_inventory_value = generate_waste_report1(report_type, user_branch)

    # Filter the waste report based on the selected report type
    if report_type == 'daily':
        waste_report = filter_daily_report(waste_report)
    elif report_type == 'monthly':
        waste_report = filter_monthly_report(waste_report)
    elif report_type == 'annual':
        waste_report = filter_annual_report(waste_report)

    context = {
        'waste_report': waste_report,
        'wasted_inventory_value': wasted_inventory_value,
        'report_type': report_type,
    }
    return render(request, 'reports/pharmacist-reports.html', context)





import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.optimizers import Adam

import math
import numpy as np

def salesreports(request):
    # Define the LSTM sales prediction function
    def lstm_sales_prediction(sales):
        sequence_length = 10  # Number of previous sales data to consider
        x = []
        y = []
        for i in range(len(sales) - sequence_length):
            x.append(sales[i:i+sequence_length])
            y.append(sales[i+sequence_length])
        x = tf.convert_to_tensor(x)
        y = tf.convert_to_tensor(y, dtype=tf.float32)  # Convert to float32

        train_size = int(len(x) * 0.8)
        x_train, x_test = x[:train_size], x[train_size:]
        y_train, y_test = y[:train_size], y[train_size:]

        model = Sequential()
        model.add(LSTM(32, input_shape=(sequence_length, 1)))
        model.add(Dense(1))
        model.compile(optimizer=Adam(), loss='mse')

        model.fit(x_train, y_train, epochs=10)

        predictions = model.predict(x_test)

        return predictions.flatten().tolist(), y_test.numpy().flatten().tolist()

    date_range = request.GET.get('date_range')
    end_date = datetime.now().date()
    user_branch = request.user.branch

    if date_range == '1_month':
        start_date = end_date - timedelta(days=30)
    elif date_range == '3_months':
        start_date = end_date - timedelta(days=90)
    elif date_range == '6_months':
        start_date = end_date - timedelta(days=180)
    elif date_range == '12_months':
        start_date = end_date - timedelta(days=365)
    else:
        start_date = end_date - timedelta(days=30)

    sales = Sale.objects.filter(Sale_Date__range=[start_date, end_date], branch=user_branch)

    num_sales = sales.count()

    top_items = (
        Sale_Detail.objects
        .filter(sale__in=sales)
        .values('product__Product_Name', 'product__Product_Category')
        .annotate(quantity_sold=Sum('Item_Quantity'))
        .annotate(sales_generated=Sum(F('Item_Quantity') * Coalesce('product__Product_Price', 1), output_field=DecimalField()))
        .annotate(avg_quantity_sold=Avg('Item_Quantity'))
        .order_by('-quantity_sold')[:5]
    )

    for item in top_items:
        item['sales_generated'] = Decimal(item['sales_generated']).quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)

    total_sales_value = (
        Sale_Detail.objects
        .filter(sale__in=sales)
        .annotate(sale_value=F('Item_Quantity') * Coalesce('product__Product_Price', 1))
        .aggregate(total_sales=Sum('sale_value', output_field=DecimalField()))
    )

    total_sales_value = total_sales_value['total_sales'] if total_sales_value['total_sales'] is not None else Decimal(0)
    total_sales_value = Decimal(total_sales_value).quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)

    # Convert the Decimal sales values to float before passing to the LSTM model
    lstm_predictions, y_test = lstm_sales_prediction([float(sale.Sale_total) for sale in sales])

    # Generate stock replenishment recommendations
    stock_replenishment = []
    for item in top_items:
        if item['quantity_sold'] >= 30:
            stock_replenishment.append(item['product__Product_Name'])

    # Generate seasonal trends based on categories
    category_trends = {}
    for item in top_items:
        category = item['product__Product_Category']
        if category not in category_trends:
            category_trends[category] = []
        category_trends[category].extend(lstm_predictions)

    seasonal_trends = (
        Sale_Detail.objects
        .filter(sale__in=sales)
        .values('product__Product_Category')
        .annotate(quantity_sold=Sum('Item_Quantity'))
        .annotate(sales_generated=Sum(F('Item_Quantity') * Coalesce('product__Product_Price', 1), output_field=DecimalField()))
        .order_by('-sales_generated')
    )

    for category in seasonal_trends:
        category['sales_generated'] = Decimal(category['sales_generated']).quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)

    # Calculate evaluation metrics
    mae = np.mean(np.abs(np.array(lstm_predictions) - np.array(y_test)))
    rmse = math.sqrt(np.mean(np.square(np.array(lstm_predictions) - np.array(y_test))))
    mape = np.mean(np.abs(np.array(lstm_predictions) - np.array(y_test)) / np.array(y_test)) * 100

    context = {
        'date_range': date_range,
        'num_sales': num_sales,
        'top_items': top_items,
        'total_sales_value': total_sales_value,
        'lstm_predictions': lstm_predictions,
        'stock_replenishment': stock_replenishment,
        'seasonal_trends': seasonal_trends,
        'categories': [category['product__Product_Category'] for category in seasonal_trends],
        'sales_generated': [category['sales_generated'] for category in seasonal_trends],
        'mae': mae,
        'rmse': rmse,
        'mape': mape,
    }

    return render(request, 'reports/sales_report.html', context)







def supplierreports(request):
    report_type = request.GET.get('report_type', 'daily')  # Get the selected report type from the request
    user_branch = request.user.branch  # Get the user's branch (assuming you have a branch field in the User model)

    # Calculate the start and end dates based on the report type
    today = date.today()
    if report_type == 'daily':
        start_date = today
        end_date = today
    elif report_type == 'monthly':
        start_date = today.replace(day=1)
        end_date = today
    elif report_type == 'annual':
        start_date = today.replace(month=1, day=1)
        end_date = today
    else:
        start_date = today
        end_date = today

    # Get the supplier rating summaries for the user's branch
    supplier_ratings = Supplier.objects.filter(branch=user_branch).values('Supplier_Rating').annotate(total=Count('Supplier_Rating'))

    # Get the number of suppliers in the user's branch
    supplier_count = Supplier.objects.filter(branch=user_branch).count()

    # Get the order summaries for the user's branch
    order_summaries = Order_Stock.objects.filter(branch=user_branch, Order_Date__gte=start_date, Order_Date__lte=end_date).select_related('supplier').values('supplier__Supplier_Name').annotate(
    total_orders=Count('id'),
    total_quantity=Sum('Order_Quantity'),
    total_amount=Sum('Order_Total'),
    total_cancellations=Count(
        Case(When(Order_Status='Cancelled', then=1), output_field=models.IntegerField())
    )
    )

    total_cancellations = Order_Stock.objects.filter(branch=user_branch, Order_Date__gte=start_date, Order_Date__lte=end_date, Order_Status='Cancelled').count()

    context = {
        'supplier_ratings': supplier_ratings,
        'supplier_count': supplier_count,
        'order_summaries': order_summaries,
        'report_type': report_type,
        'total_cancellations': total_cancellations,  # Add the total cancellations to the context
    }

    return render(request, 'reports/supplier_report.html', context)


def inventoryreports(request):
    report_type = request.GET.get('report_type', 'daily')  # Get the selected report type from the request
    user_branch = request.user.branch  # Get the user's branch (assuming you have a branch field in the User model)

    # Calculate the start and end dates based on the report type
    #Daily: High mobility threshold is >= 2, Stagnant threshold is <= 1.
    #Monthly: High mobility threshold is > 20, Stagnant threshold is < 5.
    #Annual: High mobility threshold is > 100, Stagnant threshold is < 20.
    #Any other report type: High mobility threshold is >= 2, Stagnant threshold is <= 1.
    today = date.today()
    if report_type == 'daily':
        start_date = today
        end_date = today
        high_mobility_threshold = 2
        stagnant_threshold = 1
    elif report_type == 'monthly':
        start_date = today.replace(day=1)
        end_date = today
        high_mobility_threshold = 20
        stagnant_threshold = 5
    elif report_type == 'annual':
        start_date = today.replace(month=1, day=1)
        end_date = today
        high_mobility_threshold = 100
        stagnant_threshold = 20
    else:
        start_date = today
        end_date = today
        high_mobility_threshold = 2
        stagnant_threshold = 1

    # Calculate the date range for weekly sales comparison
    weekly_start_date = today - timedelta(days=7)

    # Query the products based on the selected report type and user's branch
    high_mobility_products = (
        Product.objects.filter(
            branch=user_branch,
            Product_Quantity__gt=0,
            sale_details__sale__Sale_Date__range=[weekly_start_date, end_date],
        )
        .values('Product_Name', 'Product_Category')
        .annotate(weekly_sales=Sum('sale_details__Item_Quantity'))
        .filter(weekly_sales__gte=high_mobility_threshold)
    )

    stagnant_products = (
        Product.objects.filter(
            branch=user_branch,
            Product_Quantity__gt=0,
            sale_details__sale__Sale_Date__range=[weekly_start_date, end_date],
        )
        .values('Product_Name', 'Product_Category')
        .annotate(weekly_sales=Sum('sale_details__Item_Quantity'))
        .filter(weekly_sales__lt=stagnant_threshold)
    )

    products_near_expiry = Product.objects.filter(
        branch=user_branch,
        Product_Quantity__gt=0,
        Product_Expirydate__gte=start_date,
        Product_Expirydate__lte=end_date,
    )

    context = {
        'high_mobility_products': high_mobility_products,
        'stagnant_products': stagnant_products,
        'products_near_expiry': products_near_expiry,
        'report_type': report_type,
    }

    return render(request, 'reports/inventory_report.html', context)




def adminsalesreports(request):
    mybranches = Branch_Location.objects.all()
    # Define the LSTM sales prediction function
    def lstm_sales_prediction(sales):
        sequence_length = 10  # Number of previous sales data to consider
        x = []
        y = []
        for i in range(len(sales) - sequence_length):
            x.append(sales[i:i+sequence_length])
            y.append(sales[i+sequence_length])
        x = tf.convert_to_tensor(x)
        y = tf.convert_to_tensor(y, dtype=tf.float32)  # Convert to float32

        train_size = int(len(x) * 0.8)
        x_train, x_test = x[:train_size], x[train_size:]
        y_train, y_test = y[:train_size], y[train_size:]

        model = Sequential()
        model.add(LSTM(32, input_shape=(sequence_length, 1)))
        model.add(Dense(1))
        model.compile(optimizer=Adam(), loss='mse')

        model.fit(x_train, y_train, epochs=10)

        predictions = model.predict(x_test)

        return predictions.flatten().tolist(), y_test.numpy().flatten().tolist()

    date_range = request.GET.get('date_range')
    end_date = datetime.now().date()

    if date_range == '1_month':
        start_date = end_date - timedelta(days=30)
    elif date_range == '3_months':
        start_date = end_date - timedelta(days=90)
    elif date_range == '6_months':
        start_date = end_date - timedelta(days=180)
    elif date_range == '12_months':
        start_date = end_date - timedelta(days=365)
    else:
        start_date = end_date - timedelta(days=30)

    ## Get the selected branch from the request
    #user_branch = request.GET.get('branch')
    #if user_branch == 'all':
        # If 'All Branches' is selected, remove the branch filter to retrieve data from all branches
     #   sales = Sale.objects.filter(Sale_Date__range=[start_date, end_date])
    #else:
        # Filter the sales data and other related models by the selected branch
    #    sales = Sale.objects.filter(Sale_Date__range=[start_date, end_date], branch=user_branch)

    

    sales = Sale.objects.filter(Sale_Date__range=[start_date, end_date], branch=3) #set to branch 3 first

    num_sales = sales.count()

    top_items = (
        Sale_Detail.objects
        .filter(sale__in=sales)
        .values('product__Product_Name', 'product__Product_Category')
        .annotate(quantity_sold=Sum('Item_Quantity'))
        .annotate(sales_generated=Sum(F('Item_Quantity') * Coalesce('product__Product_Price', 1), output_field=DecimalField()))
        .annotate(avg_quantity_sold=Avg('Item_Quantity'))
        .order_by('-quantity_sold')[:5]
    )

    for item in top_items:
        item['sales_generated'] = Decimal(item['sales_generated']).quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)

    total_sales_value = (
        Sale_Detail.objects
        .filter(sale__in=sales)
        .annotate(sale_value=F('Item_Quantity') * Coalesce('product__Product_Price', 1))
        .aggregate(total_sales=Sum('sale_value', output_field=DecimalField()))
    )

    total_sales_value = total_sales_value['total_sales'] if total_sales_value['total_sales'] is not None else Decimal(0)
    total_sales_value = Decimal(total_sales_value).quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)

    # Convert the Decimal sales values to float before passing to the LSTM model
    lstm_predictions, y_test = lstm_sales_prediction([float(sale.Sale_total) for sale in sales])

    # Generate stock replenishment recommendations
    stock_replenishment = []
    for item in top_items:
        if item['quantity_sold'] >= 30:
            stock_replenishment.append(item['product__Product_Name'])

    # Generate seasonal trends based on categories
    category_trends = {}
    for item in top_items:
        category = item['product__Product_Category']
        if category not in category_trends:
            category_trends[category] = []
        category_trends[category].extend(lstm_predictions)

    seasonal_trends = (
        Sale_Detail.objects
        .filter(sale__in=sales)
        .values('product__Product_Category')
        .annotate(quantity_sold=Sum('Item_Quantity'))
        .annotate(sales_generated=Sum(F('Item_Quantity') * Coalesce('product__Product_Price', 1), output_field=DecimalField()))
        .order_by('-sales_generated')
    )

    for category in seasonal_trends:
        category['sales_generated'] = Decimal(category['sales_generated']).quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)

    # Calculate evaluation metrics
    mae = np.mean(np.abs(np.array(lstm_predictions) - np.array(y_test)))
    rmse = math.sqrt(np.mean(np.square(np.array(lstm_predictions) - np.array(y_test))))
    mape = np.mean(np.abs(np.array(lstm_predictions) - np.array(y_test)) / np.array(y_test)) * 100

    context = {
        'date_range': date_range,
        'num_sales': num_sales,
        'top_items': top_items,
        'total_sales_value': total_sales_value,
        'lstm_predictions': lstm_predictions,
        'stock_replenishment': stock_replenishment,
        'seasonal_trends': seasonal_trends,
        'categories': [category['product__Product_Category'] for category in seasonal_trends],
        'sales_generated': [category['sales_generated'] for category in seasonal_trends],
        'mae': mae,
        'rmse': rmse,
        'mape': mape,
        'mybranches': mybranches,
    }

    return render(request, 'reports/admin_sales_report.html', context)






def adminsupplierreports(request):
    mybranches = Branch_Location.objects.all()
    report_type = request.GET.get('report_type', 'daily')  # Get the selected report type from the request
    branch_selected = request.GET.get('branch', 'all')  # Get the selected branch from the request

    # Calculate the start and end dates based on the report type
    today = date.today()
    if report_type == 'daily':
        start_date = today
        end_date = today
    elif report_type == 'monthly':
        start_date = today.replace(day=1)
        end_date = today
    elif report_type == 'annual':
        start_date = today.replace(month=1, day=1)
        end_date = today
    else:
        start_date = today
        end_date = today

    # Filter the suppliers based on the selected branch or retrieve all suppliers
    if branch_selected == 'all':
        supplier_ratings = Supplier.objects.values('Supplier_Rating').annotate(total=Count('Supplier_Rating'))
        supplier_count = Supplier.objects.count()
        order_summaries = Order_Stock.objects.filter(Order_Date__gte=start_date, Order_Date__lte=end_date).select_related('supplier').values('supplier__Supplier_Name').annotate(
            total_orders=Count('id'),
            total_quantity=Sum('Order_Quantity'),
            total_amount=Sum('Order_Total'),
            total_cancellations=Count(
                Case(When(Order_Status='Cancelled', then=1), output_field=models.IntegerField())
            )
        )
        total_cancellations = Order_Stock.objects.filter(Order_Date__gte=start_date, Order_Date__lte=end_date, Order_Status='Cancelled').count()
    else:
        supplier_ratings = Supplier.objects.filter(branch__Branch_Name=branch_selected).values('Supplier_Rating').annotate(total=Count('Supplier_Rating'))
        supplier_count = Supplier.objects.filter(branch__Branch_Name=branch_selected).count()
        order_summaries = Order_Stock.objects.filter(branch__Branch_Name=branch_selected, Order_Date__gte=start_date, Order_Date__lte=end_date).select_related('supplier').values('supplier__Supplier_Name').annotate(
            total_orders=Count('id'),
            total_quantity=Sum('Order_Quantity'),
            total_amount=Sum('Order_Total'),
            total_cancellations=Count(
                Case(When(Order_Status='Cancelled', then=1), output_field=models.IntegerField())
            )
        )
        total_cancellations = Order_Stock.objects.filter(branch__Branch_Name=branch_selected, Order_Date__gte=start_date, Order_Date__lte=end_date, Order_Status='Cancelled').count()

    context = {
        'supplier_ratings': supplier_ratings,
        'supplier_count': supplier_count,
        'order_summaries': order_summaries,
        'report_type': report_type,
        'total_cancellations': total_cancellations,
        'mybranches': mybranches,
    }

    return render(request, 'reports/admin_supplier_report.html', context)



def admininventoryreports(request):
    mybranches = Branch_Location.objects.all()
    report_type = request.GET.get('report_type', 'daily')  # Get the selected report type from the request
    branch_selected = request.GET.get('branch', 'all')  # Get the selected branch from the request

    # Calculate the start and end dates based on the report type
    # Daily: High mobility threshold is >= 2, Stagnant threshold is <= 1.
    # Monthly: High mobility threshold is > 20, Stagnant threshold is < 5.
    # Annual: High mobility threshold is > 100, Stagnant threshold is < 20.
    # Any other report type: High mobility threshold is >= 2, Stagnant threshold is <= 1.
    today = date.today()
    if report_type == 'daily':
        start_date = today
        end_date = today
        high_mobility_threshold = 2
        stagnant_threshold = 1
    elif report_type == 'monthly':
        start_date = today.replace(day=1)
        end_date = today
        high_mobility_threshold = 20
        stagnant_threshold = 5
    elif report_type == 'annual':
        start_date = today.replace(month=1, day=1)
        end_date = today
        high_mobility_threshold = 100
        stagnant_threshold = 20
    else:
        start_date = today
        end_date = today
        high_mobility_threshold = 2
        stagnant_threshold = 1

    # Calculate the date range for weekly sales comparison
    weekly_start_date = today - timedelta(days=7)

    # Filter the products based on the selected branch or retrieve all products
    if branch_selected == 'all':
        high_mobility_products = (
            Product.objects.filter(
                Product_Quantity__gt=0,
                branch__in=mybranches,  # Filter by branches selected in mybranches
                sale_details__sale__Sale_Date__range=[weekly_start_date, end_date],
            )
            .values('Product_Name', 'Product_Category')
            .annotate(weekly_sales=Sum('sale_details__Item_Quantity'))
            .filter(weekly_sales__gte=high_mobility_threshold)
        )

        stagnant_products = (
            Product.objects.filter(
                Product_Quantity__gt=0,
                branch__in=mybranches,  # Filter by branches selected in mybranches
                sale_details__sale__Sale_Date__range=[weekly_start_date, end_date],
            )
            .values('Product_Name', 'Product_Category')
            .annotate(weekly_sales=Sum('sale_details__Item_Quantity'))
            .filter(weekly_sales__lt=stagnant_threshold)
        )

        products_near_expiry = Product.objects.filter(
            Product_Quantity__gt=0,
            branch__in=mybranches,  # Filter by branches selected in mybranches
            Product_Expirydate__gte=start_date,
            Product_Expirydate__lte=end_date,
        )
    else:
        high_mobility_products = (
            Product.objects.filter(
                Product_Quantity__gt=0,
                branch__Branch_Name=branch_selected,  # Filter by the selected branch
                sale_details__sale__Sale_Date__range=[weekly_start_date, end_date],
            )
            .values('Product_Name', 'Product_Category')
            .annotate(weekly_sales=Sum('sale_details__Item_Quantity'))
            .filter(weekly_sales__gte=high_mobility_threshold)
        )

        stagnant_products = (
            Product.objects.filter(
                Product_Quantity__gt=0,
                branch__Branch_Name=branch_selected,  # Filter by the selected branch
                sale_details__sale__Sale_Date__range=[weekly_start_date, end_date],
            )
            .values('Product_Name', 'Product_Category')
            .annotate(weekly_sales=Sum('sale_details__Item_Quantity'))
            .filter(weekly_sales__lt=stagnant_threshold)
        )

        products_near_expiry = Product.objects.filter(
            Product_Quantity__gt=0,
            branch__Branch_Name=branch_selected,  # Filter by the selected branch
            Product_Expirydate__gte=start_date,
            Product_Expirydate__lte=end_date,
        )

    context = {
        'high_mobility_products': high_mobility_products,
        'stagnant_products': stagnant_products,
        'products_near_expiry': products_near_expiry,
        'report_type': report_type,
        'mybranches': mybranches,
    }

    return render(request, 'reports/admin_inventory_report.html', context)

