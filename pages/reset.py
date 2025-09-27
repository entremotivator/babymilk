# update_password_page.py

import streamlit as st
import re
import requests
from supabase import create_client, Client
import time

# Load Supabase credentials from st.secrets
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_ANON_KEY"]

# Initialize client (needed for reset_password_for_email)
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def validate_email(email: str) -> bool:
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password: str):
    """Validate password strength"""
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    if not re.search(r"[A-Z]", password):
        return False, "Password must contain at least one uppercase letter"
    if not re.search(r"[a-z]", password):
        return False, "Password must contain at least one lowercase letter"
    if not re.search(r"\d", password):
        return False, "Password must contain at least one number"
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False, "Password must contain at least one special character"
    return True, ""

def reset_password(email: str):
    """Send password reset email"""
    try:
        supabase.auth.reset_password_for_email(
            email,
            redirect_to="https://yourapp.com/update-password"  # must match your page URL
        )
        return True, f"✅ Password reset email sent to {email}"
    except Exception as e:
        return False, f"❌ Reset error: {str(e)}"

# ---------------- UI ---------------- #

st.title("🔐 Password Reset")

query_params = st.query_params

# If no token in URL → show "request reset email"
if "access_token" not in query_params:
    st.subheader("Request a Reset Email")

    email_input = st.text_input("Enter your email address")
    if st.button("Send Reset Email"):
        if not email_input:
            st.error("Please enter your email")
        elif not validate_email(email_input):
            st.error("Invalid email format")
        else:
            success, msg = reset_password(email_input)
            if success:
                st.success(msg)
            else:
                st.error(msg)

# If token present → show password update form
else:
    st.subheader("Set a New Password")

    access_token = query_params["access_token"]

    new_password = st.text_input("New Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    if st.button("Update Password"):
        if not new_password or not confirm_password:
            st.error("Please fill in both password fields")
        elif new_password != confirm_password:
            st.error("Passwords do not match")
        else:
            is_valid, error_msg = validate_password(new_password)
            if not is_valid:
                st.error(error_msg)
            else:
                try:
                    # Call Supabase REST API directly
                    url = f"{SUPABASE_URL}/auth/v1/user"
                    headers = {
                        "apikey": SUPABASE_KEY,
                        "Authorization": f"Bearer {access_token}"
                    }
                    payload = {"password": new_password}

                    response = requests.put(url, headers=headers, json=payload)

                    if response.status_code == 200:
                        st.success("✅ Password updated successfully!")
                        st.balloons()
                        st.markdown("Redirecting to login page in 3 seconds...")
                        time.sleep(3)
                        st.switch_page("pages/login.py")  # adjust to your login page path
                    else:
                        error_detail = response.json()
                        st.error(f"❌ Failed to update password: {error_detail}")

                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")

