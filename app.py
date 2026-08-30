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
# CSS (VIBRANT, PROFESSIONAL, ZERO-GAP STYLING & CLEAN IMAGE RENDERING)
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
   AUTO-ADJUSTING THUMBNAIL SIZING & DELETING STRAY ARTIFACTS
   ============================================================ */

[data-testid="stImage"] img {
    width: 100% !important;
    height: 60px !important;
    object-fit: contain !important;
    border-radius: 3px;
    display: block;
    margin: auto;
}

/* Hide any numerical counter or string label automatically generated next to images */
[data-testid="stImageCaption"] {
    display: none !important;
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
    background: linear-gradient(135deg
