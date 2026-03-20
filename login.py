import streamlit as st
from database import get_users

def validate_email_simple(email):
    """Simple email validation using Python string methods"""
    if not email:
        return False, "Email cannot be empty"
    
    if '@' not in email:
        return False, "Email must contain @ symbol"
    
    # Split by @ to check parts
    parts = email.split('@')
    if len(parts) != 2:
        return False, "Email format is invalid"
    
    username, domain = parts
    
    if not username:
        return False, "Email must have a username before @"
    
    if not domain:
        return False, "Email must have a domain after @"
    
    # Check if domain has extension (like .com, .in)
    if '.' not in domain:
        return False, "Email must have domain extension (e.g., @gmail.com)"
    
    domain_parts = domain.split('.')
    if len(domain_parts) < 2:
        return False, "Email must have valid domain extension"
    
    # Check if extension exists and has at least 2 characters
    extension = domain_parts[-1]
    if len(extension) < 2:
        return False, "Domain extension must be at least 2 characters"
    
    return True, ""

def login_page():
    # Header
    st.title("🔐 Login")
    st.write("Welcome back! Please login to your account")
    st.divider()
    
    # Create centered layout
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.subheader("Enter Your Credentials")
        st.write("")
        
        # Email Input
        mail = st.text_input(
            "📧 Email Address",
            placeholder="example@gmail.com",
            help="Enter your registered email"
        )
        
        # Password Input
        password = st.text_input(
            "🔒 Password",
            type="password",
            placeholder="Enter your password",
            help="Enter your password"
        )
        
        st.write("")
        
        # Buttons
        col_a, col_b = st.columns(2)
        
        with col_a:
            login_btn = st.button("🚀 Login", key="login_submit_btn", use_container_width=True, type="primary")
        
        with col_b:
            back_btn = st.button("🏠 Back", key="back_home_btn", use_container_width=True)
        
        # Handle Back Button
        if back_btn:
            st.session_state.page = "home"
            st.rerun()
        
        # Handle Login
        if login_btn:
            # Validate inputs
            errors = []
            
            # Validate email
            email_valid, email_error = validate_email_simple(mail)
            if not email_valid:
                errors.append(f"❌ {email_error}")
            
            # Validate password
            if not password:
                errors.append("❌ Password cannot be empty")
            elif len(password) < 8:
                errors.append("❌ Password must be at least 8 characters")
            
            # Show errors if any
            if errors:
                for error in errors:
                    st.error(error)
            else:
                # Proceed with login
                data = get_users(mail)
                
                if data:
                    user_row = data[0]
                    db_id = user_row[0]
                    db_owner = user_row[1]
                    db_mail = user_row[2]
                    db_password = user_row[4]
                    
                    if db_mail == mail and str(db_password) == password:
                        st.success(f"✅ Welcome back, {db_owner}!")
                        
                        # Save user data to session state
                        st.session_state['user'] = {
                            'id': db_id,
                            'username': db_owner,
                            'email': db_mail
                        }
                        
                        # Redirect to dashboard
                        st.session_state.page = "dashboard"
                        st.rerun()
                    else:
                        st.error("❌ Invalid email or password")
                else:
                    st.error("❌ User not found. Please sign up first")
        
        st.divider()
        
        # Sign up link
        st.info("Don't have an account?")
        if st.button("📝 Create New Account", key="goto_signup", use_container_width=True):
            st.session_state.page = "sign_up"
            st.rerun()