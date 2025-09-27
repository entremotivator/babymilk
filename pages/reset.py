# update_password_page.py

import streamlit as st
from supabase import create_client, Client

# Load Supabase credentials from Streamlit secrets
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_ANON_KEY"]

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

st.title("Update Your Password")

# Input new password
new_password = st.text_input("Enter your new password", type="password")

if st.button("Update Password"):
    if new_password:
        try:
            # Update user password for the currently logged-in user
            user = supabase.auth.update_user({"password": new_password})
            if user:
                st.success("Password updated successfully!")
            else:
                st.error("Failed to update password. Are you logged in?")
        except Exception as e:
            st.error(f"Error updating password: {str(e)}")
    else:
        st.warning("Please enter a new password.")
