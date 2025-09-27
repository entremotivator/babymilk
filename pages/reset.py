# update_password_page.py
import streamlit as st
import re
from supabase import create_client, Client

# Load Supabase credentials from Streamlit secrets
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_ANON_KEY"]

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

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

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

st.title("🔐 Set Your New Password")
st.markdown("Please enter your email and new password to complete the reset process.")

# Password update form
with st.form("password_update_form"):
    st.subheader("Reset Your Password")
    
    # Email confirmation
    email = st.text_input("Email Address", placeholder="your.email@example.com", help="Enter the email address associated with your account")
    
    # New password
    new_password = st.text_input("New Password", type="password", help="Must be at least 8 characters with uppercase, lowercase, number, and special character")
    
    # Confirm new password
    confirm_password = st.text_input("Confirm New Password", type="password")
    
    # Show password requirements
    st.caption("Password Requirements:")
    st.caption("• At least 8 characters long")
    st.caption("• Contains uppercase and lowercase letters")
    st.caption("• Contains at least one number")
    st.caption("• Contains at least one special character (!@#$%^&*(),.?\":{}|<>)")
    
    submit_button = st.form_submit_button("Update Password", type="primary")

if submit_button:
    # Validation checks
    if not email:
        st.error("Please enter your email address")
    elif not validate_email(email):
        st.error("Please enter a valid email address")
    elif not new_password:
        st.error("Please enter a new password")
    elif not confirm_password:
        st.error("Please confirm your new password")
    elif new_password != confirm_password:
        st.error("Passwords do not match")
    else:
        # Validate password strength
        is_valid, error_msg = validate_password(new_password)
        if not is_valid:
            st.error(error_msg)
        else:
            try:
                # Update user password using the reset token from URL params
                # The token should be automatically handled by Supabase from the email link
                result = supabase.auth.update_user({"password": new_password})
                
                if result.user:
                    st.success("✅ Password updated successfully!")
                    st.balloons()
                    st.markdown("""
                    **Success!** Your password has been updated.
                    
                    **What's next?**
                    - Your password is now active
                    - You can now log in with your new password
                    - Keep your password secure and don't share it with anyone
                    """)
                    
                    # Optional redirect info
                    st.info("You can now close this page and log in with your new password.")
                    
                else:
                    st.error("❌ Failed to update password.")
                    st.error("The reset link may have expired or already been used. Please request a new password reset.")
                        
            except Exception as e:
                st.error(f"❌ Error updating password: {str(e)}")
                
                # Provide helpful error messages based on common issues
                if "Invalid reset token" in str(e) or "expired" in str(e).lower():
                    st.error("The reset link has expired or is invalid. Please request a new password reset.")
                elif "User not found" in str(e):
                    st.error("User not found. Please check your email address.")
                else:
                    st.error("Please try again or request a new password reset if the issue persists.")

# Security information
with st.expander("🛡️ Password Security Tips"):
    st.markdown("""
    - **Use a unique password** that you don't use for other accounts
    - **Consider using a password manager** to generate and store strong passwords
    - **Don't share your password** with anyone
    - **Change your password regularly** (every 3-6 months)
    - **Avoid using personal information** like birthdays or names
    """)

# Help section
st.markdown("---")
st.caption("🔒 This reset link will expire for security purposes. If you're having trouble, please request a new password reset.")
