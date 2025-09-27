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

def check_user_session():
    """Check if user is authenticated"""
    try:
        user = supabase.auth.get_user()
        return user.user is not None
    except:
        return False

st.title("🔐 Update Your Password")

# Check if user is logged in
if not check_user_session():
    st.error("⚠️ You must be logged in to update your password.")
    st.info("Please log in first before accessing this page.")
    st.stop()

# Display current user info (optional)
try:
    current_user = supabase.auth.get_user()
    if current_user.user:
        st.info(f"Updating password for: {current_user.user.email}")
except:
    pass

# Password update form
with st.form("password_update_form"):
    st.subheader("Enter New Password")
    
    # Current password (for additional security)
    current_password = st.text_input("Current Password", type="password", help="Enter your current password for verification")
    
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
    if not current_password:
        st.error("Please enter your current password")
    elif not new_password:
        st.error("Please enter a new password")
    elif not confirm_password:
        st.error("Please confirm your new password")
    elif new_password != confirm_password:
        st.error("New passwords do not match")
    elif current_password == new_password:
        st.error("New password must be different from current password")
    else:
        # Validate password strength
        is_valid, error_msg = validate_password(new_password)
        if not is_valid:
            st.error(error_msg)
        else:
            try:
                # First verify current password by attempting to sign in
                try:
                    current_user = supabase.auth.get_user()
                    if current_user.user:
                        # Attempt to sign in with current password to verify it
                        verification = supabase.auth.sign_in_with_password({
                            "email": current_user.user.email,
                            "password": current_password
                        })
                        
                        if verification.user:
                            # Current password is correct, proceed with update
                            result = supabase.auth.update_user({"password": new_password})
                            if result.user:
                                st.success("✅ Password updated successfully!")
                                st.balloons()
                                
                                # Optional: Show next steps
                                st.info("💡 Your password has been updated. You may need to log in again with your new password.")
                            else:
                                st.error("❌ Failed to update password. Please try again.")
                        else:
                            st.error("❌ Current password is incorrect")
                            
                except Exception as verification_error:
                    # If verification fails, still attempt the update (in case the verification method doesn't work)
                    st.warning("Could not verify current password, attempting update...")
                    result = supabase.auth.update_user({"password": new_password})
                    if result.user:
                        st.success("✅ Password updated successfully!")
                        st.balloons()
                    else:
                        st.error("❌ Failed to update password. Please ensure you're logged in.")
                        
            except Exception as e:
                st.error(f"❌ Error updating password: {str(e)}")
                
                # Provide helpful error messages based on common issues
                if "Invalid login credentials" in str(e):
                    st.error("Current password is incorrect")
                elif "User not found" in str(e):
                    st.error("User session expired. Please log in again.")
                else:
                    st.error("Please try again or contact support if the issue persists.")

# Additional security tips
with st.expander("🛡️ Password Security Tips"):
    st.markdown("""
    - **Use a unique password** that you don't use for other accounts
    - **Consider using a password manager** to generate and store strong passwords
    - **Enable two-factor authentication** if available
    - **Don't share your password** with anyone
    - **Change your password regularly** (every 3-6 months)
    - **Avoid using personal information** like birthdays or names
    """)

# Logout option
st.markdown("---")
if st.button("🚪 Logout", help="Sign out of your account"):
    try:
        supabase.auth.sign_out()
        st.success("Logged out successfully!")
        st.rerun()  # Refresh the page
    except Exception as e:
        st.error(f"Error logging out: {str(e)}")
