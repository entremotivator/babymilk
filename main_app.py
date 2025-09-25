import streamlit as st
from supabase import create_client, Client
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import base64
import os

# -------------------------
# Streamlit UI Helpers
# -------------------------

def apply_custom_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #e0f7fa 0%, #b2ebf2 50%, #80deea 100%);
        color: #004d40;
        font-family: 'Inter', sans-serif;
    }

    /* Sidebar width and color */
    [data-testid="stSidebar"][aria-expanded="true"] > div:first-child {
        width: 340px;
    }
    [data-testid="stSidebar"] {
        min-width: 340px;
        background: linear-gradient(180deg, #e0f7fa 0%, #b2ebf2 100%);
        color: #004d40 !important;
        border-right: 2px solid #00796b;
    }

    /* Sidebar headings */
    .sidebar-header {
        color: #004d40 !important;
        font-weight: 700;
        font-size: 1.2rem;
        margin-top: 1rem;
        margin-bottom: 0.5rem;
        font-family: 'Inter', sans-serif;
    }

    /* Sidebar buttons */
    .stSidebar .stButton>button, .stSidebar .stDownloadButton>button {
        background: linear-gradient(90deg, #00796b 0%, #004d40 100%);
        color: #ffffff;
        font-weight: bold;
        border-radius: 12px;
        margin-top: 8px;
        font-family: 'Inter', sans-serif;
        transition: all 0.3s ease;
    }
    .stSidebar .stButton>button:hover {
        background: linear-gradient(90deg, #004d40 0%, #00251a 100%);
        box-shadow: 0 6px 20px rgba(0, 77, 64, 0.5);
        transform: translateY(-2px);
    }

    /* Sidebar inputs */
    .stSidebar .stTextInput>div>div>input, 
    .stSidebar .stSelectbox>div>div>select {
        background: #ffffff;
        color: #004d40;
        border-radius: 10px;
        font-family: 'Inter', sans-serif;
    }

    </style>
    """, unsafe_allow_html=True)

def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def display_logo():
    logo_path = "logo.png"
    if os.path.exists(logo_path):
        st.markdown(f"""
        <div style="display: flex; justify-content: center; align-items: center; margin: 2rem 0;">
            <img src="data:image/png;base64,{get_base64_of_bin_file(logo_path)}" alt="Logo" style="max-width:300px;">
        </div>
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
# Session State Initialization
# -------------------------
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "role" not in st.session_state:
    st.session_state.role = None
if "user" not in st.session_state:
    st.session_state.user = None

# -------------------------
# Authentication Logic
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
    st.experimental_rerun()

# -------------------------
# Page definitions
# -------------------------

def login_page():
    st.title("AI Agent Toolkit Login")
    
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Login")
        with st.form("login_form"):
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Login")
            if submit:
                success, message = login(email, password)
                if success:
                    st.success(message)
                    st.experimental_rerun()
                else:
                    st.error(message)

    with col2:
        st.subheader("Sign Up")
        with st.form("signup_form"):
            email = st.text_input("Email", key="signup_email")
            password = st.text_input("Password", type="password", key="signup_password")
            submit = st.form_submit_button("Sign Up")
            if submit:
                success, message = signup(email, password)
                if success:
                    st.success(message)
                else:
                    st.error(message)

    st.subheader("Forgot Password")
    with st.form("reset_form"):
        email = st.text_input("Email", key="reset_email")
        submit = st.form_submit_button("Send Reset Link")
        if submit:
            success, message = reset_password(email)
            if success:
                st.success(message)
            else:
                st.error(message)

def show_resources():
    st.subheader("📚 Resources")
    st.write("Here are some resources to help you get started with the AI Agent Toolkit:")
    st.markdown("- [Streamlit Documentation](https://docs.streamlit.io/)")
    st.markdown("- [Supabase Documentation](https://supabase.com/docs)")
    st.markdown("- [Plotly Express Documentation](https://plotly.com/python/plotly-express/)")

def show_admin_settings():
    st.subheader("⚙️ Settings")
    st.write("Here you can configure the system settings for the AI Agent Toolkit.")
    
    maintenance_mode = st.checkbox("Maintenance Mode", value=False)
    if maintenance_mode:
        st.warning("The application is currently in maintenance mode.")

def show_user_help():
    st.subheader("❓ Help")
    st.write("If you need help, please contact us at support@example.com")


# -------------------------
# User Management & Admin Reports
# -------------------------

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
            confirmed_users = len([u for u in auth_users.users if getattr(u, 'email_confirmed_at', None)])
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
                         color_discrete_sequence=['#00796b'])
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='#004d40'
            )
            st.plotly_chart(fig, use_container_width=True)
            role_data = pd.DataFrame({
                'Role': ['Users', 'Admins'],
                'Count': [user_count, admin_count]
            })
            fig_pie = px.pie(role_data, values='Count', names='Role', 
                           title='User Role Distribution',
                           color_discrete_sequence=['#00796b', '#004d40'])
            fig_pie.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='#004d40'
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
            auth_info = next((u for u in auth_users.users if u.id == profile["id"]), None)
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
                            st.experimental_rerun()
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
                                st.experimental_rerun()
                            except Exception as e:
                                st.error(f"Failed to delete: {e}")
        else:
            st.info("No users found matching your criteria.")
    except Exception as e:
        st.error(f"Error loading users: {e}")

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
                 color_discrete_sequence=['#00796b'])
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='#004d40'
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
        theme = st.selectbox("Theme", ["Light Blue", "Dark", "Auto"])
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
        if notif['read']:
            st.info(f"{notif['message']} - {notif['time']}")
        else:
            st.success(f"{notif['message']} - {notif['time']}")

# -------------------------
# Sidebar Menu (All Users)
# -------------------------

def show_sidebar_menu():
    st.sidebar.title("🧭 AI Agent Toolkit Menu")

    if st.session_state.user:
        st.sidebar.markdown(f"👤 **{st.session_state.user.email.split('@')[0].title()}**")
        st.sidebar.markdown(f"🎭 **Role:** {st.session_state.role.capitalize()}")
    st.sidebar.divider()

    nav_items = ["🏠 Dashboard", "📊 Analytics", "📚 Resources", "🔔 Notifications", "👤 Profile", "❓ Help"]
    if st.session_state.role == "admin":
        nav_items.insert(2, "👥 User Management")
        nav_items.insert(4, "⚙️ Settings")

    page = st.sidebar.radio("Navigate to:", nav_items, index=0)
    
    if st.sidebar.button("🚪 Logout"):
        logout()

    return page

# -------------------------
# Main Application Logic
# -------------------------

def main():
    st.set_page_config(
        page_title="AI Agent Toolkit",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    apply_custom_css()

    if not st.session_state.authenticated:
        login_page()
    else:
        display_logo()
        if st.session_state.role == "admin":
            st.title("👑 AI Agent Toolkit - Admin Dashboard")
            page = show_sidebar_menu()

            if page == "📊 Analytics":
                show_admin_analytics()
            elif page == "👥 User Management":
                show_user_management()
            elif page == "📚 Resources":
                show_resources()
            elif page == "⚙️ Settings":
                show_admin_settings()
            elif page == "🔔 Notifications":
                show_user_notifications(st.session_state.user.email)
            elif page == "👤 Profile":
                show_user_profile(st.session_state.user.id, st.session_state.user.email)
            elif page == "❓ Help":
                show_user_help()
            else:
                show_user_activity(st.session_state.user.id, st.session_state.user.email)
        else:
            st.title("🤖 Welcome to the AI Agent Toolkit")
            page = show_sidebar_menu()

            if page == "🏠 Dashboard":
                show_user_activity(st.session_state.user.id, st.session_state.user.email)
            elif page == "📚 Resources":
                show_resources()
            elif page == "🔔 Notifications":
                show_user_notifications(st.session_state.user.email)
            elif page == "👤 Profile":
                show_user_profile(st.session_state.user.id, st.session_state.user.email)
            elif page == "❓ Help":
                show_user_help()

if __name__ == "__main__":
    main()

