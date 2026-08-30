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


/* ============================================================
   GENERAL
   ============================================================ */

html,
body,
[class*="css"] {
    font-family: 'Inter', sans-serif !important;
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


/* ============================================================
   MAIN CONTAINER
   ============================================================ */

.stMainBlockContainer,
div[data-testid="stMainBlockContainer"],
.block-container {
    padding-top: 0rem !important;
    margin-top: 0rem !important;
    padding-left: 0.4rem !important;
    padding-right: 0.4rem !important;
    max-width: 100% !important;
}


/* ============================================================
   HM MOBILES HEADER
   ============================================================ */

.brand-banner {
    background: #2563eb;

    padding: 3px 5px;

    border-radius: 4px;

    text-align: center;

    margin: 0 0 2px 0 !important;

    box-shadow: 0 1px 2px rgba(0,0,0,0.08);
}

.brand-title {
    color: white !important;

    font-size: 12px !important;

    font-weight: 800 !important;

    letter-spacing: 0.5px;

    margin: 0 !important;

    padding: 0 !important;

    line-height: 1.1 !important;
}


/* ============================================================
   STORE / CART NAVIGATION
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
    width: 100% !important;

    margin: 0 !important;

    padding: 0 !important;
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

    height: 28px !important;

    display: flex !important;

    align-items: center !important;

    justify-content: center !important;

    padding: 0 4px !important;

    margin: 0 !important;

    border: 1px solid #2563eb !important;

    border-radius: 4px !important;

    background: white !important;

    box-sizing: border-box !important;
}

.hm-nav-box [data-testid="stRadio"] > div > label > div:first-child {
    display: none !important;
}

.hm-nav-box [data-testid="stRadio"] > div > label p {
    color: #2563eb !important;

    font-size: 11px !important;

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

    margin-bottom: 3px !important;
}

.category-area label {
    font-size: 12px !important;

    margin-bottom: 2px !important;
}


/* ============================================================
   PRODUCT CARD
   ============================================================ */

.product-card {
    width: 100% !important;

    border: 1px solid #e2e8f0;

    border-radius: 7px;

    padding: 5px;

    margin-bottom: 8px;

    box-sizing: border-box;

    background: white;
}


/* ============================================================
   IMAGE ROW
   IMPORTANT:
   LEFT BUTTON + IMAGE + RIGHT BUTTON
   ============================================================ */

.product-image-row {
    width: 100% !important;

    display: flex !important;

    flex-direction: row !important;

    flex-wrap: nowrap !important;

    align-items: center !important;

    justify-content: center !important;

    gap: 2px !important;
}


/* ============================================================
   IMAGE COLUMN
   ============================================================ */

.product-image-wrapper {
    flex: 1 1 auto !important;

    min-width: 0 !important;

    max-width: 430px !important;

    display: flex !important;

    justify-content: center !important;

    align-items: center !important;
}


/* ============================================================
   SMALLER PRODUCT IMAGE
   ============================================================ */

.product-image-wrapper img {
    width: 100% !important;

    max-width: 390px !important;

    height: 185px !important;

    object-fit: contain !important;

    display: block !important;

    border-radius: 5px !important;
}


/* ============================================================
   LEFT / RIGHT IMAGE BUTTON
   ============================================================ */

.image-side-button {
    width: 32px !important;

    min-width: 32px !important;

    max-width: 32px !important;

    height: 32px !important;

    min-height: 32px !important;

    padding: 0 !important;

    margin: 0 !important;

    border-radius: 50% !important;

    display: flex !important;

    align-items: center !important;

    justify-content: center !important;

    font-size: 15px !important;
}


/* ============================================================
   PRODUCT NAME
   ============================================================ */

.product-name {
    text-align: center;

    font-size: 15px;

    font-weight: 700;

    margin-top: 3px;

    margin-bottom: 2px;
}


/* ============================================================
   PRICE
   STOCK REMOVED
   ============================================================ */

.product-price {
    text-align: center;

    font-size: 12px;

    font-weight: 700;

    margin-bottom: 2px;
}


/* ============================================================
   DESCRIPTION
   ============================================================ */

.product-description {
    text-align: center;

    font-size: 11px;

    margin-bottom: 2px;
}


/* ============================================================
   QUANTITY LABEL
   ============================================================ */

div[data-testid="stNumberInput"] label {
    font-size: 11px !important;

    margin-bottom: 1px !important;
}


/* ============================================================
   SMALL QUANTITY BOX
   ============================================================ */

div[data-testid="stNumberInput"] {
    width: 150px !important;

    max-width: 150px !important;

    margin: 0 auto 4px auto !important;
}

div[data-testid="stNumberInput"] > div {
    min-height: 31px !important;

    height: 31px !important;

    border-radius: 6px !important;
}

div[data-testid="stNumberInput"] input {
    height: 29px !important;

    min-height: 29px !important;

    padding: 2px 4px !important;

    font-size: 11px !important;

    text-align: center !important;
}


/* ============================================================
   SMALL MINUS / PLUS BUTTONS
   ============================================================ */

div[data-testid="stNumberInput"] button {
    width: 25px !important;

    min-width: 25px !important;

    max-width: 25px !important;

    height: 29px !important;

    min-height: 29px !important;

    padding: 0 !important;

    margin: 0 !important;

    font-size: 12px !important;

    line-height: 1 !important;
}

div[data-testid="stNumberInput"] button svg {
    width: 11px !important;

    height: 11px !important;
}


/* ============================================================
   ADD TO CART BUTTON
   ============================================================ */

div.stButton > button {
    font-size: 11px !important;

    min-height: 30px !important;

    height: 30px !important;

    padding: 2px 8px !important;

    border-radius: 5px !important;
}


/* ============================================================
   MOBILE
   ============================================================ */

@media (max-width: 640px) {

    .stMainBlockContainer,
    div[data-testid="stMainBlockContainer"],
    .block-container {
        padding-left: 2px !important;

        padding-right: 2px !important;
    }


    /* --------------------------------
       HEADER
       -------------------------------- */

    .brand-banner {
        padding: 3px 4px !important;

        margin-bottom: 2px !important;
    }

    .brand-title {
        font-size: 11px !important;
    }


    /* --------------------------------
       NAV
       -------------------------------- */

    .hm-nav-box {
        width: 180px !important;

        max-width: 180px !important;
    }


    /* --------------------------------
       PRODUCT CARD
       -------------------------------- */

    .product-card {
        padding: 3px !important;

        margin-bottom: 7px !important;
    }


    /* --------------------------------
       FORCE IMAGE ROW HORIZONTAL
       -------------------------------- */

    div[data-testid="stHorizontalBlock"] {
        flex-wrap: nowrap !important;

        align-items: center !important;

        width: 100% !important;
    }


    div[data-testid="stHorizontalBlock"]
    > div[data-testid="column"] {
        flex-shrink: 0 !important;

        align-self: center !important;
    }


    /* --------------------------------
       LEFT ARROW COLUMN
       -------------------------------- */

    div[data-testid="stHorizontalBlock"]
    > div[data-testid="column"]:first-child {
        width: 32px !important;

        min-width: 32px !important;

        max-width: 32px !important;

        flex: 0 0 32px !important;
    }


    /* --------------------------------
       MIDDLE IMAGE COLUMN
       -------------------------------- */

    div[data-testid="stHorizontalBlock"]
    > div[data-testid="column"]:nth-child(2) {
        min-width: 0 !important;

        flex: 1 1 auto !important;

        width: auto !important;
    }


    /* --------------------------------
       RIGHT ARROW COLUMN
       -------------------------------- */

    div[data-testid="stHorizontalBlock"]
    > div[data-testid="column"]:last-child {
        width: 32px !important;

        min-width: 32px !important;

        max-width: 32px !important;

        flex: 0 0 32px !important;
    }


    /* --------------------------------
       SMALL IMAGE
       -------------------------------- */

    div[data-testid="stHorizontalBlock"]
    > div[data-testid="column"]:nth-child(2)
    img {
        width: 100% !important;

        height: 175px !important;

        max-height: 175px !important;

        object-fit: contain !important;
    }


    /* --------------------------------
       ARROW BUTTONS
       -------------------------------- */

    div[data-testid="stHorizontalBlock"]
    > div[data-testid="column"]
    button {
        width: 30px !important;

        min-width: 30px !important;

        max-width: 30px !important;

        height: 30px !important;

        min-height: 30px !important;

        padding: 0 !important;

        margin: 0 !important;

        border-radius: 50% !important;

        font-size: 14px !important;
    }


    /* --------------------------------
       PRODUCT TEXT
       -------------------------------- */

    .product-name {
        font-size: 14px !important;

        margin-top: 2px !important;
    }

    .product-price {
        font-size: 11px !important;
    }

    .product-description {
        font-size: 10px !important;
    }


    /* --------------------------------
       SMALL QUANTITY
       -------------------------------- */

    div[data-testid="stNumberInput"] {
        width: 135px !important;

        max-width: 135px !important;
    }

    div[data-testid="stNumberInput"] > div {
        height: 29px !important;

        min-height: 29px !important;
    }

    div[data-testid="stNumberInput"] input {
        height: 27px !important;

        min-height: 27px !important;

        font-size: 10px !important;
    }

    div[data-testid="stNumberInput"] button {
        width: 23px !important;

        min-width: 23px !important;

        max-width: 23px !important;

        height: 27px !important;

        min-height: 27px !important;

        font-size: 11px !important;
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
# LOGIN
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

            st.markdown(
                "### Customer Portal Login"
            )


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
# LOAD INVENTORY
# ============================================================

@st.cache_data(ttl=0)
def load_inventory_from_sheet():

    sheet_csv_url = (
        "https://docs.google.com/spreadsheets/d/"
        "1zXy8vwQtv2h5PooBLLEfVHAI_-aNBJK2K44kEMvczLQ/"
        "export?format=csv"
    )

    try:

        return pd.read_csv(
            sheet_csv_url
        )

    except Exception:

        return pd.DataFrame()


inv_df = load_inventory_from_sheet()

product_records = []


# ============================================================
# READ GOOGLE SHEET
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

                # IMAGE COLUMN — UNCHANGED
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

            "category":
                "Headset",

            "stock":
                "50",

            "price":
                "1200",

            "description":
                "High performance audio",

            "image":
                ""
        }
    ]


# ============================================================
# STORE
# ============================================================

if st.session_state.current_view == "Home":

    # --------------------------------------------------------
    # CATEGORY
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
    # FILTER PRODUCTS
    # --------------------------------------------------------

    filtered_items = [

        p

        for p in product_records

        if p["category"].strip().lower()
        == selected_cat.strip().lower()

    ]


    # --------------------------------------------------------
    # ALL PRODUCTS
    # ONE IMAGE PER PRODUCT
    # --------------------------------------------------------

    if filtered_items:

        for idx, prod in enumerate(
            filtered_items
        ):

            st.markdown(
                '<div class="product-card">',
                unsafe_allow_html=True
            )


            # =================================================
            # IMAGE + LEFT / RIGHT BUTTONS
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

                    current_index = st.session_state.get(
                        f"image_index_{idx}",
                        0
                    )

                    st.session_state[
                        f"image_index_{idx}"
                    ] = max(
                        0,
                        current_index - 1
                    )

                    st.rerun()


            # -------------------------------------------------
            # PRODUCT IMAGE
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

                    current_index = st.session_state.get(
                        f"image_index_{idx}",
                        0
                    )

                    st.session_state[
                        f"image_index_{idx}"
                    ] = current_index + 1

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
            # PRICE ONLY
            # STOCK REMOVED
            # =================================================

            st.markdown(
                f"""
                <div class="product-price">
                    Price: ₹{prod["price"]}
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
            # SMALL BOX WITH - AND +
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
                # CATEGORY IS NOT STORED.
                # ONLY PRODUCT NAME + QUANTITY.

                cart_item = {

                    "product":
                        prod["name"],

                    "quantity":
                        f"{int(q_val)} Units"
                }


                st.session_state.cart.append(
                    cart_item
                )


                st.success(
                    f"{prod['name']} added to cart!"
                )


                st.rerun()


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

                # ONLY PRODUCT NAME + QUANTITY
                # CATEGORY IS NOT DISPLAYED

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
