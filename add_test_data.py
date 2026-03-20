"""
Complete Test Data Insertion Script
Clears ALL existing data and adds fresh users with correct passwords,
customers, inventory, transactions, and suppliers.

Usage:
    python add_test_data.py
"""

import sqlite3
from datetime import datetime, timedelta
import random

DATABASE_NAME = "Vyapar_Digikhata.db"

def get_conn():
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    return conn

# ─────────────────────────────────────────────
# STEP 0: Wipe all existing data
# ─────────────────────────────────────────────
def clear_all_data():
    print("\n" + "=" * 60)
    print("STEP 0: Clearing ALL existing data")
    print("=" * 60)
    conn = get_conn()
    cursor = conn.cursor()
    tables = ["payment_reminders", "transactions", "inventory", "suppliers", "customers", "users"]
    for table in tables:
        try:
            cursor.execute(f"DELETE FROM {table}")
            cursor.execute(f"DELETE FROM sqlite_sequence WHERE name='{table}'")
            print(f"  Cleared: {table}")
        except Exception as e:
            print(f"  {table}: {e}")
    conn.commit()
    conn.close()

# ─────────────────────────────────────────────
# STEP 1: Users
# ─────────────────────────────────────────────
TEST_USERS = [
    {
        'name': 'Kavya Patel',
        'email': 'kavya@gmail.com',
        'shop_name': 'Kavya General Store',
        'password': 'Kavya!123'
    },
    {
        'name': 'Nirav Shah',
        'email': 'nIrav@gmail.com',
        'shop_name': 'Nirav Electronics',
        'password': 'Nirav@123'
    },
    {
        'name': 'Asha Desai',
        'email': 'asha@gmail.com',
        'shop_name': 'Asha Textiles',
        'password': 'Asha#123'
    },
    {
        'name': 'Vyapar DigiKhata',
        'email': 'vyapar.digikhata26@gmail.com',
        'shop_name': 'Vyapar DigiKhata Demo',
        'password': 'vyapar@26'
    },
]

def add_users():
    print("\n" + "=" * 60)
    print("STEP 1: Adding Users")
    print("=" * 60)
    conn = get_conn()
    cursor = conn.cursor()
    created = []
    for u in TEST_USERS:
        cursor.execute(
            "INSERT INTO users(owner_name, email, shop_name, password) VALUES(?,?,?,?)",
            (u['name'], u['email'], u['shop_name'], u['password'])
        )
        user_id = cursor.lastrowid
        print(f"  Added: {u['email']}  |  pass: {u['password']}")
        created.append({'id': user_id, **u})
    conn.commit()
    conn.close()
    return created

# ─────────────────────────────────────────────
# STEP 2: Customers
# ─────────────────────────────────────────────
CUSTOMERS = {
    'kavya@gmail.com': [
        {'name': 'Ramesh Kumar',  'contact': '9876543210', 'address': '123 MG Road, Ahmedabad'},
        {'name': 'Priya Sharma',  'contact': '9876543211', 'address': '45 CG Road, Ahmedabad'},
        {'name': 'Vijay Patel',   'contact': '9876543212', 'address': '78 SG Highway, Ahmedabad'},
        {'name': 'Anjali Mehta',  'contact': '9876543213', 'address': '90 Ashram Road, Ahmedabad'},
        {'name': 'Suresh Desai',  'contact': '9876543214', 'address': '12 Satellite, Ahmedabad'},
    ],
    'nIrav@gmail.com': [
        {'name': 'Kiran Shah',    'contact': '9876543215', 'address': '34 Navrangpura, Ahmedabad'},
        {'name': 'Meera Joshi',   'contact': '9876543216', 'address': '56 Bodakdev, Ahmedabad'},
        {'name': 'Rajesh Rao',    'contact': '9876543217', 'address': '23 Vastrapur, Ahmedabad'},
        {'name': 'Pooja Nair',    'contact': '9876543218', 'address': '67 Maninagar, Ahmedabad'},
    ],
    'asha@gmail.com': [
        {'name': 'Deepak Singh',  'contact': '9876543219', 'address': '89 Paldi, Ahmedabad'},
        {'name': 'Sneha Reddy',   'contact': '9876543220', 'address': '11 Ambawadi, Ahmedabad'},
        {'name': 'Amit Gupta',    'contact': '9876543221', 'address': '33 Thaltej, Ahmedabad'},
        {'name': 'Nisha Kapoor',  'contact': '9876543222', 'address': '55 Bopal, Ahmedabad'},
        {'name': 'Rahul Verma',   'contact': '9876543223', 'address': '77 Gota, Ahmedabad'},
    ],
    'vyapar.digikhata26@gmail.com': [
        {'name': 'Demo Customer 1', 'contact': '9800000001', 'address': 'Demo Address 1, Ahmedabad'},
        {'name': 'Demo Customer 2', 'contact': '9800000002', 'address': 'Demo Address 2, Ahmedabad'},
        {'name': 'Demo Customer 3', 'contact': '9800000003', 'address': 'Demo Address 3, Ahmedabad'},
    ],
}

def add_customers(users):
    print("\n" + "=" * 60)
    print("STEP 2: Adding Customers")
    print("=" * 60)
    conn = get_conn()
    cursor = conn.cursor()
    customer_ids = {}
    for u in users:
        email = u['email']
        customer_ids[email] = []
        print(f"\n  {u['name']} ({email}):")
        for c in CUSTOMERS.get(email, []):
            cursor.execute(
                "INSERT INTO customers(user_id, name, contact, address) VALUES(?,?,?,?)",
                (u['id'], c['name'], c['contact'], c['address'])
            )
            cid = cursor.lastrowid
            customer_ids[email].append(cid)
            print(f"    Added: {c['name']}")
    conn.commit()
    conn.close()
    return customer_ids

# ─────────────────────────────────────────────
# STEP 3: Inventory
# ─────────────────────────────────────────────
INVENTORY = {
    'kavya@gmail.com': [
        {'item': 'Rice (1kg)',        'quantity': 50, 'price': 60.00},
        {'item': 'Wheat Flour (1kg)', 'quantity': 40, 'price': 45.00},
        {'item': 'Sugar (1kg)',        'quantity': 8,  'price': 50.00},
        {'item': 'Cooking Oil (1L)',   'quantity': 25, 'price': 180.00},
        {'item': 'Tea Powder (250g)',  'quantity': 15, 'price': 120.00},
        {'item': 'Coffee (200g)',      'quantity': 4,  'price': 250.00},
        {'item': 'Salt (1kg)',         'quantity': 60, 'price': 20.00},
        {'item': 'Masala Mix',         'quantity': 9,  'price': 80.00},
    ],
    'nIrav@gmail.com': [
        {'item': 'LED TV 32"',      'quantity': 12, 'price': 15000.00},
        {'item': 'Washing Machine', 'quantity': 3,  'price': 18000.00},
        {'item': 'Refrigerator',    'quantity': 5,  'price': 25000.00},
        {'item': 'Microwave Oven',  'quantity': 8,  'price': 8000.00},
        {'item': 'Ceiling Fan',     'quantity': 20, 'price': 1500.00},
        {'item': 'Mixer Grinder',   'quantity': 15, 'price': 3500.00},
    ],
    'asha@gmail.com': [
        {'item': 'Cotton Saree',  'quantity': 25, 'price': 1200.00},
        {'item': 'Silk Saree',    'quantity': 6,  'price': 3500.00},
        {'item': 'Cotton Shirt',  'quantity': 30, 'price': 450.00},
        {'item': 'Jeans Pant',    'quantity': 9,  'price': 800.00},
        {'item': 'Bedsheet Set',  'quantity': 18, 'price': 600.00},
        {'item': 'Towel Set',     'quantity': 40, 'price': 250.00},
        {'item': 'Kurta Set',     'quantity': 3,  'price': 950.00},
    ],
    'vyapar.digikhata26@gmail.com': [
        {'item': 'Demo Product A', 'quantity': 10, 'price': 500.00},
        {'item': 'Demo Product B', 'quantity': 5,  'price': 1200.00},
        {'item': 'Demo Product C', 'quantity': 20, 'price': 300.00},
    ],
}

def add_inventory(users):
    print("\n" + "=" * 60)
    print("STEP 3: Adding Inventory")
    print("=" * 60)
    conn = get_conn()
    cursor = conn.cursor()
    for u in users:
        email = u['email']
        print(f"\n  {u['name']} ({email}):")
        for item in INVENTORY.get(email, []):
            cursor.execute(
                "INSERT INTO inventory(user_id, item_name, quantity, price_per_unit) VALUES(?,?,?,?)",
                (u['id'], item['item'], item['quantity'], item['price'])
            )
            print(f"    Added: {item['item']}  (Qty: {item['quantity']}, Rs.{item['price']})")
    conn.commit()
    conn.close()

# ─────────────────────────────────────────────
# STEP 4: Transactions
# ─────────────────────────────────────────────
def add_transactions(users, customer_ids):
    print("\n" + "=" * 60)
    print("STEP 4: Adding Transactions")
    print("=" * 60)
    conn = get_conn()
    cursor = conn.cursor()
    for u in users:
        email = u['email']
        cids = customer_ids.get(email, [])
        if not cids:
            continue
        count = 0
        for days_ago in range(60, 0, -5):
            for _ in range(random.randint(1, 3)):
                cid = random.choice(cids)
                ttype = random.choice(['Credit', 'Credit', 'Debit'])
                amount = random.choice([500, 1000, 1500, 2000, 2500, 3000, 5000])
                date = (datetime.now() - timedelta(days=days_ago)).strftime('%Y-%m-%d')
                desc = (f"Sale - Invoice #{random.randint(1000, 9999)}"
                        if ttype == 'Credit'
                        else f"Payment received - #{random.randint(1000, 9999)}")
                cursor.execute(
                    "INSERT INTO transactions(user_id, customer_id, type, amount, date, description) VALUES(?,?,?,?,?,?)",
                    (u['id'], cid, ttype, amount, date, desc)
                )
                count += 1
        print(f"  {u['name']}: {count} transactions added")
    conn.commit()
    conn.close()

# ─────────────────────────────────────────────
# STEP 5: Suppliers
# ─────────────────────────────────────────────
SUPPLIERS = {
    'kavya@gmail.com': [
        {'name': 'Wholesale Grain Traders', 'contact': '9123456780', 'due': 50000,  'paid': 30000},
        {'name': 'Spice Suppliers Ltd',     'contact': '9123456781', 'due': 25000,  'paid': 25000},
        {'name': 'Oil Distributors',        'contact': '9123456782', 'due': 35000,  'paid': 20000},
    ],
    'nIrav@gmail.com': [
        {'name': 'Electronics Wholesale Hub', 'contact': '9123456783', 'due': 500000, 'paid': 350000},
        {'name': 'Appliance Distributors',    'contact': '9123456784', 'due': 300000, 'paid': 300000},
    ],
    'asha@gmail.com': [
        {'name': 'Textile Mills',         'contact': '9123456785', 'due': 150000, 'paid': 100000},
        {'name': 'Cotton Suppliers',      'contact': '9123456786', 'due': 80000,  'paid': 60000},
        {'name': 'Garment Manufacturers', 'contact': '9123456787', 'due': 120000, 'paid': 120000},
    ],
    'vyapar.digikhata26@gmail.com': [
        {'name': 'Demo Supplier', 'contact': '9123456788', 'due': 10000, 'paid': 5000},
    ],
}

def add_suppliers(users):
    print("\n" + "=" * 60)
    print("STEP 5: Adding Suppliers")
    print("=" * 60)
    conn = get_conn()
    cursor = conn.cursor()
    for u in users:
        email = u['email']
        print(f"\n  {u['name']} ({email}):")
        for s in SUPPLIERS.get(email, []):
            cursor.execute(
                "INSERT INTO suppliers(user_id, supplier_name, contact, amount_due, amount_paid) VALUES(?,?,?,?,?)",
                (u['id'], s['name'], s['contact'], s['due'], s['paid'])
            )
            balance = s['due'] - s['paid']
            print(f"    Added: {s['name']}  (Due: Rs.{s['due']}, Paid: Rs.{s['paid']}, Balance: Rs.{balance})")
    conn.commit()
    conn.close()

# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────
def main():
    print("\n" + "*" * 60)
    print("*" + "  VYAPAR DIGIKHATA - FRESH DATA SETUP  ".center(58) + "*")
    print("*" * 60)

    clear_all_data()
    users        = add_users()
    customer_ids = add_customers(users)
    add_inventory(users)
    add_transactions(users, customer_ids)
    add_suppliers(users)

    print("\n" + "=" * 60)
    print("ALL DONE! LOGIN CREDENTIALS")
    print("=" * 60)
    for u in TEST_USERS:
        print(f"  {u['email']:<38}  {u['password']}")
    print("=" * 60)
    print("\nRun:  streamlit run app.py\n")

if __name__ == "__main__":
    main()