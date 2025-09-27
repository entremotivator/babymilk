# complete_password_reset.py
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

# Check URL parameters to determine which flow to show
query_params = st.query_params
has_reset_tokens = "access_token" in query_params and "refresh_token" in query_params

if has_reset_tokens:
    # PASSWORD UPDATE FLOW (from email link)
    st.title("🔐 Set Your New Password")
    st.markdown("Complete your password reset by entering your email and new password.")
    
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
        st.error("Please request a new password reset using the form below.")
        st.markdown("---")
        # Fall back to reset request form
        has_reset_tokens = False

if has_reset_tokens:
    # Password update form (only shown if tokens are valid)
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
                                    st.success("Session cleared. You can now login with your new password.")
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
                                st.info("Please request a new password reset using the form below")
                                # Show reset request form
                                st.query_params.clear()
                                st.rerun()
                            else:
                                st.error("Please try again or contact support if the issue persists")
                                
            except Exception as e:
                st.error(f"❌ Error verifying email: {str(e)}")

else:
    # PASSWORD RESET REQUEST FLOW (initial request)
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
                # Send password reset email
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
                    ### 📬 What happens next?
                    
                    1. **Check your email** - Look for our password reset message
                    2. **Click the reset link** - This will bring you back to this page
                    3. **Set your new password** - Enter and confirm your new password
                    4. **Start using your account** - Log in with your new password
                    
                    **⏰ Important:** The reset link will expire in 1 hour for security.
                    """)
                    
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

# Common sections for both flows
st.markdown("---")

# Help section
with st.expander("❓ Need Help?"):
    if has_reset_tokens:
        st.markdown("""
        **Password Update Issues:**
        - **Email doesn't match?** Use the same email you requested the reset with
        - **Password too weak?** Make sure it meets all requirements above
        - **Link expired?** Request a new password reset below
        
        **Still need help?**
        - Contact support for assistance
        """)
    else:
        st.markdown("""
        **Not receiving the reset email?**
        - Check your spam/junk mail folder
        - Make sure you entered the correct email address
        - Wait a few minutes - emails can sometimes be delayed
        - Try requesting another reset if it's been over 10 minutes
        
        **Don't have access to your email?**
        - Contact support for assistance
        
        **Remember your password?**
        - Go back to the login page
        """)

# Password security tips
with st.expander("🛡️ Password Security Best Practices"):
    st.markdown("""
    **Creating a Strong Password:**
    - Use at least 8 characters (longer is better)
    - Mix uppercase and lowercase letters
    - Include numbers and special characters
    - Avoid personal information (names, birthdays, etc.)
    - Consider using a passphrase (e.g., "Coffee$Morning123!")
    
    **Keeping Your Password Safe:**
    - Don't reuse passwords across multiple sites
    - Consider using a password manager
    - Never share your password with anyone
    - Log out of shared or public computers
    - Change your password if you suspect it's been compromised
    
    **Additional Security:**
    - Enable two-factor authentication if available
    - Keep your email account secure
    - Be cautious of phishing attempts
    """)

# Security notice
if has_reset_tokens:
    st.caption("🔒 **Security:** This reset link expires after use and cannot be shared. Keep your new password secure.")
else:
    st.caption("🔒 **Security Notice:** Reset links are single-use and expire after 1 hour. Never share reset links with others.")
