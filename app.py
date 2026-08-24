from datetime import datetime
import csv
import os
import random
import chromadb
from google import genai
from google.genai import types
import pandas as pd
import streamlit as st

# 1. Streamlit Page Configuration
st.set_page_config(
    page_title="Enterprise AI Assistant with Smart Cart",
    page_icon="🛒",
    layout="wide",
)

st.title("🔐 Enterprise AI Assistant (Portal)")

# 2. Sidebar - Role Selection & Secure Login System
st.sidebar.header("👤 User Authentication")
role = st.sidebar.selectbox("Select Role", ["Customer", "Owner / Admin"])

# Initialize Session States
if "logged_in_user" not in st.session_state:
    st.session_state.logged_in_user = None
if "user_phone" not in st.session_state:
    st.session_state.user_phone = None
if "user_role" not in st.session_state:
    st.session_state.user_role = None
if "password_verified" not in st.session_state:
    st.session_state.password_verified = False
if "otp_sent" not in st.session_state:
    st.session_state.otp_sent = False
if "generated_otp" not in st.session_state:
    st.session_state.generated_otp = None
if "cart" not in st.session_state:
    st.session_state.cart = []
if "current_view" not in st.session_state:
    st.session_state.current_view = "Home"


# --- OWNER SECURE LOGIN FLOW ---
if role == "Owner / Admin":
    st.sidebar.subheader("👑 Owner Secure Login")

    if st.session_state.user_role != "Owner":
        if not st.session_state.password_verified:
            owner_pass = st.sidebar.text_input(
                "1. Enter Admin Password:", type="password", key="owner_pass_input"
            )
            if st.sidebar.button("Verify Password"):
                if owner_pass == "admin123":
                    st.session_state.password_verified = True
                    st.sidebar.success("✅ Password correct! Enter mobile number.")
                    st.rerun()
                else:
                    st.sidebar.error("❌ Incorrect Password!")

        elif st.session_state.password_verified and not st.session_state.otp_sent:
            mobile_number = st.sidebar.text_input(
                "2. Enter Mobile Number:", max_chars=10, key="owner_mobile_input"
            )
            if st.sidebar.button("Send OTP to Mobile"):
                if len(mobile_number) == 10 and mobile_number.isdigit():
                    otp = str(random.randint(100000, 999999))
                    st.session_state.generated_otp = otp
                    st.session_state.otp_sent = True
                    st.sidebar.success(f"✅ OTP sent to +91 {mobile_number}")
                    st.sidebar.info(f"🔑 [Test SMS OTP]: {otp}")
                    st.rerun()
                else:
                    st.sidebar.warning("⚠️ Enter a valid 10-digit mobile number.")

        elif st.session_state.otp_sent:
            entered_otp = st.sidebar.text_input(
                "3. Enter 6-digit OTP:", max_chars=6, type="password", key="owner_otp_input"
            )
            if st.sidebar.button("Confirm OTP & Login"):
                if entered_otp.strip() == str(st.session_state.generated_otp).strip():
                    st.session_state.logged_in_user = "Owner"
                    st.session_state.user_role = "Owner"
                    st.session_state.password_verified = False
                    st.session_state.otp_sent = False
                    st.sidebar.success("✅ Owner Login Successful!")
                    st.rerun()
                else:
                    st.sidebar.error("❌ Invalid OTP.")

    if st.session_state.user_role == "Owner":
        st.sidebar.markdown("---")
        st.sidebar.subheader("📊 Owner Controls")
        if st.sidebar.button("Logout"):
            st.session_state.clear()
            st.rerun()

# --- CUSTOMER LOGIN FLOW ---
else:
    st.sidebar.subheader("🛍️ Customer Direct Login")

    if st.session_state.user_role != "Customer":
        with st.sidebar.form("customer_direct_login"):
            cust_name = st.text_input("Enter Your Name:")
            cust_phone = st.text_input("Enter Mobile Number:", max_chars=10)
            login_btn = st.form_submit_button("Login")

            if login_btn:
                if cust_name.strip() and len(cust_phone) == 10 and cust_phone.isdigit():
                    st.session_state.logged_in_user = cust_name.strip()
                    st.session_state.user_phone = cust_phone.strip()
                    st.session_state.user_role = "Customer"
                    st.success("✅ Login Successful!")
                    st.rerun()
                else:
                    st.sidebar.warning("⚠️ Please provide a valid name and 10-digit mobile number.")

    if st.session_state.user_role == "Customer":
        st.sidebar.write(f"Logged in: **{st.session_state.logged_in_user}**")
        st.sidebar.write(f"Phone: **{st.session_state.user_phone}**")
        if st.sidebar.button("Logout"):
            st.session_state.clear()
            st.rerun()

# Stop execution if not logged in
if not st.session_state.logged_in_user:
    st.warning("⚠️ Please log in via the sidebar to access the portal.")
    st.stop()


# 3. Gemini API Configuration & Database Setup
db_path = "./chroma_db"

try:
    api_key_input = st.secrets["GOOGLE_API_KEY"]
    client = genai.Client(api_key=api_key_input)
    chroma_client = chromadb.PersistentClient(path=db_path)
    collection = chroma_client.get_or_create_collection(name="my_inventory_library")
except Exception as e:
    st.error(f"Error connecting to Database or API Key missing: {e}")
    st.stop()


def load_inventory_to_chroma():
    file_name = "inventory.csv"
    if not os.path.exists(file_name):
        return
    try:
        existing = collection.get(ids=[file_name])
        if not existing or not existing["ids"]:
            df = pd.read_csv(file_name)
            file_text = df.to_string(index=False)
            if file_text.strip():
                collection.add(documents=[file_text], ids=[file_name])
    except Exception:
        pass


load_inventory_to_chroma()


# Product records grouped by your requested categories
product_records = [
    {"id": "ITM001", "name": "Bluetooth Wireless Headset", "price": "1200", "stock": "50", "category": "Headset"},
    {"id": "ITM002", "name": "Over-Ear Gaming Headset", "price": "1800", "stock": "40", "category": "Headset"},
    
    {"id": "ITM003", "name": "Fast Type-C Charger 33W", "price": "650", "stock": "120", "category": "Charger"},
    {"id": "ITM004", "name": "Dual Port Fast Wall Charger", "price": "500", "stock": "90", "category": "Charger"},
    
    {"id": "ITM005", "name": "Braided Micro USB Cable", "price": "250", "stock": "200", "category": "Cable"},
    {"id": "ITM006", "name": "Type-C Fast Charging Cable", "price": "300", "stock": "150", "category": "Cable"},
    
    {"id": "ITM007", "name": "Professional Studio Mic", "price": "2500", "stock": "30", "category": "Mic"},
    {"id": "ITM008", "name": "Mini Lavalier Clip-on Mic", "price": "450", "stock": "80", "category": "Mic"},
    
    {"id": "ITM009", "name": "Lithium Mobile Replacement Battery", "price": "800", "stock": "45", "category": "Battery"},
    
    {"id": "ITM010", "name": "Edge-to-Edge Tempered Glass", "price": "200", "stock": "300", "category": "Tempered"},
    
    {"id": "ITM011", "name": "Wireless Bluetooth Ear Pods", "price": "1500", "stock": "75", "category": "Ear pod"},
]


# 4. Define Tools
def search_knowledge_base(query: str) -> str:
    """Search inventory data, stock details, and products from the vector database."""
    try:
        results = collection.query(query_texts=[query], n_results=1)
        if results["documents"] and len(results["documents"][0]) > 0:
            return results["documents"][0][0]
        return "No relevant information found."
    except Exception as e:
        return f"Error during search: {e}"


def add_to_cart(product_name: str, quantity: str = "1 Unit") -> str:
    """Add a product or service item into the shopping cart with custom quantity/weight."""
    st.session_state.cart.append({"product": product_name, "quantity": str(quantity)})
    st.session_state.last_booked_item = product_name
    return f"Added '{product_name}' (Qty: {quantity}) to your cart successfully!"


def calculate_total_price(price: float, quantity: int, discount_percentage: float = 0.0) -> str:
    """Calculate total price including quantity and optional discount."""
    subtotal = price * quantity
    discount_amount = subtotal * (discount_percentage / 100)
    final_total = subtotal - discount_amount
    return f"Calculation Result: Subtotal = ₹{subtotal}, Discount = ₹{discount_amount}, Final Total = ₹{final_total}"


def process_cart_checkout(address: str, secondary_phone: str, description: str, payment_method: str, location_link: str) -> str:
    """Checkout all items currently in the cart with delivery and payment details."""
    if not st.session_state.cart:
        return "Your cart is empty. Please add products first."
    
    customer_name = st.session_state.logged_in_user
    primary_phone = st.session_state.user_phone
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    txn_id = "TXN" + datetime.now().strftime("%Y%m%d%H%M%S")

    cart_summary = ", ".join([f"{item['quantity']} of {item['product']}" for item in st.session_state.cart])
    st.session_state.last_booked_item = cart_summary

    file_exists = os.path.isfile("orders.csv")
    with open("orders.csv", mode="a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Timestamp", "Customer Name", "Primary Phone", "Items", "Address", "Secondary Phone", "Description", "Live Location"])
        writer.writerow([timestamp, customer_name, primary_phone, cart_summary, address, secondary_phone, description, location_link])

    pay_exists = os.path.isfile("payments.csv")
    with open("payments.csv", mode="a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not pay_exists:
            writer.writerow(["Timestamp", "Customer Name", "Items", "Method", "Transaction ID"])
        writer.writerow([timestamp, customer_name, cart_summary, payment_method, txn_id])

    st.session_state.cart = []
    return f"Checkout complete! Order placed for: {cart_summary}. Payment via {payment_method} successful (TXN ID: {txn_id})."


def add_product_review(rating: int, review_comment: str) -> str:
    """Submit a product review and rating (1 to 5 stars)."""
    item = st.session_state.get("last_booked_item", "General Products")
    customer_name = st.session_state.logged_in_user
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    file_exists = os.path.isfile("reviews.csv")
    with open("reviews.csv", mode="a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Timestamp", "Customer Name", "Product", "Rating", "Comment"])
        writer.writerow([timestamp, customer_name, item, rating, review_comment])

    return f"Thank you, {customer_name}! Your review ({rating}/5 stars) has been saved."


# 5. Interface Logic
if st.session_state.user_role == "Owner":
    st.subheader("👑 Owner Admin Dashboard")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 📦 Customer Orders")
        if os.path.exists("orders.csv"):
            st.dataframe(pd.read_csv("orders.csv"), hide_index=True)
        else:
            st.info("No orders found.")

    with col2:
        st.markdown("### 💳 Payment Records")
        if os.path.exists("payments.csv"):
            st.dataframe(pd.read_csv("payments.csv"), hide_index=True)
        else:
            st.info("No payments found.")

    st.markdown("---")
    st.markdown("### ⭐ Customer Reviews")
    if os.path.exists("reviews.csv"):
        st.dataframe(pd.read_csv("reviews.csv"), hide_index=True)
    else:
        st.info("No reviews found.")

else:
    # Top Navigation Bar (Home & Cart Buttons)
    nav_col1, nav_col2, nav_col3 = st.columns([3, 1, 1])
    with nav_col1:
        st.write(f"Welcome, **{st.session_state.logged_in_user}**!")
    with nav_col2:
        if st.button("🏠 Home", use_container_width=True):
            st.session_state.current_view = "Home"
            st.rerun()
    with nav_col3:
        cart_count = len(st.session_state.cart)
        if st.button(f"🛒 Cart ({cart_count})", use_container_width=True):
            st.session_state.current_view = "Cart"
            st.rerun()

    st.markdown("---")

    # View Switching: Home View vs Cart/Checkout View
    if st.session_state.current_view == "Home":
        col_catalog, col_ai = st.columns([1.2, 1.8], gap="large")

        with col_catalog:
            with st.container(height=650, border=True):
                st.markdown("### 📂 Product Categories")
                st.caption("Click any category below to view and add items directly:")

                categories = ["Headset", "Charger", "Cable", "Mic", "Battery", "Tempered", "Ear pod"]

                for cat in categories:
                    with st.expander(f"📦 {cat}"):
                        cat_products = [p for p in product_records if p['category'] == cat]
                        
                        if cat_products:
                            for idx, prod in enumerate(cat_products):
                                # Row-wise structured layout inside columns
                                r_info, r_qty, r_unit, r_btn = st.columns([2.5, 1, 1, 1], vertical_alignment="center")
                                
                                with r_info:
                                    st.markdown(f"**{prod['name']}**  \n<small style='color:gray;'>₹{prod['price']} | Stock: {prod['stock']}</small>", unsafe_allow_html=True)
                                
                                with r_qty:
                                    q_val = st.number_input("Qty", min_value=1.0, value=1.0, step=1.0, key=f"qty_{cat}_{idx}", label_visibility="collapsed")
                                
                                with r_unit:
                                    u_val = st.selectbox("Unit", ["Units", "Pieces"], key=f"unit_{cat}_{idx}", label_visibility="collapsed")
                                
                                with r_btn:
                                    if st.button("Add", key=f"btn_{cat}_{idx}", use_container_width=True):
                                        full_q_str = f"{int(q_val)} {u_val}"
                                        st.session_state.cart.append({"product": prod['name'], "quantity": full_q_str})
                                        st.success(f"Added!")
                                        st.rerun()
                                
                                st.markdown("---")
                        else:
                            st.info(f"No items available under {cat}.")

        with col_ai:
            st.markdown("### 💬 AI Assistant Search & Chat")
            
            user_prompt = st.text_input("Ask AI about inventory, products, or requests:", placeholder="Type here...", key="top_ai_search_input")
            
            if user_prompt:
                msg_id = len(st.session_state.get("messages", []))
                if "messages" not in st.session_state:
                    st.session_state.messages = []
                
                st.session_state.messages.append({"role": "user", "content": user_prompt, "id": msg_id})
                
                with st.spinner("AI Assistant is processing..."):
                    try:
                        context_memory = f" [Context - User: {st.session_state.logged_in_user}, Phone: {st.session_state.user_phone}]"
                        full_prompt = user_prompt + context_memory

                        response = client.models.generate_content(
                            model="gemini-2.5-flash",
                            contents=full_prompt,
                            config=types.GenerateContentConfig(
                                tools=[
                                    search_knowledge_base,
                                    add_to_cart,
                                    calculate_total_price,
                                    process_cart_checkout,
                                    add_product_review,
                                ],
                                temperature=0.3,
                                system_instruction=(
                                    "You are an advanced multi-lingual enterprise e-commerce AI assistant. "
                                    "1. Detect user language and ALWAYS respond in that same language. "
                                    "2. When listing products, mention their exact names clearly."
                                ),
                            ),
                        )

                        final_reply = ""
                        if response.function_calls:
                            for function_call in response.function_calls:
                                tool_name = function_call.name
                                tool_args = function_call.args

                                if tool_name == "search_knowledge_base":
                                    tool_result = search_knowledge_base(**tool_args)
                                elif tool_name == "add_to_cart":
                                    tool_result = add_to_cart(**tool_args)
                                    st.rerun()
                                elif tool_name == "calculate_total_price":
                                    tool_result = calculate_total_price(**tool_args)
                                elif tool_name == "process_cart_checkout":
                                    tool_result = process_cart_checkout(**tool_args)
                                elif tool_name == "add_product_review":
                                    tool_result = add_product_review(**tool_args)
                                else:
                                    tool_result = "Tool not found."

                                followup_prompt = f"The tool '{tool_name}' returned: '{tool_result}'. Respond naturally to user request: '{user_prompt}' in user's language."
                                final_response = client.models.generate_content(
                                    model="gemini-2.5-flash", contents=followup_prompt
                                )
                                final_reply = final_response.text
                        else:
                            final_reply = response.text

                        st.session_state.messages.append({"role": "assistant", "content": final_reply, "id": msg_id + 1})
                    except Exception as e:
                        st.error(f"Error: {e}")

            st.markdown("---")
            
            with st.container(height=500, border=True):
                if "messages" in st.session_state:
                    for message in st.session_state.messages:
                        with st.chat_message(message["role"]):
                            st.markdown(message["content"])
                            
                            if message["role"] == "assistant":
                                for p_idx, prod in enumerate(product_records):
                                    if prod['name'].lower() in message["content"].lower():
                                        with st.container():
                                            st.markdown(f"👉 **Quick Add: {prod['name']}**")
                                            ai_q_col, ai_u_col, ai_b_col = st.columns([1, 1, 1])
                                            with ai_q_col:
                                                aq_val = st.number_input("Qty", min_value=1.0, value=1.0, step=1.0, key=f"ai_q_{message.get('id', 0)}_{p_idx}")
                                            with ai_u_col:
                                                au_val = st.selectbox("Unit", ["Units", "Pieces"], key=f"ai_u_{message.get('id', 0)}_{p_idx}")
                                            with ai_b_col:
                                                st.write("")
                                                if st.button("Add to Cart", key=f"ai_btn_{message.get('id', 0)}_{p_idx}"):
                                                    full_aq_str = f"{int(aq_val)} {au_val}"
                                                    st.session_state.cart.append({"product": prod['name'], "quantity": full_aq_str})
                                                    st.success(f"Added {full_aq_str} of {prod['name']}!")
                                                    st.rerun()

    else:
        st.subheader("🛒 Your Shopping Cart & Checkout")
        if st.session_state.cart:
            for c_idx, item in enumerate(st.session_state.cart):
                cc1, cc2 = st.columns([4, 1])
                with cc1:
                    st.write(f"- **{item['product']}** ({item['quantity']})")
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
