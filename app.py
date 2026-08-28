import os
import streamlit as st

# Example product dictionary containing a raw image string from Google Sheets
prod = {
    "name": "Bluetooth Wireless Headset",
    "image": "images/Headset 1 1.jpg \\ images/Headset 1 2.jpg \\ images/Headset 1 3.jpg"
}

# Unique session state key for the image slider index
slide_key = "product_image_index"
if slide_key not in st.session_state:
    st.session_state[slide_key] = 0

# 1. Parse and sanitize image paths (handles both backslash and comma separators)
raw_img = prod.get("image", "")
if raw_img:
    # Split string by common delimiters used in your sheet
    img_paths = [img.strip() for img in raw_img.replace("\\", ",").split(",") if img.strip()]
    
    # Filter for paths that actually exist on disk
    valid_paths = [p for p in img_paths if os.path.exists(p)]
    
    if valid_paths:
        total_imgs = len(valid_paths)
        current_idx = st.session_state[slide_key]
        
        # 2. Layout carousel controls and display frame
        l_btn, img_display, r_btn = st.columns([0.5, 4, 0.5])
        
        with l_btn:
            st.markdown("<div style='height: 50px;'></div>", unsafe_allow_html=True)
            if st.button("‹", key="prev_img"):
                st.session_state[slide_key] = (current_idx - 1) % total_imgs
                st.rerun()
                
        with img_display:
            # Display current image centered with a fixed display width
            _, center_col, _ = st.columns([1, 3, 1])
            with center_col:
                st.image(valid_paths[current_idx], use_container_width=True)
            st.caption(f"Image {current_idx + 1} of {total_imgs}")
            
        with r_btn:
            st.markdown("<div style='height: 50px;'></div>", unsafe_allow_html=True)
            if st.button("›", key="next_img"):
                st.session_state[slide_key] = (current_idx + 1) % total_imgs
                st.rerun()
    else:
        st.info("No valid image files found on disk.")
else:
    st.caption("No image provided.")
