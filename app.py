# --- CART / CHECKOUT VIEW ---
else:
    st.subheader("🛒 Your Shopping Cart & Checkout")
    
    if st.session_state.cart:
        for c_idx, item in enumerate(st.session_state.cart):
            cc1, cc2 = st.columns([4, 1])
            with cc1:
                st.markdown(f"- **{item['product']}** ({item['quantity']})")
            with cc2:
                if st.button("Remove Item", key=f"rem_cart_view_{c_idx}"):
                    st.session_state.cart.pop(c_idx)
                    st.rerun()
        
        st.markdown("---")
        st.subheader("📍 Secure Checkout Form (UPI / Cash on Delivery)")
        
        # Placed INSIDE the form so the file and button sync perfectly together
        with st.form("checkout_form_main_view"):
            checkout_address = st.text_area("Delivery Address:")
            secondary_phone = st.text_input("Alternative Contact Number:", max_chars=10)
            product_desc = st.text_area("Product Specifications / Custom Description:")
            payment_method = st.selectbox("Payment Method", ["Cash on Delivery (COD)", "UPI Payment (GPay / PhonePe / Paytm)"])
            
            payment_screenshot = st.file_uploader(
                "Upload UPI Payment Screenshot (If paid via UPI)", 
                type=["jpg", "png", "jpeg"],
                help="200MB per file • JPG, PNG"
            )
            
            submit_checkout = st.form_submit_button("Complete Order & Send via WhatsApp")
            if submit_checkout:
                if checkout_address and secondary_phone:
                    screenshot_url = "No UPI Screenshot Provided"
                    if payment_screenshot is not None:
                        with st.spinner("Uploading payment screenshot..."):
                            hosted_url = upload_image_to_host(payment_screenshot)
                            if hosted_url:
                                screenshot_url = hosted_url
                    
                    cart_summary = ", ".join([f"{item['quantity']} of {item['product']}" for item in st.session_state.cart])
                    
                    st.session_state.pending_whatsapp_order = {
                        "name": st.session_state.logged_in_user,
                        "phone": st.session_state.user_phone,
                        "items": cart_summary,
                        "address": checkout_address,
                        "alt_phone": secondary_phone,
                        "desc": product_desc,
                        "payment": payment_method,
                        "screenshot": screenshot_url
                    }
                    st.success("✅ Order prepared! Click the WhatsApp button below to send your order.")
                else:
                    st.warning("⚠️ Please provide delivery address and secondary contact number.")

        if "pending_whatsapp_order" in st.session_state and st.session_state.pending_whatsapp_order:
            ord_info = st.session_state.pending_whatsapp_order
            raw_wa_message = (
                f"New Order - HM Mobiles\n"
                f"Customer: {ord_info['name']} ({ord_info['phone']})\n"
                f"Items: {ord_info['items']}\n"
                f"Address: {ord_info['address']}\n"
                f"Alt Phone: {ord_info['alt_phone']}\n"
                f"Description: {ord_info['desc']}\n"
                f"Payment: {ord_info['payment']}\n"
                f"Payment Proof Image URL: {ord_info['screenshot']}"
            )
            encoded_message = urllib.parse.quote(raw_wa_message)
            wa_url = f"https://wa.me/919840450113?text={encoded_message}"
            
            st.markdown("---")
            st.markdown("### 📲 Finalize Order via WhatsApp")
            
            if ord_info['screenshot'] != "No UPI Screenshot Provided" and "unsplash.com" not in ord_info['screenshot']:
                st.image(ord_info['screenshot'], caption="Uploaded Payment Screenshot", width=200)
                st.info("💡 Tip: You can save the image above to attach it directly in your WhatsApp chat.")
            
            st.markdown(f'<a href="{wa_url}" target="_blank"><button style="background-color: #25D366; color: white; padding: 12px 20px; border: none; border-radius: 8px; font-size: 16px; font-weight: 700; cursor: pointer; width: 100%;">💬 Click Here to Send Order on WhatsApp</button></a>', unsafe_allow_html=True)
            
            if st.button("Clear / Reset Cart & Finish"):
                st.session_state.cart = []
                st.session_state.pop("pending_whatsapp_order", None)
                st.session_state.current_view = "Home"
                st.rerun()

    else:
        st.info("Your cart is empty. Click **Home / Menu** above to browse products.")
