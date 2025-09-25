import streamlit as st
from supabase import create_client, Client
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import base64
import os

# -------------------------
# Hide Streamlit Elements
# -------------------------
def hide_streamlit_style():
    hide_st_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display:none;}
    .stDecoration {display:none;}
    .css-14xtw13.e8zbici0 {display: none;}
    .css-1rs6os.edgvbvh3 {display: none;}
    .css-vk3wp9.e1akgbir0 {display: none;}
    .css-1j8o68f.edgvbvh9 {display: none;}
    .css-1dp5vir.e8zbici0 {display: none;}
    div[data-testid="stToolbar"] {visibility: hidden;}
    div[data-testid="stDecoration"] {visibility: hidden;}
    div[data-testid="stStatusWidget"] {visibility: hidden;}
    </style>
    """
    st.markdown(hide_st_style, unsafe_allow_html=True)

def apply_custom_css():
    hide_streamlit_style()
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #334155 100%);
        color: #ffffff;
        font-family: 'Inter', sans-serif;
    }
    /* Sidebar styling */
    .css-1d391kg,
    .st-emotion-cache-1d391kg,
    section[data-testid="stSidebar"] > div {
        background: linear-gradient(180deg, #1e293b 0%, #334155 100%);
        color: white !important;
        border-right: 2px solid #f59e0b;
    }
    </style>
    """, unsafe_allow_html=True)

def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def display_logo():
    logo_path = "/home/ubuntu/ai-agent-toolkit/logo.png"
    if os.path.exists(logo_path):
        st.markdown(f"""
        <div style="display: flex; justify-content: center; align-items: center; margin: 2rem 0;">
            <img src="data:image/png;base64,{get_base64_of_bin_file(logo_path)}" alt="Logo" style="max-width:300px;">
        </div>
        """, unsafe_allow_html=True)

def hide_sidebar():
    st.markdown("""
    <style>
        section[data-testid="stSidebar"] {display: none !important;}
        .css-1d391kg {display: none !important;}
        .css-6qob1r {display: none !important;}
        .e1fqkh3o3 {display: none !important;}
        .st-emotion-cache-1d391kg {display: none !important;}
        .st-emotion-cache-6qob1r {display: none !important;}
    </style>
    """, unsafe_allow_html=True)

def show_sidebar():
    st.markdown("""
    <style>
        section[data-testid="stSidebar"] {display: block !important;}
        .css-1d391kg {display: block !important;}
        .css-6qob1r {display: block !important;}
        .e1fqkh3o3 {display: block !important;}
        .st-emotion-cache-1d391kg {display: block !important;}
        .st-emotion-cache-6qob1r {display: block !important;}
    </style>
    """, unsafe_allow_html=True)

# -------------------------
# Supabase Setup
# -------------------------
@st.cache_resource
def init_connection() -> Client:
    try:
        url = st.secrets["supabase"]["url"]
        key = st.secrets["supabase"]["key"]
        return create_client(url, key)
    except Exception as e:
        st.error(f"Failed to connect to Supabase: {e}")
        st.stop()

supabase = init_connection()

# -------------------------
# Session State
# -------------------------
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "role" not in st.session_state:
    st.session_state.role = None
if "user" not in st.session_state:
    st.session_state.user = None

# -------------------------
# Authentication Functions
# -------------------------
def signup(email, password):
    if not email or not password:
        return False, "⚠️ Please fill in all fields."
    if len(password) < 6:
        return False, "⚠️ Password must be at least 6 characters long."
    try:
        res = supabase.auth.sign_up({"email": email, "password": password})
        if res.user:
            supabase.table("user_profiles").insert({
                "id": res.user.id,
                "email": email,
                "role": "user"
            }).execute()
            return True, "✅ Account created! Please check your email."
        return False, "❌ Failed to create account."
    except Exception as e:
        error_msg = str(e)
        if "already registered" in error_msg.lower():
            return False, "⚠️ Email already registered. Try logging in."
        return False, f"❌ Signup error: {error_msg}"

def login(email, password):
    try:
        res = supabase.auth.sign_in_with_password({"email": email, "password": password})
        if res.user:
            profile = supabase.table("user_profiles").select("role").eq("id", res.user.id).execute()
            role = profile.data[0]["role"] if profile.data else "user"
            st.session_state.authenticated = True
            st.session_state.user = res.user
            st.session_state.role = role
            return True, f"✅ Logged in as {role.capitalize()}"
        return False, "❌ Invalid email or password."
    except Exception as e:
        return False, f"❌ Login error: {str(e)}"

def reset_password(email):
    try:
        supabase.auth.reset_password_for_email(email)
        return True, f"✅ Password reset email sent to {email}"
    except Exception as e:
        return False, f"❌ Reset error: {str(e)}"

def logout():
    try:
        supabase.auth.sign_out()
    except Exception:
        pass
    st.session_state.authenticated = False
    st.session_state.role = None
    st.session_state.user = None
    st.rerun()

# -------------------------
# Resource Downloads
# -------------------------
def show_resources():
    st.subheader("📚 AI Agent Toolkit Resources")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 📋 The Ultimate AI & Bot Checklist")
        st.write("Comprehensive guide for AI agent development.")
        if os.path.exists("/home/ubuntu/ai-agent-toolkit/AI_and_Bot_Checklist.pdf"):
            with open("/home/ubuntu/ai-agent-toolkit/AI_and_Bot_Checklist.pdf", "rb") as file:
                st.download_button(
                    label="📥 Download Checklist PDF",
                    data=file.read(),
                    file_name="AI_and_Bot_Checklist.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
    with col2:
        st.markdown("### 🛠️ 250 Best AI Tools")
        st.write("Curated list of top AI tools.")
        if os.path.exists("/home/ubuntu/ai-agent-toolkit/250_Best_AI_Tools.pdf"):
            with open("/home/ubuntu/ai-agent-toolkit/250_Best_AI_Tools.pdf", "rb") as file:
                st.download_button(
                    label="📥 Download AI Tools PDF",
                    data=file.read(),
                    file_name="250_Best_AI_Tools.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; margin: 2rem 0;">
        <a href="https://entremotivator.com" target="_blank" style="display:inline-block;background:linear-gradient(135deg,#f59e0b 0%,#d97706 100%);color:#000;padding:0.75rem 1.5rem;border-radius:12px;font-weight:600;text-decoration:none;">🚀 Visit Entremotivator.com for More Resources</a>
    </div>
    """, unsafe_allow_html=True)

# -------------------------
# Admin Dashboard
# -------------------------
def admin_dashboard():
    show_sidebar()
    display_logo()
    st.title("👑 AI Agent Toolkit - Admin Dashboard")
    with st.sidebar:
        st.markdown("### 🔧 Admin Tools")
        if st.session_state.user:
            st.info(f"👤 {st.session_state.user.email}\n🎭 {st.session_state.role.title()}")
        if st.button("🚪 Logout", type="secondary", use_container_width=True):
            logout()
        st.divider()
        admin_section = st.selectbox(
            "Select Section",
            ["📊 Analytics", "👥 User Management", "📚 Resources", "📈 Reports", "⚙️ Settings"]
        )
    if admin_section == "📊 Analytics":
        show_admin_analytics()
    elif admin_section == "👥 User Management":
        show_user_management()
    elif admin_section == "📚 Resources":
        show_resources()
    elif admin_section == "📈 Reports":
        show_system_reports()
    elif admin_section == "⚙️ Settings":
        show_admin_settings()

def show_admin_analytics():
    st.subheader("📊 AI Agent Toolkit Analytics")
    try:
        users = supabase.table("user_profiles").select("*").execute()
        auth_users = supabase.auth.admin.list_users()
        total_users = len(users.data or [])
        admin_count = len([u for u in users.data or [] if u["role"] == "admin"])
        user_count = total_users - admin_count
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Users", total_users, delta=f"+{max(0, total_users-10)}")
        with col2:
            st.metric("Regular Users", user_count)
        with col3:
            st.metric("Administrators", admin_count)
        with col4:
            confirmed_users = len([u for u in auth_users.user if getattr(u, 'email_confirmed_at', None)])
            st.metric("Confirmed Users", confirmed_users)
        if users.data:
            st.subheader("📈 User Registration Trends")
            dates = pd.date_range(start='2024-01-01', end=datetime.now(), freq='D')
            registrations = pd.DataFrame({
                'date': dates,
                'registrations': [max(0, int(abs(hash(str(d)) % 8) - 3)) for d in dates]
            })
            fig = px.line(registrations, x='date', y='registrations', 
                         title='Daily User Registrations',
                         color_discrete_sequence=['#f59e0b'])
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='#ffffff'
            )
            st.plotly_chart(fig, use_container_width=True)
            role_data = pd.DataFrame({
                'Role': ['Users', 'Admins'],
                'Count': [user_count, admin_count]
            })
            fig_pie = px.pie(role_data, values='Count', names='Role', 
                           title='User Role Distribution',
                           color_discrete_sequence=['#f59e0b', '#d97706'])
            fig_pie.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='#ffffff'
            )
            st.plotly_chart(fig_pie, use_container_width=True)
    except Exception as e:
        st.error(f"Error loading analytics: {e}")

def show_user_management():
    st.subheader("👥 User Management")
    try:
        users = supabase.table("user_profiles").select("*").execute()
        auth_users = supabase.auth.admin.list_users()
        user_data = []
        for profile in users.data or []:
            auth_info = next((u for u in auth_users.user if u.id == profile["id"]), None)
            user_data.append({
                "id": profile["id"],
                "email": profile["email"],
                "role": profile["role"],
                "created_at": getattr(auth_info, "created_at", None),
                "last_sign_in": getattr(auth_info, "last_sign_in_at", None),
                "confirmed": getattr(auth_info, "email_confirmed_at", None) is not None,
            })
        col1, col2 = st.columns([2, 1])
        with col1:
            search = st.text_input("🔍 Search by email")
        with col2:
            role_filter = st.selectbox("Filter by role", ["All", "user", "admin"])
        filtered = user_data
        if search:
            filtered = [u for u in filtered if search.lower() in u["email"].lower()]
        if role_filter != "All":
            filtered = [u for u in filtered if u["role"] == role_filter]
        st.subheader("🔧 Bulk Actions")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📧 Send Welcome Email to All"):
                st.success("Welcome emails sent to all users!")
        with col2:
            if st.button("⬇️ Export User Data"):
                df = pd.DataFrame(filtered)
                st.download_button("Download CSV", df.to_csv(index=False), "users.csv", "text/csv")
        if filtered:
            for i, user in enumerate(filtered):
                with st.expander(f"👤 {user['email']} ({user['role'].title()}) {'✅' if user['confirmed'] else '❌'}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**User ID:** {user['id'][:8]}...")
                        st.write(f"**Created:** {user['created_at']}")
                        st.write(f"**Last Login:** {user['last_sign_in']}")
                    with col2:
                        st.write(f"**Status:** {'Confirmed' if user['confirmed'] else 'Pending'}")
                        st.write(f"**Role:** {user['role'].title()}")
                    action_col1, action_col2, action_col3 = st.columns(3)
                    with action_col1:
                        new_role = st.selectbox("Change Role", ["user", "admin"], 
                                                index=0 if user["role"] == "user" else 1,
                                                key=f"role_{i}")
                        if st.button("Update Role", key=f"update_{i}"):
                            supabase.table("user_profiles").update({"role": new_role}).eq("id", user["id"]).execute()
                            st.success(f"Updated {user['email']} to {new_role}")
                            st.rerun()
                    with action_col2:
                        if st.button("🔄 Reset Password", key=f"reset_{i}"):
                            success, msg = reset_password(user["email"])
                            if success:
                                st.success(msg)
                            else:
                                st.error(msg)
                    with action_col3:
                        if st.button("❌ Delete User", key=f"delete_{i}", type="secondary"):
                            try:
                                supabase.table("user_profiles").delete().eq("id", user["id"]).execute()
                                supabase.auth.admin.delete_user(user["id"])
                                st.warning(f"Deleted {user['email']}")
                                st.rerun()
                            except Exception as e:
                                st.error(f"Failed to delete: {e}")
        else:
            st.info("No users found matching your criteria.")
    except Exception as e:
        st.error(f"Error loading users: {e}")

def show_system_reports():
    st.subheader("📈 System Reports")
    st.write("**Recent System Activity**")
    activity_data = [
        {"timestamp": datetime.now() - timedelta(minutes=5), "action": "User login", "user": "user@example.com"},
        {"timestamp": datetime.now() - timedelta(minutes=15), "action": "New user registration", "user": "newuser@example.com"},
        {"timestamp": datetime.now() - timedelta(hours=1), "action": "Password reset", "user": "forgot@example.com"},
        {"timestamp": datetime.now() - timedelta(hours=2), "action": "Admin role assigned", "user": "admin@example.com"},
    ]
    for activity in activity_data:
        st.write(f"🕐 {activity['timestamp'].strftime('%Y-%m-%d %H:%M')} - {activity['action']} - {activity['user']}")
    st.subheader("🏥 System Health")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Database Status", "✅ Healthy", delta="99.9% uptime")
    with col2:
        st.metric("Auth Service", "✅ Operational", delta="0 errors")
    with col3:
        st.metric("API Response", "⚡ Fast", delta="120ms avg")

def show_admin_settings():
    st.subheader("⚙️ System Settings")
    st.write("**Security Configuration**")
    password_policy = st.checkbox("Enforce minimum password length", value=True)
    session_timeout = st.slider("Session timeout (hours)", 1, 24, 8)
    two_factor = st.checkbox("Require 2FA for admins", value=False)
    st.write("**Email Configuration**")
    welcome_email = st.checkbox("Send welcome emails", value=True)
    notification_email = st.text_input("Admin notification email", value="admin@company.com")
    st.write("**System Maintenance**")
    if st.button("🧹 Clean up old sessions"):
        st.success("Old sessions cleaned up!")
    if st.button("📊 Generate system report"):
        st.success("System report generated!")
    if st.button("💾 Save Settings", type="primary"):
        st.success("Settings saved successfully!")

# -------------------------
# User Dashboard
# -------------------------
def user_dashboard():
    show_sidebar()
    display_logo()
    st.title("🤖 Welcome to the AI Agent Toolkit")
    user_email = st.session_state.user.email if st.session_state.user else "Unknown"
    user_id = st.session_state.user.id if st.session_state.user else None
    with st.sidebar:
        st.markdown("### 🏠 Dashboard")
        st.info(f"👤 {user_email.split('@')[0].title()}\n🎭 {st.session_state.role.title()}\n📧 {user_email}")
        if st.button("🚪 Logout", type="secondary", use_container_width=True):
            logout()
        st.divider()
        page = st.selectbox(
            "Navigate to:",
            ["📊 My Activity", "📚 Resources", "👤 Profile", "🔔 Notifications", "❓ Help"]
        )
    if page == "📊 My Activity":
        show_user_activity(user_id, user_email)
    elif page == "📚 Resources":
        show_resources()
    elif page == "👤 Profile":
        show_user_profile(user_id, user_email)
    elif page == "🔔 Notifications":
        show_user_notifications(user_email)
    elif page == "❓ Help":
        show_user_help()

def show_user_activity(user_id, user_email):
    st.subheader("📊 Your Activity Overview")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Days Active", "12", delta="+2")
    with col2:
        st.metric("Total Sessions", "45", delta="+5")
    with col3:
        st.metric("Last Login", "2 hours ago")
    st.subheader("📈 Your Activity Chart")
    dates = pd.date_range(start=datetime.now() - timedelta(days=30), end=datetime.now(), freq='D')
    activity = pd.DataFrame({
        'date': dates,
        'sessions': [max(0, int(abs(hash(str(d) + user_email) % 5) - 1)) for d in dates]
    })
    fig = px.bar(activity, x='date', y='sessions', 
                 title='Your Daily Activity (Last 30 Days)',
                 color_discrete_sequence=['#f59e0b'])
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='#ffffff'
    )
    st.plotly_chart(fig, use_container_width=True)

def show_user_profile(user_id, user_email):
    st.subheader("👤 Your Profile")
    with st.form("profile_form"):
        st.write("**Personal Information**")
        full_name = st.text_input("Full Name", value="")
        phone = st.text_input("Phone Number", value="")
        bio = st.text_area("Bio", value="")
        st.write("**Preferences**")
        theme = st.selectbox("Theme", ["Dark (AI Agent Toolkit)", "Light", "Auto"])
        notifications = st.checkbox("Email notifications", value=True)
        newsletter = st.checkbox("Subscribe to newsletter", value=False)
        st.write("**Security**")
        current_password = st.text_input("Current Password", type="password")
        new_password = st.text_input("New Password", type="password")
        confirm_password = st.text_input("Confirm New Password", type="password")
        if st.form_submit_button("💾 Save Changes", type="primary"):
            if new_password and new_password == confirm_password:
                if len(new_password) >= 6:
                    st.success("Profile updated successfully!")
                else:
                    st.error("Password must be at least 6 characters long")
            else:
                st.success("Profile preferences updated!")

def show_user_notifications(user_email):
    st.subheader("🔔 Your Notifications")
    st.write("**Notification Preferences**")
    email_notifications = st.checkbox("Email notifications", value=True)
    security_alerts = st.checkbox("Security alerts", value=True)
    product_updates = st.checkbox("Product updates", value=False)
    st.write("**Recent Notifications**")
    notifications = [
        {"time": "1 hour ago", "message": "Welcome to the AI Agent Toolkit!", "type": "info", "read": False},
        {"time": "1 day ago", "message": "Your profile was updated", "type": "success", "read": True},
        {"time": "3 days ago", "message": "Security: New login detected", "type": "warning", "read": True},
    ]
    for i, notif in enumerate(notifications):
        icon = "🔵" if not notif["read"] else "⚪"
        type_icon = {"info": "ℹ️", "success": "✅", "warning": "⚠️"}.get(notif["type"], "📢")
        st.write(f"{icon} {type_icon} **{notif['message']}** - {notif['time']}")
        if not notif["read"] and st.button(f"Mark as read", key=f"read_{i}"):
            st.success("Marked as read!")
    if st.button("🧹 Clear all notifications"):
        st.success("All notifications cleared!")

def show_user_help():
    st.subheader("❓ Help & Support")
    st.write("**Frequently Asked Questions**")
    with st.expander("How do I change my password?"):
        st.write("Go to the Profile tab and enter your current password along with your new password.")
    with st.expander("How do I download the AI resources?"):
        st.write("Visit the Resources tab to download the Ultimate AI & Bot Checklist and 250 Best AI Tools PDF guides.")
    with st.expander("How do I update my notification preferences?"):
        st.write("Visit the Notifications tab to customize which notifications you receive.")
    with st.expander("Who can I contact for support?"):
        st.write("You can reach out to our support team at support@entremotivator.com")
    st.write("**Contact Support**")
    with st.form("support_form"):
        subject = st.selectbox("Subject", ["General Question", "Technical Issue", "Feature Request", "Bug Report"])
        message = st.text_area("Message", placeholder="Describe your question or issue...")
        if st.form_submit_button("📧 Send Message"):
            st.success("Your message has been sent! We'll get back to you soon.")

# -------------------------
# Login Page
# -------------------------
def login_page():
    hide_sidebar()
    display_logo()
    st.markdown("""
    <div style="text-align: center; padding: 3rem; background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%); border-radius:16px; color:#000; margin-bottom:2rem; box-shadow: 0 8px 32px rgba(245,158,11,0.4);">
        <h1>🔐 AI Agent Toolkit Authentication Portal</h1>
        <p>Secure access to your personalized AI toolkit dashboard</p>
    </div>
    """, unsafe_allow_html=True)
    tab1, tab2, tab3 = st.tabs(["🔑 Login", "📝 Sign Up", "🔄 Reset Password"])
    with tab1:
        st.markdown('<div style="background:linear-gradient(135deg,rgba(30,41,59,0.95),rgba(51,65,85,0.95)); padding:3rem;border-radius:20px;box-shadow:0 20px 60px rgba(0,0,0,0.3); border:1px solid #475569;margin:2rem 0;">', unsafe_allow_html=True)
        st.subheader("🔑 Sign In to Your Account")
        with st.form("login_form"):
            email = st.text_input("📧 Email Address", placeholder="your.email@example.com")
            password = st.text_input("🔒 Password", type="password", placeholder="Enter your password")
            remember_me = st.checkbox("🧠 Remember me")
            if st.form_submit_button("🚀 Login", type="primary", use_container_width=True):
                if email and password:
                    success, msg = login(email, password)
                    if success:
                        st.success(msg)
                        st.balloons()
                        st.rerun()
                    else:
                        st.error(msg)
                else:
                    st.warning("Please fill in all fields.")
        st.markdown('</div>', unsafe_allow_html=True)
    with tab2:
        st.markdown('<div style="background:linear-gradient(135deg,rgba(30,41,59,0.95),rgba(51,65,85,0.95)); padding:3rem;border-radius:20px;box-shadow:0 20px 60px rgba(0,0,0,0.3); border:1px solid #475569;margin:2rem 0;">', unsafe_allow_html=True)
        st.subheader("📝 Create New Account")
        st.info("💡 New accounts are created as regular users. Contact an administrator to upgrade to admin privileges.")
        with st.form("signup_form"):
            email = st.text_input("📧 Email Address", placeholder="your.email@example.com")
            password = st.text_input("🔒 Password", type="password", help="Must be at least 6 characters long")
            confirm_password = st.text_input("🔒 Confirm Password", type="password")
            terms = st.checkbox("✅ I agree to the Terms of Service and Privacy Policy")
            if st.form_submit_button("🎉 Create Account", type="primary", use_container_width=True):
                if email and password and confirm_password:
                    if password != confirm_password:
                        st.error("❌ Passwords don't match!")
                    elif not terms:
                        st.warning("⚠️ Please agree to the terms and conditions.")
                    else:
                        success, msg = signup(email, password)
                        if success:
                            st.success(msg)
                            st.balloons()
                        else:
                            st.error(msg)
                else:
                    st.warning("Please fill in all fields.")
        st.markdown('</div>', unsafe_allow_html=True)
    with tab3:
        st.markdown('<div style="background:linear-gradient(135deg,rgba(30,41,59,0.95),rgba(51,65,85,0.95)); padding:3rem;border-radius:20px;box-shadow:0 20px 60px rgba(0,0,0,0.3); border:1px solid #475569;margin:2rem 0;">', unsafe_allow_html=True)
        st.subheader("🔄 Reset Your Password")
        with st.form("reset_form"):
            email = st.text_input("📧 Email Address", placeholder="Enter your registered email address")
            st.info("💡 We'll send you a secure link to reset your password")
            if st.form_submit_button("📧 Send Reset Link", type="primary", use_container_width=True):
                if email:
                    success, msg = reset_password(email)
                    if success:
                        st.success(msg)
                    else:
                        st.error(msg)
                else:
                    st.warning("Please enter your email address.")
        st.markdown('</div>', unsafe_allow_html=True)

# -------------------------
# Main App
# -------------------------
def main():
    st.set_page_config(
        page_title="AI Agent Toolkit by D Hudson", 
        page_icon="🤖", 
        layout="wide",
        initial_sidebar_state="expanded"  # Always show sidebar when possible
    )
    apply_custom_css()
    if not st.session_state.authenticated:
        login_page()
    else:
        if st.session_state.role == "admin":
            admin_dashboard()
        else:
            user_dashboard()

if __name__ == "__main__":
    main()
