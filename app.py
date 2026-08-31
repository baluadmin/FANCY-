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
# PROFESSIONAL COLOURFUL MOBILE-FIRST DESIGN
# ============================================================

st.markdown(
    """
    <style>

    /* ========================================================
       GLOBAL
       ======================================================== */

    @import url(
        'https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&display=swap'
    );

    * {
        box-sizing: border-box;
    }

    html,
    body,
    [class*="css"] {
        font-family: "Poppins", sans-serif !important;
    }

    html,
    body,
    .stApp,
    [data-testid="stAppViewContainer"],
    [data-testid="stMain"] {
        width: 100% !important;
        max-width: 100% !important;
        overflow-x: hidden !important;
    }


    /* ========================================================
       HIDE STREAMLIT DEFAULT UI
       ======================================================== */

    #MainMenu {
        display: none !important;
        visibility: hidden !important;
    }

    header {
        display: none !important;
        visibility: hidden !important;
    }

    footer {
        display: none !important;
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
       MAIN CONTAINER
       ======================================================== */

    .block-container {
        width: 100% !important;
        max-width: 1150px !important;

        margin: 0 auto !important;

        padding-top: 0.45rem !important;
        padding-bottom: 0.8rem !important;
        padding-left: 0.65rem !important;
        padding-right: 0.65rem !important;
    }


    /* ========================================================
       NORMAL TEXT
       ======================================================== */

    p,
    label,
    span {
        font-weight: 500;
    }


    /* ========================================================
       LOGIN PAGE HEADER
       ======================================================== */

    .login-header {
        width: 100%;

        text-align: center;

        margin-top: 8px;
        margin-bottom: 14px;
    }

    .login-logo {
        display: inline-block;

        padding: 8px 18px;

        border-radius: 12px;

        background:
            linear-gradient(
                135deg,
                #2563eb,
                #4f46e5,
                #7c3aed
            );

        color: white !important;

        font-size: 28px !important;
        font-weight: 800 !important;

        letter-spacing: 1px;

        box-shadow:
            0 5px 15px rgba(37, 99, 235, 0.25);
    }

    .login-subtitle {
        margin-top: 7px;

        color: #64748b !important;

        font-size: 12px !important;

        line-height: 1.4;
    }


    /* ========================================================
       LOGIN CARD
       ======================================================== */

    .login-card {
        width: 100%;

        max-width: 520px;

        margin: 0 auto 12px auto;

        padding: 18px;

        background:
            linear-gradient(
                145deg,
                #ffffff,
                #f8fafc
            );

        border-radius: 16px;

        border: 1px solid #dbeafe;

        box-shadow:
            0 8px 25px rgba(15, 23, 42, 0.08);
    }

    .login-card-title {
        text-align: center;

        color: #1e3a8a !important;

        font-size: 18px !important;

        font-weight: 700 !important;

        margin-bottom: 12px;
    }


    /* ========================================================
       INPUTS
       ======================================================== */

    input,
    textarea,
    div[data-baseweb="select"] > div {

        width: 100% !important;

        background-color: white !important;

        color: #0f172a !important;

        border: 1.5px solid #cbd5e1 !important;

        border-radius: 8px !important;

        font-size: 13px !important;

        font-weight: 500 !important;
    }

    input:focus,
    textarea:focus {

        border-color: #2563eb !important;

        box-shadow:
            0 0 0 2px rgba(37, 99, 235, 0.12) !important;
    }


    /* ========================================================
       LOGIN BUTTON
       ======================================================== */

    button[kind="primaryFormSubmit"] {

        width: 100% !important;

        min-height: 42px !important;

        border: none !important;

        border-radius: 9px !important;

        background:
            linear-gradient(
                135deg,
                #2563eb,
                #4f46e5
            ) !important;

        color: white !important;

        font-size: 14px !important;

        font-weight: 700 !important;

        box-shadow:
            0 4px 12px rgba(37, 99, 235, 0.25);
    }

    button[kind="primaryFormSubmit"]:hover {

        background:
            linear-gradient(
                135deg,
                #1d4ed8,
                #4338ca
            ) !important;

        color: white !important;
    }


    /* ========================================================
       FORM
       ======================================================== */

    div[data-testid="stForm"] {

        border: none !important;

        padding: 0 !important;

        margin: 0 !important;
    }


    /* ========================================================
       BRAND HEADER AFTER LOGIN
       ======================================================== */

    .brand-banner {

        width: 100%;

        padding: 9px 10px;

        margin-bottom: 6px;

        border-radius: 10px;

        background:
            linear-gradient(
                135deg,
                #2563eb 0%,
                #4f46e5 48%,
                #7c3aed 100%
            );

        color: white !important;

        text-align: center;

        box-shadow:
            0 5px 15px rgba(37, 99, 235, 0.20);

        border: none;
    }

    .brand-title {

        margin: 0 !important;

        color: white !important;

        font-size: 17px !important;

        line-height: 1.2 !important;

        font-weight: 800 !important;

        letter-spacing: 0.4px;
    }


    /* ========================================================
       WELCOME
       ======================================================== */

    .mobile-welcome {

        width: 100%;

        padding: 5px 7px;

        margin-bottom: 5px;

        border-radius: 7px;

        background: #eff6ff;

        border-left: 3px solid #2563eb;

        color: #1e3a8a !important;

        font-size: 11px !important;

        line-height: 1.3 !important;

        overflow: hidden;

        text-overflow: ellipsis;

        white-space: nowrap;
    }


    /* ========================================================
       GENERAL BUTTON
       ======================================================== */

    div.stButton > button {

        width: 100% !important;

        min-height: 36px !important;

        padding: 0.25rem 0.35rem !important;

        border-radius: 8px !important;

        background: white !important;

        color: #1e293b !important;

        border: 1.5px solid #cbd5e1 !important;

        font-size: 11px !important;

        font-weight: 700 !important;

        white-space: nowrap !important;

        overflow: hidden !important;

        text-overflow: ellipsis !important;

        transition: all 0.15s ease;
    }

    div.stButton > button:hover {

        background: #eff6ff !important;

        color: #1d4ed8 !important;

        border-color: #60a5fa !important;
    }


    /* ========================================================
       NAVIGATION BUTTON COLOURS
       ======================================================== */

    /* Home */

    button[key="nav_home"] {

        background: #eff6ff !important;

        color: #1d4ed8 !important;

        border-color: #93c5fd !important;
    }


    /* Cart */

    button[key="nav_cart"] {

        background: #fff7ed !important;

        color: #c2410c !important;

        border-color: #fdba74 !important;
    }


    /* Logout */

    button[key="nav_logout"] {

        background: #fef2f2 !important;

        color: #dc2626 !important;

        border-color: #fca5a5 !important;
    }


    /* ========================================================
       NAVIGATION ROW
       ======================================================== */

    div[data-testid="stHorizontalBlock"] {

        width: 100% !important;

        max-width: 100% !important;

        gap: 0.25rem !important;
    }

    div[data-testid="stHorizontalBlock"]
    > div[data-testid="column"] {

        min-width: 0 !important;

        padding-left: 2px !important;

        padding-right: 2px !important;
    }


    /* ========================================================
       DIVIDER
       ======================================================== */

    hr {

        border: none !important;

        border-top: 1px solid #dbeafe !important;

        margin-top: 6px !important;

        margin-bottom: 7px !important;
    }


    /* ========================================================
       SECTION HEADER
       ======================================================== */

    .section-header {

        width: 100%;

        padding: 7px 9px;

        margin: 4px 0 6px 0;

        border-radius: 8px;

        background:
            linear-gradient(
                90deg,
                #eff6ff,
                #f5f3ff
            );

        border-left: 4px solid #2563eb;

        color: #1e3a8a !important;

        font-size: 14px !important;

        font-weight: 700 !important;
    }


    /* ========================================================
       CATEGORY AREA
       ======================================================== */

    .category-title {

        font-size: 13px !important;

        font-weight: 700 !important;

        color: #334155 !important;

        margin: 3px 0 5px 2px !important;
    }


    /* ========================================================
       CATEGORY BUTTONS
       ======================================================== */

    button[key^="menu_btn_"] {

        min-height: 34px !important;

        font-size: 10px !important;

        background:
            linear-gradient(
                135deg,
                #f8fafc,
                #eef2ff
            ) !important;

        color: #3730a3 !important;

        border-color: #c7d2fe !important;
    }

    button[key^="menu_btn_"]:hover {

        background:
            linear-gradient(
                135deg,
                #dbeafe,
                #ede9fe
            ) !important;

        border-color: #818cf8 !important;
    }


    /* ========================================================
       CURRENT CATEGORY
       ======================================================== */

    .current-category {

        display: inline-block;

        padding: 5px 11px;

        margin: 3px 0 7px 0;

        border-radius: 20px;

        background:
            linear-gradient(
                135deg,
                #2563eb,
                #7c3aed
            );

        color: white !important;

        font-size: 12px !important;

        font-weight: 700 !important;

        box-shadow:
            0 3px 8px rgba(37, 99, 235, 0.20);
    }


    /* ========================================================
       PRODUCT CARD
       ======================================================== */

    .product-card-header {

        margin-bottom: 4px;
    }

    .product-name {

        color: #172554 !important;

        font-size: 13px !important;

        line-height: 1.25 !important;

        font-weight: 700 !important;

        margin: 0 0 3px 0 !important;
    }

    .product-price {

        color: #15803d !important;

        font-size: 15px !important;

        line-height: 1.2 !important;

        font-weight: 800 !important;

        margin: 0 0 5px 0 !important;
    }

    .product-description-title {

        color: #475569 !important;

        font-size: 10px !important;

        font-weight: 700 !important;

        margin-bottom: 2px !important;
    }

    .product-description {

        color: #64748b !important;

        font-size: 10px !important;

        line-height: 1.35 !important;

        margin: 0 !important;
    }


    /* ========================================================
       PRODUCT IMAGE
       ======================================================== */

    [data-testid="stImage"] {

        width: 100% !important;

        text-align: center !important;
    }

    [data-testid="stImage"] img {

        max-width: 100% !important;

        height: auto !important;

        border-radius: 8px !important;
    }


    /* ========================================================
       IMAGE ARROWS
       ======================================================== */

    button[key^="prev_"],
    button[key^="next_"] {

        min-height: 32px !important;

        height: 32px !important;

        padding: 0 !important;

        border-radius: 50% !important;

        background: #eff6ff !important;

        color: #2563eb !important;

        border: 1px solid #93c5fd !important;

        font-size: 18px !important;

        line-height: 1 !important;
    }


    /* ========================================================
       ADD BUTTON
       ======================================================== */

    button[key^="add_btn_"] {

        min-height: 34px !important;

        background:
            linear-gradient(
                135deg,
                #16a34a,
                #15803d
            ) !important;

        color: white !important;

        border: none !important;

        font-size: 10px !important;

        font-weight: 700 !important;

        box-shadow:
            0 3px 8px rgba(22, 163, 74, 0.20);
    }

    button[key^="add_btn_"]:hover {

        background:
            linear-gradient(
                135deg,
                #15803d,
                #166534
            ) !important;

        color: white !important;
    }


    /* ========================================================
       QUANTITY
       ======================================================== */

    [data-testid="stNumberInput"] input {

        min-height: 34px !important;

        height: 34px !important;

        font-size: 11px !important;

        text-align: center !important;
    }


    /* ========================================================
       PRODUCT BORDER
       ======================================================== */

    div[data-testid="stVerticalBlockBorderWrapper"] {

        width: 100% !important;

        border: 1px solid #dbeafe !important;

        border-radius: 12px !important;

        background:
            linear-gradient(
                145deg,
                #ffffff,
                #f8fafc
            ) !important;

        box-shadow:
            0 3px 10px rgba(15, 23, 42, 0.05);

        padding: 5px !important;
    }


    /* ========================================================
       CART PAGE
       ======================================================== */

    .cart-header {

        width: 100%;

        padding: 9px 10px;

        margin-bottom: 7px;

        border-radius: 9px;

        background:
            linear-gradient(
                135deg,
                #fff7ed,
                #ffedd5
            );

        border-left: 4px solid #f97316;

        color: #9a3412 !important;

        font-size: 15px !important;

        font-weight: 800 !important;
    }


    .cart-item {

        padding: 7px;

        margin-bottom: 5px;

        border-radius: 8px;

        background: #f8fafc;

        border: 1px solid #e2e8f0;

        color: #334155 !important;

        font-size: 11px !important;
    }


    /* Remove cart button */

    button[key^="rem_cart_view_"] {

        min-height: 32px !important;

        background: #fef2f2 !important;

        color: #dc2626 !important;

        border-color: #fca5a5 !important;

        font-size: 9px !important;
    }


    /* ========================================================
       CHECKOUT
       ======================================================== */

    .checkout-header {

        width: 100%;

        padding: 8px 10px;

        margin: 6px 0 7px 0;

        border-radius: 9px;

        background:
            linear-gradient(
                135deg,
                #ecfdf5,
                #d1fae5
            );

        border-left: 4px solid #16a34a;

        color: #166534 !important;

        font-size: 14px !important;

        font-weight: 700 !important;
    }


    button[kind="primaryFormSubmit"] {

        box-shadow:
            0 4px 10px rgba(37, 99, 235, 0.20);
    }


    /* ========================================================
       SUCCESS / WARNING / INFO
       ======================================================== */

    div[data-testid="stAlert"] {

        border-radius: 8px !important;

        font-size: 11px !important;
    }


    /* ========================================================
       MOBILE PORTRAIT
       ======================================================== */

    @media (max-width: 600px) {

        .block-container {

            padding-left: 5px !important;

            padding-right: 5px !important;

            padding-top: 3px !important;

            padding-bottom: 6px !important;
        }

        .login-header {

            margin-top: 3px;

            margin-bottom: 9px;
        }

        .login-logo {

            font-size: 23px !important;

            padding: 6px 14px;
        }

        .login-subtitle {

            font-size: 9px !important;

            margin-top: 4px;
        }

        .login-card {

            padding: 11px;

            border-radius: 12px;
        }

        .login-card-title {

            font-size: 15px !important;

            margin-bottom: 8px;
        }

        .brand-banner {

            padding: 6px 5px;

            margin-bottom: 4px;

            border-radius: 7px;
        }

        .brand-title {

            font-size: 12px !important;
        }

        .mobile-welcome {

            font-size: 8px !important;

            padding: 4px 5px;

            margin-bottom: 3px;
        }

        div.stButton > button {

            min-height: 30px !important;

            height: 30px !important;

            font-size: 8px !important;

            border-radius: 6px !important;

            padding: 0.1rem 0.15rem !important;
        }

        button[key^="menu_btn_"] {

            min-height: 29px !important;

            height: 29px !important;

            font-size: 8px !important;
        }

        .section-header {

            padding: 5px 7px;

            font-size: 11px !important;

            margin-bottom: 4px;
        }

        .category-title {

            font-size: 10px !important;
        }

        .current-category {

            font-size: 10px !important;

            padding: 4px 9px;

            margin-bottom: 5px;
        }

        .product-name {

            font-size: 10px !important;
        }

        .product-price {

            font-size: 12px !important;
        }

        .product-description-title {

            font-size: 8px !important;
        }

        .product-description {

            font-size: 8px !important;

            line-height: 1.25 !important;
        }

        input,
        textarea,
        div[data-baseweb="select"] > div {

            font-size: 11px !important;

            min-height: 32px !important;
        }

        [data-testid="stNumberInput"] input {

            min-height: 29px !important;

            height: 29px !important;

            font-size: 9px !important;
        }

        button[key^="add_btn_"] {

            min-height: 29px !important;

            height: 29px !important;

            font-size: 8px !important;
        }

        button[key^="prev_"],
        button[key^="next_"] {

            min-height: 28px !important;

            height: 28px !important;

            font-size: 15px !important;
        }

        .cart-header {

            font-size: 12px !important;

            padding: 6px 8px;
        }

        .checkout-header {

            font-size: 11px !important;

            padding: 6px 8px;
        }

        .cart-item {

            font-size: 9px !important;

            padding: 5px;
        }

        button[key^="rem_cart_view_"] {

            min-height: 28px !important;

            height: 28px !important;

            font-size: 8px !important;
        }
    }


    /* ========================================================
       VERY SMALL PHONES
       ======================================================== */

    @media (max-width: 380px) {

        .block-container {

            padding-left: 3px !important;

            padding-right: 3px !important;
        }

        .login-logo {

            font-size: 21px !important;
        }

        .login-subtitle {

            font-size: 8px !important;
        }

        .brand-title {

            font-size: 10px !important;
        }

        .mobile-welcome {

            font-size: 7px !important;
        }

        div.stButton > button {

            font-size: 7px !important;
        }

        button[key^="menu_btn_"] {

            font-size: 7px !important;
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


# ============================================================
# LOGIN LOGGER
# ============================================================

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

        print(
            f"Login sheet error: {e}"
        )


# ============================================================
# LOGIN PAGE
# ============================================================

if not st.session_state.logged_in_user:

    st.markdown(
        """
        <div class="login-header">

            <div class="login-logo">
                HM MOBILES
            </div>

            <div class="login-subtitle">
                Thiruverkadu • Premium Mobile Accessories & Service
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


    st.markdown(
        """
        <div class="login-card">

            <div class="login-card-title">
                🔐 Customer Portal Login
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


    with st.form(
        "customer_direct_login_center"
    ):

        cust_name = st.text_input(
            "Your Name:",
            placeholder="Enter your name",
        )

        cust_phone = st.text_input(
            "Mobile Number:",
            max_chars=10,
            placeholder="Enter 10-digit mobile number",
        )

        login_btn = st.form_submit_button(
            "🔐 Secure Login",
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

                st.session_state.logged_in_user = (
                    clean_name
                )

                st.session_state.user_phone = (
                    clean_phone
                )

                st.session_state.user_role = (
                    "Customer"
                )

                st.session_state.selected_menu = (
                    "Headset"
                )

                st.session_state.current_view = (
                    "Home"
                )


                log_login_to_sheet(
                    clean_name,
                    clean_phone,
                )


                st.success(
                    "✅ Login Successful!"
                )

                st.rerun()


            else:

                st.warning(
                    "⚠️ Please provide a valid name "
                    "and 10-digit mobile number."
                )


    st.stop()


# ============================================================
# AFTER LOGIN - BRAND HEADER
# ============================================================

st.markdown(
    """
    <div class="brand-banner">

        <div class="brand-title">
            📱 HM MOBILES THIRUVERKADU
        </div>

    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# AFTER LOGIN - NAVIGATION
# ============================================================

top_comm, top_home, top_cart, top_logout = st.columns(
    [2.5, 0.8, 0.9, 0.9],
    gap="small",
)


# ============================================================
# WELCOME
# ============================================================

with top_comm:

    st.markdown(
        f"""
        <div class="mobile-welcome">
            👋 Welcome,
            <b>{st.session_state.logged_in_user}</b>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# HOME BUTTON
# ============================================================

with top_home:

    if st.button(
        "🏠 Home",
        key="nav_home",
        use_container_width=True,
    ):

        st.session_state.current_view = "Home"

        st.rerun()


# ============================================================
# CART BUTTON
# ============================================================

with top_cart:

    cart_count = len(
        st.session_state.cart
    )

    if st.button(
        f"🛒 {cart_count}",
        key="nav_cart",
        use_container_width=True,
    ):

        st.session_state.current_view = "Cart"

        st.rerun()


# ============================================================
# LOGOUT BUTTON
# ============================================================

with top_logout:

    if st.button(
        "🚪",
        key="nav_logout",
        use_container_width=True,
    ):

        st.session_state.clear()

        st.rerun()


st.markdown("---")


# ============================================================
# INVENTORY
# ============================================================

@st.cache_data(ttl=2)
def load_inventory_from_sheet():

    sheet_csv_url = (
        "https://docs.google.com/spreadsheets/d/"
        "1zXy8vwQtv2h5PooBLLEfVHAI_-aNBJK2K44kEMvczLQ"
        "/export?format=csv"
    )

    try:

        df = pd.read_csv(
            sheet_csv_url
        )

        df.to_csv(
            "inventory.csv",
            index=False,
        )

        return df

    except Exception as e:

        print(
            f"Inventory loading error: {e}"
        )

        if os.path.exists(
            "inventory.csv"
        ):

            try:

                return pd.read_csv(
                    "inventory.csv"
                )

            except Exception:

                pass

        return pd.DataFrame()


# ============================================================
# LOAD INVENTORY
# ============================================================

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
                        if len(row) > 5
                        and pd.notna(row.iloc[5])
                        else ""
                    ),

                    "image": (
                        str(row.iloc[6]).strip()
                        if len(row) > 6
                        and pd.notna(row.iloc[6])
                        else ""
                    ),
                }
            )

    except Exception as e:

        print(
            f"Product parsing error: {e}"
        )

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
            "description": "Premium wireless headset",
        },

        {
            "id": "ITM002",
            "name": "Over-Ear Gaming Headset",
            "price": "1800",
            "stock": "40",
            "category": "Headset",
            "image": "",
            "description": "Comfortable gaming headset",
        },

        {
            "id": "ITM003",
            "name": "Fast Type-C Charger 33W",
            "price": "650",
            "stock": "120",
            "category": "Charger",
            "image": "",
            "description": "33W fast charging adapter",
        },

        {
            "id": "ITM004",
            "name": "Dual Port Fast Wall Charger",
            "price": "500",
            "stock": "90",
            "category": "Charger",
            "image": "",
            "description": "Dual port fast charger",
        },

        {
            "id": "ITM005",
            "name": "Braided Micro USB Cable",
            "price": "250",
            "stock": "200",
            "category": "Cable",
            "image": "",
            "description": "Strong braided charging cable",
        },

        {
            "id": "ITM006",
            "name": "Type-C Fast Charging Cable",
            "price": "300",
            "stock": "150",
            "category": "Cable",
            "image": "",
            "description": "Fast Type-C charging cable",
        },

        {
            "id": "ITM007",
            "name": "Professional Studio Mic",
            "price": "2500",
            "stock": "30",
            "category": "Mic",
            "image": "",
            "description": "Professional studio microphone",
        },

        {
            "id": "ITM008",
            "name": "Mini Lavalier Clip-on Mic",
            "price": "450",
            "stock": "80",
            "category": "Mic",
            "image": "",
            "description": "Compact clip-on microphone",
        },

        {
            "id": "ITM009",
            "name": "Lithium Mobile Replacement Battery",
            "price": "800",
            "stock": "45",
            "category": "Battery",
            "image": "",
            "description": "Mobile replacement battery",
        },

        {
            "id": "ITM010",
            "name": "Edge-to-Edge Tempered Glass",
            "price": "200",
            "stock": "300",
            "category": "Tempered",
            "image": "",
            "description": "Full-screen tempered glass",
        },

        {
            "id": "ITM011",
            "name": "Wireless Bluetooth Ear Pods",
            "price": "1500",
            "stock": "75",
            "category": "Ear pod",
            "image": "",
            "description": "Wireless Bluetooth ear pods",
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
            "Your cart is empty. "
            "Please add products first."
        )


    customer_name = (
        st.session_state.logged_in_user
    )

    primary_phone = (
        st.session_state.user_phone
    )

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


    st.session_state.last_booked_item = (
        cart_summary
    )


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

        print(
            f"Order sheet error: {e}"
        )


    # --------------------------------------------------------
    # LOCAL ORDER BACKUP
    # --------------------------------------------------------

    file_exists = os.path.isfile(
        "orders.csv"
    )


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
        f"Checkout complete! "
        f"Order placed for: "
        f"{cart_summary}. "
        f"Order successful "
        f"(TXN ID: {txn_id})."
    )


# ============================================================
# HOME VIEW
# ============================================================

if st.session_state.current_view == "Home":

    st.markdown(
        """
        <div class="section-header">
            🛍️ Mobile Accessories
        </div>
        """,
        unsafe_allow_html=True,
    )


    # ========================================================
    # CATEGORY LIST
    # ========================================================

    categories = []


    for product in product_records:

        category = (
            product.get(
                "category",
                "",
            )
            .strip()
        )


        if (
            category
            and category not in categories
        ):

            categories.append(
                category
            )


    if not categories:

        categories = [
            "Headset"
        ]


    # ========================================================
    # CATEGORY BUTTON GRID
    # ========================================================

    category_count = min(
        len(categories),
        4,
    )


    category_columns = st.columns(
        category_count,
        gap="small",
    )


    for index, category in enumerate(
        categories
    ):

        with category_columns[
            index % category_count
        ]:

            if st.button(
                category,
                key=f"menu_btn_{category}",
                use_container_width=True,
            ):

                st.session_state.selected_menu = (
                    category
                )

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
        <div class="current-category">
            📂 {current_cat}
        </div>
        """,
        unsafe_allow_html=True,
    )


    # ========================================================
    # FILTER PRODUCTS
    # ========================================================

    filtered_items = [

        p
        for p in product_records

        if p.get(
            "category",
            "",
        )
        == current_cat
    ]


    # ========================================================
    # PRODUCTS
    # ========================================================

    if filtered_items:

        for idx, prod in enumerate(
            filtered_items
        ):

            slide_key = (
                f"slide_{current_cat}_{idx}"
            )


            if slide_key not in st.session_state:

                st.session_state[
                    slide_key
                ] = 0


            # =================================================
            # PRODUCT CARD
            # =================================================

            with st.container(
                border=True
            ):

                # ---------------------------------------------
                # IMAGE / DESCRIPTION / DETAILS
                # ---------------------------------------------

                p_img_col, p_desc_col, p_details_col = (
                    st.columns(
                        [1.25, 1.35, 1.25],
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
                            .replace(
                                "\\",
                                ",",
                            )
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


                            # ---------------------------------
                            # IMAGE NAVIGATION
                            # ---------------------------------

                            l_btn, img_display, r_btn = (
                                st.columns(
                                    [0.45, 3.1, 0.45],
                                    gap="small",
                                )
                            )


                            # ---------------------------------
                            # PREVIOUS
                            # ---------------------------------

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
                                        ]
                                        > 0
                                    ):

                                        st.session_state[
                                            slide_key
                                        ] -= 1

                                    else:

                                        st.session_state[
                                            slide_key
                                        ] = (
                                            total_imgs
                                            - 1
                                        )

                                    st.rerun()


                            # ---------------------------------
                            # IMAGE
                            # ---------------------------------

                            with img_display:

                                image_path = (
                                    valid_paths[
                                        current_idx
                                    ]
                                )


                                st.image(
                                    image_path,
                                    use_container_width=True,
                                )


                            # ---------------------------------
                            # NEXT
                            # ---------------------------------

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
                                        ]
                                        + 1
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
                                "🖼️ No Image"
                            )

                    else:

                        st.caption(
                            "🖼️ No Image"
                        )


                # =================================================
                # DESCRIPTION
                # =================================================

                with p_desc_col:

                    st.markdown(
                        """
                        <div class="product-description-title">
                            DESCRIPTION
                        </div>
                        """,
                        unsafe_allow_html=True,
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


                    # ---------------------------------------------
                    # QUANTITY / ADD
                    # ---------------------------------------------

                    q_col, b_col = st.columns(
                        [1, 1],
                        gap="small",
                    )


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


                    with b_col:

                        if st.button(
                            "➕ Add",
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


                # =================================================
                # PRODUCT SEPARATOR
                # =================================================

                st.markdown(
                    """
                    <hr
                        style="
                            margin-top:7px;
                            margin-bottom:2px;
                            border:none;
                            border-top:1px solid #dbeafe;
                        "
                    >
                    """,
                    unsafe_allow_html=True,
                )


    else:

        st.info(
            "No products found in this category."
        )


# ============================================================
# CART VIEW
# ============================================================

else:

    st.markdown(
        """
        <div class="cart-header">
            🛒 Your Shopping Cart
        </div>
        """,
        unsafe_allow_html=True,
    )


    # ========================================================
    # CART HAS ITEMS
    # ========================================================

    if st.session_state.cart:

        for c_idx, item in enumerate(
            st.session_state.cart
        ):

            cc1, cc2 = st.columns(
                [3.3, 1],
                gap="small",
            )


            # ------------------------------------------------
            # ITEM
            # ------------------------------------------------

            with cc1:

                st.markdown(
                    f"""
                    <div class="cart-item">
                        📦 <b>{item['product']}</b>
                        <br>
                        <span>
                            Quantity:
                            {item['quantity']}
                        </span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )


            # ------------------------------------------------
            # REMOVE
            # ------------------------------------------------

            with cc2:

                if st.button(
                    "Remove",
                    key=(
                        f"rem_cart_view_{c_idx}"
                    ),

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
            <div class="checkout-header">
                📍 Secure Checkout
            </div>
            """,
            unsafe_allow_html=True,
        )


        with st.form(
            "checkout_form_main_view"
        ):

            checkout_address = st.text_area(
                "Delivery Address:",
                placeholder=(
                    "Enter complete delivery address"
                ),
            )


            secondary_phone = st.text_input(
                "Alternative Contact Number:",
                max_chars=10,
                placeholder=(
                    "Enter 10-digit number"
                ),
            )


            product_desc = st.text_area(
                "Product Specifications / Custom Description:",
                placeholder=(
                    "Any special requirements?"
                ),
            )


            submit_checkout = (
                st.form_submit_button(
                    "✅ Complete Order",
                    use_container_width=True,
                )
            )


            if submit_checkout:

                clean_address = (
                    checkout_address.strip()
                )

                clean_secondary_phone = (
                    secondary_phone.strip()
                )

                clean_description = (
                    product_desc.strip()
                )


                if (

                    clean_address

                    and len(
                        clean_secondary_phone
                    ) == 10

                    and clean_secondary_phone.isdigit()
                ):

                    result_msg = (
                        process_cart_checkout(
                            clean_address,

                            clean_secondary_phone,

                            clean_description,
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
                        "⚠️ Please provide a delivery "
                        "address and valid 10-digit "
                        "secondary contact number."
                    )


    # ========================================================
    # EMPTY CART
    # ========================================================

    else:

        st.info(
            "🛒 Your cart is empty."
        )


        if st.button(
            "🏠 Browse Products",
            use_container_width=True,
        ):

            st.session_state.current_view = (
                "Home"
            )

            st.rerun()
