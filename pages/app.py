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
            response = supabase.auth.admin.list_users()
            
            # The response might be structured differently depending on the version
            # Try accessing users as an attribute or key
            if hasattr(response, 'users'):
                users_list = response.users
            elif isinstance(response, dict) and 'users' in response:
                users_list = response['users']
            else:
                users_list = response
            
            # Find the target user
            target_user = next((u for u in users_list if u.email == email or (isinstance(u, dict) and u.get("email") == email)), None)
            
            if target_user:
                # Get user ID (handle both object and dict formats)
                user_id = target_user.id if hasattr(target_user, 'id') else target_user['id']
                
                # 2. Update password
                updated = supabase.auth.admin.update_user_by_id(
                    user_id,
                    {"password": new_password}
                )
                st.success(f"✅ Password updated successfully for {email}")
                st.json(updated if isinstance(updated, dict) else updated.__dict__)
            else:
                st.error("❌ User not found")
                st.info(f"Debug: Found {len(users_list)} total users")
        except Exception as e:
            st.error(f"Error: {e}")
            st.info("Try checking the Supabase client version and API response structure")
