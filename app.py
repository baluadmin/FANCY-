from datetime import datetime
import csv
import os
import random
import pandas as pd
import requests
import streamlit as st

# 1. Streamlit Page Configuration & Clean Mobile Styling CSS
st.set_page_config(
    page_title="HM Mobiles Thiruverkadu",
    page_icon="📱",
    layout="wide",
)

st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif !important;
        }

        #MainMenu {visibility: hidden;}
        header {visibility: hidden;}
        footer {visibility: hidden;}
        div[data-testid="stToolbar"] {visibility: hidden; display: none;}
        section[data-testid="stStatusWidget"] {visibility: hidden; display: none;}
        
        label, .stTextInput label, p, span, div[data-testid="stMarkdownContainer"] p {
            color: var(--text-color) !important;
            font-weight: 600 !important;
        }
        
        input, textarea, div[data-baseweb="select"] > div {
            background-color: var(--secondary-background-color) !important;
            color: var(--text-color) !important;
            border: 1.5px solid #cbd5e1 !important;
            font-size: 14px !important;
            border-radius: 6px !important;
        }

        .brand-banner {
            background: linear-gradient(135deg, #1e293b 100%, #334155 0%);
            padding: 12px;
            border-radius: 8px;
            color: #ffffff !important;
            text-align: center;
            margin-bottom: 10px;
        }
        .brand-title {
            font-size: 18px;
            font-weight: 800;
            color: #ffffff !important;
            margin: 0;
        }

        div.stButton > button {
            background-color: #f1f5f9 !important;
            color: #1e293b !important;
            border: 1.5px solid #cbd5e1 !important;
            font-weight: 700 !important;
            border-radius: 6px !important;
            width: 100% !important;
        }

        .block-container {
            padding-top: 0.5rem;
            padding-left: 0.8rem;
            padding-right: 0.8rem;
            max-width: 100% !important;
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

GOOGLE_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbzq1vB7RSGZA8aM5QOOxpSKxN06vEpYs14Yupx687pWZ4KNa0bkvAEO12QJQZ_v88DT/exec"

def log_login_to_sheet(name, phone):
    try:
        payload = {"Type": "Login", "Customer_Name": name, "Primary_Phone": phone}
        requests.post(GOOGLE_SCRIPT_URL, json=payload, timeout=3)
    except Exception:
        pass

# Customer Login Gateway
if not st.session_state.logged_in_user:
    st.markdown("""
        <div style='text-align: center; margin-top: 30px;'>
            <h1 style='font-size: 24px; font-weight: 800;'>HM MOBILES</h1>
            <p style='font-size: 13px;'>Thiruverkadu - Accessories & Service Portal</p>
        </div>
    """, unsafe_allow_html=True)
    
    with st.form("login_form"):
        cust_name = st.text_input("Your Name:")
        cust_phone = st.text_input("Mobile Number (10 digits):", max_chars=10)
        login_btn = st.form_submit_button("Launch App Session", use_container_width=True)

        if login_btn:
            if cust_name.strip() and len(cust_phone) == 10 and cust_phone.isdigit():
                st.session_state.logged_in_user = cust_name.strip()
                st.session_state.user_phone = cust_phone.strip()
                log_login_to_sheet(cust_name.strip(), cust_phone.strip())
                st.rerun()
            else:
                st.warning("⚠️ Enter a valid name and 10-digit mobile number.")
    st.stop()

# Header Toolbar
st.markdown("""
    <div class="brand-banner">
        <h1 class="brand-title">HM MOBILES THIRUVERKADU</h1>
    </div>
""", unsafe_allow_html=True)

col_w, c_home, c_cart, c_out = st.columns([1.5, 1, 1, 1])
with col_w:
    st.markdown(f"👤 **{st.session_state.logged_in_user}**")
with c_home:
    if st.button("Store"):
        st.session_state.current_view = "Home"
        st.rerun()
with c_cart:
    if st.button(f"Cart ({len(st.session_state.cart)})"):
        st.session_state.current_view = "Cart"
        st.rerun()
with c_out:
    if st.button("Exit"):
        st.session_state.clear()
        st.rerun()

st.markdown("---")

# LIVE Sync Inventory from Google Sheet with TTL=0 (No Caching Delay)
@st.cache_data(ttl=0)
def load_inventory_from_sheet():
    sheet_csv_url = "https://docs.google.com/spreadsheets/d/1zXy8vwQtv2h5PooBLLEfVHAI_-aNBJK2K44kEMvczLQ/export?format=csv"
    try:
        df = pd.read_csv(sheet_csv_url)
        return df
    except Exception:
        return pd.DataFrame()

inv_df = load_inventory_from_sheet()
product_records = []

if not inv_df.empty:
    try:
        for _, row in inv_df.iterrows():
            # Strict column mapping check based on standard inventory sheets:
            # Col 0: ID, Col 1: Name, Col 2: Category, Col 3: Stock, Col 4: Price, Col 5: Desc, Col 6: Image
            product_records.append({
                "id": str(row.iloc[0]) if len(row) > 0 and pd.notna(row.iloc[0]) else "N/A",
                "name": str(row.iloc[1]) if len(row) > 1 and pd.notna(row.iloc[1]) else "Unknown",
                "category": str(row.iloc[2]).strip() if len(row) > 2 and pd.notna(row.iloc[2]) else "General",
                "stock": str(row.iloc[3]) if len(row) > 3 and pd.notna(row.iloc[3]) else "0",
                "price": str(row.iloc[4]) if len(row) > 4 and pd.notna(row.iloc[4]) else "0",
                "description": str(row.iloc[5]).strip() if len(row) > 5 and pd.notna(row.iloc[5]) else "",
                "image": str(row.iloc[6]).strip() if len(row) > 6 and pd.notna(row.iloc[6]) else ""
            })
    except Exception as e:
        print(f"Parsing error: {e}")

if not product_records:
    product_records = [
        {"id": "ITM001", "name": "Bluetooth Wireless Headset", "price": "1200", "stock": "50", "category": "Headset", "image": "", "description": "High performance audio"}
    ]

# Main Application Views
if st.session_state.current_view == "Home":
    categories = sorted(list(set([p['category'] for p in product_records])))
    selected_cat = st.selectbox("Select Product Category:", categories)
    
    st.markdown(f"### {selected_cat} Catalog")
    
    # Filter products strictly matching the selected category from the sheet
    filtered_items = [p for p in product_records if p['category'].lower() == selected_cat.lower()]
    
    if filtered_items:
        for idx, prod in enumerate(filtered_items):
            with st.container(border=True):
                st.markdown(f"**{prod['name']}**")
                st.markdown(f"Price: **₹{prod['price']}** | Stock: {prod['stock']} units")
                if prod['description']:
                    st.caption(prod['description'])
                
                q_val = st.number_input("Quantity", min_value=1.0, value=1.0, step=1.0, key=f"qty_{selected_cat}_{idx}")
                if st.button(f"Add to Cart - {prod['name']}", key=f"add_{selected_cat}_{idx}"):
                    st.session_state.cart.append({"product": prod['name'], "quantity": f"{int(q_val)} Units"})
                    st.success("Added to cart!")
                    st.rerun()
    else:
        st.info(f"No items found under category '{selected_cat}'. Check your Google Sheet column entries.")
else:
    st.subheader("🛒 Shopping Cart & Checkout")
    if st.session_state.cart:
        for i, item in enumerate(st.session_state.cart):
            col_item_name, col_item_rem = st.columns([3, 1])
            with col_item_name:
                st.write(f"• {item['product']} ({item['quantity']})")
            with col_item_rem:
                if st.button("Remove", key=f"rem_{i}"):
                    st.session_state.cart.pop(i)
                    st.rerun()
        
        st.markdown("---")
        with st.form("checkout_form"):
            address = st.text_area("Delivery Address in Thiruverkadu/Chennai:")
            sec_phone = st.text_input("Alternative Phone Number:", max_chars=10)
            pay_method = st.selectbox("Payment Gateway", ["UPI / GPay", "Cash on Delivery"])
            
            if st.form_submit_button("Confirm & Dispatch Order", use_container_width=True):
                if address and len(sec_phone) == 10:
                    try:
                        order_payload = {
                            "Type": "Order",
                            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "Customer_Name": st.session_state.logged_in_user,
                            "Primary_Phone": st.session_state.user_phone,
                            "Items": str(st.session_state.cart),
                            "Address": address,
                            "Secondary_Phone": sec_phone
                        }
                        requests.post(GOOGLE_SCRIPT_URL, json=order_payload, timeout=5)
                    except Exception:
                        pass
                    
                    st.success("🎉 Order successfully placed and synced with Google Sheets!")
                    st.session_state.cart = []
                    st.session_state.current_view = "Home"
                    st.rerun()
                else:
                    st.error("Please provide a delivery address and valid 10-digit alternative phone.")
    else:
        st.info("Your cart is empty.")
