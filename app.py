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

# 1. Streamlit Page Configuration & Professional High-Contrast Styling CSS
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
        
        input, textarea {
            background-color: var(--secondary-background-color) !important;
            color: var(--text-color) !important;
            border: 1.5px solid #cbd5e1 !important;
            font-size: 14px !important;
            font-weight: 500 !important;
            border-radius: 6px !important;
        }

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

        div[data-testid="stHorizontalBlock"] {
            display: flex;
            flex-direction: row;
            flex-wrap: nowrap;
            width: 100%;
        }
        div[data-testid="column"] {
            flex: 1 1 33% !important;
            min-width: 0px !important;
            padding: 0px 6px !important;
        }
        .block-container {
            padding-top: 1rem;
            padding-bottom: 0rem;
            padding-left: 1.5rem;
            padding-right: 1.5rem;
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

# Google Apps Script Web App Endpoint URL
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


# Owner Login & Customer Login Screen
if not st.session_state.logged_in_user:
    st.markdown("""
        <div style='text-align: center; margin-top: 30px; margin-bottom: 15px;'>
            <h1 style='font-size: 30px; font-weight: 800; margin-bottom: 4px;'>HM MOBILES</h1>
            <p style='font-size: 14px; font-weight: 500;'>Thiruverkadu - Portal Login</p>
        </div>
    """, unsafe_allow_html=True)
    
    _, mid_col, _ = st.columns([1.3, 1, 1.3])
    
    with mid_col:
        with st.container():
            st.markdown("""
                <div style='padding: 25px; border-radius: 12px; border: 1.5px solid #cbd5e1; box-shadow: 0 4px 15px -3px rgba(0,0,0,0.05); text-align: center;'>
                    <h3 style='margin-top: 0; margin-bottom: 15px; font-size: 18px; font-weight: 750;'>Login (Customer or Owner)</h3>
            """, unsafe_allow_html=True)
            
            with st.form("customer_direct_login_center"):
                cust_name = st.text_input("Name / Owner:")
                cust_phone = st.text_input("Mobile Number:", max_chars=10)
                login_btn = st.form_submit_button("Secure Login", use_container_width=True)

                if login_btn:
                    if cust_name.strip() and len(cust_phone) == 10 and cust_phone.isdigit():
                        st.session_state.logged_in_user = cust_name.strip()
                        st.session_state.user_phone = cust_phone.strip()
                        
                        if cust_phone == "9840450113" or "owner" in cust_name.lower():
                            st.session_state.user_role = "Owner"
                            st.session_state.current_view = "OwnerDashboard"
                        else:
                            st.session_state.user_role = "Customer"
                            st.session_state.selected_menu = "Headset"
                        
                        log_login_to_sheet(cust_name.strip(), cust_phone.strip())
                        st.success("✅ Login Successful!")
                        st.rerun()
                    else:
                        st.warning("⚠️ Please provide a valid name and 10-digit mobile number.")
            
            st.markdown("</div>", unsafe_allow_html=True)
    
    st.stop()


# --- HEADER & NAVIGATION ---
st.markdown("""
    <div class="brand-banner">
        <h1 class="brand-title">HM MOBILES THIRUVERKADU</h1>
    </div>
""", unsafe_allow_html=True)

top_c1, top_c2, top_c3, top_c4 = st.columns([2.2, 1, 1, 1])
with top_c1:
    role_badge = "👑 [Owner]" if st.session_state.user_role == "Owner" else "👤 [Customer]"
    st.markdown(f"👋 Welcome back, **{st.session_state.logged_in_user}** {role_badge}!")
with top_c2:
    if st.button("Home / Menu", use_container_width=True):
        st.session_state.current_view = "Home"
        st.rerun()
with top_c3:
    if st.session_state.user_role == "Owner":
        if st.button("🛠️ Owner Panel", use_container_width=True):
            st.session_state.current_view = "OwnerDashboard"
            st.rerun()
    else:
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
    st.error(f"Error connecting to Database: {e}")
    st.stop()


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


def log_new_item_to_sheet(item_id, name, category, stock, price, image_url):
    try:
        payload = {
            "Type": "AddItem",
            "Item_ID": item_id,
            "Item_Name": name,
            "Category": category,
            "Stock_Quantity": stock,
            "Price_INR": price,
            "Image": image_url
        }
        requests.post(GOOGLE_SCRIPT_URL, json=payload)
    except Exception as e:
        print(f"Add item error: {e}")


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
                "image": str(row.iloc[5]) if len(row) > 5 and pd.notna(row.iloc[5]) else "https://images.unsplash.com/photo-1546435770-a3e426bf472b?w=400&q=80"
            })
    except Exception:
        product_records = []


# --- OWNER DASHBOARD VIEW WITH URL INPUT ---
if st.session_state.current_view == "OwnerDashboard" and st.session_state.user_role == "Owner":
    st.subheader("🛠️ Owner Inventory & Menu Management Dashboard")
    st.markdown("Add new products directly to your catalog and Google Sheet:")
    
    with st.form("owner_add_item_form"):
        col_1, col_2 = st.columns(2)
        with col_1:
            new_id = st.text_input("Item ID (e.g., ITM012):")
            new_name = st.text_input("Product Name:")
            new_cat = st.text_input("Category (e.g., Charger, Headset, Backcase):")
        with col_2:
            new_stock = st.number_input("Stock Quantity:", min_value=1, value=50)
            new_price = st.number_input("Price (INR):", min_value=1.0, value=500.0)
            new_img = st.text_input("Image URL (Google Drive link or direct link):", placeholder="https://...")
            
        submit_item = st.form_submit_button("➕ Add Item to Menu & Sheet")
        
        if submit_item:
            if new_id and new_name and new_cat:
                image_link = new_img if new_img.strip() else "https://images.unsplash.com/photo-1546435770-a3e426bf472b?w=400&q=80"
                log_new_item_to_sheet(new_id, new_name, new_cat, new_stock, new_price, image_link)
                st.success(f"✅ Successfully added '{new_name}' to inventory sheet!")
                st.balloons()
            else:
                st.warning("⚠️ Please fill in Item ID, Name, and Category.")

    st.markdown("---")
    st.subheader("📋 Current Live Inventory Catalog")
    st.dataframe(inv_df, use_container_width=True)

# --- STANDARD CUSTOMER HOME / MENU VIEW ---
elif st.session_state.current_view == "Home":
    col_menu, col_items, col_ai = st.columns([0.8, 1.4, 1.5], gap="small")

    with col_menu:
        st.markdown("Menu")
        with st.container(height=550, border=True):
            categories = list(set([p['category'] for p in product_records])) if product_records else ["Headset"]
            for cat in categories:
                if st.button(cat, key=f"menu_btn_{cat}", use_container_width=True):
                    st.session_state.selected_menu = cat
                    st.rerun()

    with col_items:
        current_cat = st.session_state.get("selected_menu", "Headset")
        st.markdown(f"{current_cat}")
        with st.container(height=550, border=True):
            filtered_items = [p for p in product_records if p['category'] == current_cat]
            
            if filtered_items:
                for idx, prod in enumerate(filtered_items):
                    img_col, info_col, action_col = st.columns([1, 1.8, 1.8], gap="small")
                    
                    with img_col:
                        img_url = prod.get("image", "https://images.unsplash.com/photo-1546435770-a3e426bf472b?w=400&q=80")
                        try:
                            st.image(img_url, use_container_width=True)
                        except Exception:
                            st.markdown("📱")
                    
                    with info_col:
                        st.markdown(f"**{prod['name']}**")
                        st.caption(f"₹{prod['price']}")
                    
                    with action_col:
                        q_val = st.number_input("Qty", min_value=1.0, value=1.0, step=1.0, key=f"qty_{current_cat}_{idx}", label_visibility="collapsed")
                        if st.button("Add", key=f"add_btn_{current_cat}_{idx}", use_container_width=True):
                            full_q_str = f"{int(q_val)} Units"
                            st.session_state.cart.append({"product": prod['name'], "quantity": full_q_str})
                            st.success(f"Added!")
                            st.rerun()
                            
                    st.markdown("---")
            else:
                st.info("No items found.")

    with col_ai:
        st.markdown("AI Assistant")
        user_prompt = st.text_input("Ask AI:", placeholder="Type here...", key="top_ai_search_input", label_visibility="collapsed")
        
        if user_prompt:
            msg_id = len(st.session_state.get("messages", []))
            if "messages" not in st.session_state:
                st.session_state.messages = []
            st.session_state.messages.append({"role": "user", "content": user_prompt, "id": msg_id})
            
            with st.spinner("Processing..."):
                try:
                    response = client.models.generate_content(
                        model="gemini-3.6-flash",
                        contents=user_prompt,
                        config=types.GenerateContentConfig(temperature=0.3),
                    )
                    st.session_state.messages.append({"role": "assistant", "content": response.text, "id": msg_id + 1})
                except Exception as e:
                    st.error(f"Error: {e}")

        with st.container(height=460, border=True):
            if "messages" in st.session_state:
                for message in st.session_state.messages:
                    with st.chat_message(message["role"]):
                        st.markdown(message["content"])

# --- CART / CHECKOUT VIEW ---
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
                    st.success("✅ Order placed successfully!")
                    st.session_state.cart = []
                    st.session_state.current_view = "Home"
                    st.rerun()
                else:
                    st.warning("⚠️ Please provide delivery address and secondary contact number.")
    else:
        st.info("Your cart is empty. Click **Home / Menu** above to browse products.")
