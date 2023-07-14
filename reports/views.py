from django.shortcuts import render, HttpResponse, HttpResponseRedirect, redirect
from django.template import loader
from django.contrib import messages 
from admin_dash.models import Branch_Location

#import models to be used in analytics and reports
from assist_dash.models import Product,Supplier,Order_Stock,Sale,Sale_Detail
from .wastereport_utils import *
from django.db.models import Sum
from .pm_utils import prepare_sales_data, train_lstm_model, evaluate_model
from datetime import datetime, timedelta
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

def adminreports(request): #waste reports
    report_type = request.GET.get('report_type', 'daily')
    branch = request.GET.get('branch')

    # Retrieve the branch based on the branch name
    if branch != 'all':
        # Generate the waste report
        waste_report, wasted_inventory_value = generate_waste_report1(report_type, branch)
    else:
        # Generate the waste report
        waste_report, wasted_inventory_value = generate_waste_report(report_type)

    

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



from datetime import datetime

def salesreports(request):
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

    sales_df = prepare_sales_data()
    sales_df['date'] = pd.to_datetime(sales_df['sale_id']).dt.date
    sales_df['sale_time'] = pd.to_datetime(sales_df['sale_id']).dt.time
    sales_data = sales_df[['date', 'sale_id', 'Item_Quantity', 'Product_Price']]
    sales_data.set_index('date', inplace=True)

    scaler = MinMaxScaler()
    sales_data[['Item_Quantity', 'Product_Price']] = scaler.fit_transform(sales_data[['Item_Quantity', 'Product_Price']])

    split_ratio = 0.8
    split_index = int(len(sales_data) * split_ratio)
    train_data = sales_data[:split_index]
    test_data = sales_data[split_index:]

    X_train = train_data[['Item_Quantity', 'Product_Price']].values
    y_train = train_data['Item_Quantity'].values

    X_test = test_data[['Item_Quantity', 'Product_Price']].values
    y_test = test_data['Item_Quantity'].values

    X_train = X_train.reshape((X_train.shape[0], 1, X_train.shape[1]))
    X_test = X_test.reshape((X_test.shape[0], 1, X_test.shape[1]))

    #parameters
    num_units = 1
    activation_func = 'tanh'
    num_epochs = 50
    batch_size = 1

    model = train_lstm_model(X_train, y_train, num_units, activation_func, num_epochs, batch_size)
    mse, mae, rmse = evaluate_model(model, X_test, y_test)

    context = {
        'mse': mse,
        'mae': mae,
        'rmse': rmse,
    }

    return render(request, 'reports/sales_report.html', context)

from django.db.models import Count, Sum
from datetime import date, timedelta

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
    order_summaries = Order_Stock.objects.filter(branch=user_branch, Order_Date__gte=start_date, Order_Date__lte=end_date).values('supplier').annotate(total_orders=Count('id'), total_quantity=Sum('Order_Quantity'), total_amount=Sum('Order_Total'))

    context = {
        'supplier_ratings': supplier_ratings,
        'supplier_count': supplier_count,
        'order_summaries': order_summaries,
        'report_type': report_type,
    }

    return render(request, 'reports/supplier_report.html', context)


from datetime import date, timedelta

def inventoryreports(request):
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

    # Query the products based on the selected report type and user's branch
    high_mobility_products = Product.objects.filter(branch=user_branch, Product_Quantity__gt=0, Product_Category='High Mobility')
    stagnant_products = Product.objects.filter(branch=user_branch, Product_Quantity__gt=50, Product_Category='Stagnant')
    products_near_expiry = Product.objects.filter(branch=user_branch, Product_Quantity__gt=0, Product_Expirydate__gte=start_date, Product_Expirydate__lte=end_date)

    context = {
        'high_mobility_products': high_mobility_products,
        'stagnant_products': stagnant_products,
        'products_near_expiry': products_near_expiry,
        'report_type': report_type,
    }

    return render(request, 'reports/inventory_report.html', context)


