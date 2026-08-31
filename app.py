from datetime import datetime
import csv
import os
import random

import pandas as pd
import requests
import streamlit as st


# ============================================================
# 1. STREAMLIT PAGE CONFIGURATION
# ============================================================
st.set_page_config(
    page_title="HM Mobiles Thiruverkadu",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ============================================================
# 2. RESPONSIVE / MOBILE-FRIENDLY CSS
#    IMPORTANT:
#    - Do NOT stack every Streamlit column on mobile.
#    - Product image and product information stay side-by-side.
#    - The page remains a single-window application.
# ============================================================
st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');

        html, body, [class*="css"] {
            font-family: 'Poppins', sans-serif !important;
        }

        #MainMenu,
        header,
        footer,
        div[data-testid="stToolbar"],
        section[data-testid="stStatusWidget"],
        iframe[title="streamlit_app.manage"],
        .manage-app,
        div[class*="viewerBadge"],
        div[data-testid="stDecoration"] {
            visibility: hidden !important;
            display: none !important;
        }

        a.stMarkdownHeaderLink,
        h1 svg, h2 svg, h3 svg, h4 svg, h5 svg, h6 svg {
            display: none !important;
        }

        label,
        .stTextInput label,
        .stTextArea label,
        p,
        span,
        div[data-testid="stMarkdownContainer"] p {
            color: var(--text-color) !important;
            font-weight: 500 !important;
        }

        input,
        textarea,
        div[data-baseweb="select"] > div {
            background-color: var(--secondary-background-color) !important;
            color: var(--text-color) !important;
            border: 1.5px solid #cbd5e1 !important;
            font-size: 14px !important;
            font-weight: 400 !important;
            border-radius: 6px !important;
        }

        .brand-banner {
            background: linear-gradient(135deg, #e0f2fe 100%, #bae6fd 0%);
            padding: 10px 14px;
            border-radius: 8px;
            color: #0f172a !important;
            text-align: center;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
            margin-bottom: 8px;
            border: 1.5px solid #7dd3fc;
        }

        .brand-title {
            font-size: 18px;
            font-weight: 700;
            letter-spacing: 0.5px;
            color: #0f172a !important;
            margin: 0;
        }

        div.stButton > button,
        div.stFormSubmitButton > button {
            background-color: #f1f5f9 !important;
            color: #1e293b !important;
            border: 1.5px solid #cbd5e1 !important;
            font-weight: 600 !important;
            font-size: 13px !important;
            border-radius: 6px !important;
            padding: 0.3rem 0.4rem !important;
            width: 100% !important;
            min-height: 36px !important;
        }

        div.stButton > button:hover,
        div.stFormSubmitButton > button:hover {
            background-color: #e2e8f0 !important;
            color: #0f172a !important;
            border: 1px solid #94a3b8 !important;
        }

        /* Main content width */
        .block-container {
            padding-top: 0.5rem !important;
            padding-bottom: 0rem !important;
            padding-left: 0.6rem !important;
            padding-right: 0.6rem !important;
            max-width: 1100px !important;
            margin: auto !important;
        }

        /* Product cards */
        div[data-testid="stVerticalBlockBorderWrapper"] {
            border-radius: 8px !important;
            border-color: #cbd5e1 !important;
        }

        /* Keep columns side-by-side on mobile */
        @media (max-width: 768px) {
            .block-container {
                padding-left: 5px !important;
                padding-right: 5px !important;
                max-width: 100% !important;
            }

            /*
             * DO NOT use:
             * flex-direction: column
             * width: 100%
             * min-width: 100%
             *
             * Those rules caused the original mobile collapsing.
             */

            div[data-testid="stHorizontalBlock"] {
                flex-wrap: nowrap !important;
                gap: 0.35rem !important;
                align-items: center !important;
            }

            div[data-testid="column"] {
                min-width: 0 !important;
                padding-left: 2px !important;
                padding-right: 2px !important;
            }

            .brand-banner {
                padding: 8px 5px !important;
                margin-bottom: 5px !important;
            }

            .brand-title {
                font-size: 15px !important;
                letter-spacing: 0.2px !important;
            }

            div.stButton > button,
            div.stFormSubmitButton > button {
                font-size: 11px !important;
                padding: 0.25rem 0.2rem !important;
                min-height: 34px !important;
                white-space: nowrap !important;
            }

            input,
            textarea,
            div[data-baseweb="select"] > div {
                font-size: 13px !important;
            }

            div[data-testid="stImage"] img {
                max-width: 100% !important;
                height: auto !important;
            }

            /* Product card columns */
            div[data-testid="stVerticalBlockBorderWrapper"] {
                padding: 5px !important;
            }
        }

        @media (max-width: 420px) {
            .brand-title {
                font-size: 14px !important;
            }

            div.stButton > button,
            div.stFormSubmitButton > button {
                font-size: 10px !important;
            }

            .block-container {
                padding-left: 3px !important;
                padding-right: 3px !important;
            }
        }

        /* Prevent accidental horizontal page overflow */
        [data-testid="stAppViewContainer"],
        [data-testid="stAppViewContainer"] > .main,
        section.main {
            overflow-x: hidden !important;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# 3. SESSION STATE
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
# 4. GOOGLE APPS SCRIPT URL
# ============================================================
GOOGLE_SCRIPT_URL = (
    "https://script.google.com/macros/s/"
    "AKfycbzq1vB7RSGZA8aM5QOOxpSKxN06vEpYs14Yupx687pWZ4KNa0bkvAEO12QJZ_v88DT"
    "/exec"
)


# ============================================================
# 5. LOGIN LOGGING
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
        print(f"Login sheet error: {e}")


# ============================================================
# 6. CUSTOMER LOGIN
# ============================================================
if not st.session_state.logged_in_user:

    st.markdown(
        """
        <div style="
            text-align:center;
            margin-top:30px;
            margin-bottom:10px;
        ">
            <h1 style="
                font-size:24px;
                font-weight:700;
                margin-bottom:2px;
            ">
                HM MOBILES
            </h1>

            <p style="
                font-size:12px;
                font-weight:400;
            ">
                Thiruverkadu - Premium Mobile Accessories
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    _, mid_col, _ = st.columns([0.1, 1, 0.1])

    with mid_col:

        with st.form("customer_direct_login_center"):

            cust_name = st.text_input(
                "Your Name:"
            )

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
                    and len(cust_phone) == 10
                    and cust_phone.isdigit()
                ):

                    st.session_state.logged_in_user = cust_name.strip()
                    st.session_state.user_phone = cust_phone.strip()
                    st.session_state.user_role = "Customer"
                    st.session_state.selected_menu = "Headset"

                    log_login_to_sheet(
                        cust_name.strip(),
                        cust_phone.strip(),
                    )

                    st.success("✅ Login Successful!")
                    st.rerun()

                else:

                    st.warning(
                        "⚠️ Please provide a valid name and 10-digit mobile number."
                    )

    st.stop()


# ============================================================
# 7. HEADER
# ============================================================
st.markdown(
    """
    <div class="brand-banner">
        <h1 class="brand-title">
            HM MOBILES THIRUVERKADU
        </h1>
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# 8. TOP NAVIGATION
# ============================================================
top_comm, top_c1, top_c2, top_c3 = st.columns(
    [1.6, 0.8, 0.9, 0.7],
    gap="small",
)

with top_comm:

    st.markdown(
        f"""
        <p style="
            font-size:12px;
            margin:0;
            white-space:nowrap;
            overflow:hidden;
            text-overflow:ellipsis;
        ">
            Hi, <b>{st.session_state.logged_in_user}</b>
        </p>
        """,
        unsafe_allow_html=True,
    )


with top_c1:

    if st.button(
        "Home",
        use_container_width=True,
        key="top_home",
    ):

        st.session_state.current_view = "Home"
        st.rerun()


with top_c2:

    cart_count = len(st.session_state.cart)

    if st.button(
        f"Cart ({cart_count})",
        use_container_width=True,
        key="top_cart",
    ):

        st.session_state.current_view = "Cart"
        st.rerun()


with top_c3:

    if st.button(
        "Logout",
        use_container_width=True,
        key="top_logout",
    ):

        st.session_state.clear()
        st.rerun()


st.markdown(
    "<hr style='margin:6px 0px;'>",
    unsafe_allow_html=True,
)


# ============================================================
# 9. LOAD INVENTORY
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
            sheet_csv_url,
            dtype=str,
        )

        if not df.empty:
            return df

    except Exception:
        pass

    # Local CSV fallback
    if os.path.exists("inventory.csv"):

        try:

            return pd.read_csv(
                "inventory.csv",
                dtype=str,
            )

        except Exception:
            pass

    return pd.DataFrame()


inv_df = load_inventory_from_sheet()


# ============================================================
# 10. CONVERT INVENTORY TO PRODUCT RECORDS
# ============================================================
product_records = []


if not inv_df.empty:

    try:

        for _, row in inv_df.iterrows():

            product_records.append(
                {
                    "id": str(row.iloc[0]) if len(row) > 0 else "",
                    "name": str(row.iloc[1]) if len(row) > 1 else "",
                    "category": str(row.iloc[2]) if len(row) > 2 else "",
                    "stock": str(row.iloc[3]) if len(row) > 3 else "",
                    "price": str(row.iloc[4]) if len(row) > 4 else "",
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

    except Exception:
        product_records = []


# ============================================================
# 11. FALLBACK PRODUCTS
# ============================================================
if not product_records:

    product_records = [
        {
            "id": "ITM001",
            "name": "Bluetooth Wireless Headset",
            "price": "1200",
            "stock": "50",
            "category": "Headset",
            "image": "",
            "description": "High bass wireless headset with long battery life.",
        },
        {
            "id": "ITM002",
            "name": "Over-Ear Gaming Headset",
            "price": "1800",
            "stock": "40",
            "category": "Headset",
            "image": "",
            "description": "Immersive sound with noise cancellation mic.",
        },
        {
            "id": "ITM003",
            "name": "Fast Type-C Charger 33W",
            "price": "650",
            "stock": "120",
            "category": "Charger",
            "image": "",
            "description": "Quick charge wall adapter for smartphones.",
        },
        {
            "id": "ITM004",
            "name": "Wireless Bluetooth Ear Pods",
            "price": "1500",
            "stock": "75",
            "category": "Ear pod",
            "image": "",
            "description": "True wireless stereo earbuds.",
        },
    ]


# ============================================================
# 12. CHECKOUT / ORDER PROCESS
# ============================================================
def process_cart_checkout(
    address: str,
    secondary_phone: str,
    description: str,
) -> str:

    if not st.session_state.cart:
        return "Your cart is empty."

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

    st.session_state.cart = []

    return (
        f"Order placed successfully! "
        f"(TXN ID: {txn_id})"
    )


# ============================================================
# 13. VIEW SWITCHING
# ============================================================
if st.session_state.current_view == "Home":

    # --------------------------------------------------------
    # CATEGORY LIST
    # --------------------------------------------------------
    categories = []

    for product in product_records:

        category = str(
            product.get("category", "")
        ).strip()

        if category and category not in categories:
            categories.append(category)

    if not categories:
        categories = ["Headset"]

    # Horizontal scrolling category bar on mobile
    st.markdown(
        """
        <style>
            .category-scroll {
                display:flex;
                gap:6px;
                overflow-x:auto;
                padding:2px 0 7px 0;
                scrollbar-width:none;
            }

            .category-scroll::-webkit-scrollbar {
                display:none;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    cat_cols = st.columns(
        len(categories),
        gap="small",
    )

    for idx, cat in enumerate(categories):

        with cat_cols[idx]:

            is_selected = (
                st.session_state.selected_menu
                == cat
            )

            btn_label = (
                f"📌 {cat}"
                if is_selected
                else cat
            )

            if st.button(
                btn_label,
                key=f"cat_tab_{idx}_{cat}",
                use_container_width=True,
            ):

                st.session_state.selected_menu = cat
                st.rerun()


    st.markdown(
        "<hr style='margin:6px 0px;'>",
        unsafe_allow_html=True,
    )


    # --------------------------------------------------------
    # CURRENT CATEGORY
    # --------------------------------------------------------
    current_cat = st.session_state.get(
        "selected_menu",
        categories[0],
    )

    if current_cat not in categories:
        current_cat = categories[0]
        st.session_state.selected_menu = current_cat

    st.markdown(
        f"**Category: {current_cat}**"
    )


    filtered_items = [
        p
        for p in product_records
        if p.get("category") == current_cat
    ]


    # --------------------------------------------------------
    # PRODUCT LIST
    # --------------------------------------------------------
    if filtered_items:

        for idx, prod in enumerate(filtered_items):

            with st.container(border=True):

                # IMPORTANT:
                # Keep image and product details
                # side-by-side even on mobile.
                img_col, info_col = st.columns(
                    [1.1, 2.9],
                    gap="small",
                )


                # ------------------------------------------------
                # IMAGE AREA
                # ------------------------------------------------
                with img_col:

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

                        # Existing project stores local images
                        # in the images folder.
                        valid_paths = []

                        for image_path in img_paths:

                            # Direct path
                            if os.path.exists(image_path):
                                valid_paths.append(
                                    image_path
                                )
                                continue

                            # Relative project path
                            relative_path = os.path.join(
                                os.getcwd(),
                                image_path,
                            )

                            if os.path.exists(relative_path):
                                valid_paths.append(
                                    relative_path
                                )
                                continue

                            # images folder
                            images_path = os.path.join(
                                "images",
                                os.path.basename(
                                    image_path
                                ),
                            )

                            if os.path.exists(images_path):
                                valid_paths.append(
                                    images_path
                                )

                        if valid_paths:

                            # Maximum 6 images
                            display_paths = valid_paths[:6]

                            # Show images in two small columns
                            sub_c1, sub_c2 = st.columns(
                                2,
                                gap="small",
                            )

                            half_len = (
                                len(display_paths) + 1
                            ) // 2

                            col1_imgs = display_paths[
                                :half_len
                            ]

                            col2_imgs = display_paths[
                                half_len:
                            ]


                            with sub_c1:

                                for image_index, img_path in enumerate(
                                    col1_imgs
                                ):

                                    st.image(
                                        img_path,
                                        width=45,
                                        key=(
                                            f"img_left_"
                                            f"{idx}_"
                                            f"{image_index}"
                                        ),
                                    )


                            with sub_c2:

                                for image_index, img_path in enumerate(
                                    col2_imgs
                                ):

                                    st.image(
                                        img_path,
                                        width=45,
                                        key=(
                                            f"img_right_"
                                            f"{idx}_"
                                            f"{image_index}"
                                        ),
                                    )

                        else:

                            st.caption(
                                "No Image"
                            )

                    else:

                        st.caption(
                            "No Image"
                        )


                # ------------------------------------------------
                # PRODUCT INFORMATION
                # ------------------------------------------------
                with info_col:

                    st.markdown(
                        f"**{prod['name']}**"
                    )

                    st.markdown(
                        f"""
                        <span style="
                            color:#0284c7;
                            font-weight:700;
                            font-size:16px;
                        ">
                            ₹{prod['price']}
                        </span>
                        """,
                        unsafe_allow_html=True,
                    )

                    description = prod.get(
                        "description",
                        "",
                    )

                    if description:
                        st.caption(
                            description
                        )


                    # Quantity + Add to Cart
                    q_col, b_col = st.columns(
                        [0.85, 1.35],
                        gap="small",
                    )

                    with q_col:

                        q_val = st.number_input(
                            "Qty",
                            min_value=1,
                            value=1,
                            step=1,
                            key=(
                                f"qty_"
                                f"{current_cat}_"
                                f"{idx}"
                            ),
                            label_visibility="collapsed",
                        )


                    with b_col:

                        if st.button(
                            "Add to Cart",
                            key=(
                                f"add_"
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
                                    "product": prod["name"],
                                    "quantity": full_q_str,
                                }
                            )

                            st.success(
                                "Added!"
                            )

                            st.rerun()

    else:

        st.info(
            "No items found in this category."
        )


# ============================================================
# 14. CART / CHECKOUT VIEW
# ============================================================
else:

    st.subheader(
        "🛒 Shopping Cart"
    )


    if st.session_state.cart:

        for c_idx, item in enumerate(
            st.session_state.cart
        ):

            cc1, cc2 = st.columns(
                [3, 1],
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
                    key=f"rem_{c_idx}",
                    use_container_width=True,
                ):

                    st.session_state.cart.pop(
                        c_idx
                    )

                    st.rerun()


        st.markdown("---")


        st.subheader(
            "📍 Delivery Details"
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
                "Notes / Custom Request (Optional):"
            )


            submit_checkout = st.form_submit_button(
                "Complete Order",
                use_container_width=True,
            )


            if submit_checkout:

                if (
                    checkout_address.strip()
                    and len(secondary_phone) == 10
                    and secondary_phone.isdigit()
                ):

                    result_msg = (
                        process_cart_checkout(
                            checkout_address.strip(),
                            secondary_phone.strip(),
                            product_desc.strip(),
                        )
                    )

                    st.success(
                        result_msg
                    )

                    st.session_state.current_view = "Home"

                    st.rerun()

                else:

                    st.warning(
                        "⚠️ Please provide address "
                        "and a valid 10-digit alternative "
                        "contact number."
                    )


    else:

        st.info(
            "Your cart is empty. "
            "Click **Home** to browse products."
        )
