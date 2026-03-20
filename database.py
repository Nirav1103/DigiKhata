import sqlite3

# --- CONNECTION ---
def get_connection():
    conn = sqlite3.connect("Vyapar_Digikhata.db")
    conn.row_factory = sqlite3.Row
    return conn

def create_table():
    conn = get_connection()
    cursor = conn.cursor()
    
    # Users Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        owner_name TEXT,
        email TEXT,
        shop_name TEXT,
        password TEXT
    )
    """)
    
    # Customers Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS customers(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        name TEXT,
        contact TEXT UNIQUE,
        address TEXT,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    """)
    
    # Inventory Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS inventory(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        item_name TEXT,
        quantity INTEGER,
        price_per_unit REAL,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    """)
    
    # Transactions Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        customer_id INTEGER,
        type TEXT,
        amount REAL,
        date TEXT,
        description TEXT,
        FOREIGN KEY(user_id) REFERENCES users(id),
        FOREIGN KEY(customer_id) REFERENCES customers(id)
    )
    """)

    # Suppliers Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS suppliers(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        supplier_name TEXT,
        contact TEXT,
        amount_due REAL,
        amount_paid REAL,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    """)
    
    conn.commit()
    conn.close()

# Initialize tables immediately
create_table()

# --- VALIDATION FUNCTIONS ---

def validate_phone(phone):
    """
    Validate and format phone number
    Returns: (is_valid: bool, result: str or error_message)
    """
    if not phone:
        return False, "Phone number cannot be empty"
    
    # Remove any spaces, dashes, or parentheses
    cleaned_phone = ''.join(filter(str.isdigit, phone))
    
    # Check if it's exactly 10 digits
    if len(cleaned_phone) != 10:
        return False, "Phone number must be exactly 10 digits"
    
    # Check if it starts with valid digit (6-9 for Indian mobile numbers)
    if cleaned_phone[0] not in ['6', '7', '8', '9']:
        return False, "Mobile number must start with 6, 7, 8, or 9"
    
    return True, cleaned_phone

# --- USER FUNCTIONS ---

def insert_user(name, email, shop_name, password):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users(owner_name,email,shop_name,password) VALUES(?,?,?,?)", 
                   (name, email, shop_name, password))
    conn.commit()
    conn.close()

def get_users(email):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users where email=?", (email,))
    data = cursor.fetchall()
    conn.close()
    return data

def chek_pass(p):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE password = ?", (p,))
    data = cursor.fetchone()
    conn.close()
    return True if data else False

# --- CUSTOMER FUNCTIONS ---

def check_contact_exists(contact):
    """Check if a contact number already exists"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM customers WHERE contact=?", (contact,))
    result = cursor.fetchone()
    conn.close()
    return result is not None

def add_customer(user_id, name, contact, address):
    """Add customer with unique contact validation"""
    # First check if contact already exists (for all users, not just current user)
    if check_contact_exists(contact):
        return False, "❌ This contact number is already registered with another customer!"
    
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO customers(user_id, name, contact, address) VALUES(?,?,?,?)", 
                       (user_id, name, contact, address))
        conn.commit()
        conn.close()
        return True, "✅ Customer added successfully!"
    except sqlite3.IntegrityError:
        return False, "❌ This contact number is already registered!"

def get_customers(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM customers WHERE user_id=?", (user_id,))
    customers = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return customers

def get_customer_by_id(customer_id):
    """Get a specific customer by ID"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM customers WHERE id = ?", (customer_id,))
    customer = cursor.fetchone()
    conn.close()
    return dict(customer) if customer else None

# --- INVENTORY FUNCTIONS ---

def add_inventory_item(user_id, item_name, quantity, price, cost_price=0.0):
    """Add inventory item with cost price for profit margin"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Check if cost_price column exists, if not add it
    cursor.execute("PRAGMA table_info(inventory)")
    columns = [column[1] for column in cursor.fetchall()]
    
    if 'cost_price' not in columns:
        cursor.execute("ALTER TABLE inventory ADD COLUMN cost_price REAL DEFAULT 0.0")
    
    cursor.execute("INSERT INTO inventory(user_id, item_name, quantity, price_per_unit, cost_price) VALUES(?,?,?,?,?)", 
                   (user_id, item_name, quantity, price, cost_price))
    conn.commit()
    conn.close()

def get_inventory(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    
    # Check if cost_price column exists
    cursor.execute("PRAGMA table_info(inventory)")
    columns = [column[1] for column in cursor.fetchall()]
    
    if 'cost_price' not in columns:
        cursor.execute("ALTER TABLE inventory ADD COLUMN cost_price REAL DEFAULT 0.0")
        conn.commit()
    
    cursor.execute("SELECT * FROM inventory WHERE user_id=?", (user_id,))
    items = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return items

def update_inventory_quantity(item_id, new_quantity):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE inventory SET quantity=? WHERE id=?", (new_quantity, item_id))
    conn.commit()
    conn.close()

def get_total_inventory_value(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(quantity * price_per_unit) FROM inventory WHERE user_id=?", (user_id,))
    result = cursor.fetchone()[0]
    conn.close()
    return result if result else 0.0

# --- TRANSACTION FUNCTIONS ---

def add_transaction(user_id, customer_id, trans_type, amount, date, description, item_id=None, quantity=None):
    """Add transaction and update inventory if item is purchased"""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        # Insert transaction
        cursor.execute("INSERT INTO transactions(user_id, customer_id, type, amount, date, description) VALUES(?,?,?,?,?,?)", 
                       (user_id, customer_id, trans_type, amount, date, description))
        
        # If item is purchased (Credit transaction with item), reduce inventory
        if trans_type == "Credit" and item_id and quantity:
            # Check current stock
            cursor.execute("SELECT quantity FROM inventory WHERE id=?", (item_id,))
            current_stock = cursor.fetchone()
            
            if current_stock and current_stock[0] >= quantity:
                # Update inventory
                cursor.execute("UPDATE inventory SET quantity = quantity - ? WHERE id=?", (quantity, item_id))
                conn.commit()
                conn.close()
                return True, "Transaction added and inventory updated!"
            else:
                conn.rollback()
                conn.close()
                return False, "Insufficient stock! Transaction cancelled."
        
        conn.commit()
        conn.close()
        return True, "Transaction added successfully!"
        
    except Exception as e:
        conn.rollback()
        conn.close()
        return False, f"Error: {str(e)}"

def get_transactions(user_id, customer_id=None):
    conn = get_connection()
    cursor = conn.cursor()
    if customer_id:
        cursor.execute("SELECT * FROM transactions WHERE user_id=? AND customer_id=? ORDER BY date DESC", (user_id, customer_id))
    else:
        cursor.execute("SELECT * FROM transactions WHERE user_id=? ORDER BY date DESC", (user_id,))
    transactions = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return transactions

def get_transactions_filtered(user_id, start_date, end_date, customer_id=None):
    """Get transactions within a date range"""
    conn = get_connection()
    cursor = conn.cursor()
    if customer_id:
        cursor.execute(
            "SELECT * FROM transactions WHERE user_id=? AND customer_id=? AND date BETWEEN ? AND ? ORDER BY date DESC",
            (user_id, customer_id, start_date, end_date)
        )
    else:
        cursor.execute(
            "SELECT * FROM transactions WHERE user_id=? AND date BETWEEN ? AND ? ORDER BY date DESC",
            (user_id, start_date, end_date)
        )
    transactions = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return transactions

def get_net_balance(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT type, SUM(amount) FROM transactions WHERE user_id=? GROUP BY type", (user_id,))
    rows = cursor.fetchall()
    
    credits = 0
    debits = 0
    for row in rows:
        if row['type'] == 'Credit':
            credits = row[1]
        elif row['type'] == 'Debit':
            debits = row[1]
            
    conn.close()
    return credits - debits

def get_income_expense(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT type, SUM(amount) FROM transactions WHERE user_id=? GROUP BY type", (user_id,))
    rows = cursor.fetchall()
    
    income = 0
    expense = 0
    for row in rows:
        if row['type'] == 'Credit':
            income = row[1]
        elif row['type'] == 'Debit':
            expense = row[1]
            
    conn.close()
    return income, expense

def get_customer_profit_comparison(user_id):
    """Get profit/loss for each customer"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            c.name,
            c.id,
            SUM(CASE WHEN t.type = 'Credit' THEN t.amount ELSE 0 END) as total_credit,
            SUM(CASE WHEN t.type = 'Debit' THEN t.amount ELSE 0 END) as total_debit,
            SUM(CASE WHEN t.type = 'Credit' THEN t.amount ELSE -t.amount END) as net_profit
        FROM customers c
        LEFT JOIN transactions t ON c.id = t.customer_id
        WHERE c.user_id = ?
        GROUP BY c.id, c.name
        HAVING (total_credit > 0 OR total_debit > 0)
        ORDER BY net_profit DESC
    """, (user_id,))
    
    results = cursor.fetchall()
    conn.close()
    return [dict(row) for row in results]

# --- SUPPLIER FUNCTIONS ---

def add_supplier(user_id, name, contact, due, paid):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO suppliers(user_id, supplier_name, contact, amount_due, amount_paid) VALUES(?,?,?,?,?)", 
                   (user_id, name, contact, due, paid))
    conn.commit()
    conn.close()

def get_suppliers(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM suppliers WHERE user_id=?", (user_id,))
    suppliers = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return suppliers

def update_supplier_due(supplier_id, amount):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE suppliers SET amount_due = amount_due + ? WHERE id=?", (amount, supplier_id))
    conn.commit()
    conn.close()

def update_supplier_payment(supplier_id, amount):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE suppliers SET amount_paid = amount_paid + ? WHERE id=?", (amount, supplier_id))
    conn.commit()
    conn.close()