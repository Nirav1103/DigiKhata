import streamlit as st
from login import login_page 
from sign_up import sign_up_page
from dashboard import show_dashboard 

st.set_page_config(
    page_title="Vyapar : DigiKhata",
    page_icon="📒",
    layout="centered"
)

# --- ENHANCED CSS STYLING WITH LIGHT BLUE THEME ---
st.markdown("""
    <style>
    /* Main Title Styling */
    .main-header {
        text-align: center;
        padding: 2rem 0 1rem 0;
        
        /* UPDATED: Text is now Light Blue (#0284C7) to match the theme */
        /* The emoji will appear naturally (Yellow) */
        color: #0284C7 !important; 
        background: none;
        -webkit-text-fill-color: initial;
        -webkit-background-clip: initial;
        background-clip: initial;
        
        font-size: 3.8rem;
        font-weight: bold;
        margin-bottom: 0;
    }
    
    /* Subtitle Styling */
    .sub-header {
        text-align: center;
        color: #475569;
        font-size: 1.3rem;
        margin-top: 0;
        padding-bottom: 1rem;
    }
    
    /* Hero Feature Box */
    .feature-box {
        background: linear-gradient(135deg, #0EA5E9 0%, #0284C7 100%);
        padding: 2.5rem;
        border-radius: 20px;
        text-align: center;
        color: white;
        margin: 1rem 0;
        box-shadow: 0 8px 20px rgba(14, 165, 233, 0.3);
    }
    .feature-title {
        font-size: 1.8rem;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    .feature-text {
        font-size: 1.15rem;
        line-height: 1.7;
        opacity: 0.95;
    }
    
    /* Section Headers */
    .section-header {
        text-align: center;
        color: #0284C7 !important; /* Added !important for Dark Mode */
        font-size: 2.5rem;
        font-weight: bold;
        margin: 3rem 0 1rem 0;
    }
    
    .section-subtitle {
        text-align: center;
        color: #64748b !important; /* Added !important for Dark Mode */
        font-size: 1.1rem;
        margin-bottom: 2.5rem;
        line-height: 1.6;
    }
    
    /* Feature Cards - ENHANCED */
    .benefit-card {
        background: linear-gradient(145deg, #F0F9FF 0%, #E0F2FE 100%);
        padding: 2rem;
        border-radius: 15px;
        margin: 0.5rem 0;
        border-left: 5px solid #0EA5E9;
        transition: all 0.3s;
        box-shadow: 0 4px 6px rgba(14, 165, 233, 0.1);
        min-height: 200px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    .benefit-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 12px 24px rgba(14, 165, 233, 0.2);
        border-left-width: 8px;
    }
    
    /* Why Choose Cards */
    .why-choose-card {
        padding: 1.2rem;
        margin: 0.5rem 0;
        background: linear-gradient(145deg, #F0F9FF 0%, #E0F2FE 100%);
        border-radius: 10px;
        border: 2px solid #BAE6FD;
        min-height: 85px;
        display: flex;
        align-items: center;
        transition: all 0.3s;
    }
    .why-choose-card:hover {
        transform: translateX(8px);
        box-shadow: 0 6px 15px rgba(14, 165, 233, 0.15);
        border-color: #0EA5E9;
    }
    
    /* How It Works Steps */
    .step-card {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        margin: 1rem 0;
        border: 3px solid #BAE6FD;
        transition: all 0.3s;
        position: relative;
    }
    .step-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 25px rgba(14, 165, 233, 0.2);
        border-color: #0EA5E9;
    }
    .step-number {
        position: absolute;
        top: -20px;
        left: 50%;
        transform: translateX(-50%);
        width: 50px;
        height: 50px;
        background: linear-gradient(135deg, #0EA5E9 0%, #0284C7 100%);
        color: white;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
        font-weight: bold;
        box-shadow: 0 4px 10px rgba(14, 165, 233, 0.3);
    }
    .step-title {
        font-size: 1.4rem;
        font-weight: bold;
        color: #0284C7 !important; /* Added !important for Dark Mode visibility */
        margin: 1.5rem 0 0.5rem 0;
        text-align: center;
    }
    .step-description {
        color: #64748b !important; /* Added !important for Dark Mode visibility */
        line-height: 1.7;
        text-align: center;
        font-size: 1rem;
    }
    
    /* Feature Detail Cards - FIXED HEIGHT FOR CONSISTENCY */
    .feature-detail-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        border: 2px solid #E0F2FE;
        transition: all 0.3s;
        min-height: 480px; /* INCREASED HEIGHT TO ENSURE ALL TEXT IS VISIBLE */
        max-height: 480px;
        display: flex;
        flex-direction: column;
        overflow-y: auto; /* ALLOW SCROLLING IF NEEDED */
    }
    .feature-detail-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 20px rgba(14, 165, 233, 0.15);
        border-color: #0EA5E9;
    }
    .feature-icon-large {
        font-size: 3rem;
        margin-bottom: 0.8rem;
        text-align: center;
    }
    .feature-detail-title {
        font-size: 1.3rem;
        font-weight: bold;
        color: #0284C7 !important; /* Added !important for Dark Mode visibility */
        margin: 0.3rem 0;
        text-align: center;
    }
    .feature-detail-text {
        color: #64748b !important; /* Added !important for Dark Mode visibility */
        line-height: 1.5;
        text-align: center;
        margin-bottom: 0.8rem;
        font-size: 0.95rem;
    }
    .feature-points {
        background: #F0F9FF;
        padding: 0.8rem;
        border-radius: 10px;
        margin-top: 0.5rem;
        flex-grow: 1;
    }
    .feature-point {
        display: flex;
        align-items: flex-start;
        gap: 0.5rem;
        margin: 0.4rem 0;
        color: #475569 !important; /* Added !important for Dark Mode visibility */
        font-size: 0.9rem;
        line-height: 1.4;
    }
    .feature-point-icon {
        color: #0EA5E9;
        font-size: 1rem;
        margin-top: 2px;
        flex-shrink: 0;
    }
    
    /* CTA Section */
    .cta-section {
        background: linear-gradient(135deg, #0EA5E9 0%, #0284C7 100%);
        padding: 3rem 2rem;
        border-radius: 20px;
        text-align: center;
        color: white;
        margin: 3rem 0;
        box-shadow: 0 10px 30px rgba(14, 165, 233, 0.3);
    }
    
    /* Info Box */
    .info-box {
        background: linear-gradient(145deg, #F0F9FF 0%, #E0F2FE 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 4px solid #0EA5E9;
        margin: 1rem 0;
    }
    .info-box-title {
        font-weight: bold;
        color: #0284C7;
        font-size: 1.1rem;
        margin-bottom: 0.5rem;
    }
    .info-box-text {
        color: #64748b;
        line-height: 1.6;
    }
    </style>
""", unsafe_allow_html=True)

# Session State Initialization
if 'page' not in st.session_state:
    st.session_state.page = "home"

def home_page():
    # Header Section
    st.markdown("<h1 class='main-header'>📒 Vyapar : DigiKhata</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-header'>Smart Digital Khata Book for Modern Businesses</p>", unsafe_allow_html=True)
    
    st.write("")
    
    # Hero Section - full width with buttons inside
    st.markdown("""
        <div class='feature-box'>
            <div class='feature-title'>📊 Manage Your Business Digitally & Efficiently</div>
            <div class='feature-text'>
                Say goodbye to paper-based khata books!<br>
                Track customers, inventory, and transactions all in one place.<br>
                <b>100% Free • Unlimited Entries • Secure Data</b>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.write("")
    col_l, col_login, col_signup, col_r = st.columns([1, 1.5, 1.5, 1])
    with col_login:
        if st.button("🔐 Login to Your Account", key="hero_login_btn", use_container_width=True, type="primary"):
            st.session_state.page = "login"
            st.rerun()
    with col_signup:
        if st.button("📝 Create New Account", key="hero_signup_btn", use_container_width=True):
            st.session_state.page = "sign_up"
            st.rerun()
    
    st.write("---")
    
    # --- HOW IT WORKS SECTION ---
    st.markdown("<h2 class='section-header'>🚀 How It Works</h2>", unsafe_allow_html=True)
    st.markdown("<p class='section-subtitle'>Getting started with Vyapar DigiKhata is super simple! Follow these 4 easy steps and you'll be managing your business digitally in less than 5 minutes.</p>", unsafe_allow_html=True)
    
    # Step 1
    st.markdown("""
        <div class='step-card'>
            <div class='step-number'>1</div>
            <h3 class='step-title'>🔐 Create Your Account</h3>
            <p class='step-description'>
                Sign up with your name, email, and shop details. It takes just 30 seconds!<br>
                Choose a secure 6-digit password to protect your business data.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    st.write("")
    
    # Step 2
    st.markdown("""
        <div class='step-card'>
            <div class='step-number'>2</div>
            <h3 class='step-title'>👥 Add Your Customers & Suppliers</h3>
            <p class='step-description'>
                Add all your customers with their names, phone numbers, and addresses.<br>
                Add suppliers too! Track who you owe money to and manage all relationships in one place.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    st.write("")
    
    # Step 3
    st.markdown("""
        <div class='step-card'>
            <div class='step-number'>3</div>
            <h3 class='step-title'>📦 Setup Your Inventory</h3>
            <p class='step-description'>
                Add all your products/items with quantities and prices.<br>
                DigiKhata will automatically track stock levels and alert you when items are running low!
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    st.write("")
    
    # Step 4
    st.markdown("""
        <div class='step-card'>
            <div class='step-number'>4</div>
            <h3 class='step-title'>💰 Start Recording Transactions</h3>
            <p class='step-description'>
                Record every sale and payment instantly!<br>
                Just select customer, add amount, choose Credit (you'll get) or Debit (you gave), and done!<br>
                DigiKhata automatically calculates all balances for you.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    st.write("")
    st.write("---")
    
    # --- DETAILED FEATURES SECTION ---
    st.markdown("<h2 class='section-header'>✨ Powerful Features</h2>", unsafe_allow_html=True)
    st.markdown("<p class='section-subtitle'>Everything you need to manage your business efficiently, all in one application</p>", unsafe_allow_html=True)
    
    # Feature 1: Customer Management
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
            <div class='feature-detail-card'>
                <div class='feature-icon-large'>👥</div>
                <h3 class='feature-detail-title'>Customer Management</h3>
                <p class='feature-detail-text'>
                    Manage unlimited customers and track every detail about them
                </p>
                <div class='feature-points'>
                    <div class='feature-point'>
                        <span class='feature-point-icon'>✓</span>
                        <span>Add unlimited customers with names, phone, address</span>
                    </div>
                    <div class='feature-point'>
                        <span class='feature-point-icon'>✓</span>
                        <span>Track who owes you money (Credit balance)</span>
                    </div>
                    <div class='feature-point'>
                        <span class='feature-point-icon'>✓</span>
                        <span>View complete transaction history per customer</span>
                    </div>
                    <div class='feature-point'>
                        <span class='feature-point-icon'>✓</span>
                        <span>Search and filter customers easily</span>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    # Feature 2: Transaction Tracking
    with col2:
        st.markdown("""
            <div class='feature-detail-card'>
                <div class='feature-icon-large'>💸</div>
                <h3 class='feature-detail-title'>Transaction Recording</h3>
                <p class='feature-detail-text'>
                    Record all business transactions in seconds
                </p>
                <div class='feature-points'>
                    <div class='feature-point'>
                        <span class='feature-point-icon'>✓</span>
                        <span>Credit (You'll Get) & Debit (You Gave) tracking</span>
                    </div>
                    <div class='feature-point'>
                        <span class='feature-point-icon'>✓</span>
                        <span>Add dates, amounts, and descriptions</span>
                    </div>
                    <div class='feature-point'>
                        <span class='feature-point-icon'>✓</span>
                        <span>Automatic balance calculations</span>
                    </div>
                    <div class='feature-point'>
                        <span class='feature-point-icon'>✓</span>
                        <span>View all transactions with dates and details</span>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    st.write("")
    
    # Feature 3: Inventory Management
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
            <div class='feature-detail-card'>
                <div class='feature-icon-large'>📦</div>
                <h3 class='feature-detail-title'>Inventory Control</h3>
                <p class='feature-detail-text'>
                    Never run out of stock! Manage your inventory smartly
                </p>
                <div class='feature-points'>
                    <div class='feature-point'>
                        <span class='feature-point-icon'>✓</span>
                        <span>Add items with quantities and prices</span>
                    </div>
                    <div class='feature-point'>
                        <span class='feature-point-icon'>✓</span>
                        <span>Low stock alerts when items are running low</span>
                    </div>
                    <div class='feature-point'>
                        <span class='feature-point-icon'>✓</span>
                        <span>Update stock levels easily</span>
                    </div>
                    <div class='feature-point'>
                        <span class='feature-point-icon'>✓</span>
                        <span>See total inventory value instantly</span>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    # Feature 4: Supplier Management
    with col2:
        st.markdown("""
            <div class='feature-detail-card'>
                <div class='feature-icon-large'>🏭</div>
                <h3 class='feature-detail-title'>Supplier Tracking</h3>
                <p class='feature-detail-text'>
                    Manage suppliers and track what you owe them
                </p>
                <div class='feature-points'>
                    <div class='feature-point'>
                        <span class='feature-point-icon'>✓</span>
                        <span>Add multiple suppliers with contact details</span>
                    </div>
                    <div class='feature-point'>
                        <span class='feature-point-icon'>✓</span>
                        <span>Track amount due and amount paid</span>
                    </div>
                    <div class='feature-point'>
                        <span class='feature-point-icon'>✓</span>
                        <span>Update payments and dues easily</span>
                    </div>
                    <div class='feature-point'>
                        <span class='feature-point-icon'>✓</span>
                        <span>See outstanding balances at a glance</span>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    st.write("")
    
    # Feature 5: Business Analytics
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
            <div class='feature-detail-card'>
                <div class='feature-icon-large'>📊</div>
                <h3 class='feature-detail-title'>Business Analytics</h3>
                <p class='feature-detail-text'>
                    Beautiful charts and graphs to understand your business
                </p>
                <div class='feature-points'>
                    <div class='feature-point'>
                        <span class='feature-point-icon'>✓</span>
                        <span>Monthly transaction trends with line charts</span>
                    </div>
                    <div class='feature-point'>
                        <span class='feature-point-icon'>✓</span>
                        <span>Income vs Expense comparison</span>
                    </div>
                    <div class='feature-point'>
                        <span class='feature-point-icon'>✓</span>
                        <span>Top customers by credit amount</span>
                    </div>
                    <div class='feature-point'>
                        <span class='feature-point-icon'>✓</span>
                        <span>Visual profit/loss overview</span>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    # Feature 6: Reports & Export
    with col2:
        st.markdown("""
            <div class='feature-detail-card'>
                <div class='feature-icon-large'>📄</div>
                <h3 class='feature-detail-title'>Reports & Export</h3>
                <p class='feature-detail-text'>
                    Generate reports and export data for your records
                </p>
                <div class='feature-points'>
                    <div class='feature-point'>
                        <span class='feature-point-icon'>✓</span>
                        <span>Export customer data to CSV/Excel</span>
                    </div>
                    <div class='feature-point'>
                        <span class='feature-point-icon'>✓</span>
                        <span>Export transaction history</span>
                    </div>
                    <div class='feature-point'>
                        <span class='feature-point-icon'>✓</span>
                        <span>Print-friendly format for all reports</span>
                    </div>
                    <div class='feature-point'>
                        <span class='feature-point-icon'>✓</span>
                        <span>Share data with accountants easily</span>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    st.write("")
    st.write("---")
    
    # --- BENEFITS SECTION ---
    st.markdown("<h3 class='section-header'>🎯 Why Choose DigiKhata?</h3>", unsafe_allow_html=True)
    st.markdown("<p class='section-subtitle'>Benefits that make your business management easier than ever</p>", unsafe_allow_html=True)
    
    benefits = [
        ("✅", "No more paper mess - Everything digital and organized"),
        ("✅", "Automatic calculations - Zero math errors guaranteed"),
        ("✅", "Customer credit tracking - Know exactly who owes what"),
        ("✅", "Inventory management - Never run out of stock again"),
        ("✅", "Visual reports - Understand your business better with charts"),
        ("✅", "Secure & Private - Your data is encrypted and safe"),
        ("✅", "100% Free - No hidden charges or premium plans"),
        ("✅", "Easy to use - No technical knowledge required")
    ]
    
    col1, col2 = st.columns(2)
    
    for i, (icon, text) in enumerate(benefits):
        target_col = col1 if i % 2 == 0 else col2
        with target_col:
            st.markdown(f"""
                <div class='why-choose-card'>
                    <span style='font-size: 1.5rem; margin-right: 0.8rem; flex-shrink: 0;'>{icon}</span>
                    <span style='font-size: 1rem; color: #334155; line-height: 1.4;'>{text}</span>
                </div>
            """, unsafe_allow_html=True)
    
    st.write("")
    st.write("---")
    
    
    # Call to Action
    st.markdown("""
        <div class='cta-section'>
            <h2 style='margin-bottom: 1rem; font-size: 2.5rem;'>🚀 Ready to Go Digital?</h2>
            <p style='font-size: 1.3rem; margin-bottom: 0.5rem;'>Join thousands of businesses managing their khata digitally!</p>
            <p style='font-size: 1.1rem; opacity: 0.9;'>Start for FREE today • No credit card required • Setup in 2 minutes</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Action Buttons removed - buttons are above hero section only
    st.write("")
    
    # Footer
    st.write("")
    st.write("")
    st.markdown("""
        <div style='text-align: center; color: #94a3b8; padding: 2rem 0; border-top: 1px solid #e2e8f0; margin-top: 2rem;'>
            <p style='font-size: 1.1rem; color: #0284C7; font-weight: 600;'>© 2026 Vyapar DigiKhata</p>
            <p style='font-size: 1rem; margin: 0.5rem 0;'>Made with ❤️ by L.J. University Students</p>
            <p style='font-size: 0.9rem; margin-top: 1rem; color: #0EA5E9; font-weight: 600;'>🎓 Innovation Village - College Project</p>
            <p style='font-size: 0.88rem; color: #64748b; margin-top: 0.3rem;'>Under the guidance of <strong style='color: #0284C7;'>Prof. Parth Sinroza</strong></p>
            <p style='font-size: 0.85rem; margin-top: 1rem;'>Manage your business the smart way 📊</p>
        </div>
    """, unsafe_allow_html=True)

# --- THE ROUTER LOGIC ---

if st.session_state.page == "home":
    home_page()

elif st.session_state.page == "login":
    login_page()

elif st.session_state.page == "sign_up":
    sign_up_page()

elif st.session_state.page == "dashboard":
    show_dashboard()

# --- SCROLL POSITION FIX ---
st.markdown("""
    <script>
    window.addEventListener('beforeunload', function() {
        sessionStorage.setItem('scrollPos', window.pageYOffset || document.documentElement.scrollTop);
    });
    
    window.addEventListener('load', function() {
        var scrollPos = sessionStorage.getItem('scrollPos');
        if (scrollPos) {
            window.scrollTo(0, parseInt(scrollPos));
        }
    });
    
    const observer = new MutationObserver(function() {
        var scrollPos = sessionStorage.getItem('scrollPos');
        if (scrollPos && !window.scrollRestored) {
            window.scrollTo(0, parseInt(scrollPos));
            window.scrollRestored = true;
            setTimeout(() => { window.scrollRestored = false; }, 100);
        }
    });
    
    observer.observe(document.body, { childList: true, subtree: true });
    
    var scrollTimeout;
    window.addEventListener('scroll', function() {
        clearTimeout(scrollTimeout);
        scrollTimeout = setTimeout(function() {
            sessionStorage.setItem('scrollPos', window.pageYOffset || document.documentElement.scrollTop);
        }, 50);
    });
    </script>
""", unsafe_allow_html=True)