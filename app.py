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

        /* Professional Light Blue Header Banner */
        .brand-banner {
            background: linear-gradient(135deg, #e0f2fe 100%, #bae6fd 0%);
            padding: 10px 14px;
            border-radius: 8px;
            color: #0f172a !important;
            text-align: center;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
            margin-bottom: 8px;
            border: 1.5px solid #7dd3fc;
        }
        .brand-title {
            font-size: 18px;
            font-weight: 700;
            letter-spacing: 0.5px;
            color: #0f172a !important;
            margin: 0;
        }

        /* Compact, Full-Width Buttons tightly fitted inside columns */
        div.stButton > button {
            background-color: #f1f5f9 !important;
            color: #1e293b !important;
            border: 1.5px solid #cbd5e1 !important;
            font-weight: 600 !important;
            font-size: 13px !important;
            border-radius: 6px !important;
            padding: 0.3rem 0.4rem !important;
            width: 100% !important;
            display: block !important;
        }
        div.stButton > button:hover {
            background-color: #e2e8f0 !important;
            color: #0f172a !important;
            border: 1px solid #94a3b8 !important;
        }

        /* FORCE IMAGE GRID COLUMNS TO STAY HORIZONTAL ON MOBILE */
        @media (max-width: 768px) {
            /* Target the specific container holding the 3 image columns */
            div.element-container:has(img) {
                display: inline-block !important;
                width: 33.33% !important;
            }
            div[data-testid="stHorizontalBlock"]:has(img) {
                flex-direction: row !important;
                flex-wrap: nowrap !important;
            }
            div[data-testid="stHorizontalBlock"]:has(img) > div[data-testid="column"] {
                width: 33.33% !important;
                flex: 1 1 33.33% !important;
                min-width: 0px !important;
                padding: 0px 1px !important;
            }
        }

        .block-container {
            padding-top: 0.5rem;
            padding-bottom: 0rem;
            padding-left: 0.6rem;
            padding-right: 0.6rem;
            max-width: 480px !important;
            margin: auto;
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

GOOGLE_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbzq1vB7RSGZA8aM5QOOxpSKxN06vEpYs14Yupx687pWZ4KNa0bkvAEO12QJQZ_v88DT/exec"

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

# Customer Login Screen
if not st.session_state.logged_in_user:
    st.markdown("""
        <div style='text-align: center; margin-top: 30px; margin-bottom: 10px;'>
            <h1 style='font-size: 24px; font-weight: 700; margin-bottom: 2px;'>HM MOBILES</h1>
            <p style='font-size: 12px; font-weight: 400;'>Thiruverkadu - Premium Mobile Accessories</p>
        </div>
    """, unsafe_allow_html=True)
    
    _, mid_col, _ = st.columns([0.1, 1, 0.1])
    
    with mid_col:
        with st.container():
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

# Header & Navigation
st.markdown("""
    <div class="brand-banner">
        <h1 class="brand-title">HM MOBILES THIRUVERKADU</h1>
    </div>
""", unsafe_allow_html=True)

top_comm, top_c1, top_c2, top_c3 = st.columns([1.6, 0.8, 0.9, 0.7], gap="small")
with top_comm:
    st.markdown(f"<p style='font-size: 12px; margin: 0;'>Hi, <b>{st.session_state.logged_in_user}</b></p>", unsafe_allow_html=True)
with top_c1:
    if st.button("Home", use_container_width=True):
        st.session_state.current_view = "Home"
        st.rerun()
with top_c2:
    cart_count = len(st.session_state.cart)
    if st.button(f"Cart ({cart_count})", use_container_width=True):
        st.session_state.current_view = "Cart"
        st.rerun()
with top_c3:
    if st.button("Logout", use_container_width=True):
        st.session_state.clear()
        st.rerun()

st.markdown("<hr style='margin: 6px 0px;'>", unsafe_allow_html=True)

@st.cache_data(ttl=2)
def load_inventory_from_sheet():
    sheet_csv_url = "https://docs.google.com/spreadsheets/d/1zXy8vwQtv2h5PooBLLEfVHAI_-aNBJK2K44kEMvczLQ/export?format=csv"
    try:
        df = pd.read_csv(sheet_csv_url)
        if not df.empty:
            return df
    except Exception:
        pass
    
    if os.path.exists("inventory.csv"):
        try:
            return pd.read_csv("inventory.csv")
        except Exception:
            pass
            
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
        {"id": "ITM001", "name": "Bluetooth Wireless Headset", "price": "1200", "stock": "50", "category": "Headset", "image": "", "description": "High bass wireless headset with long battery life."},
        {"id": "ITM002", "name": "Over-Ear Gaming Headset", "price": "1800", "stock": "40", "category": "Headset", "image": "", "description": "Immersive sound with noise cancellation mic."},
        {"id": "ITM003", "name": "Fast Type-C Charger 33W", "price": "650", "stock": "120", "category": "Charger", "image": "", "description": "Quick charge wall adapter for smartphones."},
        {"id": "ITM004", "name": "Wireless Bluetooth Ear Pods", "price": "1500", "stock": "75", "category": "Ear pod", "image": "", "description": "True wireless stereo earbuds."}
    ]

def process_cart_checkout(address: str, secondary_phone: str, description: str) -> str:
    if not st.session_state.cart:
        return "Your cart is empty."
    
    customer_name = st.session_state.logged_in_user
    primary_phone = st.session_state.user_phone
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    txn_id = "TXN" + datetime.now().strftime("%Y%m%d%H%M%S")

    cart_summary = ", ".join([f"{item['quantity']} of {item['product']}" for item in st.session_state.cart])

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

    st.session_state.cart = []
    return f"Order placed successfully! (TXN ID: {txn_id})"

# View Switching: Home View vs Cart/Checkout View
if st.session_state.current_view == "Home":
    categories = list(set([p['category'] for p in product_records]))
    
    cat_cols = st.columns(len(categories) if len(categories) > 0 else 1, gap="small")
    for idx, cat in enumerate(categories):
        with cat_cols[idx % len(cat_cols)]:
            is_selected = st.session_state.selected_menu == cat
            btn_label = f"📌 {cat}" if is_selected else cat
            if st.button(btn_label, key=f"cat_tab_{cat}", use_container_width=True):
                st.session_state.selected_menu = cat
                st.rerun()

    st.markdown("<hr style='margin: 6px 0px;'>", unsafe_allow_html=True)

    current_cat = st.session_state.get("selected_menu", categories[0] if categories else "Headset")
    st.markdown(f"**Category: {current_cat}**")
    
    filtered_items = [p for p in product_records if p['category'] == current_cat]
    
    if filtered_items:
        for idx, prod in enumerate(filtered_items):
            with st.container(border=True):
                raw_img = prod.get("image", "")
                if raw_img:
                    img_paths = [img.strip() for img in raw_img.replace("\\", ",").split(",") if img.strip()]
                    valid_paths = [p for p in img_paths if os.path.exists(p)]
                    if valid_paths:
                        display_paths = valid_paths[:6]
                        rows_of_imgs = [display_paths[i:i+3] for i in range(0, len(display_paths), 3)]
                        
                        for row_imgs in rows_of_imgs:
                            cols = st.columns(len(row_imgs))
                            for c_i, img_path in enumerate(row_imgs):
                                with cols[c_i]:
                                    _, center_img, _ = st.columns([0.2, 3.6, 0.2])
                                    with center_img:
                                        st.image(img_path, width=45)
                    else:
                        st.caption("No Image")
                else:
                    st.caption("No Image")

                st.markdown("<hr style='margin: 4px 0px;'>", unsafe_allow_html=True)
                
                st.markdown(f"**{prod['name']}**")
                st.markdown(f"<span style='color: #0284c7; font-weight: 700;'>₹{prod['price']}</span>", unsafe_allow_html=True)
                st.caption(prod.get('description', ''))
                
                q_col, b_col = st.columns([1, 1.2], gap="small")
                with q_col:
                    q_val = st.number_input("Qty", min_value=1.0, value=1.0, step=1.0, key=f"qty_{current_cat}_{idx}", label_visibility="collapsed")
                with b_col:
                    if st.button("Add to Cart", key=f"add_{current_cat}_{idx}", use_container_width=True):
                        full_q_str = f"{int(q_val)} Units"
                        st.session_state.cart.append({"product": prod['name'], "quantity": full_q_str})
                        st.success("Added!")
                        st.rerun()
    else:
        st.info("No items found in this category.")

else:
    st.subheader("🛒 Shopping Cart")
    if st.session_state.cart:
        for c_idx, item in enumerate(st.session_state.cart):
            cc1, cc2 = st.columns([3, 1])
            with cc1:
                st.markdown(f"- **{item['product']}** ({item['quantity']})")
            with cc2:
                if st.button("Remove", key=f"rem_{c_idx}"):
                    st.session_state.cart.pop(c_idx)
                    st.rerun()
        
        st.markdown("---")
        st.subheader("📍 Delivery Details")
        with st.form("checkout_form_main_view"):
            checkout_address = st.text_area("Delivery Address:")
            secondary_phone = st.text_input("Alternative Contact Number:", max_chars=10)
            product_desc = st.text_area("Notes / Custom Request (Optional):")
            
            submit_checkout = st.form_submit_button("Complete Order", use_container_width=True)
            if submit_checkout:
                if checkout_address and secondary_phone:
                    result_msg = process_cart_checkout(checkout_address, secondary_phone, product_desc)
                    st.success(result_msg)
                    st.session_state.current_view = "Home"
                    st.rerun()
                else:
                    st.warning("⚠️ Please provide address and alternative contact number.")
    else:
        st.info("Your cart is empty. Click **Home** to browse products.")
