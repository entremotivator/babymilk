# pages/forgot_password.py

import streamlit as st
import re
import requests
import time
from supabase import create_client, Client
from typing import Tuple, Optional

# Load Supabase credentials from st.secrets
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_ANON_KEY"]

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Page configuration
st.set_page_config(
    page_title="Forgot Password",
    page_icon="🔐",
    layout="centered"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
    }
    .success-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        margin: 1rem 0;
    }
    .error-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
        margin: 1rem 0;
    }
    .info-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        color: #0c5460;
        margin: 1rem 0;
    }
    .password-requirements {
        font-size: 0.9rem;
        color: #666;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)


# ---------------- Helper Functions ---------------- #

def validate_email(email: str) -> bool:
    """Validate email format using regex pattern"""
    if not email:
        return False
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_password(password: str) -> Tuple[bool, str]:
    """
    Validate password strength requirements
    Returns: (is_valid, error_message)
    """
    if not password:
        return False, "Password is required"
    
    requirements = []
    
    if len(password) < 8:
        requirements.append("at least 8 characters long")
    if not re.search(r"[A-Z]", password):
        requirements.append("at least one uppercase letter")
    if not re.search(r"[a-z]", password):
        requirements.append("at least one lowercase letter")
    if not re.search(r"\d", password):
        requirements.append("at least one number")
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        requirements.append("at least one special character (!@#$%^&*(),.?\":{}|<>)")
    
    if requirements:
        return False, f"Password must contain {', '.join(requirements)}"
    
    return True, ""


def send_reset_email(email: str) -> Tuple[bool, str]:
    """
    Send password reset email using Supabase
    Returns: (success, message)
    """
    try:
        # Note: redirect_to URL should be configured in Supabase dashboard
        # under Authentication > URL Configuration > Site URL
        response = supabase.auth.reset_password_for_email(email)
        return True, f"Password reset email sent to {email}. Please check your inbox and spam folder."
    except Exception as e:
        error_msg = str(e)
        if "not found" in error_msg.lower():
            # Don't reveal if email exists for security reasons
            return True, f"If {email} is registered, you will receive a password reset email."
        return False, f"Failed to send reset email: {error_msg}"


def update_password_with_token(access_token: str, new_password: str) -> Tuple[bool, str]:
    """
    Update user password using access token from reset email
    Returns: (success, message)
    """
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
            error_detail = response.json() if response.content else {"message": "Unknown error"}
            error_msg = error_detail.get("message", "Failed to update password")
            return False, f"Error: {error_msg}"
            
    except requests.RequestException as e:
        return False, f"Network error: {str(e)}"
    except Exception as e:
        return False, f"Unexpected error: {str(e)}"


def display_password_requirements():
    """Display password requirements in a formatted box"""
    st.markdown("""
    <div class="password-requirements">
    <strong>Password Requirements:</strong>
    <ul>
        <li>At least 8 characters long</li>
        <li>At least one uppercase letter (A-Z)</li>
        <li>At least one lowercase letter (a-z)</li>
        <li>At least one number (0-9)</li>
        <li>At least one special character (!@#$%^&*(),.?":{}|<>)</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)


def show_loading_message():
    """Show a loading spinner with message"""
    with st.spinner("Processing your request..."):
        time.sleep(1)


# ---------------- Main Application Logic ---------------- #

def main():
    """Main application logic"""
    
    # Header
    st.markdown('<h1 class="main-header">🔐 Forgot Password</h1>', unsafe_allow_html=True)
    
    # Get query parameters
    query_params = st.query_params
    access_token = query_params.get("access_token")
    token_type = query_params.get("type")
    
    # Initialize session state
    if "reset_email_sent" not in st.session_state:
        st.session_state.reset_email_sent = False
    if "password_updated" not in st.session_state:
        st.session_state.password_updated = False
    
    # Case 1: User has clicked reset link (has access token)
    if access_token and token_type == "recovery":
        handle_password_reset(access_token)
    
    # Case 2: Request password reset email
    else:
        handle_reset_request()


def handle_reset_request():
    """Handle the initial password reset request"""
    
    st.subheader("Reset Your Password")
    st.markdown("Enter your email address and we'll send you a link to reset your password.")
    
    # Email input form
    with st.form("reset_request_form"):
        email = st.text_input(
            "Email Address",
            placeholder="Enter your email address",
            help="We'll send a password reset link to this email"
        )
        
        submit_button = st.form_submit_button("Send Reset Email", use_container_width=True)
        
        if submit_button:
            if not email:
                st.error("Please enter your email address")
            elif not validate_email(email):
                st.error("Please enter a valid email address")
            else:
                show_loading_message()
                success, message = send_reset_email(email)
                
                if success:
                    st.session_state.reset_email_sent = True
                    st.success(message)
                    st.markdown("""
                    <div class="info-box">
                    <strong>Next Steps:</strong>
                    <ol>
                        <li>Check your email inbox (and spam folder)</li>
                        <li>Click the reset link in the email</li>
                        <li>Create your new password</li>
                    </ol>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.error(message)
    
    # Show additional help information
    if not st.session_state.reset_email_sent:
        st.markdown("---")
        st.markdown("### Need Help?")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Didn't receive the email?**")
            st.markdown("• Check your spam/junk folder")
            st.markdown("• Make sure you entered the correct email")
            st.markdown("• Wait a few minutes and try again")
        
        with col2:
            st.markdown("**Remember your password?**")
            if st.button("Back to Login", use_container_width=True):
                try:
                    st.switch_page("pages/login.py")
                except:
                    st.info("Please navigate to the login page")


def handle_password_reset(access_token: str):
    """Handle password reset when user clicks the email link"""
    
    st.subheader("Create New Password")
    st.markdown("Please enter your new password below.")
    
    # Password reset form
    with st.form("password_reset_form"):
        new_password = st.text_input(
            "New Password",
            type="password",
            placeholder="Enter your new password"
        )
        
        confirm_password = st.text_input(
            "Confirm New Password",
            type="password",
            placeholder="Confirm your new password"
        )
        
        # Show password requirements
        display_password_requirements()
        
        submit_button = st.form_submit_button("Update Password", use_container_width=True)
        
        if submit_button:
            # Validate inputs
            if not new_password or not confirm_password:
                st.error("Please fill in both password fields")
            elif new_password != confirm_password:
                st.error("Passwords do not match")
            else:
                # Validate password strength
                is_valid, error_msg = validate_password(new_password)
                if not is_valid:
                    st.error(error_msg)
                else:
                    # Update password
                    show_loading_message()
                    success, message = update_password_with_token(access_token, new_password)
                    
                    if success:
                        st.session_state.password_updated = True
                        st.success(message)
                        st.balloons()
                        
                        # Show success message and redirect info
                        st.markdown("""
                        <div class="success-box">
                        <strong>Success!</strong> Your password has been updated successfully.
                        <br>You can now log in with your new password.
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Auto-redirect countdown
                        placeholder = st.empty()
                        for i in range(5, 0, -1):
                            placeholder.info(f"Redirecting to login page in {i} seconds...")
                            time.sleep(1)
                        
                        try:
                            st.switch_page("pages/login.py")
                        except:
                            st.info("👉 Please navigate to the login page manually.")
                    else:
                        st.error(message)
    
    # Manual navigation option
    if st.session_state.password_updated:
        if st.button("Go to Login Page", use_container_width=True):
            try:
                st.switch_page("pages/login.py")
            except:
                st.info("Please navigate to the login page manually.")


# ---------------- Run the Application ---------------- #

if __name__ == "__main__":
    main()
