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
        @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@500;600;700;800&display=swap');

        /* Apply Font Family Globally */
        html, body, [class*="css"] {
            font-family: 'Montserrat', sans-serif !important;
            font-size: 20px !important;
        }

        /* Set App Background to Light Blue with Yellow Accents */
        .stApp {
            background-color: #e0f2fe !important; /* Soft light blue */
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
        
        /* Automatically adapt text color */
        label, .stTextInput label, p, span, div[data-testid="stMarkdownContainer"] p {
            color: #0f172a !important;
            font-weight: 600 !important;
            font-size: 18px !important;
        }
        
        /* Input boxes styling supporting light blue / yellow theme */
        input, textarea, div[data-baseweb="select"] > div {
            background-color: #ffffff !important;
            color: #0f172a !important;
            border: 2px solid #fde047 !important;
            font-size: 18px !important;
            font-weight: 500 !important;
            border-radius: 8px !important;
        }

        /* Professional Warm Yellow Header Banner on Light Blue */
        .brand-banner {
            background: linear-gradient(135deg, #fef08a 100%, #fde047 0%);
            padding: 18px 22px;
            border-radius: 10px;
            color: #713f12 !important;
            text-align: center;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
            margin-bottom: 15px;
            border: 2px solid #facc15;
        }
        .brand-title {
            font-size: 32px !important;
            font-weight: 800 !important;
            letter-spacing: 0.5px;
            color: #713f12 !important;
            margin: 0;
        }

        /* Compact, Full-Width Yellow Buttons tightly fitted inside columns */
        div.stButton > button {
            background-color: #fef08a !important;
            color: #713f12 !important;
            border: 2px solid #facc15 !important;
            font-weight: 700 !important;
            font-size: 18px !important;
            border-radius: 8px !important;
            padding: 0.6rem 0.8rem !important;
            width: 100% !important;
            display: block !important;
        }
        div.stButton > button:hover {
            background-color: #fde047 !important;
            color: #713f12 !important;
            border: 2px solid #eab308 !important;
        }

        /* Responsive Mobile Handling: Fix Header Buttons Wrapping */
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
            padding-top: 0.8rem;
            padding-bottom: 0rem;
            padding-left: 1.2rem;
            padding-right: 1.2rem;
            max-width: 100% !important;
        }

        .login-title {
            text-align: center;
            margin: 2px 0 4px 0;
        }

        .login-title h1 {
            font-size: 32px !important;
            font-weight: 800 !important;
            margin: 0 0 2px 0;
            color: #0369a1 !important;
        }

        .login-title p {
            font-size: 16px !important;
            margin: 0;
        }

        .login-card {
            max-width: 620px;
            margin: 0 auto;
            padding: 12px 18px 14px 18px;
            border-radius: 10px;
            background-color: #ffffff;
            border: 2px solid #fde047;
            box-shadow: 0 4px 12px -3px rgba(0,0,0,0.05);
            text-align: center;
        }

        .login-card h3 {
            margin: 0 0 5px 0;
            font-size: 22px !important;
            font-weight: 700 !important;
            color: #0369a1 !important;
        }

        div[data-testid="stForm"] {
            border: none !important;
            padding: 6px 0 0 0 !important;
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
if "product_page" not in st.session_state:
    st.session_state.product_page = 0

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


# 2. Compact landscape-friendly Customer Login Screen (Before Login)
if not st.session_state.logged_in_user:

    st.markdown("""
        <div class="login-title">
            <h1>HM MOBILES</h1>
            <p>Thiruverkadu - Premium Mobile Accessories & Service</p>
        </div>
    """, unsafe_allow_html=True)

    _, login_col, _ = st.columns([1, 2.4, 1])

    with login_col:

        st.markdown("""
            <div class="login-card">
                <h3>Customer Portal Login</h3>
            </div>
        """, unsafe_allow_html=True)

        with st.form("customer_direct_login_center"):

            name_col, phone_col = st.columns(2, gap="small")

            with name_col:
                cust_name = st.text_input("Your Name:")

            with phone_col:
                cust_phone = st.text_input(
                    "Mobile Number:",
                    max_chars=10
                )

            login_btn = st.form_submit_button(
                "Secure Login",
                use_container_width=True
            )

            if login_btn:
                if cust_name.strip() and len(cust_phone) == 10 and cust_phone.isdigit():

                    st.session_state.logged_in_user = cust_name.strip()
                    st.session_state.user_phone = cust_phone.strip()
                    st.session_state.user_role = "Customer"
                    st.session_state.selected_menu = "Headset"
                    st.session_state.product_page = 0

                    log_login_to_sheet(
                        cust_name.strip(),
                        cust_phone.strip()
                    )

                    st.success("✅ Login Successful!")
                    st.rerun()

                else:
                    st.warning(
                        "⚠️ Please provide a valid name and 10-digit mobile number."
                    )

    st.stop()


# --- AFTER LOGIN: PROPERLY ARRANGED HEADER & NAVIGATION (NO WRAPPING) ---
st.markdown("""
    <div class="brand-banner">
        <h1 class="brand-title">HM MOBILES THIRUVERKADU</h1>
    </div>
""", unsafe_allow_html=True)

# Adjusted column ratios to ensure Home, Cart, and Logout fit neatly in a single horizontal row without wrapping
top_comm, top_space, top_c1, top_c2, top_c3 = st.columns([2.2, 0.4, 1.3, 1.3, 1.3], gap="small")
with top_comm:
    st.markdown(f"👋 Welcome, **{st.session_state.logged_in_user}**!")
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


# Load Product Records from Google Sheet Data dynamically with correct index mapping
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
        {"id": "ITM001", "name": "Bluetooth Wireless Headset", "price": "1200", "stock": "50", "category": "Headset", "image": "", "description": "High quality wireless sound with long battery backup."},
        {"id": "ITM002", "name": "Over-Ear Gaming Headset", "price": "1800", "stock": "40", "category": "Headset", "image": "", "description": "Immersive sound with noise cancellation mic."},
        {"id": "ITM003", "name": "Fast Type-C Charger 33W", "price": "650", "stock": "120", "category": "Charger", "image": "", "description": "Quick charge adapter for modern smartphones."},
        {"id": "ITM004", "name": "Dual Port Fast Wall Charger", "price": "500", "stock": "90", "category": "Charger", "image": "", "description": "Charge two devices simultaneously safely."},
        {"id": "ITM005", "name": "Braided Micro USB Cable", "price": "250", "stock": "200", "category": "Cable", "image": "", "description": "Durable tangle-free charging and sync cable."},
        {"id": "ITM006", "name": "Type-C Fast Charging Cable", "price": "300", "stock": "150", "category": "Cable", "image": "", "description": "High-speed data transfer and quick charging cable."},
        {"id": "ITM007", "name": "Professional Studio Mic", "price": "2500", "stock": "30", "category": "Mic", "image": "", "description": "Clear vocal recording microphone for creators."},
        {"id": "ITM008", "name": "Mini Lavalier Clip-on Mic", "price": "450", "stock": "80", "category": "Mic", "image": "", "description": "Compact clip-on microphone for interviews and vlogs."},
        {"id": "ITM009", "name": "Lithium Mobile Replacement Battery", "price": "800", "stock": "45", "category": "Battery", "image": "", "description": "Reliable high-capacity replacement battery."},
        {"id": "ITM010", "name": "Edge-to-Edge Tempered Glass", "price": "200", "stock": "300", "category": "Tempered", "image": "", "description": "9H hardness crystal clear screen protector."},
        {"id": "ITM011", "name": "Wireless Bluetooth Ear Pods", "price": "1500", "stock": "75", "category": "Ear pod", "image": "", "description": "True wireless earbuds with charging case."},
        {"id": "ITM012", "name": "MagSafe Wireless Power Bank", "price": "2200", "stock": "60", "category": "Charger", "image": "", "description": "High-capacity magnetic portable charger for fast wireless charging."},
        {"id": "ITM013", "name": "RGB Phone Cooler Fan", "price": "950", "stock": "85", "category": "Headset", "image": "", "description": "Semiconductor mobile radiator gaming cooler with RGB lights."},
        {"id": "ITM014", "name": "Heavy Duty Phone Stand", "price": "350", "stock": "110", "category": "Headset", "image": "", "description": "Adjustable aluminum desktop phone and tablet holder stand."},
        {"id": "ITM015", "name": "Bluetooth Camera Shutter Remote", "price": "180", "stock": "150", "category": "Headset", "image": "", "description": "Wireless remote control selfie clicker for smartphones."},
    ]


def process_cart_checkout(address: str, secondary_phone: str, description: str) -> str:
    """Checkout all items currently in the cart with delivery details, and send to Google Sheet 'HM Mobiles Orders'."""
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
    col_menu, col_items = st.columns([1, 2.5], gap="small")

    # --- SECTION 1: MENU ---
    with col_menu:
        st.markdown("Menu")
        with st.container(height=2400, border=True):
            categories = list(set([p['category'] for p in product_records]))
            for cat in categories:
                if st.button(cat, key=f"menu_btn_{cat}", use_container_width=True):
                    st.session_state.selected_menu = cat
                    st.session_state.product_page = 0  # Reset to page 0 on category change
                    st.rerun()

    # --- SECTION 2: ITEMS ---
    with col_items:
        current_cat = st.session_state.get("selected_menu", "Headset")
        st.markdown(f"{current_cat}")
        with st.container(height=2400, border=True):
            filtered_items = [p for p in product_records if p['category'] == current_cat]
            
            if filtered_items:
                items_per_page = 18
                total_items = len(filtered_items)
                total_pages = max(1, (total_items + items_per_page - 1) // items_per_page)
                
                if st.session_state.product_page >= total_pages:
                    st.session_state.product_page = 0
                
                start_idx = st.session_state.product_page * items_per_page
                end_idx = min(start_idx + items_per_page, total_items)
                current_page_items = filtered_items[start_idx:end_idx]

                for idx, prod in enumerate(current_page_items):
                    global_idx = start_idx + idx
                    slide_key = f"slide_{current_cat}_{global_idx}"
                    
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
                                    st.markdown("<div style='height: 35px;'></div>", unsafe_allow_html=True)
                                    if st.button("‹", key=f"prev_{current_cat}_{global_idx}"):
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
                                                st.markdown("<div style='height: 1px;'></div>", unsafe_allow_html=True)
                                                st.image(valid_paths[current_idx], width=160)
                                        with sub_col2:
                                            _, center_sub2, _ = st.columns([1, 4, 1])
                                            with center_sub2:
                                                st.markdown("<div style='height: 1px;'></div>", unsafe_allow_html=True)
                                                next_idx = (current_idx + 1) % total_imgs
                                                st.image(valid_paths[next_idx], width=160)
                                    else:
                                        _, center_img_col, _ = st.columns([1, 4, 1])
                                        with center_img_col:
                                            st.markdown("<div style='height: 1px;'></div>", unsafe_allow_html=True)
                                            st.image(valid_paths[0], width=180)
                                        
                                with r_btn:
                                    st.markdown("<div style='height: 35px;'></div>", unsafe_allow_html=True)
                                    if st.button("›", key=f"next_{current_cat}_{global_idx}"):
                                        if st.session_state[slide_key] + 1 < total_imgs:
                                            st.session_state[slide_key] += 1
                                        else:
                                            st.session_state[slide_key] = total_imgs - 1
                                        st.rerun()
                            else:
                                st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
                                st.markdown("<p style='text-align: center; color: #64748b; font-size: 20px;'>No Image</p>", unsafe_allow_html=True)
                        else:
                            st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
                            st.markdown("<p style='text-align: center; color: #64748b; font-size: 20px;'>No Image</p>", unsafe_allow_html=True)
                            
                    with p_div1_col:
                        st.markdown("<div style='border-left: 2px solid #fde047; height: 110px; margin-top: 1px;'></div>", unsafe_allow_html=True)

                    with p_desc_col:
                        st.markdown("<div style='height: 1px;'></div>", unsafe_allow_html=True)
                        st.markdown("**Description:**")
                        st.caption(prod.get('description', ''))

                    with p_div2_col:
                        st.markdown("<div style='border-left: 2px solid #fde047; height: 110px; margin-top: 1px;'></div>", unsafe_allow_html=True)

                    with p_details_col:
                        st.markdown("<div style='height: 1px;'></div>", unsafe_allow_html=True)
                        st.markdown(f"**{prod['name']}**")
                        st.markdown(f"₹{prod['price']}")
                        
                        q_col, b_col = st.columns([1, 1], gap="small")
                        with q_col:
                            q_val = st.number_input("Qty", min_value=1.0, value=1.0, step=1.0, key=f"qty_{current_cat}_{global_idx}", label_visibility="collapsed")
                        with b_col:
                            if st.button("Add", key=f"add_btn_{current_cat}_{global_idx}", use_container_width=True):
                                full_q_str = f"{int(q_val)} Units"
                                st.session_state.cart.append({"product": prod['name'], "quantity": full_q_str})
                                st.success(f"Added!")
                                st.rerun()
                                    
                    st.markdown("<hr style='margin-top: 4px; margin-bottom: 4px; border: none; border-top: 2px solid #fde047;'>", unsafe_allow_html=True)
                
                # Pagination Controls at the bottom
                if total_pages > 1:
                    pg_prev, pg_info, pg_next = st.columns([1, 2, 1], gap="small")
                    with pg_prev:
                        if st.button("⬅ Prev", use_container_width=True):
                            if st.session_state.product_page > 0:
                                st.session_state.product_page -= 1
                                st.rerun()
                    with pg_info:
                        st.markdown(f"<p style='text-align: center; margin-top: 2px;'>Page {st.session_state.product_page + 1} of {total_pages}</p>", unsafe_allow_html=True)
                    with pg_next:
                        if st.button("Next ➡", use_container_width=True):
                            if st.session_state.product_page < total_pages - 1:
                                st.session_state.product_page += 1
                                st.rerun()
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
            
            submit_checkout = st.form_submit_button("Complete Order")
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
