from datetime import datetime
import csv
import os
import random
import pandas as pd
import requests
import streamlit as st

# 1. Streamlit Page Configuration & Responsive Mobile View Styling
st.set_page_config(
    page_title="HM Mobiles Thiruverkadu",
    page_icon="📱",
    layout="centered",
)

st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');

        html, body, [class*="css"] {
            font-family: 'Poppins', sans-serif !important;
        }

        #MainMenu {visibility: hidden;}
        header {visibility: hidden;}
        footer {visibility: hidden;}
        div[data-testid="stToolbar"] {visibility: hidden; display: none;}
        section[data-testid="stStatusWidget"] {visibility: hidden; display: none;}
        
        label, .stTextInput label, p, span, div[data-testid="stMarkdownContainer"] p {
            color: var(--text-color) !important;
            font-weight: 500 !important;
        }
        
        input, textarea, div[data-baseweb="select"] > div {
            background-color: var(--secondary-background-color) !important;
            color: var(--text-color) !important;
            border: 1.5px solid #cbd5e1 !important;
            font-size: 14px !important;
            border-radius: 6px !important;
        }

        .brand-banner {
            background: linear-gradient(135deg, #e0f2fe 100%, #bae6fd 0%);
            padding: 12px;
            border-radius: 8px;
            color: #0f172a !important;
            text-align: center;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
            margin-bottom: 10px;
            border: 1.5px solid #7dd3fc;
        }
        .brand-title {
            font-size: 18px;
            font-weight: 700;
            color: #0f172a !important;
            margin: 0;
        }

        div.stButton > button {
            background-color: #f1f5f9 !important;
            color: #1e293b !important;
            border: 1.5px solid #cbd5e1 !important;
            font-weight: 600 !important;
            font-size: 14px !important;
            border-radius: 6px !important;
            padding: 0.4rem 0.5rem !important;
            width: 100% !important;
        }
        div.stButton > button:hover {
            background-color: #e2e8f0 !important;
            color: #0f172a !important;
        }

        .block-container {
            padding-top: 0.5rem;
            padding-bottom: 1rem;
            padding-left: 0.8rem;
            padding-right: 0.8rem;
            max-width: 480px !important;
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
        requests.post(GOOGLE_SCRIPT_URL, json=payload, timeout=3)
    except Exception:
        pass

# --- CUSTOMER LOGIN SCREEN ---
if not st.session_state.logged_in_user:
    st.markdown("""
        <div style='text-align: center; margin-top: 30px; margin-bottom: 15px;'>
            <h1 style='font-size: 24px; font-weight: 700; margin-bottom: 2px;'>HM MOBILES</h1>
            <p style='font-size: 13px;'>Thiruverkadu - Mobile Accessories & Service</p>
        </div>
    """, unsafe_allow_html=True)
    
    with st.form("customer_direct_login_center"):
        cust_name = st.text_input("Your Name:")
        cust_phone = st.text_input("Mobile Number:", max_chars=10)
        login_btn = st.form_submit_button("Secure Login", use_container_width=True)

        if login_btn:
            if cust_name.strip() and len(cust_phone) == 10 and cust_phone.isdigit():
                st.session_state.logged_in_user = cust_name.strip()
                st.session_state.user_phone = cust_phone.strip()
                log_login_to_sheet(cust_name.strip(), cust_phone.strip())
                st.success("✅ Login Successful!")
                st.rerun()
            else:
                st.warning("⚠️ Enter a valid name and 10-digit mobile number.")
    st.stop()

# --- MOBILE APP HEADER & NAVIGATION ---
st.markdown("""
    <div class="brand-banner">
        <h1 class="brand-title">HM MOBILES THIRUVERKADU</h1>
    </div>
""", unsafe_allow_html=True)

top_comm, top_c1, top_c2, top_c3 = st.columns([1.5, 1, 1, 1], gap="small")
with top_comm:
    st.markdown(f"Hi, **{st.session_state.logged_in_user.split()[0]}**")
with top_c1:
    if st.button("Home", use_container_width=True):
        st.session_state.current_view = "Home"
        st.rerun()
with top_c2:
    cart_cnt = len(st.session_state.cart)
    if st.button(f"Cart({cart_cnt})", use_container_width=True):
        st.session_state.current_view = "Cart"
        st.rerun()
with top_c3:
    if st.button("Logout", use_container_width=True):
        st.session_state.clear()
        st.rerun()

st.markdown("---")

@st.cache_data(ttl=2)
def load_inventory_from_sheet():
    sheet_csv_url = "https://docs.google.com/spreadsheets/d/1zXy8vwQtv2h5PooBLLEfVHAI_-aNBJK2K44kEMvczLQ/export?format=csv"
    try:
        df = pd.read_csv(sheet_csv_url)
        df.to_csv("inventory.csv", index=False)
        return df
    except Exception:
        if os.path.exists("inventory.csv"):
            return pd.read_csv("inventory.csv")
        return pd.DataFrame()

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
        {"id": "ITM001", "name": "Bluetooth Wireless Headset", "price": "1200", "stock": "50", "category": "Headset", "image": "", "description": "Good bass quality"},
        {"id": "ITM003", "name": "Fast Type-C Charger 33W", "price": "650", "stock": "120", "category": "Charger", "image": "", "description": "Quick charging support"}
    ]

# --- HOME / SHOP VIEW ---
if st.session_state.current_view == "Home":
    categories = list(set([p['category'] for p in product_records]))
    if categories:
        selected_cat = st.selectbox("Select Category:", categories, key="category_selector_mobile")
        st.session_state.selected_menu = selected_cat

    current_cat = st.session_state.get("selected_menu", categories[0] if categories else "Headset")
    filtered_items = [p for p in product_records if p['category'] == current_cat]

    if filtered_items:
        for idx, prod in enumerate(filtered_items):
            with st.container(border=True):
                st.markdown(f"**{prod['name']}**")
                st.markdown(f"Price: **₹{prod['price']}**")
                if prod.get('description'):
                    st.caption(prod['description'])
                
                q_col, b_col = st.columns([1, 1], gap="small")
                with q_col:
                    q_val = st.number_input("Qty", min_value=1.0, value=1.0, step=1.0, key=f"q_{current_cat}_{idx}")
                with b_col:
                    st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)
                    if st.button("Add to Cart", key=f"add_{current_cat}_{idx}", use_container_width=True):
                        st.session_state.cart.append({"product": prod['name'], "quantity": f"{int(q_val)} Units"})
                        st.success("Added!")
                        st.rerun()
    else:
        st.info("No items found in this category.")

# --- CART / CHECKOUT VIEW ---
else:
    st.subheader("🛒 Your Cart")
    if st.session_state.cart:
        for c_idx, item in enumerate(st.session_state.cart):
            col_info, col_del = st.columns([3, 1])
            with col_info:
                st.markdown(f"• **{item['product']}** ({item['quantity']})")
            with col_del:
                if st.button("X", key=f"rem_{c_idx}"):
                    st.session_state.cart.pop(c_idx)
                    st.rerun()
        
        st.markdown("---")
        st.subheader("📍 Checkout Details")
        with st.form("mobile_checkout_form"):
            address = st.text_area("Delivery Address:")
            sec_phone = st.text_input("Alternative Mobile Number:", max_chars=10)
            custom_notes = st.text_area("Special Instructions (Optional):")
            
            if st.form_submit_button("Confirm Order", use_container_width=True):
                if address and len(sec_phone) == 10:
                    cart_summary = ", ".join([f"{i['quantity']} {i['product']}" for i in st.session_state.cart])
                    try:
                        requests.post(GOOGLE_SCRIPT_URL, json={
                            "Type": "Order",
                            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "Customer_Name": st.session_state.logged_in_user,
                            "Primary_Phone": st.session_state.user_phone,
                            "Items": cart_summary,
                            "Address": address,
                            "Secondary_Phone": sec_phone,
                            "Description": custom_notes
                        }, timeout=3)
                    except Exception:
                        pass
                    
                    st.session_state.cart = []
                    st.success("🎉 Order placed successfully!")
                    st.session_state.current_view = "Home"
                    st.rerun()
                else:
                    st.warning("⚠️ Please provide a valid address and 10-digit alternative number.")
    else:
        st.info("Your cart is empty.")
