import streamlit as st
from supabase import create_client, Client
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import base64
import os
import json

# -------------------------
# Sidebar Widget State Management
# -------------------------
if "sidebar_closed" not in st.session_state:
    st.session_state.sidebar_closed = False
if "sidebar_visible" not in st.session_state:
    st.session_state.sidebar_visible = True

def toggle_sidebar():
    """Toggle sidebar visibility - once closed, cannot be reopened"""
    if not st.session_state.sidebar_closed:
        st.session_state.sidebar_visible = not st.session_state.sidebar_visible
        if not st.session_state.sidebar_visible:
            st.session_state.sidebar_closed = True

def sidebar_widget_css():
    """CSS for sidebar widget functionality"""
    if st.session_state.sidebar_closed:
        # Hide sidebar permanently once closed
        sidebar_display = "none !important"
        main_margin = "0 !important"
        widget_display = "none !important"
    elif st.session_state.sidebar_visible:
        # Show sidebar
        sidebar_display = "block !important"
        main_margin = "370px !important"
        widget_display = "block"
    else:
        # Hide sidebar but show toggle button
        sidebar_display = "none !important"
        main_margin = "0 !important"
        widget_display = "block"
    
    return f"""
    <style>
        /* Sidebar Widget Toggle Button */
        .sidebar-widget {{
            position: fixed;
            top: 20px;
            left: 20px;
            z-index: 999999;
            background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
            border: none;
            border-radius: 12px;
            padding: 12px 16px;
            color: #000000;
            font-weight: 600;
            font-family: 'Inter', sans-serif;
            cursor: pointer;
            box-shadow: 0 4px 12px rgba(245, 158, 11, 0.4);
            transition: all 0.3s ease;
            display: {widget_display};
        }}
        
        .sidebar-widget:hover {{
            background: linear-gradient(135deg, #d97706 0%, #b45309 100%);
            box-shadow: 0 6px 20px rgba(245, 158, 11, 0.6);
            transform: translateY(-2px);
        }}
        
        .sidebar-widget.closed {{
            background: #6b7280;
            cursor: not-allowed;
            opacity: 0.6;
        }}
        
        .sidebar-widget.closed:hover {{
            background: #6b7280;
            transform: none;
            box-shadow: 0 4px 12px rgba(107, 114, 128, 0.4);
        }}
        
        /* Sidebar Control */
        section[data-testid="stSidebar"] {{
            display: {sidebar_display};
            visibility: visible !important;
            width: 350px !important;
            min-width: 350px !important;
        }}
        
        .css-1d391kg, .st-emotion-cache-1d391kg {{
            display: {sidebar_display};
            visibility: visible !important;
            width: 350px !important;
        }}
        
        /* Main content adjustment */
        .main .block-container {{
            padding-left: {main_margin};
            transition: padding-left 0.3s ease;
        }}
        
        /* Widget status indicator */
        .widget-status {{
            position: fixed;
            top: 70px;
            left: 20px;
            z-index: 999998;
            background: rgba(30, 41, 59, 0.9);
            color: #ffffff;
            padding: 8px 12px;
            border-radius: 8px;
            font-size: 12px;
            font-family: 'Inter', sans-serif;
            border: 1px solid #475569;
            display: {widget_display};
        }}
    </style>
    """

def render_sidebar_widget():
    """Render the sidebar toggle widget"""
    if st.session_state.sidebar_closed:
        button_text = "🚫 Sidebar Permanently Closed"
        button_class = "sidebar-widget closed"
        status_text = "Status: Sidebar permanently closed"
        onclick = ""
    elif st.session_state.sidebar_visible:
        button_text = "◀️ Close Sidebar"
        button_class = "sidebar-widget"
        status_text = "Status: Sidebar open"
        onclick = "document.getElementById('close-sidebar-btn').click();"
    else:
        button_text = "▶️ Open Sidebar"
        button_class = "sidebar-widget"
        status_text = "Status: Sidebar closed (can reopen)"
        onclick = "document.getElementById('open-sidebar-btn').click();"
    
    widget_html = f"""
    <div class="{button_class}" onclick="{onclick}">
        {button_text}
    </div>
    <div class="widget-status">
        {status_text}
    </div>
    """
    
    st.markdown(widget_html, unsafe_allow_html=True)
    
    # Hidden buttons for Streamlit interaction
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Close Sidebar", key="close-sidebar-btn", help="Close sidebar permanently"):
            if not st.session_state.sidebar_closed:
                st.session_state.sidebar_visible = False
                st.session_state.sidebar_closed = True
                st.rerun()
    
    with col2:
        if st.button("Open Sidebar", key="open-sidebar-btn", help="Open sidebar"):
            if not st.session_state.sidebar_closed:
                st.session_state.sidebar_visible = True
                st.rerun()
    
    # Style the hidden buttons
    st.markdown("""
    <style>
        div[data-testid="column"]:has(button[kind="secondary"]) {
            display: none !important;
        }
    </style>
    """, unsafe_allow_html=True)

# -------------------------
# Hide Streamlit Elements
# -------------------------
def hide_streamlit_style():
    """Hide Streamlit default elements for cloud deployment - only GitHub link"""
    hide_st_style = """
            <style>
            /* Hide GitHub link specifically */
            .stActionButton[data-testid="stActionButton"] {display: none;}
            .stAppViewContainer > .main .stActionButton {display: none;}
            div[data-testid="stActionButton"] {display: none;}
            
            /* Hide specific GitHub deployment elements */
            .stDeployButton {display: none !important;}
            div[data-testid="stDecoration"] {display: none;}
            div[data-testid="stToolbar"] {visibility: hidden;}
            
            /* Keep other elements visible but hide GitHub link */
            #MainMenu {visibility: visible;}
            footer {visibility: visible;}
            header {visibility: visible;}
            
            /* Ensure sidebar is always visible and prominent when not closed */
            section[data-testid="stSidebar"] {
                width: 350px !important;
                min-width: 350px !important;
            }
            
            .css-1d391kg, .st-emotion-cache-1d391kg {
                width: 350px !important;
            }
            </style>
            """
    st.markdown(hide_st_style, unsafe_allow_html=True)

# -------------------------
# Professional Styling
# -------------------------
def apply_custom_css():
    """Apply professional AI Agent Toolkit theme with enhanced sidebar"""
    hide_streamlit_style()
    
    # Apply sidebar widget CSS
    st.markdown(sidebar_widget_css(), unsafe_allow_html=True)
    
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
    
    /* <CHANGE> Enhanced Sidebar styling - Fixed and always visible */
    .css-1d391kg,
    .st-emotion-cache-1d391kg,
    section[data-testid="stSidebar"] {
        display: block !important;
        visibility: visible !important;
        background: linear-gradient(180deg, #1e293b 0%, #334155 100%) !important;
        color: white !important;
        border-right: 3px solid #f59e0b !important;
        box-shadow: 4px 0 20px rgba(245, 158, 11, 0.3) !important;
        width: 350px !important;
        min-width: 350px !important;
    }
    
    section[data-testid="stSidebar"] > div {
        background: linear-gradient(180deg, #1e293b 0%, #334155 100%) !important;
        padding: 2rem 1.5rem !important;
    }
    
    /* Sidebar content styling */
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
        font-family: 'Inter', sans-serif;
    }
    
    /* Sidebar headers */
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: #f59e0b !important;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: 700;
    }
    
    /* Enhanced sidebar buttons */
    section[data-testid="stSidebar"] .stButton > button {
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%) !important;
        color: #000000 !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.75rem 1.5rem !important;
        font-weight: 600 !important;
        font-family: 'Inter', sans-serif !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 12px rgba(245, 158, 11, 0.4) !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        width: 100% !important;
        margin: 0.5rem 0 !important;
    }
    
    section[data-testid="stSidebar"] .stButton > button:hover {
        background: linear-gradient(135deg, #d97706 0%, #b45309 100%) !important;
        box-shadow: 0 6px 20px rgba(245, 158, 11, 0.6) !important;
        transform: translateY(-2px) !important;
    }
    
    /* Sidebar selectbox styling */
    section[data-testid="stSidebar"] .stSelectbox > div > div > select {
        background: rgba(15, 23, 42, 0.9) !important;
        color: #ffffff !important;
        border: 2px solid #f59e0b !important;
        border-radius: 12px !important;
        font-weight: 500;
        padding: 0.75rem !important;
    }
    
    /* Sidebar info boxes */
    section[data-testid="stSidebar"] .stInfo {
        background: linear-gradient(135deg, rgba(245, 158, 11, 0.2) 0%, rgba(217, 119, 6, 0.2) 100%) !important;
        border: 2px solid #f59e0b !important;
        border-radius: 12px !important;
        padding: 1rem !important;
        margin: 1rem 0 !important;
        text-align: center;
        font-weight: 500;
    }
    
    /* Main content button styling */
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
    
    /* <CHANGE> Download button styling for JSON downloads */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.75rem 1.5rem !important;
        font-weight: 600 !important;
        font-family: 'Inter', sans-serif !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3) !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
    }
    
    .stDownloadButton > button:hover {
        background: linear-gradient(135deg, #059669 0%, #047857 100%) !important;
        box-shadow: 0 6px 20px rgba(16, 185, 129, 0.5) !important;
        transform: translateY(-2px) !important;
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
    
    /* Collaboration features */
    .collaboration-section {
        background: linear-gradient(135deg, rgba(245, 158, 11, 0.1) 0%, rgba(217, 119, 6, 0.1) 100%);
        border: 2px solid #f59e0b;
        border-radius: 16px;
        padding: 2rem;
        margin: 2rem 0;
        text-align: center;
    }
    
    .collaboration-section h3 {
        color: #f59e0b !important;
        margin-bottom: 1rem;
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

def force_show_sidebar():
    """Force sidebar to be visible and prominent when not closed"""
    if not st.session_state.sidebar_closed and st.session_state.sidebar_visible:
        st.markdown("""
        <style>
            /* Force sidebar visibility with !important */
            section[data-testid="stSidebar"] {
                display: block !important;
                visibility: visible !important;
                width: 350px !important;
                min-width: 350px !important;
                z-index: 999999 !important;
            }
            
            .css-1d391kg, .st-emotion-cache-1d391kg {
                display: block !important;
                visibility: visible !important;
                width: 350px !important;
                z-index: 999999 !important;
            }
        </style>
        """, unsafe_allow_html=True)

# -------------------------
# Supabase Setup
# -------------------------
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
        return False, "⚠️ Please fill in all fields."
    
    if len(password) < 6:
        return False, "⚠️ Password must be at least 6 characters long."
    
    try:
        res = supabase.auth.sign_up({"email": email, "password": password})
        if res.user:
            # Always create as regular user
            supabase.table("user_profiles").insert({
                "id": res.user.id,
                "email": email,
                "role": "user"  # Always user, no admin signup
            }).execute()
            return True, "✅ Account created! Please check your email to verify your account, then log in."
        return False, "❌ Failed to create account."
    except Exception as e:
        error_msg = str(e)
        if "already registered" in error_msg.lower():
            return False, "⚠️ Email already registered. Try logging in."
        return False, f"❌ Signup error: {error_msg}"

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
            return True, f"✅ Welcome to the AI Agent Toolkit! Logged in as {role.capitalize()}"
        return False, "❌ Invalid email or password."
    except Exception as e:
        return False, f"❌ Login error: {str(e)}"

def reset_password(email):
    """Reset password"""
    try:
        supabase.auth.reset_password_for_email(email)
        return True, f"✅ Password reset email sent to {email}"
    except Exception as e:
        return False, f"❌ Reset error: {str(e)}"

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
# <CHANGE> Enhanced JSON Download Functions
# -------------------------
def get_user_data_as_json():
    """Get user data from Supabase as JSON"""
    try:
        # Get user profiles
        users = supabase.table("user_profiles").select("*").execute()
        
        # Get auth users for additional info
        auth_users = supabase.auth.admin.list_users()
        
        # Combine data
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
        
        return {
            "export_timestamp": datetime.now().isoformat(),
            "total_users": len(user_data),
            "users": user_data
        }
    except Exception as e:
        st.error(f"Error fetching user data: {e}")
        return None

def get_analytics_data_as_json():
    """Get analytics data as JSON"""
    try:
        users = supabase.table("user_profiles").select("*").execute()
        auth_users = supabase.auth.admin.list_users()
        
        total_users = len(users.data or [])
        admin_count = len([u for u in users.data or [] if u["role"] == "admin"])
        user_count = total_users - admin_count
        confirmed_users = len([u for u in auth_users.user if getattr(u, 'email_confirmed_at', None)])
        
        # Generate sample activity data
        dates = pd.date_range(start='2024-01-01', end=datetime.now(), freq='D')
        activity_data = []
        for date in dates:
            activity_data.append({
                "date": date.strftime('%Y-%m-%d'),
                "registrations": max(0, int(abs(hash(str(date)) % 8) - 3)),
                "active_users": max(0, int(abs(hash(str(date)) % 20) - 5))
            })
        
        return {
            "export_timestamp": datetime.now().isoformat(),
            "summary": {
                "total_users": total_users,
                "regular_users": user_count,
                "administrators": admin_count,
                "confirmed_users": confirmed_users
            },
            "daily_activity": activity_data,
            "user_roles": {
                "users": user_count,
                "admins": admin_count
            }
        }
    except Exception as e:
        st.error(f"Error generating analytics data: {e}")
        return None

def get_system_config_as_json():
    """Get system configuration as JSON"""
    return {
        "export_timestamp": datetime.now().isoformat(),
        "system_info": {
            "app_name": "AI Agent Toolkit",
            "version": "2.0.0",
            "author": "D Hudson",
            "environment": "production"
        },
        "features": {
            "authentication": True,
            "user_management": True,
            "analytics": True,
            "resource_downloads": True,
            "community_features": True
        },
        "integrations": {
            "supabase": True,
            "streamlit": True,
            "plotly": True
        }
    }

# -------------------------
# Resource Downloads
# -------------------------
def show_resources():
    """Display downloadable resources"""
    st.subheader("📚 AI Agent Toolkit Resources")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📋 The Ultimate AI & Bot Checklist")
        st.write("A comprehensive checklist to guide you through every stage of AI agent development.")
        
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
        st.write("A curated list of the most innovative and effective AI tools available today.")
        
        if os.path.exists("/home/ubuntu/ai-agent-toolkit/250_Best_AI_Tools.pdf"):
            with open("/home/ubuntu/ai-agent-toolkit/250_Best_AI_Tools.pdf", "rb") as file:
                st.download_button(
                    label="📥 Download AI Tools PDF",
                    data=file.read(),
                    file_name="250_Best_AI_Tools.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
    
    # <CHANGE> Added JSON download section
    st.markdown("---")
    st.markdown("### 📊 JSON Data Downloads")
    st.write("Export system data in JSON format for analysis or backup purposes.")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📥 Download User Data JSON", use_container_width=True):
            user_json = get_user_data_as_json()
            if user_json:
                st.download_button(
                    label="💾 Save User Data JSON",
                    data=json.dumps(user_json, indent=2),
                    file_name=f"user_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json",
                    use_container_width=True
                )
    
    with col2:
        if st.button("📊 Download Analytics JSON", use_container_width=True):
            analytics_json = get_analytics_data_as_json()
            if analytics_json:
                st.download_button(
                    label="💾 Save Analytics JSON",
                    data=json.dumps(analytics_json, indent=2),
                    file_name=f"analytics_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json",
                    use_container_width=True
                )
    
    with col3:
        if st.button("⚙️ Download System Config JSON", use_container_width=True):
            config_json = get_system_config_as_json()
            if config_json:
                st.download_button(
                    label="💾 Save Config JSON",
                    data=json.dumps(config_json, indent=2),
                    file_name=f"system_config_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json",
                    use_container_width=True
                )
    
    st.markdown("---")
    st.markdown("### 🌐 Additional Resources")
    st.markdown("""
    <div style="text-align: center; margin: 2rem 0;">
        <a href="https://entremotivator.com" target="_blank" class="resource-link">
            🚀 Visit Entremotivator.com for More Resources
        </a>
    </div>
    """, unsafe_allow_html=True)

    # Add collaboration section
    show_collaboration_section()

def show_collaboration_section():
    """Show collaboration features"""
    st.markdown("""
    <div class="collaboration-section">
        <h3>🤝 Collaborate with the Community</h3>
        <p>Join our growing community of AI enthusiasts and professionals!</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("💬 Join Discussion Forum", use_container_width=True):
            st.success("Redirecting to community forum...")
    with col2:
        if st.button("📖 Share Your Experience", use_container_width=True):
            st.success("Opening experience sharing form...")
    with col3:
        if st.button("🎯 Request Feature", use_container_width=True):
            st.success("Opening feature request form...")

# -------------------------
# Admin Dashboard
# -------------------------
def admin_dashboard():
    """Admin dashboard with full management features"""
    force_show_sidebar()
    
    display_logo()
    st.title("🎛️ AI Agent Toolkit - Admin Dashboard")
    
    # Render sidebar widget
    render_sidebar_widget()
    
    # <CHANGE> Fixed sidebar - always visible and properly styled
    if st.session_state.sidebar_visible and not st.session_state.sidebar_closed:
        with st.sidebar:
            st.markdown("### 🎛️ Admin Command Center")
            st.markdown("---")
            
            if st.session_state.user:
                st.markdown(f"""
                <div style="text-align: center; padding: 1rem; background: rgba(245, 158, 11, 0.1); border-radius: 12px; margin: 1rem 0;">
                    <h4>👑 Administrator</h4>
                    <p><strong>Email:</strong> {st.session_state.user.email}</p>
                    <p><strong>Role:</strong> {st.session_state.role.title()}</p>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("### 🚀 Quick Actions")
            if st.button("🔄 Refresh Data", use_container_width=True):
                st.success("Data refreshed!")
            
            if st.button("📊 Export Reports", use_container_width=True):
                st.success("Reports exported!")
            
            if st.button("🚪 Logout", type="secondary", use_container_width=True):
                logout()
            
            st.markdown("---")
            
            admin_section = st.selectbox(
                "📋 Select Admin Section",
                ["📊 Analytics", "👥 User Management", "📚 Resources", "📋 Reports", "⚙️ Settings"],
                help="Choose the admin section you want to manage"
            )
            
            st.markdown("---")
            st.markdown("### 🎯 System Status")
            st.success("🟢 All Systems Operational")
            st.info("👥 Active Users: 156")
            st.warning("⚡ Server Load: Medium")
    else:
        admin_section = "📊 Analytics"  # Default when sidebar is closed
    
    if admin_section == "📊 Analytics":
        show_admin_analytics()
    elif admin_section == "👥 User Management":
        show_user_management()
    elif admin_section == "📚 Resources":
        show_resources()
    elif admin_section == "📋 Reports":
        show_system_reports()
    elif admin_section == "⚙️ Settings":
        show_admin_settings()

def show_admin_analytics():
    """Show admin analytics"""
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
    """Show user management interface"""
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

        st.subheader("🎯 Bulk Actions")
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
                        if st.button("🔐 Reset Password", key=f"reset_{i}"):
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
    """Show system reports"""
    st.subheader("📋 System Reports")
    
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
    """Show admin settings"""
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
    """User dashboard with personalized features"""
    force_show_sidebar()
    
    display_logo()
    st.title("🚀 AI Agent Toolkit - Your Personal Dashboard")
    
    # Render sidebar widget
    render_sidebar_widget()
    
    # <CHANGE> Fixed sidebar - always visible and properly styled
    if st.session_state.sidebar_visible and not st.session_state.sidebar_closed:
        with st.sidebar:
            st.markdown("### 🎯 Your AI Toolkit")
            st.markdown("---")
            
            if st.session_state.user:
                st.markdown(f"""
                <div style="text-align: center; padding: 1rem; background: rgba(245, 158, 11, 0.1); border-radius: 12px; margin: 1rem 0;">
                    <h4>👤 Welcome Back!</h4>
                    <p><strong>Email:</strong> {st.session_state.user.email}</p>
                    <p><strong>Role:</strong> {st.session_state.role.title()}</p>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("### 🚀 Quick Actions")
            if st.button("📚 Browse Resources", use_container_width=True):
                st.success("Loading resources...")
            
            if st.button("🤝 Join Community", use_container_width=True):
                st.success("Connecting to community...")
            
            if st.button("🚪 Logout", type="secondary", use_container_width=True):
                logout()
            
            st.markdown("---")
            
            user_section = st.selectbox(
                "📋 Select Section",
                ["🏠 Dashboard", "📚 Resources", "🤝 Community", "👤 Profile", "🔔 Notifications", "❓ Help"],
                help="Choose the section you want to explore"
            )
            
            st.markdown("---")
            st.markdown("### 🎯 Your Progress")
            st.progress(0.7, text="Profile Completion: 70%")
            st.progress(0.4, text="Resources Downloaded: 40%")
            st.progress(0.9, text="Community Engagement: 90%")
    else:
        user_section = "🏠 Dashboard"  # Default when sidebar is closed
    
    if user_section == "🏠 Dashboard":
        show_user_dashboard_home()
    elif user_section == "📚 Resources":
        show_resources()
    elif user_section == "🤝 Community":
        show_community_features()
    elif user_section == "👤 Profile":
        show_user_profile(st.session_state.user.id, st.session_state.user.email)
    elif user_section == "🔔 Notifications":
        show_user_notifications(st.session_state.user.email)
    elif user_section == "❓ Help":
        show_user_help()

def show_user_dashboard_home():
    """Show user dashboard home"""
    st.subheader("🏠 Welcome to Your AI Agent Toolkit Dashboard")
    
    # Welcome message
    st.markdown("""
    <div class="dashboard-card">
        <h3>🎯 Your AI Journey Starts Here</h3>
        <p>Welcome to the most comprehensive AI Agent Toolkit available. Explore resources, connect with the community, and accelerate your AI development journey.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick stats
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Resources Available", "250+", delta="New tools added weekly")
    with col2:
        st.metric("Community Members", "1,500+", delta="+50 this week")
    with col3:
        st.metric("Success Stories", "89", delta="+5 this month")
    with col4:
        st.metric("Your Downloads", "3", delta="+1 today")
    
    # Recent activity
    st.subheader("📈 Your Recent Activity")
    activity_chart_data = pd.DataFrame({
        'Date': pd.date_range(start='2024-01-01', periods=30, freq='D'),
        'Activity Score': [abs(hash(str(d)) % 10) for d in pd.date_range(start='2024-01-01', periods=30, freq='D')]
    })
    
    fig = px.area(activity_chart_data, x='Date', y='Activity Score', 
                  title='Your 30-Day Activity Trend',
                  color_discrete_sequence=['#f59e0b'])
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='#ffffff'
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Progress tracking
    st.subheader("🏆 Achievement Progress")
    col1, col2 = st.columns(2)
    with col1:
        st.progress(0.7, text="AI Toolkit Explorer: 70%")
        st.progress(0.4, text="Resource Collector: 40%")
    with col2:
        st.progress(0.9, text="Daily User: 90%")
        st.progress(0.2, text="Community Contributor: 20%")

def show_user_profile(user_id, user_email):
    """Show user profile"""
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
    """Show user notifications"""
    st.subheader("🔔 Your Notifications")
    
    st.write("**Notification Preferences**")
    email_notifications = st.checkbox("Email notifications", value=True)
    security_alerts = st.checkbox("Security alerts", value=True)
    product_updates = st.checkbox("Product updates", value=False)
    community_updates = st.checkbox("Community updates", value=True)
    
    st.write("**Recent Notifications**")
    notifications = [
        {"time": "1 hour ago", "message": "Welcome to the AI Agent Toolkit!", "type": "info", "read": False},
        {"time": "1 day ago", "message": "Your profile was updated", "type": "success", "read": True},
        {"time": "3 days ago", "message": "Security: New login detected", "type": "warning", "read": True},
        {"time": "1 week ago", "message": "New community challenge available!", "type": "info", "read": False},
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
    """Show user help"""
    st.subheader("❓ Help & Support")
    
    st.write("**Frequently Asked Questions**")
    
    with st.expander("How do I change my password?"):
        st.write("Go to the Profile tab and enter your current password along with your new password.")
    
    with st.expander("How do I download the AI resources?"):
        st.write("Visit the Resources tab to download the Ultimate AI & Bot Checklist and 250 Best AI Tools PDF guides.")
    
    with st.expander("How do I update my notification preferences?"):
        st.write("Visit the Notifications tab to customize which notifications you receive.")
    
    with st.expander("How can I collaborate with other users?"):
        st.write("Visit the Community tab to join discussions, participate in challenges, and share your experiences.")
    
    with st.expander("Who can I contact for support?"):
        st.write("You can reach out to our support team at support@entremotivator.com")
    
    st.write("**Contact Support**")
    with st.form("support_form"):
        subject = st.selectbox("Subject", ["General Question", "Technical Issue", "Feature Request", "Bug Report", "Community Help"])
        message = st.text_area("Message", placeholder="Describe your question or issue...")
        
        if st.form_submit_button("📧 Send Message"):
            st.success("Your message has been sent! We'll get back to you soon.")

def show_community_features():
    """Show community collaboration features"""
    st.subheader("🤝 Community & Collaboration")
    
    st.markdown("""
    <div class="collaboration-section">
        <h3>🌟 Connect with Fellow AI Enthusiasts</h3>
        <p>Join our vibrant community of AI practitioners, developers, and enthusiasts!</p>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["💬 Discussions", "🏆 Challenges", "📝 Share Experience", "🤖 AI Showcase"])
    
    with tab1:
        st.subheader("💬 Community Discussions")
        st.write("**Popular Topics**")
        topics = [
            {"title": "Best AI Tools for 2024", "replies": 45, "last_active": "2 hours ago"},
            {"title": "Automation Success Stories", "replies": 32, "last_active": "4 hours ago"},
            {"title": "Claude vs GPT-4 Comparison", "replies": 67, "last_active": "1 day ago"},
            {"title": "Getting Started with AI Agents", "replies": 28, "last_active": "2 days ago"},
        ]
        
        for topic in topics:
            with st.expander(f"🗨️ {topic['title']} ({topic['replies']} replies)"):
                st.write(f"**Last Activity:** {topic['last_active']}")
                st.write("Join the discussion and share your thoughts!")
                if st.button(f"Join Discussion", key=f"join_{topic['title']}"):
                    st.success("Joining discussion thread...")
        
        if st.button("➕ Start New Discussion", type="primary"):
            st.success("Opening new discussion form...")
    
    with tab2:
        st.subheader("🏆 Community Challenges")
        st.write("**Current Challenges**")
        challenges = [
            {"name": "30-Day AI Automation Challenge", "participants": 156, "days_left": 12},
            {"name": "Build Your First AI Agent", "participants": 89, "days_left": 25},
            {"name": "AI Tool Discovery Marathon", "participants": 203, "days_left": 5},
        ]
        
        for challenge in challenges:
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"**{challenge['name']}**")
                st.write(f"👥 {challenge['participants']} participants | ⏰ {challenge['days_left']} days left")
            with col2:
                if st.button("Join", key=f"join_{challenge['name']}"):
                    st.success(f"Joined {challenge['name']}!")
    
    with tab3:
        st.subheader("📝 Share Your Experience")
        with st.form("experience_form"):
            experience_type = st.selectbox("Experience Type", 
                ["Success Story", "Lesson Learned", "Tool Review", "Tutorial", "Case Study"])
            title = st.text_input("Title")
            content = st.text_area("Share your experience...", height=200)
            tags = st.text_input("Tags (comma-separated)", placeholder="ai, automation, productivity")
            
            if st.form_submit_button("📤 Share Experience"):
                st.success("Thank you for sharing! Your experience will help others in the community.")
                st.balloons()
    
    with tab4:
        st.subheader("🤖 AI Showcase")
        st.write("**Featured AI Projects from Community**")
        projects = [
            {"title": "Customer Service Bot", "author": "John D.", "likes": 45, "description": "Automated customer support using Claude"},
            {"title": "Content Generation Pipeline", "author": "Sarah M.", "likes": 67, "description": "AI-powered content creation workflow"},
            {"title": "Data Analysis Assistant", "author": "Mike R.", "likes": 34, "description": "Intelligent data insights generator"},
        ]
        
        for project in projects:
            with st.expander(f"🚀 {project['title']} by {project['author']} (👍 {project['likes']})"):
                st.write(project['description'])
                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button("👍 Like", key=f"like_{project['title']}"):
                        st.success("Liked!")
                with col2:
                    if st.button("💬 Comment", key=f"comment_{project['title']}"):
                        st.success("Opening comments...")
                with col3:
                    if st.button("🔗 Learn More", key=f"learn_{project['title']}"):
                        st.success("Loading project details...")

# -------------------------
# Login Page
# -------------------------
def login_page():
    """Professional login page without sidebar"""
    st.markdown("""
    <style>
        section[data-testid="stSidebar"] {display: none !important;}
        .css-1d391kg {display: none !important;}
        .css-6qob1r {display: none !important;}
        .e1fqkh3o3 {display: none !important;}
        .st-emotion-cache-1d391kg {display: none !important;}
        .st-emotion-cache-6qob1r {display: none !important;}
        .sidebar-widget {display: none !important;}
        .widget-status {display: none !important;}
    </style>
    """, unsafe_allow_html=True)
    
    display_logo()
    
    st.markdown("""
    <div class="welcome-header">
        <h1>🎯 AI Agent Toolkit Authentication Portal</h1>
        <p>Secure access to your personalized AI toolkit dashboard</p>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["🔑 Login", "📝 Sign Up", "🔐 Reset Password"])

    with tab1:
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        st.subheader("🔑 Sign In to Your Account")
        with st.form("login_form"):
            email = st.text_input("📧 Email Address", placeholder="your.email@example.com")
            password = st.text_input("🔒 Password", type="password", placeholder="Enter your password")
            
            remember_me = st.checkbox("🧠 Remember me")
            
            if st.form_submit_button("🔑 Login", type="primary", use_container_width=True):
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
        st.subheader("📝 Create New Account")

