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
    page_title="Enterprise AI Assistant with Smart Review",
    page_icon="⭐",
    layout="centered",
)

st.title("🔐 Enterprise AI Assistant (Portal)")

# 2. Sidebar - Role Selection & Secure Login System
st.sidebar.header("👤 User Authentication")
role = st.sidebar.selectbox("Select Role", ["Customer", "Owner / Admin"])

# Initialize Session States for Login & OTP Workflow
if "logged_in_user" not in st.session_state:
  st.session_state.logged_in_user = None
if "user_role" not in st.session_state:
  st.session_state.user_role = None
if "password_verified" not in st.session_state:
  st.session_state.password_verified = False
if "otp_sent" not in st.session_state:
  st.session_state.otp_sent = False
if "generated_otp" not in st.session_state:
  st.session_state.generated_otp = None


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
          st.sidebar.success("✅ Password correct! Now enter your mobile number.")
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
          st.sidebar.warning(
              "⚠️ Please enter a valid 10-digit mobile number."
          )

    elif st.session_state.otp_sent:
      entered_otp = st.sidebar.text_input(
          "3. Enter 6-digit OTP:", max_chars=6, type="password", key="owner_otp_input"
      )
      if st.sidebar.button("Confirm OTP & Login"):
        if entered_otp == st.session_state.generated_otp:
          st.session_state.logged_in_user = "Owner"
          st.session_state.user_role = "Owner"
          st.session_state.password_verified = False
          st.session_state.otp_sent = False
          st.sidebar.success("✅ Owner Login Successful!")
          st.rerun()
        else:
          st.sidebar.error("❌ Invalid OTP. Please try again.")

  if st.session_state.user_role == "Owner":
    st.sidebar.markdown("---")
    st.sidebar.subheader("📊 Owner Dashboard Controls")
    if st.sidebar.button("Logout"):
      st.session_state.logged_in_user = None
      st.session_state.user_role = None
      st.session_state.password_verified = False
      st.session_state.otp_sent = False
      st.rerun()

# --- CUSTOMER LOGIN FLOW ---
else:
  st.sidebar.subheader("🛍️ Customer Login")
  customer_name_input = st.sidebar.text_input("Enter Your Name:")

  if st.sidebar.button("Login as Customer"):
    if customer_name_input.strip():
      st.session_state.logged_in_user = customer_name_input.strip()
      st.session_state.user_role = "Customer"
      st.sidebar.success(f"✅ Welcome, {customer_name_input}!")
    else:
      st.sidebar.warning("⚠️ Please enter your name to login.")

  if st.session_state.user_role == "Customer":
    st.sidebar.write(
        f"Logged in as: **{st.session_state.logged_in_user}**"
    )
    if st.sidebar.button("Logout"):
      st.session_state.logged_in_user = None
      st.session_state.user_role = None
      st.rerun()

# Stop execution if not logged in
if not st.session_state.logged_in_user:
  st.warning("⚠️ Please login using the sidebar to access the application.")
  st.stop()


# 3. Gemini API Configuration & Database Setup
db_path = "./chroma_db"

try:
  api_key_input = st.secrets["GOOGLE_API_KEY"]
  client = genai.Client(api_key=api_key_input)
  chroma_client = chromadb.PersistentClient(path=db_path)
  collection = chroma_client.get_or_create_collection(
      name="my_inventory_library"
  )
except Exception as e:
  st.error(
      f"Error connecting to Database or API Key missing in Secrets: {e}"
  )
  st.stop()


# Load inventory.csv automatically
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


# 4. Define Tools (Search, Book, Pay, Review)
def search_knowledge_base(query: str) -> str:
  """Search inventory data, stock details, and products from the vector database."""
  try:
    results = collection.query(query_texts=[query], n_results=1)
    if results["documents"] and len(results["documents"][0]) > 0:
      return results["documents"][0][0]
    return "No relevant information found."
  except Exception as e:
    return f"Error during search: {e}"


def book_home_delivery(service_type: str, address: str = "Not Provided") -> str:
  """Book a home delivery service or order for products."""
  customer_name = st.session_state.logged_in_user
  st.session_state.last_booked_item = service_type
  timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

  file_exists = os.path.isfile("orders.csv")
  with open("orders.csv", mode="a", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    if not file_exists:
      writer.writerow(["Timestamp", "Customer Name", "Item", "Address"])
    writer.writerow([timestamp, customer_name, service_type, address])

  return (
      f"Success! {customer_name}, your order for {service_type} is successfully"
      " scheduled. Please provide your review and rating from 1 to 5 stars for"
      " this item."
  )


def calculate_total_price(
    price: float, quantity: int, discount_percentage: float = 0.0
) -> str:
  """Calculate the total price including quantity and optional discount."""
  subtotal = price * quantity
  discount_amount = subtotal * (discount_percentage / 100)
  final_total = subtotal - discount_amount
  return (
      f"Calculation Result: Subtotal = ₹{subtotal}, Discount ="
      f" ₹{discount_amount}, Final Total = ₹{final_total}"
  )


def process_payment(amount: float, payment_method: str) -> str:
  """Process payment for the order."""
  item = st.session_state.get("last_booked_item", "General Product")
  customer_name = st.session_state.logged_in_user
  timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
  txn_id = "TXN" + datetime.now().strftime("%Y%m%d%H%M%S")

  file_exists = os.path.isfile("payments.csv")
  with open("payments.csv", mode="a", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    if not file_exists:
      writer.writerow(
          [
              "Timestamp",
              "Customer Name",
              "Item",
              "Amount",
              "Method",
              "Transaction ID",
          ]
      )
    writer.writerow(
        [timestamp, customer_name, item, amount, payment_method, txn_id]
    )

  return (
      f"Payment of ₹{amount} via {payment_method} processed successfully for"
      f" {customer_name}! Transaction ID: {txn_id}."
  )


def add_product_review(rating: int, review_comment: str) -> str:
  """Submit a product review and rating (1 to 5) and say thanks."""
  item = st.session_state.get("last_booked_item", "General Product")
  customer_name = st.session_state.logged_in_user
  timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

  file_exists = os.path.isfile("reviews.csv")
  with open("reviews.csv", mode="a", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    if not file_exists:
      writer.writerow(["Timestamp", "Customer Name", "Product", "Rating", "Comment"])
    writer.writerow([timestamp, customer_name, item, rating, review_comment])

  return (
      f"Thank you so much, {customer_name}! Your review ({rating}/5 stars) for"
      f" '{item}' has been saved successfully. We truly appreciate your"
      " feedback!"
  )


# 5. Interface based on Role
if st.session_state.user_role == "Owner":
  st.subheader("👑 Owner Admin Dashboard")
  st.write("Secure login verified.")

  col1, col2 = st.columns(2)
  with col1:
    st.markdown("### 📦 All Customer Orders")
    if os.path.exists("orders.csv"):
      st.dataframe(pd.read_csv("orders.csv"), hide_index=True)
    else:
      st.info("No orders found yet.")

  with col2:
    st.markdown("### 💳 Payment Records")
    if os.path.exists("payments.csv"):
      st.dataframe(pd.read_csv("payments.csv"), hide_index=True)
    else:
      st.info("No payments found yet.")

  st.markdown("---")
  st.markdown("### ⭐ Customer Reviews & Feedback")
  if os.path.exists("reviews.csv"):
    st.dataframe(pd.read_csv("reviews.csv"), hide_index=True)
  else:
    st.info("No reviews found yet.")

else:
  st.write(
      f"Welcome, **{st.session_state.logged_in_user}**! You can search products,"
      " place orders, make payments, and write reviews here."
  )

  if "messages" not in st.session_state:
    st.session_state.messages = []
  if "last_booked_item" not in st.session_state:
    st.session_state.last_booked_item = None

  for message in st.session_state.messages:
    with st.chat_message(message["role"]):
      st.markdown(message["content"])

  if user_prompt := st.chat_input(
      "Type your question or request here (Supports all languages)..."
  ):
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
      st.markdown(user_prompt)

    with st.chat_message("assistant"):
      with st.spinner("AI Agent is thinking..."):
        try:
          context_memory = (
              f" [Context - User: {st.session_state.logged_in_user}, Last item:"
              f" {st.session_state.last_booked_item}]"
          )
          full_prompt = user_prompt + context_memory

          response = client.models.generate_content(
              model="gemini-3.5-flash-lite",  # <--- ஸ்கிரீன்ஷாட்டில் உள்ள சரியான மாடல் பெயர்
              contents=full_prompt,
              config=types.GenerateContentConfig(
                  tools=[
                      search_knowledge_base,
                      book_home_delivery,
                      calculate_total_price,
                      process_payment,
                      add_product_review,
                  ],
                  temperature=0.3,
                  system_instruction=(
                      "You are an advanced multi-lingual enterprise AI"
                      " assistant. 1. Detect user language and ALWAYS respond"
                      " in that same language. 2. Use tools accurately. 3."
                      " REVIEW RULE: Immediately after booking a home"
                      " delivery, automatically ask the customer to provide a"
                      " rating from 1 to 5 stars and a review comment. 4. THANK"
                      " YOU RULE: When the customer provides their"
                      " rating/review, use the 'add_product_review' tool and"
                      " warmly say thanks to the customer."
                  ),
              ),
          )

          final_reply = ""
          if response.function_calls:
            for function_call in response.function_calls:
              tool_name = function_call.name
              tool_args = function_call.args

              st.caption(f"🔧 Executing Tool: `{tool_name}`")

              if tool_name == "search_knowledge_base":
                tool_result = search_knowledge_base(**tool_args)
              elif tool_name == "book_home_delivery":
                tool_result = book_home_delivery(**tool_args)
              elif tool_name == "calculate_total_price":
                tool_result = calculate_total_price(**tool_args)
              elif tool_name == "process_payment":
                tool_result = process_payment(**tool_args)
              elif tool_name == "add_product_review":
                tool_result = add_product_review(**tool_args)
              else:
                tool_result = "Tool not found."

              followup_prompt = (
                  f"The tool '{tool_name}' returned: '{tool_result}'. Now"
                  f" answer user request: '{user_prompt}' in the user's"
                  " language naturally."
              )
              final_response = client.models.generate_content(
                  model="gemini-3.5-flash-lite", contents=followup_prompt
              )
              final_reply = final_response.text
          else:
            final_reply = response.text

          st.markdown(final_reply)
          st.session_state.messages.append(
              {"role": "assistant", "content": final_reply}
          )

        except Exception as e:
          st.error(f"Error: {e}")
