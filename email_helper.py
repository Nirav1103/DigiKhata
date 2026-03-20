"""
Email Notification Helper
Sends email notifications for low stock and overdue payments

Uses Python's built-in smtplib for sending emails
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import streamlit as st

def send_notification_email(to_email, subject, body):
    """
    Send email notification using Gmail SMTP
    
    Args:
        to_email: Recipient email address
        subject: Email subject
        body: Email body (HTML supported)
    
    Returns:
        (success: bool, message: str)
    """
    
    # Email configuration - using a generic SMTP approach
    # For production, you should configure these in session state or environment variables
    
    # Check if email settings are configured
    if 'email_settings' not in st.session_state or not st.session_state.email_settings.get('enabled', False):
        return False, "Email notifications are not configured. Please enable them in Settings."
    
    email_config = st.session_state.email_settings
    
    try:
        # Create message
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = email_config.get('smtp_email', '')
        message["To"] = to_email
        
        # Create HTML and plain text versions
        text_body = body.replace('<br>', '\n').replace('<b>', '').replace('</b>', '')
        html_body = f"""
        <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                {body}
                <br><br>
                <hr style="border: 1px solid #e0e0e0;">
                <p style="color: #666; font-size: 12px;">
                    This is an automated notification from Vyapar DigiKhata<br>
                    Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                </p>
            </body>
        </html>
        """
        
        # Attach both versions
        part1 = MIMEText(text_body, "plain")
        part2 = MIMEText(html_body, "html")
        message.attach(part1)
        message.attach(part2)
        
        # Send email based on provider
        smtp_server = email_config.get('smtp_server', 'smtp.gmail.com')
        smtp_port = email_config.get('smtp_port', 587)
        smtp_email = email_config.get('smtp_email', '')
        smtp_password = email_config.get('smtp_password', '')
        
        if not smtp_email or not smtp_password:
            return False, "Email credentials not configured"
        
        # Connect to SMTP server
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_email, smtp_password)
            server.send_message(message)
        
        return True, "Email sent successfully"
        
    except smtplib.SMTPAuthenticationError:
        return False, "Authentication failed. Please check your email and password."
    except smtplib.SMTPException as e:
        return False, f"SMTP error: {str(e)}"
    except Exception as e:
        return False, f"Error sending email: {str(e)}"

def generate_low_stock_email(low_stock_items, shop_name):
    """Generate email body for low stock notification"""
    
    critical_items = [item for item in low_stock_items if item['quantity'] <= 5]
    low_items = [item for item in low_stock_items if item['quantity'] > 5]
    
    body = f"""
    <h2 style="color: #e74c3c;">🔔 Low Stock Alert - {shop_name}</h2>
    <p>Dear Shop Owner,</p>
    <p>This is an automated notification about items running low in your inventory.</p>
    """
    
    if critical_items:
        body += f"""
        <h3 style="color: #c0392b;">🔴 Critical Stock ({len(critical_items)} items with ≤5 units)</h3>
        <table style="border-collapse: collapse; width: 100%; margin: 10px 0;">
            <tr style="background-color: #f8d7da;">
                <th style="border: 1px solid #ddd; padding: 8px; text-align: left;">Item Name</th>
                <th style="border: 1px solid #ddd; padding: 8px; text-align: center;">Stock</th>
                <th style="border: 1px solid #ddd; padding: 8px; text-align: right;">Price/Unit</th>
            </tr>
        """
        for item in critical_items:
            body += f"""
            <tr>
                <td style="border: 1px solid #ddd; padding: 8px;">{item['item_name']}</td>
                <td style="border: 1px solid #ddd; padding: 8px; text-align: center; color: #c0392b;"><b>{item['quantity']}</b></td>
                <td style="border: 1px solid #ddd; padding: 8px; text-align: right;">₹{item['price_per_unit']:.2f}</td>
            </tr>
            """
        body += "</table>"
    
    if low_items:
        body += f"""
        <h3 style="color: #f39c12;">🟡 Low Stock ({len(low_items)} items with 6-10 units)</h3>
        <table style="border-collapse: collapse; width: 100%; margin: 10px 0;">
            <tr style="background-color: #fff3cd;">
                <th style="border: 1px solid #ddd; padding: 8px; text-align: left;">Item Name</th>
                <th style="border: 1px solid #ddd; padding: 8px; text-align: center;">Stock</th>
                <th style="border: 1px solid #ddd; padding: 8px; text-align: right;">Price/Unit</th>
            </tr>
        """
        for item in low_items:
            body += f"""
            <tr>
                <td style="border: 1px solid #ddd; padding: 8px;">{item['item_name']}</td>
                <td style="border: 1px solid #ddd; padding: 8px; text-align: center; color: #f39c12;"><b>{item['quantity']}</b></td>
                <td style="border: 1px solid #ddd; padding: 8px; text-align: right;">₹{item['price_per_unit']:.2f}</td>
            </tr>
            """
        body += "</table>"
    
    body += """
    <p><b>Action Required:</b> Please restock these items to avoid running out of inventory.</p>
    <p>Login to your Vyapar DigiKhata dashboard to manage your inventory.</p>
    """
    
    return body

def generate_overdue_payment_email(overdue_customers, shop_name):
    """Generate email body for overdue payment notification"""
    
    total_overdue_amount = sum(customer['pending_amount'] for customer in overdue_customers)
    
    body = f"""
    <h2 style="color: #e67e22;">💰 Overdue Payment Alert - {shop_name}</h2>
    <p>Dear Shop Owner,</p>
    <p>This is an automated notification about customers with overdue payments.</p>
    
    <h3 style="color: #d35400;">Customer Payment Status</h3>
    <table style="border-collapse: collapse; width: 100%; margin: 10px 0;">
        <tr style="background-color: #ffe5cc;">
            <th style="border: 1px solid #ddd; padding: 8px; text-align: left;">Customer Name</th>
            <th style="border: 1px solid #ddd; padding: 8px; text-align: right;">Pending Amount</th>
            <th style="border: 1px solid #ddd; padding: 8px; text-align: center;">Days Overdue</th>
            <th style="border: 1px solid #ddd; padding: 8px; text-align: center;">Last Transaction</th>
        </tr>
    """
    
    for customer in overdue_customers:
        body += f"""
        <tr>
            <td style="border: 1px solid #ddd; padding: 8px;">{customer['customer_name']}</td>
            <td style="border: 1px solid #ddd; padding: 8px; text-align: right;">₹{customer['pending_amount']:,.2f}</td>
            <td style="border: 1px solid #ddd; padding: 8px; text-align: center; color: #e67e22;"><b>{customer['days_overdue']}</b></td>
            <td style="border: 1px solid #ddd; padding: 8px; text-align: center;">{customer['last_transaction_date']}</td>
        </tr>
        """
    
    body += f"""
    </table>
    
    <div style="background-color: #fff3e0; padding: 15px; border-left: 4px solid #ff9800; margin: 15px 0;">
        <p style="margin: 0;"><b>Total Overdue Amount: ₹{total_overdue_amount:,.2f}</b></p>
    </div>
    
    <p><b>Action Required:</b> Please follow up with these customers to collect pending payments.</p>
    <p>Login to your Vyapar DigiKhata dashboard to view detailed transaction history.</p>
    """
    
    return body

def send_low_stock_notification(user_email, low_stock_items, shop_name):
    """Send low stock notification email"""
    subject = f"⚠️ Low Stock Alert - {shop_name}"
    body = generate_low_stock_email(low_stock_items, shop_name)
    return send_notification_email(user_email, subject, body)

def send_overdue_payment_notification(user_email, overdue_customers, shop_name):
    """Send overdue payment notification email"""
    subject = f"💰 Overdue Payment Alert - {shop_name}"
    body = generate_overdue_payment_email(overdue_customers, shop_name)
    return send_notification_email(user_email, subject, body)