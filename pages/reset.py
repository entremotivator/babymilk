import streamlit as st
from supabase import create_client, Client
import requests
import re
import hashlib

# Page configuration
st.set_page_config(
    page_title="Password Reset - Loy",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="collapsed"
)

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

def apply_custom_css():
    """Apply Loy-branded styling for password reset page"""
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
    
    .loy-header {
        text-align: center;
        margin: 2rem 0;
        padding: 2rem;
        background: linear-gradient(135deg, rgba(245, 158, 11, 0.1) 0%, rgba(217, 119, 6, 0.1) 100%);
        border-radius: 20px;
        border: 1px solid rgba(245, 158, 11, 0.3);
    }
    
    .loy-logo {
        font-size: 3rem;
        font-weight: 700;
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 1rem;
    }
    
    .reset-container {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.95) 0%, rgba(51, 65, 85, 0.95) 100%);
        padding: 3rem;
        border-radius: 20px;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
        border: 1px solid #475569;
        margin: 2rem auto;
        max-width: 600px;
        backdrop-filter: blur(20px);
    }
    
    .success-message {
        background: linear-gradient(135deg, rgba(34, 197, 94, 0.2) 0%, rgba(16, 185, 129, 0.2) 100%);
        border: 1px solid #22c55e;
        color: #86efac !important;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
    }
    
    .error-message {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.2) 0%, rgba(220, 38, 38, 0.2) 100%);
        border: 1px solid #ef4444;
        color: #fca5a5 !important;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
    }
    
    .warning-message {
        background: linear-gradient(135deg, rgba(245, 158, 11, 0.2) 0%, rgba(217, 119, 6, 0.2) 100%);
        border: 1px solid #f59e0b;
        color: #fcd34d !important;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
    }
    
    .info-box {
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.2) 0%, rgba(99, 102, 241, 0.2) 100%);
        border: 1px solid #3b82f6;
        color: #93c5fd !important;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
    }
    
    .password-requirements {
        background: rgba(15, 23, 42, 0.8);
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        font-size: 0.9em;
    }
    
    .requirement {
        display: flex;
        align-items: center;
        margin: 0.5rem 0;
        font-size: 0.9em;
    }
    
    .requirement.met {
        color: #86efac;
    }
    
    .requirement.unmet {
        color: #fca5a5;
    }
    
    .strength-meter {
        margin: 1rem 0;
    }
    
    .strength-bar {
        background: #334155;
        height: 8px;
        border-radius: 4px;
        margin: 0.5rem 0;
        overflow: hidden;
    }
    
    .strength-fill {
        height: 100%;
        transition: all 0.3s ease;
        border-radius: 4px;
    }
    
    .navigation-buttons {
        margin-top: 2rem;
        padding-top: 2rem;
        border-top: 1px solid #475569;
    }
    
    .security-tips {
        background: rgba(15, 23, 42, 0.6);
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 2rem;
        margin: 2rem 0;
    }
    </style>
    """, unsafe_allow_html=True)

def send_password_reset_email(email):
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
            return False, "Invalid email address or email not found in our system"
        elif response.status_code == 429:
            return False, "Too many requests. Please wait before trying again"
        else:
            return False, f"Failed to send reset email (Error: {response.status_code})"
            
    except Exception as e:
        return False, f"Connection error: {str(e)}"

def validate_email(email):
    """Enhanced email validation"""
    if not email:
        return False
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def check_password_requirements(password):
    """Check password requirements and return detailed status"""
    if not password:
        return {}, 0
        
    requirements = {
        "length": len(password) >= 8,
        "uppercase": any(c.isupper() for c in password),
        "lowercase": any(c.islower() for c in password),
        "number": any(c.isdigit() for c in password),
        "special": any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?~`" for c in password)
    }
    
    strength_score = sum(requirements.values())
    return requirements, strength_score

def check_user_exists(email):
    """Check if user exists in the database"""
    try:
        result = supabase.table('users').select('email').eq('email', email).execute()
        return len(result.data) > 0
    except Exception:
        return False

def update_user_password(email, new_password):
    """Update user password in the database (simplified for demo)"""
    try:
        # In a real implementation, you'd use proper password hashing
        hashed_password = hashlib.sha256(new_password.encode()).hexdigest()
        
        result = supabase.table('users').update({
            'password': hashed_password,
            'password_updated_at': 'now()'
        }).eq('email', email).execute()
        
        return len(result.data) > 0
    except Exception as e:
        st.error(f"Error updating password: {str(e)}")
        return False

def password_reset_page():
    """Complete Loy password reset page"""
    
    # Apply styling
    apply_custom_css()
    
    # Header with Loy branding
    st.markdown("""
    <div class="loy-header">
        <div class="loy-logo">LOY</div>
        <h1>🔐 Reset Your Password</h1>
        <p style="font-size: 1.1em; opacity: 0.9;">
            Secure password reset for your Loy account
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize session state
    if 'reset_step' not in st.session_state:
        st.session_state.reset_step = 'email_verification'
    if 'verified_email' not in st.session_state:
        st.session_state.verified_email = None
    
    st.markdown('<div class="reset-container">', unsafe_allow_html=True)
    
    if st.session_state.reset_step == 'email_verification':
        # Email verification step
        st.subheader("Step 1: Verify Your Email")
        
        with st.form("email_verification_form", clear_on_submit=False):
            email = st.text_input(
                "Email Address",
                placeholder="Enter your registered email address",
                help="This must be the email address associated with your Loy account"
            )
            
            verify_email_button = st.form_submit_button("Verify Email & Send Reset Link", type="primary")
            
            if verify_email_button:
                if not email:
                    st.markdown('<div class="error-message">❌ <strong>Email Required:</strong> Please enter your email address.</div>', unsafe_allow_html=True)
                elif not validate_email(email):
                    st.markdown('<div class="error-message">❌ <strong>Invalid Email:</strong> Please enter a valid email address.</div>', unsafe_allow_html=True)
                else:
                    # Check if user exists
                    if check_user_exists(email):
                        # Send reset email
                        success, message = send_password_reset_email(email)
                        
                        if success:
                            st.session_state.verified_email = email
                            st.session_state.reset_step = 'password_reset'
                            st.markdown(f'''
                            <div class="success-message">
                            ✅ <strong>Email Verified & Reset Link Sent!</strong><br>
                            We've sent a password reset link to <strong>{email}</strong><br><br>
                            You can now proceed to set your new password below, or use the link in your email.
                            </div>
                            ''', unsafe_allow_html=True)
                            st.rerun()
                        else:
                            st.markdown(f'''
                            <div class="error-message">
                            ❌ <strong>Reset Failed:</strong> {message}<br>
                            Please try again or contact support if the problem persists.
                            </div>
                            ''', unsafe_allow_html=True)
                    else:
                        st.markdown('''
                        <div class="error-message">
                        ❌ <strong>Email Not Found:</strong> This email address is not registered with Loy.<br>
                        Please check the spelling or create a new account.
                        </div>
                        ''', unsafe_allow_html=True)
    
    elif st.session_state.reset_step == 'password_reset':
        # Password reset step
        st.subheader("Step 2: Set New Password")
        st.markdown(f"**Email:** {st.session_state.verified_email}")
        
        with st.form("password_reset_form", clear_on_submit=False):
            # New password input
            new_password = st.text_input(
                "New Password",
                type="password",
                placeholder="Enter your new secure password",
                help="Choose a strong password with at least 8 characters"
            )
            
            # Confirm password input
            confirm_password = st.text_input(
                "Confirm New Password",
                type="password",
                placeholder="Re-enter your new password",
                help="Must match the new password above"
            )
            
            # Password requirements display
            if new_password:
                requirements, strength_score = check_password_requirements(new_password)
                
                st.markdown('<div class="password-requirements">', unsafe_allow_html=True)
                st.markdown("**Password Security Requirements:**")
                
                req_items = [
                    ("length", "At least 8 characters"),
                    ("uppercase", "One uppercase letter (A-Z)"),
                    ("lowercase", "One lowercase letter (a-z)"),
                    ("number", "One number (0-9)"),
                    ("special", "One special character (!@#$%^&*)")
                ]
                
                req_html = []
                for key, label in req_items:
                    status = "met" if requirements.get(key, False) else "unmet"
                    icon = "✅" if requirements.get(key, False) else "❌"
                    req_html.append(f'<div class="requirement {status}">{icon} {label}</div>')
                
                st.markdown(''.join(req_html), unsafe_allow_html=True)
                
                # Strength indicator
                strength_labels = ["Very Weak", "Weak", "Fair", "Good", "Very Strong"]
                strength_colors = ["#ef4444", "#f97316", "#eab308", "#22c55e", "#16a34a"]
                strength_index = min(strength_score - 1, 4) if strength_score > 0 else 0
                
                if strength_score > 0:
                    st.markdown(f'''
                    <div class="strength-meter">
                        <strong>Password Strength: 
                        <span style="color: {strength_colors[strength_index]}">
                        {strength_labels[strength_index]}
                        </span></strong>
                        <div class="strength-bar">
                            <div class="strength-fill" style="background: {strength_colors[strength_index]}; width: {(strength_score/5)*100}%;"></div>
                        </div>
                    </div>
                    ''', unsafe_allow_html=True)
                
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Submit button
            reset_password_button = st.form_submit_button("Reset Password", type="primary")
            
            if reset_password_button:
                # Validation
                errors = []
                
                if not new_password:
                    errors.append("New password is required")
                elif len(new_password) < 8:
                    errors.append("Password must be at least 8 characters long")
                
                if not confirm_password:
                    errors.append("Please confirm your password")
                elif new_password != confirm_password:
                    errors.append("Passwords do not match")
                
                # Display errors
                if errors:
                    error_html = '<div class="error-message">❌ <strong>Please fix the following issues:</strong><ul>'
                    for error in errors:
                        error_html += f'<li>{error}</li>'
                    error_html += '</ul></div>'
                    st.markdown(error_html, unsafe_allow_html=True)
                else:
                    # Check password strength
                    requirements, strength_score = check_password_requirements(new_password)
                    
                    if strength_score < 3:
                        st.markdown('''
                        <div class="warning-message">
                        ⚠️ <strong>Weak Password Warning:</strong><br>
                        Your password doesn't meet all security requirements. We recommend using a stronger password for better account security.
                        </div>
                        ''', unsafe_allow_html=True)
                    
                    # Update password in database
                    if update_user_password(st.session_state.verified_email, new_password):
                        st.markdown('''
                        <div class="success-message">
                        🎉 <strong>Password Reset Successful!</strong><br>
                        Your password has been updated successfully.<br><br>
                        <strong>Next Steps:</strong><br>
                        • You can now log in with your new password<br>
                        • Update saved passwords in your browsers<br>
                        • Consider enabling two-factor authentication<br>
                        • Keep your new password secure and private
                        </div>
                        ''', unsafe_allow_html=True)
                        
                        st.balloons()
                        
                        # Reset session state
                        st.session_state.reset_step = 'success'
                        st.session_state.verified_email = None
                        
                    else:
                        st.markdown('''
                        <div class="error-message">
                        ❌ <strong>Update Failed:</strong> There was an error updating your password.<br>
                        Please try again or contact support if the problem persists.
                        </div>
                        ''', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Security Information
    st.markdown("---")
    st.markdown('<div class="security-tips">', unsafe_allow_html=True)
    st.subheader("🛡️ Loy Security Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Password Best Practices:**
        - Use a unique password for your Loy account
        - Include uppercase and lowercase letters
        - Add numbers and special characters
        - Avoid using personal information
        - Consider using a password manager
        - Change passwords regularly
        """)
    
    with col2:
        st.markdown("""
        **Account Security Tips:**
        - Enable two-factor authentication when available
        - Log out from shared or public devices
        - Monitor your account for unusual activity
        - Keep your email account secure
        - Don't share your password with anyone
        - Update your recovery information regularly
        """)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Navigation buttons
    st.markdown('<div class="navigation-buttons">', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("← Back to Login", use_container_width=True):
            st.session_state.reset_step = 'email_verification'
            st.session_state.verified_email = None
            st.info("🔄 Navigate back to the Loy login page")
    
    with col2:
        if st.button("🔄 Start Over", use_container_width=True):
            st.session_state.reset_step = 'email_verification'
            st.session_state.verified_email = None
            st.rerun()
    
    with col3:
        if st.button("❓ Need Help?", use_container_width=True):
            st.info("📧 Contact Loy Support: support@loy.com")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; opacity: 0.7; margin: 2rem 0;">
        <p>© 2024 Loy - Secure Password Management</p>
        <p>Protected by enterprise-grade security measures</p>
    </div>
    """, unsafe_allow_html=True)

# Run the password reset page
if __name__ == "__main__":
    password_reset_page()
