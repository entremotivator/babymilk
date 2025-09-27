import streamlit as st
from supabase import create_client, Client
import requests

# Initialize Supabase connection
@st.cache_resource
def init_connection():
    """Initialize Supabase connection"""
    try:
        url = st.secrets["supabase"]["url"]
        key = st.secrets["supabase"]["key"]
        return create_client(url, key)
    except Exception as e:
        st.error(f"Failed to connect to Supabase: {e}")
        st.stop()

supabase = init_connection()

# Initialize session state
if "authenticated" not in st.session_state:
    st.session_state.authenticated = True  # Set to True for testing
if "user" not in st.session_state:
    st.session_state.user = {"email": "user@example.com", "id": "123"}  # Mock user for testing

def apply_custom_css():
    """Apply styling for password change page"""
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #334155 100%);
        color: #ffffff;
        font-family: 'Inter', sans-serif;
    }
    
    .stMarkdown, .stText, p, span, div {
        color: #ffffff !important;
        font-family: 'Inter', sans-serif;
    }
    
    h1, h2, h3, h4, h5, h6 {
        color: #f59e0b !important;
        font-weight: 600;
        font-family: 'Inter', sans-serif;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
        color: #000000;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        font-family: 'Inter', sans-serif;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(245, 158, 11, 0.3);
        width: 100%;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #d97706 0%, #b45309 100%);
        box-shadow: 0 6px 20px rgba(245, 158, 11, 0.5);
        transform: translateY(-2px);
    }
    
    .stTextInput > div > div > input {
        background-color: rgba(30, 41, 59, 0.8);
        border: 2px solid #475569;
        border-radius: 12px;
        color: #ffffff !important;
        font-family: 'Inter', sans-serif;
        padding: 0.75rem;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #f59e0b;
        box-shadow: 0 0 0 3px rgba(245, 158, 11, 0.2);
        background-color: rgba(30, 41, 59, 1);
    }
    
    .password-container {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.95) 0%, rgba(51, 65, 85, 0.95) 100%);
        padding: 3rem;
        border-radius: 20px;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
        border: 1px solid #475569;
        margin: 2rem 0;
        backdrop-filter: blur(20px);
    }
    
    .success-message {
        background: linear-gradient(135deg, rgba(34, 197, 94, 0.2) 0%, rgba(16, 185, 129, 0.2) 100%);
        border: 1px solid #22c55e;
        color: #86efac !important;
        padding: 1rem;
        border-radius: 12px;
        margin: 1rem 0;
    }
    
    .error-message {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.2) 0%, rgba(220, 38, 38, 0.2) 100%);
        border: 1px solid #ef4444;
        color: #fca5a5 !important;
        padding: 1rem;
        border-radius: 12px;
        margin: 1rem 0;
    }
    
    .info-box {
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.2) 0%, rgba(99, 102, 241, 0.2) 100%);
        border: 1px solid #3b82f6;
        color: #93c5fd !important;
        padding: 1rem;
        border-radius: 12px;
        margin: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)

def reset_password_via_email(email):
    """Send password reset email using Supabase REST API"""
    try:
        url = st.secrets["supabase"]["url"]
        anon_key = st.secrets["supabase"]["key"]
        
        reset_url = f"{url}/auth/v1/recover"
        headers = {
            "apikey": anon_key,
            "Content-Type": "application/json"
        }
        payload = {"email": email}
        
        response = requests.post(reset_url, headers=headers, json=payload)
        
        if response.status_code == 200:
            return True, "Password reset email sent successfully"
        elif response.status_code == 400:
            return False, "Invalid email address"
        elif response.status_code == 429:
            return False, "Too many requests. Please try again later"
        else:
            return False, "Failed to send reset email"
            
    except Exception as e:
        return False, f"Error: {str(e)}"

def change_password_direct(new_password):
    """Change password directly using Supabase auth"""
    try:
        response = supabase.auth.update_user({"password": new_password})
        if response.user:
            return True, "Password changed successfully"
        else:
            return False, "Failed to change password"
    except Exception as e:
        return False, f"Error changing password: {str(e)}"

def password_change_page():
    """Main password change page"""
    
    # Apply styling
    apply_custom_css()
    
    # Header
    st.markdown("""
    <div style="text-align: center; margin: 2rem 0;">
        <h1>🔐 Change Your Password</h1>
        <p>Update your account password securely</p>
    </div>
    """, unsafe_allow_html=True)
    
    # User info display
    if st.session_state.user:
        st.markdown(f"""
        <div class="info-box">
            <strong>Current User:</strong> {st.session_state.user['email']}
        </div>
        """, unsafe_allow_html=True)
    
    # Create two columns for different password change methods
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="password-container">
        """, unsafe_allow_html=True)
        
        st.subheader("📧 Method 1: Email Reset")
        st.markdown("**Recommended - Most Secure**")
        st.write("We'll send a secure reset link to your email address.")
        
        with st.form("email_reset_form", clear_on_submit=True):
            email_input = st.text_input(
                "Email Address", 
                value=st.session_state.user['email'] if st.session_state.user else "",
                help="Enter your registered email address"
            )
            
            if st.form_submit_button("Send Reset Email", type="primary"):
                if email_input:
                    success, message = reset_password_via_email(email_input)
                    if success:
                        st.markdown(f'<div class="success-message">✅ {message}</div>', unsafe_allow_html=True)
                        st.info("Check your inbox and spam folder for the reset link.")
                    else:
                        st.markdown(f'<div class="error-message">❌ {message}</div>', unsafe_allow_html=True)
                else:
                    st.markdown('<div class="error-message">❌ Please enter your email address</div>', unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="password-container">
        """, unsafe_allow_html=True)
        
        st.subheader("🔑 Method 2: Direct Change")
        st.markdown("**Quick Change - Current Session**")
        st.write("Change your password immediately without email verification.")
        
        with st.form("direct_change_form", clear_on_submit=True):
            new_password = st.text_input(
                "New Password", 
                type="password",
                help="Must be at least 6 characters long"
            )
            confirm_password = st.text_input(
                "Confirm New Password", 
                type="password",
                help="Re-enter your new password"
            )
            
            # Password strength indicator
            if new_password:
                strength_score = 0
                if len(new_password) >= 6:
                    strength_score += 1
                if any(c.isupper() for c in new_password):
                    strength_score += 1
                if any(c.islower() for c in new_password):
                    strength_score += 1
                if any(c.isdigit() for c in new_password):
                    strength_score += 1
                if any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in new_password):
                    strength_score += 1
                
                strength_colors = ["red", "orange", "yellow", "lightgreen", "green"]
                strength_labels = ["Very Weak", "Weak", "Fair", "Good", "Strong"]
                
                if strength_score > 0:
                    st.markdown(f"""
                    <div style="margin: 0.5rem 0;">
                        <small>Password Strength: 
                        <span style="color: {strength_colors[min(strength_score-1, 4)]}">
                        {strength_labels[min(strength_score-1, 4)]}
                        </span></small>
                    </div>
                    """, unsafe_allow_html=True)
            
            if st.form_submit_button("Change Password", type="primary"):
                if not new_password or not confirm_password:
                    st.markdown('<div class="error-message">❌ Please fill in both password fields</div>', unsafe_allow_html=True)
                elif new_password != confirm_password:
                    st.markdown('<div class="error-message">❌ Passwords do not match</div>', unsafe_allow_html=True)
                elif len(new_password) < 6:
                    st.markdown('<div class="error-message">❌ Password must be at least 6 characters long</div>', unsafe_allow_html=True)
                else:
                    success, message = change_password_direct(new_password)
                    if success:
                        st.markdown(f'<div class="success-message">✅ {message}</div>', unsafe_allow_html=True)
                        st.balloons()
                        st.info("Your password has been updated. You may need to log in again on other devices.")
                    else:
                        st.markdown(f'<div class="error-message">❌ {message}</div>', unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Security tips section
    st.markdown("---")
    st.subheader("🛡️ Password Security Tips")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **Strong Password Guidelines:**
        - At least 8-12 characters
        - Mix of uppercase & lowercase
        - Include numbers
        - Use special characters
        - Avoid common words
        """)
    
    with col2:
        st.markdown("""
        **What to Avoid:**
        - Personal information
        - Dictionary words
        - Sequential numbers
        - Repeated characters
        - Previously breached passwords
        """)
    
    with col3:
        st.markdown("""
        **Best Practices:**
        - Use unique passwords
        - Enable 2FA when available
        - Regular password updates
        - Use password managers
        - Never share passwords
        """)
    
    # Navigation buttons
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        if st.button("← Back to Dashboard", use_container_width=True):
            st.info("Navigate back to dashboard")
    
    with col2:
        if st.button("🔄 Refresh Page", use_container_width=True):
            st.rerun()
    
    with col3:
        if st.button("❓ Need Help?", use_container_width=True):
            st.info("Contact support if you need assistance")

# Run the password change page
if __name__ == "__main__":
    st.set_page_config(
        page_title="Password Change - AI Agent Toolkit",
        page_icon="🔐",
        layout="wide"
    )
    
    password_change_page()
