from datetime import datetime
import csv
import os

import pandas as pd
import requests
import streamlit as st


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="HM Mobiles Thiruverkadu",
    page_icon="📱",
    layout="centered",
    initial_sidebar_state="collapsed",
)


# ============================================================
# RESPONSIVE MOBILE-FIRST CSS
# ============================================================

st.markdown(
    """
    <style>

    /* ========================================================
       GLOBAL
       ======================================================== */

    @import url(
        'https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap'
    );

    html,
    body,
    [class*="css"] {
        font-family: "Poppins", sans-serif !important;
    }

    #MainMenu {
        visibility: hidden !important;
    }

    header {
        visibility: hidden !important;
    }

    footer {
        visibility: hidden !important;
    }

    div[data-testid="stToolbar"] {
        display: none !important;
    }

    section[data-testid="stStatusWidget"] {
        display: none !important;
    }

    div[data-testid="stDecoration"] {
        display: none !important;
    }

    div[class*="viewerBadge"] {
        display: none !important;
    }

    iframe[title="streamlit_app.manage"] {
        display: none !important;
    }

    .manage-app {
        display: none !important;
    }

    a.stMarkdownHeaderLink {
        display: none !important;
    }

    h1 svg,
    h2 svg,
    h3 svg,
    h4 svg,
    h5 svg,
    h6 svg {
        display: none !important;
    }


    /* ========================================================
       MAIN PAGE CONTAINER
       ======================================================== */

    .block-container {
        width: 100% !important;
        max-width: 1100px !important;

        padding-top: 0.45rem !important;
        padding-bottom: 0.5rem !important;
        padding-left: 0.6rem !important;
        padding-right: 0.6rem !important;

        margin: 0 auto !important;
    }


    /* ========================================================
       GENERAL TEXT
       ======================================================== */

    p,
    label,
    span,
    div[data-testid="stMarkdownContainer"] p {
        font-weight: 500;
    }


    /* ========================================================
       INPUTS
       ======================================================== */

    input,
    textarea,
    div[data-baseweb="select"] > div {
        background-color: var(--secondary-background-color) !important;
        color: var(--text-color) !important;

        border: 1px solid #cbd5e1 !important;
        border-radius: 7px !important;

        font-size: 14px !important;
        min-height: 38px !important;

        box-sizing: border-box !important;
    }


    /* ========================================================
       LOGIN PAGE
       ======================================================== */

    .hm-login-title {
        width: 100%;
        text-align: center;

        margin-top: 4px;
        margin-bottom: 12px;
    }

    .hm-login-title h1 {
        margin: 0 !important;

        font-size: 30px !important;
        line-height: 1.15 !important;

        font-weight: 700 !important;
        letter-spacing: 0.4px;
    }

    .hm-login-title p {
        margin: 5px 0 0 0 !important;

        font-size: 13px !important;
        line-height: 1.35 !important;
    }


    .login-box {
        width: 100%;
        max-width: 520px;

        margin: 0 auto;

        padding: 16px;

        box-sizing: border-box;

        border: 1px solid #cbd5e1;
        border-radius: 10px;

        background: var(--secondary-background-color);

        box-shadow: 0 3px 10px rgba(0, 0, 0, 0.05);
    }

    .login-heading {
        text-align: center;

        font-size: 18px !important;
        font-weight: 600 !important;

        margin: 0 0 12px 0 !important;
    }


    div[data-testid="stForm"] {
        border: none !important;
        padding: 0 !important;
        margin: 0 !important;
    }


    /* ========================================================
       FORM BUTTONS
       ======================================================== */

    div.stButton > button,
    button[kind="primaryFormSubmit"] {
        width: 100% !important;

        min-height: 38px !important;

        padding: 0.25rem 0.45rem !important;

        border-radius: 7px !important;

        background-color: #f1f5f9 !important;
        color: #1e293b !important;

        border: 1px solid #cbd5e1 !important;

        font-size: 13px !important;
        font-weight: 600 !important;

        white-space: nowrap !important;

        box-sizing: border-box !important;
    }

    div.stButton > button:hover,
    button[kind="primaryFormSubmit"]:hover {
        background-color: #e2e8f0 !important;
        border-color: #94a3b8 !important;
    }


    /* ========================================================
       AFTER LOGIN - BRAND
       ======================================================== */

    .brand-banner {
        width: 100%;

        padding: 7px 8px;

        margin-bottom: 6px;

        box-sizing: border-box;

        border-radius: 7px;

        border: 1px solid #bae6fd;

        background: #e0f2fe;

        text-align: center;
    }

    .brand-title {
        margin: 0 !important;

        font-size: 16px !important;
        line-height: 1.2 !important;

        font-weight: 700 !important;

        color: #0f172a !important;

        letter-spacing: 0.2px;
    }


    /* ========================================================
       TOP NAVIGATION
       ======================================================== */

    .mobile-welcome {
        font-size: 12px !important;

        line-height: 1.2 !important;

        margin: 0 !important;

        padding: 4px 0 !important;

        white-space: nowrap !important;

        overflow: hidden !important;
        text-overflow: ellipsis !important;
    }


    /* Keep navigation compact */
    div[data-testid="stHorizontalBlock"] {
        gap: 0.25rem !important;
    }

    div[data-testid="stHorizontalBlock"]
    > div[data-testid="column"] {
        padding-left: 2px !important;
        padding-right: 2px !important;
    }


    /* ========================================================
       DIVIDER
       ======================================================== */

    hr {
        margin-top: 5px !important;
        margin-bottom: 7px !important;

        border: none !important;
        border-top: 1px solid #d1d5db !important;
    }


    /* ========================================================
       SECTION TITLES
       ======================================================== */

    .section-title {
        font-size: 15px !important;

        font-weight: 600 !important;

        margin: 2px 0 5px 0 !important;
    }


    /* ========================================================
       MENU
       ======================================================== */

    .menu-title {
        font-size: 14px !important;
        font-weight: 600 !important;

        margin: 0 0 4px 0 !important;
    }


    /* ========================================================
       PRODUCT AREA
       ======================================================== */

    .product-name {
        font-size: 14px !important;

        line-height: 1.25 !important;

        font-weight: 600 !important;

        margin: 0 0 2px 0 !important;
    }

    .product-price {
        font-size: 14px !important;

        font-weight: 600 !important;

        margin: 0 0 4px 0 !important;
    }

    .product-description {
        font-size: 11px !important;

        line-height: 1.3 !important;

        margin: 0 !important;
    }


    /* Product image */
    img {
        max-width: 100% !important;
        height: auto !important;
    }


    /* ========================================================
       PRODUCT CONTAINER
       ======================================================== */

    div[data-testid="stVerticalBlockBorderWrapper"] {
        width: 100% !important;

        box-sizing: border-box !important;
    }


    /* ========================================================
       QUANTITY
       ======================================================== */

    [data-testid="stNumberInput"] input {
        font-size: 12px !important;

        min-height: 34px !important;
    }


    /* ========================================================
       CART
       ======================================================== */

    .cart-title {
        font-size: 17px !important;

        font-weight: 600 !important;

        margin: 0 0 6px 0 !important;
    }


    /* ========================================================
       SMALL MOBILE
       ======================================================== */

    @media (max-width: 600px) {

        .block-container {
            padding-left: 0.35rem !important;
            padding-right: 0.35rem !important;
            padding-top: 0.25rem !important;
        }

        .hm-login-title {
            margin-top: 2px !important;
            margin-bottom: 8px !important;
        }

        .hm-login-title h1 {
            font-size: 23px !important;
        }

        .hm-login-title p {
            font-size: 10px !important;
        }

        .login-box {
            padding: 10px !important;
            max-width: 100% !important;
        }

        .login-heading {
            font-size: 15px !important;
            margin-bottom: 8px !important;
        }

        .brand-title {
            font-size: 12px !important;
        }

        .brand-banner {
            padding: 5px 5px !important;
            margin-bottom: 4px !important;
        }

        .mobile-welcome {
            font-size: 9px !important;
        }

        div.stButton > button,
        button[kind="primaryFormSubmit"] {
            min-height: 32px !important;
            height: 32px !important;

            padding: 0.15rem 0.2rem !important;

            font-size: 9px !important;

            border-radius: 5px !important;
        }

        input,
        textarea,
        div[data-baseweb="select"] > div {
            font-size: 12px !important;
            min-height: 34px !important;
        }

        .section-title {
            font-size: 13px !important;
        }

        .menu-title {
            font-size: 12px !important;
        }

        .product-name {
            font-size: 12px !important;
        }

        .product-price {
            font-size: 12px !important;
        }

        .product-description {
            font-size: 9px !important;
        }
    }


    /* ========================================================
       VERY SMALL PHONES
       ======================================================== */

    @media (max-width: 380px) {

        .block-container {
            padding-left: 0.2rem !important;
            padding-right: 0.2rem !important;
        }

        .hm-login-title h1 {
            font-size: 21px !important;
        }

        .hm-login-title p {
            font-size: 9px !important;
        }

        .brand-title {
            font-size: 11px !important;
        }

        .mobile-welcome {
            font-size: 8px !important;
        }

        div.stButton > button,
        button[kind="primaryFormSubmit"] {
            font-size: 8px !important;

            min-height: 29px !important;
            height: 29px !important;
        }
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

        requests.post(
            GOOGLE_SCRIPT_URL,
            json=payload,
            timeout=15,
        )

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

    st.markdown(
        """
        <div class="login-box">
            <div class="login-heading">
                Customer Portal Login
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.form("customer_direct_login_center"):

        cust_name = st.text_input(
            "Your Name:",
            key="login_customer_name",
        )

        cust_phone = st.text_input(
            "Mobile Number:",
            max_chars=10,
            key="login_customer_phone",
        )

        login_btn = st.form_submit_button(
            "Secure Login",
            use_container_width=True,
        )

        if login_btn:

            clean_name = cust_name.strip()
            clean_phone = cust_phone.strip()

            if (
                clean_name
                and len(clean_phone) == 10
                and clean_phone.isdigit()
            ):

                st.session_state.logged_in_user = clean_name
                st.session_state.user_phone = clean_phone
                st.session_state.user_role = "Customer"

                st.session_state.selected_menu = "Headset"
                st.session_state.current_view = "Home"

                log_login_to_sheet(
                    clean_name,
                    clean_phone,
                )

                st.rerun()

            else:

                st.warning(
                    "⚠️ Please provide a valid name and 10-digit mobile number."
                )

    st.stop()


# ============================================================
# AFTER LOGIN - SMALL BRAND HEADER
# ============================================================

st.markdown(
    """
    <div class="brand-banner">
        <div class="brand-title">
            HM MOBILES THIRUVERKADU
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# AFTER LOGIN - NAVIGATION
# ============================================================

top_comm, top_home, top_cart, top_logout = st.columns(
    [2.4, 0.8, 0.9, 0.9],
    gap="small",
)


# ------------------------------------------------------------
# WELCOME
# ------------------------------------------------------------

with top_comm:

    st.markdown(
        f"""
        <div class="mobile-welcome">
            👋 Welcome,
            <b>{st.session_state.logged_in_user}</b>!
        </div>
        """,
        unsafe_allow_html=True,
    )


# ------------------------------------------------------------
# HOME
# ------------------------------------------------------------

with top_home:

    if st.button(
        "Home",
        key="nav_home",
        use_container_width=True,
    ):

        st.session_state.current_view = "Home"

        st.rerun()


# ------------------------------------------------------------
# CART
# ------------------------------------------------------------

with top_cart:

    cart_count = len(st.session_state.cart)

    if st.button(
        f"Cart ({cart_count})",
        key="nav_cart",
        use_container_width=True,
    ):

        st.session_state.current_view = "Cart"

        st.rerun()


# ------------------------------------------------------------
# LOGOUT
# ------------------------------------------------------------

with top_logout:

    if st.button(
        "Logout",
        key="nav_logout",
        use_container_width=True,
    ):

        st.session_state.clear()

        st.rerun()


st.markdown("---")


# ============================================================
# LOAD INVENTORY FROM GOOGLE SHEETS
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

        df.to_csv(
            "inventory.csv",
            index=False,
        )

        return df

    except Exception as e:

        print(f"Inventory loading error: {e}")

        if os.path.exists("inventory.csv"):

            try:
                return pd.read_csv("inventory.csv")
            except Exception:
                pass

        return pd.DataFrame()


# ============================================================
# BUILD PRODUCT RECORDS
# ============================================================

inv_df = load_inventory_from_sheet()

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
            "description": "ewdftgdsgdfgdfgfdg",
        },

        {
            "id": "ITM002",
            "name": "Over-Ear Gaming Headset",
            "price": "1800",
            "stock": "40",
            "category": "Headset",
            "image": "",
            "description": "ewdftgdsgdfgdfgfdg",
        },

        {
            "id": "ITM003",
            "name": "Fast Type-C Charger 33W",
            "price": "650",
            "stock": "120",
            "category": "Charger",
            "image": "",
            "description": "ewdftgdsgdfgdfgfdg",
        },

        {
            "id": "ITM004",
            "name": "Dual Port Fast Wall Charger",
            "price": "500",
            "stock": "90",
            "category": "Charger",
            "image": "",
            "description": "ewdftgdsgdfgdfgfdg",
        },

        {
            "id": "ITM005",
            "name": "Braided Micro USB Cable",
            "price": "250",
            "stock": "200",
            "category": "Cable",
            "image": "",
            "description": "ewdftgdsgdfgdfgfdg",
        },

        {
            "id": "ITM006",
            "name": "Type-C Fast Charging Cable",
            "price": "300",
            "stock": "150",
            "category": "Cable",
            "image": "",
            "description": "ewdftgdsgdfgdfgfdg",
        },

        {
            "id": "ITM007",
            "name": "Professional Studio Mic",
            "price": "2500",
            "stock": "30",
            "category": "Mic",
            "image": "",
            "description": "ewdftgdsgdfgdfgfdg",
        },

        {
            "id": "ITM008",
            "name": "Mini Lavalier Clip-on Mic",
            "price": "450",
            "stock": "80",
            "category": "Mic",
            "image": "",
            "description": "ewdftgdsgdfgdfgfdg",
        },

        {
            "id": "ITM009",
            "name": "Lithium Mobile Replacement Battery",
            "price": "800",
            "stock": "45",
            "category": "Battery",
            "image": "",
            "description": "ewdftgdsgdfgdfgfdg",
        },

        {
            "id": "ITM010",
            "name": "Edge-to-Edge Tempered Glass",
            "price": "200",
            "stock": "300",
            "category": "Tempered",
            "image": "",
            "description": "ewdftgdsgdfgdfgfdg",
        },

        {
            "id": "ITM011",
            "name": "Wireless Bluetooth Ear Pods",
            "price": "1500",
            "stock": "75",
            "category": "Ear pod",
            "image": "",
            "description": "ewdftgdsgdfgdfgfdg",
        },
    ]


# ============================================================
# CHECKOUT FUNCTION
# ============================================================

def process_cart_checkout(
    address: str,
    secondary_phone: str,
    description: str,
) -> str:

    if not st.session_state.cart:

        return (
            "Your cart is empty. Please add products first."
        )

    customer_name = st.session_state.logged_in_user

    primary_phone = st.session_state.user_phone

    timestamp = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    txn_id = (
        "TXN"
        + datetime.now().strftime(
            "%Y%m%d%H%M%S"
        )
    )

    cart_summary = ", ".join(
        [
            f"{item['quantity']} of {item['product']}"
            for item in st.session_state.cart
        ]
    )

    st.session_state.last_booked_item = cart_summary


    # --------------------------------------------------------
    # GOOGLE SHEET ORDER
    # --------------------------------------------------------

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
        }

        requests.post(
            GOOGLE_SCRIPT_URL,
            json=order_data,
            timeout=15,
        )

    except Exception as e:

        print(f"Order sheet error: {e}")


    # --------------------------------------------------------
    # LOCAL ORDER BACKUP
    # --------------------------------------------------------

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
            ]
        )


    # --------------------------------------------------------
    # CLEAR CART
    # --------------------------------------------------------

    st.session_state.cart = []


    return (
        f"Checkout complete! Order placed for: "
        f"{cart_summary}. "
        f"Order successful "
        f"(TXN ID: {txn_id})."
    )


# ============================================================
# HOME VIEW
# ============================================================

if st.session_state.current_view == "Home":

    st.markdown(
        '<div class="section-title">Products</div>',
        unsafe_allow_html=True,
    )


    # ========================================================
    # CATEGORY MENU
    # ========================================================

    categories = []

    for product in product_records:

        category = product.get(
            "category",
            "",
        ).strip()

        if category and category not in categories:

            categories.append(category)


    if not categories:

        categories = ["Headset"]


    # Compact category buttons
    category_columns = st.columns(
        min(len(categories), 4),
        gap="small",
    )


    for index, category in enumerate(categories):

        with category_columns[
            index % len(category_columns)
        ]:

            if st.button(
                category,
                key=f"menu_btn_{category}",
                use_container_width=True,
            ):

                st.session_state.selected_menu = category

                st.rerun()


    # ========================================================
    # CURRENT CATEGORY
    # ========================================================

    current_cat = st.session_state.get(
        "selected_menu",
        "Headset",
    )


    st.markdown(
        f"""
        <div class="menu-title">
            {current_cat}
        </div>
        """,
        unsafe_allow_html=True,
    )


    filtered_items = [
        p
        for p in product_records
        if p.get("category", "") == current_cat
    ]


    # ========================================================
    # PRODUCTS
    # ========================================================

    if filtered_items:

        for idx, prod in enumerate(filtered_items):

            slide_key = (
                f"slide_{current_cat}_{idx}"
            )


            if slide_key not in st.session_state:

                st.session_state[slide_key] = 0


            # ------------------------------------------------
            # PRODUCT BOX
            # ------------------------------------------------

            with st.container(
                border=True,
            ):

                # Product layout:
                #
                # Image
                # Description
                # Product details
                #
                p_img_col, p_desc_col, p_details_col = (
                    st.columns(
                        [1.25, 1.4, 1.35],
                        gap="small",
                    )
                )


                # =================================================
                # IMAGE
                # =================================================

                with p_img_col:

                    raw_img = prod.get(
                        "image",
                        "",
                    )


                    if raw_img:

                        img_paths = [
                            img.strip()
                            for img in raw_img
                            .replace("\\", ",")
                            .split(",")
                            if img.strip()
                        ]


                        valid_paths = [
                            path
                            for path in img_paths
                            if os.path.exists(path)
                        ]


                        if valid_paths:

                            total_imgs = len(
                                valid_paths
                            )

                            current_idx = (
                                st.session_state[
                                    slide_key
                                ]
                            )


                            # Image controls
                            l_btn, img_display, r_btn = (
                                st.columns(
                                    [0.7, 3.0, 0.7],
                                    gap="small",
                                )
                            )


                            # ------------------------------------------------
                            # PREVIOUS
                            # ------------------------------------------------

                            with l_btn:

                                if st.button(
                                    "‹",
                                    key=(
                                        f"prev_"
                                        f"{current_cat}_"
                                        f"{idx}"
                                    ),
                                ):

                                    if (
                                        st.session_state[
                                            slide_key
                                        ] > 0
                                    ):

                                        st.session_state[
                                            slide_key
                                        ] -= 1

                                    else:

                                        st.session_state[
                                            slide_key
                                        ] = (
                                            total_imgs - 1
                                        )

                                    st.rerun()


                            # ------------------------------------------------
                            # IMAGE
                            # ------------------------------------------------

                            with img_display:

                                image_path = valid_paths[
                                    current_idx
                                ]

                                st.image(
                                    image_path,
                                    use_container_width=True,
                                )


                            # ------------------------------------------------
                            # NEXT
                            # ------------------------------------------------

                            with r_btn:

                                if st.button(
                                    "›",
                                    key=(
                                        f"next_"
                                        f"{current_cat}_"
                                        f"{idx}"
                                    ),
                                ):

                                    if (
                                        st.session_state[
                                            slide_key
                                        ] + 1
                                        < total_imgs
                                    ):

                                        st.session_state[
                                            slide_key
                                        ] += 1

                                    else:

                                        st.session_state[
                                            slide_key
                                        ] = 0

                                    st.rerun()


                        else:

                            st.caption(
                                "No Image"
                            )

                    else:

                        st.caption(
                            "No Image"
                        )


                # =================================================
                # DESCRIPTION
                # =================================================

                with p_desc_col:

                    st.markdown(
                        "**Description:**"
                    )

                    description_text = (
                        prod.get(
                            "description",
                            "",
                        )
                    )

                    if description_text:

                        st.markdown(
                            f"""
                            <div class="product-description">
                                {description_text}
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )

                    else:

                        st.caption(
                            "No description"
                        )


                # =================================================
                # PRODUCT DETAILS
                # =================================================

                with p_details_col:

                    st.markdown(
                        f"""
                        <div class="product-name">
                            {prod.get("name", "")}
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )


                    st.markdown(
                        f"""
                        <div class="product-price">
                            ₹{prod.get("price", "0")}
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )


                    q_col, b_col = st.columns(
                        [1, 1],
                        gap="small",
                    )


                    # ------------------------------------------------
                    # QUANTITY
                    # ------------------------------------------------

                    with q_col:

                        q_val = st.number_input(
                            "Qty",
                            min_value=1.0,
                            value=1.0,
                            step=1.0,
                            key=(
                                f"qty_"
                                f"{current_cat}_"
                                f"{idx}"
                            ),
                            label_visibility="collapsed",
                        )


                    # ------------------------------------------------
                    # ADD
                    # ------------------------------------------------

                    with b_col:

                        if st.button(
                            "Add",
                            key=(
                                f"add_btn_"
                                f"{current_cat}_"
                                f"{idx}"
                            ),
                            use_container_width=True,
                        ):

                            full_q_str = (
                                f"{int(q_val)} Units"
                            )


                            st.session_state.cart.append(
                                {
                                    "product": prod.get(
                                        "name",
                                        "",
                                    ),
                                    "quantity": full_q_str,
                                }
                            )


                            st.success(
                                "Added!"
                            )

                            st.rerun()


    else:

        st.info(
            "No items found."
        )


# ============================================================
# CART / CHECKOUT VIEW
# ============================================================

else:

    st.markdown(
        """
        <div class="cart-title">
            🛒 Your Shopping Cart & Checkout
        </div>
        """,
        unsafe_allow_html=True,
    )


    # ========================================================
    # CART HAS PRODUCTS
    # ========================================================

    if st.session_state.cart:

        for c_idx, item in enumerate(
            st.session_state.cart
        ):

            cc1, cc2 = st.columns(
                [3.5, 1],
                gap="small",
            )


            with cc1:

                st.markdown(
                    f"""
                    **{item['product']}**
                    ({item['quantity']})
                    """
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


        # ====================================================
        # CHECKOUT
        # ====================================================

        st.markdown(
            """
            <div class="section-title">
                📍 Secure Checkout Form
            </div>
            """,
            unsafe_allow_html=True,
        )


        with st.form(
            "checkout_form_main_view"
        ):

            checkout_address = st.text_area(
                "Delivery Address:"
            )


            secondary_phone = st.text_input(
                "Alternative Contact Number:",
                max_chars=10,
            )


            product_desc = st.text_area(
                "Product Specifications / Custom Description:"
            )


            submit_checkout = st.form_submit_button(
                "Complete Order",
                use_container_width=True,
            )


            if submit_checkout:

                clean_secondary_phone = (
                    secondary_phone.strip()
                )


                if (
                    checkout_address.strip()
                    and len(clean_secondary_phone) == 10
                    and clean_secondary_phone.isdigit()
                ):

                    result_msg = (
                        process_cart_checkout(
                            checkout_address.strip(),
                            clean_secondary_phone,
                            product_desc.strip(),
                        )
                    )


                    st.success(
                        result_msg
                    )


                    st.session_state.current_view = (
                        "Home"
                    )


                    st.rerun()


                else:

                    st.warning(
                        "⚠️ Please provide delivery address "
                        "and a valid 10-digit secondary contact number."
                    )


    # ========================================================
    # EMPTY CART
    # ========================================================

    else:

        st.info(
            "Your cart is empty. "
            "Click **Home** above to browse and add products."
        )
