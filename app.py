from datetime import datetime
import csv
import os
import random
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
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');

        /* Apply Professional Font Family Globally */
        html, body, [class*="css"] {
            font-family: 'Poppins', sans-serif !important;
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
            font-weight: 500 !important;
        }
        
        /* Input boxes styling supporting both modes */
        input, textarea, div[data-baseweb="select"] > div {
            background-color: var(--secondary-background-color) !important;
            color: var(--text-color) !important;
            border: 1.5px solid #cbd5e1 !important;
            font-size: 14px !important;
            font-weight: 400 !important;
            border-radius: 6px !important;
        }

        /* Ultra-Compact Top Bar for Brand Name */
        .brand-top-bar {
            background: linear-gradient(135deg, #e0f2fe 100%, #bae6fd 0%);
            padding: 4px 10px;
            border-radius: 4px;
            color: #0f172a !important;
            text-align: center;
            border: 1px solid #7dd3fc;
            margin-bottom: 6px;
        }
        .brand-top-title {
            font-size: 13px;
            font-weight: 700;
            letter-spacing: 0.5px;
            color: #0f172a !important;
            margin: 0;
            line-height: 1.2;
        }

        /* Compact Buttons */
        div.stButton > button {
            background-color: #f1f5f9 !important;
            color: #1e293b !important;
            border: 1.5px solid #cbd5e1 !important;
            font-weight: 600 !important;
            font-size: 13px !important;
            border-radius: 6px !important;
            padding: 0.25rem 0.4rem !important;
            width: 100% !important;
            display: block !important;
        }
        div.stButton > button:hover {
            background-color: #e2e8f0 !important;
            color: #0f172a !important;
            border: 1px solid #94a3b8 !important;
        }

        .block-container {
            padding-top: 0.4rem;
            padding-bottom: 0rem;
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
        <div style='text-align: center; margin-top: 20px; margin-bottom: 10px;'>
            <h1 style='font-size: 20px; font-weight: 700; margin-bottom: 2px;'>HM MOBILES - THIRUVERKADU</h1>
            <p style='font-size: 12px; font-weight: 400;'>Premium Mobile Accessories & Service</p>
        </div>
    """, unsafe_allow_html=True)
    
    _, mid_col, _ = st.columns([1.5, 1, 1.5])
    
    with mid_col:
        with st.container():
            st.markdown("""
                <div style='padding: 15px; border-radius: 10px; border: 1.5px solid #cbd5e1; box-shadow: 0 4px 12px -3px rgba(0,0,0,0.05); text-align: center;'>
                    <h3 style='margin-top: 0; margin-bottom: 10px; font-size: 15px; font-weight: 600;'>Customer Portal Login</h3>
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
                        st.session_state.user_role = "Customer"
                        st.session_state.selected_menu = "Headset"
                        
                        log_login_to_sheet(cust_name.strip(), cust_phone.strip())

                        st.success("✅ Login Successful!")
                        st.rerun()
                    else:
                        st.warning("⚠️ Please provide a valid name and 10-digit mobile number.")
    
    st.stop()


# --- AFTER LOGIN: ULTRA-SMALL SINGLE LINE BRAND TITLE & NAVIGATION ROW ---
st.markdown("""
    <div class="brand-top-bar">
        <p class="brand-top-title">HM MOBILES - THIRUVERKADU</p>
    </div>
""", unsafe_allow_html=True)

# Single horizontal line layout for Welcome message, Home, Cart, and Logout buttons
top_c1, top_c2, top_c3, top_c4 = st.columns([1.6, 0.8, 0.9, 0.8], gap="small")
with top_c1:
    st.markdown(f"<p style='font-size: 13px; margin: 4px 0;'>👋 <b>{st.session_state.logged_in_user}</b></p>", unsafe_allow_html=True)
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


# Load Inventory Directly from Google Sheets CSV Link with Short TTL Cache
@st.cache_data(ttl=2)
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


# Load Product Records from Google Sheet Data dynamically
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
        {"id": "ITM001", "name": "Bluetooth Wireless Headset", "price": "1200", "stock": "50", "category": "Headset", "image": "", "description": "High bass wireless headset."},
        {"id": "ITM002", "name": "Over-Ear Gaming Headset", "price": "1800", "stock": "40", "category": "Headset", "image": "", "description": "RGB gaming headset."},
        {"id": "ITM003", "name": "Fast Type-C Charger 33W", "price": "650", "stock": "120", "category": "Charger", "image": "", "description": "Quick charge adapter."},
        {"id": "ITM004", "name": "Dual Port Fast Wall Charger", "price": "500", "stock": "90", "category": "Charger", "image": "", "description": "Dual USB wall charger."},
        {"id": "ITM005", "name": "Braided Micro USB Cable", "price": "250", "stock": "200", "category": "Cable", "image": "", "description": "Durable braided cable."},
        {"id": "ITM006", "name": "Type-C Fast Charging Cable", "price": "300", "stock": "150", "category": "Cable", "image": "", "description": "Fast data sync cable."},
        {"id": "ITM007", "name": "Professional Studio Mic", "price": "2500", "stock": "30", "category": "Mic", "image": "", "description": "Condenser microphone."},
        {"id": "ITM008", "name": "Mini Lavalier Clip-on Mic", "price": "450", "stock": "80", "category": "Mic", "image": "", "description": "Clip-on mic for phones."},
        {"id": "ITM009", "name": "Lithium Mobile Replacement Battery", "price": "800", "stock": "45", "category": "Battery", "image": "", "description": "High capacity cell battery."},
        {"id": "ITM010", "name": "Edge-to-Edge Tempered Glass", "price": "200", "stock": "300", "category": "Tempered", "image": "", "description": "9H hardness glass guard."},
        {"id": "ITM011", "name": "Wireless Bluetooth Ear Pods", "price": "1500", "stock": "75", "category": "Ear pod", "image": "", "description": "True wireless earbuds."},
    ]


def process_cart_checkout(address: str, secondary_phone: str, description: str) -> str:
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
            "Description": description
        }
        requests.post(GOOGLE_SCRIPT_URL, json=order_data)
    except Exception as e:
        print(f"Order sheet error: {e}")

    file_exists = os.path.isfile("orders.csv")
    with open("orders.csv", mode="a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Timestamp", "Customer Name", "Primary Phone", "Items", "Address", "Secondary Phone", "Description"])
        writer.writerow([timestamp, customer_name, primary_phone, cart_summary, address, secondary_phone, description])

    st.session_state.cart = []
    return f"Checkout complete! Order placed for: {cart_summary}. Order successful (TXN ID: {txn_id})."


# View Switching: Home View vs Cart/Checkout View
if st.session_state.current_view == "Home":
    categories = list(set([p['category'] for p in product_records]))
    
    selected_cat = st.selectbox(
        "Select Product Category:",
        categories,
        index=categories.index(st.session_state.get("selected_menu", categories[0])) if st.session_state.get("selected_menu") in categories else 0
    )
    st.session_state.selected_menu = selected_cat

    st.markdown("---")
    st.markdown(f"### {selected_cat} Collection")

    filtered_items = [p for p in product_records if p['category'] == selected_cat]

    if filtered_items:
        for idx, prod in enumerate(filtered_items):
            slide_key = f"slide_{selected_cat}_{idx}"
            if slide_key not in st.session_state:
                st.session_state[slide_key] = 0

            with st.container(border=True):
                p_img_col, p_details_col = st.columns([1, 1], gap="medium")
                
                with p_img_col:
                    raw_img = prod.get("image", "")
                    if raw_img:
                        img_paths = [img.strip() for img in raw_img.replace("\\", ",").split(",") if img.strip()]
                        valid_paths = [p for p in img_paths if os.path.exists(p)]
                        if valid_paths:
                            total_imgs = len(valid_paths)
                            current_idx = st.session_state[slide_key]
                            
                            st.image(valid_paths[current_idx], use_container_width=True)
                            
                            if total_imgs > 1:
                                l_col, r_col = st.columns(2)
                                with l_col:
                                    if st.button("◀ Prev", key=f"prev_{selected_cat}_{idx}", use_container_width=True):
                                        st.session_state[slide_key] = (current_idx - 1) % total_imgs
                                        st.rerun()
                                with r_col:
                                    if st.button("Next ▶", key=f"next_{selected_cat}_{idx}", use_container_width=True):
                                        st.session_state[slide_key] = (current_idx + 1) % total_imgs
                                        st.rerun()
                        else:
                            st.caption("No Image")
                    else:
                        st.caption("No Image")

                with p_details_col:
                    st.markdown(f"**{prod['name']}**")
                    st.markdown(f"Price: **₹{prod['price']}**")
                    st.caption(f"Description: {prod.get('description', 'N/A')}")
                    
                    q_val = st.number_input("Quantity", min_value=1.0, value=1.0, step=1.0, key=f"qty_{selected_cat}_{idx}")
                    if st.button("Add to Cart", key=f"add_btn_{selected_cat}_{idx}", use_container_width=True):
                        full_q_str = f"{int(q_val)} Units"
                        st.session_state.cart.append({"product": prod['name'], "quantity": full_q_str})
                        st.success(f"Added!")
                        st.rerun()
    else:
        st.info("No items found in this category.")

else:
    st.subheader("🛒 Your Shopping Cart & Checkout")
    if st.session_state.cart:
        for c_idx, item in enumerate(st.session_state.cart):
            cc1, cc2 = st.columns([4, 1])
            with cc1:
                st.markdown(f"- **{item['product']}** ({item['quantity']})")
            with cc2:
                if st.button("Remove", key=f"rem_cart_view_{c_idx}", use_container_width=True):
                    st.session_state.cart.pop(c_idx)
                    st.rerun()
        
        st.markdown("---")
        st.subheader("📍 Secure Checkout Form")
        with st.form("checkout_form_main_view"):
            checkout_address = st.text_area("Delivery Address:")
            secondary_phone = st.text_input("Alternative Contact Number:", max_chars=10)
            product_desc = st.text_area("Product Specifications / Custom Description:")
            
            submit_checkout = st.form_submit_button("Complete Order", use_container_width=True)
            if submit_checkout:
                if checkout_address and secondary_phone:
                    result_msg = process_cart_checkout(
                        checkout_address, secondary_phone, product_desc
                    )
                    st.success(result_msg)
                    st.session_state.current_view = "Home"
                    st.rerun()
                else:
                    st.warning("⚠️ Please provide delivery address and secondary contact number.")
    else:
        _, center_msg_col, _ = st.columns([1, 2, 1])
        with center_msg_col:
            st.info("Your cart is empty. Click **Home** above to browse and add products.")
