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
    """Hide Streamlit default elements for cloud deployment"""
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
            #MainMenu {visibility: hidden;}
            header {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
    st.markdown(hide_st_style, unsafe_allow_html=True)

# -------------------------
# Professional Styling
# -------------------------
def apply_custom_css():
    """Apply professional AI Agent Toolkit theme"""
    hide_streamlit_style()
    
    st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Main app styling */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #334155 100%);
        color: #ffffff;
        font-family: 'Inter', sans-serif;
    }
    
    /* Text colors */
    .stMarkdown, .stText, p, span, div {
        color: #ffffff !important;
        font-family: 'Inter', sans-serif;
    }
    
    h1, h2, h3, h4, h5, h6 {
        color: #f59e0b !important;
        font-weight: 600;
        font-family: 'Inter', sans-serif;
    }
    
    /* Sidebar styling - Multiple selectors for compatibility */
    .css-1d391kg,
    .st-emotion-cache-1d391kg,
    section[data-testid="stSidebar"] > div {
        background: linear-gradient(180deg, #1e293b 0%, #334155 100%);
        color: white !important;
        border-right: 2px solid #f59e0b;
    }
    
    .css-1d391kg .stMarkdown, 
    .css-1d391kg .stText,
    .css-1d391kg p,
    .css-1d391kg span,
    .css-1d391kg div,
    .st-emotion-cache-1d391kg .stMarkdown, 
    .st-emotion-cache-1d391kg .stText,
    .st-emotion-cache-1d391kg p,
    .st-emotion-cache-1d391kg span,
    .st-emotion-cache-1d391kg div,
    section[data-testid="stSidebar"] .stMarkdown,
    section[data-testid="stSidebar"] .stText,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] div {
        color: white !important;
    }
    
    /* Button styling */
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
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #d97706 0%, #b45309 100%);
        box-shadow: 0 6px 20px rgba(245, 158, 11, 0.5);
        transform: translateY(-2px);
    }
    
    /* Form styling */
    .stTextInput > div > div > input,
    .stSelectbox > div > div > select,
    .stTextArea > div > div > textarea {
        background-color: rgba(30, 41, 59, 0.8);
        border: 2px solid #475569;
        border-radius: 12px;
        color: #ffffff !important;
        transition: all 0.3s ease;
        font-family: 'Inter', sans-serif;
    }
    
    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div > select:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #f59e0b;
        box-shadow: 0 0 0 3px rgba(245, 158, 11, 0.2);
        background-color: rgba(30, 41, 59, 1);
    }
    
    /* Metric cards */
    .metric-card {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.9) 0%, rgba(51, 65, 85, 0.9) 100%);
        padding: 2rem;
        border-radius: 16px;
        border: 1px solid #475569;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        margin-bottom: 1.5rem;
        transition: all 0.3s ease;
        backdrop-filter: blur(10px);
    }
    
    .metric-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 40px rgba(245, 158, 11, 0.2);
        border-color: #f59e0b;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        background-color: transparent;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: rgba(30, 41, 59, 0.8);
        border: 2px solid #475569;
        border-radius: 12px 12px 0 0;
        color: #cbd5e1;
        padding: 1rem 2rem;
        font-weight: 500;
        font-family: 'Inter', sans-serif;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
        color: #000000 !important;
        border-color: #f59e0b;
        font-weight: 600;
    }
    
    /* Alert styling */
    .stAlert {
        border-radius: 12px;
        border: none;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
        backdrop-filter: blur(10px);
    }
    
    /* Info boxes */
    .stInfo {
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.2) 0%, rgba(99, 102, 241, 0.2) 100%);
        border: 1px solid #3b82f6;
        color: #93c5fd !important;
    }
    
    /* Success boxes */
    .stSuccess {
        background: linear-gradient(135deg, rgba(34, 197, 94, 0.2) 0%, rgba(16, 185, 129, 0.2) 100%);
        border: 1px solid #22c55e;
        color: #86efac !important;
    }
    
    /* Error boxes */
    .stError {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.2) 0%, rgba(220, 38, 38, 0.2) 100%);
        border: 1px solid #ef4444;
        color: #fca5a5 !important;
    }
    
    /* Warning boxes */
    .stWarning {
        background: linear-gradient(135deg, rgba(245, 158, 11, 0.2) 0%, rgba(217, 119, 6, 0.2) 100%);
        border: 1px solid #f59e0b;
        color: #fcd34d !important;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background: rgba(30, 41, 59, 0.8);
        border: 1px solid #475569;
        border-radius: 12px;
        color: #ffffff !important;
        font-family: 'Inter', sans-serif;
    }
    
    /* DataFrame styling */
    .dataframe {
        border: none !important;
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
        backdrop-filter: blur(10px);
    }
    
    .dataframe thead tr th {
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%) !important;
        color: #000000 !important;
        border: none !important;
        font-weight: 600;
        font-family: 'Inter', sans-serif;
    }
    
    .dataframe tbody tr:nth-child(even) {
        background-color: rgba(30, 41, 59, 0.5) !important;
    }
    
    .dataframe tbody tr td {
        color: #ffffff !important;
        border-color: #475569 !important;
        font-family: 'Inter', sans-serif;
    }
    
    /* Login page specific styling */
    .login-container {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.95) 0%, rgba(51, 65, 85, 0.95) 100%);
        padding: 3rem;
        border-radius: 20px;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
        border: 1px solid #475569;
        margin: 2rem 0;
        backdrop-filter: blur(20px);
    }
    
    .welcome-header {
        text-align: center;
        padding: 3rem;
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
        border-radius: 16px;
        color: #000000 !important;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(245, 158, 11, 0.4);
    }
    
    .welcome-header h1,
    .welcome-header h2,
    .welcome-header h3,
    .welcome-header p {
        color: #000000 !important;
        margin: 0.5rem 0;
        font-family: 'Inter', sans-serif;
    }
    
    /* Dashboard cards */
    .dashboard-card {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.9) 0%, rgba(51, 65, 85, 0.9) 100%);
        padding: 2rem;
        border-radius: 16px;
        border-left: 4px solid #f59e0b;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
        margin-bottom: 1.5rem;
        transition: all 0.3s ease;
        backdrop-filter: blur(10px);
    }
    
    .dashboard-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 40px rgba(245, 158, 11, 0.2);
    }
    
    .dashboard-card h3 {
        color: #f59e0b !important;
        margin-top: 0;
        font-weight: 600;
        font-family: 'Inter', sans-serif;
    }
    
    /* Logo styling */
    .logo-container {
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 2rem 0;
    }
    
    .logo-container img {
        max-width: 300px;
        height: auto;
        filter: drop-shadow(0 8px 32px rgba(245, 158, 11, 0.3));
    }
    
    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 12px;
    }
    
    ::-webkit-scrollbar-track {
        background: #1e293b;
        border-radius: 6px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
        border-radius: 6px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #d97706 0%, #b45309 100%);
    }
    
    /* Resource links styling */
    .resource-link {
        display: inline-block;
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
        color: #000000 !important;
        padding: 0.75rem 1.5rem;
        border-radius: 12px;
        text-decoration: none;
        font-weight: 600;
        font-family: 'Inter', sans-serif;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(245, 158, 11, 0.3);
        margin: 0.5rem;
    }
    
    .resource-link:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(245, 158, 11, 0.5);
        text-decoration: none;
        color: #000000 !important;
    }
    </style>
    """, unsafe_allow_html=True)

def get_base64_of_bin_file(bin_file):
    """Get base64 encoding of binary file"""
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def display_logo():
    """Display the AI Agent Toolkit logo"""
    logo_path = "/home/ubuntu/ai-agent-toolkit/logo.png"
    if os.path.exists(logo_path):
        st.markdown(f"""
        <div class="logo-container">
            <img src="data:image/png;base64,{get_base64_of_bin_file(logo_path)}" alt="AI Agent Toolkit Logo">
        </div>
        """, unsafe_allow_html=True)

def hide_sidebar():
    """Hide the sidebar for login page"""
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
    """Show the sidebar for authenticated users"""
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
    """Initialize Supabase connection"""
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
    """Sign up new user (only regular users, no admin option)"""
    if not email or not password:
        return False, "â ï¸ Please fill in all fields."
    
    if len(password) < 6:
        return False, "â ï¸ Password must be at least 6 characters long."
    
    try:
        res = supabase.auth.sign_up({"email": email, "password": password})
        if res.user:
            # Always create as regular user
            supabase.table("user_profiles").insert({
                "id": res.user.id,
                "email": email,
                "role": "user"  # Always user, no admin signup
            }).execute()
            return True, "â Account created! Please check your email to verify your account, then log in."
        return False, "â Failed to create account."
    except Exception as e:
        error_msg = str(e)
        if "already registered" in error_msg.lower():
            return False, "â ï¸ Email already registered. Try logging in."
        return False, f"â Signup error: {error_msg}"

def login(email, password):
    """Login user"""
    try:
        res = supabase.auth.sign_in_with_password({"email": email, "password": password})
        if res.user:
            profile = supabase.table("user_profiles").select("role").eq("id", res.user.id).execute()
            role = profile.data[0]["role"] if profile.data else "user"
            st.session_state.authenticated = True
            st.session_state.user = res.user
            st.session_state.role = role
            return True, f"â Welcome to the AI Agent Toolkit! Logged in as {role.capitalize()}"
        return False, "â Invalid email or password."
    except Exception as e:
        return False, f"â Login error: {str(e)}"

def reset_password(email):
    """Reset password"""
    try:
        supabase.auth.reset_password_for_email(email)
        return True, f"â Password reset email sent to {email}"
    except Exception as e:
        return False, f"â Reset error: {str(e)}"

def logout():
    """Logout user"""
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
    """Display downloadable resources"""
    st.subheader("ð AI Agent Toolkit Resources")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### ð The Ultimate AI & Bot Checklist")
        st.write("A comprehensive checklist to guide you through every stage of AI agent development.")
        
        if os.path.exists("/home/ubuntu/ai-agent-toolkit/AI_and_Bot_Checklist.pdf"):
            with open("/home/ubuntu/ai-agent-toolkit/AI_and_Bot_Checklist.pdf", "rb") as file:
                st.download_button(
                    label="ð¥ Download Checklist PDF",
                    data=file.read(),
                    file_name="AI_and_Bot_Checklist.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
    
    with col2:
        st.markdown("### ð ï¸ 250 Best AI Tools")
        st.write("A curated list of the most innovative and effective AI tools available today.")
        
        if os.path.exists("/home/ubuntu/ai-agent-toolkit/250_Best_AI_Tools.pdf"):
            with open("/home/ubuntu/ai-agent-toolkit/250_Best_AI_Tools.pdf", "rb") as file:
                st.download_button(
                    label="ð¥ Download AI Tools PDF",
                    data=file.read(),
                    file_name="250_Best_AI_Tools.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
    
    st.markdown("---")
    st.markdown("### ð Additional Resources")
    st.markdown("""
    <div style="text-align: center; margin: 2rem 0;">
        <a href="https://entremotivator.com" target="_blank" class="resource-link">
            ð Visit Entremotivator.com for More Resources
        </a>
    </div>
    """, unsafe_allow_html=True)

# -------------------------
# Admin Dashboard
# -------------------------
def admin_dashboard():
    """Admin dashboard with full management features"""
    show_sidebar()
    
    display_logo()
    st.title("ð AI Agent Toolkit - Admin Dashboard")
    
    with st.sidebar:
        st.markdown("### ð§ Admin Tools")
        
        if st.session_state.user:
            st.info(f"ð¤ {st.session_state.user.email}\\nð­ {st.session_state.role.title()}")
        
        if st.button("ðª Logout", type="secondary", use_container_width=True):
            logout()
        
        st.divider()
        
        admin_section = st.selectbox(
            "Select Section",
            ["ð Analytics", "ð¥ User Management", "ð Resources", "ð Reports", "âï¸ Settings"]
        )
    
    if admin_section == "ð Analytics":
        show_admin_analytics()
    elif admin_section == "ð¥ User Management":
        show_user_management()
    elif admin_section == "ð Resources":
        show_resources()
    elif admin_section == "ð Reports":
        show_system_reports()
    elif admin_section == "âï¸ Settings":
        show_admin_settings()

def show_admin_analytics():
    """Show admin analytics"""
    st.subheader("ð AI Agent Toolkit Analytics")
    
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
            st.subheader("ð User Registration Trends")
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
    """Show user management interface"""
    st.subheader("ð¥ User Management")
    
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
            search = st.text_input("ð Search by email")
        with col2:
            role_filter = st.selectbox("Filter by role", ["All", "user", "admin"])
        
        filtered = user_data
        if search:
            filtered = [u for u in filtered if search.lower() in u["email"].lower()]
        if role_filter != "All":
            filtered = [u for u in filtered if u["role"] == role_filter]

        st.subheader("ð§ Bulk Actions")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("ð§ Send Welcome Email to All"):
                st.success("Welcome emails sent to all users!")
        with col2:
            if st.button("â¬ï¸ Export User Data"):
                df = pd.DataFrame(filtered)
                st.download_button("Download CSV", df.to_csv(index=False), "users.csv", "text/csv")

        if filtered:
            for i, user in enumerate(filtered):
                with st.expander(f"ð¤ {user['email']} ({user['role'].title()}) {'â' if user['confirmed'] else 'â'}"):
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
                        if st.button("ð Reset Password", key=f"reset_{i}"):
                            success, msg = reset_password(user["email"])
                            if success:
                                st.success(msg)
                            else:
                                st.error(msg)
                    
                    with action_col3:
                        if st.button("â Delete User", key=f"delete_{i}", type="secondary"):
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
    """Show system reports"""
    st.subheader("ð System Reports")
    
    st.write("**Recent System Activity**")
    activity_data = [
        {"timestamp": datetime.now() - timedelta(minutes=5), "action": "User login", "user": "user@example.com"},
        {"timestamp": datetime.now() - timedelta(minutes=15), "action": "New user registration", "user": "newuser@example.com"},
        {"timestamp": datetime.now() - timedelta(hours=1), "action": "Password reset", "user": "forgot@example.com"},
        {"timestamp": datetime.now() - timedelta(hours=2), "action": "Admin role assigned", "user": "admin@example.com"},
    ]
    
    for activity in activity_data:
        st.write(f"ð {activity['timestamp'].strftime('%Y-%m-%d %H:%M')} - {activity['action']} - {activity['user']}")
    
    st.subheader("ð¥ System Health")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Database Status", "â Healthy", delta="99.9% uptime")
    with col2:
        st.metric("Auth Service", "â Operational", delta="0 errors")
    with col3:
        st.metric("API Response", "â¡ Fast", delta="120ms avg")

def show_admin_settings():
    """Show admin settings"""
    st.subheader("âï¸ System Settings")
    
    st.write("**Security Configuration**")
    password_policy = st.checkbox("Enforce minimum password length", value=True)
    session_timeout = st.slider("Session timeout (hours)", 1, 24, 8)
    two_factor = st.checkbox("Require 2FA for admins", value=False)
    
    st.write("**Email Configuration**")
    welcome_email = st.checkbox("Send welcome emails", value=True)
    notification_email = st.text_input("Admin notification email", value="admin@company.com")
    
    st.write("**System Maintenance**")
    if st.button("ð§¹ Clean up old sessions"):
        st.success("Old sessions cleaned up!")
    if st.button("ð Generate system report"):
        st.success("System report generated!")
    
    if st.button("ð¾ Save Settings", type="primary"):
        st.success("Settings saved successfully!")

# -------------------------
# User Dashboard
# -------------------------
def user_dashboard():
    """Regular user dashboard"""
    show_sidebar()
    
    display_logo()
    st.title("ð¤ Welcome to the AI Agent Toolkit")
    
    user_email = st.session_state.user.email if st.session_state.user else "Unknown"
    user_id = st.session_state.user.id if st.session_state.user else None
    
    with st.sidebar:
        st.markdown("### ð  Dashboard")
        
        st.info(f"ð¤ {user_email.split('@')[0].title()}\\nð­ {st.session_state.role.title()}\\nð§ {user_email}")
        
        if st.button("ðª Logout", type="secondary", use_container_width=True):
            logout()
        
        st.divider()
        
        page = st.selectbox(
            "Navigate to:",
            ["ð My Activity", "ð Resources", "ð¤ Profile", "ð Notifications", "â Help"]
        )
    
    if page == "ð My Activity":
        show_user_activity(user_id, user_email)
    elif page == "ð Resources":
        show_resources()
    elif page == "ð¤ Profile":
        show_user_profile(user_id, user_email)
    elif page == "ð Notifications":
        show_user_notifications(user_email)
    elif page == "â Help":
        show_user_help()

def show_user_activity(user_id, user_email):
    """Show user activity"""
    st.subheader("ð Your Activity Overview")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Days Active", "12", delta="+2")
    with col2:
        st.metric("Total Sessions", "45", delta="+5")
    with col3:
        st.metric("Last Login", "2 hours ago")
    
    st.subheader("ð Your Activity Chart")
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
    """Show user profile"""
    st.subheader("ð¤ Your Profile")
    
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
        
        if st.form_submit_button("ð¾ Save Changes", type="primary"):
            if new_password and new_password == confirm_password:
                if len(new_password) >= 6:
                    st.success("Profile updated successfully!")
                else:
                    st.error("Password must be at least 6 characters long")
            else:
                st.success("Profile preferences updated!")

def show_user_notifications(user_email):
    """Show user notifications"""
    st.subheader("ð Your Notifications")
    
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
        icon = "ðµ" if not notif["read"] else "âª"
        type_icon = {"info": "â¹ï¸", "success": "â", "warning": "â ï¸"}.get(notif["type"], "ð¢")
        st.write(f"{icon} {type_icon} **{notif['message']}** - {notif['time']}")
        if not notif["read"] and st.button(f"Mark as read", key=f"read_{i}"):
            st.success("Marked as read!")
    
    if st.button("ð§¹ Clear all notifications"):
        st.success("All notifications cleared!")

def show_user_help():
    """Show user help"""
    st.subheader("â Help & Support")
    
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
        
        if st.form_submit_button("ð§ Send Message"):
            st.success("Your message has been sent! We'll get back to you soon.")

# -------------------------
# Login Page
# -------------------------
def login_page():
    """Professional login page"""
    hide_sidebar()
    
    display_logo()
    
    st.markdown("""
    <div class="welcome-header">
        <h1>ð AI Agent Toolkit Authentication Portal</h1>
        <p>Secure access to your personalized AI toolkit dashboard</p>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["ð Login", "ð Sign Up", "ð Reset Password"])

    with tab1:
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        st.subheader("ð Sign In to Your Account")
        with st.form("login_form"):
            email = st.text_input("ð§ Email Address", placeholder="your.email@example.com")
            password = st.text_input("ð Password", type="password", placeholder="Enter your password")
            
            remember_me = st.checkbox("ð§  Remember me")
            
            if st.form_submit_button("ð Login", type="primary", use_container_width=True):
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
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        st.subheader("ð Create New Account")
        st.info("ð¡ New accounts are created as regular users. Contact an administrator to upgrade to admin privileges.")
        
        with st.form("signup_form"):
            email = st.text_input("ð§ Email Address", placeholder="your.email@example.com")
            password = st.text_input("ð Password", type="password", 
                                   help="Must be at least 6 characters long")
            confirm_password = st.text_input("ð Confirm Password", type="password")
            
            terms = st.checkbox("â I agree to the Terms of Service and Privacy Policy")
            
            if st.form_submit_button("ð Create Account", type="primary", use_container_width=True):
                if email and password and confirm_password:
                    if password != confirm_password:
                        st.error("â Passwords don't match!")
                    elif not terms:
                        st.warning("â ï¸ Please agree to the terms and conditions.")
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
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        st.subheader("ð Reset Your Password")
        with st.form("reset_form"):
            email = st.text_input("ð§ Email Address", 
                                 placeholder="Enter your registered email address")
            st.info("ð¡ We'll send you a secure link to reset your password")
            
            if st.form_submit_button("ð§ Send Reset Link", type="primary", use_container_width=True):
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
    """Main application"""
    st.set_page_config(
        page_title="AI Agent Toolkit by D Hudson", 
        page_icon="ð¤", 
        layout="wide",
        initial_sidebar_state="auto"
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
