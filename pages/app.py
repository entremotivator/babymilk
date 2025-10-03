import streamlit as st
from supabase import create_client

# Initialize Supabase client with service role key
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_SERVICE_ROLE_KEY = st.secrets["SUPABASE_SERVICE_ROLE_KEY"]

supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)

# Page UI
st.title("🔑 Supabase Admin - Update User Password")

# Placeholders from what you gave me
email = st.text_input("User Email", value="Blitzmakzhitz@gmail.com")
new_password = st.text_input("New Password", type="password", value="12345agentkit")

if st.button("Update Password"):
    if not email or not new_password:
        st.warning("⚠️ Please enter both email and new password.")
    else:
        try:
            # 1. List all users and find the one with this email
            users = supabase.auth.admin.list_users()
            target_user = next((u for u in users["users"] if u["email"] == email), None)

            if target_user:
                # 2. Update password
                updated = supabase.auth.admin.update_user_by_id(
                    target_user["id"],
                    {"password": new_password}
                )
                st.success(f"✅ Password updated successfully for {email}")
                st.json(updated)
            else:
                st.error("❌ User not found")
        except Exception as e:
            st.error(f"Error: {e}")
