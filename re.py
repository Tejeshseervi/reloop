import streamlit as st
import pandas as pd
import uuid
import datetime
import random
import time

# ==========================================
# 1. CONFIGURATION & ASSETS
# ==========================================
st.set_page_config(
    page_title="Reloop Enterprise",
    page_icon="♻️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 🔥 FORCE LIGHT THEME (Fix dark screen on other laptops/browsers)
st.markdown("""
<style>
html, body, [class*="css"], .stApp {
    background-color: #F1F5F9 !important;
    color: #0F172A !important;
}
</style>
""", unsafe_allow_html=True)

# Modern Color Palette (Sophisticated Green Tech)
COLORS = {
    "primary": "#00D9A3",      # Vibrant mint
    "primary_dark": "#00B88C", # Darker mint
    "secondary": "#6366F1",    # Indigo
    "accent": "#F59E0B",       # Amber
    "success": "#10B981",      # Green
    "danger": "#EF4444",       # Red
    "dark": "#0F172A",         # Slate 900
    "dark_light": "#1E293B",   # Slate 800
    "card_bg": "#FFFFFF",
    "card_hover": "#F8FAFC",
    "bg": "#F1F5F9",           # Slate 100
    "text": "#0F172A",         # Slate 900
    "text_light": "#64748B",   # Slate 500
    "border": "#E2E8F0"        # Slate 200
}

# ==========================================
# 2. ENHANCED CUSTOM CSS
# ==========================================
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    /* Global Reset */
    * {{
        font-family: 'Inter', sans-serif;
    }}
    
    html, body, .stApp {{
        background: linear-gradient(135deg, {COLORS['bg']} 0%, #E0F2FE 100%) !important;
        color: {COLORS['text']} !important;
    }}
    
    /* Force light background for all elements */
    .main, .block-container, div, p, span, label {{
        color: {COLORS['text']} !important;
    }}
    
    /* Hide Streamlit Branding */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {{
        background: linear-gradient(180deg, {COLORS['dark']} 0%, {COLORS['dark_light']} 100%);
        border-right: 1px solid rgba(255,255,255,0.1);
    }}
    
    section[data-testid="stSidebar"] h1, 
    section[data-testid="stSidebar"] h2, 
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] p, 
    section[data-testid="stSidebar"] span, 
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] .stRadio > label {{
        color: #F1F5F9 !important;
    }}
    
    section[data-testid="stSidebar"] .stRadio > div {{
        background-color: rgba(255,255,255,0.05);
        border-radius: 12px;
        padding: 8px;
    }}
    
    section[data-testid="stSidebar"] .stRadio label[data-baseweb="radio"] {{
        background-color: rgba(255,255,255,0.05);
        border-radius: 8px;
        padding: 12px 16px;
        margin: 4px 0;
        transition: all 0.3s ease;
    }}
    
    section[data-testid="stSidebar"] .stRadio label[data-baseweb="radio"]:hover {{
        background-color: rgba(0,217,163,0.15);
        transform: translateX(4px);
    }}
    
    /* Enhanced Card Component */
    .modern-card {{
        background: {COLORS['card_bg']};
        border-radius: 16px;
        padding: 28px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05), 0 10px 25px -5px rgba(0,0,0,0.05);
        border: 1px solid {COLORS['border']};
        margin-bottom: 24px;
        transition: all 0.3s ease;
    }}
    
    .modern-card:hover {{
        box-shadow: 0 20px 40px -10px rgba(0,0,0,0.1);
        transform: translateY(-2px);
    }}
    
    /* Gradient Card */
    .gradient-card {{
        background: linear-gradient(135deg, {COLORS['primary']} 0%, {COLORS['secondary']} 100%);
        border-radius: 20px;
        padding: 32px;
        color: white;
        box-shadow: 0 20px 40px -10px rgba(0,217,163,0.3);
        margin-bottom: 24px;
    }}
    
    /* Metric Cards */
    div[data-testid="stMetric"] {{
        background: white;
        padding: 20px;
        border-radius: 14px;
        border: 1px solid {COLORS['border']};
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        transition: all 0.3s ease;
    }}
    
    div[data-testid="stMetric"]:hover {{
        box-shadow: 0 10px 25px -5px rgba(0,0,0,0.1);
        transform: translateY(-4px);
    }}
    
    div[data-testid="stMetric"] label {{
        font-size: 0.875rem !important;
        font-weight: 600 !important;
        color: {COLORS['text_light']} !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }}
    
    div[data-testid="stMetric"] [data-testid="stMetricValue"] {{
        font-size: 2rem !important;
        font-weight: 700 !important;
        color: {COLORS['text']} !important;
    }}
    
    /* Enhanced Buttons */
    .stButton > button {{
        border-radius: 12px;
        font-weight: 600;
        border: none;
        padding: 12px 28px;
        transition: all 0.3s ease;
        font-size: 0.95rem;
        letter-spacing: 0.3px;
    }}
    
    .stButton > button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 10px 20px -5px rgba(0,0,0,0.2);
    }}
    
    div.stButton > button:first-child {{
        background: linear-gradient(135deg, {COLORS['primary']} 0%, {COLORS['primary_dark']} 100%);
        color: white;
    }}
    
    div.stButton > button:hover {{
        background: linear-gradient(135deg, {COLORS['primary_dark']} 0%, {COLORS['primary']} 100%);
    }}
    
    /* Form Inputs */
    .stTextInput > div > div > input,
    .stSelectbox > div > div > select,
    .stNumberInput > div > div > input,
    .stTextArea textarea {{
        border-radius: 10px;
        border: 2px solid {COLORS['border']};
        padding: 12px 16px;
        transition: all 0.3s ease;
        background-color: white !important;
        color: {COLORS['text']} !important;
    }}
    
    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div > select:focus,
    .stNumberInput > div > div > input:focus,
    .stTextArea textarea:focus {{
        border-color: {COLORS['primary']};
        box-shadow: 0 0 0 3px rgba(0,217,163,0.1);
        background-color: white !important;
        color: {COLORS['text']} !important;
    }}
    
    /* Select box options */
    .stSelectbox > div > div > select option {{
        background-color: white !important;
        color: {COLORS['text']} !important;
    }}
    
    /* Force light theme on date picker */
    .stDateInput > div > div > input {{
        background-color: white !important;
        color: {COLORS['text']} !important;
    }}
    
    /* Date and Number inputs */
    input[type="date"],
    input[type="number"] {{
        background-color: white !important;
        color: {COLORS['text']} !important;
    }}
    
    /* Selectbox inner elements */
    .stSelectbox [data-baseweb="select"] {{
        background-color: white !important;
    }}
    
    .stSelectbox [data-baseweb="select"] > div {{
        background-color: white !important;
        color: {COLORS['text']} !important;
    }}
    
    /* Dropdown menu for selectbox */
    [role="listbox"] {{
        background-color: white !important;
    }}
    
    [role="option"] {{
        background-color: white !important;
        color: {COLORS['text']} !important;
    }}
    
    [role="option"]:hover {{
        background-color: {COLORS['bg']} !important;
    }}
    
    /* Multiselect */
    .stMultiSelect > div > div {{
        background-color: white !important;
    }}
    
    .stMultiSelect span {{
        color: {COLORS['text']} !important;
    }}
    
    /* Slider labels */
    .stSlider > div > div > div > div {{
        color: {COLORS['text']} !important;
    }}
    
    /* DataFrames */
    .stDataFrame, .stDataFrame * {{
        color: {COLORS['text']} !important;
        background-color: white !important;
    }}
    
    /* Info/Warning/Success boxes text */
    .stAlert p, .stAlert div {{
        color: {COLORS['text']} !important;
    }}
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 8px;
        background-color: transparent;
    }}
    
    .stTabs [data-baseweb="tab"] {{
        border-radius: 10px;
        padding: 12px 24px;
        background-color: white;
        border: 2px solid {COLORS['border']};
        font-weight: 600;
    }}
    
    .stTabs [aria-selected="true"] {{
        background: linear-gradient(135deg, {COLORS['primary']} 0%, {COLORS['primary_dark']} 100%);
        color: white !important;
        border-color: {COLORS['primary']};
    }}
    
    /* Headers */
    .main-header {{
        font-size: 2.75rem;
        font-weight: 800;
        background: linear-gradient(135deg, {COLORS['primary']} 0%, {COLORS['secondary']} 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
        letter-spacing: -0.5px;
    }}
    
    .sub-header {{
        font-size: 1.15rem;
        color: {COLORS['text_light']};
        margin-bottom: 2.5rem;
        font-weight: 500;
    }}
    
    /* Info/Success/Warning Boxes */
    .stAlert {{
        border-radius: 12px;
        border: none;
        padding: 16px 20px;
    }}
    
    /* File Uploader */
    .stFileUploader {{
        border: 2px dashed {COLORS['border']};
        border-radius: 12px;
        padding: 24px;
        background: white;
        transition: all 0.3s ease;
    }}
    
    .stFileUploader:hover {{
        border-color: {COLORS['primary']};
        background: {COLORS['card_hover']};
    }}
    
    /* Progress Bar */
    .stProgress > div > div > div > div {{
        background: linear-gradient(90deg, {COLORS['primary']} 0%, {COLORS['secondary']} 100%);
    }}
    
    /* Custom Utility Classes */
    .badge {{
        display: inline-block;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        letter-spacing: 0.3px;
    }}
    
    .badge-success {{
        background-color: rgba(16,185,129,0.1);
        color: {COLORS['success']};
    }}
    
    .badge-warning {{
        background-color: rgba(245,158,11,0.1);
        color: {COLORS['accent']};
    }}
    
    .badge-primary {{
        background-color: rgba(0,217,163,0.1);
        color: {COLORS['primary']};
    }}
    
    /* Stat Box */
    .stat-box {{
        background: white;
        border-radius: 14px;
        padding: 20px;
        text-align: center;
        border: 1px solid {COLORS['border']};
        transition: all 0.3s ease;
    }}
    
    .stat-box:hover {{
        box-shadow: 0 10px 25px -5px rgba(0,0,0,0.1);
        transform: translateY(-4px);
    }}
    
    .stat-value {{
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, {COLORS['primary']} 0%, {COLORS['secondary']} 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 8px 0;
    }}
    
    .stat-label {{
        font-size: 0.875rem;
        color: {COLORS['text_light']};
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }}
    
    /* Activity Item */
    .activity-item {{
        padding: 16px;
        border-bottom: 1px solid {COLORS['border']};
        display: flex;
        justify-content: space-between;
        align-items: center;
        transition: all 0.3s ease;
    }}
    
    .activity-item:hover {{
        background-color: {COLORS['card_hover']};
        padding-left: 24px;
    }}
    
    .activity-item:last-child {{
        border-bottom: none;
    }}
    
    /* Product Card */
    .product-card {{
        background: white;
        border-radius: 16px;
        padding: 24px;
        border: 1px solid {COLORS['border']};
        transition: all 0.3s ease;
        height: 100%;
    }}
    
    .product-card:hover {{
        box-shadow: 0 20px 40px -10px rgba(0,0,0,0.1);
        transform: translateY(-8px);
        border-color: {COLORS['primary']};
    }}
    
    /* Rate Card */
    .rate-card {{
        background: white;
        border-radius: 14px;
        padding: 20px;
        text-align: center;
        border: 1px solid {COLORS['border']};
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }}
    
    .rate-card::before {{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 4px;
        background: linear-gradient(90deg, {COLORS['primary']} 0%, {COLORS['secondary']} 100%);
    }}
    
    .rate-card:hover {{
        box-shadow: 0 15px 30px -5px rgba(0,0,0,0.15);
        transform: translateY(-6px);
    }}
    
    /* Slider */
    .stSlider > div > div > div {{
        background: {COLORS['primary']} !important;
    }}
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 3. BACKEND LOGIC (Mock Database Class)
# ==========================================
class ReloopSystem:
    """
    Simulates a microservice backend. 
    Handles User Auth, Inventory, Transactions, and Ledger.
    """
    def __init__(self):
        # Initialize session state for persistence
        if "db" not in st.session_state:
            st.session_state.db = {
                "users": {
                    "demo": {
                        "password": "123", 
                        "points": 2450, 
                        "co2_saved": 67.8, 
                        "role": "user", 
                        "history": [],
                        "email": "demo@reloop.com",
                        "member_since": "2024-01-15",
                        "total_recycled": 156
                    }
                },
                "rates": {
                    "Copper Wire": 1150.0, 
                    "Aluminum Cans": 160.0, 
                    "Iron/Steel": 38.0, 
                    "Brass": 360.0, 
                    "Newspaper": 14.0, 
                    "Cardboard": 10.0, 
                    "PET Bottles": 55.0, 
                    "E-Waste (Mixed)": 480.0
                },
                "market_inventory": [
                    {"id": "F01", "name": "Organic Vermicompost", "subtitle": "Premium 5kg Pack", "cost": 250, "type": "fertilizer", "icon": "🌱"},
                    {"id": "F02", "name": "Bio-Enzyme Cleaner", "subtitle": "All-Purpose 500ml", "cost": 150, "type": "liquid", "icon": "🧴"},
                    {"id": "R01", "name": "Recycled PET Fabric", "subtitle": "Eco-Friendly 1m Roll", "cost": 400, "type": "material", "icon": "🧵"},
                    {"id": "R02", "name": "Bamboo Toothbrush Set", "subtitle": "Pack of 4", "cost": 180, "type": "hygiene", "icon": "🪥"},
                    {"id": "F03", "name": "Compost Starter Kit", "subtitle": "Complete Setup", "cost": 350, "type": "fertilizer", "icon": "♻️"},
                    {"id": "R03", "name": "Reusable Shopping Bags", "subtitle": "Set of 5", "cost": 200, "type": "lifestyle", "icon": "🛍️"},
                ],
                "vouchers": [
                    {"id": "V01", "brand": "Zomato", "icon": "🍕", "color": "#E23744", "amounts": [100, 200, 500, 1000]},
                    {"id": "V02", "brand": "Swiggy", "icon": "🍔", "color": "#FC8019", "amounts": [100, 200, 500, 1000]},
                    {"id": "V03", "brand": "Amazon", "icon": "📦", "color": "#FF9900", "amounts": [250, 500, 1000, 2000]},
                    {"id": "V04", "brand": "Flipkart", "icon": "🛒", "color": "#2874F0", "amounts": [250, 500, 1000, 2000]},
                    {"id": "V05", "brand": "Myntra", "icon": "👗", "color": "#FF3F6C", "amounts": [200, 500, 1000, 1500]},
                    {"id": "V06", "brand": "Nykaa", "icon": "💄", "color": "#FC2779", "amounts": [200, 500, 1000, 1500]},
                    {"id": "V07", "brand": "BookMyShow", "icon": "🎬", "color": "#C4242B", "amounts": [150, 300, 500, 1000]},
                    {"id": "V08", "brand": "Uber", "icon": "🚗", "color": "#5E5E5E", "amounts": [100, 200, 500, 1000]},
                    {"id": "V09", "brand": "Ola", "icon": "🚕", "color": "#7ED321", "amounts": [100, 200, 500, 1000]},
                    {"id": "V10", "brand": "BigBasket", "icon": "🥬", "color": "#84C225", "amounts": [200, 500, 1000, 2000]},
                    {"id": "V11", "brand": "MakeMyTrip", "icon": "✈️", "color": "#ED1B24", "amounts": [500, 1000, 2000, 5000]},
                    {"id": "V12", "brand": "Domino's Pizza", "icon": "🍕", "color": "#0078AE", "amounts": [150, 300, 500, 1000]},
                ],
                "pickups": []
            }
    
    @property
    def data(self):
        return st.session_state.db

    def authenticate(self, username, password):
        user = self.data["users"].get(username)
        if user and user["password"] == password:
            return True, user
        return False, None

    def register(self, username, password, email):
        if username in self.data["users"]:
            return False, "Username already exists"
        self.data["users"][username] = {
            "password": password, 
            "points": 100,  # Welcome bonus
            "co2_saved": 0,
            "role": "user",
            "email": email,
            "history": [],
            "member_since": datetime.datetime.now().strftime("%Y-%m-%d"),
            "total_recycled": 0
        }
        return True, "Account created successfully! Welcome to Reloop!"

    def get_market_rates(self):
        # Simulate slight market fluctuation
        rates = self.data["rates"].copy()
        for k, v in rates.items():
            fluctuation = random.uniform(-0.02, 0.02) # +/- 2%
            rates[k] = round(v * (1 + fluctuation), 2)
        return rates

    def log_transaction(self, username, description, amount, type="debit"):
        user = self.data["users"][username]
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        
        record = {
            "id": str(uuid.uuid4())[:8],
            "time": timestamp,
            "desc": description,
            "amount": amount,
            "type": type
        }
        user["history"].insert(0, record)
        return record

    def schedule_pickup(self, username, details):
        self.data["pickups"].append({
            "id": str(uuid.uuid4())[:8],
            "user": username,
            "status": "Scheduled",
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
            **details
        })

# Initialize System
sys = ReloopSystem()

# ==========================================
# 4. UI COMPONENT FUNCTIONS
# ==========================================

def render_login():
    # Create centered layout
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Logo and Header
        st.markdown(f"""
        <div style='text-align: center; padding: 40px 0 30px 0;'>
            <div style='font-size: 4rem; margin-bottom: 10px;'>♻️</div>
            <h1 style='
                font-size: 3.5rem; 
                font-weight: 800; 
                margin: 0;
                background: linear-gradient(135deg, {COLORS['primary']} 0%, {COLORS['secondary']} 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            '>reloop</h1>
            <p style='font-size: 1.2rem; color: {COLORS['text_light']}; margin-top: 10px;'>
                Transform waste into wealth
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Login/Register Tabs
        tab1, tab2 = st.tabs(["🔐 Sign In", "✨ Create Account"])
        
        with tab1:
            st.markdown("<div style='padding: 20px 0;'>", unsafe_allow_html=True)
            with st.form("login_form", clear_on_submit=False):
                u = st.text_input("Username", placeholder="Enter your username")
                p = st.text_input("Password", type="password", placeholder="Enter your password")
                
                col_a, col_b, col_c = st.columns([1, 2, 1])
                with col_b:
                    submit = st.form_submit_button("Sign In", use_container_width=True)
                
                if submit:
                    if u and p:
                        success, user_obj = sys.authenticate(u, p)
                        if success:
                            st.session_state.user = u
                            st.session_state.user_data = user_obj
                            st.success("Welcome back! Redirecting...")
                            time.sleep(0.5)
                            st.rerun()
                        else:
                            st.error("Invalid credentials. Please try again.")
                    else:
                        st.warning("Please fill in all fields")
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Demo credentials hint
            st.info("💡 Demo credentials: **demo** / **123**")
        
        with tab2:
            st.markdown("<div style='padding: 20px 0;'>", unsafe_allow_html=True)
            with st.form("reg_form", clear_on_submit=True):
                new_u = st.text_input("Username", placeholder="Choose a username")
                email = st.text_input("Email", placeholder="your.email@example.com")
                new_p = st.text_input("Password", type="password", placeholder="Create a strong password")
                confirm_p = st.text_input("Confirm Password", type="password", placeholder="Re-enter your password")
                
                col_a, col_b, col_c = st.columns([1, 2, 1])
                with col_b:
                    submit = st.form_submit_button("Create Account", use_container_width=True)
                
                if submit:
                    if not all([new_u, email, new_p, confirm_p]):
                        st.warning("Please fill in all fields")
                    elif new_p != confirm_p:
                        st.error("Passwords don't match")
                    elif len(new_p) < 6:
                        st.warning("Password should be at least 6 characters")
                    else:
                        ok, msg = sys.register(new_u, new_p, email)
                        if ok:
                            st.success(msg)
                            st.balloons()
                        else:
                            st.error(msg)
            st.markdown("</div>", unsafe_allow_html=True)
        
        # Footer
        st.markdown(f"""
        <div style='text-align: center; padding: 40px 0 20px 0; color: {COLORS['text_light']}; font-size: 0.9rem;'>
            <p>Join thousands of users making a difference 🌍</p>
        </div>
        """, unsafe_allow_html=True)

def render_sidebar():
    with st.sidebar:
        # Logo
        st.markdown(f"""
        <div style='text-align: center; padding: 20px 0 30px 0;'>
            <div style='font-size: 2.5rem;'>♻️</div>
            <h2 style='
                color: {COLORS['primary']}; 
                margin: 10px 0 5px 0;
                font-size: 2rem;
                font-weight: 800;
            '>reloop</h2>
            <p style='color: {COLORS['text_light']}; font-size: 0.85rem; margin: 0;'>
                Circular Economy Platform
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # User Info
        u_data = st.session_state.user_data
        st.markdown(f"""
        <div style='
            background: linear-gradient(135deg, {COLORS['primary']} 0%, {COLORS['secondary']} 100%);
            padding: 20px;
            border-radius: 14px;
            margin-bottom: 25px;
            color: white;
        '>
            <div style='font-size: 0.85rem; opacity: 0.9; margin-bottom: 8px;'>Welcome back,</div>
            <div style='font-size: 1.3rem; font-weight: 700; margin-bottom: 15px;'>
                {st.session_state.user}
            </div>
            <div style='background: rgba(255,255,255,0.2); padding: 12px; border-radius: 10px;'>
                <div style='font-size: 0.8rem; opacity: 0.9; margin-bottom: 4px;'>Wallet Balance</div>
                <div style='font-size: 2rem; font-weight: 800;'>{u_data['points']}</div>
                <div style='font-size: 0.85rem; opacity: 0.9;'>points (≈ ₹{u_data['points']})</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Navigation
        menu = st.radio(
            "Navigation", 
            ["🏠 Dashboard", "🚛 Schedule Pickup", "🛒 Eco-Market", "🎁 Vouchers", "💳 Wallet & Bills"],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        # Quick Stats
        st.markdown(f"""
        <div style='padding: 15px 0;'>
            <div style='margin-bottom: 15px;'>
                <div style='font-size: 0.75rem; color: {COLORS['text_light']}; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 5px;'>
                    CO₂ Saved
                </div>
                <div style='font-size: 1.5rem; font-weight: 700; color: {COLORS['success']};'>
                    {u_data['co2_saved']} kg
                </div>
            </div>
            <div>
                <div style='font-size: 0.75rem; color: {COLORS['text_light']}; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 5px;'>
                    Total Recycled
                </div>
                <div style='font-size: 1.5rem; font-weight: 700; color: {COLORS['primary']};'>
                    {u_data.get('total_recycled', 0)} kg
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Logout Button
        if st.button("🚪 Log Out", use_container_width=True):
            for key in ['user', 'user_data']:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()
        
        # Footer
        st.markdown(f"""
        <div style='padding: 20px 0 10px 0; text-align: center; font-size: 0.75rem; color: {COLORS['text_light']};'>
            <p>Member since {u_data.get('member_since', '2024')}</p>
        </div>
        """, unsafe_allow_html=True)
        
        return menu

# ==========================================
# 5. MAIN PAGES
# ==========================================

def page_dashboard():
    st.markdown("<div class='main-header'>Dashboard</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-header'>Your environmental impact at a glance</div>", unsafe_allow_html=True)
    
    u_data = st.session_state.user_data
    
    # Top Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Wallet Balance", f"{u_data['points']} pts", "+125 pts", delta_color="normal")
    
    with col2:
        st.metric("CO₂ Saved", f"{u_data['co2_saved']} kg", "+2.3 kg", delta_color="normal")
    
    with col3:
        st.metric("Scrap Recycled", f"{u_data.get('total_recycled', 156)} kg", "+8 kg", delta_color="normal")
    
    with col4:
        st.metric("Green Rank", "Eco-Warrior", "Level 5", delta_color="normal")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Live Market Rates Section
    st.markdown("### 📈 Live Market Rates")
    st.markdown("<p style='color: #64748B; margin-bottom: 20px;'>Real-time pricing for recyclable materials</p>", unsafe_allow_html=True)
    
    rates = sys.get_market_rates()
    rate_items = list(rates.items())
    
    cols = st.columns(4)
    for i in range(min(8, len(rate_items))):
        with cols[i % 4]:
            name, price = rate_items[i]
            trend = random.choice(["↗", "↘", "→"])
            trend_color = "#10B981" if trend == "↗" else "#EF4444" if trend == "↘" else "#64748B"
            
            st.markdown(f"""
            <div class="rate-card">
                <div style="font-size: 0.85rem; font-weight: 600; color: {COLORS['text_light']}; margin-bottom: 8px;">
                    {name}
                </div>
                <div style="font-size: 2rem; font-weight: 800; color: {COLORS['primary']}; margin: 10px 0;">
                    ₹{price}
                </div>
                <div style="font-size: 0.8rem; color: {COLORS['text_light']};">
                    per kg <span style="color: {trend_color}; font-size: 1.1rem; margin-left: 5px;">{trend}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Activity and Stats Row
    col_left, col_right = st.columns([2, 1])
    
    with col_left:
        st.markdown("### 🕒 Recent Activity")
        
        if not u_data['history']:
            st.markdown("""
            <div class="modern-card" style="text-align: center; padding: 40px;">
                <div style="font-size: 3rem; margin-bottom: 15px;">📦</div>
                <h4>No Activity Yet</h4>
                <p style="color: #64748B;">Schedule your first pickup to start earning points!</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("<div class='modern-card' style='padding: 0;'>", unsafe_allow_html=True)
            for item in u_data['history'][:5]:
                icon = "💰" if item['type'] == 'credit' else "🛒"
                color = COLORS['success'] if item['type'] == 'credit' else COLORS['danger']
                sign = '+' if item['type'] == 'credit' else '-'
                
                st.markdown(f"""
                <div class="activity-item">
                    <div style="display: flex; align-items: center; gap: 15px;">
                        <div style="font-size: 1.5rem;">{icon}</div>
                        <div>
                            <div style="font-weight: 600; margin-bottom: 4px;">{item['desc']}</div>
                            <div style="font-size: 0.85rem; color: {COLORS['text_light']};">{item['time']}</div>
                        </div>
                    </div>
                    <div style="font-size: 1.25rem; font-weight: 700; color: {color};">
                        {sign}{item['amount']} pts
                    </div>
                </div>
                """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
    
    with col_right:
        st.markdown("### 🏆 Achievements")
        
        achievements = [
            {"title": "First Pickup", "desc": "Completed first recycling", "icon": "🎯", "unlocked": True},
            {"title": "Eco Warrior", "desc": "50kg recycled", "icon": "⚡", "unlocked": True},
            {"title": "Green Leader", "desc": "100kg milestone", "icon": "🌟", "unlocked": True},
            {"title": "Planet Hero", "desc": "500kg recycled", "icon": "🦸", "unlocked": False},
        ]
        
        for ach in achievements:
            opacity = "1" if ach['unlocked'] else "0.4"
            bg = "rgba(16,185,129,0.1)" if ach['unlocked'] else "rgba(100,116,139,0.05)"
            
            st.markdown(f"""
            <div style="
                background: {bg};
                padding: 15px;
                border-radius: 12px;
                margin-bottom: 12px;
                opacity: {opacity};
                border: 1px solid {'#10B981' if ach['unlocked'] else COLORS['border']};
            ">
                <div style="display: flex; align-items: center; gap: 12px;">
                    <div style="font-size: 2rem;">{ach['icon']}</div>
                    <div>
                        <div style="font-weight: 600; margin-bottom: 2px;">{ach['title']}</div>
                        <div style="font-size: 0.8rem; color: {COLORS['text_light']};">{ach['desc']}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

def page_schedule():
    st.markdown("<div class='main-header'>Schedule Pickup 🚛</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-header'>Book a convenient time for our team to collect your recyclables</div>", unsafe_allow_html=True)
    
    # Info banner at top
    st.info("📍 Free doorstep pickup • Instant payment • Real-time tracking • Eco-friendly disposal")
    
    st.markdown("<div class='modern-card'>", unsafe_allow_html=True)
    st.markdown("#### 📝 Pickup Details")
    
    with st.form("pickup_form"):
            address = st.text_area(
                "Pickup Address",
                value="",
                placeholder="Enter your full address with landmark",
                height=80
            )
            
            col1, col2 = st.columns(2)
            with col1:
                pickup_date = st.date_input(
                    "Preferred Date",
                    min_value=datetime.date.today(),
                    help="Select a date for pickup"
                )
            
            with col2:
                time_slot = st.selectbox(
                    "Time Slot",
                    ["Morning (9 AM - 12 PM)", "Afternoon (1 PM - 4 PM)", "Evening (5 PM - 8 PM)"]
                )
            
            est_weight = st.slider(
                "Estimated Total Weight (kg)",
                min_value=1,
                max_value=100,
                value=10,
                help="Approximate weight helps us send the right vehicle"
            )
            
            contact = st.text_input(
                "Contact Number",
                placeholder="+91 XXXXX XXXXX"
            )
            
            notes = st.text_area(
                "Additional Notes (Optional)",
                placeholder="Any special instructions for the pickup team...",
                height=60
            )
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            col_a, col_b, col_c = st.columns([1, 2, 1])
            with col_b:
                submitted = st.form_submit_button("🚛 Confirm Pickup", use_container_width=True)
            
            if submitted:
                if not address or not contact:
                    st.error("Please fill in all required fields")
                else:
                    details = {
                        "address": address,
                        "date": str(pickup_date),
                        "time_slot": time_slot,
                        "weight": est_weight,
                        "contact": contact,
                        "notes": notes
                    }
                    sys.schedule_pickup(st.session_state.user, details)
                    st.balloons()
                    st.success("🎉 Pickup scheduled successfully! You'll receive a confirmation SMS shortly.")
                    time.sleep(1)
                    st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)

def page_market():
    st.markdown("<div class='main-header'>Eco-Market 🛒</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-header'>Redeem your points for sustainable products</div>", unsafe_allow_html=True)
    
    # User balance banner
    u_data = st.session_state.user_data
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, {COLORS['primary']} 0%, {COLORS['secondary']} 100%);
        color: white;
        padding: 20px 30px;
        border-radius: 16px;
        margin-bottom: 30px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    ">
        <div>
            <div style="font-size: 0.9rem; opacity: 0.9; margin-bottom: 5px;">Available Balance</div>
            <div style="font-size: 2.5rem; font-weight: 800;">{u_data['points']} points</div>
        </div>
        <div style="font-size: 3rem;">💰</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Filter/Category tabs
    category_filter = st.radio(
        "Category",
        ["All Products", "Fertilizers", "Lifestyle", "Hygiene", "Materials"],
        horizontal=True,
        label_visibility="collapsed"
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Products Grid
    items = sys.data["market_inventory"]
    
    # Filter logic
    if category_filter != "All Products":
        filter_map = {
            "Fertilizers": "fertilizer",
            "Lifestyle": "lifestyle",
            "Hygiene": "hygiene",
            "Materials": "material"
        }
        items = [item for item in items if item['type'] == filter_map.get(category_filter, "")]
    
    cols = st.columns(3)
    for idx, item in enumerate(items):
        with cols[idx % 3]:
            can_afford = u_data['points'] >= item['cost']
            opacity = "1" if can_afford else "0.7"
            
            st.markdown(f"""
            <div class="product-card" style="opacity: {opacity};">
                <div style="text-align: center; font-size: 3.5rem; margin-bottom: 15px;">
                    {item['icon']}
                </div>
                <h3 style="margin: 0 0 5px 0; font-size: 1.1rem;">{item['name']}</h3>
                <p style="color: {COLORS['text_light']}; font-size: 0.9rem; margin-bottom: 15px;">
                    {item['subtitle']}
                </p>
                <div style="
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    padding-top: 15px;
                    border-top: 1px solid {COLORS['border']};
                ">
                    <span class="badge badge-primary">{item['type']}</span>
                    <div style="font-size: 1.5rem; font-weight: 800; color: {COLORS['primary']};">
                        {item['cost']} pts
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(
                f"{'🛒 Purchase' if can_afford else '🔒 Insufficient Points'}", 
                key=item['id'],
                use_container_width=True,
                disabled=not can_afford
            ):
                if can_afford:
                    u_data['points'] -= item['cost']
                    sys.log_transaction(
                        st.session_state.user, 
                        f"Purchased {item['name']}", 
                        item['cost'], 
                        "debit"
                    )
                    st.success(f"✅ {item['name']} purchased! Check your orders.")
                    st.balloons()
                    time.sleep(1)
                    st.rerun()
    
    # Empty state
    if not items:
        st.markdown("""
        <div style="text-align: center; padding: 60px 20px;">
            <div style="font-size: 4rem; margin-bottom: 20px;">🔍</div>
            <h3>No Products Found</h3>
            <p style="color: #64748B;">Try selecting a different category</p>
        </div>
        """, unsafe_allow_html=True)

def page_vouchers():
    st.markdown("<div class='main-header'>Gift Vouchers 🎁</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-header'>Redeem your points for vouchers from top Indian brands</div>", unsafe_allow_html=True)
    
    u_data = st.session_state.user_data
    
    # User balance banner
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, {COLORS['primary']} 0%, {COLORS['secondary']} 100%);
        color: white;
        padding: 20px 30px;
        border-radius: 16px;
        margin-bottom: 30px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    ">
        <div>
            <div style="font-size: 0.9rem; opacity: 0.9; margin-bottom: 5px;">Available Balance</div>
            <div style="font-size: 2.5rem; font-weight: 800;">{u_data['points']} points</div>
        </div>
        <div style="font-size: 3rem;">💰</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 🏪 Popular Brands")
    
    vouchers = sys.data["vouchers"]
    
    # Display vouchers in grid
    cols = st.columns(3)
    for idx, voucher in enumerate(vouchers):
        with cols[idx % 3]:
            st.markdown(f"""
            <div class="modern-card" style="text-align: center; border: 2px solid {voucher['color']}15;">
                <div style="
                    width: 80px;
                    height: 80px;
                    background: {voucher['color']}15;
                    border-radius: 50%;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    margin: 0 auto 15px;
                    font-size: 2.5rem;
                ">
                    {voucher['icon']}
                </div>
                <h3 style="margin: 0 0 10px 0; color: {voucher['color']};">{voucher['brand']}</h3>
                <p style="color: {COLORS['text_light']}; font-size: 0.9rem; margin-bottom: 15px;">
                    Choose amount & redeem
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # Amount selection
            selected_amount = st.selectbox(
                "Select Amount",
                voucher['amounts'],
                format_func=lambda x: f"₹{x} ({x} points)",
                key=f"amt_{voucher['id']}",
                label_visibility="collapsed"
            )
            
            can_afford = u_data['points'] >= selected_amount
            
            if st.button(
                f"{'🎁 Redeem Voucher' if can_afford else '🔒 Insufficient Points'}",
                key=f"btn_{voucher['id']}",
                use_container_width=True,
                disabled=not can_afford,
                type="primary" if can_afford else "secondary"
            ):
                if can_afford:
                    u_data['points'] -= selected_amount
                    voucher_code = f"{voucher['brand'][:3].upper()}{random.randint(1000, 9999)}{random.choice('ABCDEFGH')}{random.randint(100, 999)}"
                    sys.log_transaction(
                        st.session_state.user,
                        f"{voucher['brand']} Voucher ₹{selected_amount}",
                        selected_amount,
                        "debit"
                    )
                    
                    # Show success message with voucher code
                    st.success(f"✅ Voucher redeemed successfully!")
                    st.info(f"🎫 Voucher Code: **{voucher_code}**")
                    st.balloons()
                    time.sleep(2)
                    st.rerun()
            
            st.markdown("<br>", unsafe_allow_html=True)
    
    # Info section
    st.markdown("---")
    st.markdown("### ℹ️ How to Use Vouchers")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="modern-card" style="text-align: center;">
            <div style="font-size: 3rem; margin-bottom: 10px;">1️⃣</div>
            <h4>Select Brand</h4>
            <p style="color: {COLORS['text_light']}; font-size: 0.9rem;">
                Choose your favorite brand from the list
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="modern-card" style="text-align: center;">
            <div style="font-size: 3rem; margin-bottom: 10px;">2️⃣</div>
            <h4>Choose Amount</h4>
            <p style="color: {COLORS['text_light']}; font-size: 0.9rem;">
                Pick the voucher denomination you want
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="modern-card" style="text-align: center;">
            <div style="font-size: 3rem; margin-bottom: 10px;">3️⃣</div>
            <h4>Get Code</h4>
            <p style="color: {COLORS['text_light']}; font-size: 0.9rem;">
                Receive voucher code instantly via email & SMS
            </p>
        </div>
        """, unsafe_allow_html=True)

def page_wallet():
    st.markdown("<div class='main-header'>Wallet & Bills 💳</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-header'>Manage your earnings and pay utility bills</div>", unsafe_allow_html=True)
    
    u_data = st.session_state.user_data
    
    # Wallet Overview
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="stat-box">
            <div class="stat-label">Current Balance</div>
            <div class="stat-value">{u_data['points']}</div>
            <div style="font-size: 0.9rem; color: {COLORS['text_light']};">points (₹{u_data['points']})</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        total_earned = sum([t['amount'] for t in u_data['history'] if t['type'] == 'credit']) if u_data['history'] else 0
        st.markdown(f"""
        <div class="stat-box">
            <div class="stat-label">Total Earned</div>
            <div class="stat-value" style="background: linear-gradient(135deg, {COLORS['success']} 0%, {COLORS['primary']} 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                {total_earned}
            </div>
            <div style="font-size: 0.9rem; color: {COLORS['text_light']};">lifetime points</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        total_spent = sum([t['amount'] for t in u_data['history'] if t['type'] == 'debit']) if u_data['history'] else 0
        st.markdown(f"""
        <div class="stat-box">
            <div class="stat-label">Total Spent</div>
            <div class="stat-value" style="background: linear-gradient(135deg, {COLORS['danger']} 0%, {COLORS['accent']} 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                {total_spent}
            </div>
            <div style="font-size: 0.9rem; color: {COLORS['text_light']};">lifetime points</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Tabs for different actions
    tab1, tab2, tab3 = st.tabs(["💸 Bill Payments", "🏦 Withdraw Cash", "📜 Transaction History"])
    
    with tab1:
        st.markdown("#### Pay Utility Bills with Points")
        st.info("💡 Convenience fee: 5% | Instant processing")
        
        col_left, col_right = st.columns([2, 1])
        
        with col_left:
            st.markdown("<div class='modern-card'>", unsafe_allow_html=True)
            
            biller = st.selectbox(
                "Select Biller",
                ["💡 Electricity (NPCL)", "💧 Water Supply", "🔥 Gas Connection", "📱 Mobile Postpaid", "🌐 Broadband Internet"],
                help="Choose the utility service"
            )
            
            account_no = st.text_input("Account/Consumer Number", placeholder="Enter your account number")
            
            amt = st.number_input(
                "Bill Amount (₹)",
                min_value=100,
                max_value=10000,
                step=50,
                help="Enter the bill amount to pay"
            )
            
            if amt > 0:
                fee = int(amt * 0.05)
                total = int(amt + fee)
                
                st.markdown(f"""
                <div style="
                    background: {COLORS['bg']};
                    padding: 15px;
                    border-radius: 10px;
                    margin: 15px 0;
                ">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                        <span>Bill Amount:</span>
                        <strong>₹{amt}</strong>
                    </div>
                    <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                        <span>Convenience Fee (5%):</span>
                        <strong>₹{fee}</strong>
                    </div>
                    <div style="
                        display: flex;
                        justify-content: space-between;
                        padding-top: 10px;
                        border-top: 2px solid {COLORS['border']};
                        font-size: 1.1rem;
                    ">
                        <strong>Total Points Required:</strong>
                        <strong style="color: {COLORS['primary']};">{total} pts</strong>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button("💳 Pay Bill", use_container_width=True, type="primary"):
                    if not account_no:
                        st.error("Please enter account number")
                    elif u_data['points'] >= total:
                        u_data['points'] -= total
                        sys.log_transaction(
                            st.session_state.user,
                            f"Bill Payment: {biller}",
                            total,
                            "debit"
                        )
                        txn_id = str(uuid.uuid4())[:12].upper()
                        st.success(f"✅ Payment successful! Transaction ID: {txn_id}")
                        st.balloons()
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error(f"❌ Insufficient balance. You need {total - u_data['points']} more points.")
            
            st.markdown("</div>", unsafe_allow_html=True)
        
        with col_right:
            st.markdown(f"""
            <div class="modern-card" style="background: rgba(99,102,241,0.05); border-color: {COLORS['secondary']};">
                <h4 style="margin-top: 0; color: {COLORS['secondary']};">📌 Quick Tips</h4>
                <ul style="margin: 0; padding-left: 20px; color: {COLORS['text_light']}; font-size: 0.9rem;">
                    <li style="margin-bottom: 10px;">Payments are processed instantly</li>
                    <li style="margin-bottom: 10px;">5% fee applies to all bill payments</li>
                    <li style="margin-bottom: 10px;">Save transaction ID for records</li>
                    <li>Check your email for receipt</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
    
    with tab2:
        st.markdown("#### Withdraw Points to Bank Account")
        st.warning("⚠️ Demo Mode: No actual money transfer occurs")
        
        col_left, col_right = st.columns([2, 1])
        
        with col_left:
            st.markdown("<div class='modern-card'>", unsafe_allow_html=True)
            
            bank_name = st.text_input("Bank Name", placeholder="e.g., HDFC Bank")
            account_num = st.text_input("Account Number", placeholder="XXXX XXXX XXXX")
            ifsc = st.text_input("IFSC Code", placeholder="e.g., HDFC0001234")
            
            w_amt = st.number_input(
                "Withdrawal Amount (points)",
                min_value=500,
                max_value=u_data['points'],
                step=100,
                help="Minimum withdrawal: 500 points"
            )
            
            if w_amt >= 500:
                st.markdown(f"""
                <div style="
                    background: {COLORS['bg']};
                    padding: 15px;
                    border-radius: 10px;
                    margin: 15px 0;
                ">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                        <span>Withdrawal Amount:</span>
                        <strong>{w_amt} points</strong>
                    </div>
                    <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                        <span>Bank Transfer:</span>
                        <strong>₹{w_amt}</strong>
                    </div>
                    <div style="
                        display: flex;
                        justify-content: space-between;
                        padding-top: 10px;
                        border-top: 2px solid {COLORS['border']};
                    ">
                        <span>Processing Time:</span>
                        <strong style="color: {COLORS['primary']};">3-5 Business Days</strong>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button("🏦 Request Withdrawal", use_container_width=True, type="primary"):
                    if not all([bank_name, account_num, ifsc]):
                        st.error("Please fill in all bank details")
                    elif u_data['points'] >= w_amt:
                        u_data['points'] -= w_amt
                        sys.log_transaction(
                            st.session_state.user,
                            f"Bank Withdrawal - {bank_name}",
                            w_amt,
                            "debit"
                        )
                        ref_id = str(uuid.uuid4())[:12].upper()
                        st.success(f"✅ Withdrawal request submitted! Reference ID: {ref_id}")
                        st.info("💼 Your withdrawal will be processed within 3-5 business days")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("❌ Insufficient balance")
            
            st.markdown("</div>", unsafe_allow_html=True)
        
        with col_right:
            st.markdown(f"""
            <div class="modern-card" style="background: rgba(245,158,11,0.05); border-color: {COLORS['accent']};">
                <h4 style="margin-top: 0; color: {COLORS['accent']};">ℹ️ Information</h4>
                <ul style="margin: 0; padding-left: 20px; color: {COLORS['text_light']}; font-size: 0.9rem;">
                    <li style="margin-bottom: 10px;">Minimum withdrawal: 500 pts</li>
                    <li style="margin-bottom: 10px;">No processing fees</li>
                    <li style="margin-bottom: 10px;">1 point = ₹1</li>
                    <li>Secure bank transfer via NEFT</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
    
    with tab3:
        st.markdown("#### Transaction History")
        
        if not u_data['history']:
            st.markdown("""
            <div style="text-align: center; padding: 60px 20px;">
                <div style="font-size: 4rem; margin-bottom: 20px;">📭</div>
                <h3>No Transactions Yet</h3>
                <p style="color: #64748B;">Your transaction history will appear here</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            # Create DataFrame for better display
            history_data = []
            for txn in u_data['history']:
                history_data.append({
                    "Date": txn['time'],
                    "Description": txn['desc'],
                    "Type": "Credit" if txn['type'] == 'credit' else "Debit",
                    "Amount": f"{'+ ' if txn['type'] == 'credit' else '- '}{txn['amount']} pts",
                    "ID": txn['id']
                })
            
            df = pd.DataFrame(history_data)
            
            # Display in styled table
            st.markdown("<div class='modern-card'>", unsafe_allow_html=True)
            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Date": st.column_config.TextColumn("Date & Time", width="medium"),
                    "Description": st.column_config.TextColumn("Description", width="large"),
                    "Type": st.column_config.TextColumn("Type", width="small"),
                    "Amount": st.column_config.TextColumn("Amount", width="medium"),
                    "ID": st.column_config.TextColumn("Transaction ID", width="medium")
                }
            )
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Download option
            if st.button("📥 Download Statement (CSV)", use_container_width=False):
                csv = df.to_csv(index=False)
                st.download_button(
                    "💾 Save File",
                    csv,
                    f"reloop_statement_{datetime.datetime.now().strftime('%Y%m%d')}.csv",
                    "text/csv"
                )

# ==========================================
# 6. APP EXECUTION FLOW
# ==========================================

if "user" not in st.session_state:
    render_login()
else:
    # Authenticated View
    selected_page = render_sidebar()
    
    # Route to appropriate page
    page_map = {
        "🏠 Dashboard": page_dashboard,
        "🚛 Schedule Pickup": page_schedule,
        "🛒 Eco-Market": page_market,
        "🎁 Vouchers": page_vouchers,
        "💳 Wallet & Bills": page_wallet
    }
    
    page_func = page_map.get(selected_page)
    if page_func:
        page_func()
