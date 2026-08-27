from datetime import datetime
import csv
import os
import random
import chromadb
from google import genai
from google.genai import types
import pandas as pd
import requests
import streamlit as st

# 1. Page Configuration & Mobile Responsive Layout Injection
st.set_page_config(
    page_title="HM Mobiles Thiruverkadu",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="collapsed"
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
        iframe[title="streamlit_app.manage"] {display: none !important;}
        .manage-app {display: none !important;}
        div[class*="viewerBadge"] {display: none !important;}
        div[data-testid="stDecoration"] {display: none;}
        a.stMarkdownHeaderLink {display: none !important;}
        h1 svg, h2 svg, h3 svg, h4 svg, h5 svg, h6 svg {display: none !important;}
        
        label, .stTextInput label, p, span, div[data-testid="stMarkdownContainer"] p {
            color: var(--text-color) !important;
            font-weight: 600 !important;
        }
        
        input, textarea, div[data-baseweb="select"] > div {
            background-color: var(--secondary-background-color) !important;
            color: var(--text-color) !important;
            border: 1.5px solid #cbd5e1 !important;
            font-size: 14px !important;
            font-weight: 500 !important;
            border-radius: 6px !important;
        }

        .brand-banner {
            background: linear-gradient(135deg, #0284c7 100%, #38bdf8 0%);
            padding: 16px;
            border-radius: 10px;
            color: #ffffff !important;
            text-align: center;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            margin-bottom: 12px;
        }
        .brand-title {
            font-size: 22px;
            font-weight: 800;
            letter-spacing: 0.5px;
            color: #ffffff !important;
            margin: 0;
        }

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

        /* Keep Top Navigation Buttons Side-by-Side on Mobile */
        div[data-testid="stHorizontalBlock"]:has(button[kind="secondary"]) {
            flex-direction: row !important;
            flex-wrap: nowrap !important;
        }

        @media (max-width: 900px) {
            div:not(:has(button[kind="secondary"])) > div[data-testid="stHorizontalBlock"] {
                flex-direction: column !important;
                flex-wrap: wrap !important;
            }
            div:not(:has(button[kind="secondary"])) > div[data-testid="stHorizontalBlock"] > div[data-testid="column"] {
                width: 100% !important;
                flex: 1 1 100% !important;
                min-width: 100% !important;
                padding: 4px 0px !important;
            }
        }

        .block-container {
            padding-top: 1rem;
            padding-bottom: 0rem;
            padding-left: 1rem;
            padding-right: 1rem;
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

GOOGLE_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbzq1vB7RSGZA8aM5QOOxpSKxN06vEpYs14Yupx687pWZ4KNa0bkvAEO12QJQZ_v88DT/exec"

def log_login_to_sheet(name, phone):
    try:
        payload = {"Type": "Login", "Customer_Name": name, "Primary_Phone": phone}
        requests.post(GOOGLE_SCRIPT_URL, json=payload)
    except Exception as e:
        print(f"Login sheet error: {e}")

if not st.session_state.logged_in_user:
    st.markdown("""
        <div style='text-align: center; margin-top: 30px; margin-bottom: 15px;'>
            <h1 style='font-size: 28px; font-weight: 800; margin-bottom: 4px;'>HM MOBILES</h1>
            <p style='font-size: 13px; font-weight: 500;'>Thiruverkadu - Mobile Portal</p>
        </div>
    """, unsafe_allow_html=True)
    
    _, mid_col, _ = st.columns([0.2, 1, 0.2])
    with mid_col:
        with st.container():
            st.markdown("""
                <div style='padding: 20px; border-radius: 12px; border: 1.5px solid #cbd5e1; text-align: center;'>
                    <h3 style='margin-top: 0; margin-bottom: 15px; font-size: 18px;'>Customer Login</h3>
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
                        st.warning("⚠️ Enter a valid name and 10-digit number.")
            st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

st.markdown("""
    <div class="brand-banner">
        <h1 class="brand-title">HM MOBILES THIRUVERKADU</h1>
    </div>
""", unsafe_allow_html=True)

top_c1, top_c2, top_c3, top_c4 = st.columns([2, 1, 1, 1])
with top_c1:
    st.markdown(f"👋 **{st.session_state.logged_in_user}**")
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

db_path = "./chroma_db"
try:
    api_key_input = st.secrets["GOOGLE_API_KEY"]
    client = genai.Client(api_key=api_key_input)
    chroma_client = chromadb.PersistentClient(path=db_path)
    collection = chroma_client.get_or_create_collection(name="my_inventory_library")
except Exception as e:
    st.stop()

@st.cache_data(ttl=5)
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
                "price": str(row.iloc[4])
            })
    except Exception:
        product_records = []

if not product_records:
    product_records = [
        {"id": "ITM001", "name": "Bluetooth Wireless Headset", "price": "1200", "stock": "50", "category": "Headset"},
        {"id": "ITM002", "name": "Over-Ear Gaming Headset", "price": "1800", "stock": "40", "category": "Headset"},
        {"id": "ITM003", "name": "Fast Type-C Charger 33W", "price": "650", "stock": "120", "category": "Charger"},
    ]

def process_cart_checkout(address: str, secondary_phone: str, description: str, payment_method: str, location_link: str) -> str:
    if not st.session_state.cart:
        return "Your cart is empty."
    customer_name = st.session_state.logged_in_user
    primary_phone = st.session_state.user_phone
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cart_summary = ", ".join([f"{item['quantity']} of {item['product']}" for item in st.session_state.cart])
    
    try:
        order_data = {
            "Type": "Order", "Timestamp": timestamp, "Customer_Name": customer_name,
            "Primary_Phone": primary_phone, "Items": cart_summary, "Address": address,
            "Secondary_Phone": secondary_phone, "Description": description, "Live_Location": location_link
        }
        requests.post(GOOGLE_SCRIPT_URL, json=order_data)
    except Exception:
        pass

    st.session_state.cart = []
    return f"Order placed successfully for {cart_summary}!"

if st.session_state.current_view == "Home":
    col_menu, col_items = st.columns([1, 2], gap="small")
    with col_menu:
        st.markdown("Categories")
        categories = list(set([p['category'] for p in product_records]))
        for cat in categories:
            if st.button(cat, key=f"menu_btn_{cat}", use_container_width=True):
                st.session_state.selected_menu = cat
                st.rerun()

    with col_items:
        current_cat = st.session_state.get("selected_menu", "Headset")
        st.markdown(f"**{current_cat}**")
        filtered_items = [p for p in product_records if p['category'] == current_cat]
        
        if filtered_items:
            for idx, prod in enumerate(filtered_items):
                p_info, p_qty, p_btn = st.columns([1.5, 1, 1], gap="small")
                with p_info:
                    st.markdown(f"**{prod['name']}**")
                    st.caption(f"₹{prod['price']}")
                with p_qty:
                    q_val = st.number_input("Qty", min_value=1.0, value=1.0, step=1.0, key=f"qty_{current_cat}_{idx}", label_visibility="collapsed")
                with p_btn:
                    if st.button("Add", key=f"add_btn_{current_cat}_{idx}", use_container_width=True):
                        st.session_state.cart.append({"product": prod['name'], "quantity": f"{int(q_val)} Units"})
                        st.success("Added!")
                        st.rerun()
                st.markdown("---")
else:
    st.subheader("🛒 Cart & Checkout")
    if st.session_state.cart:
        for c_idx, item in enumerate(st.session_state.cart):
            cc1, cc2 = st.columns([4, 1])
            with cc1:
                st.markdown(f"- **{item['product']}** ({item['quantity']})")
            with cc2:
                if st.button("Remove", key=f"rem_{c_idx}"):
                    st.session_state.cart.pop(c_idx)
                    st.rerun()
        
        with st.form("checkout_form"):
            addr = st.text_area("Delivery Address:")
            phone = st.text_input("Alt Phone:", max_chars=10)
            desc = st.text_area("Notes:")
            pay = st.selectbox("Payment", ["UPI", "COD"])
            loc = st.text_input("Location Link:")
            if st.form_submit_button("Complete Order"):
                if addr and phone:
                    msg = process_cart_checkout(addr, phone, desc, pay, loc)
                    st.success(msg)
                    st.session_state.current_view = "Home"
                    st.rerun()
                else:
                    st.warning("Provide address and phone.")
    else:
        st.info("Cart is empty.")
