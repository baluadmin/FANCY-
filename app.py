from datetime import datetime
import csv
import os

import pandas as pd
import requests
import streamlit as st


# ============================================================
# HM MOBILES THIRUVERKADU
# ONE RESPONSIVE LAYOUT FOR DESKTOP + MOBILE
# ============================================================

st.set_page_config(
    page_title="HM Mobiles Thiruverkadu",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ============================================================
# RESPONSIVE CSS
# ============================================================

st.markdown(
    """
    <style>
    * { box-sizing: border-box !important; }

    html, body, [data-testid="stApp"], [data-testid="stAppViewContainer"],
    [data-testid="stMain"], [data-testid="stMainBlockContainer"] {
        width: 100% !important;
        max-width: 100% !important;
        min-width: 0 !important;
        overflow-x: hidden !important;
    }

    .block-container {
        width: 100% !important;
        max-width: 100% !important;
        margin: 0 !important;
        padding: 10px 12px 24px !important;
    }

    #MainMenu, header, footer, div[data-testid="stToolbar"],
    section[data-testid="stStatusWidget"], div[data-testid="stDecoration"],
    div[class*="viewerBadge"] { display: none !important; }

    div[data-testid="stHorizontalBlock"] {
        width: 100% !important;
        max-width: 100% !important;
        min-width: 0 !important;
        flex-wrap: nowrap !important;
    }
    div[data-testid="stHorizontalBlock"] > div[data-testid="column"] {
        min-width: 0 !important;
        max-width: 100% !important;
    }

    /* LOGIN */
    .hm-login-title { text-align:center !important; margin:12px auto 16px !important; }
    .hm-login-title h1 { margin:0 !important; font-size:32px !important; line-height:1.15 !important; }
    .hm-login-title p { margin:5px 0 0 !important; font-size:13px !important; }
    div[data-testid="stForm"] { width:min(430px,100%) !important; max-width:430px !important; margin:auto !important; }

    input, textarea, div[data-baseweb="select"] > div { max-width:100% !important; min-width:0 !important; }

    /* HEADER */
    .hm-brand {
        width:100% !important;
        min-height:0 !important;
        display:flex !important; align-items:center !important; justify-content:center !important;
        padding:20px 12px !important; margin:0 0 8px !important;
        background:#dff1ff !important; border:1px solid #69b9f4 !important; border-radius:7px !important;
    }
    .hm-brand-title {
        width:100% !important; color:#071b35 !important; text-align:center !important;
        font-size:34px !important; line-height:1.35 !important; font-weight:400 !important;
        overflow-wrap:normal !important;
    }

    /* NAV */
    .hm-nav { width:100% !important; overflow:hidden !important; }
    .hm-nav div[data-testid="stHorizontalBlock"] { gap:10px !important; align-items:center !important; }
    .hm-nav div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:first-child { flex:1 1 auto !important; width:auto !important; }
    .hm-nav div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:not(:first-child) { flex:0 0 auto !important; width:auto !important; }
    .hm-nav p { margin:0 !important; font-size:11px !important; white-space:nowrap !important; }
    .hm-nav div.stButton > button { min-width:68px !important; min-height:36px !important; padding:5px 10px !important; font-size:11px !important; white-space:nowrap !important; }

    /* CATEGORY BAR */
    .hm-category-bar { width:100% !important; overflow:hidden !important; }
    .hm-category-bar div[data-testid="stHorizontalBlock"] { gap:14px !important; margin-bottom:0 !important; }
    .hm-category-bar div[data-testid="stHorizontalBlock"] > div[data-testid="column"] { flex:1 1 0 !important; width:0 !important; overflow:hidden !important; }
    .hm-category-bar div.stButton > button {
        width:100% !important; min-width:0 !important; min-height:51px !important;
        padding:6px 5px !important; font-size:11px !important; line-height:1.25 !important;
        white-space:normal !important;
    }
    .hm-divider { border-top:1px solid #d7d7d7 !important; margin:20px 0 11px !important; width:100% !important; }
    .hm-category-title { font-size:14px !important; font-weight:600 !important; margin:0 0 17px !important; }

    /* PRODUCT CARD */
    .hm-product-card {
        width:100% !important; max-width:100% !important; min-width:0 !important; overflow:hidden !important;
        border:1px solid #d5d5d5 !important; border-radius:8px !important;
        padding:14px !important; margin:0 0 14px !important; background:#fff !important;
    }
    .hm-product-card div[data-testid="stHorizontalBlock"] { gap:8px !important; flex-wrap:nowrap !important; }
    .hm-product-card img {
        width:100% !important; max-width:100% !important; height:auto !important;
        max-height:105px !important; object-fit:contain !important; display:block !important;
    }
    .hm-no-image { height:105px !important; display:flex !important; align-items:center !important; justify-content:center !important; color:#888 !important; font-size:12px !important; }
    .hm-card-divider { border-top:1px solid #d8d8d8 !important; margin:13px 0 11px !important; width:100% !important; }
    .hm-product-name { font-size:14px !important; line-height:1.25 !important; font-weight:500 !important; margin:0 0 16px !important; color:#101010 !important; }
    .hm-product-price { font-size:14px !important; line-height:1.2 !important; margin:0 0 18px !important; color:#101010 !important; }
    .hm-product-description { font-size:11px !important; line-height:1.3 !important; color:#888 !important; min-height:28px !important; margin:0 0 9px !important; overflow-wrap:anywhere !important; }
    .hm-product-card .stNumberInput, .hm-product-card .stButton { width:100% !important; max-width:100% !important; }
    .hm-product-card input { min-width:0 !important; width:100% !important; min-height:36px !important; font-size:11px !important; }
    .hm-product-card div.stButton > button { width:100% !important; min-height:36px !important; font-size:11px !important; padding:5px 8px !important; }
    .hm-product-card [data-testid="stVerticalBlock"] { gap:.35rem !important; }

    /* CART */
    .hm-cart { width:100% !important; max-width:100% !important; overflow:hidden !important; }

    /* PHONE */
    @media (max-width:600px) {
        .block-container { max-width:100% !important; width:100% !important; padding:8px 7px 20px !important; }
        .hm-brand { min-height:0 !important; padding:18px 10px !important; }
        .hm-brand-title { font-size:32px !important; line-height:1.35 !important; }
        .hm-nav { width:100% !important; max-width:100% !important; overflow:visible !important; }
        .hm-nav div[data-testid="stHorizontalBlock"] { gap:6px !important; width:100% !important; overflow:visible !important; }
        .hm-nav div[data-testid="stHorizontalBlock"] > div[data-testid="column"] { min-width:0 !important; overflow:visible !important; }
        .hm-nav div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:first-child { flex:1 1 0 !important; width:0 !important; }
        .hm-nav div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:nth-child(2),
        .hm-nav div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:nth-child(3),
        .hm-nav div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:nth-child(4) { flex:0 0 22% !important; width:22% !important; }
        .hm-nav p { font-size:10px !important; }
        .hm-nav div.stButton > button { width:100% !important; min-width:0 !important; min-height:36px !important; padding:5px 4px !important; font-size:10px !important; }
        .hm-category-bar div[data-testid="stHorizontalBlock"] { gap:14px !important; }
        .hm-category-bar div.stButton > button { min-height:51px !important; font-size:11px !important; }
        .hm-divider { margin:20px 0 11px !important; }
        .hm-product-card { padding:13px !important; margin-bottom:14px !important; }
        .hm-product-card div[data-testid="stHorizontalBlock"] { gap:5px !important; }
        .hm-product-card img { max-height:100px !important; }
        .hm-product-name, .hm-product-price { font-size:14px !important; }
        .hm-product-description { font-size:11px !important; }
    }

    @media (max-width:380px) {
        .block-container { padding-left:6px !important; padding-right:6px !important; }
        .hm-brand { min-height:0 !important; }
        .hm-brand-title { font-size:28px !important; }
        .hm-nav div[data-testid="stHorizontalBlock"] { gap:5px !important; }
        .hm-nav div.stButton > button { min-width:0 !important; padding:5px 3px !important; font-size:9px !important; }
        .hm-category-bar div[data-testid="stHorizontalBlock"] { gap:7px !important; }
        .hm-category-bar div.stButton > button { font-size:10px !important; }
        .hm-product-card { padding:11px !important; }
        .hm-product-card img { max-height:88px !important; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# SESSION STATE
# ============================================================

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


# ============================================================
# GOOGLE APPS SCRIPT
# ============================================================

GOOGLE_SCRIPT_URL = (
    "https://script.google.com/macros/s/"
    "AKfycbzq1vB7RSGZA8aM5QOOxpSKxN06vEpYs14Yupx687pWZ4KNa0bkvAEO12QJQZ_v88DT"
    "/exec"
)


def log_login_to_sheet(name, phone):
    try:
        payload = {
            "Type": "Login",
            "Customer_Name": name,
            "Primary_Phone": phone,
        }
        requests.post(GOOGLE_SCRIPT_URL, json=payload, timeout=15)
    except Exception as e:
        print(f"Login sheet error: {e}")


# ============================================================
# LOGIN PAGE
# ============================================================

if not st.session_state.logged_in_user:

    st.markdown(
        """
        <div class="hm-login-title">
            <h1>HM MOBILES</h1>
            <p>Thiruverkadu - Premium Mobile Accessories & Service</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # NO st.columns() here.
    # The form automatically centers on desktop and fills the phone width.
    with st.form("customer_direct_login_center", border=True):

        st.markdown(
            "<h3 style='text-align:center; margin:0 0 10px 0;'>"
            "Customer Portal Login</h3>",
            unsafe_allow_html=True,
        )

        cust_name = st.text_input("Your Name:")

        cust_phone = st.text_input(
            "Mobile Number:",
            max_chars=10,
        )

        login_btn = st.form_submit_button(
            "Secure Login",
            use_container_width=True,
        )

        if login_btn:

            if (
                cust_name.strip()
                and len(cust_phone.strip()) == 10
                and cust_phone.strip().isdigit()
            ):
                st.session_state.logged_in_user = cust_name.strip()
                st.session_state.user_phone = cust_phone.strip()
                st.session_state.user_role = "Customer"
                st.session_state.selected_menu = "Headset"
                st.session_state.current_view = "Home"

                log_login_to_sheet(
                    cust_name.strip(),
                    cust_phone.strip(),
                )

                st.rerun()

            else:
                st.warning(
                    "⚠️ Please provide a valid name and 10-digit mobile number."
                )

    st.stop()


# ============================================================
# AFTER LOGIN - HEADER
# ============================================================

st.markdown(
    """
    <div class="hm-brand">
        <div class="hm-brand-title">HM MOBILES THIRUVERKADU</div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# HEADER NAVIGATION
# SAME HORIZONTAL ROW ON DESKTOP + MOBILE
# ============================================================

st.markdown('<div class="hm-nav">', unsafe_allow_html=True)

top_comm, top_home, top_cart, top_logout = st.columns(
    [2.4, 0.8, 0.9, 0.9],
    gap="small",
)

with top_comm:
    st.markdown(
        f"👋 Welcome, **{st.session_state.logged_in_user}**!"
    )

with top_home:
    if st.button(
        "Home",
        key="nav_home",
        use_container_width=True,
    ):
        st.session_state.current_view = "Home"
        st.rerun()

with top_cart:
    cart_count = len(st.session_state.cart)

    if st.button(
        f"Cart ({cart_count})",
        key="nav_cart",
        use_container_width=True,
    ):
        st.session_state.current_view = "Cart"
        st.rerun()

with top_logout:
    if st.button(
        "Logout",
        key="nav_logout",
        use_container_width=True,
    ):
        st.session_state.clear()
        st.rerun()

st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")


# ============================================================
# LOAD INVENTORY
# ============================================================

@st.cache_data(ttl=2)
def load_inventory_from_sheet():

    sheet_csv_url = (
        "https://docs.google.com/spreadsheets/d/"
        "1zXy8vwQtv2h5PooBLLEfVHAI_-aNBJK2K44kEMvczLQ"
        "/export?format=csv"
    )

    try:
        df = pd.read_csv(sheet_csv_url)
        df.to_csv("inventory.csv", index=False)
        return df

    except Exception as e:

        print(f"Inventory error: {e}")

        if os.path.exists("inventory.csv"):
            return pd.read_csv("inventory.csv")

        return pd.DataFrame()


inv_df = load_inventory_from_sheet()


# ============================================================
# PRODUCT RECORDS
# ============================================================

product_records = []

if not inv_df.empty:

    try:

        for _, row in inv_df.iterrows():

            product_records.append(
                {
                    "id": str(row.iloc[0]),
                    "name": str(row.iloc[1]),
                    "category": str(row.iloc[2]),
                    "stock": str(row.iloc[3]),
                    "price": str(row.iloc[4]),
                    "description": (
                        str(row.iloc[5]).strip()
                        if len(row) > 5 and pd.notna(row.iloc[5])
                        else ""
                    ),
                    "image": (
                        str(row.iloc[6]).strip()
                        if len(row) > 6 and pd.notna(row.iloc[6])
                        else ""
                    ),
                }
            )

    except Exception as e:

        print(f"Product parsing error: {e}")
        product_records = []


# ============================================================
# FALLBACK PRODUCTS
# ============================================================

if not product_records:

    product_records = [
        {
            "id": "ITM001",
            "name": "Bluetooth Wireless Headset",
            "price": "1200",
            "stock": "50",
            "category": "Headset",
            "image": (
                "images/Headset 1 1.jpg \\ "
                "images/Headset 1 2.jpg \\ "
                "images/Headset 1 3.jpg"
            ),
            "description": "Premium Bluetooth wireless headset.",
        },
        {
            "id": "ITM002",
            "name": "Over-Ear Gaming Headset",
            "price": "1800",
            "stock": "40",
            "category": "Headset",
            "image": "",
            "description": "Comfortable over-ear gaming headset.",
        },
        {
            "id": "ITM003",
            "name": "Fast Type-C Charger 33W",
            "price": "650",
            "stock": "120",
            "category": "Charger",
            "image": "",
            "description": "33W fast Type-C wall charger.",
        },
        {
            "id": "ITM004",
            "name": "Dual Port Fast Wall Charger",
            "price": "500",
            "stock": "90",
            "category": "Charger",
            "image": "",
            "description": "Dual-port fast charging adapter.",
        },
        {
            "id": "ITM005",
            "name": "Braided Micro USB Cable",
            "price": "250",
            "stock": "200",
            "category": "Cable",
            "image": "",
            "description": "Durable braided Micro USB cable.",
        },
        {
            "id": "ITM006",
            "name": "Type-C Fast Charging Cable",
            "price": "300",
            "stock": "150",
            "category": "Cable",
            "image": "",
            "description": "Fast charging Type-C cable.",
        },
        {
            "id": "ITM007",
            "name": "Professional Studio Mic",
            "price": "2500",
            "stock": "30",
            "category": "Mic",
            "image": "",
            "description": "Professional studio microphone.",
        },
        {
            "id": "ITM008",
            "name": "Mini Lavalier Clip-on Mic",
            "price": "450",
            "stock": "80",
            "category": "Mic",
            "image": "",
            "description": "Compact clip-on microphone.",
        },
        {
            "id": "ITM009",
            "name": "Lithium Mobile Replacement Battery",
            "price": "800",
            "stock": "45",
            "category": "Battery",
            "image": "",
            "description": "Mobile replacement battery.",
        },
        {
            "id": "ITM010",
            "name": "Edge-to-Edge Tempered Glass",
            "price": "200",
            "stock": "300",
            "category": "Tempered",
            "image": "",
            "description": "Full edge-to-edge tempered glass.",
        },
        {
            "id": "ITM011",
            "name": "Wireless Bluetooth Ear Pods",
            "price": "1500",
            "stock": "75",
            "category": "Ear pod",
            "image": "",
            "description": "Wireless Bluetooth ear pods.",
        },
    ]


# ============================================================
# CHECKOUT
# ============================================================

def process_cart_checkout(
    address: str,
    secondary_phone: str,
    description: str,
    payment_method: str,
    location_link: str,
) -> str:

    if not st.session_state.cart:
        return "Your cart is empty. Please add products first."

    customer_name = st.session_state.logged_in_user
    primary_phone = st.session_state.user_phone

    timestamp = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    txn_id = (
        "TXN"
        + datetime.now().strftime("%Y%m%d%H%M%S")
    )

    cart_summary = ", ".join(
        [
            f"{item['quantity']} of {item['product']}"
            for item in st.session_state.cart
        ]
    )

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
            "Live_Location": location_link,
        }

        requests.post(
            GOOGLE_SCRIPT_URL,
            json=order_data,
            timeout=15,
        )

    except Exception as e:

        print(f"Order sheet error: {e}")

    file_exists = os.path.isfile("orders.csv")

    with open(
        "orders.csv",
        mode="a",
        newline="",
        encoding="utf-8",
    ) as f:

        writer = csv.writer(f)

        if not file_exists:
            writer.writerow(
                [
                    "Timestamp",
                    "Customer Name",
                    "Primary Phone",
                    "Items",
                    "Address",
                    "Secondary Phone",
                    "Description",
                    "Live Location",
                ]
            )

        writer.writerow(
            [
                timestamp,
                customer_name,
                primary_phone,
                cart_summary,
                address,
                secondary_phone,
                description,
                location_link,
            ]
        )

    st.session_state.cart = []

    return (
        f"Checkout complete! Order placed for: "
        f"{cart_summary}. Payment via "
        f"{payment_method} successful "
        f"(TXN ID: {txn_id})."
    )


# ============================================================
# HOME - MOBILE SINGLE WINDOW LAYOUT
# ============================================================

if st.session_state.current_view == "Home":

    # ------------------------------------------------------------
    # CATEGORY BUTTONS - FULL WIDTH, ALWAYS INSIDE SCREEN
    # ------------------------------------------------------------
    st.markdown('<div class="hm-category-bar">', unsafe_allow_html=True)

    categories = list(
        dict.fromkeys(
            [p["category"] for p in product_records]
        )
    )

    if categories:
        # Use rows of three buttons so the categories never
        # create horizontal scrolling on a phone.
        for row_start in range(0, len(categories), 3):
            row_categories = categories[row_start:row_start + 3]
            cols = st.columns(3, gap="small")

            for col_idx, cat in enumerate(row_categories):
                with cols[col_idx]:
                    if st.button(
                        cat,
                        key=f"menu_btn_{cat}",
                        use_container_width=True,
                    ):
                        st.session_state.selected_menu = cat
                        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("<div class='hm-divider'></div>", unsafe_allow_html=True)

    # ------------------------------------------------------------
    # SELECTED CATEGORY
    # ------------------------------------------------------------
    current_cat = st.session_state.get(
        "selected_menu",
        categories[0] if categories else "Headset",
    )

    st.markdown(
        f'<div class="hm-category-title">Category: {current_cat}</div>',
        unsafe_allow_html=True,
    )

    filtered_items = [
        p for p in product_records
        if p["category"] == current_cat
    ]

    # ------------------------------------------------------------
    # PRODUCTS - ONE FULL-WIDTH CARD PER PRODUCT
    # ------------------------------------------------------------
    if filtered_items:
        for idx, prod in enumerate(filtered_items):

            slide_key = f"slide_{current_cat}_{idx}"
            if slide_key not in st.session_state:
                st.session_state[slide_key] = 0

            st.markdown('<div class="hm-product-card">', unsafe_allow_html=True)

            # ----------------------------------------------------
            # ALL PRODUCT IMAGES - 3 PER ROW
            # ----------------------------------------------------
            raw_img = prod.get("image", "")
            img_paths = []

            if raw_img:
                img_paths = [
                    img.strip()
                    for img in raw_img.replace("\\", ",").split(",")
                    if img.strip()
                ]

            valid_paths = [
                img for img in img_paths
                if os.path.exists(img)
            ]

            if valid_paths:
                image_cols = st.columns(3, gap="small")
                for image_idx, image_path in enumerate(valid_paths):
                    with image_cols[image_idx % 3]:
                        st.image(
                            image_path,
                            use_container_width=True,
                        )
            else:
                st.markdown(
                    '<div class="hm-no-image">No Image</div>',
                    unsafe_allow_html=True,
                )

            st.markdown('<div class="hm-card-divider"></div>', unsafe_allow_html=True)

            # ----------------------------------------------------
            # PRODUCT DETAILS
            # ----------------------------------------------------
            st.markdown(
                f'<div class="hm-product-name">{prod["name"]}</div>',
                unsafe_allow_html=True,
            )

            st.markdown(
                f'<div class="hm-product-price">₹{prod["price"]}</div>',
                unsafe_allow_html=True,
            )

            description = prod.get("description", "")
            if description:
                st.markdown(
                    f'<div class="hm-product-description">{description}</div>',
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    '<div class="hm-product-description">No description available.</div>',
                    unsafe_allow_html=True,
                )

            # ----------------------------------------------------
            # QUANTITY + ADD TO CART - SAME ROW
            # ----------------------------------------------------
            action_col, add_col = st.columns([1, 1.65], gap="small")

            with action_col:
                q_val = st.number_input(
                    "Qty",
                    min_value=1.0,
                    value=1.0,
                    step=1.0,
                    key=f"qty_{current_cat}_{idx}",
                    label_visibility="collapsed",
                )

            with add_col:
                if st.button(
                    "Add to Cart",
                    key=f"add_btn_{current_cat}_{idx}",
                    use_container_width=True,
                ):
                    full_q_str = f"{int(q_val)} Units"
                    st.session_state.cart.append(
                        {
                            "product": prod["name"],
                            "quantity": full_q_str,
                        }
                    )
                    st.success("Added to cart!")
                    st.rerun()

            st.markdown('</div>', unsafe_allow_html=True)

    else:
        st.info("No items found.")


# ============================================================
# CART / CHECKOUT
# ============================================================

else:

    st.subheader(
        "🛒 Your Shopping Cart & Checkout"
    )

    if st.session_state.cart:

        for c_idx, item in enumerate(
            st.session_state.cart
        ):

            cc1, cc2 = st.columns(
                [4, 1],
                gap="small",
            )

            with cc1:
                st.markdown(
                    f"- **{item['product']}** "
                    f"({item['quantity']})"
                )

            with cc2:

                if st.button(
                    "Remove",
                    key=f"rem_cart_view_{c_idx}",
                    use_container_width=True,
                ):

                    st.session_state.cart.pop(
                        c_idx
                    )

                    st.rerun()

        st.markdown("---")

        st.subheader(
            "📍 Secure Checkout Form"
        )

        with st.form(
            "checkout_form_main_view",
            border=True,
        ):

            checkout_address = st.text_area(
                "Delivery Address:"
            )

            secondary_phone = st.text_input(
                "Alternative Contact Number:",
                max_chars=10,
            )

            product_desc = st.text_area(
                "Product Specifications / "
                "Custom Description:"
            )

            payment_method = st.selectbox(
                "Payment Method",
                [
                    "UPI / GPay",
                    "Credit/Debit Card",
                    "Cash on Delivery",
                ],
            )

            live_location = st.text_input(
                "Live Location Link "
                "(Google Maps Share URL):"
            )

            submit_checkout = (
                st.form_submit_button(
                    "Complete Order & Pay"
                )
            )

            if submit_checkout:

                if (
                    checkout_address.strip()
                    and secondary_phone.strip()
                ):

                    result_msg = (
                        process_cart_checkout(
                            checkout_address,
                            secondary_phone,
                            product_desc,
                            payment_method,
                            live_location,
                        )
                    )

                    st.success(result_msg)

                    st.session_state.current_view = (
                        "Home"
                    )

                    st.rerun()

                else:

                    st.warning(
                        "⚠️ Please provide delivery "
                        "address and secondary contact "
                        "number."
                    )

    else:

        st.info(
            "Your cart is empty. Click **Home** "
            "above to browse and add products."
        )
