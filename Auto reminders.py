"""
Automated Reminders Module
Tracks and sends payment reminders automatically

Creates a reminder schedule table and tracks sent reminders
"""

import sqlite3
from datetime import datetime, timedelta
import database as db

DATABASE_NAME = "Vyapar_Digikhata.db"

def init_reminders_table():
    """Create reminders tracking table"""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS payment_reminders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            customer_id INTEGER NOT NULL,
            reminder_day INTEGER NOT NULL,
            sent_date TEXT NOT NULL,
            pending_amount REAL NOT NULL,
            days_overdue INTEGER NOT NULL,
            status TEXT DEFAULT 'sent',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (customer_id) REFERENCES customers(id)
        )
    ''')
    
    conn.commit()
    conn.close()

# Initialize table
init_reminders_table()

def check_reminder_sent(user_id, customer_id, reminder_day):
    """Check if reminder already sent for this day threshold"""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    
    # Check if reminder sent in last 24 hours for this threshold
    yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    
    cursor.execute('''
        SELECT * FROM payment_reminders 
        WHERE user_id = ? AND customer_id = ? 
        AND reminder_day = ? AND sent_date >= ?
    ''', (user_id, customer_id, reminder_day, yesterday))
    
    result = cursor.fetchone()
    conn.close()
    
    return result is not None

def log_reminder(user_id, customer_id, reminder_day, pending_amount, days_overdue):
    """Log sent reminder"""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO payment_reminders 
        (user_id, customer_id, reminder_day, sent_date, pending_amount, days_overdue)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (user_id, customer_id, reminder_day, datetime.now().strftime('%Y-%m-%d'), 
          pending_amount, days_overdue))
    
    conn.commit()
    conn.close()

def get_customers_needing_reminders(user_id):
    """
    Get customers who need payment reminders
    Returns list categorized by reminder day (10, 20, 30 days)
    """
    from settings import get_overdue_customers
    
    overdue_customers = get_overdue_customers(user_id)
    
    reminders_needed = {
        10: [],  # 10 days overdue
        20: [],  # 20 days overdue
        30: []   # 30+ days overdue
    }
    
    for customer in overdue_customers:
        days = customer['days_overdue']
        customer_id = customer['customer_id']
        
        # Determine which reminder threshold
        if days >= 30 and not check_reminder_sent(user_id, customer_id, 30):
            reminders_needed[30].append(customer)
        elif days >= 20 and not check_reminder_sent(user_id, customer_id, 20):
            reminders_needed[20].append(customer)
        elif days >= 10 and not check_reminder_sent(user_id, customer_id, 10):
            reminders_needed[10].append(customer)
    
    return reminders_needed

def get_reminder_history(user_id, customer_id=None):
    """Get reminder history for user or specific customer"""
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    if customer_id:
        cursor.execute('''
            SELECT r.*, c.name as customer_name 
            FROM payment_reminders r
            JOIN customers c ON r.customer_id = c.id
            WHERE r.user_id = ? AND r.customer_id = ?
            ORDER BY r.sent_date DESC
        ''', (user_id, customer_id))
    else:
        cursor.execute('''
            SELECT r.*, c.name as customer_name 
            FROM payment_reminders r
            JOIN customers c ON r.customer_id = c.id
            WHERE r.user_id = ?
            ORDER BY r.sent_date DESC
            LIMIT 50
        ''', (user_id,))
    
    reminders = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return reminders

def get_reminder_stats(user_id):
    """Get reminder statistics for dashboard"""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    
    # Total reminders sent
    cursor.execute('SELECT COUNT(*) FROM payment_reminders WHERE user_id = ?', (user_id,))
    total_sent = cursor.fetchone()[0]
    
    # Reminders in last 30 days
    thirty_days_ago = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
    cursor.execute('''
        SELECT COUNT(*) FROM payment_reminders 
        WHERE user_id = ? AND sent_date >= ?
    ''', (user_id, thirty_days_ago))
    recent_sent = cursor.fetchone()[0]
    
    # By reminder day
    cursor.execute('''
        SELECT reminder_day, COUNT(*) as count 
        FROM payment_reminders 
        WHERE user_id = ?
        GROUP BY reminder_day
    ''', (user_id,))
    
    by_day = {row[0]: row[1] for row in cursor.fetchall()}
    
    conn.close()
    
    return {
        'total_sent': total_sent,
        'recent_sent': recent_sent,
        'day_10': by_day.get(10, 0),
        'day_20': by_day.get(20, 0),
        'day_30': by_day.get(30, 0)
    }

def generate_reminder_message(customer_name, pending_amount, days_overdue, shop_name):
    """Generate appropriate reminder message based on days overdue"""
    
    if days_overdue >= 30:
        urgency = "URGENT"
        tone = "We kindly request immediate attention to this matter."
    elif days_overdue >= 20:
        urgency = "IMPORTANT"
        tone = "We would appreciate your prompt payment."
    else:
        urgency = "REMINDER"
        tone = "This is a friendly reminder about your pending payment."
    
    message = f"""🔔 *{urgency} - Payment Reminder*

Dear {customer_name},

{tone}

💰 *Amount Due:* ₹{pending_amount:,.2f}
📅 *Days Overdue:* {days_overdue} days

Please make the payment at your earliest convenience to avoid any inconvenience.

Thank you for your continued business!

Best regards,
{shop_name}

_Automated reminder from Vyapar DigiKhata_"""
    
    return message