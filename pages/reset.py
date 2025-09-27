# simple_password_reset.py

import streamlit as st
import re
import requests
from supabase import create_client, Client
from typing import Tuple

# Load Supabase credentials
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_ANON_KEY"]

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Page configuration
st.set_page_config(
    page_title="Reset Password",
    page_icon="🔐",
    layout="centered"
)

# Simple CSS styling
st.markdown("""
<style>
    .main-container {
        max-width: 500px;
        margin: 2rem auto;
        padding: 2rem;
        background: #f8f9fa;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    .stButton > button {
        width: 100%;
        background-color: #007bff;
        color: white;
        border: none;
        padding: 0.75rem;
        border-radius: 5px;
        font-weight: bold;
    }
    .stButton > button:hover {
        background-color: #0056b3;
    }
    .password-requirements {
        font-size: 0.9rem;
        color: #666;
        background: #e9ecef;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)


def validate_email(email: str) -> bool:
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_password(password: str) -> Tuple[bool, str]:
    """Validate password strength"""
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    if not re.search(r"[A-Z]", password):
        return False, "Password must contain at least one uppercase letter"
    if not re.search(r"[a-z]", password):
        return False, "Password must contain at least one lowercase letter"
    if not re.search(r"\d", password):
        return False, "Password must contain at least one number"
    return True, ""


def send_reset_email(email: str) -> Tuple[bool, str]:
    """Send password reset email"""
    try:
        supabase.auth.reset_password_for_email(email)
        return True, f"Password reset email sent to {email}"
    except Exception as e:
        return False, f"Error sending reset email: {str(e)}"


def update_password(access_token: str, new_password: str) -> Tuple[bool, str]:
    """Update password using access token"""
    try:
        url = f"{SUPABASE_URL}/auth/v1/user"
        headers = {
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        payload = {"password": new_password}
        
        response = requests.put(url, headers=headers, json=payload)
        
        if response.status_code == 200:
            return True, "Password updated successfully!"
        else:
            return False, "Failed to update password"
            
    except Exception as e:
        return False, f"Error updating password: {str(e)}"


def main():
    """Main application"""
    
    st.title("🔐 Reset Password")
    
    # Check if we have an access token from the reset email link
    query_params = st.query_params
    access_token = query_params.get("access_token")
    
    if access_token:
        # Step 2: Password change form
        st.subheader("Enter New Password")
        
        with st.form("password_form"):
            new_password = st.text_input("New Password", type="password")
            confirm_password = st.text_input("Confirm Password", type="password")
            
            # Show password requirements
            st.markdown("""
            <div class="password-requirements">
                <strong>Password Requirements:</strong><br>
                • At least 8 characters<br>
                • One uppercase letter<br>
                • One lowercase letter<br>
                • One number
            </div>
            """, unsafe_allow_html=True)
            
            submit = st.form_submit_button("Update Password")
            
            if submit:
                if not new_password or not confirm_password:
                    st.error("Please fill in both password fields")
                elif new_password != confirm_password:
                    st.error("Passwords do not match")
                else:
                    is_valid, error_msg = validate_password(new_password)
                    if not is_valid:
                        st.error(error_msg)
                    else:
                        success, message = update_password(access_token, new_password)
                        if success:
                            st.success(message)
                            st.balloons()
                            st.info("You can now close this page and log in with your new password")
                        else:
                            st.error(message)
    
    else:
        # Step 1: Email input form
        st.subheader("Enter Your Email")
        st.write("We'll send you a link to reset your password")
        
        with st.form("email_form"):
            email = st.text_input("Email Address", placeholder="your@email.com")
            
            submit = st.form_submit_button("Send Reset Email")
            
            if submit:
                if not email:
                    st.error("Please enter your email address")
                elif not validate_email(email):
                    st.error("Please enter a valid email address")
                else:
                    success, message = send_reset_email(email)
                    if success:
                        st.success(message)
                        st.info("Check your email and click the reset link to continue")
                    else:
                        st.error(message)


if __name__ == "__main__":
    main()
