# update_password_page.py

import streamlit as st
import re
import requests

# Load Supabase credentials from Streamlit secrets
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_ANON_KEY"]

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

st.title("🔐 Set Your New Password")
st.markdown("Complete your password reset by entering your email and new password.")

# ✅ Get token from URL
query_params = st.query_params
if "access_token" not in query_params:
    st.error("❌ Invalid or missing reset token")
    st.info("Please request a new password reset from the login page.")
    st.stop()

access_token = query_params["access_token"]

# Password update form
with st.form("password_update_form"):
    st.subheader("Enter Your New Password")

    email_input = st.text_input("Confirm Your Email Address", placeholder="Enter your email")

    new_password = st.text_input("New Password", type="password")
    confirm_password = st.text_input("Confirm New Password", type="password")

    with st.expander("🛡️ Password Requirements"):
        st.markdown("""
        - Minimum **8 characters**  
        - At least **one uppercase** (A-Z)  
        - At least **one lowercase** (a-z)  
        - At least **one number** (0-9)  
        - At least **one special character** (!@#$%^&*...)  
        """)

    submit_button = st.form_submit_button("Update Password", type="primary")

if submit_button:
    # Validation checks
    if not email_input:
        st.error("Please enter your email address")
    elif not validate_email(email_input):
        st.error("Invalid email address format")
    elif not new_password or not confirm_password:
        st.error("Please fill in both password fields")
    elif new_password != confirm_password:
        st.error("Passwords do not match")
    else:
        # Password strength
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
                    st.markdown("""
                    ### 🎉 Password Reset Complete!
                    You can now log in with your new password.  
                    """)
                else:
                    error_detail = response.json()
                    st.error(f"❌ Failed to update password: {error_detail}")

            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

# Extra security info
st.markdown("---")
with st.expander("🔐 Password Security Tips"):
    st.markdown("""
    - Use a unique password you don't reuse elsewhere  
    - Consider a passphrase (e.g., `Coffee$Morning123!`)  
    - Store passwords in a manager, not your memory  
    - Enable 2FA if available  
    """)
