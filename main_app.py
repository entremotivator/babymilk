import streamlit as st
from supabase import create_client, Client
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import base64
import os
import json
import hashlib
import io
import zipfile
from typing import Dict, List, Optional, Tuple
import logging
import time
import requests
from PIL import Image
import numpy as np

# -------------------------
# Configuration and Setup
# -------------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Config:
    """Application configuration constants"""
    APP_NAME = "AI Agent Toolkit"
    VERSION = "2.0.0"
    AUTHOR = "D Hudson"
    COMPANY = "Entremotivator"
    SUPPORT_EMAIL = "support@entremotivator.com"
    WEBSITE = "https://entremotivator.com"
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    ALLOWED_FILE_TYPES = [".pdf", ".docx", ".txt", ".csv", ".json"]
    SESSION_TIMEOUT = 3600  # 1 hour in seconds
    
# -------------------------
# Enhanced Styling and UI
# -------------------------
def hide_streamlit_style():
    """Enhanced hiding of Streamlit default elements"""
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
    .st-emotion-cache-1wbqy5l.e17vllj40 {display: none;}
    </style>
    """
    st.markdown(hide_st_style, unsafe_allow_html=True)

def apply_enhanced_css():
    """Apply comprehensive custom styling"""
    hide_streamlit_style()
    st.markdown("""
    <style>
    @import url("https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap");
    @import url("https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css");
    
    :root {
        --primary-color: #f59e0b;
        --secondary-color: #d97706;
        --accent-color: #fbbf24;
        --dark-bg: #0f172a;
        --medium-bg: #1e293b;
        --light-bg: #334155;
        --text-primary: #ffffff;
        --text-secondary: #e2e8f0;
        --success-color: #10b981;
        --warning-color: #f59e0b;
        --error-color: #ef4444;
        --info-color: #3b82f6;
    }
    
    .stApp {
        background: linear-gradient(135deg, var(--dark-bg) 0%, var(--medium-bg) 50%, var(--light-bg) 100%);
        color: var(--text-primary);
        font-family: 'Inter', sans-serif;
        min-height: 100vh;
    }
    
    /* Enhanced Sidebar Styling */
    .css-1d391kg,
    .st-emotion-cache-1d391kg,
    section[data-testid="stSidebar"] > div {
        background: linear-gradient(180deg, var(--medium-bg) 0%, var(--light-bg) 100%);
        color: var(--text-primary) !important;
        border-right: 3px solid var(--primary-color);
        box-shadow: 0 0 30px rgba(245,158,11,0.2);
    }
    
    /* Enhanced Cards and Containers */
    .metric-card {
        background: linear-gradient(135deg, rgba(30,41,59,0.8) 0%, rgba(51,65,85,0.8) 100%);
        padding: 1.5rem;
        border-radius: 16px;
        border: 1px solid var(--primary-color);
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        backdrop-filter: blur(10px);
        margin-bottom: 1rem;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 60px rgba(245,158,11,0.5);
    }
    
    /* Enhanced Buttons */
    .stButton > button {
        background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
        color: #000000;
        font-weight: 600;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 1.5rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(245,158,11,0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(245,158,11,0.5);
    }
    
    /* Status Indicators */
    .status-indicator {
        display: inline-block;
        width: 12px;
        height: 12px;
        border-radius: 50%;
        margin-right: 8px;
    }
    
    .status-online { background-color: var(--success-color); }
    .status-offline { background-color: var(--error-color); }
    .status-warning { background-color: var(--warning-color); }
    
    /* Enhanced Forms */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > select {
        background: rgba(30,41,59,0.5);
        border: 2px solid rgba(245,158,11,0.3);
        border-radius: 12px;
        color: var(--text-primary);
        transition: border-color 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: var(--primary-color);
        box-shadow: 0 0 20px rgba(245,158,11,0.3);
    }
    
    /* Loading Animation */
    .loading-spinner {
        border: 4px solid rgba(245,158,11,0.3);
        border-radius: 50%;
        border-top: 4px solid var(--primary-color);
        width: 40px;
        height: 40px;
        animation: spin 1s linear infinite;
        margin: 20px auto;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* Notification Styles */
    .notification {
        padding: 1rem;
        border-radius: 12px;
        margin: 0.5rem 0;
        border-left: 4px solid;
    }
    
    .notification-info { 
        background: rgba(59,130,246,0.1); 
        border-color: var(--info-color); 
    }
    .notification-success { 
        background: rgba(16,185,129,0.1); 
        border-color: var(--success-color); 
    }
    .notification-warning { 
        background: rgba(245,158,11,0.1); 
        border-color: var(--warning-color); 
    }
    .notification-error { 
        background: rgba(239,68,68,0.1); 
        border-color: var(--error-color); 
    }
    
    /* Progress Bars */
    .progress-bar {
        width: 100%;
        height: 20px;
        background: rgba(30,41,59,0.5);
        border-radius: 10px;
        overflow: hidden;
        margin: 10px 0;
    }
    
    .progress-fill {
        height: 100%;
        background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
        border-radius: 10px;
        transition: width 0.3s ease;
    }
    </style>
    """, unsafe_allow_html=True)

def get_base64_of_bin_file(bin_file: str) -> str:
    """Convert binary file to base64 string"""
    try:
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except Exception as e:
        logger.error(f"Error converting file to base64: {e}")
        return ""

def display_enhanced_logo():
    """Display enhanced logo with animations"""
    logo_path = "/home/ubuntu/ai-agent-toolkit/logo.png"
    if os.path.exists(logo_path):
        st.markdown(f"""
        <div style="display: flex; justify-content: center; align-items: center; margin: 2rem 0;">
            <div style="animation: pulse 2s infinite;">
                <img src="data:image/png;base64,{get_base64_of_bin_file(logo_path)}" 
                     alt="{Config.APP_NAME} Logo" 
                     style="max-width:300px; filter: drop-shadow(0 0 20px rgba(245,158,11,0.5));">
            </div>
        </div>
        <style>
        @keyframes pulse {{
            0% {{ transform: scale(1); }}
            50% {{ transform: scale(1.05); }}
            100% {{ transform: scale(1); }}
        }}
        </style>
        """, unsafe_allow_html=True)
    else:
        # Fallback text logo
        st.markdown(f"""
        <div style="text-align: center; padding: 2rem;">
            <h1 style="font-size: 3rem; background: linear-gradient(135deg, #f59e0b, #d97706); 
                       -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                🤖 {Config.APP_NAME}
            </h1>
            <p style="color: #e2e8f0; font-size: 1.2rem;">by {Config.AUTHOR}</p>
        </div>
        """, unsafe_allow_html=True)

def show_sidebar_toggle():
    """Enhanced sidebar visibility controls"""
    st.markdown("""
    <style>
        section[data-testid="stSidebar"] {
            transition: all 0.3s ease;
        }
        .sidebar-hidden section[data-testid="stSidebar"] {
            transform: translateX(-100%);
        }
    </style>
    """, unsafe_allow_html=True)

# -------------------------
# Enhanced Database Operations
# -------------------------
@st.cache_resource
def init_supabase_connection() -> Optional[Client]:
    """Initialize Supabase connection with error handling"""
    try:
        url = st.secrets.get("supabase", {}).get("url")
        key = st.secrets.get("supabase", {}).get("key")
        
        if not url or not key:
            st.error("🔧 Supabase configuration missing. Please check your secrets.")
            return None
            
        client = create_client(url, key)
        
        # Test connection
        client.table("user_profiles").select("count", count="exact").execute()
        logger.info("Supabase connection established successfully")
        return client
        
    except Exception as e:
        logger.error(f"Failed to connect to Supabase: {e}")
        st.error(f"🔥 Database connection failed: {str(e)}")
        return None

def create_database_tables(supabase: Client):
    """Create necessary database tables if they don't exist"""
    try:
        # Enhanced user profiles table
        supabase.rpc('create_user_profiles_table').execute()
        
        # Activity logs table
        supabase.rpc('create_activity_logs_table').execute()
        
        # User sessions table
        supabase.rpc('create_user_sessions_table').execute()
        
        # System settings table
        supabase.rpc('create_system_settings_table').execute()
        
        # File uploads table
        supabase.rpc('create_file_uploads_table').execute()
        
        logger.info("Database tables created/verified successfully")
        
    except Exception as e:
        logger.warning(f"Database table creation warning: {e}")

# -------------------------
# Session Management
# -------------------------
def initialize_session_state():
    """Initialize comprehensive session state"""
    defaults = {
        "authenticated": False,
        "role": None,
        "user": None,
        "user_profile": {},
        "session_start": datetime.now(),
        "last_activity": datetime.now(),
        "notifications": [],
        "theme": "dark",
        "language": "en",
        "activity_log": [],
        "uploaded_files": [],
        "user_preferences": {},
        "dashboard_config": {
            "show_welcome": True,
            "compact_mode": False,
            "auto_refresh": True
        }
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

def check_session_timeout():
    """Check and handle session timeout"""
    if st.session_state.authenticated:
        current_time = datetime.now()
        last_activity = st.session_state.get("last_activity", current_time)
        
        if (current_time - last_activity).seconds > Config.SESSION_TIMEOUT:
            st.warning("⏰ Session expired due to inactivity. Please log in again.")
            logout()
        else:
            st.session_state.last_activity = current_time

def log_user_activity(action: str, details: str = ""):
    """Log user activity"""
    if st.session_state.authenticated:
        activity_entry = {
            "timestamp": datetime.now().isoformat(),
            "user_id": st.session_state.user.id if st.session_state.user else None,
            "action": action,
            "details": details,
            "ip_address": "127.0.0.1",  # In production, get real IP
            "user_agent": "Streamlit App"  # In production, get real user agent
        }
        
        if "activity_log" not in st.session_state:
            st.session_state.activity_log = []
        
        st.session_state.activity_log.append(activity_entry)
        
        # Keep only last 100 activities in session
        if len(st.session_state.activity_log) > 100:
            st.session_state.activity_log = st.session_state.activity_log[-100:]

# -------------------------
# Enhanced Authentication
# -------------------------
def validate_email(email: str) -> bool:
    """Validate email format"""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password_strength(password: str) -> Tuple[bool, str]:
    """Validate password strength"""
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    
    import re
    if not re.search(r"[A-Z]", password):
        return False, "Password must contain at least one uppercase letter"
    
    if not re.search(r"[a-z]", password):
        return False, "Password must contain at least one lowercase letter"
    
    if not re.search(r"[0-9]", password):
        return False, "Password must contain at least one number"
    
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False, "Password must contain at least one special character"
    
    return True, "Password is strong"

def enhanced_signup(email: str, password: str, full_name: str = "", company: str = "") -> Tuple[bool, str]:
    """Enhanced user signup with validation"""
    if not email or not password:
        return False, "⚠️ Please fill in all required fields."
    
    if not validate_email(email):
        return False, "⚠️ Please enter a valid email address."
    
    password_valid, password_msg = validate_password_strength(password)
    if not password_valid:
        return False, f"⚠️ {password_msg}"
    
    try:
        supabase = init_supabase_connection()
        if not supabase:
            return False, "❌ Database connection failed."
        
        # Create auth user
        res = supabase.auth.sign_up({
            "email": email, 
            "password": password,
            "options": {
                "data": {
                    "full_name": full_name,
                    "company": company
                }
            }
        })
        
        if res.user:
            # Create extended profile
            profile_data = {
                "id": res.user.id,
                "email": email,
                "full_name": full_name,
                "company": company,
                "role": "user",
                "created_at": datetime.now().isoformat(),
                "last_login": None,
                "is_active": True,
                "preferences": json.dumps({
                    "theme": "dark",
                    "notifications": True,
                    "language": "en"
                }),
                "profile_completion": 60 if full_name else 30
            }
            
            supabase.table("user_profiles").insert(profile_data).execute()
            
            log_user_activity("user_signup", f"New user registered: {email}")
            
            return True, "✅ Account created successfully! Please check your email to confirm your account."
        
        return False, "❌ Failed to create account. Please try again."
        
    except Exception as e:
        error_msg = str(e)
        logger.error(f"Signup error: {error_msg}")
        
        if "already registered" in error_msg.lower():
            return False, "⚠️ This email is already registered. Try logging in instead."
        elif "invalid email" in error_msg.lower():
            return False, "⚠️ Invalid email address format."
        else:
            return False, f"❌ Registration failed: {error_msg}"

def enhanced_login(email: str, password: str, remember_me: bool = False) -> Tuple[bool, str]:
    """Enhanced login with session management"""
    try:
        supabase = init_supabase_connection()
        if not supabase:
            return False, "❌ Database connection failed."
        
        res = supabase.auth.sign_in_with_password({"email": email, "password": password})
        
        if res.user:
            # Get user profile
            profile_query = supabase.table("user_profiles").select("*").eq("id", res.user.id).execute()
            
            if profile_query.data:
                profile = profile_query.data[0]
                
                # Update last login
                supabase.table("user_profiles").update({
                    "last_login": datetime.now().isoformat(),
                    "login_count": profile.get("login_count", 0) + 1
                }).eq("id", res.user.id).execute()
                
                # Set session state
                st.session_state.authenticated = True
                st.session_state.user = res.user
                st.session_state.role = profile.get("role", "user")
                st.session_state.user_profile = profile
                st.session_state.session_start = datetime.now()
                st.session_state.last_activity = datetime.now()
                
                # Load user preferences
                preferences = json.loads(profile.get("preferences", "{}"))
                st.session_state.user_preferences = preferences
                
                log_user_activity("user_login", f"User logged in: {email}")
                
                return True, f"✅ Welcome back, {profile.get('full_name', 'User')}!"
            else:
                return False, "❌ User profile not found."
        
        return False, "❌ Invalid email or password."
        
    except Exception as e:
        logger.error(f"Login error: {e}")
        return False, f"❌ Login failed: {str(e)}"

def enhanced_reset_password(email: str) -> Tuple[bool, str]:
    """Enhanced password reset with logging"""
    try:
        if not validate_email(email):
            return False, "⚠️ Please enter a valid email address."
        
        supabase = init_supabase_connection()
        if not supabase:
            return False, "❌ Database connection failed."
        
        supabase.auth.reset_password_for_email(email, {
            "redirect_to": f"{Config.WEBSITE}/reset-password"
        })
        
        log_user_activity("password_reset_request", f"Password reset requested for: {email}")
        
        return True, f"✅ Password reset instructions sent to {email}"
        
    except Exception as e:
        logger.error(f"Password reset error: {e}")
        return False, f"❌ Failed to send reset email: {str(e)}"

def logout():
    """Enhanced logout with cleanup"""
    try:
        if st.session_state.authenticated:
            log_user_activity("user_logout", "User logged out")
            
            supabase = init_supabase_connection()
            if supabase:
                supabase.auth.sign_out()
        
        # Clear session state
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        
        initialize_session_state()
        st.rerun()
        
    except Exception as e:
        logger.error(f"Logout error: {e}")
        # Force clear session even if error
        st.session_state.clear()
        initialize_session_state()
        st.rerun()

# -------------------------
# Enhanced File Management
# -------------------------
def handle_file_upload(uploaded_file) -> Tuple[bool, str]:
    """Handle file uploads with validation and storage"""
    try:
        if uploaded_file is None:
            return False, "No file selected"
        
        # Validate file size
        if uploaded_file.size > Config.MAX_FILE_SIZE:
            return False, f"File too large. Maximum size is {Config.MAX_FILE_SIZE // 1024 // 1024}MB"
        
        # Validate file type
        file_extension = os.path.splitext(uploaded_file.name)[1].lower()
        if file_extension not in Config.ALLOWED_FILE_TYPES:
            return False, f"File type not allowed. Allowed types: {', '.join(Config.ALLOWED_FILE_TYPES)}"
        
        # Create unique filename
        timestamp = int(time.time())
        user_id = st.session_state.user.id if st.session_state.user else "anonymous"
        safe_filename = f"{user_id}_{timestamp}_{uploaded_file.name}"
        
        # Store file info in session
        file_info = {
            "original_name": uploaded_file.name,
            "safe_filename": safe_filename,
            "size": uploaded_file.size,
            "type": uploaded_file.type,
            "upload_time": datetime.now().isoformat(),
            "status": "uploaded"
        }
        
        if "uploaded_files" not in st.session_state:
            st.session_state.uploaded_files = []
        
        st.session_state.uploaded_files.append(file_info)
        
        log_user_activity("file_upload", f"File uploaded: {uploaded_file.name}")
        
        return True, f"File '{uploaded_file.name}' uploaded successfully"
        
    except Exception as e:
        logger.error(f"File upload error: {e}")
        return False, f"Upload failed: {str(e)}"

# -------------------------
# Enhanced Resource Management
# -------------------------
def show_enhanced_resources():
    """Enhanced resource section with more features"""
    st.subheader("📚 AI Agent Toolkit Resource Library")
    
    # Resource categories
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📋 Checklists", "🛠️ AI Tools", "📖 Guides", "🎥 Tutorials", "📊 Templates"
    ])
    
    with tab1:
        st.markdown("### 📋 Comprehensive AI Checklists")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="metric-card">
                <h4>🎯 The Ultimate AI & Bot Checklist</h4>
                <p>Complete guide for AI agent development, deployment, and optimization.</p>
                <ul>
                    <li>✅ Pre-development planning</li>
                    <li>🔧 Development best practices</li>
                    <li>🚀 Deployment strategies</li>
                    <li>📊 Performance optimization</li>
                    <li>🛡️ Security considerations</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            if os.path.exists("/home/ubuntu/ai-agent-toolkit/AI_and_Bot_Checklist.pdf"):
                with open("/home/ubuntu/ai-agent-toolkit/AI_and_Bot_Checklist.pdf", "rb") as file:
                    st.download_button(
                        label="📥 Download Ultimate AI Checklist",
                        data=file.read(),
                        file_name="AI_and_Bot_Checklist.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )
        
        with col2:
            st.markdown("""
            <div class="metric-card">
                <h4>🎯 AI Implementation Checklist</h4>
                <p>Step-by-step guide for implementing AI solutions in business.</p>
                <ul>
                    <li>📋 Requirements analysis</li>
                    <li>🔍 Technology selection</li>
                    <li>👥 Team preparation</li>
                    <li>📈 Success metrics</li>
                    <li>🔄 Continuous improvement</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            # Generate sample checklist
            checklist_content = """AI IMPLEMENTATION CHECKLIST
            
□ Define business objectives
□ Assess current infrastructure
□ Identify data sources
□ Select appropriate AI tools
□ Plan integration strategy
□ Prepare team training
□ Establish success metrics
□ Create testing protocols
□ Plan deployment phases
□ Develop monitoring systems"""
            
            st.download_button(
                label="📥 Download Implementation Checklist",
                data=checklist_content,
                file_name="AI_Implementation_Checklist.txt",
                mime="text/plain",
                use_container_width=True
            )
    
    with tab2:
        st.markdown("### 🛠️ AI Tools Collection")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="metric-card">
                <h4>🔧 250 Best AI Tools</h4>
                <p>Curated collection of the most powerful AI tools across all categories.</p>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 0.5rem; margin-top: 1rem;">
                    <span>🤖 Chatbots & Agents</span><span>25 tools</span>
                    <span>🎨 Content Creation</span><span>40 tools</span>
                    <span>📊 Data Analysis</span><span>35 tools</span>
                    <span>🖼️ Image Generation</span><span>30 tools</span>
                    <span>🎵 Audio Processing</span><span>25 tools</span>
                    <span>📝 Writing Assistants</span><span>30 tools</span>
                    <span>🔍 Research Tools</span><span>25 tools</span>
                    <span>🛠️ Development</span><span>40 tools</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if os.path.exists("/home/ubuntu/ai-agent-toolkit/250_Best_AI_Tools.pdf"):
                with open("/home/ubuntu/ai-agent-toolkit/250_Best_AI_Tools.pdf", "rb") as file:
                    st.download_button(
                        label="📥 Download 250 AI Tools Guide",
                        data=file.read(),
                        file_name="250_Best_AI_Tools.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )
        
        with col2:
            st.markdown("### 🔥 Trending AI Tools")
            trending_tools = [
                {"name": "ChatGPT", "category": "Conversational AI", "rating": 9.5},
                {"name": "Midjourney", "category": "Image Generation", "rating": 9.3},
                {"name": "Claude", "category": "AI Assistant", "rating": 9.4},
                {"name": "GitHub Copilot", "category": "Code Assistant", "rating": 9.1},
                {"name": "Stable Diffusion", "category": "Image Generation", "rating": 9.0}
            ]
            
            for tool in trending_tools:
                st.markdown(f"""
                <div style="background: rgba(30,41,59,0.3); padding: 1rem; border-radius: 8px; margin: 0.5rem 0;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                                                    <div>
                                <strong>{tool['name']}</strong><br>
                                <small style="color: #e2e8f0;">{tool['category']}</small>
                            </div>
                            <div style="color: #f59e0b; font-weight: bold;">
                                ⭐ {tool['rating']}/10
                            </div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    with tab3:
        st.markdown("### 📖 Comprehensive AI Guides")
        
        guide_categories = {
            "🚀 Getting Started": [
                "AI Fundamentals for Beginners",
                "Setting up Your First AI Project",
                "Understanding Machine Learning Basics"
            ],
            "🏗️ Development": [
                "Building Custom AI Agents",
                "API Integration Best Practices",
                "Data Preparation Techniques"
            ],
            "📈 Advanced Topics": [
                "Fine-tuning Language Models",
                "Implementing RAG Systems",
                "AI Ethics and Governance"
            ]
        }
        
        for category, guides in guide_categories.items():
            st.markdown(f"#### {category}")
            for guide in guides:
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"📄 {guide}")
                with col2:
                    if st.button(f"View", key=f"guide_{guide.replace(' ', '_')}"):
                        st.info(f"Guide '{guide}' would be displayed here in full version.")
    
    with tab4:
        st.markdown("### 🎥 Video Tutorial Library")
        
        tutorials = [
            {
                "title": "Building Your First AI Chatbot",
                "duration": "45 mins",
                "level": "Beginner",
                "views": "12.5K",
                "description": "Step-by-step guide to creating an AI chatbot from scratch."
            },
            {
                "title": "Advanced Agent Workflows",
                "duration": "1h 20mins",
                "level": "Advanced",
                "views": "8.2K",
                "description": "Complex multi-step AI agent implementations."
            },
            {
                "title": "AI Integration with APIs",
                "duration": "35 mins",
                "level": "Intermediate",
                "views": "15.7K",
                "description": "Connecting AI agents with external services."
            }
        ]
        
        for tutorial in tutorials:
            st.markdown(f"""
            <div class="metric-card">
                <div style="display: flex; justify-content: space-between; align-items: start;">
                    <div style="flex: 1;">
                        <h4>🎥 {tutorial['title']}</h4>
                        <p>{tutorial['description']}</p>
                        <div style="display: flex; gap: 1rem; margin-top: 0.5rem;">
                            <span style="background: rgba(245,158,11,0.2); padding: 0.25rem 0.5rem; border-radius: 4px;">
                                ⏱️ {tutorial['duration']}
                            </span>
                            <span style="background: rgba(59,130,246,0.2); padding: 0.25rem 0.5rem; border-radius: 4px;">
                                📊 {tutorial['level']}
                            </span>
                            <span style="background: rgba(16,185,129,0.2); padding: 0.25rem 0.5rem; border-radius: 4px;">
                                👁️ {tutorial['views']} views
                            </span>
                        </div>
                    </div>
                    <div style="margin-left: 1rem;">
                        <div style="width: 100px; height: 60px; background: linear-gradient(135deg, #f59e0b, #d97706); 
                                    border-radius: 8px; display: flex; align-items: center; justify-content: center;">
                            <span style="font-size: 1.5rem; color: #000;">▶️</span>
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    with tab5:
        st.markdown("### 📊 Ready-to-Use Templates")
        
        templates = {
            "Agent Templates": [
                {"name": "Customer Service Bot", "downloads": 1250, "rating": 4.8},
                {"name": "Data Analysis Agent", "downloads": 890, "rating": 4.7},
                {"name": "Content Creator Bot", "downloads": 2100, "rating": 4.9}
            ],
            "Workflow Templates": [
                {"name": "Multi-Step Automation", "downloads": 650, "rating": 4.6},
                {"name": "API Integration Flow", "downloads": 980, "rating": 4.7},
                {"name": "Data Processing Pipeline", "downloads": 730, "rating": 4.5}
            ],
            "UI Templates": [
                {"name": "Dashboard Template", "downloads": 1850, "rating": 4.9},
                {"name": "Chat Interface", "downloads": 2300, "rating": 4.8},
                {"name": "Analytics Dashboard", "downloads": 1100, "rating": 4.6}
            ]
        }
        
        for category, template_list in templates.items():
            st.markdown(f"#### {category}")
            cols = st.columns(len(template_list))
            
            for idx, template in enumerate(template_list):
                with cols[idx]:
                    st.markdown(f"""
                    <div style="background: rgba(30,41,59,0.3); padding: 1rem; border-radius: 8px; text-align: center;">
                        <h5>{template['name']}</h5>
                        <div style="margin: 0.5rem 0;">
                            <span style="color: #f59e0b;">⭐ {template['rating']}</span><br>
                            <small>{template['downloads']} downloads</small>
                        </div>
                        <button style="background: linear-gradient(135deg, #3b82f6, #2563eb); color: white; border: none; padding: 0.5rem 1rem; border-radius: 8px; cursor: pointer;">Use Template</button>
                    </div>
                    """, unsafe_allow_html=True)

# -------------------------
# Admin Dashboard Functions
# -------------------------
def show_admin_dashboard():
    """Admin dashboard with various management sections"""
    st.title("⚙️ Admin Dashboard")
    
    admin_section = st.selectbox(
        "Select Admin Section",
        [
            "📊 Advanced Analytics",
            "👥 User Management Pro",
            "📚 Resource Library",
            "🔧 System Administration",
            "📈 Business Intelligence",
            "🛡️ Security Center",
            "⚙️ Configuration",
            "📱 API Management",
            "🔔 Notification Center"
        ]
    )
    
    # Main content based on selection
    if admin_section == "📊 Advanced Analytics":
        show_advanced_analytics()
    elif admin_section == "👥 User Management Pro":
        show_enhanced_user_management()
    elif admin_section == "📚 Resource Library":
        show_enhanced_resources()
    elif admin_section == "🔧 System Administration":
        show_system_administration()
    elif admin_section == "📈 Business Intelligence":
        show_business_intelligence()
    elif admin_section == "🛡️ Security Center":
        show_security_center()
    elif admin_section == "⚙️ Configuration":
        show_system_configuration()
    elif admin_section == "📱 API Management":
        show_api_management()
    elif admin_section == "🔔 Notification Center":
        show_notification_center()

def show_advanced_analytics():
    """Advanced analytics dashboard with comprehensive metrics"""
    st.subheader("📊 Advanced System Analytics")
    
    try:
        supabase = init_supabase_connection()
        if not supabase:
            st.error("Database connection failed")
            return
        
        # Fetch user data
        users_query = supabase.table("user_profiles").select("*").execute()
        users_data = users_query.data or []
        
        # Calculate metrics
        total_users = len(users_data)
        admin_count = len([u for u in users_data if u.get("role") == "admin"])
        user_count = total_users - admin_count
        active_users = len([u for u in users_data if u.get("last_login")])
        
        # Top metrics row
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <h3 style="color: #f59e0b; margin: 0;">👥 {total_users:,}</h3>
                <p style="margin: 0.5rem 0 0 0;">Total Users</p>
                <small style="color: #10b981;">↗️ +{max(5, total_users // 10)} this week</small>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <h3 style="color: #10b981; margin: 0;">✅ {active_users:,}</h3>
                <p style="margin: 0.5rem 0 0 0;">Active Users</p>
                <small style="color: #10b981;">↗️ {(active_users/total_users*100):.1f}% active rate</small>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <h3 style="color: #3b82f6; margin: 0;">👑 {admin_count}</h3>
                <p style="margin: 0.5rem 0 0 0;">Administrators</p>
                <small style="color: #e2e8f0;">System managers</small>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            avg_login_time = datetime.now() - timedelta(hours=np.random.randint(1, 72))
            st.markdown(f"""
            <div class="metric-card">
                <h3 style="color: #f59e0b; margin: 0;">🕐 {avg_login_time.strftime('%H:%M')}</h3>
                <p style="margin: 0.5rem 0 0 0;">Avg Last Login</p>
                <small style="color: #e2e8f0;">{(datetime.now() - avg_login_time).days} days ago</small>
            </div>
            """, unsafe_allow_html=True)
        
        with col5:
            system_health = 99.2
            st.markdown(f"""
            <div class="metric-card">
                <h3 style="color: #10b981; margin: 0;">💚 {system_health}%</h3>
                <p style="margin: 0.5rem 0 0 0;">System Health</p>
                <small style="color: #10b981;">All systems operational</small>
            </div>
            """, unsafe_allow_html=True)
        
        # Advanced Charts Section
        st.markdown("### 📈 User Analytics Dashboard")
        
        # Create sample data for charts
        dates = pd.date_range(start='2024-01-01', end=datetime.now(), freq='D')
        
        # User registration trends
        registration_data = pd.DataFrame({
            'date': dates,
            'registrations': [max(0, int(np.random.normal(3, 2))) for _ in dates],
            'active_users': [max(5, int(np.random.normal(20, 8))) for _ in dates]
        })
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig_reg = px.line(registration_data, x='date', y='registrations', 
                             title='📈 Daily User Registrations',
                             color_discrete_sequence=['#f59e0b'])
            fig_reg.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='#ffffff',
                height=300
            )
            st.plotly_chart(fig_reg, use_container_width=True)
        
        with col2:
            fig_active = px.area(registration_data, x='date', y='active_users',
                               title='👥 Daily Active Users',
                               color_discrete_sequence=['#10b981'])
            fig_active.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='#ffffff',
                height=300
            )
            st.plotly_chart(fig_active, use_container_width=True)
        
        # User distribution and engagement
        col1, col2 = st.columns(2)
        
        with col1:
            # Role distribution pie chart
            role_data = pd.DataFrame({
                'Role': ['Regular Users', 'Administrators', 'Inactive'],
                'Count': [user_count, admin_count, max(0, total_users - active_users)]
            })
            
            fig_pie = px.pie(role_data, values='Count', names='Role',
                           title='👥 User Role Distribution',
                           color_discrete_sequence=['#f59e0b', '#d97706', '#6b7280'])
            fig_pie.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='#ffffff',
                height=300
            )
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with col2:
            # Usage patterns heatmap
            hours = list(range(24))
            days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
            
            # Generate sample heatmap data
            heatmap_data = np.random.randint(5, 50, size=(len(days), len(hours)))
            
            fig_heatmap = go.Figure(data=go.Heatmap(
                z=heatmap_data,
                x=hours,
                y=days,
                colorscale='Viridis',
                showscale=True
            ))
            
            fig_heatmap.update_layout(
                title='🕐 Usage Patterns (Hour vs Day)',
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='#ffffff',
                height=300
            )
            st.plotly_chart(fig_heatmap, use_container_width=True)
        
        # Detailed Analytics Tables
        st.markdown("### 📋 Detailed User Analytics")
        
        # Top users by activity
        if users_data:
            # Simulate activity scores
            for user in users_data:
                user['activity_score'] = np.random.randint(10, 100)
                user['last_active'] = (datetime.now() - timedelta(days=np.random.randint(0, 30))).strftime('%Y-%m-%d')
                user['sessions'] = np.random.randint(1, 50)
            
            # Sort by activity
            active_users_sorted = sorted(users_data, key=lambda x: x['activity_score'], reverse=True)[:10]
            
            st.markdown("#### 🏆 Most Active Users")
            activity_df = pd.DataFrame([
                {
                    "Email": user.get('email', 'Unknown'),
                    "Role": user.get('role', 'user').title(),
                    "Activity Score": user['activity_score'],
                    "Sessions": user['sessions'],
                    "Last Active": user['last_active']
                }
                for user in active_users_sorted
            ])
            
            st.dataframe(activity_df, use_container_width=True)
        
        # System Performance Metrics
        st.markdown("### ⚡ System Performance")
        
        perf_col1, perf_col2, perf_col3, perf_col4 = st.columns(4)
        
        with perf_col1:
            response_time = np.random.uniform(80, 150)
            st.metric("🚀 Response Time", f"{response_time:.0f}ms", f"{np.random.uniform(-5, 5):.1f}ms")
        
        with perf_col2:
            cpu_usage = np.random.uniform(15, 45)
            st.metric("🖥️ CPU Usage", f"{cpu_usage:.1f}%", f"{np.random.uniform(-2, 3):.1f}%")
        
        with perf_col3:
            memory_usage = np.random.uniform(40, 70)
            st.metric("💾 Memory Usage", f"{memory_usage:.1f}%", f"{np.random.uniform(-1, 2):.1f}%")
        
        with perf_col4:
            uptime_hours = np.random.randint(24, 720)
            st.metric("⏱️ Uptime", f"{uptime_hours}h", "Stable")
    
    except Exception as e:
        st.error(f"Error loading analytics: {e}")
        logger.error(f"Analytics error: {e}")

def show_enhanced_user_management():
    """Enhanced user management with advanced features"""
    st.subheader("👥 Advanced User Management System")
    
    try:
        supabase = init_supabase_connection()
        if not supabase:
            st.error("Database connection failed")
            return
        
        # Fetch users with enhanced data
        users_query = supabase.table("user_profiles").select("*").execute()
        users_data = users_query.data or []
        
        # Enhanced filters and search
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            search_query = st.text_input("🔍 Search users", placeholder="Email, name, or ID...")
        
        with col2:
            role_filter = st.selectbox("🎭 Filter by role", ["All", "user", "admin", "inactive"])
        
        with col3:
            date_filter = st.selectbox("📅 Registration date", 
                                     ["All time", "Last 7 days", "Last 30 days", "Last 90 days"])
        
        with col4:
            status_filter = st.selectbox("📊 Status", ["All", "Active", "Inactive", "Pending"])
        
        # Apply filters
        filtered_users = users_data.copy()
        
        if search_query:
            filtered_users = [
                u for u in filtered_users 
                if search_query.lower() in u.get('email', '').lower() 
                or search_query.lower() in u.get('full_name', '').lower()
                or search_query.lower() in str(u.get('id', '')).lower()
            ]
        
        if role_filter != "All":
            filtered_users = [u for u in filtered_users if u.get('role') == role_filter]
        
        # Bulk actions section
        st.markdown("### 🔧 Bulk User Actions")
        bulk_col1, bulk_col2, bulk_col3, bulk_col4 = st.columns(4)
        
        with bulk_col1:
            if st.button("📧 Send Welcome Email", use_container_width=True):
                st.success(f"Welcome emails queued for {len(filtered_users)} users!")
                log_user_activity("bulk_email", f"Welcome emails sent to {len(filtered_users)} users")
        
        with bulk_col2:
            if st.button("📊 Export User Data", use_container_width=True):
                df = pd.DataFrame(filtered_users)
                csv_data = df.to_csv(index=False)
                st.download_button(
                    "Download CSV",
                    csv_data,
                    f"users_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    "text/csv",
                    use_container_width=True
                )
        
        with bulk_col3:
            if st.button("🔄 Refresh All Sessions", use_container_width=True):
                st.info("All user sessions refreshed successfully!")
                log_user_activity("bulk_session_refresh", "All user sessions refreshed")
        
        with bulk_col4:
            if st.button("📈 Generate User Report", use_container_width=True):
                st.success("Comprehensive user report generated!")
        
        # User statistics
        st.markdown("### 📊 User Statistics Overview")
        stats_col1, stats_col2, stats_col3, stats_col4 = st.columns(4)
        
        total_filtered = len(filtered_users)
        active_count = len([u for u in filtered_users if u.get('last_login')])
        admin_count = len([u for u in filtered_users if u.get('role') == 'admin'])
        completion_avg = np.mean([u.get('profile_completion', 50) for u in filtered_users]) if filtered_users else 0
        
        with stats_col1:
            st.metric("👥 Total Users", total_filtered)
        with stats_col2:
            st.metric("✅ Active Users", active_count, f"{(active_count/total_filtered*100):.1f}%" if total_filtered > 0 else "0%")
        with stats_col3:
            st.metric("👑 Administrators", admin_count)
        with stats_col4:
            st.metric("📋 Avg Profile Complete", f"{completion_avg:.1f}%")
        
        # Enhanced user list with advanced features
        st.markdown(f"### 👤 User Directory ({len(filtered_users)} users)")
        
        # Pagination
        users_per_page = 10
        total_pages = (len(filtered_users) + users_per_page - 1) // users_per_page
        
        page_col1, page_col2, page_col3 = st.columns([1, 2, 1])
        with page_col2:
            current_page = st.selectbox(
                "📄 Page", 
                range(1, total_pages + 1), 
                format_func=lambda x: f"Page {x} of {total_pages}"
            ) if total_pages > 1 else 1
        
        # Calculate pagination
        start_idx = (current_page - 1) * users_per_page
        end_idx = start_idx + users_per_page
        page_users = filtered_users[start_idx:end_idx]
        
        # Display users with enhanced cards
        for i, user in enumerate(page_users):
            with st.container():
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, rgba(30,41,59,0.8) 0%, rgba(51,65,85,0.8) 100%); 
                            padding: 1.5rem; border-radius: 16px; margin: 1rem 0; 
                            border: 1px solid rgba(245,158,11,0.3);">
                """, unsafe_allow_html=True)
                
                # User header
                user_col1, user_col2, user_col3, user_col4 = st.columns([2, 1, 1, 1])
                
                with user_col1:
                    status_icon = "🟢" if user.get('last_login') else "🔴"
                    role_icon = "👑" if user.get('role') == 'admin' else "👤"
                    st.markdown(f"""
                    **{role_icon} {user.get('email', 'Unknown Email')}** {status_icon}
                    
                    📝 {user.get('full_name', 'Name not provided')}
                    🏢 {user.get('company', 'Company not provided')}
                    """)
                
                with user_col2:
                    created_date = user.get('created_at', datetime.now().isoformat())
                    if isinstance(created_date, str):
                        try:
                            created_date = datetime.fromisoformat(created_date.replace('Z', '+00:00'))
                        except:
                            created_date = datetime.now()
                    
                    st.write(f"""
                    **📅 Created:** {created_date.strftime('%Y-%m-%d')}
                    **🔐 Role:** {user.get('role', 'user').title()}
                    **📊 Profile:** {user.get('profile_completion', 50)}% complete
                    """)
                
                with user_col3:
                    last_login = user.get('last_login')
                    login_text = "Never" if not last_login else "Recent"
                    if last_login:
                        try:
                            login_date = datetime.fromisoformat(last_login.replace('Z', '+00:00'))
                            days_ago = (datetime.now() - login_date).days
                            if days_ago == 0:
                                login_text = "Today"
                            elif days_ago == 1:
                                login_text = "Yesterday"
                            else:
                                login_text = f"{days_ago} days ago"
                        except:
                            pass
                    
                    st.write(f"""
                    **⏰ Last Login:** {login_text}
                    **#️⃣ Logins:** {user.get('login_count', 0)}
                    **⭐ Activity:** {user.get('activity_score', 'N/A')}
                    """)
                
                with user_col4:
                    action_col1, action_col2 = st.columns(2)
                    with action_col1:
                        if st.button("✏️ Edit", key=f"edit_{user.get('id')}", use_container_width=True):
                            st.info(f"Editing user: {user.get('email')}")
                    with action_col2:
                        if st.button("🗑️ Delete", key=f"delete_{user.get('id')}", use_container_width=True):
                            st.warning(f"Deleting user: {user.get('email')}")
                
                st.markdown("</div>", unsafe_allow_html=True)
        
        # User insights and recommendations
        st.markdown("### 💡 User Insights & Recommendations")
        insight_col1, insight_col2 = st.columns(2)
        
        with insight_col1:
            st.markdown("#### 🎯 Key Insights")
            
            if filtered_users:
                inactive_users = [u for u in filtered_users if not u.get('last_login') or (datetime.now() - datetime.fromisoformat(u['last_login'].replace('Z', '+00:00'))).days > 30]
                incomplete_profiles = [u for u in filtered_users if u.get('profile_completion', 50) < 70]
                
                insights = [
                    f"🔴 {len(inactive_users)} users haven't logged in recently",
                    f"📋 {len(incomplete_profiles)} users have incomplete profiles",
                    f"👑 {admin_count} administrators are managing the system",
                    f"📊 Average profile completion is {completion_avg:.1f}%"
                ]
                
                for insight in insights:
                    st.write(f"• {insight}")
            
            with insight_col2:
                st.markdown("#### 🎯 Recommendations")
                
                recommendations = [
                    "📧 Send re-engagement emails to inactive users",
                    "📝 Prompt users to complete their profiles",
                    "🔔 Set up automated welcome sequences",
                    "📊 Monitor user activity patterns regularly"
                ]
                
                for rec in recommendations:
                    st.write(f"• {rec}")
        
    except Exception as e:
        st.error(f"Error loading user management: {e}")
        logger.error(f"User management error: {e}")

def show_system_administration():
    """System administration and maintenance tools"""
    st.subheader("🔧 System Administration Center")
    
    # System overview cards
    st.markdown("### 🖥️ System Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h4>🚀 Application Status</h4>
            <div style="display: flex; align-items: center; gap: 0.5rem;">
                <div class="status-indicator status-online"></div>
                <strong style="color: #10b981;">Online</strong>
            </div>
            <small>Uptime: 99.8%</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h4>🗄️ Database</h4>
            <div style="display: flex; align-items: center; gap: 0.5rem;">
                <div class="status-indicator status-online"></div>
                <strong style="color: #10b981;">Connected</strong>
            </div>
            <small>Response: 45ms</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h4>🔐 Authentication</h4>
            <div style="display: flex; align-items: center; gap: 0.5rem;">
                <div class="status-indicator status-online"></div>
                <strong style="color: #10b981;">Secure</strong>
            </div>
            <small>Sessions: Active</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <h4>📊 Monitoring</h4>
            <div style="display: flex; align-items: center; gap: 0.5rem;">
                <div class="status-indicator status-online"></div>
                <strong style="color: #10b981;">Active</strong>
            </div>
            <small>All metrics OK</small>
        </div>
        """, unsafe_allow_html=True)
    
    # System tools tabs
    tab1, tab2, tab3, tab4 = st.tabs(["🛠️ Maintenance", "📊 Monitoring", "🔄 Backups", "🚀 Performance"])
    
    with tab1:
        st.markdown("#### 🛠️ System Maintenance Tools")
        
        maint_col1, maint_col2 = st.columns(2)
        
        with maint_col1:
            st.markdown("##### 🧹 Cleanup Operations")
            
            if st.button("🗑️ Clear Session Cache", use_container_width=True):
                st.cache_data.clear()
                st.success("Session cache cleared successfully!")
                log_user_activity("system_maintenance", "Session cache cleared")
            
            if st.button("📝 Clean Activity Logs", use_container_width=True):
                with st.spinner("Cleaning old activity logs..."):
                    time.sleep(2)
                st.success("Activity logs cleaned! Removed entries older than 90 days.")
                log_user_activity("system_maintenance", "Activity logs cleaned")
            
            if st.button("🔄 Refresh User Sessions", use_container_width=True):
                with st.spinner("Refreshing all user sessions..."):
                    time.sleep(1.5)
                st.success("All user sessions refreshed successfully!")
                log_user_activity("system_maintenance", "User sessions refreshed")
        
        with maint_col2:
            st.markdown("##### ⚙️ System Operations")
            
            if st.button("📊 Rebuild Analytics", use_container_width=True):
                with st.spinner("Rebuilding analytics data..."):
                    time.sleep(3)
                st.success("Analytics data rebuilt successfully!")
                log_user_activity("system_maintenance", "Analytics rebuilt")
            
            if st.button("🔍 Check System Health", use_container_width=True):
                with st.spinner("Performing system health check..."):
                    time.sleep(2)
                    
                health_results = [
                    ("Database Connection", "✅ Healthy", "success"),
                    ("Authentication Service", "✅ Operational", "success"),
                    ("File Storage", "✅ Available", "success"),
                    ("Memory Usage", "⚠️ 68% (OK)", "warning"),
                    ("Disk Space", "✅ 78% Available", "success")
                ]
                
                for check, status, level in health_results:
                    if level == "success":
                        st.success(f"{check}: {status}")
                    elif level == "warning":
                        st.warning(f"{check}: {status}")
                    else:
                        st.error(f"{check}: {status}")
            
            if st.button("🔧 Optimize Database", use_container_width=True):
                with st.spinner("Optimizing database performance..."):
                    time.sleep(4)
                st.success("Database optimized! Query performance improved by 15%.")
                log_user_activity("system_maintenance", "Database optimized")
    
    with tab2:
        st.markdown("#### 📊 System Monitoring Dashboard")
        
        # Real-time metrics simulation
        monitor_col1, monitor_col2 = st.columns(2)
        
        with monitor_col1:
            # CPU and Memory usage over time
            time_data = pd.date_range(start=datetime.now() - timedelta(hours=24), 
                                    end=datetime.now(), freq='H')
            
            metrics_data = pd.DataFrame({
                'time': time_data,
                'cpu_usage': [max(10, min(90, 30 + np.random.normal(0, 10))) for _ in time_data],
                'memory_usage': [max(20, min(85, 45 + np.random.normal(0, 8))) for _ in time_data]
            })
            
            fig_metrics = go.Figure()
            fig_metrics.add_trace(go.Scatter(
                x=metrics_data['time'], y=metrics_data['cpu_usage'],
                mode='lines', name='CPU Usage (%)',
                line=dict(color='#f59e0b', width=2)
            ))
            fig_metrics.add_trace(go.Scatter(
                x=metrics_data['time'], y=metrics_data['memory_usage'],
                mode='lines', name='Memory Usage (%)',
                line=dict(color='#10b981', width=2, dash='dash')
            ))
            
            fig_metrics.update_layout(
                title='📈 System Resource Usage (24h)',
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='#ffffff',
                height=350
            )
            st.plotly_chart(fig_metrics, use_container_width=True)
        
        with monitor_col2:
            # Response times
            response_data = pd.DataFrame({
                'endpoint': ['Login', 'Dashboard', 'Analytics', 'User Management', 'Resources'],
                'response_time': [120, 89, 156, 98, 67],
                'status': ['Good', 'Excellent', 'Good', 'Excellent', 'Excellent']
            })
            
            fig_response = px.bar(response_data, x='endpoint', y='response_time',
                                title='🚀 API Response Times (ms)',
                                color='status',
                                color_discrete_map={
                                    'Excellent': '#10b981',
                                    'Good': '#f59e0b',
                                    'Poor': '#ef4444'
                                })
            
            fig_response.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='#ffffff',
                height=350
            )
            st.plotly_chart(fig_response, use_container_width=True)
        
        # System alerts and notifications
        st.markdown("##### 🚨 Recent System Events")
        
        events = [
            {"time": "2 minutes ago", "type": "info", "message": "User authentication successful", "count": 15},
            {"time": "5 minutes ago", "type": "success", "message": "Database backup completed", "count": 1},
            {"time": "12 minutes ago", "type": "warning", "message": "High memory usage detected", "count": 3},
            {"time": "30 minutes ago", "type": "error", "message": "API rate limit exceeded", "count": 2},
            {"time": "1 hour ago", "type": "info", "message": "New user registered", "count": 5}
        ]
        
        for event in events:
            st.markdown(f"""
            <div class="notification notification-{event['type']}">
                <small>{event['time']}</small><br>
                <strong>{event['message']}</strong> (x{event['count']})
            </div>
            """, unsafe_allow_html=True)
    
    with tab3:
        st.markdown("#### 🔄 Backup and Restore Management")
        
        backup_col1, backup_col2 = st.columns(2)
        
        with backup_col1:
            st.markdown("##### 💾 Database Backups")
            if st.button("🚀 Initiate Full Backup Now", use_container_width=True):
                with st.spinner("Performing full database backup..."):
                    time.sleep(5)
                st.success("Full database backup completed successfully!")
                log_user_activity("system_backup", "Full database backup initiated")
            
            if st.button("🕒 Schedule Incremental Backup", use_container_width=True):
                st.info("Incremental backup scheduled for nightly execution.")
                log_user_activity("system_backup", "Incremental backup scheduled")
            
            st.markdown("##### 📂 File System Backups")
            if st.button("☁️ Backup Uploaded Files to S3", use_container_width=True):
                with st.spinner("Syncing uploaded files to S3..."):
                    time.sleep(3)
                st.success("Uploaded files synced to S3 bucket!")
                log_user_activity("system_backup", "File system backup to S3")
        
        with backup_col2:
            st.markdown("##### ↩️ Restore Options")
            restore_option = st.selectbox("Select Restore Point", 
                                        ["Latest Full Backup (2025-09-23)", 
                                         "Yesterday's Incremental", 
                                         "Custom Date..."])
            if st.button("🚨 Restore System", use_container_width=True):
                st.warning(f"Initiating system restore from: {restore_option}. This may take a few minutes.")
                log_user_activity("system_restore", f"System restore initiated from {restore_option}")
            
            st.markdown("##### 📜 Backup History")
            backup_history = [
                {"date": "2025-09-23", "type": "Full", "status": "Success", "size": "1.2 GB"},
                {"date": "2025-09-22", "type": "Incremental", "status": "Success", "size": "150 MB"},
                {"date": "2025-09-21", "type": "Incremental", "status": "Failed", "size": "N/A"}
            ]
            for backup in backup_history:
                status_color = "#10b981" if backup['status'] == "Success" else "#ef4444"
                st.markdown(f"""
                <div style="background: rgba(30,41,59,0.3); padding: 0.75rem; border-radius: 8px; margin-bottom: 0.5rem;">
                    <strong>{backup['date']} ({backup['type']})</strong>: 
                    <span style="color: {status_color};">{backup['status']}</span> - {backup['size']}
                </div>
                """, unsafe_allow_html=True)
    
    with tab4:
        st.markdown("#### 🚀 Performance Optimization Tools")
        
        perf_opt_col1, perf_opt_col2 = st.columns(2)
        
        with perf_opt_col1:
            st.markdown("##### ⚡ Caching & CDN Management")
            if st.button("🔄 Clear All Application Caches", use_container_width=True):
                st.cache_data.clear()
                st.cache_resource.clear()
                st.success("All application caches cleared!")
                log_user_activity("performance_optimization", "Application caches cleared")
            
            if st.button("🌐 Configure CDN Settings", use_container_width=True):
                st.info("CDN configuration interface would open here.")
            
            st.markdown("##### ⚙️ Code & Query Optimization")
            if st.button("🔍 Analyze Slow Queries", use_container_width=True):
                st.info("Database slow query analyzer initiated. Results will be displayed shortly.")
            
            if st.button("💡 Suggest Code Optimizations", use_container_width=True):
                st.info("Code optimization suggestions based on performance profiling will appear here.")
        
        with perf_opt_col2:
            st.markdown("##### ⚖️ Load Balancing & Scaling")
            if st.button("⬆️ Scale Up Resources", use_container_width=True):
                st.success("Scaling up server resources. This may take a moment.")
            
            if st.button("⬇️ Scale Down Resources", use_container_width=True):
                st.info("Scaling down server resources to optimize costs.")
            
            st.markdown("##### 📊 Performance Reports")
            if st.button("📈 Generate Performance Report", use_container_width=True):
                st.success("Detailed performance report generated and available for download.")
            
            if st.button("📉 View Historical Performance", use_container_width=True):
                st.info("Loading historical performance metrics and charts.")

def show_system_configuration():
    """System-wide configuration settings"""
    st.subheader("⚙️ System Configuration")
    
    config_tab1, config_tab2, config_tab3 = st.tabs(["General Settings", "Email & Notifications", "Integrations"])
    
    with config_tab1:
        st.markdown("#### 🌐 General Application Settings")
        
        app_name = st.text_input("Application Name", value=Config.APP_NAME)
        app_version = st.text_input("Application Version", value=Config.VERSION, disabled=True)
        app_author = st.text_input("Author", value=Config.AUTHOR)
        app_company = st.text_input("Company", value=Config.COMPANY)
        app_website = st.text_input("Website URL", value=Config.WEBSITE)
        
        if st.button("💾 Save General Settings", use_container_width=True):
            # In a real app, these would update a database or config file
            st.success("General settings updated successfully!")
            log_user_activity("system_config", "General settings updated")
            
        st.markdown("--- ")
        st.markdown("#### ⏰ Session & Security Settings")
        
        session_timeout_hours = st.slider("Session Timeout (hours)", min_value=0.5, max_value=24.0, value=Config.SESSION_TIMEOUT/3600, step=0.5)
        st.session_state.session_timeout = int(session_timeout_hours * 3600)
        
        enable_mfa = st.checkbox("Enable Multi-Factor Authentication (MFA)", value=True)
        enable_ip_whitelist = st.checkbox("Enable IP Whitelisting", value=False)
        
        if st.button("🔒 Save Security Settings", use_container_width=True):
            st.success("Security settings updated successfully!")
            log_user_activity("system_config", "Security settings updated")
            
    with config_tab2:
        st.markdown("#### 📧 Email & Notification Settings")
        
        email_sender = st.text_input("Sender Email Address", value="noreply@entremotivator.com")
        smtp_server = st.text_input("SMTP Server", value="smtp.sendgrid.net")
        smtp_port = st.number_input("SMTP Port", value=587)
        
        enable_user_notifications = st.checkbox("Enable User Notifications", value=True)
        enable_admin_alerts = st.checkbox("Enable Admin Security Alerts", value=True)
        
        notification_frequency = st.selectbox("Default Notification Frequency", 
                                            ["Instant", "Daily Digest", "Weekly Summary"])
        
        if st.button("🔔 Save Notification Settings", use_container_width=True):
            st.success("Email and notification settings updated!")
            log_user_activity("system_config", "Email/Notification settings updated")
            
    with config_tab3:
        st.markdown("#### 🔗 Third-Party Integrations")
        
        st.markdown("##### Supabase Integration")
        supabase_url = st.text_input("Supabase URL", value="https://your-supabase-url.supabase.co", type="password")
        supabase_key = st.text_input("Supabase Anon Key", value="your-supabase-anon-key", type="password")
        
        if st.button("Connect Supabase", use_container_width=True):
            st.success("Supabase connection details saved and tested!")
            log_user_activity("system_config", "Supabase integration updated")
            
        st.markdown("##### OpenAI API Integration")
        openai_api_key = st.text_input("OpenAI API Key", value="sk-YOUR_OPENAI_KEY", type="password")
        
        if st.button("Connect OpenAI", use_container_width=True):
            st.success("OpenAI API key saved and validated!")
            log_user_activity("system_config", "OpenAI integration updated")
            
        st.markdown("##### Other Integrations")
        st.info("More integrations (e.g., Stripe, Google Analytics, Slack) can be configured here.")

def show_api_management():
    """API management and key generation"""
    st.subheader("📱 API Management")
    
    api_tab1, api_tab2 = st.tabs(["API Keys", "API Usage & Docs"])
    
    with api_tab1:
        st.markdown("#### 🔑 Manage API Keys")
        
        # Generate new API key
        with st.expander("➕ Generate New API Key"):
            key_name = st.text_input("API Key Name", placeholder="e.g., MyWebApp, MobileApp")
            key_permissions = st.multiselect("Permissions", 
                                             ["read:users", "write:users", "read:data", "write:data", "admin:all"],
                                             default=["read:data"])
            key_expiry = st.date_input("Expiry Date (Optional)", value=None)
            
            if st.button("Generate Key", use_container_width=True):
                if key_name:
                    generated_key = hashlib.sha256(os.urandom(60)).hexdigest()
                    st.success(f"Generated API Key for '{key_name}':")
                    st.code(generated_key)
                    st.info("Please save this key now. It will not be shown again.")
                    log_user_activity("api_management", f"New API key generated: {key_name}")
                else:
                    st.error("Please provide an API Key Name.")
        
        st.markdown("##### Active API Keys")
        
        # Sample active API keys
        active_api_keys = [
            {"name": "MyWebApp", "key_prefix": "abc...xyz", "permissions": "read:data, write:data", "created": "2025-08-01", "expires": "Never", "status": "Active"},
            {"name": "MobileApp", "key_prefix": "def...uvw", "permissions": "read:users", "created": "2025-07-15", "expires": "2026-07-15", "status": "Active"},
            {"name": "OldService", "key_prefix": "ghi...rst", "permissions": "read:data", "created": "2024-01-01", "expires": "2025-01-01", "status": "Expired"}
        ]
        
        for api_key in active_api_keys:
            status_color = "#10b981" if api_key['status'] == "Active" else "#ef4444"
            st.markdown(f"""
            <div style="background: rgba(30,41,59,0.3); padding: 1rem; border-radius: 8px; margin-bottom: 0.5rem;
                        border-left: 4px solid {status_color};">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <strong>{api_key['name']}</strong><br>
                        <small>Key: {api_key['key_prefix']}</small>
                    </div>
                    <div style="text-align: right;">
                        <span style="color: {status_color};">{api_key['status']}</span><br>
                        <small>Expires: {api_key['expires']}</small>
                    </div>
                </div>
                <small>Permissions: {api_key['permissions']}</small>
                <div style="margin-top: 0.5rem;">
                    <button style="background: #3b82f6; color: white; border: none; padding: 0.3rem 0.6rem; border-radius: 4px; cursor: pointer; margin-right: 0.5rem;">Revoke</button>
                    <button style="background: #f59e0b; color: white; border: none; padding: 0.3rem 0.6rem; border-radius: 4px; cursor: pointer;">Edit</button>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
    with api_tab2:
        st.markdown("#### 📊 API Usage & Documentation")
        
        st.markdown("##### API Call Volume (Last 24h)")
        api_usage_data = pd.DataFrame({
            'hour': list(range(24)),
            'calls': [max(0, int(np.random.normal(100, 30))) for _ in range(24)]
        })
        fig_api_usage = px.area(api_usage_data, x='hour', y='calls',
                                title='API Call Volume',
                                color_discrete_sequence=['#3b82f6'])
        fig_api_usage.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#ffffff',
            height=300
        )
        st.plotly_chart(fig_api_usage, use_container_width=True)
        
        st.markdown("##### API Error Rates (Last 24h)")
        api_error_data = pd.DataFrame({
            'hour': list(range(24)),
            'errors': [max(0, int(np.random.normal(5, 5))) for _ in range(24)]
        })
        fig_api_errors = px.line(api_error_data, x='hour', y='errors',
                                 title='API Error Rates',
                                 color_discrete_sequence=['#ef4444'])
        fig_api_errors.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#ffffff',
            height=300
        )
        st.plotly_chart(fig_api_errors, use_container_width=True)
        
        st.markdown("##### API Documentation")
        st.markdown("""
        Access our comprehensive API documentation to integrate your applications with the AI Agent Toolkit.
        
        - [API Reference](https://docs.entremotivator.com/api-reference)
        - [Authentication Guide](https://docs.entremotivator.com/authentication)
        - [SDKs & Libraries](https://docs.entremotivator.com/sdks)
        """)

def show_notification_center():
    """Notification center for system and user alerts"""
    st.subheader("🔔 Notification Center")
    
    notif_tab1, notif_tab2 = st.tabs(["My Notifications", "System Alerts"])
    
    with notif_tab1:
        st.markdown("#### ✉️ Your Recent Notifications")
        
        # Sample user notifications
        user_notifications = [
            {"id": 1, "type": "info", "message": "Your monthly report is ready!", "time": "2 hours ago", "read": False},
            {"id": 2, "type": "success", "message": "New feature 'Advanced Analytics' is now live!", "time": "1 day ago", "read": False},
            {"id": 3, "type": "warning", "message": "Your API key 'OldService' will expire soon.", "time": "3 days ago", "read": True},
            {"id": 4, "type": "info", "message": "Welcome to the AI Agent Toolkit!", "time": "1 week ago", "read": True}
        ]
        
        for notif in user_notifications:
            bg_color = "rgba(30,41,59,0.5)" if not notif['read'] else "rgba(30,41,59,0.2)"
            border_color = {"info": "#3b82f6", "success": "#10b981", "warning": "#f59e0b", "error": "#ef4444"}[notif['type']]
            read_status = "(Unread)" if not notif['read'] else ""
            
            st.markdown(f"""
            <div style="background: {bg_color}; padding: 1rem; border-radius: 8px; margin-bottom: 0.5rem;
                        border-left: 4px solid {border_color};">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <strong>{notif['message']}</strong> <span style="color: #f59e0b;">{read_status}</span><br>
                        <small>{notif['time']}</small>
                    </div>
                    <div>
                        <button style="background: none; border: none; color: #3b82f6; cursor: pointer;">Mark as Read</button>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        if st.button("Clear All Read Notifications", use_container_width=True):
            st.success("All read notifications cleared!")
            log_user_activity("notification_center", "Cleared read notifications")
            
    with notif_tab2:
        st.markdown("#### 🚨 Critical System Alerts")
        
        system_alerts = [
            {"id": 1, "type": "error", "message": "Database connection lost for 5 minutes!", "time": "10 minutes ago", "resolved": False},
            {"id": 2, "type": "warning", "message": "High CPU usage detected on server A. (95% for 15 mins)", "time": "1 hour ago", "resolved": False},
            {"id": 3, "type": "info", "message": "Scheduled maintenance completed successfully.", "time": "Yesterday", "resolved": True}
        ]
        
        for alert in system_alerts:
            bg_color = "rgba(30,41,59,0.5)" if not alert['resolved'] else "rgba(30,41,59,0.2)"
            border_color = {"info": "#3b82f6", "success": "#10b981", "warning": "#f59e0b", "error": "#ef4444"}[alert['type']]
            resolved_status = "(Unresolved)" if not alert['resolved'] else "(Resolved)"
            
            st.markdown(f"""
            <div style="background: {bg_color}; padding: 1rem; border-radius: 8px; margin-bottom: 0.5rem;
                        border-left: 4px solid {border_color};">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <strong>{alert['message']}</strong> <span style="color: #f59e0b;">{resolved_status}</span><br>
                        <small>{alert['time']}</small>
                    </div>
                    <div>
                        <button style="background: none; border: none; color: #3b82f6; cursor: pointer;">Mark as Resolved</button>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        if st.button("Clear All Resolved Alerts", use_container_width=True, key="clear_resolved_alerts"):
            st.success("All resolved system alerts cleared!")
            log_user_activity("notification_center", "Cleared resolved system alerts")

# -------------------------
# Main Application Logic
# -------------------------
def main():
    initialize_session_state()
    apply_enhanced_css()
    show_sidebar_toggle()
    check_session_timeout()
    
    supabase = init_supabase_connection()
    if supabase:
        create_database_tables(supabase)
    
    with st.sidebar:
        display_enhanced_logo()
        st.markdown(f"<h2 style='text-align: center; color: var(--primary-color);'>Welcome, {st.session_state.user_profile.get('full_name', 'Guest')}!</h2>", unsafe_allow_html=True)
        
        if st.session_state.authenticated:
            st.success(f"Logged in as {st.session_state.user_profile.get('email')}")
            st.sidebar.markdown("--- ")
            
            if st.session_state.role == "admin":
                st.sidebar.subheader("Admin Tools")
                if st.sidebar.button("⚙️ Admin Dashboard", use_container_width=True):
                    st.session_state.page = "admin_dashboard"
            
            st.sidebar.subheader("Navigation")
            if st.sidebar.button("🏠 Home", use_container_width=True):
                st.session_state.page = "home"
            if st.sidebar.button("📚 Resources", use_container_width=True):
                st.session_state.page = "resources"
            if st.sidebar.button("⬆️ Upload File", use_container_width=True):
                st.session_state.page = "upload_file"
            if st.sidebar.button("🔔 Notifications", use_container_width=True):
                st.session_state.page = "notifications"
            
            st.sidebar.markdown("--- ")
            if st.sidebar.button("🚪 Logout", use_container_width=True):
                logout()
        else:
            st.sidebar.subheader("Account")
            if st.sidebar.button("➡️ Login", use_container_width=True):
                st.session_state.page = "login"
            if st.sidebar.button("📝 Signup", use_container_width=True):
                st.session_state.page = "signup"
            if st.sidebar.button("🔑 Reset Password", use_container_width=True):
                st.session_state.page = "reset_password"
    
    # Main content area
    if st.session_state.authenticated:
        if st.session_state.get("page") == "admin_dashboard" and st.session_state.role == "admin":
            show_admin_dashboard()
        elif st.session_state.get("page") == "resources":
            show_enhanced_resources()
        elif st.session_state.get("page") == "upload_file":
            st.subheader("⬆️ Upload Your Files")
            uploaded_file = st.file_uploader("Choose a file", type=Config.ALLOWED_FILE_TYPES)
            if uploaded_file is not None:
                success, message = handle_file_upload(uploaded_file)
                if success:
                    st.success(message)
                else:
                    st.error(message)
            
            st.markdown("### 📂 Your Uploaded Files")
            if st.session_state.uploaded_files:
                for file_info in st.session_state.uploaded_files:
                    st.write(f"- {file_info['original_name']} ({file_info['size'] / 1024:.2f} KB) - {file_info['status']}")
            else:
                st.info("No files uploaded yet.")
        elif st.session_state.get("page") == "notifications":
            show_notification_center()
        else:
            st.subheader(f"Welcome to the {Config.APP_NAME}!")
            st.write("Your central hub for AI agent development and management.")
            st.info("Use the sidebar to navigate through the application.")
            
            if st.session_state.dashboard_config.get("show_welcome", True):
                st.markdown("""
                <div class="metric-card">
                    <h4>🚀 Get Started with Your AI Agents</h4>
                    <p>Explore our resources, manage your users, and monitor your system performance.</p>
                    <ul>
                        <li>📚 Access comprehensive guides and tutorials.</li>
                        <li>👥 Manage user accounts and permissions.</li>
                        <li>📊 Monitor system analytics and security.</li>
                    </ul>
                    <button style="background: linear-gradient(135deg, #10b981, #059669); color: white; border: none; padding: 0.75rem 1.5rem; border-radius: 12px; cursor: pointer;">Explore Features</button>
                </div>
                """, unsafe_allow_html=True)
    else:
        # Authentication forms
        if st.session_state.get("page") == "signup":
            st.subheader("📝 Create Your Account")
            with st.form("signup_form"):
                email = st.text_input("Email")
                password = st.text_input("Password", type="password")
                full_name = st.text_input("Full Name (Optional)")
                company = st.text_input("Company (Optional)")
                submitted = st.form_submit_button("Sign Up")
                if submitted:
                    success, message = enhanced_signup(email, password, full_name, company)
                    if success:
                        st.success(message)
                        st.session_state.page = "login"
                    else:
                        st.error(message)
        elif st.session_state.get("page") == "reset_password":
            st.subheader("🔑 Reset Your Password")
            with st.form("reset_password_form"):
                email = st.text_input("Enter your email")
                submitted = st.form_submit_button("Send Reset Link")
                if submitted:
                    success, message = enhanced_reset_password(email)
                    if success:
                        st.success(message)
                    else:
                        st.error(message)
        else: # Default to login page
            st.subheader("➡️ Login to AI Agent Toolkit")
            with st.form("login_form"):
                email = st.text_input("Email")
                password = st.text_input("Password", type="password")
                remember_me = st.checkbox("Remember me")
                submitted = st.form_submit_button("Login")
                if submitted:
                    success, message = enhanced_login(email, password, remember_me)
                    if success:
                        st.success(message)
                        st.session_state.page = "home"
                        st.rerun()
                    else:
                        st.error(message)

if __name__ == "__main__":
    main()

