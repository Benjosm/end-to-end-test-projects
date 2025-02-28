import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import current_app

logger = logging.getLogger(__name__)

def send_low_stock_notification(product):
    """Send notification when product stock is low."""
    if not current_app.config["NOTIFICATION_ENABLED"]:
        logger.info(f"Notifications disabled: Skipping low stock alert for {product.name}")
        return False
    
    smtp_server = "smtp.example.com"
    smtp_port = 587
    smtp_username = "inventory@example.com"
    smtp_password = "password123"  # Security issue: Hardcoded password
    
    sender = "inventory@example.com"
    recipients = ["manager@example.com"]
    
    # Create message
    msg = MIMEMultipart()
    msg["From"] = sender
    msg["To"] = ", ".join(recipients)
    msg["Subject"] = f"Low Stock Alert: {product.name}"
    
    body = f"""
    Low Stock Alert
    
    Product: {product.name}
    SKU: {product.sku}
    Current Quantity: {product.quantity}
    Low Stock Threshold: {product.low_stock_threshold}
    
    Please restock this item soon.
    """
    
    msg.attach(MIMEText(body, "plain"))
    
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.login(smtp_username, smtp_password)
        server.send_message(msg)
        server.quit()
        
        logger.info(f"Low stock notification sent for {product.name}")
        return True
    except Exception as e:
        logger.error(f"Failed to send notification: {str(e)}")
        return False

def send_inventory_report(recipient, report_data):
    """Send inventory report to specified recipient."""
    if not current_app.config["NOTIFICATION_ENABLED"]:
        logger.info("Notifications disabled: Skipping inventory report")
        return False
    
    logger.warning("send_inventory_report not implemented")
    return False
