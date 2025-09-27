import requests
import streamlit as st
from supabase import create_client, Client

# Add this to your imports at the top of your file

# Replace your existing reset_password function with this:
def reset_password(email):
    """Reset password using Supabase REST API"""
    try:
        # Get Supabase credentials
        url = st.secrets["supabase"]["url"]
        anon_key = st.secrets["supabase"]["key"]
        
        # Supabase Auth REST API endpoint
        reset_url = f"{url}/auth/v1/recover"
        
        headers = {
            "apikey": anon_key,
            "Content-Type": "application/json"
        }
        
        payload = {
            "email": email
        }
        
        response = requests.post(reset_url, headers=headers, json=payload)
        
        if response.status_code == 200:
            return True, f"Password reset email sent to {email}"
        else:
            # Handle specific error cases
            if response.status_code == 400:
                return False, "Invalid email address"
            elif response.status_code == 429:
                return False, "Too many requests. Please try again later."
            else:
                return False, f"Failed to send reset email. Please try again."
                
    except Exception as e:
        return False, f"Reset error: {str(e)}"

# Add this new function for updating passwords (if needed elsewhere in your app)
def update_user_password(user_id, new_password):
    """Update user password directly (admin function)"""
    try:
        # Use Supabase client to update password
        supabase.auth.admin.update_user_by_id(
            user_id, 
            {"password": new_password}
        )
        return True, "Password updated successfully"
    except Exception as e:
        return False, f"Failed to update password: {str(e)}"

# Updated profile form section - replace the security section in show_user_profile():
def show_user_profile_security_section():
    """Security section for user profile with proper password change"""
    st.write("**Change Password**")
    
    with st.form("password_change_form"):
        current_password = st.text_input("Current Password", type="password", key="current_pw")
        new_password = st.text_input("New Password", type="password", key="new_pw")
        confirm_password = st.text_input("Confirm New Password", type="password", key="confirm_pw")
        
        if st.form_submit_button("Update Password", key="update_password_btn"):
            if not all([current_password, new_password, confirm_password]):
                st.error("Please fill in all password fields")
            elif new_password != confirm_password:
                st.error("New passwords don't match")
            elif len(new_password) < 6:
                st.error("Password must be at least 6 characters long")
            else:
                # First verify current password by attempting to sign in
                try:
                    # Use current user's email
                    user_email = st.session_state.user.email
                    
                    # Verify current password
                    verify_response = supabase.auth.sign_in_with_password({
                        "email": user_email, 
                        "password": current_password
                    })
                    
                    if verify_response.user:
                        # Current password is correct, now update to new password
                        update_response = supabase.auth.update_user({
                            "password": new_password
                        })
                        
                        if update_response.user:
                            st.success("Password updated successfully!")
                        else:
                            st.error("Failed to update password")
                    else:
                        st.error("Current password is incorrect")
                        
                except Exception as e:
                    if "Invalid login credentials" in str(e):
                        st.error("Current password is incorrect")
                    else:
                        st.error(f"Error updating password: {str(e)}")

# Alternative simpler approach using password reset for password changes:
def trigger_password_reset_for_user():
    """Trigger password reset for current user"""
    if st.session_state.user and st.session_state.user.email:
        success, message = reset_password(st.session_state.user.email)
        if success:
            st.success("Password reset email sent! Check your inbox.")
            st.info("You'll receive a secure link to set your new password.")
        else:
            st.error(message)
    else:
        st.error("Unable to send reset email. Please try logging out and back in.")

# Updated user profile function with the security section:
def show_user_profile_updated(user_id, user_email):
    """Updated user profile with working password change"""
    st.subheader("Your Profile")
    
    with st.form("profile_form"):
        st.write("**Personal Information**")
        full_name = st.text_input("Full Name", value="")
        phone = st.text_input("Phone Number", value="")
        bio = st.text_area("Bio", value="")
        
        st.write("**Preferences**")
        theme = st.selectbox("Theme", ["Dark (AI Agent Toolkit)", "Light", "Auto"])
        notifications = st.checkbox("Email notifications", value=True)
        newsletter = st.checkbox("Subscribe to newsletter", value=False)
        
        if st.form_submit_button("Save Preferences", type="primary", key="save_prefs"):
            st.success("Profile preferences updated!")
    
    # Separate section for password change
    st.markdown("---")
    st.subheader("Change Password")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Option 1: Reset via Email**")
        st.write("The safest way to change your password")
        if st.button("Send Password Reset Email", type="primary", key="reset_email_btn"):
            trigger_password_reset_for_user()
    
    with col2:
        st.write("**Option 2: Change Directly**")
        with st.form("direct_password_change"):
            current_pw = st.text_input("Current Password", type="password")
            new_pw = st.text_input("New Password", type="password") 
            confirm_pw = st.text_input("Confirm Password", type="password")
            
            if st.form_submit_button("Change Password", key="direct_change"):
                if not all([current_pw, new_pw, confirm_pw]):
                    st.error("Please fill all fields")
                elif new_pw != confirm_pw:
                    st.error("Passwords don't match")
                elif len(new_pw) < 6:
                    st.error("Password must be at least 6 characters")
                else:
                    try:
                        # Update password using Supabase auth
                        response = supabase.auth.update_user({"password": new_pw})
                        if response.user:
                            st.success("Password changed successfully!")
                        else:
                            st.error("Failed to change password")
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
