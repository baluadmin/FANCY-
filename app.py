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
# CSS
# ============================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
}

#MainMenu {
    visibility: hidden;
}

header {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

div[data-testid="stToolbar"] {
    display: none !important;
}

section[data-testid="stStatusWidget"] {
    display: none !important;
}


/* ============================================================
   GENERAL
   ============================================================ */

.stMainBlockContainer,
div[data-testid="stMainBlockContainer"],
.block-container {
    padding-top: 0rem !important;
    margin-top: 0rem !important;
    padding-left: 0.5rem !important;
    padding-right: 0.5rem !important;
    max-width: 100% !important;
}

label,
.stTextInput label,
p {
    font-weight: 600 !important;
}


/* ============================================================
   HM MOBILES HEADER
   ============================================================ */

.brand-banner {
    background: #2563eb;

    padding: 4px 6px;

    border-radius: 4px;

    text-align: center;

    margin: 0 0 2px 0 !important;

    box-shadow: 0 1px 2px rgba(0,0,0,0.08);
}

.brand-title {
    color: white !important;

    font-size: 13px !important;

    font-weight: 800 !important;

    letter-spacing: 0.5px;

    margin: 0 !important;

    padding: 0 !important;

    line-height: 1.1 !important;
}


/* ============================================================
   STORE + CART
   ============================================================ */

.hm-nav-box {
    width: 190px !important;

    max-width: 190px !important;

    margin: 2px auto 3px auto !important;

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

    gap: 5px !important;

    justify-content: center !important;

    align-items: center !important;
}

.hm-nav-box [data-testid="stRadio"] > div > label {
    flex: 1 1 0 !important;

    width: 50% !important;

    max-width: 50% !important;

    min-width: 0 !important;

    height: 30px !important;

    display: flex !important;

    align-items: center !important;

    justify-content: center !important;

    padding: 0 4px !important;

    margin: 0 !important;

    border: 1.5px solid #2563eb !important;

    border-radius: 4px !important;

    background: white !important;

    box-sizing: border-box !important;
}

.hm-nav-box [data-testid="stRadio"] > div > label > div:first-child {
    display: none !important;
}

.hm-nav-box [data-testid="stRadio"] > div > label p {
    color: #2563eb !important;

    font-size: 12px !important;

    font-weight: 700 !important;

    margin: 0 !important;

    padding: 0 !important;

    white-space: nowrap !important;
}

.hm-nav-box [data-testid="stRadio"] > div > label:has(input:checked) {
    background: #eff6ff !important;

    border-color: #1d4ed8 !important;
}


/* ============================================================
   CATEGORY
   ============================================================ */

.category-area {
    margin-top: 0 !important;

    margin-bottom: 5px !important;
}


/* ============================================================
   PRODUCT CARD
   ============================================================ */

.product-card {
    width: 100%;

    border: 1px solid #e2e8f0;

    border-radius: 8px;

    padding: 6px;

    margin-bottom: 10px;

    box-sizing: border-box;

    background: white;
}


/* ============================================================
   PRODUCT IMAGE ROW
   BUTTONS ARE CENTERED WITH IMAGE
   ============================================================ */

.product-image-row {
    display: flex;

    flex-direction: row;

    align-items: center;

    justify-content: center;

    width: 100%;

    gap: 3px;
}


/* ============================================================
   IMAGE
   ============================================================ */

.product-image-wrapper {
    flex: 1;

    min-width: 0;

    max-width: 520px;

    display: flex;

    justify-content: center;

    align-items: center;
}

.product-image-wrapper img {
    width: 100%;

    max-width: 500px;

    height: 250px;

    object-fit: contain;

    display: block;

    border-radius: 6px;
}


/* ============================================================
   SIDE BUTTONS
   ============================================================ */

.image-button {
    width: 38px;

    min-width: 38px;

    height: 38px;

    border: 1.5px solid #2563eb;

    border-radius: 50%;

    background: white;

    color: #2563eb;

    display: flex;

    align-items: center;

    justify-content: center;

    font-size: 19px;

    font-weight: 700;
}


/* ============================================================
   PRODUCT INFORMATION
   ============================================================ */

.product-name {
    text-align: center;

    font-size: 16px;

    font-weight: 700;

    margin-top: 4px;

    margin-bottom: 2px;
}

.product-price {
    text-align: center;

    font-size: 13px;

    font-weight: 700;

    margin-bottom: 2px;
}

.product-description {
    text-align: center;

    font-size: 12px;

    margin-bottom: 3px;
}


/* ============================================================
   MOBILE
   ============================================================ */

@media (max-width: 640px) {

    .product-card {
        padding: 4px;

        margin-bottom: 8px;
    }

    .product-image-row {
        gap: 2px;
    }

    .product-image-wrapper {
        max-width: calc(100% - 78px);
    }

    .product-image-wrapper img {
        width: 100%;

        height: 210px;

        object-fit: contain;
    }

    .image-button {
        width: 34px;

        min-width: 34px;

        height: 34px;

        font-size: 17px;
    }

    .product-name {
        font-size: 15px;
    }

    .product-price {
        font-size: 13px;
    }
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


            cust_name = st.text_input(
                "Your Name:"
            )


            cust_phone = st.text_input(
                "Mobile Number (10 digits):",
                max_chars=10
            )


            login_btn = st.form_submit_button(
                "Secure Login",
                use_container_width=True
            )


            if login_btn:

                if (
                    cust_name.strip()
                    and len(cust_phone) == 10
                    and cust_phone.isdigit()
                ):

                    st.session_state.logged_in_user = (
                        cust_name.strip()
                    )

                    st.session_state.user_phone = (
                        cust_phone.strip()
                    )


                    log_login_to_sheet(
                        cust_name.strip(),
                        cust_phone.strip()
                    )


                    st.rerun()

                else:

                    st.warning(
                        "⚠️ Enter a valid name and 10-digit mobile number."
                    )


    st.stop()


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="sticky-header-container">',
    unsafe_allow_html=True
)


st.markdown("""
    <div class="brand-banner">
        <div class="brand-title">HM MOBILES</div>
    </div>
""", unsafe_allow_html=True)


# ============================================================
# STORE / CART
# ============================================================

st.markdown(
    '<div class="hm-nav-box">',
    unsafe_allow_html=True
)


nav_choice = st.radio(
    "Navigation",

    [
        "Store",
        f"Cart({len(st.session_state.cart)})"
    ],

    index=(
        0
        if st.session_state.current_view == "Home"
        else 1
    ),

    horizontal=True,

    label_visibility="collapsed",

    key="hm_navigation"
)


new_view = (
    "Home"
    if nav_choice == "Store"
    else "Cart"
)


if st.session_state.current_view != new_view:

    st.session_state.current_view = new_view

    st.rerun()


st.markdown(
    "</div>",
    unsafe_allow_html=True
)

st.markdown(
    "</div>",
    unsafe_allow_html=True
)


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

        df = pd.read_csv(
            sheet_csv_url
        )

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

            product_records.append({

                "id":
                    str(row.iloc[0])
                    if len(row) > 0
                    and pd.notna(row.iloc[0])
                    else "N/A",

                "name":
                    str(row.iloc[1])
                    if len(row) > 1
                    and pd.notna(row.iloc[1])
                    else "Unknown",

                "category":
                    str(row.iloc[2]).strip()
                    if len(row) > 2
                    and pd.notna(row.iloc[2])
                    else "General",

                "stock":
                    str(row.iloc[3])
                    if len(row) > 3
                    and pd.notna(row.iloc[3])
                    else "0",

                "price":
                    str(row.iloc[4])
                    if len(row) > 4
                    and pd.notna(row.iloc[4])
                    else "0",

                "description":
                    str(row.iloc[5]).strip()
                    if len(row) > 5
                    and pd.notna(row.iloc[5])
                    else "",

                # IMAGE COLUMN
                "image":
                    str(row.iloc[6]).strip()
                    if len(row) > 6
                    and pd.notna(row.iloc[6])
                    else ""
            })


    except Exception as e:

        print(
            f"Parsing error: {e}"
        )


# ============================================================
# DEFAULT PRODUCT
# ============================================================

if not product_records:

    product_records = [

        {
            "id": "ITM001",

            "name":
                "Bluetooth Wireless Headset",

            "price":
                "1200",

            "stock":
                "50",

            "category":
                "Headset",

            "image":
                "",

            "description":
                "High performance audio"
        }
    ]


# ============================================================
# STORE
# ============================================================

if st.session_state.current_view == "Home":

    # --------------------------------------------------------
    # CATEGORY SELECTOR
    # --------------------------------------------------------

    categories = sorted(
        list(
            set(
                [
                    p["category"]
                    for p in product_records
                ]
            )
        )
    )


    st.markdown(
        '<div class="category-area">',
        unsafe_allow_html=True
    )


    selected_cat = st.selectbox(
        "Select Product Category:",
        categories,
        key="category_selector"
    )


    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # FILTER ONLY
    # CATEGORY IS NEVER STORED IN CART
    # --------------------------------------------------------

    filtered_items = [

        p

        for p in product_records

        if p["category"].strip().lower()
        == selected_cat.strip().lower()

    ]


    # --------------------------------------------------------
    # SHOW ALL PRODUCTS
    # ONE IMAGE FOR EACH PRODUCT
    # --------------------------------------------------------

    if filtered_items:

        for idx, prod in enumerate(
            filtered_items
        ):

            # =================================================
            # PRODUCT CARD
            # =================================================

            st.markdown(
                '<div class="product-card">',
                unsafe_allow_html=True
            )


            # =================================================
            # IMAGE + SIDE BUTTONS
            # =================================================

            left_col, image_col, right_col = st.columns(
                [0.55, 5, 0.55],
                vertical_alignment="center"
            )


            # -------------------------------------------------
            # LEFT BUTTON
            # -------------------------------------------------

            with left_col:

                if st.button(
                    "◀",
                    key=f"previous_{selected_cat}_{idx}",
                    use_container_width=True
                ):

                    # Button is vertically centered
                    # beside the product image.

                    st.session_state[
                        f"image_index_{idx}"
                    ] = max(
                        0,
                        st.session_state.get(
                            f"image_index_{idx}",
                            0
                        ) - 1
                    )

                    st.rerun()


            # -------------------------------------------------
            # IMAGE
            # -------------------------------------------------

            with image_col:

                if prod["image"]:

                    try:

                        st.image(
                            prod["image"],
                            use_container_width=True
                        )

                    except Exception:

                        st.info(
                            "Product image could not be loaded."
                        )

                else:

                    st.info(
                        "No product image available."
                    )


            # -------------------------------------------------
            # RIGHT BUTTON
            # -------------------------------------------------

            with right_col:

                if st.button(
                    "▶",
                    key=f"next_{selected_cat}_{idx}",
                    use_container_width=True
                ):

                    st.session_state[
                        f"image_index_{idx}"
                    ] = (
                        st.session_state.get(
                            f"image_index_{idx}",
                            0
                        ) + 1
                    )

                    st.rerun()


            # =================================================
            # PRODUCT NAME
            # =================================================

            st.markdown(
                f"""
                <div class="product-name">
                    {prod["name"]}
                </div>
                """,
                unsafe_allow_html=True
            )


            # =================================================
            # PRICE + STOCK
            # =================================================

            st.markdown(
                f"""
                <div class="product-price">
                    Price: ₹{prod["price"]}
                    &nbsp; | &nbsp;
                    Stock: {prod["stock"]} units
                </div>
                """,
                unsafe_allow_html=True
            )


            # =================================================
            # DESCRIPTION
            # =================================================

            if prod["description"]:

                st.markdown(
                    f"""
                    <div class="product-description">
                        {prod["description"]}
                    </div>
                    """,
                    unsafe_allow_html=True
                )


            # =================================================
            # QUANTITY
            # =================================================

            q_val = st.number_input(
                "Quantity",
                min_value=1.0,
                value=1.0,
                step=1.0,
                key=f"qty_{selected_cat}_{idx}"
            )


            # =================================================
            # ADD TO CART
            # =================================================

            if st.button(
                "Add to Cart",
                key=f"add_{selected_cat}_{idx}",
                use_container_width=True
            ):

                # IMPORTANT:
                # ONLY PRODUCT NAME + QUANTITY
                # CATEGORY IS NOT ADDED.

                cart_item = {
                    "product": prod["name"],
                    "quantity": f"{int(q_val)} Units"
                }


                st.session_state.cart.append(
                    cart_item
                )


                st.success(
                    f"{prod['name']} added to cart!"
                )


                st.rerun()


            # =================================================
            # CLOSE PRODUCT CARD
            # =================================================

            st.markdown(
                "</div>",
                unsafe_allow_html=True
            )


    else:

        st.info(
            f"No items found under category "
            f"'{selected_cat}'."
        )


# ============================================================
# CART
# ============================================================

else:

    st.subheader(
        "🛒 Shopping Cart & Checkout"
    )


    if st.session_state.cart:

        # ----------------------------------------------------
        # CART ITEMS
        # ----------------------------------------------------

        for i, item in enumerate(
            st.session_state.cart
        ):

            col_item_name, col_item_remove = st.columns(
                [3, 1]
            )


            with col_item_name:

                # ONLY PRODUCT + QUANTITY
                st.write(
                    f"• {item['product']} "
                    f"({item['quantity']})"
                )


            with col_item_remove:

                if st.button(
                    "Remove",
                    key=f"remove_cart_{i}"
                ):

                    st.session_state.cart.pop(
                        i
                    )

                    st.rerun()


        st.markdown("---")


        # ----------------------------------------------------
        # CHECKOUT
        # ----------------------------------------------------

        with st.form("checkout_form"):

            address = st.text_area(
                "Delivery Address:"
            )


            sec_phone = st.text_input(
                "Alternative Phone Number:",
                max_chars=10
            )


            pay_method = st.selectbox(
                "Payment Gateway",
                [
                    "UPI / GPay",
                    "Cash on Delivery"
                ]
            )


            checkout_button = st.form_submit_button(
                "Confirm & Dispatch Order",
                use_container_width=True
            )


            if checkout_button:

                if (
                    address.strip()
                    and len(sec_phone) == 10
                    and sec_phone.isdigit()
                ):

                    try:

                        order_payload = {

                            "Type":
                                "Order",

                            "Timestamp":
                                datetime.now().strftime(
                                    "%Y-%m-%d %H:%M:%S"
                                ),

                            "Customer_Name":
                                st.session_state.logged_in_user,

                            "Primary_Phone":
                                st.session_state.user_phone,

                            "Items":
                                str(
                                    st.session_state.cart
                                ),

                            "Address":
                                address.strip(),

                            "Secondary_Phone":
                                sec_phone.strip(),

                            "Payment_Method":
                                pay_method
                        }


                        requests.post(
                            GOOGLE_SCRIPT_URL,
                            json=order_payload,
                            timeout=5
                        )


                    except Exception:

                        pass


                    st.success(
                        "🎉 Order successfully placed "
                        "and synced with Google Sheets!"
                    )


                    st.session_state.cart = []

                    st.session_state.current_view = "Home"

                    st.rerun()


                else:

                    st.error(
                        "Please provide a delivery address "
                        "and valid 10-digit alternative phone."
                    )


    else:

        st.info(
            "Your cart is empty."
        )
