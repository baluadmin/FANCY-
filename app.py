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
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

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
            font-weight: 500 !important;
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

        /* Professional Neutral Dark/Slate Header Banner */
        .brand-banner {
            background: linear-gradient(135deg, #1e293b 100%, #334155 0%);
            padding: 16px 20px;
            border-radius: 10px;
            color: #ffffff !important;
            text-align: center;
            box-shadow: 0 4px 12px -2px rgba(30, 41, 59, 0.15);
            margin-bottom: 16px;
        }
        .brand-title {
            font-size: 22px;
            font-weight: 800;
            letter-spacing: 0.5px;
            color: #ffffff !important;
            margin: 0;
        }

        /* Compact, Full-Width Buttons tightly fitted inside columns */
        div.stButton > button {
            background-color: #f8fafc !important;
            color: #1e293b !important;
            border: 1.5px solid #cbd5e1 !important;
            font-weight: 700 !important;
            font-size: 15px !important;
            border-radius: 6px !important;
            padding: 0.45rem 0.6rem !important;
            width: 100% !important;
            display: block !important;
            transition: all 0.2s ease;
        }
        div.stButton > button:hover {
            background-color: #e2e8f0 !important;
            color: #0f172a !important;
            border: 1.5px solid #94a3b8 !important;
        }

        /* Responsive Mobile Handling: Keep Top Navigation Row Horizontal */
        @media (max-width: 900px) {
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
            padding-bottom: 1rem;
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
            <h1 style='font-size: 28px; font-weight: 800; margin-bottom: 4px; letter-spacing: 0.5px;'>HM MOBILES</h1>
            <p style='font-size: 14px; font-weight: 500; opacity: 0.8;'>Thiruverkadu - Premium Mobile Accessories & Service</p>
        </div>
    """, unsafe_allow_html=True)
    
    _, mid_col, _ = st.columns([1.5, 1, 1.5])
    
    with mid_col:
        with st.container():
            st.markdown("""
                <div style='padding: 24px; border-radius: 12px; border: 1.5px solid #cbd5e1; box-shadow: 0 6px 16px -4px rgba(0,0,0,0.06); text-align: center; background-color: var(--secondary-background-color);'>
                    <h3 style='margin-top: 0; margin-bottom: 16px; font-size: 17px; font-weight: 800;'>Customer Portal Login</h3>
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


# --- AFTER LOGIN: COMPACT PROFESSIONAL HEADER & NAVIGATION ---
st.markdown("""
    <div class="brand-banner">
        <h1 class="brand-title">HM MOBILES THIRUVERKADU</h1>
    </div>
""", unsafe_allow_html=True)

# Perfectly aligned top navigation bar with vertical centering applied to the welcome text and buttons
top_comm, top_space, top_c1, top_c2, top_c3 = st.columns([2.6, 1.4, 1.0, 1.0, 1.0], gap="small")

with top_comm:
    st.markdown(f"""
        <div style='display: flex; align-items: center; height: 40px;'>
            <span style='font-size: 14px; font-weight: 600;'>👋 Welcome, <strong>{st.session_state.logged_in_user}</strong>!</span>
        </div>
    """, unsafe_allow_html=True)

with top_space:
    st.empty()

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

st.markdown("<div style='margin-top: 4px;'></div>", unsafe_allow_html=True)
st.markdown("<hr style='margin: 8px 0 16px 0; border: none; border-top: 1px solid #cbd5e1;'>", unsafe_allow_html=True)


# --- OFFER OF THE DAY BANNER SECTION ---
promo_image_path = "images/Headset 1 1.jpg"
img_html = ""

if os.path.exists(promo_image_path):
    img_html = f"<img src='{promo_image_path}' style='width: 55px; height: 55px; object-fit: cover; border-radius: 6px; border: 1px solid #cbd5e1;'>"
else:
    img_html = "<div style='font-size: 11px; color: #64748b;'>No Image</div>"

st.markdown(f"""
    <div style='background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%); padding: 14px 20px; border-radius: 10px; border: 1.5px solid #cbd5e1; margin-bottom: 16px; display: flex; align-items: center; justify-content: space-between; box-shadow: 0 2px 8px rgba(0,0,0,0.03);'>
        <div style='flex-grow: 1; padding-right: 16px;'>
            <h4 style='margin: 0 0 4px 0; color: #1e293b; font-size: 15px; font-weight: 800;'>🔥 OFFER OF THE DAY</h4>
            <p style='margin: 0; color: #334155; font-size: 13px; font-weight: 600;'>Get special discounts on premium accessories today! Check out our featured items below.</p>
        </div>
        <div>
            {img_html}
        </div>
    </div>
""", unsafe_allow_html=True)


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


# Load Product Records from Google Sheet Data dynamically with correct index mapping (Description is Column F -> Index 5, Image is Column G -> Index 6)
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
        {"id": "ITM001", "name": "Bluetooth Wireless Headset", "price": "1200", "stock": "50", "category": "Headset", "image": "images/Headset 1 1.jpg \\ images/Headset 1 2.jpg \\ images/Headset 1 3.jpg", "description": "ewdftgdsgdfgdfgfdg"},
        {"id": "ITM002", "name": "Over-Ear Gaming Headset", "price": "1800", "stock": "40", "category": "Headset", "image": "", "description": "ewdftgdsgdfgdfgfdg"},
        {"id": "ITM003", "name": "Fast Type-C Charger 33W", "price": "650", "stock": "120", "category": "Charger", "image": "", "description": "ewdftgdsgdfgdfgfdg"},
        {"id": "ITM004", "name": "Dual Port Fast Wall Charger", "price": "500", "stock": "90", "category": "Charger", "image": "", "description": "ewdftgdsgdfgdfgfdg"},
        {"id": "ITM005", "name": "Braided Micro USB Cable", "price": "250", "stock": "200", "category": "Cable", "image": "", "description": "ewdftgdsgdfgdfgfdg"},
        {"id": "ITM006", "name": "Type-C Fast Charging Cable", "price": "300", "stock": "150", "category": "Cable", "image": "", "description": "ewdftgdsgdfgdfgfdg"},
        {"id": "ITM007", "name": "Professional Studio Mic", "price": "2500", "stock": "30", "category": "Mic", "image": "", "description": "ewdftgdsgdfgdfgfdg"},
        {"id": "ITM008", "name": "Mini Lavalier Clip-on Mic", "price": "450", "stock": "80", "category": "Mic", "image": "", "description": "ewdftgdsgdfgdfgfdg"},
        {"id": "ITM009", "name": "Lithium Mobile Replacement Battery", "price": "800", "stock": "45", "category": "Battery", "image": "", "description": "ewdftgdsgdfgdfgfdg"},
        {"id": "ITM010", "name": "Edge-to-Edge Tempered Glass", "price": "200", "stock": "300", "category": "Tempered", "image": "", "description": "ewdftgdsgdfgdfgfdg"},
        {"id": "ITM011", "name": "Wireless Bluetooth Ear Pods", "price": "1500", "stock": "75", "category": "Ear pod", "image": "", "description": "ewdftgdsgdfgdfgfdg"},
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
    col_menu, col_items = st.columns([1, 2.6], gap="medium")

    # --- SECTION 1: MENU ---
    with col_menu:
        st.markdown("<p style='font-size: 15px; font-weight: 700; margin-bottom: 8px;'>Categories</p>", unsafe_allow_html=True)
        with st.container(height=500, border=True):
            st.markdown("<div style='height: 4px;'></div>", unsafe_allow_html=True)
            categories = list(set([p['category'] for p in product_records]))
            for cat in categories:
                if st.button(cat, key=f"menu_btn_{cat}", use_container_width=True):
                    st.session_state.selected_menu = cat
                    st.rerun()

    # --- SECTION 2: ITEMS ---
    with col_items:
        current_cat = st.session_state.get("selected_menu", "Headset")
        st.markdown(f"<p style='font-size: 15px; font-weight: 700; margin-bottom: 8px;'>{current_cat}</p>", unsafe_allow_html=True)
        with st.container(height=500, border=True):
            st.markdown("<div style='height: 4px;'></div>", unsafe_allow_html=True)
            filtered_items = [p for p in product_records if p['category'] == current_cat]
            
            if filtered_items:
                for idx, prod in enumerate(filtered_items):
                    slide_key = f"slide_{current_cat}_{idx}"
                    
                    if slide_key not in st.session_state:
                        st.session_state[slide_key] = 0

                    p_img_col, p_div1_col, p_desc_col, p_div2_col, p_details_col = st.columns([2.5, 0.05, 2.2, 0.05, 1.8], gap="small")
                    
                    with p_img_col:
                        raw_img = prod.get("image", "")
                        if raw_img:
                            img_paths = [img.strip() for img in raw_img.replace("\\", ",").split(",") if img.strip()]
                            valid_paths = [p for p in img_paths if os.path.exists(p)]
                            if valid_paths:
                                total_imgs = len(valid_paths)
                                current_idx = st.session_state[slide_key]
                                
                                l_btn, img_display, r_btn = st.columns([0.3, 3.4, 0.3])
                                
                                with l_btn:
                                    st.markdown("<div style='height: 44px;'></div>", unsafe_allow_html=True)
                                    if st.button("‹", key=f"prev_{current_cat}_{idx}"):
                                        if st.session_state[slide_key] > 0:
                                            st.session_state[slide_key] -= 1
                                        else:
                                            st.session_state[slide_key] = total_imgs - 1
                                        st.rerun()
                                        
                                with img_display:
                                    if total_imgs >= 2:
                                        sub_col1, sub_col2 = st.columns(2, gap="small")
                                        with sub_col1:
                                            _, center_sub1, _ = st.columns([1, 4, 1])
                                            with center_sub1:
                                                st.image(valid_paths[current_idx], width=90)
                                        with sub_col2:
                                            _, center_sub2, _ = st.columns([1, 4, 1])
                                            with center_sub2:
                                                next_idx = (current_idx + 1) % total_imgs
                                                st.image(valid_paths[next_idx], width=90)
                                    else:
                                        _, center_img_col, _ = st.columns([1, 4, 1])
                                        with center_img_col:
                                            st.image(valid_paths[0], width=90)
                                        
                                with r_btn:
                                    st.markdown("<div style='height: 44px;'></div>", unsafe_allow_html=True)
                                    if st.button("›", key=f"next_{current_cat}_{idx}"):
                                        if st.session_state[slide_key] + 1 < total_imgs:
                                            st.session_state[slide_key] += 1
                                        else:
                                            st.session_state[slide_key] = 0
                                        st.rerun()
                            else:
                                st.caption("No Image")
                        else:
                            st.caption("No Image")
                            
                    with p_div1_col:
                        st.markdown("<div style='border-left: 1px solid #cbd5e1; height: 130px; margin-top: 5px;'></div>", unsafe_allow_html=True)

                    with p_desc_col:
                        st.markdown("<div style='height: 6px;'></div>", unsafe_allow_html=True)
                        st.markdown("<span style='font-size: 12px; font-weight: 700; color: #64748b;'>DESCRIPTION</span>", unsafe_allow_html=True)
                        st.markdown(f"<p style='font-size: 13px; font-weight: 500; margin-top: 4px; line-height: 1.4;'>{prod.get('description', '')}</p>", unsafe_allow_html=True)

                    with p_div2_col:
                        st.markdown("<div style='border-left: 1px solid #cbd5e1; height: 130px; margin-top: 5px;'></div>", unsafe_allow_html=True)

                    with p_details_col:
                        st.markdown("<div style='height: 4px;'></div>", unsafe_allow_html=True)
                        st.markdown(f"<p style='font-size: 14px; font-weight: 700; margin-bottom: 2px;'>{prod['name']}</p>", unsafe_allow_html=True)
                        st.markdown(f"<p style='font-size: 15px; font-weight: 800; color: #0f172a; margin-bottom: 8px;'>₹{prod['price']}</p>", unsafe_allow_html=True)
                        
                        q_col, b_col = st.columns([1, 1.1], gap="small")
                        with q_col:
                            q_val = st.number_input("Qty", min_value=1.0, value=1.0, step=1.0, key=f"qty_{current_cat}_{idx}", label_visibility="collapsed")
                        with b_col:
                            if st.button("Add", key=f"add_btn_{current_cat}_{idx}", use_container_width=True):
                                full_q_str = f"{int(q_val)} Units"
                                st.session_state.cart.append({"product": prod['name'], "quantity": full_q_str})
                                st.success(f"Added!")
                                st.rerun()
                                    
                    st.markdown("<hr style='margin-top: 14px; margin-bottom: 14px; border: none; border-top: 1px solid #cbd5e1;'>", unsafe_allow_html=True)
            else:
                st.info("No items found.")

else:
    st.markdown("<h3 style='font-size: 20px; font-weight: 800; margin-bottom: 16px;'>🛒 Your Shopping Cart & Checkout</h3>", unsafe_allow_html=True)
    if st.session_state.cart:
        with st.container(border=True):
            st.markdown("<p style='font-size: 14px; font-weight: 700; margin-bottom: 10px;'>Review Cart Items</p>", unsafe_allow_html=True)
            for c_idx, item in enumerate(st.session_state.cart):
                cc1, cc2 = st.columns([5, 1])
                with cc1:
                    st.markdown(f"• **{item['product']}** — *({item['quantity']})*")
                with cc2:
                    if st.button("Remove", key=f"rem_cart_view_{c_idx}"):
                        st.session_state.cart.pop(c_idx)
                        st.rerun()
        
        st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
        st.markdown("<h3 style='font-size: 18px; font-weight: 800; margin-bottom: 12px;'>📍 Secure Checkout Form</h3>", unsafe_allow_html=True)
        
        with st.form("checkout_form_main_view"):
            checkout_address = st.text_area("Delivery Address:")
            secondary_phone = st.text_input("Alternative Contact Number:", max_chars=10)
            product_desc = st.text_area("Product Specifications / Custom Description:")
            payment_method = st.selectbox("Payment Method", ["UPI / GPay", "Credit/Debit Card", "Cash on Delivery"])
            live_location = st.text_input("Live Location Link (Google Maps Share URL):")
            
            st.markdown("<div style='height: 4px;'></div>", unsafe_allow_html=True)
            submit_checkout = st.form_submit_button("Complete Order & Pay", use_container_width=True)
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
