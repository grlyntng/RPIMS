# utils.py
from assist_dash.models import Product
from .models import Notification
from datetime import datetime, timedelta
from django.utils.timezone import utc

def check_notifications():
    # Retrieve all products with stock quantity <= 9
    low_stock_products = Product.objects.filter(Product_Quantity__lte=9)

    # Retrieve all products with expiration date within 30 days from now
    expiration_date_threshold = datetime.utcnow().replace(tzinfo=utc) + timedelta(days=30)
    expiring_products = Product.objects.filter(Product_Expirydate__lte=expiration_date_threshold)

    # Generate notifications for low stock products
    for product in low_stock_products:
        
        notification_content = f"The stock quantity for {product.Product_Name} is low ({product.Product_Quantity})."
        # Check if a notification with the same content already exists
        existing_notification = Notification.objects.filter(Notification_Content=notification_content).first()
        if existing_notification:
            continue  # Skip creating duplicate notification
        notification = Notification(
            Notification_Type='Low Stock',
            Notification_Content=notification_content,
            branch=product.branch
        )
        notification.save()

    # Generate notifications for expiring products
    for product in expiring_products:
        notification_content = f"The product {product.Product_Name} is expiring soon on {product.Product_Expirydate}."
        # Check if a notification with the same content already exists
        existing_notification = Notification.objects.filter(Notification_Content=notification_content).first()
        if existing_notification:
            continue  # Skip creating duplicate notification
        notification = Notification(
            Notification_Type='Near Expiration',
            Notification_Content=notification_content,
            branch=product.branch
        )
        notification.save()