from datetime import datetime
import pandas as pd
import requests
import re
import streamlit as st


# ============================================================
# PAGE CONFIG
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

#MainMenu,
header,
footer,
div[data-testid="stToolbar"],
section[data-testid="stStatusWidget"] {
    display: none !important;
}


/* ============================================================
   MAIN
   ============================================================ */

.stMainBlockContainer,
div[data-testid="stMainBlockContainer"],
.block-container {
    padding-top: 0rem !important;
    margin-top: 0rem !important;
    padding-left: 3px !important;
    padding-right: 3px !important;
    max-width: 100% !important;
}


/* ============================================================
   HEADER
   ============================================================ */

.sticky-header-container {
    width: 100%;
    margin: 0 !important;
    padding: 0 !important;
}

.brand-banner {
    background: #2563eb;

    padding: 3px 5px;

    border-radius: 4px;

    text-align: center;

    margin: 0 0 2px 0 !important;
}

.brand-title {
    color: white !important;

    font-size: 11px !important;

    font-weight: 800 !important;

    letter-spacing: 0.5px;

    margin: 0 !important;

    padding: 0 !important;

    line-height: 1.1 !important;
}


/* ============================================================
   STORE / CART
   ============================================================ */

.hm-nav-box {
    width: 190px !important;

    max-width: 190px !important;

    margin: 2px auto 3px auto !important;

    padding: 0 !important;

    border: none !important;

    background: transparent !important;
}

.hm-nav-box [data-testid="stRadio"] {
    width: 100% !important;

    margin: 0 !important;

    padding: 0 !important;
}

.hm-nav-box [data-testid="stRadio"] > div {
    width: 100% !important;

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

    margin-bottom: 4px !important;
}

.category-area label {
    font-size: 11px !important;

    margin-bottom: 1px !important;
}


/* ============================================================
   PRODUCT CARD
   ============================================================ */

.product-card {
    width: 100% !important;

    border: 1px solid #dfe3e8;

    border-radius: 7px;

    padding: 4px;

    margin-bottom: 7px;

    background: white;

    box-sizing: border-box;
}


/* ============================================================
   IMAGE ROW
   ============================================================ */

.image-row {
    width: 100% !important;

    display: flex !important;

    flex-direction: row !important;

    flex-wrap: nowrap !important;

    align-items: center !important;

    justify-content: center !important;
}


/* ============================================================
   IMAGE
   ============================================================ */

.product-image-box {
    width: 100% !important;

    display: flex !important;

    justify-content: center !important;

    align-items: center !important;

    overflow: hidden !important;
}

.product-image-box img {
    width: 100% !important;

    height: 170px !important;

    object-fit: contain !important;

    display: block !important;

    margin: auto !important;
}


/* ============================================================
   ARROW BUTTONS
   ============================================================ */

.arrow-column {
    display: flex !important;

    align-items: center !important;

    justify-content: center !important;
}

.arrow-column button {
    width: 30px !important;

    min-width: 30px !important;

    max-width: 30px !important;

    height: 30px !important;

    min-height: 30px !important;

    max-height: 30px !important;

    padding: 0 !important;

    margin: 0 !important;

    border-radius: 50% !important;

    font-size: 13px !important;

    line-height: 1 !important;
}


/* ============================================================
   PRODUCT NAME
   ============================================================ */

.product-name {
    text-align: center;

    font-size: 14px;

    font-weight: 700;

    margin: 2px 0 1px 0;
}


/* ============================================================
   PRICE
   ============================================================ */

.product-price {
    text-align: center;

    font-size: 11px;

    font-weight: 700;

    margin: 0 0 1px 0;
}


/* ============================================================
   DESCRIPTION
   ============================================================ */

.product-description {
    text-align: center;

    font-size: 10px;

    font-weight: 400;

    margin: 0 0 2px 0;
}


/* ============================================================
   QUANTITY
   ============================================================ */

div[data-testid="stNumberInput"] {
    width: 130px !important;

    max-width: 130px !important;

    margin: 0 auto 3px auto !important;
}

div[data-testid="stNumberInput"] label {
    font-size: 10px !important;

    margin-bottom: 0 !important;
}

div[data-testid="stNumberInput"] > div {
    height: 28px !important;

    min-height: 28px !important;

    border-radius: 5px !important;
}

div[data-testid="stNumberInput"] input {
    height: 26px !important;

    min-height: 26px !important;

    padding: 0 !important;

    font-size: 10px !important;

    text-align: center !important;
}

div[data-testid="stNumberInput"] button {
    width: 23px !important;

    min-width: 23px !important;

    max-width: 23px !important;

    height: 26px !important;

    min-height: 26px !important;

    padding: 0 !important;

    margin: 0 !important;
}

div[data-testid="stNumberInput"] button svg {
    width: 10px !important;

    height: 10px !important;
}


/* ============================================================
   ADD CART
   ============================================================ */

.product-card div.stButton > button {
    height: 29px !important;

    min-height: 29px !important;

    padding: 2px 5px !important;

    font-size: 10px !important;

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


    /* Force image row horizontal */

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


    /* LEFT */

    div[data-testid="stHorizontalBlock"]
    > div[data-testid="column"]:first-child {
        width: 32px !important;

        min-width: 32px !important;

        max-width: 32px !important;

        flex: 0 0 32px !important;
    }


    /* IMAGE */

    div[data-testid="stHorizontalBlock"]
    > div[data-testid="column"]:nth-child(2) {
        width: auto !important;

        min-width: 0 !important;

        flex: 1 1 auto !important;
    }


    /* RIGHT */

    div[data-testid="stHorizontalBlock"]
    > div[data-testid="column"]:last-child {
        width: 32px !important;

        min-width: 32px !important;

        max-width: 32px !important;

        flex: 0 0 32px !important;
    }


    /* SMALL IMAGE */

    div[data-testid="stHorizontalBlock"]
    > div[data-testid="column"]:nth-child(2) img {
        width: 100% !important;

        height: 165px !important;

        max-height: 165px !important;

        object-fit: contain !important;
    }


    /* SMALL ARROWS */

    div[data-testid="stHorizontalBlock"]
    > div[data-testid="column"] button {
        width: 28px !important;

        min-width: 28px !important;

        max-width: 28px !important;

        height: 28px !important;

        min-height: 28px !important;

        padding: 0 !important;

        margin: 0 !important;

        border-radius: 50% !important;

        font-size: 12px !important;
    }


    /* PRODUCT TEXT */

    .product-name {
        font-size: 13px !important;
    }

    .product-price {
        font-size: 10px !important;
    }

    .product-description {
        font-size: 9px !important;
    }


    /* QUANTITY */

    div[data-testid="stNumberInput"] {
        width: 120px !important;

        max-width: 120px !important;
    }

    div[data-testid="stNumberInput"] input {
        font-size: 9px !important;
    }

    div[data-testid="stNumberInput"] button {
        width: 21px !important;

        min-width: 21px !important;

        max-width: 21px !important;
    }

}

</style>
""", unsafe_allow_html=True)


# ============================================================
# SESSION STATE
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

        requests.post(
            GOOGLE_SCRIPT_URL,

            json={
                "Type": "Login",
                "Customer_Name": name,
                "Primary_Phone": phone
            },

            timeout=3
        )

    except Exception:
        pass


# ============================================================
# IMAGE URL CONVERTER
# ============================================================

def convert_image_url(image_value):

    if not image_value:
        return None


    image_url = str(image_value).strip()


    if image_url.lower() in [
        "nan",
        "none",
        "null",
        ""
    ]:
        return None


    # --------------------------------------------------------
    # Google Drive file ID
    # --------------------------------------------------------

    drive_match = re.search(
        r"(?:/d/|id=)([a-zA-Z0-9_-]{20,})",
        image_url
    )


    if drive_match:

        file_id = drive_match.group(1)

        return (
            f"https://drive.google.com/uc?"
            f"export=view&id={file_id}"
        )


    # --------------------------------------------------------
    # Google Drive open URL
    # --------------------------------------------------------

    if "drive.google.com" in image_url:

        file_id_match = re.search(
            r"[-\w]{20,}",
            image_url
        )

        if file_id_match:

            file_id = file_id_match.group(0)

            return (
                f"https://drive.google.com/uc?"
                f"export=view&id={file_id}"
            )


    # --------------------------------------------------------
    # Google Photos / normal URL
    # --------------------------------------------------------

    return image_url


# ============================================================
# LOGIN
# ============================================================

if not st.session_state.logged_in_user:

    st.markdown("""
        <div class="brand-banner">
            <div class="brand-title">
                HM MOBILES
            </div>
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
        <div class="brand-title">
            HM MOBILES
        </div>
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
# LOAD GOOGLE SHEET
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

        st.error(
            f"Product data error: {e}"
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
                p["category"]
                for p in product_records
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
    # FILTER
    # --------------------------------------------------------

    filtered_items = [

        p

        for p in product_records

        if p["category"].strip().lower()
        == selected_cat.strip().lower()

    ]


    # --------------------------------------------------------
    # PRODUCTS
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
            # IMAGE ROW
            # =================================================

            left_col, image_col, right_col = st.columns(
                [0.45, 5, 0.45],
                vertical_alignment="center"
            )


            # -------------------------------------------------
            # LEFT BUTTON
            # -------------------------------------------------

            with left_col:

                if st.button(
                    "◀",

                    key=f"prev_{selected_cat}_{idx}",

                    use_container_width=True
                ):

                    current = st.session_state.get(
                        f"image_index_{idx}",
                        0
                    )

                    st.session_state[
                        f"image_index_{idx}"
                    ] = max(
                        0,
                        current - 1
                    )

                    st.rerun()


            # -------------------------------------------------
            # IMAGE
            # -------------------------------------------------

            with image_col:

                image_url = convert_image_url(
                    prod["image"]
                )


                if image_url:

                    try:

                        st.image(
                            image_url,

                            width=180
                        )

                    except Exception:

                        st.warning(
                            "Image could not be loaded."
                        )

                else:

                    st.info(
                        "No image"
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

                    current = st.session_state.get(
                        f"image_index_{idx}",
                        0
                    )

                    st.session_state[
                        f"image_index_{idx}"
                    ] = current + 1

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

                # ONLY PRODUCT NAME + QUANTITY
                # CATEGORY IS NOT SAVED.

                st.session_state.cart.append({

                    "product":
                        prod["name"],

                    "quantity":
                        f"{int(q_val)} Units"
                })


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
            f"No products found under {selected_cat}"
        )


# ============================================================
# CART
# ============================================================

else:

    st.subheader(
        "🛒 Shopping Cart & Checkout"
    )


    if st.session_state.cart:

        for i, item in enumerate(
            st.session_state.cart
        ):

            col_item, col_remove = st.columns(
                [3, 1]
            )


            with col_item:

                st.write(
                    f"• {item['product']} "
                    f"({item['quantity']})"
                )


            with col_remove:

                if st.button(
                    "Remove",
                    key=f"remove_{i}"
                ):

                    st.session_state.cart.pop(
                        i
                    )

                    st.rerun()


        st.markdown("---")


        # ====================================================
        # CHECKOUT
        # ====================================================

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


            checkout = st.form_submit_button(
                "Confirm & Dispatch Order",

                use_container_width=True
            )


            if checkout:

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
                        "🎉 Order successfully placed!"
                    )


                    st.session_state.cart = []

                    st.session_state.current_view = "Home"

                    st.rerun()


                else:

                    st.error(
                        "Please enter a delivery address "
                        "and valid 10-digit phone number."
                    )


    else:

        st.info(
            "Your cart is empty."
        )
