from datetime import datetime
import csv
import os
import random
import urllib.parse
import chromadb
from google import genai
from google.genai import types
import pandas as pd
import requests
import streamlit as st

# 1. Streamlit Page Configuration & Professional Light Theme CSS
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
            background-color: #f8fafc !important;
            color: #0f172a !important;
        }

        /* Hide Streamlit default chrome, top header, menu, share, github */
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
        
        /* Force Light Theme Component Backgrounds */
        .stApp {
            background-color: #f8fafc !important;
        }

        /* Typography Colors (Dark text on light background) */
        label, .stTextInput label, p, span, div[data-testid="stMarkdownContainer"] p, h1, h2, h3, h4 {
            color: #0f172a !important;
        }
        
        /* Form Inputs Light Styling */
        input, textarea {
            background-color: #ffffff !important;
            color: #0f172a !important;
            border: 1px solid #cbd5e1 !important;
            font-size: 14px !important;
            border-radius: 8px !important;
        }

        /* Professional Header Banner */
        .brand-banner {
            background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%);
            padding: 24px;
            border-radius: 12px;
            color: #ffffff !important;
            text-align: center;
            box-shadow: 0 4px 12px rgba(2, 132, 199, 0.15);
            margin-bottom: 20px;
        }
        .brand-title {
            font-size: 28px;
            font-weight: 800;
            letter-spacing: 0.5px;
            color: #ffffff !important;
            margin: 0;
        }

        /* Sleek Modern Buttons */
        div.stButton > button {
            background-color: #0284c7 !important;
            color: #ffffff !important;
            border: none !important;
            font-weight: 600 !important;
            font-size: 14px !important;
            border-radius: 8px !important;
            padding: 0.5rem 1rem !important;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            transition: all 0.2s ease;
        }
        div.stButton > button:hover {
            background-color: #0369a1 !important;
            color: #ffffff !important;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }

        .block-container {
            padding-top: 1.5rem;
            padding-bottom: 2rem;
            padding-left: 2rem;
            padding-right: 2rem;
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


def log_order_to_sheet(name, phone, items, address, alt_phone, desc):
    try:
        payload = {
            "Type": "Order",
            "Customer_Name": name,
            "Primary_Phone": phone,
            "Items": items,
            "Address": address,
            "Alt_Phone": alt_phone,
            "Description": desc
        }
        requests.post(GOOGLE_SCRIPT_URL, json=payload)
    except Exception as e:
        print(f"Order sheet error: {e}")


# Owner Login & Customer Login Screen
if not st.session_state.logged_in_user:
    st.markdown("""
        <div style='text-align: center; margin-top: 50px; margin-bottom: 20px;'>
            <h1 style='font-size: 32px; font-weight: 800; color: #0f172a; margin-bottom: 6px;'>HM MOBILES</h1>
            <p style='font-size: 15px; color: #64748b; font-weight: 500;'>Thiruverkadu - Professional Portal</p>
        </div>
    """, unsafe_allow_html=True)
    
    _, mid_col, _ = st.columns([1.2, 1, 1.2])
    
    with mid_col:
        with st.container():
            st.markdown("""
                <div style='background: #ffffff; padding: 30px; border-radius: 16px; border: 1px solid #cbd5e1; box-shadow: 0 10px 25px -5px rgba(0,0,0,0.05);'>
                    <h3 style='margin-top: 0; margin-bottom: 20px; font-size: 18px; font-weight: 700; color: #0f172a; text-align: center;'>Account Sign In</h3>
            """, unsafe_allow_html=True)
            
            with st.form("customer_direct_login_center"):
                cust_name = st.text_input("Full Name / Owner:")
                cust_phone = st.text_input("10-Digit Mobile Number:", max_chars=10)
                login_btn = st.form_submit_button("Sign In Securely", use_container_width=True)

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
    st.markdown(f"👋 Welcome, **{st.session_state.logged_in_user}** {role_badge}")
with top_c2:
    if st.button("Store Catalog", use_container_width=True):
        st.session_state.current_view = "Home"
        st.rerun()
with top_c3:
    if st.session_state.user_role == "Owner":
        if st.button("🛠️ Owner Panel", use_container_width=True):
            st.session_state.current_view = "OwnerDashboard"
            st.rerun()
    else:
        cart_count = len(st.session_state.cart)
        if st.button(f"🛒 Cart ({cart_count})", use_container_width=True):
            st.session_state.current_view = "Cart"
            st.rerun()
with top_c4:
    if st.button("Sign Out", use_container_width=True):
        st.session_state.clear()
        st.rerun()

st.markdown("<br>", unsafe_allow_html=True)

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


def upload_image_to_host(uploaded_file):
    try:
        url = "https://api.imgbb.com/1/upload"
        payload = {"key": "6d207e02198a847aa98d0a2a901485a2"}
        files = {"image": uploaded_file.getvalue()}
        response = requests.post(url, data=payload, files=files)
        result = response.json()
        if result.get("success"):
            return result["data"]["url"]
    except Exception as e:
        print(f"Image upload error: {e}")
    return "https://images.unsplash.com/photo-1546435770-a3e426bf472b?w=400&q=80"


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


def update_item_in_sheet(item_id, name, category, stock, price, image_url):
    try:
        payload = {
            "Type": "UpdateItem",
            "Item_ID": item_id,
            "Item_Name": name,
            "Category": category,
            "Stock_Quantity": stock,
            "Price_INR": price,
            "Image": image_url
        }
        requests.post(GOOGLE_SCRIPT_URL, json=payload)
    except Exception as e:
        print(f"Update item error: {e}")


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


# --- OWNER DASHBOARD VIEW ---
if st.session_state.current_view == "OwnerDashboard" and st.session_state.user_role == "Owner":
    st.subheader("🛠️ Owner Inventory & Management Dashboard")
    
    owner_tab1, owner_tab2 = st.tabs(["➕ Add New Item", "✏️ Edit Existing Item"])
    
    with owner_tab1:
        with st.form("owner_add_item_form"):
            col_1, col_2 = st.columns(2)
            with col_1:
                new_id = st.text_input("Item ID (e.g., ITM012):")
                new_name = st.text_input("Product Name:")
                new_cat = st.text_input("Category (e.g., Charger, Headset):")
            with col_2:
                new_stock = st.number_input("Stock Quantity:", min_value=1, value=50)
                new_price = st.number_input("Price (INR):", min_value=1.0, value=500.0)
                
            uploaded_file = st.file_uploader("Upload Product Image", type=["jpg", "png", "jpeg"], key="add_img")
            submit_item = st.form_submit_button("➕ Add Item to Catalog")
            
            if submit_item:
                if new_id and new_name and new_cat:
                    image_link = "https://images.unsplash.com/photo-1546435770-a3e426bf472b?w=400&q=80"
                    if uploaded_file is not None:
                        image_link = upload_image_to_host(uploaded_file)
                    log_new_item_to_sheet(new_id, new_name, new_cat, new_stock, new_price, image_link)
                    st.success(f"✅ Successfully added '{new_name}'!")
                    st.balloons()
                else:
                    st.warning("⚠️ Please fill in Item ID, Name, and Category.")

    with owner_tab2:
        if not inv_df.empty:
            item_ids = inv_df.iloc[:, 0].astype(str).tolist()
            selected_id = st.selectbox("Select Item ID to Edit:", item_ids)
            matched_row = inv_df[inv_df.iloc[:, 0].astype(str) == selected_id]
            if not matched_row.empty:
                curr_name = str(matched_row.iloc[0, 1])
                curr_cat = str(matched_row.iloc[0, 2])
                curr_stock = int(matched_row.iloc[0, 3])
                curr_price = float(matched_row.iloc[0, 4])
                curr_img = str(matched_row.iloc[0, 5]) if len(matched_row.columns) > 5 and pd.notna(matched_row.iloc[0, 5]) else ""
                
                with st.form("owner_edit_item_form"):
                    e_col1, e_col2 = st.columns(2)
                    with e_col1:
                        edit_name = st.text_input("Product Name:", value=curr_name)
                        edit_cat = st.text_input("Category:", value=curr_cat)
                    with e_col2:
                        edit_stock = st.number_input("Stock Quantity:", min_value=0, value=curr_stock)
                        edit_price = st.number_input("Price (INR):", min_value=1.0, value=curr_price)
                        
                    edit_file = st.file_uploader("Upload New Image (Optional)", type=["jpg", "png", "jpeg"], key="edit_img")
                    submit_edit = st.form_submit_button("💾 Save Updates")
                    
                    if submit_edit:
                        final_img = curr_img
                        if edit_file is not None:
                            final_img = upload_image_to_host(edit_file)
                        update_item_in_sheet(selected_id, edit_name, edit_cat, edit_stock, edit_price, final_img)
                        st.success(f"✅ Updated Item ID {selected_id} successfully!")
        else:
            st.info("No items found.")

    st.markdown("---")
    st.subheader("📋 Live Inventory Data")
    st.dataframe(inv_df, use_container_width=True)

# --- STANDARD CUSTOMER CATALOG & STORE VIEW ---
elif st.session_state.current_view == "Home":
    col_menu, col_items, col_ai = st.columns([1, 2.2, 1.8], gap="medium")

    with col_menu:
        st.markdown("### Categories")
        categories = list(set([p['category'] for p in product_records])) if product_records else ["Headset"]
        for cat in categories:
            if st.button(cat, key=f"menu_btn_{cat}", use_container_width=True):
                st.session_state.selected_menu = cat
                st.rerun()

    with col_items:
        current_cat = st.session_state.get("selected_menu", "Headset")
        st.markdown(f"### {current_cat}")
        filtered_items = [p for p in product_records if p['category'] == current_cat]
        
        if filtered_items:
            for idx, prod in enumerate(filtered_items):
                st.markdown(f"""
                    <div style='background: #ffffff; padding: 14px 18px; border-radius: 10px; border: 1px solid #cbd5e1; margin-bottom: 10px; display: flex; align-items: center; justify-content: space-between;'>
                        <div>
                            <h4 style='margin: 0 0 4px 0; font-size: 16px; color: #0f172a;'>{prod['name']}</h4>
                            <span style='color: #0284c7; font-weight: 700; font-size: 15px;'>₹{prod['price']}</span>
                        </div>
                """, unsafe_allow_html=True)
                
                c_img, c_qty, c_btn = st.columns([1, 1, 1.2], gap="small")
                with c_img:
                    try:
                        st.image(prod.get("image", ""), width=65)
                    except Exception:
                        st.markdown("📱")
                with c_qty:
                    # Pure numeric input box without unit suffix
                    q_val = st.text_input("Qty", value="1", key=f"qty_{current_cat}_{idx}", label_visibility="collapsed")
                with c_btn:
                    if st.button("Add to Cart", key=f"add_btn_{current_cat}_{idx}", use_container_width=True):
                        qty_str = q_val.strip() if q_val.strip().isdigit() else "1"
                        full_q_str = f"{qty_str} Units"
                        st.session_state.cart.append({"product": prod['name'], "quantity": full_q_str})
                        st.success("Added!")
                        st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.info("No items found in this category.")

    with col_ai:
        st.markdown("### Assistant")
        user_prompt = st.text_input("Ask AI Assistant:", placeholder="Type a question...", key="top_ai_search_input", label_visibility="collapsed")
        
        if user_prompt:
            msg_id = len(st.session_state.get("messages", []))
            if "messages" not in st.session_state:
                st.session_state.messages = []
            st.session_state.messages.append({"role": "user", "content": user_prompt, "id": msg_id})
            
            with st.spinner("Thinking..."):
                try:
                    response = client.models.generate_content(
                        model="gemini-3.6-flash",
                        contents=user_prompt,
                        config=types.GenerateContentConfig(temperature=0.3),
                    )
                    st.session_state.messages.append({"role": "assistant", "content": response.text, "id": msg_id + 1})
                except Exception as e:
                    st.error(f"Error: {e}")

        with st.container(height=420, border=False):
            if "messages" in st.session_state:
                for message in st.session_state.messages:
                    with st.chat_message(message["role"]):
                        st.markdown(message["content"])

# --- CART & CHECKOUT VIEW ---
else:
    st.markdown("### 🛒 Your Shopping Cart & Checkout")
    
    if st.session_state.cart:
        for c_idx, item in enumerate(st.session_state.cart):
            col_item_info, col_item_del = st.columns([5, 1])
            with col_item_info:
                st.markdown(f"• **{item['product']}** — *Qty: {item['quantity']}*")
            with col_item_del:
                if st.button("Remove", key=f"rem_cart_view_{c_idx}"):
                    st.session_state.cart.pop(c_idx)
                    st.rerun()
        
        st.markdown("<hr style='margin: 20px 0; border: none; border-top: 1px solid #cbd5e1;'>", unsafe_allow_html=True)
        st.markdown("#### Delivery Information")
        
        if "checkout_address_input" not in st.session_state:
            st.session_state.checkout_address_input = ""
        if "checkout_alt_phone" not in st.session_state:
            st.session_state.checkout_alt_phone = ""
        if "checkout_desc" not in st.session_state:
            st.session_state.checkout_desc = ""

        checkout_address = st.text_area("Delivery Address:", value=st.session_state.checkout_address_input)
        secondary_phone = st.text_input("Alternative Contact Number:", value=st.session_state.checkout_alt_phone, max_chars=10)
        product_desc = st.text_area("Order Notes / Specifications (Optional):", value=st.session_state.checkout_desc)
        
        st.session_state.checkout_address_input = checkout_address
        st.session_state.checkout_alt_phone = secondary_phone
        st.session_state.checkout_desc = product_desc

        if st.button("Submit Order & Send via WhatsApp", use_container_width=True):
            if checkout_address.strip() and len(secondary_phone) == 10 and secondary_phone.isdigit():
                cart_summary = ", ".join([f"{item['quantity']} of {item['product']}" for item in st.session_state.cart])
                
                # Log order to Google Sheet
                log_order_to_sheet(
                    name=st.session_state.logged_in_user,
                    phone=st.session_state.user_phone,
                    items=cart_summary,
                    address=checkout_address,
                    alt_phone=secondary_phone,
                    desc=product_desc
                )
                
                # Build WhatsApp URL
                raw_wa_message = (
                    f"New Order - HM Mobiles\n"
                    f"Customer: {st.session_state.logged_in_user} ({st.session_state.user_phone})\n"
                    f"Items: {cart_summary}\n"
                    f"Address: {checkout_address}\n"
                    f"Alt Phone: {secondary_phone}\n"
                    f"Description: {product_desc}"
                )
                encoded_message = urllib.parse.quote(raw_wa_message)
                wa_url = f"https://wa.me/919840450113?text={encoded_message}"
                
                st.success("✅ Order logged to Google Sheet successfully! Click below to open WhatsApp.")
                st.markdown(f'<a href="{wa_url}" target="_blank"><button style="background-color: #25D366; color: white; padding: 12px 20px; border: none; border-radius: 8px; font-size: 16px; font-weight: 700; cursor: pointer; width: 100%;">💬 Open WhatsApp Chat Now</button></a>', unsafe_allow_html=True)
                
                st.session_state.cart = []
            else:
                st.warning("⚠️ Please enter a valid delivery address and a 10-digit alternative contact number.")

    else:
        st.info("Your cart is empty. Click **Store Catalog** above to browse products.")
