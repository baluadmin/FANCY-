from datetime import datetime
import csv
import os
import random
import pandas as pd
import requests
import streamlit as st

# 1. Streamlit Page Configuration & Modern Professional UI Styling
st.set_page_config(
    page_title="HM Mobiles | Thiruverkadu",
    page_icon="📱",
    layout="wide",
)

st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif !important;
        }

        #MainMenu {visibility: hidden;}
        header {visibility: hidden;}
        footer {visibility: hidden;}
        div[data-testid="stToolbar"] {visibility: hidden; display: none;}
        section[data-testid="stStatusWidget"] {visibility: hidden; display: none;}
        a.stMarkdownHeaderLink {display: none !important;}

        /* Professional Header Banner */
        .brand-banner {
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
            padding: 18px 24px;
            border-radius: 12px;
            color: #ffffff !important;
            text-align: center;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            margin-bottom: 20px;
        }
        .brand-title {
            font-size: 24px;
            font-weight: 800;
            letter-spacing: 0.5px;
            color: #ffffff !important;
            margin: 0;
        }
        .brand-subtitle {
            font-size: 13px;
            color: #94a3b8 !important;
            margin-top: 4px;
            font-weight: 500;
        }

        /* Modern Card Containers */
        .product-card {
            background: var(--secondary-background-color);
            border: 1px solid #e2e8f0;
            border-radius: 10px;
            padding: 16px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
            margin-bottom: 12px;
        }

        /* Modern Button Styling */
        div.stButton > button {
            background-color: #2563eb !important;
            color: #ffffff !important;
            border: none !important;
            font-weight: 600 !important;
            font-size: 14px !important;
            border-radius: 8px !important;
            padding: 0.5rem 1rem !important;
            width: 100% !important;
            transition: all 0.2s ease-in-out;
        }
        div.stButton > button:hover {
            background-color: #1d4ed8 !important;
            box-shadow: 0 4px 12px rgba(37, 99, 235, 0.2);
        }

        .block-container {
            padding-top: 1.5rem;
            padding-bottom: 2rem;
            max-width: 1200px !important;
        }
    </style>
""", unsafe_allow_html=True)

# Initialize Session States
if "logged_in_user" not in st.session_state:
    st.session_state.logged_in_user = None
if "user_phone" not in st.session_state:
    st.session_state.user_phone = None
if "cart" not in st.session_state:
    st.session_state.cart = []
if "current_view" not in st.session_state:
    st.session_state.current_view = "Home"
if "selected_menu" not in st.session_state:
    st.session_state.selected_menu = "Headset"

GOOGLE_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbzq1vB7RSGZA8aM5QOOxpSKxN06vEpYs14Yupx687pWZ4KNa0bkvAEO12QJQZ_v88DT/exec"

def log_login_to_sheet(name, phone):
    try:
        payload = {"Type": "Login", "Customer_Name": name, "Primary_Phone": phone}
        requests.post(GOOGLE_SCRIPT_URL, json=payload, timeout=5)
    except Exception as e:
        print(f"Login sheet error: {e}")

# 2. Polished Customer Login Screen
if not st.session_state.logged_in_user:
    st.markdown("""
        <div style='text-align: center; margin-top: 40px; margin-bottom: 20px;'>
            <h1 style='font-size: 32px; font-weight: 800; color: #1e293b; margin-bottom: 4px;'>HM MOBILES</h1>
            <p style='font-size: 15px; color: #64748b; font-weight: 500;'>Thiruverkadu - Premium Mobile Accessories & Expert Service</p>
        </div>
    """, unsafe_allow_html=True)
    
    _, mid_col, _ = st.columns([1, 1.2, 1])
    
    with mid_col:
        with st.container(border=True):
            st.markdown("<h3 style='text-align: center; margin-bottom: 16px; font-size: 18px;'>Customer Portal Sign-In</h3>", unsafe_allow_html=True)
            with st.form("customer_login_form"):
                cust_name = st.text_input("Full Name", placeholder="Enter your name")
                cust_phone = st.text_input("Mobile Number", max_chars=10, placeholder="10-digit mobile number")
                login_btn = st.form_submit_button("Access Store", use_container_width=True)

                if login_btn:
                    if cust_name.strip() and len(cust_phone) == 10 and cust_phone.isdigit():
                        st.session_state.logged_in_user = cust_name.strip()
                        st.session_state.user_phone = cust_phone.strip()
                        log_login_to_sheet(cust_name.strip(), cust_phone.strip())
                        st.toast("✅ Successfully logged in!", icon="🎉")
                        st.rerun()
                    else:
                        st.warning("⚠️ Please provide a valid name and 10-digit mobile number.")
    st.stop()

# --- HEADER & NAVIGATION ---
st.markdown("""
    <div class="brand-banner">
        <h1 class="brand-title">HM MOBILES THIRUVERKADU</h1>
        <div class="brand-subtitle">Your Trusted Neighborhood Hub for Mobile Accessories & Repairs</div>
    </div>
""", unsafe_allow_html=True)

nav_cols = [2.5, 1, 1, 1]
col_info, c1, c2, c3 = st.columns(nav_cols, gap="small")
with col_info:
    st.markdown(f"Welcome back, **{st.session_state.logged_in_user}** (`{st.session_state.user_phone}`)")
with c1:
    if st.button("🏠 Catalog", use_container_width=True):
        st.session_state.current_view = "Home"
        st.rerun()
with c2:
    cart_count = len(st.session_state.cart)
    if st.button(f"🛒 Cart ({cart_count})", use_container_width=True):
        st.session_state.current_view = "Cart"
        st.rerun()
with c3:
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.clear()
        st.rerun()

st.markdown("<hr style='margin: 15px 0; border: none; border-top: 1px solid #e2e8f0;'>", unsafe_allow_html=True)

# Load Inventory with Spinner Cache
@st.cache_data(ttl=5)
def load_inventory_from_sheet():
    sheet_csv_url = "https://docs.google.com/spreadsheets/d/1zXy8vwQtv2h5PooBLLEfVHAI_-aNBJK2K44kEMvczLQ/export?format=csv"
    try:
        df = pd.read_csv(sheet_csv_url)
        return df
    except Exception:
        if os.path.exists("inventory.csv"):
            return pd.read_csv("inventory.csv")
        return pd.DataFrame()

with st.spinner("Fetching latest inventory..."):
    inv_df = load_inventory_from_sheet()

product_records = []
if not inv_df.empty:
    try:
        for _, row in inv_df.iterrows():
            product_records.append({
                "id": str(row.iloc[0]),
                "name": str(row.iloc[1]),
                "category": str(row.iloc[2]),
                "stock": str(row.iloc[3]),
                "price": str(row.iloc[4]),
                "description": str(row.iloc[5]).strip() if len(row) > 5 and pd.notna(row.iloc[5]) else "",
                "image": str(row.iloc[6]).strip() if len(row) > 6 and pd.notna(row.iloc[6]) else ""
            })
    except Exception:
        product_records = []

if not product_records:
    product_records = [
        {"id": "ITM001", "name": "Bluetooth Wireless Headset", "price": "1200", "stock": "50", "category": "Headset", "image": "", "description": "High-definition sound with extended battery life."},
        {"id": "ITM003", "name": "Fast Type-C Charger 33W", "price": "650", "stock": "120", "category": "Charger", "image": "", "description": "Quick charge support with thermal protection."},
    ]

def process_cart_checkout(address: str, secondary_phone: str, description: str, payment_method: str, location_link: str) -> str:
    if not st.session_state.cart:
        return "Your cart is empty."
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    txn_id = "TXN" + datetime.now().strftime("%Y%m%d%H%M%S")
    cart_summary = ", ".join([f"{item['quantity']} of {item['product']}" for item in st.session_state.cart])

    try:
        order_data = {
            "Type": "Order", "Timestamp": timestamp, "Customer_Name": st.session_state.logged_in_user,
            "Primary_Phone": st.session_state.user_phone, "Items": cart_summary, "Address": address,
            "Secondary_Phone": secondary_phone, "Description": description, "Live_Location": location_link
        }
        requests.post(GOOGLE_SCRIPT_URL, json=order_data, timeout=5)
    except Exception as e:
        print(f"Order sheet error: {e}")

    st.session_state.cart = []
    return f"Order placed successfully! Reference ID: {txn_id}"

# Main App View Router
if st.session_state.current_view == "Home":
    col_menu, col_items = st.columns([1, 3], gap="medium")

    with col_menu:
        st.markdown("### Categories")
        categories = list(set([p['category'] for p in product_records]))
        for cat in categories:
            if st.button(cat, key=f"cat_btn_{cat}", use_container_width=True):
                st.session_state.selected_menu = cat
                st.rerun()

    with col_items:
        current_cat = st.session_state.get("selected_menu", categories[0] if categories else "General")
        st.markdown(f"### {current_cat} Products")
        
        filtered_items = [p for p in product_records if p['category'] == current_cat]
        if filtered_items:
            for idx, prod in enumerate(filtered_items):
                with st.container(border=True):
                    pc1, pc2 = st.columns([3, 1], gap="medium")
                    with pc1:
                        st.markdown(f"**{prod['name']}**")
                        st.caption(prod.get('description', 'No description available.'))
                        st.markdown(f"<span style='color: #2563eb; font-weight: 700; font-size: 16px;'>₹{prod['price']}</span>", unsafe_allow_html=True)
                    with pc2:
                        qty = st.number_input("Qty", min_value=1, value=1, key=f"q_{current_cat}_{idx}")
                        if st.button("Add to Cart", key=f"add_{current_cat}_{idx}", use_container_width=True):
                            st.session_state.cart.append({"product": prod['name'], "quantity": f"{qty} Units"})
                            st.toast(f"Added {qty}x {prod['name']} to cart!", icon="🛒")
                            st.rerun()
        else:
            st.info("No items available in this category.")

else:
    st.markdown("### 🛒 Shopping Cart & Secure Checkout")
    if st.session_state.cart:
        for idx, item in enumerate(st.session_state.cart):
            rc1, rc2 = st.columns([4, 1])
            with rc1:
                st.markdown(f"• **{item['product']}** — Quantity: {item['quantity']}")
            with rc2:
                if st.button("Remove", key=f"rem_{idx}", use_container_width=True):
                    st.session_state.cart.pop(idx)
                    st.rerun()

        st.markdown("---")
        with st.form("checkout_form"):
            st.markdown("#### Delivery & Payment Details")
            address = st.text_area("Delivery Address in Thiruverkadu / Chennai")
            sec_phone = st.text_input("Alternative Phone Number", max_chars=10)
            custom_notes = st.text_area("Special Instructions (Optional)")
            pay_method = st.selectbox("Payment Method", ["UPI / GPay / PhonePe", "Cash on Delivery"])
            maps_link = st.text_input("Google Maps Location Share Link (Optional)")

            if st.form_submit_button("Confirm Order", use_container_width=True):
                if address.strip() and len(sec_phone) == 10:
                    msg = process_cart_checkout(address, sec_phone, custom_notes, pay_method, maps_link)
                    st.success(msg)
                    st.session_state.current_view = "Home"
                    st.rerun()
                else:
                    st.warning("Please provide a valid delivery address and 10-digit alternative phone number.")
    else:
        st.info("Your cart is empty. Return to the Catalog to explore products.")
