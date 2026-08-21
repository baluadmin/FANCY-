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
    layout="centered",
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


# --- OWNER SECURE LOGIN FLOW (Kept secure with Admin Password & OTP) ---
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

# --- CUSTOMER LOGIN FLOW (Direct Login without OTP) ---
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
                    st.warning("⚠️ Please provide a valid name and 10-digit mobile number.")

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


def add_to_cart(product_name: str, quantity: int = 1) -> str:
    """Add a product or service item into the shopping cart."""
    st.session_state.cart.append({"product": product_name, "quantity": quantity})
    st.session_state.last_booked_item = product_name
    return f"Added {quantity}x '{product_name}' to your cart successfully!"


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

    cart_summary = ", ".join([f"{item['quantity']}x {item['product']}" for item in st.session_state.cart])
    st.session_state.last_booked_item = cart_summary

    # Save to orders
    file_exists = os.path.isfile("orders.csv")
    with open("orders.csv", mode="a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Timestamp", "Customer Name", "Primary Phone", "Items", "Address", "Secondary Phone", "Description", "Live Location"])
        writer.writerow([timestamp, customer_name, primary_phone, cart_summary, address, secondary_phone, description, location_link])

    # Save to payments
    pay_exists = os.path.isfile("payments.csv")
    with open("payments.csv", mode="a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not pay_exists:
            writer.writerow(["Timestamp", "Customer Name", "Items", "Method", "Transaction ID"])
        writer.writerow([timestamp, customer_name, cart_summary, payment_method, txn_id])

    # Clear cart after checkout
    st.session_state.cart = []

    return f"Checkout complete! Order placed for: {cart_summary}. Payment via {payment_method} successful (TXN ID: {txn_id}). Please leave your rating and review!"


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
    # Customer UI Layout
    col_main, col_cart = st.columns([2, 1])

    with col_cart:
        st.markdown("### 🛒 Your Cart")
        if st.session_state.cart:
            for idx, item in enumerate(st.session_state.cart):
                st.write(f"- **{item['product']}** (Qty: {item['quantity']})")
                if st.button(f"Remove Item {idx+1}", key=f"remove_{idx}"):
                    st.session_state.cart.pop(idx)
                    st.rerun()
            
            st.markdown("---")
            st.subheader("📍 Secure Checkout Form")
            with st.form("checkout_form"):
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
                        st.rerun()
                    else:
                        st.warning("⚠️ Please provide delivery address and secondary contact number.")
        else:
            st.info("Your cart is empty. Ask the assistant to add items.")

    with col_main:
        st.write(f"Welcome, **{st.session_state.logged_in_user}**! Search items, add to cart, or chat with the AI.")

        if "messages" not in st.session_state:
            st.session_state.messages = []

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if user_prompt := st.chat_input("Ask about inventory, add items to cart, or type in your language..."):
            st.session_state.messages.append({"role": "user", "content": user_prompt})
            with st.chat_message("user"):
                st.markdown(user_prompt)

            with st.chat_message("assistant"):
                with st.spinner("AI Assistant is processing..."):
                    try:
                        context_memory = f" [Context - User: {st.session_state.logged_in_user}, Phone: {st.session_state.user_phone}]"
                        full_prompt = user_prompt + context_memory

                        response = client.models.generate_content(
                            model="gemini-3.6-flash",
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
                                    "2. Use the 'add_to_cart' tool when a user wishes to buy or add products. "
                                    "3. Guide users to manage their cart and complete checkout using the cart panel. "
                                    "4. When feedback is provided, use 'add_product_review' and warmly thank the customer."
                                ),
                            ),
                        )

                        final_reply = ""
                        if response.function_calls:
                            for function_call in response.function_calls:
                                tool_name = function_call.name
                                tool_args = function_call.args

                                st.caption(f"🔧 Tool Executed: `{tool_name}`")

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
                                    model="gemini-3.6-flash", contents=followup_prompt
                                )
                                final_reply = final_response.text
                        else:
                            final_reply = response.text

                        st.markdown(final_reply)
                        st.session_state.messages.append({"role": "assistant", "content": final_reply})

                    except Exception as e:
                        st.error(f"Error: {e}")
