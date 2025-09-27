# reset_only_page.py
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

# Check URL parameters to see if this is a reset confirmation
query_params = st.query_params

# If we have reset parameters in the URL, show the password update form
if "access_token" in query_params and "refresh_token" in query_params:
    # This is the redirect from the reset email
    st.title("🔐 Set Your New Password")
    st.markdown("Complete your password reset by entering your new password below.")
    
    # Extract tokens from URL
    access_token = query_params["access_token"]
    refresh_token = query_params["refresh_token"]
    
    try:
        # Set the session using the tokens from the URL
        supabase.auth.set_session(access_token, refresh_token)
        
        # Password update form
        with st.form("new_password_form"):
            st.subheader("Enter Your New Password")
            
            # New password inputs
            new_password = st.text_input("New Password", type="password", 
                                       help="Must be at least 8 characters with uppercase, lowercase, number, and special character")
            confirm_password = st.text_input("Confirm New Password", type="password")
            
            # Show password requirements
            with st.expander("Password Requirements"):
                st.caption("• At least 8 characters long")
                st.caption("• Contains uppercase and lowercase letters")
                st.caption("• Contains at least one number")
                st.caption("• Contains at least one special character (!@#$%^&*(),.?\":{}|<>)")
            
            submit_button = st.form_submit_button("Update Password", type="primary")
        
        if submit_button:
            if not new_password:
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
                        # Update the user's password
                        result = supabase.auth.update_user({"password": new_password})
                        
                        if result.user:
                            st.success("✅ Password updated successfully!")
                            st.balloons()
                            st.markdown("""
                            **Success!** Your password has been reset.
                            
                            **What's next?**
                            - Your new password is now active
                            - You can log in with your new password
                            - This reset link is now expired for security
                            """)
                            
                            # Clear the URL parameters for security
                            if st.button("Continue to Login"):
                                st.query_params.clear()
                                st.rerun()
                        else:
                            st.error("❌ Failed to update password. Please try again.")
                            
                    except Exception as e:
                        st.error(f"❌ Error updating password: {str(e)}")
                        st.error("The reset link may have expired. Please request a new password reset.")
        
    except Exception as e:
        st.error("❌ Invalid or expired reset link")
        st.error("Please request a new password reset.")
        st.info("👇 Use the form below to send a new reset email")

else:
    # Show the initial password reset request form
    st.title("🔐 Reset Your Password")
    st.markdown("Enter your email address and we'll send you a secure link to reset your password.")

    # Email input form
    with st.form("password_reset_form"):
        st.subheader("Request Password Reset")
        
        email = st.text_input("Email Address", 
                            placeholder="your.email@example.com",
                            help="Enter the email address associated with your account")
        
        submit_button = st.form_submit_button("Send Reset Email", type="primary")

    if submit_button:
        if not email:
            st.error("Please enter your email address")
        elif not validate_email(email):
            st.error("Please enter a valid email address")
        else:
            try:
                # Send password reset email using the correct method
                response = supabase.auth.reset_password_email(
                    email,
                    {
                        'redirect_to': 'https://kewqjaq7qtyhhscc7regkc.streamlit.app/reset'
                    }
                )
                
                st.success("✅ Password reset email sent!")
                st.info(f"📧 Check your email at **{email}** for the reset link.")
                
                with st.container():
                    st.markdown("""
                    **What happens next?**
                    1. 📬 Check your email inbox (and spam folder)
                    2. 🔗 Click the secure reset link in the email
                    3. 🔐 You'll return here to set your new password
                    4. ✅ Log in with your new password
                    """)
                    
                st.warning("⏰ The reset link will expire in 1 hour for security.")
                
            except Exception as e:
                st.error(f"❌ Error sending reset email: {str(e)}")
                
                # Provide helpful error messages
                error_str = str(e).lower()
                if "invalid email" in error_str or "email not found" in error_str:
                    st.error("No account found with this email address")
                    st.info("Please check your email address or create a new account")
                elif "rate limit" in error_str:
                    st.error("Too many reset requests. Please wait before trying again.")
                else:
                    st.error("Please try again or contact support if the issue persists.")

# Help section
with st.expander("❓ Need Help?"):
    st.markdown("""
    **Not receiving the reset email?**
    - Check your spam/junk mail folder
    - Make sure you entered the correct email address
    - Wait a few minutes - emails can sometimes be delayed
    - Try requesting another reset if it's been over 10 minutes
    
    **Reset link not working?**
    - Make sure you're using the latest email
    - Reset links expire after 1 hour for security
    - Don't modify the URL - click directly from your email
    
    **Still having trouble?**
    - Contact support for assistance
    - Make sure your account exists with the email you're using
    """)

# Security notice
st.markdown("---")
st.caption("🔒 **Security Notice:** Reset links are single-use and expire after 1 hour. Never share reset links with others.")

# Additional security tips
with st.expander("🛡️ Password Security Best Practices"):
    st.markdown("""
    **Create a Strong Password:**
    - Use at least 8 characters (longer is better)
    - Mix uppercase and lowercase letters
    - Include numbers and special characters
    - Avoid personal information (names, birthdays, etc.)
    
    **Keep Your Password Safe:**
    - Don't reuse passwords across multiple sites
    - Consider using a password manager
    - Never share your password with anyone
    - Log out of shared or public computers
    - Change your password if you suspect it's been compromised
    """)
