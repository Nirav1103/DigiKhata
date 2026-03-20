import streamlit as st
import pandas as pd
from datetime import datetime
import database as db
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def get_notification_count(user_id):
    """Get total notification count"""
    from settings import get_low_stock_items, get_overdue_customers
    low_stock = get_low_stock_items(user_id)
    overdue = get_overdue_customers(user_id)
    return len(low_stock) + len(overdue)

def show_dashboard():
    """Main dashboard function"""
    
    # Check if user is logged in
    if 'user' not in st.session_state:
        st.error("Please login first!")
        st.session_state.page = "home"
        st.rerun()
        return
    
    user_id = st.session_state.user['id']
    username = st.session_state.user['username']
    
    # Get notification count
    notification_count = get_notification_count(user_id)
    
    # Sidebar Navigation
    st.sidebar.title(f"Welcome, {username}!")
    st.sidebar.markdown("---")
    
    # Date Range Filter
    st.sidebar.subheader("📅 Date Filter")
    
    # Initialize date range in session state
    if 'date_range' not in st.session_state:
        from datetime import datetime, timedelta
        st.session_state.date_range = {
            'start': datetime.now() - timedelta(days=30),
            'end': datetime.now()
        }
    
    filter_option = st.sidebar.selectbox(
        "Filter Period",
        ["All Time", "This Week", "This Month", "Last 30 Days", "Custom Range"]
    )
    
    # Set date range based on selection
    from datetime import datetime, timedelta
    
    if filter_option == "This Week":
        start_date = datetime.now() - timedelta(days=datetime.now().weekday())
        end_date = datetime.now()
    elif filter_option == "This Month":
        start_date = datetime.now().replace(day=1)
        end_date = datetime.now()
    elif filter_option == "Last 30 Days":
        start_date = datetime.now() - timedelta(days=30)
        end_date = datetime.now()
    elif filter_option == "Custom Range":
        col1, col2 = st.sidebar.columns(2)
        with col1:
            start_date = st.date_input("From", value=st.session_state.date_range['start'])
        with col2:
            end_date = st.date_input("To", value=st.session_state.date_range['end'])
        start_date = datetime.combine(start_date, datetime.min.time())
        end_date = datetime.combine(end_date, datetime.max.time())
    else:  # All Time
        start_date = None
        end_date = None
    
    # Store in session state
    if start_date and end_date:
        st.session_state.date_range = {'start': start_date, 'end': end_date}
    
    st.sidebar.markdown("---")
    
    # Notification Button with Badge
    if notification_count > 0:
        notification_label = f"🔔 Notifications ({notification_count})"
        notification_help = f"You have {notification_count} pending alerts!"
    else:
        notification_label = "✅ Notifications"
        notification_help = "No pending notifications"
    
    if st.sidebar.button(notification_label, use_container_width=True, help=notification_help):
        st.session_state.dashboard_menu = "Notifications"
    
    st.sidebar.markdown("---")
    
    # Check if menu selection came from notification button
    if 'dashboard_menu' not in st.session_state:
        st.session_state.dashboard_menu = "Home/Overview"
    
    menu = st.sidebar.radio(
        "Navigation",
        ["Home/Overview", "Manage Customers", "Customer Transactions", 
         "Inventory Management", "Supplier Management", "Settings"],
        index=["Home/Overview", "Manage Customers", "Customer Transactions", 
               "Inventory Management", "Supplier Management", "Settings"].index(
                   st.session_state.dashboard_menu if st.session_state.dashboard_menu != "Notifications" 
                   else "Settings"
               )
    )
    
    # Update menu state
    st.session_state.dashboard_menu = menu
    
    st.sidebar.markdown("---")
    
    # Logout Button
    if st.sidebar.button("🚪 Logout", use_container_width=True):
        st.session_state.page = "home"
        if 'user' in st.session_state:
            del st.session_state.user
        if 'dashboard_menu' in st.session_state:
            del st.session_state.dashboard_menu
        st.rerun()
    
    # Main Content Area
    if menu == "Home/Overview":
        # Pass date filter to overview
        show_overview(user_id, start_date, end_date)
    elif menu == "Manage Customers":
        manage_customers(user_id)
    elif menu == "Customer Transactions":
        customer_transactions(user_id)
    elif menu == "Inventory Management":
        inventory_management(user_id)
    elif menu == "Supplier Management":
        supplier_management(user_id)
    elif menu == "Settings":
        from settings import settings_page
        # Check if first-time user
        if st.session_state.get('first_time_user', False):
            st.success("👋 Welcome to Vyapar DigiKhata! Please complete your shop settings below.")
            st.session_state['first_time_user'] = False  # Clear the flag
            settings_page(default_tab=0)  # Open shop settings tab
        # Check if notification button was clicked
        elif 'dashboard_menu' in st.session_state and st.session_state.dashboard_menu == "Notifications":
            settings_page(default_tab=3)  # Open notifications tab (now tab 3)
        else:
            settings_page()

# ============ HOME/OVERVIEW ============

def show_overview(user_id, start_date=None, end_date=None):
    """Display overview dashboard with metrics and charts"""
    st.title("📊 Business Overview")
    
    # Show active filter
    if start_date and end_date:
        st.info(f"📅 Showing data from {start_date.strftime('%d %b %Y')} to {end_date.strftime('%d %b %Y')}")
    
    # Get filtered data
    customers = db.get_customers(user_id)
    inventory_value = db.get_total_inventory_value(user_id)
    
    # Get transactions with date filter
    if start_date and end_date:
        transactions = db.get_transactions_filtered(user_id, start_date.strftime('%Y-%m-%d'), 
                                                    end_date.strftime('%Y-%m-%d'))
    else:
        transactions = db.get_transactions(user_id)
    
    # Calculate metrics from filtered transactions
    if transactions:
        trans_df = pd.DataFrame(transactions)
        income = trans_df[trans_df['type'] == 'Credit']['amount'].sum()
        expense = trans_df[trans_df['type'] == 'Debit']['amount'].sum()
        net_balance = income - expense
    else:
        income = 0
        expense = 0
        net_balance = 0
    
    # Key Metrics
    st.subheader("Key Metrics")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Customers", len(customers))
    
    with col2:
        st.metric("Total Inventory Value", f"₹{inventory_value:,.2f}")
    
    with col3:
        st.metric("Net Balance", f"₹{net_balance:,.2f}")
    
    st.markdown("---")
    
    # Charts Section
    st.subheader("📈 Business Analytics")
    
    # Graph Type Selection
    col_select1, col_select2 = st.columns([3, 1])
    
    with col_select1:
        graph_type = st.radio(
            "Select Graph Type:",
            ["📊 Normal (Quick Overview)", "📈 Detailed (Full Analysis)"],
            horizontal=True,
            help="Normal: Simple bar chart | Detailed: Area chart with trends"
        )
    
    with col_select2:
        if "Normal" in graph_type:
            normal_graph_style = st.selectbox(
                "Style:",
                ["Bar Chart", "Line Chart"],
                help="Choose visualization style"
            )
    
    # Graph 1: Transaction Trends - Toggle between Normal and Detailed
    st.markdown("#### 📈 Daily Transaction Trends")
    
    transactions = db.get_transactions(user_id)
    
    if transactions and len(transactions) > 0:
        df = pd.DataFrame(transactions)
        df['date'] = pd.to_datetime(df['date'])
        
        if "Normal" in graph_type:
            # NORMAL VIEW: Simple Bar or Line Chart showing Profit/Loss
            st.caption("Simple view showing daily net profit/loss")
            
            # Create daily net profit/loss
            df_daily = df.copy()
            df_daily['amount_signed'] = df_daily.apply(
                lambda row: row['amount'] if row['type'] == 'Credit' else -row['amount'], 
                axis=1
            )
            
            # Group by date and sum
            daily_net = df_daily.groupby('date')['amount_signed'].sum().reset_index()
            daily_net.columns = ['Date', 'Profit/Loss (₹)']
            daily_net = daily_net.set_index('Date')
            daily_net = daily_net.sort_index()
            
            # Display based on selected style
            if normal_graph_style == "Bar Chart":
                st.bar_chart(
                    daily_net,
                    height=400,
                    color='#2196F3'  # Blue for bars
                )
            else:  # Line Chart
                st.line_chart(
                    daily_net,
                    height=400,
                    color='#2196F3'  # Blue for line
                )
            
            # Summary stats
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                total_profit_days = len(daily_net[daily_net['Profit/Loss (₹)'] > 0])
                st.metric("Profitable Days", f"{total_profit_days} days", delta="Positive")
            with col_b:
                total_loss_days = len(daily_net[daily_net['Profit/Loss (₹)'] < 0])
                st.metric("Loss Days", f"{total_loss_days} days", delta="Negative", delta_color="inverse")
            with col_c:
                avg_daily_profit = daily_net['Profit/Loss (₹)'].mean()
                st.metric("Avg Daily P/L", f"₹{avg_daily_profit:,.2f}")
        
        else:
            # DETAILED VIEW: Area Chart with Credit and Debit
            st.caption("Detailed view showing Credit (Sales) and Debit (Payments)")
            
            # Create separate series for Credit and Debit
            df_credit = df[df['type'] == 'Credit'].groupby('date')['amount'].sum().reset_index()
            df_credit.columns = ['Date', 'Credit (Sales)']
            
            df_debit = df[df['type'] == 'Debit'].groupby('date')['amount'].sum().reset_index()
            df_debit.columns = ['Date', 'Debit (Payments)']
            
            # Merge and fill missing dates with 0
            df_combined = pd.merge(df_credit, df_debit, on='Date', how='outer').fillna(0)
            df_combined = df_combined.sort_values('Date')
            
            # Calculate net profit/loss (Calculated but not plotted in a separate chart now)
            df_combined['Net Profit/Loss'] = df_combined['Credit (Sales)'] - df_combined['Debit (Payments)']
            
            # Set Date as index for Streamlit chart
            df_combined = df_combined.set_index('Date')
            
            # Display area chart using Streamlit
            st.area_chart(
                df_combined[['Credit (Sales)', 'Debit (Payments)']],
                height=400,
                color=['#4CAF50', '#F44336']  # Green for Credit, Red for Debit
            )
            
            # --- "Net Profit/Loss Trend" Chart REMOVED Here ---
        
        # Show summary stats (common for both views)
        st.write("")
        st.divider()
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            st.metric("Total Transactions", len(transactions))
        with col_b:
            total_credit = df[df['type'] == 'Credit']['amount'].sum()
            st.metric("Total Credit", f"₹{total_credit:,.2f}")
        with col_c:
            total_debit = df[df['type'] == 'Debit']['amount'].sum()
            st.metric("Total Debit", f"₹{total_debit:,.2f}")
        
        # Add profit/loss indicator
        net_total = total_credit - total_debit
        if net_total > 0:
            st.success(f"📈 Net Profit: ₹{net_total:,.2f}")
        elif net_total < 0:
            st.error(f"📉 Net Loss: ₹{abs(net_total):,.2f}")
        else:
            st.info(f"⚖️ Break Even: ₹{net_total:,.2f}")
    else:
        st.info("No transaction data available yet. Add transactions to see trends.")
    
    st.markdown("---")
    
    # Second Row: Pie Chart and Bar Chart
    col1, col2 = st.columns(2)
    
    # Graph 2: Pie Chart - Income vs Expenses
    with col1:
        st.markdown("#### 💰 Credit vs Debit Distribution")
        
        if income > 0 or expense > 0:
            # Create dataframe for visualization
            chart_data = pd.DataFrame({
                'Category': ['Income', 'Expenses'],
                'Amount': [income, expense]
            })
            
            # Display metrics
            st.write(f"**Total Credit:** ₹{income:,.2f}")
            st.write(f"**Total Debit:** ₹{expense:,.2f}")
            st.write(f"**Net Balance:** ₹{income - expense:,.2f}")
            
            # Show percentage breakdown with progress bars
            total = income + expense
            if total > 0:
                income_pct = (income / total) * 100
                expense_pct = (expense / total) * 100
                
                st.markdown("**Breakdown:**")
                st.progress(income_pct / 100, text=f"Credit: {income_pct:.1f}%")
                st.progress(expense_pct / 100, text=f"Debit: {expense_pct:.1f}%")
        else:
            st.info("No transaction data available yet.")
    
    # Graph 3: Bar Chart - Customer Profit Comparison
    with col2:
        st.markdown("#### 👥 Customer Profit Comparison")
        
        customer_profits = db.get_customer_profit_comparison(user_id)
        
        if customer_profits and len(customer_profits) > 0:
            # Prepare data
            df_profit = pd.DataFrame(customer_profits)
            
            # Take top 10 customers
            df_profit = df_profit.head(10)
            
            # Create chart data
            chart_data = df_profit[['name', 'net_profit']].copy()
            chart_data.columns = ['Customer', 'Net Profit']
            chart_data = chart_data.set_index('Customer')
            
            # Display bar chart
            st.bar_chart(chart_data, height=350, color='#4CAF50')
            
            # Show top customer
            top_customer = df_profit.iloc[0]
            st.write(f"**Top Customer:** {top_customer['name']}")
            st.write(f"**Net Profit:** ₹{top_customer['net_profit']:,.2f}")
        else:
            st.info("No customer transaction data available yet.")

# ============ MANAGE CUSTOMERS ============

def manage_customers(user_id):
    """Manage customers - Add and View"""
    st.title("👥 Manage Customers")
    
    # Add Customer Form
    st.subheader("Add New Customer")
    
    with st.form("add_customer_form"):
        name = st.text_input("Customer Name *")
        contact = st.text_input(
            "Contact Number *", 
            max_chars=10,
            placeholder="10-digit mobile number",
            help="Enter exactly 10 digits"
        )
        address = st.text_area("Address")
        
        submitted = st.form_submit_button("Add Customer")
        
        if submitted:
            if name and contact:
                # Validate phone number
                phone_valid, phone_result = db.validate_phone(contact)
                if not phone_valid:
                    st.error(phone_result)
                else:
                    # Add customer with validated phone
                    success, message = db.add_customer(user_id, name, phone_result, address)
                    if success:
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(message)
            else:
                st.error("Please enter customer name and contact number!")
    
    st.markdown("---")
    
    # View Customers
    st.subheader("Existing Customers")
    
    customers = db.get_customers(user_id)
    
    if customers:
        df = pd.DataFrame(customers)
        df = df[['id', 'name', 'contact', 'address']]
        df.columns = ['ID', 'Name', 'Contact', 'Address']
        
        # Use st.dataframe for better theme compatibility
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "ID": st.column_config.NumberColumn("ID", width="small"),
                "Name": st.column_config.TextColumn("Name", width="medium"),
                "Contact": st.column_config.TextColumn("Contact", width="medium"),
                "Address": st.column_config.TextColumn("Address", width="large")
            }
        )
        
        st.info(f"📊 Total Customers: {len(customers)}")
    else:
        st.info("No customers found. Add your first customer above!")

# ============ CUSTOMER TRANSACTIONS ============

def customer_transactions(user_id):
    """Handle customer transactions"""
    st.title("💳 Customer Transactions")
    
    customers = db.get_customers(user_id)
    
    if not customers:
        st.warning("No customers available. Please add customers first!")
        return
    
    # Select Customer
    customer_options = {f"{c['name']} (ID: {c['id']})": c['id'] for c in customers}
    selected_customer = st.selectbox("Select Customer", options=list(customer_options.keys()))
    customer_id = customer_options[selected_customer]
    
    st.markdown("---")
    
    # Add Transaction
    st.subheader("Add Transaction")
    
    col1, col2 = st.columns(2)
    
    with col1:
        trans_type = st.selectbox("Transaction Type", ["Credit", "Debit"])
    
    with col2:
        amount = st.number_input("Amount (₹)", min_value=0.0, step=0.01)
    
    date = st.date_input("Date", value=datetime.now())
    
    # Get inventory items
    inventory = db.get_inventory(user_id)
    
    # Item selection for Credit transactions (sales)
    selected_item_id = None
    quantity_sold = None
    description = ""
    
    if trans_type == "Credit":
        st.markdown("**📦 Select Item from Inventory**")
        
        if inventory:
            # Create item options with stock info
            item_options = {
                f"{item['item_name']} (Stock: {item['quantity']}, Price: ₹{item['price_per_unit']})": item['id'] 
                for item in inventory
            }
            
            selected_item = st.selectbox("Select Item *", options=list(item_options.keys()))
            selected_item_id = item_options[selected_item]
            
            # Get selected item details
            selected_item_data = next(item for item in inventory if item['id'] == selected_item_id)
            
            quantity_sold = st.number_input(
                f"Quantity (Available: {selected_item_data['quantity']})", 
                min_value=1, 
                max_value=selected_item_data['quantity'],
                step=1
            )
            
            # Auto-calculate amount
            calculated_amount = quantity_sold * selected_item_data['price_per_unit']
            st.info(f"💡 Suggested Amount: ₹{calculated_amount:,.2f}")
            
            # Auto-generate description
            description = f"Sale: {selected_item_data['item_name']} x {quantity_sold}"
        else:
            st.warning("⚠️ No inventory items available! Please add items to inventory first.")
            st.stop()
    else:
        # For Debit transactions (payments received)
        description = st.text_area("Description", placeholder="e.g., Payment received, Advance payment")
    
    if st.button("Add Transaction", type="primary"):
        if amount > 0:
            if trans_type == "Credit":
                if selected_item_id and quantity_sold:
                    success, message = db.add_transaction(
                        user_id, customer_id, trans_type, amount, 
                        date.strftime("%Y-%m-%d"), description,
                        selected_item_id, quantity_sold
                    )
                    if success:
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(message)
                else:
                    st.error("Please select an item and quantity!")
            else:
                # Debit transaction (no inventory update needed)
                success, message = db.add_transaction(
                    user_id, customer_id, trans_type, amount, 
                    date.strftime("%Y-%m-%d"), description
                )
                if success:
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)
        else:
            st.error("Please enter a valid amount!")
    
    st.markdown("---")
    
    # View Transaction History
    st.subheader("Transaction History")
    
    transactions = db.get_transactions(user_id, customer_id)
    
    if transactions:
        df = pd.DataFrame(transactions)
        df = df[['id', 'type', 'amount', 'date', 'description']]
        df.columns = ['ID', 'Type', 'Amount (₹)', 'Date', 'Description']
        
        # Separate transactions by type for better visibility
        st.write("**All Transactions:**")
        
        # Display dataframe with proper column config for theme compatibility
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "ID": st.column_config.NumberColumn("ID", width="small"),
                "Type": st.column_config.TextColumn("Type", width="small"),
                "Amount (₹)": st.column_config.NumberColumn("Amount (₹)", format="₹%.2f", width="medium"),
                "Date": st.column_config.TextColumn("Date", width="medium"),
                "Description": st.column_config.TextColumn("Description", width="large")
            }
        )
        
        st.write("")
        
        # Show separate cards for Credit and Debit
        col_credit, col_debit = st.columns(2)
        
        with col_credit:
            credit_df = df[df['Type'] == 'Credit']
            if not credit_df.empty:
                st.success(f"**💰 Credit Transactions ({len(credit_df)})**")
                st.dataframe(
                    credit_df[['Date', 'Amount (₹)', 'Description']],
                    use_container_width=True,
                    hide_index=True
                )
            else:
                st.info("No credit transactions")
        
        with col_debit:
            debit_df = df[df['Type'] == 'Debit']
            if not debit_df.empty:
                st.warning(f"**💳 Debit Transactions ({len(debit_df)})**")
                st.dataframe(
                    debit_df[['Date', 'Amount (₹)', 'Description']],
                    use_container_width=True,
                    hide_index=True
                )
            else:
                st.info("No debit transactions")
        
        st.divider()
        
        # Summary
        total_credit = df[df['Type'] == 'Credit']['Amount (₹)'].sum()
        total_debit = df[df['Type'] == 'Debit']['Amount (₹)'].sum()
        balance = total_credit - total_debit
        
        st.markdown("### Summary")
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Credit", f"₹{total_credit:,.2f}", delta=None, delta_color="normal")
        col2.metric("Total Debit", f"₹{total_debit:,.2f}", delta=None, delta_color="normal")
        
        # Show balance with color indicator
        if balance > 0:
            col3.metric("Balance", f"₹{balance:,.2f}", delta="Customer owes", delta_color="normal")
        elif balance < 0:
            col3.metric("Balance", f"₹{balance:,.2f}", delta="You owe", delta_color="inverse")
        else:
            col3.metric("Balance", f"₹{balance:,.2f}", delta="Settled", delta_color="off")
    else:
        st.info("No transactions found for this customer.")

# ============ INVENTORY MANAGEMENT ============

def inventory_management(user_id):
    """Manage inventory items"""
    st.title("📦 Inventory Management")
    
    tab1, tab2 = st.tabs(["Add New Item", "Update Stock"])
    
    # Tab 1: Add New Item
    with tab1:
        st.subheader("Add New Inventory Item")
        
        with st.form("add_inventory_form"):
            item_name = st.text_input("Item Name *")
            col1, col2 = st.columns(2)
            
            with col1:
                quantity = st.number_input("Quantity", min_value=0, step=1)
            
            with col2:
                price_per_unit = st.number_input("Price per Unit (₹)", min_value=0.0, step=0.01)
            
            submitted = st.form_submit_button("Add Item")
            
            if submitted:
                if item_name:
                    db.add_inventory_item(user_id, item_name, quantity, price_per_unit)
                    st.success(f"Item '{item_name}' added successfully!")
                    st.rerun()
                else:
                    st.error("Please enter item name!")
    
    # Tab 2: Update Stock
    with tab2:
        st.subheader("Update Stock Levels")
        
        inventory = db.get_inventory(user_id)
        
        if inventory:
            item_options = {f"{item['item_name']} (Current: {item['quantity']})": item['id'] 
                          for item in inventory}
            
            selected_item = st.selectbox("Select Item", options=list(item_options.keys()))
            item_id = item_options[selected_item]
            
            new_quantity = st.number_input("New Quantity", min_value=0, step=1)
            
            if st.button("Update Quantity"):
                db.update_inventory_quantity(item_id, new_quantity)
                st.success("Stock updated successfully!")
                st.rerun()
        else:
            st.info("No inventory items found. Add items in the 'Add New Item' tab.")
    
    st.markdown("---")
    
    # View Current Stock
    st.subheader("Current Stock Levels")
    
    inventory = db.get_inventory(user_id)
    
    if inventory:
        df = pd.DataFrame(inventory)
        df['total_value'] = df['quantity'] * df['price_per_unit']
        df = df[['id', 'item_name', 'quantity', 'price_per_unit', 'total_value']]
        df.columns = ['ID', 'Item Name', 'Quantity', 'Price/Unit (₹)', 'Total Value (₹)']
        
        # Display with proper column config for theme compatibility
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "ID": st.column_config.NumberColumn("ID", width="small"),
                "Item Name": st.column_config.TextColumn("Item Name", width="medium"),
                "Quantity": st.column_config.NumberColumn("Quantity", width="small"),
                "Price/Unit (₹)": st.column_config.NumberColumn("Price/Unit (₹)", format="₹%.2f", width="medium"),
                "Total Value (₹)": st.column_config.NumberColumn("Total Value (₹)", format="₹%.2f", width="medium")
            }
        )
        
        # Total Inventory Value
        total_value = df['Total Value (₹)'].sum()
        st.metric("Total Inventory Value", f"₹{total_value:,.2f}")
    else:
        st.info("No inventory items available.")

# ============ SUPPLIER MANAGEMENT ============

def supplier_management(user_id):
    """Manage suppliers and their transactions"""
    st.title("🏭 Supplier Management")
    
    tab1, tab2 = st.tabs(["Add Supplier", "Manage Payments & Stock"])
    
    # Tab 1: Add Supplier
    with tab1:
        st.subheader("Add New Supplier")
        
        with st.form("add_supplier_form"):
            supplier_name = st.text_input("Supplier Name *")
            contact = st.text_input("Contact Number *", max_chars=10, 
                                   help="Enter 10-digit phone number")
            
            col1, col2 = st.columns(2)
            with col1:
                amount_due = st.number_input("Initial Amount Due (₹)", min_value=0.0, step=0.01)
            with col2:
                amount_paid = st.number_input("Initial Amount Paid (₹)", min_value=0.0, step=0.01)
            
            submitted = st.form_submit_button("Add Supplier")
            
            if submitted:
                if supplier_name and contact:
                    # Validate phone
                    phone_valid, phone_result = db.validate_phone(contact)
                    if not phone_valid:
                        st.error(phone_result)
                    else:
                        db.add_supplier(user_id, supplier_name, phone_result, amount_due, amount_paid)
                        st.success(f"Supplier '{supplier_name}' added successfully!")
                        st.rerun()
                else:
                    st.error("Please enter supplier name and contact number!")
    
    # Tab 2: Manage Payments & Stock Purchase
    with tab2:
        st.subheader("Record Supplier Transactions")
        
        suppliers = db.get_suppliers(user_id)
        
        if suppliers:
            supplier_options = {s['supplier_name']: s['id'] for s in suppliers}
            selected_supplier = st.selectbox("Select Supplier", options=list(supplier_options.keys()))
            supplier_id = supplier_options[selected_supplier]
            
            transaction_type = st.radio("Transaction Type", 
                                       ["💰 Payment (Reduce Due)", "📦 Stock Purchase (Add Due & Update Inventory)"])
            
            if "Purchase" in transaction_type:
                # Stock Purchase - Link with Inventory
                st.markdown("### 📦 Stock Purchase Details")
                
                inventory = db.get_inventory(user_id)
                
                if inventory:
                    # Select or add new item
                    item_choice = st.radio("Item Selection", ["Select Existing Item", "Add New Item"])
                    
                    if item_choice == "Select Existing Item":
                        item_options = {f"{item['item_name']} (Current Stock: {item['quantity']})": item['id'] 
                                      for item in inventory}
                        selected_item_display = st.selectbox("Select Item", options=list(item_options.keys()))
                        selected_item_id = item_options[selected_item_display]
                        
                        # Get item details
                        selected_item = next(item for item in inventory if item['id'] == selected_item_id)
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            quantity_purchased = st.number_input("Quantity Purchased", min_value=1, step=1)
                        with col2:
                            price_per_unit = st.number_input("Price per Unit (₹)", 
                                                            value=float(selected_item['price_per_unit']),
                                                            min_value=0.01, step=0.01)
                        
                        total_amount = quantity_purchased * price_per_unit
                        st.info(f"💵 Total Amount: ₹{total_amount:,.2f}")
                        
                        if st.button("Record Stock Purchase", type="primary"):
                            # Update inventory
                            new_quantity = selected_item['quantity'] + quantity_purchased
                            db.update_inventory_quantity(selected_item_id, new_quantity)
                            
                            # Update supplier due
                            db.update_supplier_due(supplier_id, total_amount)
                            
                            st.success(f"✅ Stock purchase recorded!")
                            st.success(f"📦 Inventory updated: {selected_item['item_name']} +{quantity_purchased} units")
                            st.success(f"💰 Supplier due increased by ₹{total_amount:,.2f}")
                            st.rerun()
                    
                    else:  # Add New Item
                        st.markdown("**Add New Inventory Item**")
                        new_item_name = st.text_input("New Item Name")
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            quantity_purchased = st.number_input("Quantity", min_value=1, step=1)
                        with col2:
                            price_per_unit = st.number_input("Price per Unit (₹)", min_value=0.01, step=0.01)
                        
                        total_amount = quantity_purchased * price_per_unit
                        st.info(f"💵 Total Amount: ₹{total_amount:,.2f}")
                        
                        if st.button("Add Item & Record Purchase", type="primary"):
                            if new_item_name:
                                # Add new inventory item
                                db.add_inventory_item(user_id, new_item_name, quantity_purchased, price_per_unit)
                                
                                # Update supplier due
                                db.update_supplier_due(supplier_id, total_amount)
                                
                                st.success(f"✅ New item '{new_item_name}' added to inventory!")
                                st.success(f"💰 Supplier due increased by ₹{total_amount:,.2f}")
                                st.rerun()
                            else:
                                st.error("Please enter item name!")
                else:
                    st.warning("No inventory items available. You can add a new item below.")
                    
                    new_item_name = st.text_input("Item Name")
                    col1, col2 = st.columns(2)
                    with col1:
                        quantity_purchased = st.number_input("Quantity", min_value=1, step=1)
                    with col2:
                        price_per_unit = st.number_input("Price per Unit (₹)", min_value=0.01, step=0.01)
                    
                    total_amount = quantity_purchased * price_per_unit
                    st.info(f"💵 Total Amount: ₹{total_amount:,.2f}")
                    
                    if st.button("Add Item & Record Purchase", type="primary"):
                        if new_item_name:
                            db.add_inventory_item(user_id, new_item_name, quantity_purchased, price_per_unit)
                            db.update_supplier_due(supplier_id, total_amount)
                            st.success("✅ Item added and purchase recorded!")
                            st.rerun()
                        else:
                            st.error("Please enter item name!")
            
            else:  # Payment
                amount = st.number_input("Payment Amount (₹)", min_value=0.0, step=0.01)
                
                if st.button("Record Payment"):
                    if amount > 0:
                        db.update_supplier_payment(supplier_id, amount)
                        st.success(f"Payment of ₹{amount:,.2f} recorded!")
                        st.rerun()
                    else:
                        st.error("Please enter a valid amount!")
        else:
            st.info("No suppliers found. Add a supplier in the 'Add Supplier' tab.")
    
    st.markdown("---")
    
    # View Suppliers
    st.subheader("Supplier List")
    
    suppliers = db.get_suppliers(user_id)
    
    if suppliers:
        df = pd.DataFrame(suppliers)
        df['balance'] = df['amount_due'] - df['amount_paid']
        df = df[['id', 'supplier_name', 'contact', 'amount_due', 'amount_paid', 'balance']]
        df.columns = ['ID', 'Supplier Name', 'Contact', 'Amount Due (₹)', 'Amount Paid (₹)', 'Balance (₹)']
        
        # Display with proper column config for theme compatibility
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "ID": st.column_config.NumberColumn("ID", width="small"),
                "Supplier Name": st.column_config.TextColumn("Supplier Name", width="medium"),
                "Contact": st.column_config.TextColumn("Contact", width="medium"),
                "Amount Due (₹)": st.column_config.NumberColumn("Amount Due (₹)", format="₹%.2f", width="medium"),
                "Amount Paid (₹)": st.column_config.NumberColumn("Amount Paid (₹)", format="₹%.2f", width="medium"),
                "Balance (₹)": st.column_config.NumberColumn("Balance (₹)", format="₹%.2f", width="medium")
            }
        )
        
        # Summary
        total_due = df['Amount Due (₹)'].sum()
        total_paid = df['Amount Paid (₹)'].sum()
        total_balance = df['Balance (₹)'].sum()
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Due", f"₹{total_due:,.2f}")
        col2.metric("Total Paid", f"₹{total_paid:,.2f}")
        col3.metric("Outstanding Balance", f"₹{total_balance:,.2f}")
    else:
        st.info("No suppliers available.")