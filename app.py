from datetime import datetime
import pandas as pd
import requests
import streamlit as st


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="HM Mobiles",
    page_icon="📱",
    layout="wide"
)


# ============================================================
# CSS (VIBRANT, PROFESSIONAL, ZERO-GAP STYLING)
# ============================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
}

#MainMenu {visibility: hidden;}
header {visibility: hidden;}
footer {visibility: hidden;}
div[data-testid="stToolbar"] {display: none !important;}
section[data-testid="stStatusWidget"] {display: none !important;}


/* ============================================================
   CONTAINER & GAP ELIMINATION
   ============================================================ */

.stMainBlockContainer,
div[data-testid="stMainBlockContainer"],
.block-container {
    padding-top: 0rem !important;
    margin-top: 0rem !important;
    padding-left: 0.3rem !important;
    padding-right: 0.3rem !important;
    padding-bottom: 1rem !important;
    max-width: 100% !important;
}

label, .stTextInput label, p {
    font-weight: 600 !important;
}


/* ============================================================
   VIBRANT COLORFUL HEADER BANNER
   ============================================================ */

.brand-banner {
    background: linear-gradient(135deg, #6366f1 0%, #a855f7 50%, #ec4899 100%);
    padding: 3px 6px;
    border-radius: 6px;
    text-align: center;
    margin: 0 0 2px 0 !important;
    box-shadow: 0 2px 4px rgba(168, 85, 247, 0.25);
}

.brand-title {
    color: white !important;
    font-size: 12px !important;
    font-weight: 800 !important;
    letter-spacing: 0.8px;
    margin: 0 !important;
    padding: 0 !important;
    line-height: 1.1 !important;
    text-shadow: 0 1px 2px rgba(0,0,0,0.15);
}


/* ============================================================
   STORE + CART (SIDE BY SIDE COMPACT COLORFUL BOX)
   ============================================================ */

.hm-nav-box {
    width: 170px !important;
    max-width: 170px !important;
    margin: 1px auto 3px auto !important;
    padding: 0 !important;
    border: none !important;
    background: transparent !important;
    box-shadow: none !important;
}

.hm-nav-box [data-testid="stRadio"] {
    margin: 0 !important;
    padding: 0 !important;
    width: 100% !important;
}

.hm-nav-box [data-testid="stRadio"] > div {
    display: flex !important;
    flex-direction: row !important;
    flex-wrap: nowrap !important;
    gap: 4px !important;
    justify-content: center !important;
    align-items: center !important;
}

.hm-nav-box [data-testid="stRadio"] > div > label {
    flex: 1 1 0 !important;
    width: 50% !important;
    max-width: 50% !important;
    min-width: 0 !important;
    height: 24px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    padding: 0 2px !important;
    margin: 0 !important;
    border: 1.5px solid #a855f7 !important;
    border-radius: 5px !important;
    background: #fdf4ff !important;
    box-sizing: border-box !important;
    transition: all 0.2s ease;
}

.hm-nav-box [data-testid="stRadio"] > div > label > div:first-child {
    display: none !important;
}

.hm-nav-box [data-testid="stRadio"] > div > label p {
    color: #9333ea !important;
    font-size: 10px !important;
    font-weight: 700 !important;
    margin: 0 !important;
    padding: 0 !important;
    white-space: nowrap !important;
}

.hm-nav-box [data-testid="stRadio"] > div > label:has(input:checked) {
    background: linear-gradient(135deg, #8b5cf6 0%, #ec4899 100%) !important;
    border-color: #7c3aed !important;
    box-shadow: 0 1px 3px rgba(236, 72, 153, 0.3);
}

.hm-nav-box [data-testid="stRadio"] > div > label:has(input:checked) p {
    color: white !important;
}


/* ============================================================
   CATEGORY SELECTOR
   ============================================================ */

.category-area {
    margin-top: 0 !important;
    margin-bottom: 2px !important;
}

.category-area div[data-baseweb="select"] > div {
    min-height: 24px !important;
    padding-top: 0px !important;
    padding-bottom: 0px !important;
    border-color: #cbd5e1 !important;
    background-color: #f8fafc !important;
}


/* ============================================================
   PRODUCT CARD
   ============================================================ */

.product-card {
    width: 100%;
    border: 1.5px solid #e2e8f0;
    border-radius: 6px;
    padding: 3px 4px;
    margin-bottom: 3px;
    box-sizing: border-box;
    background: white;
    box-shadow: 0 1px 3px rgba(0,0,0,0.03);
}


/* ============================================================
   PRODUCT INFORMATION
   ============================================================ */

.product-name {
    text-align: center;
    font-size: 10px;
    font-weight: 700;
    color: #1e293b;
    margin-top: 1px;
    margin-bottom: 0px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.product-price {
    text-align: center;
    font-size: 9px;
    font-weight: 700;
    color: #059669;
    margin-bottom: 1px;
}


/* ============================================================
   FORM CONTROLS & BUTTONS STYLING
   ============================================================ */

div[data-baseweb="input"] input {
    height: 20px !important;
    min-height: 20px !important;
    padding-top: 0px !important;
    padding-bottom: 0px !important;
    font-size: 10px !important;
}

div.stButton > button {
    background: linear-gradient(135deg, #6366f1 0%, #ec4899 100%) !important;
    color: white !important;
    border: none !important;
    font-weight: 700 !important;
    padding-top: 0.02rem !important;
    padding-bottom: 0.02rem !important;
    min-height: 21px !important;
    font-size: 9px !important;
    border-radius: 4px !important;
    box-shadow: 0 1px 2px rgba(99, 102, 241, 0.2);
}

div.stButton > button:hover {
    background: linear-gradient(135deg, #4f46e5 0%, #db2777 100%) !important;
    color: white !important;
    box-shadow: 0 2px 4px rgba(219, 39, 119, 0.3);
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# SESSION STATES
# ============================================================

if "logged_in_user" not in st.session_state:
    st.session_state.logged_in_user = None

if "user_phone" not in st.session_state:
    st.session_state.user_phone = None

if "cart" not in st.session_state:
    st.session_state.cart = []

if "current_view" not in st.session_state:
    st.session_state.current_view = "Home"


# ============================================================
# GOOGLE SCRIPT
# ============================================================

GOOGLE_SCRIPT_URL = (
    "https://script.google.com/macros/s/"
    "AKfycbzq1vB7RSGZA8aM5QOOxpSKxN06vEpYs14Yupx687pWZ4KNa0bkvAEO12QJQZ_v88DT/"
    "exec"
)


def log_login_to_sheet(name, phone):
    try:
        payload = {
            "Type": "Login",
            "Customer_Name": name,
            "Primary_Phone": phone
        }
        requests.post(
            GOOGLE_SCRIPT_URL,
            json=payload,
            timeout=3
        )
    except Exception:
        pass


# ============================================================
# LOGIN PAGE
# ============================================================

if not st.session_state.logged_in_user:
    st.markdown("""
        <div class="brand-banner">
            <div class="brand-title">HM MOBILES</div>
        </div>
    """, unsafe_allow_html=True)

    _, mid_col, _ = st.columns([1, 2, 1])

    with mid_col:
        with st.form("login_form"):
            st.markdown("### Customer Portal Login")

            cust_name = st.text_input("Your Name:")
            cust_phone = st.text_input("Mobile Number (10 digits):", max_chars=10)

            login_btn = st.form_submit_button("Secure Login", use_container_width=True)

            if login_btn:
                if cust_name.strip() and len(cust_phone) == 10 and cust_phone.isdigit():
                    st.session_state.logged_in_user = cust_name.strip()
                    st.session_state.user_phone = cust_phone.strip()
                    log_login_to_sheet(cust_name.strip(), cust_phone.strip())
                    st.rerun()
                else:
                    st.warning("⚠️ Enter a valid name and 10-digit mobile number.")

    st.stop()


# ============================================================
# HEADER
# ============================================================

st.markdown('<div class="sticky-header-container">', unsafe_allow_html=True)

st.markdown("""
    <div class="brand-banner">
        <div class="brand-title">HM MOBILES</div>
    </div>
""", unsafe_allow_html=True)


# ============================================================
# STORE / CART
# ============================================================

st.markdown('<div class="hm-nav-box">', unsafe_allow_html=True)

nav_choice = st.radio(
    "Navigation",
    ["Store", f"Cart({len(st.session_state.cart)})"],
    index=0 if st.session_state.current_view == "Home" else 1,
    horizontal=True,
    label_visibility="collapsed",
    key="hm_navigation"
)

new_view = "Home" if nav_choice == "Store" else "Cart"

if st.session_state.current_view != new_view:
    st.session_state.current_view = new_view
    st.rerun()

st.markdown("</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)


# ============================================================
# LOAD INVENTORY FROM GOOGLE SHEET
# ============================================================

@st.cache_data(ttl=0)
def load_inventory_from_sheet():
    sheet_csv_url = (
        "https://docs.google.com/spreadsheets/d/"
        "1zXy8vwQtv2h5PooBLLEfVHAI_-aNBJK2K44kEMvczLQ/"
        "export?format=csv"
    )
    try:
        df = pd.read_csv(sheet_csv_url)
        return df
    except Exception:
        return pd.DataFrame()


inv_df = load_inventory_from_sheet()
product_records = []


# ============================================================
# READ PRODUCT DATA
# ============================================================

if not inv_df.empty:
    try:
        for _, row in inv_df.iterrows():
            raw_img = str(row.iloc[6]).strip() if len(row) > 6 and pd.notna(row.iloc[6]) else ""
            img_list = [img.strip() for img in raw_img.replace(",", "\n").split("\n") if img.strip() and img.strip().lower() != "nan"]

            product_records.append({
                "id": str(row.iloc[0]) if len(row) > 0 and pd.notna(row.iloc[0]) else "N/A",
                "name": str(row.iloc[1]) if len(row) > 1 and pd.notna(row.iloc[1]) else "Unknown",
                "category": str(row.iloc[2]).strip() if len(row) > 2 and pd.notna(row.iloc[2]) else "General",
                "stock": str(row.iloc[3]) if len(row) > 3 and pd.notna(row.iloc[3]) else "0",
                "price": str(row.iloc[4]) if len(row) > 4 and pd.notna(row.iloc[4]) else "0",
                "description": str(row.iloc[5]).strip() if len(row) > 5 and pd.notna(row.iloc[5]) else "",
                "images": img_list
            })
    except Exception as e:
        print(f"Parsing error: {e}")


# ============================================================
# DEFAULT PRODUCT
# ============================================================

if not product_records:
    product_records = [{
        "id": "ITM001",
        "name": "Bluetooth Wireless Headset",
        "price": "1200",
        "stock": "50",
        "category": "Headset",
        "images": [],
        "description": "High performance audio"
    }]


# ============================================================
# STORE (2-COLUMN GRID)
# ============================================================

if st.session_state.current_view == "Home":

    categories = sorted(list(set([p["category"] for p in product_records])))

    st.markdown('<div class="category-area">', unsafe_allow_html=True)
    selected_cat = st.selectbox("Select Product Category:", categories, key="category_selector")
    st.markdown("</div>", unsafe_allow_html=True)

    filtered_items = [
        p for p in product_records
        if p["category"].strip().lower() == selected_cat.strip().lower()
    ]

    if filtered_items:
        for i in range(0, len(filtered_items), 2):
            cols = st.columns(2)

            for col_idx in range(2):
                item_index = i + col_idx
                if item_index < len(filtered_items):
                    prod = filtered_items[item_index]

                    with cols[col_idx]:
                        st.markdown('<div class="product-card">', unsafe_allow_html=True)

                        left_col, image_col, right_col = st.columns([0.3, 5, 0.3], vertical_alignment="center")

                        img_key = f"img_idx_{selected_cat}_{item_index}"
                        if img_key not in st.session_state:
                            st.session_state[img_key] = 0

                        total_imgs = len(prod["images"])

                        with left_col:
                            if st.button("◀", key=f"prev_{selected_cat}_{item_index}"):
                                if total_imgs > 0:
                                    st.session_state[img_key] = (st.session_state[img_key] - 1) % total_imgs
                                    st.rerun()

                        with image_col:
                            if total_imgs > 0:
                                current_idx = st.session_state[img_key] % total_imgs
                                try:
                                    st.image(prod["images"][current_idx], use_container_width=True)
                                except Exception:
                                    pass  # Silently bypass broken link rendering errors
                            else:
                                pass  # Skip rendering if no valid image is provided

                        with right_col:
                            if st.button("▶", key=f"next_{selected_cat}_{item_index}"):
                                if total_imgs > 0:
                                    st.session_state[img_key] = (st.session_state[img_key] + 1) % total_imgs
                                    st.rerun()

                        st.markdown(f'<div class="product-name">{prod["name"]}</div>', unsafe_allow_html=True)
                        st.markdown(f'<div class="product-price">₹{prod["price"]} | Stk: {prod["stock"]}</div>', unsafe_allow_html=True)

                        q_val = st.number_input(
                            "Quantity", min_value=1.0, value=1.0, step=1.0,
                            key=f"qty_{selected_cat}_{item_index}", label_visibility="collapsed"
                        )

                        if st.button("Add to Cart", key=f"add_{selected_cat}_{item_index}", use_container_width=True):
                            st.session_state.cart.append({
                                "product": prod["name"],
                                "quantity": f"{int(q_val)} Units"
                            })
                            st.success("Added!")
                            st.rerun()

                        st.markdown('</div>', unsafe_allow_html=True)

    else:
        st.info(f"No items found under category '{selected_cat}'.")


# ============================================================
# CART
# ============================================================

else:
    st.subheader("🛒 Shopping Cart & Checkout")

    if st.session_state.cart:
        for i, item in enumerate(st.session_state.cart):
            col_item_name, col_item_remove = st.columns([3, 1])

            with col_item_name:
                st.write(f"• {item['product']} ({item['quantity']})")

            with col_item_remove:
                if st.button("Remove", key=f"remove_cart_{i}"):
                    st.session_state.cart.pop(i)
                    st.rerun()

        st.markdown("---")

        with st.form("checkout_form"):
            address = st.text_area("Delivery Address:")
            sec_phone = st.text_input("Alternative Phone Number:", max_chars=10)
            pay_method = st.selectbox("Payment Gateway", ["UPI / GPay", "Cash on Delivery"])

            checkout_button = st.form_submit_button("Confirm & Dispatch Order", use_container_width=True)

            if checkout_button:
                if address.strip() and len(sec_phone) == 10 and sec_phone.isdigit():
                    try:
                        order_payload = {
                            "Type": "Order",
                            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "Customer_Name": st.session_state.logged_in_user,
                            "Primary_Phone": st.session_state.user_phone,
                            "Items": str(st.session_state.cart),
                            "Address": address.strip(),
                            "Secondary_Phone": sec_phone.strip(),
                            "Payment_Method": pay_method
                        }
                        requests.post(GOOGLE_SCRIPT_URL, json=order_payload, timeout=5)
                    except Exception:
                        pass

                    st.success("🎉 Order successfully placed and synced with Google Sheets!")
                    st.session_state.cart = []
                    st.session_state.current_view = "Home"
                    st.rerun()
                else:
                    st.error("Please provide a delivery address and valid 10-digit alternative phone.")
    else:
        st.info("Your cart is empty.")
