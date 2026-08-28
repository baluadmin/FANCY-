from datetime import datetime
import csv
import os
import random
import chromadb
import pandas as pd
import requests
import streamlit as st

# 1. Streamlit Page Configuration & Professional High-Contrast Styling CSS
st.set_page_config(
    page_title="HM Mobiles Thiruverkadu",
    page_icon="📱",
    layout="wide",
)

st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

        /* Apply Professional Font Family Globally */
        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif !important;
        }

        /* Hide Streamlit default top header, menu, share, github, and floating badges/links */
        #MainMenu {visibility: hidden;}
        header {visibility: hidden;}
        footer {visibility: hidden;}
        div[data-testid="stToolbar"] {visibility: hidden; display: none;}
        section[data-testid="stStatusWidget"] {visibility: hidden; display: none;}
        iframe[title="streamlit_app.manage"] {display: none !important;}
        .manage-app {display: none !important;}
        div[class*="viewerBadge"] {display: none !important;}
        div[data-testid="stDecoration"] {display: none;}
        
        /* Completely hide header link icons next to section headers */
        a.stMarkdownHeaderLink {display: none !important;}
        h1 svg, h2 svg, h3 svg, h4 svg, h5 svg, h6 svg {display: none !important;}
        
        /* Automatically adapt text color based on Streamlit's active theme (Dark/Light Mode) */
        label, .stTextInput label, p, span, div[data-testid="stMarkdownContainer"] p {
            color: var(--text-color) !important;
            font-weight: 600 !important;
        }
        
        /* Input boxes styling supporting both modes */
        input, textarea, div[data-baseweb="select"] > div {
            background-color: var(--secondary-background-color) !important;
            color: var(--text-color) !important;
            border: 1.5px solid #cbd5e1 !important;
            font-size: 14px !important;
            font-weight: 500 !important;
            border-radius: 6px !important;
        }

        /* Light Blue Header Banner with White Text */
        .brand-banner {
            background: linear-gradient(135deg, #0284c7 100%, #38bdf8 0%);
            padding: 18px;
            border-radius: 10px;
            color: #ffffff !important;
            text-align: center;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            margin-bottom: 15px;
        }
        .brand-title {
            font-size: 24px;
            font-weight: 800;
            letter-spacing: 0.5px;
            color: #ffffff !important;
            margin: 0;
        }

        /* Action Buttons Styling */
        div.stButton > button {
            background-color: #e0f2fe !important;
            color: #0369a1 !important;
            border: 1px solid #bae6fd !important;
            font-weight: 700 !important;
            font-size: 14px !important;
            border-radius: 6px !important;
            padding: 0.4rem 1rem !important;
        }
        div.stButton > button:hover {
            background-color: #bae6fd !important;
            color: #0c4a6e !important;
            border: 1px solid #7dd3fc !important;
        }

        /* Responsive Mobile Handling: Keep Top Navigation Row Horizontal */
        @media (max-width: 900px) {
            /* Keep top nav buttons horizontal */
            .stMainBlockContainer div[data-testid="stHorizontalBlock"]:first-of-type {
                flex-direction: row !important;
                flex-wrap: nowrap !important;
            }
            .stMainBlockContainer div[data-testid="stHorizontalBlock"]:first-of-type > div[data-testid="column"] {
                width: auto !important;
                flex: 1 1 auto !important;
                min-width: 0px !important;
                padding: 0px 2px !important;
            }

            /* Stack body content sections vertically on mobile */
            div[data-testid="stHorizontalBlock"]:not(:first-of-type) {
                flex-direction: column !important;
                flex-wrap: wrap !important;
            }
            div[data-testid="stHorizontalBlock"]:not(:first-of-type) > div[data-testid="column"] {
                width: 100% !important;
                flex: 1 1 100% !important;
                min-width: 100% !important;
                padding: 4px 0px !important;
            }
        }

        .block-container {
            padding-top: 1rem;
            padding-bottom: 0rem;
            padding-left: 1.5rem;
            padding-right: 1.5rem;
            max-width: 100% !important;
        }
    </style>
""", unsafe_allow_html=True)

# Initialize Session States
if "logged_in_user" not in st.session_state:
    st.session_state.logged_in_user = None
if "user_phone" not in st.session_state:
    st.session_state.user_phone = None
if "user_role" not in st.session_state:
    st.session_state.user_role = None
if "cart" not in st.session_state:
    st.session_state.cart = []
if "current_view" not in st.session_state:
    st.session_state.current_view = "Home"
if "selected_menu" not in st.session_state:
    st.session_state.selected_menu = "Headset"

# Google Apps Script Web App Endpoint URL Updated
GOOGLE_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbzq1vB7RSGZA8aM5QOOxpSKxN06vEpYs14Yupx687pWZ4KNa0bkvAEO12QJQZ_v88DT/exec"


# Function to log customer login into the "LOGIN" tab
def log_login_to_sheet(name, phone):
    try:
        payload = {
            "Type": "Login",
            "Customer_Name": name,
            "Primary_Phone": phone
        }
        requests.post(GOOGLE_SCRIPT_URL, json=payload)
    except Exception as e:
        print(f"Login sheet error: {e}")


# 2. Centered Professional Compact Customer Login Screen (Before Login)
if not st.session_state.logged_in_user:
    st.markdown("""
        <div style='text-align: center; margin-top: 30px; margin-bottom: 15px;'>
            <h1 style='font-size: 30px; font-weight: 800; margin-bottom: 4px;'>HM MOBILES</h1>
            <p style='font-size: 14px; font-weight: 500;'>Thiruverkadu - Premium Mobile Accessories & Service</p>
        </div>
    """, unsafe_allow_html=True)
    
    _, mid_col, _ = st.columns([1.3, 1, 1.3])
    
    with mid_col:
        with st.container():
            st.markdown("""
                <div style='padding: 25px; border-radius: 12px; border: 1.5px solid #cbd5e1; box-shadow: 0 4px 15px -3px rgba(0,0,0,0.05); text-align: center;'>
                    <h3 style='margin-top: 0; margin-bottom: 15px; font-size: 18px; font-weight: 750;'>Customer Portal Login</h3>
            """, unsafe_allow_html=True)
            
            with st.form("customer_direct_login_center"):
                cust_name = st.text_input("Your Name:")
                cust_phone = st.text_input("Mobile Number:", max_chars=10)
                login_btn = st.form_submit_button("Secure Login", use_container_width=True)

                if login_btn:
                    if cust_name.strip() and len(cust_phone) == 10 and cust_phone.isdigit():
                        st.session_state.logged_in_user = cust_name.strip()
                        st.session_state.user_phone = cust_phone.strip()
                        st.session_state.user_role = "Customer"
                        st.session_state.selected_menu = "Headset"
                        
                        log_login_to_sheet(cust_name.strip(), cust_phone.strip())

                        st.success("✅ Login Successful!")
                        st.rerun()
                    else:
                        st.warning("⚠️ Please provide a valid name and 10-digit mobile number.")
            
            st.markdown("</div>", unsafe_allow_html=True)
    
    st.stop()


# --- AFTER LOGIN: MODERN PROFESSIONAL HEADER & NAVIGATION ---
st.markdown("""
    <div class="brand-banner">
        <h1 class="brand-title">HM MOBILES THIRUVERKADU</h1>
    </div>
""", unsafe_allow_html=True)

top_c1, top_c2, top_c3, top_c4 = st.columns([2, 1, 1, 1])
with top_c1:
    st.markdown(f"👋 Welcome, **{st.session_state.logged_in_user}**!")
with top_c2:
    if st.button("Home", use_container_width=True):
        st.session_state.current_view = "Home"
        st.rerun()
with top_c3:
    cart_count = len(st.session_state.cart)
    if st.button(f"Cart ({cart_count})", use_container_width=True):
        st.session_state.current_view = "Cart"
        st.rerun()
with top_c4:
    if st.button("Logout", use_container_width=True):
        st.session_state.clear()
        st.rerun()

st.markdown("---")


# Load Inventory Directly from Google Sheets CSV Link with Cache Bypass
@st.cache_data(ttl=5)
def load_inventory_from_sheet():
    sheet_csv_url = "https://docs.google.com/spreadsheets/d/1zXy8vwQtv2h5PooBLLEfVHAI_-aNBJK2K44kEMvczLQ/export?format=csv"
    try:
        df = pd.read_csv(sheet_csv_url)
        df.to_csv("inventory.csv", index=False)
        return df
    except Exception as e:
        if os.path.exists("inventory.csv"):
            return pd.read_csv("inventory.csv")
        return pd.DataFrame()


inv_df = load_inventory_from_sheet()


# Load Product Records from Google Sheet Data dynamically with correct index mapping
product_records = []
if not inv_df.empty:
    try:
        for _, row in inv_df.iterrows():
            product_records.append({
                "id": str(row.iloc[0]),
                "name": str(row.iloc[1]),  # Product Name is at column index 1
                "category": str(row.iloc[2]),
                "stock": str(row.iloc[3]),
                "price": str(row.iloc[4])   # Price is at column index 4
            })
    except Exception:
        product_records = []

if not product_records:
    product_records = [
        {"id": "ITM001", "name": "Bluetooth Wireless Headset", "price": "1200", "stock": "50", "category": "Headset"},
        {"id": "ITM002", "name": "Over-Ear Gaming Headset", "price": "1800", "stock": "40", "category": "Headset"},
        {"id": "ITM003", "name": "Fast Type-C Charger 33W", "price": "650", "stock": "120", "category": "Charger"},
        {"id": "ITM004", "name": "Dual Port Fast Wall Charger", "price": "500", "stock": "90", "category": "Charger"},
        {"id": "ITM005", "name": "Braided Micro USB Cable", "price": "250", "stock": "200", "category": "Cable"},
        {"id": "ITM006", "name": "Type-C Fast Charging Cable", "price": "300", "stock": "150", "category": "Cable"},
        {"id": "ITM007", "name": "Professional Studio Mic", "price": "2500", "stock": "30", "category": "Mic"},
        {"id": "ITM008", "name": "Mini Lavalier Clip-on Mic", "price": "450", "stock": "80", "category": "Mic"},
        {"id": "ITM009", "name": "Lithium Mobile Replacement Battery", "price": "800", "stock": "45", "category": "Battery"},
        {"id": "ITM010", "name": "Edge-to-Edge Tempered Glass", "price": "200", "stock": "300", "category": "Tempered"},
        {"id": "ITM011", "name": "Wireless Bluetooth Ear Pods", "price": "1500", "stock": "75", "category": "Ear pod"},
    ]


def process_cart_checkout(address: str, secondary_phone: str, description: str, payment_method: str, location_link: str) -> str:
    """Checkout all items currently in the cart with delivery and payment details, and send to Google Sheet 'HM Mobiles Orders'."""
    if not st.session_state.cart:
        return "Your cart is empty. Please add products first."
    
    customer_name = st.session_state.logged_in_user
    primary_phone = st.session_state.user_phone
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    txn_id = "TXN" + datetime.now().strftime("%Y%m%d%H%M%S")

    cart_summary = ", ".join([f"{item['quantity']} of {item['product']}" for item in st.session_state.cart])
    st.session_state.last_booked_item = cart_summary

    try:
        order_data = {
            "Type": "Order",
            "Timestamp": timestamp,
            "Customer_Name": customer_name,
            "Primary_Phone": primary_phone,
            "Items": cart_summary,
            "Address": address,
            "Secondary_Phone": secondary_phone,
            "Description": description,
            "Live_Location": location_link
        }
        requests.post(GOOGLE_SCRIPT_URL, json=order_data)
    except Exception as e:
        print(f"Order sheet error: {e}")

    file_exists = os.path.isfile("orders.csv")
    with open("orders.csv", mode="a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Timestamp", "Customer Name", "Primary Phone", "Items", "Address", "Secondary Phone", "Description", "Live Location"])
        writer.writerow([timestamp, customer_name, primary_phone, cart_summary, address, secondary_phone, description, location_link])

    st.session_state.cart = []
    return f"Checkout complete! Order placed for: {cart_summary}. Payment via {payment_method} successful (TXN ID: {txn_id})."


# View Switching: Home View vs Cart/Checkout View
if st.session_state.current_view == "Home":
    col_menu, col_items = st.columns([1, 2], gap="small")

    # --- SECTION 1: MENU ---
    with col_menu:
        st.markdown("Menu")
        with st.container(height=500, border=True):
            categories = list(set([p['category'] for p in product_records]))
            for cat in categories:
                if st.button(cat, key=f"menu_btn_{cat}", use_container_width=True):
                    st.session_state.selected_menu = cat
                    st.rerun()

    # --- SECTION 2: ITEMS ---
    with col_items:
        current_cat = st.session_state.get("selected_menu", "Headset")
        st.markdown(f"{current_cat}")
        with st.container(height=500, border=True):
            filtered_items = [p for p in product_records if p['category'] == current_cat]
            
            if filtered_items:
                for idx, prod in enumerate(filtered_items):
                    p_info_col, p_qty_col, p_btn_col = st.columns([1.5, 1, 1], gap="small")
                    
                    with p_info_col:
                        st.markdown(f"**{prod['name']}**")
                        st.caption(f"₹{prod['price']}")
                        
                    with p_qty_col:
                        q_val = st.number_input("Qty", min_value=1.0, value=1.0, step=1.0, key=f"qty_{current_cat}_{idx}", label_visibility="collapsed")
                        
                    with p_btn_col:
                        if st.button("Add", key=f"add_btn_{current_cat}_{idx}", use_container_width=True):
                            full_q_str = f"{int(q_val)} Units"
                            st.session_state.cart.append({"product": prod['name'], "quantity": full_q_str})
                            st.success(f"Added!")
                            st.rerun()
                    st.markdown("---")
            else:
                st.info("No items found.")

else:
    st.subheader("🛒 Your Shopping Cart & Checkout")
    if st.session_state.cart:
        for c_idx, item in enumerate(st.session_state.cart):
            cc1, cc2 = st.columns([4, 1])
            with cc1:
                st.markdown(f"- **{item['product']}** ({item['quantity']})")
            with cc2:
                if st.button("Remove Item", key=f"rem_cart_view_{c_idx}"):
                    st.session_state.cart.pop(c_idx)
                    st.rerun()
        
        st.markdown("---")
        st.subheader("📍 Secure Checkout Form")
        with st.form("checkout_form_main_view"):
            checkout_address = st.text_area("Delivery Address:")
            secondary_phone = st.text_input("Alternative Contact Number:", max_chars=10)
            product_desc = st.text_area("Product Specifications / Custom Description:")
            payment_method = st.selectbox("Payment Method", ["UPI / GPay", "Credit/Debit Card", "Cash on Delivery"])
            live_location = st.text_input("Live Location Link (Google Maps Share URL):")
            
            submit_checkout = st.form_submit_button("Complete Order & Pay")
            if submit_checkout:
                if checkout_address and secondary_phone:
                    result_msg = process_cart_checkout(
                        checkout_address, secondary_phone, product_desc, payment_method, live_location
                    )
                    st.success(result_msg)
                    st.session_state.current_view = "Home"
                    st.rerun()
                else:
                    st.warning("⚠️ Please provide delivery address and secondary contact number.")
    else:
        st.info("Your cart is empty. Click **Home** above to browse and add products.")
