
from django.db.models import F, Sum
from datetime import date
from assist_dash.models import Product,Supplier,Order_Stock,Sale,Sale_Detail

#general function
def generate_waste_report(report_type):
    # Retrieve products that are considered wasted (expired or about to expire)
    wasted_products = Product.objects.filter(Product_Expirydate__lte=date.today())

    # Calculate the monetary value of the wasted inventory
    if report_type == 'daily':
        wasted_inventory_value = calculate_waste_value(wasted_products, timedelta(days=1))
    elif report_type == 'monthly':
        wasted_inventory_value = calculate_waste_value(wasted_products, timedelta(days=30))
    elif report_type == 'annual':
        wasted_inventory_value = calculate_waste_value(wasted_products, timedelta(days=365))
    else:
        # Default to daily report if an invalid report type is provided
        wasted_inventory_value = calculate_waste_value(wasted_products, timedelta(days=1))

    # Generate the waste report
    report = []
    for product in wasted_products:
        waste_info = {
            'Product_Name': product.Product_Name,
            'Product_Quantity': product.Product_Quantity,
            'Product_Expirydate': product.Product_Expirydate,
            'Monetary_Value': product.Product_Price * product.Product_Quantity
        }
        report.append(waste_info)

    return report, wasted_inventory_value

#function for specific branch filtered
def generate_waste_report1(report_type, user_branch):
    # Retrieve products from the user's branch that are considered wasted (expired or about to expire)
    wasted_products = Product.objects.filter(branch=user_branch, Product_Expirydate__lte=date.today())

    # Calculate the monetary value of the wasted inventory
    if report_type == 'daily':
        wasted_inventory_value = calculate_waste_value(wasted_products, timedelta(days=1))
    elif report_type == 'monthly':
        wasted_inventory_value = calculate_waste_value(wasted_products, timedelta(days=30))
    elif report_type == 'annual':
        wasted_inventory_value = calculate_waste_value(wasted_products, timedelta(days=365))
    else:
        # Default to daily report if an invalid report type is provided
        wasted_inventory_value = calculate_waste_value(wasted_products, timedelta(days=1))

    # Generate the waste report
    report = []
    for product in wasted_products:
        waste_info = {
            'Product_Name': product.Product_Name,
            'Product_Quantity': product.Product_Quantity,
            'Product_Expirydate': product.Product_Expirydate,
            'Monetary_Value': product.Product_Price * product.Product_Quantity
        }
        report.append(waste_info)

    return report, wasted_inventory_value


def calculate_waste_value(wasted_products, time_period):
    start_date = date.today() - time_period
    filtered_products = wasted_products.filter(Product_Expirydate__gt=start_date)
    waste_value = filtered_products.aggregate(total_waste_value=Sum(F('Product_Price') * F('Product_Quantity')))['total_waste_value']
    return waste_value if waste_value else 0

from datetime import date, timedelta

def filter_daily_report(waste_report):
    # Filter the waste report to include products expired today
    today = date.today()
    filtered_report = [item for item in waste_report if item['Product_Expirydate'] == today]
    return filtered_report

def filter_monthly_report(waste_report):
    # Filter the waste report to include products expired in the current month
    today = date.today()
    first_day_of_month = date(today.year, today.month, 1)
    filtered_report = [item for item in waste_report if first_day_of_month <= item['Product_Expirydate'] <= today]
    return filtered_report

def filter_annual_report(waste_report):
    # Filter the waste report to include products expired in the current year
    today = date.today()
    first_day_of_year = date(today.year, 1, 1)
    filtered_report = [item for item in waste_report if first_day_of_year <= item['Product_Expirydate'] <= today]
    return filtered_report
