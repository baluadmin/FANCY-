from datetime import datetime
import pandas as pd
import requests
import re
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

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');


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
    padding-left: 0.3rem !important;
    padding-right: 0.3rem !important;
    padding-bottom: 0.5rem !important;
    max-width: 100% !important;
}


/* ============================================================
   HEADER
   ============================================================ */

.brand-banner {
    background: linear-gradient(
        135deg,
        #6366f1 0%,
        #a855f7 50%,
        #ec4899 100%
    );

    padding: 3px 6px;

    border-radius: 6px;

    text-align: center;

    margin: 0 0 2px 0 !important;

    box-shadow:
        0 2px 4px rgba(168, 85, 247, 0.25);
}

.brand-title {
    color: white !important;

    font-size: 12px !important;

    font-weight: 800 !important;

    letter-spacing: 0.8px;

    margin: 0 !important;

    padding: 0 !important;

    line-height: 1.1 !important;
}


/* ============================================================
   STORE / CART
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
    background: linear-gradient(
        135deg,
        #8b5cf6 0%,
        #ec4899 100%
    ) !important;

    border-color: #7c3aed !important;
}

.hm-nav-box [data-testid="stRadio"] > div > label:has(input:checked) p {
    color: white !important;
}


/* ============================================================
   CATEGORY
   ============================================================ */

.category-area {
    margin-top: 0 !important;

    margin-bottom: 3px !important;
}

.category-area div[data-baseweb="select"] > div {
    min-height: 26px !important;

    padding-top: 0 !important;

    padding-bottom: 0 !important;

    border-color: #cbd5e1 !important;

    background: #f8fafc !important;
}


/* ============================================================
   PRODUCT CARD
   ============================================================ */

.product-card {
    width: 100% !important;

    border: 1.5px solid #e2e8f0;

    border-radius: 6px;

    padding: 4px;

    margin-bottom: 7px;

    box-sizing: border-box;

    background: white;

    box-shadow:
        0 1px 3px rgba(0,0,0,0.03);
}


/* ============================================================
   IMAGE AREA
   ============================================================ */

.image-area {
    width: 100% !important;

    min-height: 145px !important;

    display: flex !important;

    align-items: center !important;

    justify-content: center !important;
}


/* ============================================================
   SMALL PRODUCT IMAGE
   ============================================================ */

.image-area img {
    width: 150px !important;

    height: 145px !important;

    object-fit: contain !important;

    display: block !important;

    margin: auto !important;
}


/* ============================================================
   PRODUCT NAME
   ============================================================ */

.product-name {
    text-align: center;

    font-size: 11px;

    font-weight: 700;

    color: #1e293b;

    margin-top: 2px;

    margin-bottom: 1px;

    white-space: nowrap;

    overflow: hidden;

    text-overflow: ellipsis;
}


/* ============================================================
   PRICE
   STOCK REMOVED
   ============================================================ */

.product-price {
    text-align: center;

    font-size: 10px;

    font-weight: 700;

    color: #059669;

    margin-bottom: 2px;
}


/* ============================================================
   DESCRIPTION
   ============================================================ */

.product-description {
    text-align: center;

    font-size: 9px;

    color: #64748b;

    margin-bottom: 2px;

    white-space: nowrap;

    overflow: hidden;

    text-overflow: ellipsis;
}


/* ============================================================
   NUMBER INPUT
   ============================================================ */

div[data-testid="stNumberInput"] {
    width: 125px !important;

    max-width: 125px !important;

    margin: 0 auto 3px auto !important;
}

div[data-testid="stNumberInput"] > div {
    height: 27px !important;

    min-height: 27px !important;

    border-radius: 5px !important;
}

div[data-testid="stNumberInput"] input {
    height: 25px !important;

    min-height: 25px !important;

    padding: 0 !important;

    font-size: 9px !important;

    text-align: center !important;
}

div[data-testid="stNumberInput"] button {
    width: 22px !important;

    min-width: 22px !important;

    max-width: 22px !important;

    height: 25px !important;

    min-height: 25px !important;

    padding: 0 !important;

    margin: 0 !important;
}

div[data-testid="stNumberInput"] button svg {
    width: 9px !important;

    height: 9px !important;
}


/* ============================================================
   BUTTONS
   ============================================================ */

div.stButton > button {
    min-height: 24px !important;

    height: 24px !important;

    padding: 0 4px !important;

    font-size: 9px !important;

    border-radius: 4px !important;
}


/* ============================================================
   IMAGE ARROWS
   ============================================================ */

.image-arrow button {
    width: 28px !important;

    min-width: 28px !important;

    max-width: 28px !important;

    height: 28px !important;

    min-height: 28px !important;

    max-height: 28px !important;

    padding: 0 !important;

    margin: 0 !important;

    border-radius: 50% !important;

    font-size: 12px !important;
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


    /* --------------------------------------------
       PRODUCT GRID
       -------------------------------------------- */

    div[data-testid="stHorizontalBlock"] {
        flex-wrap: nowrap !important;

        align-items: center !important;

        width: 100% !important;
    }


    /* --------------------------------------------
       IMAGE ARROW COLUMNS
       -------------------------------------------- */

    div[data-testid="stHorizontalBlock"]
    > div[data-testid="column"] {
        flex-shrink: 0 !important;

        align-self: center !important;
    }


    /* LEFT */

    div[data-testid="stHorizontalBlock"]
    > div[data-testid="column"]:first-child {
        width: 28px !important;

        min-width: 28px !important;

        max-width: 28px !important;

        flex: 0 0 28px !important;
    }


    /* CENTER IMAGE */

    div[data-testid="stHorizontalBlock"]
    > div[data-testid="column"]:nth-child(2) {
        min-width: 0 !important;

        width: auto !important;

        flex: 1 1 auto !important;
    }


    /* RIGHT */

    div[data-testid="stHorizontalBlock"]
    > div[data-testid="column"]:last-child {
        width: 28px !important;

        min-width: 28px !important;

        max-width: 28px !important;

        flex: 0 0 28px !important;
    }


    /* --------------------------------------------
       IMAGE
       -------------------------------------------- */

    div[data-testid="stHorizontalBlock"]
    > div[data-testid="column"]:nth-child(2) img {
        width: 130px !important;

        height: 135px !important;

        max-width: 130px !important;

        max-height: 135px !important;

        object-fit: contain !important;
    }


    /* --------------------------------------------
       ARROWS
       -------------------------------------------- */

    div[data-testid="stHorizontalBlock"]
    > div[data-testid="column"] button {
        width: 27px !important;

        min-width: 27px !important;

        max-width: 27px !important;

        height: 27px !important;

        min-height: 27px !important;

        max-height: 27px !important;

        padding: 0 !important;

        margin: 0 !important;

        border-radius: 50% !important;

        font-size: 11px !important;
    }


    /* --------------------------------------------
       PRODUCT TEXT
       -------------------------------------------- */

    .product-name {
        font-size: 10px !important;
    }

    .product-price {
        font-size: 9px !important;
    }

    .product-description {
        font-size: 8px !important;
    }


    /* --------------------------------------------
       QUANTITY
       -------------------------------------------- */

    div[data-testid="stNumberInput"] {
        width: 110px !important;

        max-width: 110px !important;
    }

    div[data-testid="stNumberInput"] > div {
        height: 25px !important;

        min-height: 25px !important;
    }

    div[data-testid="stNumberInput"] input {
        height: 23px !important;

        min-height: 23px !important;

        font-size: 8px !important;
    }

    div[data-testid="stNumberInput"] button {
        width: 20px !important;

        min-width: 20px !important;

        max-width: 20px !important;

        height: 23px !important;

        min-height: 23px !important;
    }


    /* --------------------------------------------
       ADD TO CART
       -------------------------------------------- */

    .product-card div.stButton > button {
        height: 24px !important;

        min-height: 24px !important;

        font-size: 9px !important;
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
# IMAGE URL FUNCTION
# ============================================================

def make_image_url(image_value):

    if image_value is None:
        return None

    image_value = str(image_value).strip()

    if image_value == "":
        return None

    if image_value.lower() in [
        "nan",
        "none",
        "null"
    ]:
        return None


    # --------------------------------------------------------
    # Already a complete URL
    # --------------------------------------------------------

    if image_value.startswith("http://"):

        return image_value

    if image_value.startswith("https://"):

        # Google Drive link
        if "drive.google.com" in image_value:

            match = re.search(
                r"(?:/d/|id=)([a-zA-Z0-9_-]+)",
                image_value
            )

            if match:

                file_id = match.group(1)

                return (
                    "https://drive.google.com/uc"
                    "?export=view&id="
                    + file_id
                )

        return image_value


    # --------------------------------------------------------
    # GitHub filename
    # --------------------------------------------------------

    GITHUB_USER = "Balumahendran"

    REPO_NAME = "python-project1"

    return (
        f"https://raw.githubusercontent.com/"
        f"{GITHUB_USER}/"
        f"{REPO_NAME}/"
        f"main/images/"
        f"{image_value}"
    )


# ============================================================
# LOGIN PAGE
# ============================================================

if not st.session_state.logged_in_user:

    st.markdown("""
        <div class="brand-banner">
            <div class="brand-title">
                HM MOBILES
            </div>
        </div>
    """, unsafe_allow_html=True)


    _, mid_col, _ = st.columns(
        [1, 2, 1]
    )


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
# STORE / CART NAVIGATION
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

            # ------------------------------------------------
            # IMAGE COLUMN = G
            # ------------------------------------------------

            raw_img = (
                str(row.iloc[6]).strip()
                if len(row) > 6
                and pd.notna(row.iloc[6])
                else ""
            )


            # ------------------------------------------------
            # SUPPORT MULTIPLE IMAGES
            #
            # Example:
            #
            # headset1.jpg
            # headset2.jpg
            # headset3.jpg
            #
            # OR:
            #
            # headset1.jpg, headset2.jpg
            # ------------------------------------------------

            image_values = re.split(
                r"[\n,]+",
                raw_img
            )


            img_list = []


            for img in image_values:

                img = img.strip()

                if not img:
                    continue

                if img.lower() == "nan":
                    continue

                img_url = make_image_url(
                    img
                )

                if img_url:
                    img_list.append(
                        img_url
                    )


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


                "images":
                    img_list

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
            "id":
                "ITM001",

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

            "images":
                []
        }

    ]


# ============================================================
# STORE
# ============================================================

if st.session_state.current_view == "Home":

    # --------------------------------------------------------
    # CATEGORIES
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
        ==
        selected_cat.strip().lower()

    ]


    # ========================================================
    # SHOW ALL PRODUCTS
    # ========================================================

    if filtered_items:

        for i in range(
            0,
            len(filtered_items),
            2
        ):

            cols = st.columns(
                2,
                gap="small"
            )


            for col_idx in range(2):

                item_index = i + col_idx


                if item_index >= len(
                    filtered_items
                ):
                    continue


                prod = filtered_items[
                    item_index
                ]


                with cols[col_idx]:

                    st.markdown(
                        '<div class="product-card">',
                        unsafe_allow_html=True
                    )


                    # =================================================
                    # IMAGE INDEX
                    # =================================================

                    img_key = (
                        f"img_idx_"
                        f"{selected_cat}_"
                        f"{item_index}"
                    )


                    if img_key not in st.session_state:

                        st.session_state[
                            img_key
                        ] = 0


                    total_imgs = len(
                        prod["images"]
                    )


                    # =================================================
                    # IMAGE + ARROWS
                    # =================================================

                    left_col, image_col, right_col = st.columns(
                        [0.35, 4, 0.35],
                        vertical_alignment="center"
                    )


                    # -------------------------------------------------
                    # LEFT BUTTON
                    # -------------------------------------------------

                    with left_col:

                        if st.button(
                            "◀",

                            key=(
                                f"prev_"
                                f"{selected_cat}_"
                                f"{item_index}"
                            )
                        ):

                            if total_imgs > 0:

                                st.session_state[
                                    img_key
                                ] = (

                                    st.session_state[
                                        img_key
                                    ] - 1

                                ) % total_imgs


                                st.rerun()


                    # -------------------------------------------------
                    # IMAGE
                    # -------------------------------------------------

                    with image_col:

                        if total_imgs > 0:

                            current_idx = (
                                st.session_state[
                                    img_key
                                ] % total_imgs
                            )


                            current_image = (
                                prod["images"][
                                    current_idx
                                ]
                            )


                            try:

                                st.image(
                                    current_image,

                                    width=130
                                )

                            except Exception:

                                st.markdown(
                                    """
                                    <div style="
                                        height:135px;
                                        display:flex;
                                        align-items:center;
                                        justify-content:center;
                                        text-align:center;
                                        font-size:9px;
                                        color:#ef4444;
                                    ">
                                        Image failed
                                    </div>
                                    """,

                                    unsafe_allow_html=True
                                )


                        else:

                            st.markdown(
                                """
                                <div style="
                                    height:135px;
                                    display:flex;
                                    align-items:center;
                                    justify-content:center;
                                    text-align:center;
                                    font-size:9px;
                                    color:#94a3b8;
                                ">
                                    No image
                                </div>
                                """,

                                unsafe_allow_html=True
                            )


                    # -------------------------------------------------
                    # RIGHT BUTTON
                    # -------------------------------------------------

                    with right_col:

                        if st.button(
                            "▶",

                            key=(
                                f"next_"
                                f"{selected_cat}_"
                                f"{item_index}"
                            )
                        ):

                            if total_imgs > 0:

                                st.session_state[
                                    img_key
                                ] = (

                                    st.session_state[
                                        img_key
                                    ] + 1

                                ) % total_imgs


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
                    # PRICE
                    # STOCK NOT SHOWN
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

                        key=(
                            f"qty_"
                            f"{selected_cat}_"
                            f"{item_index}"
                        ),

                        label_visibility="collapsed"
                    )


                    # =================================================
                    # ADD TO CART
                    # =================================================

                    if st.button(

                        "Add to Cart",

                        key=(
                            f"add_"
                            f"{selected_cat}_"
                            f"{item_index}"
                        ),

                        use_container_width=True
                    ):

                        # ---------------------------------------------
                        # CATEGORY IS NOT ADDED
                        # ---------------------------------------------

                        st.session_state.cart.append({

                            "product":
                                prod["name"],

                            "quantity":
                                f"{int(q_val)} Units"

                        })


                        st.success(
                            f"{prod['name']} added!"
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

        for i, item in enumerate(
            st.session_state.cart
        ):

            col_item_name, col_remove = st.columns(
                [3, 1]
            )


            with col_item_name:

                st.write(
                    f"• {item['product']} "
                    f"({item['quantity']})"
                )


            with col_remove:

                if st.button(
                    "Remove",

                    key=f"remove_cart_{i}"
                ):

                    st.session_state.cart.pop(
                        i
                    )

                    st.rerun()


        st.markdown("---")


        # ====================================================
        # CHECKOUT
        # ====================================================

        with st.form(
            "checkout_form"
        ):

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
