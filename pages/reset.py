# update_password_page.py
import streamlit as st
import re
from supabase import create_client, Client

# Load Supabase credentials from Streamlit secrets
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_ANON_KEY"]

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password):
    """
    Validate password strength
    Returns (is_valid, error_message)
    """
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

# Check for reset tokens in URL parameters
query_params = st.query_params
has_tokens = "access_token" in query_params and "refresh_token" in query_params

if not has_tokens:
    st.error("❌ Invalid or missing reset tokens")
    st.error("This page can only be accessed through a password reset email link.")
    st.info("Please request a new password reset from the login page.")
    st.stop()

# Extract tokens
access_token = query_params["access_token"]
refresh_token = query_params["refresh_token"]

try:
    # Set the session using the tokens from the URL
    session_response = supabase.auth.set_session(access_token, refresh_token)
    
    if session_response.user:
        # Show the user's email for verification
        user_email = session_response.user.email
        st.info(f"📧 Resetting password for: **{user_email}**")
    
except Exception as e:
    st.error("❌ Invalid or expired reset link")
    st.error("Please request a new password reset.")
    st.stop()

# Password update form
with st.form("password_update_form"):
    st.subheader("Enter Your New Password")
    
    # Email verification input
    email_input = st.text_input(
        "Confirm Your Email Address",
        placeholder="Enter your email to verify",
        help="Enter the email address associated with your account"
    )
    
    # New password
    new_password = st.text_input(
        "New Password",
        type="password",
        help="Must meet security requirements listed below"
    )
    
    # Confirm new password
    confirm_password = st.text_input(
        "Confirm New Password",
        type="password"
    )
    
    # Password requirements
    with st.expander("🛡️ Password Requirements"):
        st.markdown("""
        - **Minimum 8 characters** long
        - **At least one uppercase letter** (A-Z)
        - **At least one lowercase letter** (a-z)
        - **At least one number** (0-9)
        - **At least one special character** (!@#$%^&*(),.?\":{}|<>)
        """)
    
    submit_button = st.form_submit_button("Update Password", type="primary")

if submit_button:
    # Validation checks
    if not email_input:
        st.error("Please enter your email address for verification")
    elif not validate_email(email_input):
        st.error("Please enter a valid email address")
    elif not new_password:
        st.error("Please enter a new password")
    elif not confirm_password:
        st.error("Please confirm your new password")
    elif new_password != confirm_password:
        st.error("Passwords do not match")
    else:
        # Check if email matches the session user
        try:
            current_user = supabase.auth.get_user()
            if current_user.user and current_user.user.email.lower() != email_input.lower():
                st.error("Email address doesn't match the reset request")
                st.error("Please enter the correct email address for this reset link")
            else:
                # Validate password strength
                is_valid, error_msg = validate_password(new_password)
                if not is_valid:
                    st.error(error_msg)
                else:
                    try:
                        # Update the user's password
                        result = supabase.auth.update_user({"password": new_password})
                        
                        if result.user:
                            st.success("✅ Password updated successfully!")
                            st.balloons()
                            
                            # Success message with next steps
                            st.markdown("""
                            ### 🎉 Password Reset Complete!
                            
                            Your password has been successfully updated. Here's what you need to know:
                            
                            **✅ What's done:**
                            - Your new password is now active
                            - The reset link has been used and is no longer valid
                            - Your account is secure
                            
                            **🚀 What's next:**
                            - You can now log in with your new password
                            - Make sure to store your password securely
                            - Consider enabling two-factor authentication if available
                            """)
                            
                            # Optional: Auto sign out for security
                            if st.button("🔓 Continue to Login", type="secondary"):
                                # Clear session and redirect
                                supabase.auth.sign_out()
                                st.query_params.clear()
                                st.success("Redirecting to login...")
                                st.rerun()
                                
                        else:
                            st.error("❌ Failed to update password")
                            st.error("Please try again or request a new reset link if the problem persists")
                            
                    except Exception as e:
                        st.error(f"❌ Error updating password: {str(e)}")
                        
                        # Handle specific error types
                        error_str = str(e).lower()
                        if "expired" in error_str or "invalid" in error_str:
                            st.error("The reset link has expired or is invalid")
                            st.info("Please request a new password reset")
                        else:
                            st.error("Please try again or contact support if the issue persists")
                            
        except Exception as e:
            st.error(f"❌ Error verifying email: {str(e)}")

# Security information
st.markdown("---")

# Additional tips
with st.expander("🔐 Password Security Tips"):
    st.markdown("""
    **Creating a Strong Password:**
    - Use a unique password you don't use elsewhere
    - Consider using a passphrase (e.g., "Coffee$Morning123!")
    - Avoid personal information like birthdays or names
    - Mix different types of characters
    
    **Keeping Your Password Safe:**
    - Use a password manager to store it securely
    - Never share your password with anyone
    - Log out of shared or public devices
    - Change your password if you suspect it's compromised
    
    **Additional Security:**
    - Enable two-factor authentication if available
    - Keep your email account secure
    - Be cautious of phishing attempts
    """)

# Help section
with st.expander("❓ Having Issues?"):
    st.markdown("""
    **Common Problems:**
    - **Link expired?** Reset links expire after 1 hour for security
    - **Email doesn't match?** Use the same email you requested the reset with
    - **Password too weak?** Make sure it meets all requirements above
    - **Page not loading?** Don't modify the URL, click directly from your email
    
    **Still need help?**
    - Request a new password reset
    - Contact support for assistance
    """)

# Security notice
st.caption("🔒 **Security:** This reset link expires after use and cannot be shared. Keep your new password secure.")
