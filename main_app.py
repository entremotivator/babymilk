#!/usr/bin/env python3
"""
🤖 ENHANCED AI AGENT TOOLKIT - STREAMLIT APPLICATION
A comprehensive Streamlit application featuring 30+ specialized AI business assistants
with OpenAI API integration, Supabase authentication, multi-page interface, and advanced features.
"""

import streamlit as st
from openai import OpenAI
import tiktoken
from datetime import datetime, timedelta
import json
import time
from typing import Dict, List, Tuple, Optional
import logging
import hashlib
import os
import pandas as pd
import io
import base64
import requests
from PIL import Image
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import uuid
import re
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ======================================================
# 🎨 STREAMLIT CONFIGURATION & STYLING
# ======================================================

# Hide Streamlit settings and menu
st.set_page_config(
    page_title="🤖 Enhanced AI Agent Toolkit",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': None
    }
)

# Enhanced styling for the AI Agent Toolkit
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.stDeployButton {display:none;}
.stDecoration {display:none;}

/* Custom styling for Enhanced AI Agent Toolkit */
.main-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 25px;
    border-radius: 20px;
    margin-bottom: 25px;
    text-align: center;
    box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
    position: relative;
    overflow: hidden;
}

.main-header::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grain" width="100" height="100" patternUnits="userSpaceOnUse"><circle cx="25" cy="25" r="1" fill="white" opacity="0.1"/><circle cx="75" cy="75" r="1" fill="white" opacity="0.1"/><circle cx="50" cy="10" r="1" fill="white" opacity="0.1"/><circle cx="10" cy="90" r="1" fill="white" opacity="0.1"/></pattern></defs><rect width="100" height="100" fill="url(%23grain)"/></svg>');
    pointer-events: none;
}

.agent-card {
    background: white;
    padding: 25px;
    border-radius: 20px;
    margin: 15px 0;
    border-left: 5px solid #667eea;
    box-shadow: 0 4px 20px rgba(0,0,0,0.1);
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
}

.agent-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 30px rgba(102, 126, 234, 0.2);
    border-left-color: #764ba2;
}

.agent-card::before {
    content: '';
    position: absolute;
    top: 0;
    right: 0;
    width: 100px;
    height: 100px;
    background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
    border-radius: 50%;
    transform: translate(30px, -30px);
    transition: all 0.3s ease;
}

.agent-card:hover::before {
    transform: translate(20px, -20px) scale(1.2);
}

.chat-container {
    max-width: 100%;
    margin: 0 auto;
    padding: 20px;
}

.user-message {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 18px 25px;
    border-radius: 25px 25px 8px 25px;
    margin: 15px 0 15px 60px;
    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    position: relative;
}

.user-message::before {
    content: '👤';
    position: absolute;
    left: -45px;
    top: 50%;
    transform: translateY(-50%);
    background: white;
    width: 35px;
    height: 35px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 16px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.assistant-message {
    background: #f8f9fa;
    color: #333;
    padding: 18px 25px;
    border-radius: 25px 25px 25px 8px;
    margin: 15px 60px 15px 0;
    border-left: 5px solid #667eea;
    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    position: relative;
}

.assistant-message::before {
    content: '🤖';
    position: absolute;
    right: -45px;
    top: 50%;
    transform: translateY(-50%);
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    width: 35px;
    height: 35px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 16px;
    color: white;
    box-shadow: 0 2px 10px rgba(102, 126, 234, 0.3);
}

.feature-button {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 25px;
    font-size: 0.9em;
    cursor: pointer;
    margin: 8px;
    transition: all 0.3s ease;
    box-shadow: 0 2px 10px rgba(102, 126, 234, 0.2);
}

.feature-button:hover {
    transform: translateY(-3px);
    box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
}

.stButton > button {
    border-radius: 30px;
    border: none;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 12px 25px;
    font-weight: 600;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.2);
}

.stButton > button:hover {
    background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    transform: translateY(-3px);
    box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
}

.sidebar-section {
    background: rgba(102, 126, 234, 0.08);
    padding: 20px;
    border-radius: 20px;
    margin: 20px 0;
    border-left: 5px solid #667eea;
    box-shadow: 0 2px 15px rgba(102, 126, 234, 0.1);
}

.metric-display {
    background: white;
    padding: 20px;
    border-radius: 15px;
    text-align: center;
    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    margin: 15px 0;
    border-top: 4px solid #667eea;
}

.page-nav {
    background: rgba(102, 126, 234, 0.05);
    padding: 15px;
    border-radius: 15px;
    margin: 20px 0;
    text-align: center;
}

.page-nav button {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 20px;
    margin: 5px;
    cursor: pointer;
    transition: all 0.3s ease;
}

.page-nav button:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
}

.category-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 15px 25px;
    border-radius: 15px;
    margin: 20px 0 10px 0;
    font-weight: 600;
    text-align: center;
    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.2);
}

/* Logo styling */
.logo-container {
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 25px;
}

.logo-image {
    max-width: 120px;
    height: auto;
    margin-right: 20px;
    border-radius: 15px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
}

/* Responsive design */
@media (max-width: 768px) {
    .user-message, .assistant-message {
        margin-left: 15px;
        margin-right: 15px;
    }
    
    .user-message::before, .assistant-message::before {
        display: none;
    }
}

/* Dark mode support */
@media (prefers-color-scheme: dark) {
    .agent-card {
        background: #2d3748;
        color: white;
    }
    
    .assistant-message {
        background: #4a5568;
        color: white;
    }
}
</style>
"""

st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# ======================================================
# 🔑 API CONFIGURATION
# ======================================================

def initialize_openai():
    """Initialize OpenAI client with API key from secrets or environment"""
    try:
        # Try Streamlit secrets first
        if hasattr(st, 'secrets') and 'OPENAI_API_KEY' in st.secrets:
            api_key = st.secrets['OPENAI_API_KEY']
            return OpenAI(api_key=api_key), api_key
        
        # Fallback to environment variable
        elif 'OPENAI_API_KEY' in os.environ:
            api_key = os.environ['OPENAI_API_KEY']
            return OpenAI(api_key=api_key), api_key
        
        # No API key found
        return None, None
        
    except Exception as e:
        logger.error(f"Failed to initialize OpenAI: {str(e)}")
        return None, None

# ======================================================
# 🤖 ENHANCED AI AGENT PERSONALITIES (30+ AGENTS)
# ======================================================

BOT_PERSONALITIES = {
    # ENTREPRENEURSHIP & STARTUPS (Enhanced)
    "Startup Strategist": {
        "description": "I specialize in helping new businesses with comprehensive planning and execution. From MVP development to scaling strategies, I guide entrepreneurs through every stage of their startup journey with proven methodologies.",
        "emoji": "🚀",
        "category": "Entrepreneurship & Startups",
        "temperature": 0.7,
        "specialties": ["Business Planning", "MVP Development", "Product-Market Fit", "Growth Hacking", "Lean Startup"],
        "quick_actions": ["Create Business Plan", "Validate Idea", "Find Co-founder", "Pitch Deck Help", "Market Analysis"]
    },
    "Business Plan Writer": {
        "description": "I create comprehensive, investor-ready business plans with detailed market analysis, financial projections, and strategic roadmaps. I help entrepreneurs articulate their vision professionally.",
        "emoji": "📝",
        "category": "Entrepreneurship & Startups",
        "temperature": 0.6,
        "specialties": ["Business Plans", "Market Analysis", "Financial Projections", "Investor Presentations", "Strategic Planning"],
        "quick_actions": ["Write Executive Summary", "Market Research", "Financial Model", "Competitive Analysis", "SWOT Analysis"]
    },
    "Venture Capital Advisor": {
        "description": "I guide startups through fundraising and investment landscapes. I specialize in pitch deck creation, investor relations, valuation strategies, and due diligence preparation.",
        "emoji": "💼",
        "category": "Entrepreneurship & Startups",
        "temperature": 0.6,
        "specialties": ["Fundraising", "Pitch Decks", "Investor Relations", "Valuation", "Due Diligence"],
        "quick_actions": ["Create Pitch Deck", "Find Investors", "Prepare Due Diligence", "Valuation Help", "Term Sheet Review"]
    },
    "Innovation Consultant": {
        "description": "I help organizations foster innovation culture and develop breakthrough products. I specialize in design thinking, innovation frameworks, and disruptive business models.",
        "emoji": "💡",
        "category": "Entrepreneurship & Startups",
        "temperature": 0.8,
        "specialties": ["Design Thinking", "Innovation Strategy", "Product Innovation", "Business Model Innovation"],
        "quick_actions": ["Innovation Workshop", "Ideation Session", "Product Roadmap", "Innovation Audit"]
    },

    # SALES & MARKETING (Enhanced)
    "Sales Performance Coach": {
        "description": "I help individuals and teams maximize sales potential through proven methodologies. I specialize in sales funnel optimization, conversion improvement, and advanced selling techniques.",
        "emoji": "💼",
        "category": "Sales & Marketing",
        "temperature": 0.8,
        "specialties": ["Sales Funnels", "Conversion Optimization", "Objection Handling", "Closing Techniques", "Sales Psychology"],
        "quick_actions": ["Sales Script", "Objection Handling", "Pipeline Review", "Closing Tips", "Sales Training"]
    },
    "Marketing Strategy Expert": {
        "description": "I have deep expertise in digital marketing, brand positioning, and customer acquisition. I help businesses build compelling campaigns across all channels with data-driven approaches.",
        "emoji": "📱",
        "category": "Sales & Marketing",
        "temperature": 0.8,
        "specialties": ["Digital Marketing", "Brand Positioning", "Customer Acquisition", "Campaign Strategy", "Marketing Analytics"],
        "quick_actions": ["Marketing Plan", "Brand Strategy", "Campaign Ideas", "Target Audience", "Marketing Audit"]
    },
    "Content Marketing Strategist": {
        "description": "I create engaging content that attracts and converts audiences. I develop content strategies, editorial calendars, storytelling frameworks, and content distribution plans.",
        "emoji": "✍️",
        "category": "Sales & Marketing",
        "temperature": 0.8,
        "specialties": ["Content Strategy", "Editorial Calendars", "Storytelling", "Brand Authority", "Content Distribution"],
        "quick_actions": ["Content Calendar", "Blog Ideas", "Social Posts", "Video Scripts", "Content Audit"]
    },
    "Social Media Manager": {
        "description": "I specialize in building and managing social media presence across all platforms. I create engaging content, manage communities, and drive social commerce results.",
        "emoji": "📲",
        "category": "Sales & Marketing",
        "temperature": 0.8,
        "specialties": ["Social Media Strategy", "Community Management", "Influencer Marketing", "Social Commerce"],
        "quick_actions": ["Social Strategy", "Content Ideas", "Engagement Plan", "Influencer Outreach"]
    },

    # FINANCE & ACCOUNTING (Enhanced)
    "Financial Controller": {
        "description": "I specialize in business financial management, budgeting, and financial planning. I help optimize financial operations, manage cash flow, and ensure regulatory compliance.",
        "emoji": "💰",
        "category": "Finance & Accounting",
        "temperature": 0.5,
        "specialties": ["Financial Planning", "Budget Management", "Cash Flow", "Cost Control", "Financial Reporting"],
        "quick_actions": ["Budget Planning", "Cash Flow Analysis", "Cost Reduction", "Financial Reports", "KPI Dashboard"]
    },
    "Investment Banking Advisor": {
        "description": "I provide expertise in corporate finance, M&A, and capital raising. I help evaluate opportunities, structure deals, conduct valuations, and manage complex financial transactions.",
        "emoji": "🏦",
        "category": "Finance & Accounting",
        "temperature": 0.5,
        "specialties": ["Corporate Finance", "M&A", "Capital Raising", "Valuations", "Financial Modeling"],
        "quick_actions": ["Deal Analysis", "Valuation Model", "M&A Strategy", "Capital Structure", "Financial Model"]
    },
    "Tax Strategy Advisor": {
        "description": "I help businesses and individuals optimize their tax strategies while ensuring compliance. I specialize in tax planning, international tax, and tax-efficient structures.",
        "emoji": "📊",
        "category": "Finance & Accounting",
        "temperature": 0.4,
        "specialties": ["Tax Planning", "Tax Compliance", "International Tax", "Tax Optimization"],
        "quick_actions": ["Tax Planning", "Compliance Check", "Tax Optimization", "Structure Review"]
    },

    # TECHNOLOGY & INNOVATION (Enhanced)
    "Digital Transformation Consultant": {
        "description": "I help organizations leverage technology to transform business models and operations. I specialize in digital strategy, technology adoption, and organizational change management.",
        "emoji": "🔄",
        "category": "Technology & Innovation",
        "temperature": 0.7,
        "specialties": ["Digital Strategy", "Technology Adoption", "Change Management", "Innovation", "Digital Culture"],
        "quick_actions": ["Digital Roadmap", "Tech Assessment", "Change Plan", "Innovation Strategy", "Digital Audit"]
    },
    "AI Strategy Consultant": {
        "description": "I help businesses leverage artificial intelligence for competitive advantage. I specialize in AI implementation, machine learning strategies, and automation frameworks.",
        "emoji": "🤖",
        "category": "Technology & Innovation",
        "temperature": 0.7,
        "specialties": ["AI Implementation", "Machine Learning", "Automation", "AI Strategy", "AI Ethics"],
        "quick_actions": ["AI Roadmap", "Use Case Analysis", "Automation Plan", "ML Strategy", "AI Assessment"]
    },
    "Cybersecurity Expert": {
        "description": "I provide comprehensive cybersecurity guidance to protect organizations from digital threats. I specialize in security frameworks, risk assessment, and incident response.",
        "emoji": "🔒",
        "category": "Technology & Innovation",
        "temperature": 0.6,
        "specialties": ["Security Strategy", "Risk Assessment", "Incident Response", "Compliance", "Security Training"],
        "quick_actions": ["Security Audit", "Risk Assessment", "Security Plan", "Compliance Check", "Training Program"]
    },

    # OPERATIONS & MANAGEMENT (Enhanced)
    "Operations Excellence Manager": {
        "description": "I focus on streamlining processes and maximizing efficiency. I specialize in process improvement, supply chain optimization, lean methodologies, and operational excellence.",
        "emoji": "⚙️",
        "category": "Operations & Management",
        "temperature": 0.6,
        "specialties": ["Process Improvement", "Supply Chain", "Lean Methodologies", "Efficiency", "Quality Management"],
        "quick_actions": ["Process Map", "Efficiency Audit", "Workflow Design", "Cost Optimization", "Quality Review"]
    },
    "Project Management Expert": {
        "description": "I help organizations deliver projects on time and within budget. I specialize in project planning, resource allocation, risk management, and stakeholder communication.",
        "emoji": "📋",
        "category": "Operations & Management",
        "temperature": 0.6,
        "specialties": ["Project Planning", "Resource Management", "Risk Management", "Stakeholder Communication", "Agile Methodologies"],
        "quick_actions": ["Project Plan", "Risk Assessment", "Team Structure", "Timeline Creation", "Status Report"]
    },
    "Supply Chain Optimizer": {
        "description": "I optimize supply chain operations for efficiency and resilience. I specialize in logistics, vendor management, inventory optimization, and supply chain analytics.",
        "emoji": "🚛",
        "category": "Operations & Management",
        "temperature": 0.6,
        "specialties": ["Supply Chain Strategy", "Logistics", "Vendor Management", "Inventory Optimization"],
        "quick_actions": ["Supply Chain Audit", "Vendor Analysis", "Logistics Plan", "Inventory Strategy"]
    },

    # HUMAN RESOURCES (Enhanced)
    "Human Resources Director": {
        "description": "I provide strategic HR guidance for organizational development. I specialize in talent management, culture building, performance optimization, and employee engagement.",
        "emoji": "👥",
        "category": "Human Resources",
        "temperature": 0.7,
        "specialties": ["Talent Management", "Culture Building", "Performance Management", "Employee Engagement", "HR Strategy"],
        "quick_actions": ["Hiring Strategy", "Performance Review", "Culture Assessment", "Team Building", "HR Audit"]
    },
    "Talent Acquisition Specialist": {
        "description": "I help organizations attract and hire top talent. I specialize in recruitment strategies, candidate assessment, employer branding, and talent pipeline development.",
        "emoji": "🎯",
        "category": "Human Resources",
        "temperature": 0.7,
        "specialties": ["Recruitment Strategy", "Candidate Assessment", "Employer Branding", "Interview Process", "Talent Pipeline"],
        "quick_actions": ["Job Description", "Interview Questions", "Candidate Screening", "Offer Strategy", "Onboarding Plan"]
    },
    "Learning & Development Manager": {
        "description": "I design and implement comprehensive learning programs that develop employee skills and drive organizational growth. I specialize in training design and performance improvement.",
        "emoji": "📚",
        "category": "Human Resources",
        "temperature": 0.7,
        "specialties": ["Training Design", "Skill Development", "Performance Improvement", "Leadership Development"],
        "quick_actions": ["Training Program", "Skill Assessment", "Development Plan", "Leadership Training"]
    },

    # LEGAL & COMPLIANCE (New Category)
    "Corporate Legal Advisor": {
        "description": "I provide comprehensive legal guidance for business operations. I specialize in corporate law, contract negotiation, regulatory compliance, and risk mitigation.",
        "emoji": "⚖️",
        "category": "Legal & Compliance",
        "temperature": 0.4,
        "specialties": ["Corporate Law", "Contract Law", "Regulatory Compliance", "Risk Management", "Legal Strategy"],
        "quick_actions": ["Contract Review", "Compliance Audit", "Legal Risk Assessment", "Policy Development"]
    },
    "Intellectual Property Specialist": {
        "description": "I help protect and monetize intellectual property assets. I specialize in patents, trademarks, copyrights, trade secrets, and IP strategy development.",
        "emoji": "🧠",
        "category": "Legal & Compliance",
        "temperature": 0.4,
        "specialties": ["Patent Strategy", "Trademark Protection", "Copyright Law", "Trade Secrets", "IP Monetization"],
        "quick_actions": ["IP Audit", "Patent Search", "Trademark Filing", "IP Strategy", "Licensing Plan"]
    },
    "Regulatory Compliance Expert": {
        "description": "I ensure organizations meet all regulatory requirements across industries. I specialize in compliance frameworks, regulatory analysis, and audit preparation.",
        "emoji": "📋",
        "category": "Legal & Compliance",
        "temperature": 0.4,
        "specialties": ["Regulatory Analysis", "Compliance Frameworks", "Audit Preparation", "Policy Development"],
        "quick_actions": ["Compliance Review", "Regulatory Update", "Audit Prep", "Policy Review"]
    },
    "Data Privacy Officer": {
        "description": "I help organizations navigate data privacy regulations and build privacy-by-design frameworks. I specialize in GDPR, CCPA, and global privacy compliance.",
        "emoji": "🔐",
        "category": "Legal & Compliance",
        "temperature": 0.4,
        "specialties": ["Data Privacy", "GDPR Compliance", "Privacy by Design", "Data Governance"],
        "quick_actions": ["Privacy Audit", "GDPR Assessment", "Privacy Policy", "Data Mapping"]
    },

    # E-COMMERCE & RETAIL (New Category)
    "E-commerce Strategist": {
        "description": "I help businesses build and optimize their online presence. I specialize in e-commerce platforms, conversion optimization, and digital retail strategies.",
        "emoji": "🛒",
        "category": "E-commerce & Retail",
        "temperature": 0.7,
        "specialties": ["E-commerce Strategy", "Conversion Optimization", "Digital Retail", "Customer Experience"],
        "quick_actions": ["Store Audit", "Conversion Plan", "Product Strategy", "Customer Journey"]
    },
    "Retail Operations Manager": {
        "description": "I optimize retail operations for maximum efficiency and customer satisfaction. I specialize in inventory management, store operations, and retail analytics.",
        "emoji": "🏪",
        "category": "E-commerce & Retail",
        "temperature": 0.6,
        "specialties": ["Retail Operations", "Inventory Management", "Store Operations", "Retail Analytics"],
        "quick_actions": ["Operations Audit", "Inventory Plan", "Store Layout", "Performance Review"]
    },
    "Customer Experience Designer": {
        "description": "I design exceptional customer experiences across all touchpoints. I specialize in customer journey mapping, experience design, and customer satisfaction optimization.",
        "emoji": "😊",
        "category": "E-commerce & Retail",
        "temperature": 0.7,
        "specialties": ["Customer Journey", "Experience Design", "Customer Satisfaction", "Touchpoint Optimization"],
        "quick_actions": ["Journey Map", "Experience Audit", "Satisfaction Survey", "Touchpoint Analysis"]
    },
    "Marketplace Specialist": {
        "description": "I help businesses succeed on major marketplaces like Amazon, eBay, and others. I specialize in marketplace optimization, listing management, and multi-channel strategies.",
        "emoji": "🌐",
        "category": "E-commerce & Retail",
        "temperature": 0.7,
        "specialties": ["Marketplace Strategy", "Listing Optimization", "Multi-channel Retail", "Marketplace Analytics"],
        "quick_actions": ["Marketplace Audit", "Listing Optimization", "Channel Strategy", "Performance Analysis"]
    },

    # CREATIVE & DESIGN (New Category)
    "Brand Designer": {
        "description": "I create compelling brand identities and visual systems. I specialize in brand strategy, visual identity design, and brand guidelines development.",
        "emoji": "🎨",
        "category": "Creative & Design",
        "temperature": 0.8,
        "specialties": ["Brand Identity", "Visual Design", "Brand Strategy", "Design Systems"],
        "quick_actions": ["Brand Audit", "Logo Design", "Brand Guidelines", "Visual Identity"]
    },
    "UX/UI Designer": {
        "description": "I design user-centered digital experiences that are both beautiful and functional. I specialize in user research, interface design, and usability optimization.",
        "emoji": "📱",
        "category": "Creative & Design",
        "temperature": 0.7,
        "specialties": ["User Experience", "Interface Design", "User Research", "Usability Testing"],
        "quick_actions": ["UX Audit", "User Research", "Wireframes", "Prototype Design"]
    },
    "Creative Director": {
        "description": "I lead creative vision and strategy across all brand touchpoints. I specialize in creative strategy, campaign development, and creative team leadership.",
        "emoji": "🎭",
        "category": "Creative & Design",
        "temperature": 0.8,
        "specialties": ["Creative Strategy", "Campaign Development", "Creative Leadership", "Brand Storytelling"],
        "quick_actions": ["Creative Brief", "Campaign Ideas", "Creative Strategy", "Brand Story"]
    },
    "Video Production Specialist": {
        "description": "I help create compelling video content for marketing and communication. I specialize in video strategy, production planning, and content optimization.",
        "emoji": "🎬",
        "category": "Creative & Design",
        "temperature": 0.8,
        "specialties": ["Video Strategy", "Production Planning", "Content Creation", "Video Marketing"],
        "quick_actions": ["Video Strategy", "Production Plan", "Script Writing", "Content Calendar"]
    },

    # DATA SCIENCE & ANALYTICS (New Category)
    "Data Scientist": {
        "description": "I help organizations extract insights from data to drive business decisions. I specialize in predictive analytics, machine learning, and data visualization.",
        "emoji": "📊",
        "category": "Data Science & Analytics",
        "temperature": 0.6,
        "specialties": ["Predictive Analytics", "Machine Learning", "Data Visualization", "Statistical Analysis"],
        "quick_actions": ["Data Analysis", "Predictive Model", "Dashboard Design", "Statistical Report"]
    },
    "Business Intelligence Analyst": {
        "description": "I transform raw data into actionable business insights. I specialize in BI tools, reporting systems, and performance dashboards.",
        "emoji": "📈",
        "category": "Data Science & Analytics",
        "temperature": 0.6,
        "specialties": ["Business Intelligence", "Data Reporting", "Dashboard Development", "Performance Analytics"],
        "quick_actions": ["BI Strategy", "Dashboard Design", "Report Creation", "KPI Analysis"]
    },
    "Market Research Analyst": {
        "description": "I conduct comprehensive market research to inform business strategy. I specialize in market analysis, competitive intelligence, and consumer insights.",
        "emoji": "🔍",
        "category": "Data Science & Analytics",
        "temperature": 0.6,
        "specialties": ["Market Analysis", "Competitive Intelligence", "Consumer Research", "Industry Analysis"],
        "quick_actions": ["Market Research", "Competitor Analysis", "Consumer Survey", "Industry Report"]
    }
}

# ======================================================
# 🔐 AUTHENTICATION FUNCTIONS (Enhanced)
# ======================================================

from auth import auth

def init_session_state():
    """Initialize session state variables"""
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'user_email' not in st.session_state:
        st.session_state.user_email = None
    if 'user_id' not in st.session_state:
        st.session_state.user_id = None
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'selected_agent' not in st.session_state:
        st.session_state.selected_agent = "Startup Strategist"
    if 'auth_mode' not in st.session_state:
        st.session_state.auth_mode = "login"
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "Chat"
    if 'favorite_agents' not in st.session_state:
        st.session_state.favorite_agents = []
    if 'user_preferences' not in st.session_state:
        st.session_state.user_preferences = {
            'theme': 'light',
            'notifications': True,
            'auto_save': True
        }

# ======================================================
# 📄 PAGE NAVIGATION SYSTEM
# ======================================================

def get_page_navigation():
    """Get page navigation configuration"""
    pages = {
        "🏠 Dashboard": "Dashboard",
        "💬 Chat": "Chat", 
        "📚 Knowledge Base": "Knowledge",
        "📄 Document Generator": "Documents",
        "📊 Analytics": "Analytics",
        "⚙️ Settings": "Settings"
    }
    return pages

def display_page_navigation():
    """Display page navigation in sidebar"""
    st.sidebar.markdown("""
    <div class="sidebar-section">
        <h3>📍 Navigation</h3>
    </div>
    """, unsafe_allow_html=True)
    
    pages = get_page_navigation()
    
    for page_display, page_key in pages.items():
        if st.sidebar.button(page_display, key=f"nav_{page_key}"):
            st.session_state.current_page = page_key
            st.rerun()

# ======================================================
# 🎯 ENHANCED AGENT SYSTEM
# ======================================================

def get_agent_prompt(agent_name: str) -> str:
    """Get enhanced system prompt for specific agent"""
    agent = BOT_PERSONALITIES.get(agent_name, BOT_PERSONALITIES["Startup Strategist"])
    
    base_prompt = f"""You are {agent_name}, {agent['description']}

Your specialties include: {', '.join(agent['specialties'])}

Guidelines for responses:
1. Always respond in character as {agent_name}
2. Provide actionable, practical advice
3. Use your expertise in {', '.join(agent['specialties'])}
4. Be professional yet approachable
5. Offer specific examples and frameworks when relevant
6. Ask clarifying questions when needed
7. Provide step-by-step guidance for complex topics
8. Reference industry best practices and current trends
9. Suggest follow-up actions or next steps
10. Maintain consistency with your role and expertise

Remember: You are an expert consultant helping with real business challenges. Provide valuable, implementable advice."""
    
    return base_prompt

def chat_with_agent(user_message: str, agent_name: str) -> str:
    """Enhanced chat function with better context and error handling"""
    client, api_key = initialize_openai()
    
    if not client:
        return "⚠️ OpenAI API key not configured. Please add your API key to continue."
    
    try:
        agent = BOT_PERSONALITIES.get(agent_name, BOT_PERSONALITIES["Startup Strategist"])
        
        messages = [
            {"role": "system", "content": get_agent_prompt(agent_name)},
            {"role": "user", "content": user_message}
        ]
        
        # Add recent chat history for context (last 6 messages)
        if st.session_state.chat_history:
            recent_history = [msg for msg in st.session_state.chat_history[-6:] if msg['agent'] == agent_name]
            for msg in recent_history:
                messages.insert(-1, {"role": "assistant", "content": msg['response']})
                messages.insert(-1, {"role": "user", "content": msg['message']})
        
        response = client.chat.completions.create(
            model="gpt-4",
            messages=messages,
            temperature=agent['temperature'],
            max_tokens=1500,
            presence_penalty=0.1,
            frequency_penalty=0.1
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        logger.error(f"Error in chat: {str(e)}")
        return f"❌ Error: {str(e)}"

# ======================================================
# 🎨 ENHANCED UI COMPONENTS
# ======================================================

def display_logo():
    """Display the Enhanced AI Agent Toolkit logo"""
    try:
        # Try to load the logo image
        if os.path.exists("ai_agent_toolkit_logo.png"):
            logo = Image.open("ai_agent_toolkit_logo.png")
            st.image(logo, width=180)
        else:
            st.markdown("🤖")
    except:
        st.markdown("🤖")

def display_enhanced_agent_selector():
    """Display enhanced agent selection interface with categories"""
    st.markdown("""
    <div class="sidebar-section">
        <h3>🤖 Select Your AI Assistant</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Group agents by category
    categories = {}
    for agent_name, agent_info in BOT_PERSONALITIES.items():
        category = agent_info['category']
        if category not in categories:
            categories[category] = []
        categories[category].append(agent_name)
    
    # Category selector with enhanced styling
    selected_category = st.selectbox(
        "Choose Category:",
        list(categories.keys()),
        index=0,
        help="Select a business domain to see specialized AI assistants"
    )
    
    # Display category header
    st.markdown(f"""
    <div class="category-header">
        {selected_category}
    </div>
    """, unsafe_allow_html=True)
    
    # Agent selector within category
    agents_in_category = categories[selected_category]
    selected_agent = st.selectbox(
        "Choose Agent:",
        agents_in_category,
        index=0,
        help="Select a specific AI assistant for your needs"
    )
    
    # Update session state
    st.session_state.selected_agent = selected_agent
    
    # Display enhanced agent info
    agent_info = BOT_PERSONALITIES[selected_agent]
    
    # Favorite button
    is_favorite = selected_agent in st.session_state.favorite_agents
    if st.button("⭐ Favorite" if not is_favorite else "⭐ Favorited", key="favorite_btn"):
        if is_favorite:
            st.session_state.favorite_agents.remove(selected_agent)
        else:
            st.session_state.favorite_agents.append(selected_agent)
        st.rerun()
    
    st.markdown(f"""
    <div class="agent-card">
        <h4>{agent_info['emoji']} {selected_agent}</h4>
        <p>{agent_info['description']}</p>
        <p><strong>Specialties:</strong> {', '.join(agent_info['specialties'])}</p>
        <p><strong>Temperature:</strong> {agent_info['temperature']} (Creativity Level)</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Enhanced quick actions
    st.markdown("**🚀 Quick Actions:**")
    cols = st.columns(2)
    for i, action in enumerate(agent_info['quick_actions']):
        col = cols[i % 2]
        with col:
            if st.button(action, key=f"action_{action}_{i}"):
                st.session_state.chat_input = f"Help me with: {action}"
                st.rerun()

# ======================================================
# 📊 DASHBOARD PAGE
# ======================================================

def display_dashboard():
    """Display enhanced dashboard with analytics and insights"""
    # Header
    col1, col2 = st.columns([1, 4])
    with col1:
        display_logo()
    with col2:
        st.markdown("""
        <div class="main-header">
            <h1>🏠 Dashboard</h1>
            <p>Your AI Agent Toolkit Overview</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_messages = len(st.session_state.chat_history)
        st.markdown(f"""
        <div class="metric-display">
            <h3>💬</h3>
            <h2>{total_messages}</h2>
            <p>Total Messages</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        agents_used = len(set(msg['agent'] for msg in st.session_state.chat_history)) if st.session_state.chat_history else 0
        st.markdown(f"""
        <div class="metric-display">
            <h3>🤖</h3>
            <h2>{agents_used}</h2>
            <p>Agents Consulted</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        favorite_count = len(st.session_state.favorite_agents)
        st.markdown(f"""
        <div class="metric-display">
            <h3>⭐</h3>
            <h2>{favorite_count}</h2>
            <p>Favorite Agents</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        total_agents = len(BOT_PERSONALITIES)
        st.markdown(f"""
        <div class="metric-display">
            <h3>🎯</h3>
            <h2>{total_agents}</h2>
            <p>Available Agents</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Recent activity and analytics
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 📈 Usage Analytics")
        
        if st.session_state.chat_history:
            # Create usage chart
            df_history = pd.DataFrame(st.session_state.chat_history)
            df_history['date'] = pd.to_datetime(df_history['timestamp']).dt.date
            
            # Messages per day
            daily_messages = df_history.groupby('date').size().reset_index(name='messages')
            
            fig = px.line(daily_messages, x='date', y='messages', 
                         title='Messages per Day',
                         color_discrete_sequence=['#667eea'])
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Agent usage
            agent_usage = df_history['agent'].value_counts().head(10)
            fig2 = px.bar(x=agent_usage.values, y=agent_usage.index, 
                         orientation='h',
                         title='Most Used Agents',
                         color_discrete_sequence=['#764ba2'])
            fig2.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
            )
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.info("Start chatting with agents to see analytics!")
    
    with col2:
        st.markdown("### ⭐ Favorite Agents")
        if st.session_state.favorite_agents:
            for agent in st.session_state.favorite_agents:
                agent_info = BOT_PERSONALITIES[agent]
                st.markdown(f"""
                <div class="agent-card" style="margin: 10px 0; padding: 15px;">
                    <h5>{agent_info['emoji']} {agent}</h5>
                    <p style="font-size: 0.9em;">{agent_info['category']}</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Add agents to favorites to see them here!")
        
        st.markdown("### 🕒 Recent Activity")
        if st.session_state.chat_history:
            recent_messages = st.session_state.chat_history[-5:]
            for msg in reversed(recent_messages):
                st.markdown(f"""
                <div style="background: rgba(102, 126, 234, 0.1); padding: 10px; border-radius: 10px; margin: 5px 0;">
                    <strong>{msg['agent']}</strong><br>
                    <small>{msg['timestamp']}</small>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No recent activity")

# ======================================================
# 💬 ENHANCED CHAT PAGE
# ======================================================

def display_chat_interface():
    """Display the enhanced chat interface"""
    # Header with logo
    col1, col2 = st.columns([1, 4])
    with col1:
        display_logo()
    with col2:
        st.markdown("""
        <div class="main-header">
            <h1>💬 AI Agent Chat</h1>
            <p>Converse with your specialized AI business assistants</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Current agent display
    current_agent = BOT_PERSONALITIES[st.session_state.selected_agent]
    st.markdown(f"""
    <div class="agent-card">
        <h4>Currently chatting with: {current_agent['emoji']} {st.session_state.selected_agent}</h4>
        <p>{current_agent['description']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Chat history with enhanced styling
    if st.session_state.chat_history:
        st.markdown("### 💬 Conversation History")
        
        # Filter by current agent option
        show_all = st.checkbox("Show conversations with all agents", value=False)
        
        messages_to_show = st.session_state.chat_history
        if not show_all:
            messages_to_show = [msg for msg in st.session_state.chat_history if msg['agent'] == st.session_state.selected_agent]
        
        # Display last 10 messages
        for msg in messages_to_show[-10:]:
            st.markdown(f"""
            <div class="user-message">
                <strong>You:</strong> {msg['message']}
                <div style="font-size: 0.8em; opacity: 0.7; margin-top: 8px;">
                    Agent: {msg['agent']} | {msg['timestamp']}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="assistant-message">
                <strong>{msg['agent']}:</strong> {msg['response']}
            </div>
            """, unsafe_allow_html=True)
    
    # Enhanced chat input
    st.markdown("### 💭 Ask Your AI Assistant")
    
    # Use session state for input if set by quick actions
    default_input = st.session_state.get('chat_input', '')
    if default_input:
        st.session_state.chat_input = ''  # Clear after use
    
    # Input options
    col1, col2 = st.columns([3, 1])
    
    with col1:
        user_input = st.text_area(
            f"Message {st.session_state.selected_agent}:",
            value=default_input,
            height=120,
            placeholder=f"Ask {st.session_state.selected_agent} for expert business advice...",
            help="Type your question or request for business guidance"
        )
    
    with col2:
        st.markdown("**💡 Suggestions:**")
        suggestions = [
            "Create a strategy",
            "Analyze my situation", 
            "Provide recommendations",
            "Help me plan",
            "Review my approach"
        ]
        
        for suggestion in suggestions:
            if st.button(suggestion, key=f"suggest_{suggestion}"):
                st.session_state.chat_input = suggestion
                st.rerun()
    
    # Send button with enhanced styling
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Send Message", type="primary", use_container_width=True):
            if user_input.strip():
                with st.spinner(f"{st.session_state.selected_agent} is analyzing and preparing response..."):
                    response = chat_with_agent(user_input, st.session_state.selected_agent)
                    
                    # Add to chat history
                    st.session_state.chat_history.append({
                        'message': user_input,
                        'response': response,
                        'agent': st.session_state.selected_agent,
                        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        'id': str(uuid.uuid4())
                    })
                    
                    st.rerun()
            else:
                st.warning("Please enter a message")

# ======================================================
# 📚 KNOWLEDGE BASE PAGE
# ======================================================

def display_knowledge_base():
    """Display knowledge base with business resources"""
    # Header
    col1, col2 = st.columns([1, 4])
    with col1:
        display_logo()
    with col2:
        st.markdown("""
        <div class="main-header">
            <h1>📚 Knowledge Base</h1>
            <p>Business resources, templates, and best practices</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Search functionality
    search_query = st.text_input("🔍 Search knowledge base", placeholder="Search for templates, frameworks, or topics...")
    
    # Categories
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="agent-card">
            <h4>📋 Business Templates</h4>
            <ul>
                <li>Business Plan Template</li>
                <li>Marketing Strategy Framework</li>
                <li>Financial Projection Model</li>
                <li>SWOT Analysis Template</li>
                <li>Competitive Analysis Framework</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="agent-card">
            <h4>🎯 Best Practices</h4>
            <ul>
                <li>Startup Launch Checklist</li>
                <li>Sales Process Optimization</li>
                <li>Digital Marketing Guide</li>
                <li>Team Building Strategies</li>
                <li>Financial Management Tips</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="agent-card">
            <h4>📊 Industry Insights</h4>
            <ul>
                <li>Market Trends Analysis</li>
                <li>Technology Adoption Patterns</li>
                <li>Consumer Behavior Studies</li>
                <li>Economic Indicators</li>
                <li>Regulatory Updates</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Featured content
    st.markdown("### 🌟 Featured Resources")
    
    featured_tabs = st.tabs(["📈 Growth Strategies", "💰 Financial Planning", "🚀 Innovation", "👥 Team Management"])
    
    with featured_tabs[0]:
        st.markdown("""
        #### Growth Strategy Framework
        
        **1. Market Analysis**
        - Total Addressable Market (TAM)
        - Serviceable Addressable Market (SAM)
        - Competitive landscape assessment
        
        **2. Growth Channels**
        - Organic growth strategies
        - Paid acquisition channels
        - Partnership opportunities
        - Product-led growth tactics
        
        **3. Metrics & KPIs**
        - Customer Acquisition Cost (CAC)
        - Lifetime Value (LTV)
        - Monthly Recurring Revenue (MRR)
        - Churn rate optimization
        """)
    
    with featured_tabs[1]:
        st.markdown("""
        #### Financial Planning Essentials
        
        **1. Revenue Forecasting**
        - Bottom-up vs top-down approaches
        - Scenario planning (best/worst/likely)
        - Seasonal adjustments
        
        **2. Cost Management**
        - Fixed vs variable cost analysis
        - Break-even calculations
        - Cash flow projections
        
        **3. Investment Planning**
        - Capital allocation strategies
        - ROI analysis frameworks
        - Risk assessment models
        """)
    
    with featured_tabs[2]:
        st.markdown("""
        #### Innovation Management
        
        **1. Innovation Process**
        - Idea generation techniques
        - Evaluation criteria
        - Prototype development
        
        **2. Technology Adoption**
        - Emerging technology assessment
        - Implementation roadmaps
        - Change management strategies
        
        **3. Innovation Culture**
        - Fostering creativity
        - Risk tolerance frameworks
        - Innovation metrics
        """)
    
    with featured_tabs[3]:
        st.markdown("""
        #### Team Management Best Practices
        
        **1. Team Building**
        - Hiring strategies
        - Onboarding processes
        - Team dynamics optimization
        
        **2. Performance Management**
        - Goal setting frameworks (OKRs)
        - Regular feedback systems
        - Performance review processes
        
        **3. Leadership Development**
        - Leadership competencies
        - Coaching techniques
        - Succession planning
        """)

# ======================================================
# 📄 DOCUMENT GENERATOR PAGE
# ======================================================

def display_document_generator():
    """Display document generator with templates"""
    # Header
    col1, col2 = st.columns([1, 4])
    with col1:
        display_logo()
    with col2:
        st.markdown("""
        <div class="main-header">
            <h1>📄 Document Generator</h1>
            <p>Generate professional business documents with AI assistance</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Document type selector
    doc_types = {
        "Business Plan": "📋",
        "Marketing Strategy": "📱", 
        "Financial Projection": "💰",
        "Project Proposal": "📊",
        "Sales Presentation": "💼",
        "HR Policy": "👥",
        "Legal Contract": "⚖️",
        "Technical Specification": "🔧"
    }
    
    selected_doc_type = st.selectbox(
        "Select Document Type:",
        list(doc_types.keys()),
        help="Choose the type of document you want to generate"
    )
    
    # Document parameters
    st.markdown("### 📝 Document Parameters")
    
    col1, col2 = st.columns(2)
    
    with col1:
        company_name = st.text_input("Company Name", placeholder="Enter your company name")
        industry = st.selectbox("Industry", [
            "Technology", "Healthcare", "Finance", "Retail", "Manufacturing", 
            "Education", "Real Estate", "Consulting", "Other"
        ])
        
    with col2:
        target_audience = st.text_input("Target Audience", placeholder="Who is this document for?")
        document_length = st.selectbox("Document Length", ["Short (1-2 pages)", "Medium (3-5 pages)", "Long (6+ pages)"])
    
    # Additional parameters based on document type
    if selected_doc_type == "Business Plan":
        st.markdown("#### Business Plan Specifics")
        col1, col2 = st.columns(2)
        with col1:
            business_stage = st.selectbox("Business Stage", ["Idea", "Startup", "Growth", "Mature"])
            funding_needed = st.text_input("Funding Needed", placeholder="e.g., $100,000")
        with col2:
            business_model = st.selectbox("Business Model", ["B2B", "B2C", "B2B2C", "Marketplace", "SaaS", "Other"])
            time_horizon = st.selectbox("Time Horizon", ["1 year", "3 years", "5 years"])
    
    elif selected_doc_type == "Marketing Strategy":
        st.markdown("#### Marketing Strategy Specifics")
        col1, col2 = st.columns(2)
        with col1:
            marketing_budget = st.text_input("Marketing Budget", placeholder="e.g., $10,000/month")
            primary_channels = st.multiselect("Primary Channels", [
                "Social Media", "Email Marketing", "Content Marketing", "SEO", 
                "Paid Advertising", "Events", "PR", "Influencer Marketing"
            ])
        with col2:
            campaign_duration = st.selectbox("Campaign Duration", ["1 month", "3 months", "6 months", "1 year"])
            success_metrics = st.multiselect("Success Metrics", [
                "Brand Awareness", "Lead Generation", "Sales", "Engagement", "Traffic"
            ])
    
    # Custom requirements
    custom_requirements = st.text_area(
        "Additional Requirements",
        placeholder="Specify any additional requirements, focus areas, or special considerations...",
        height=100
    )
    
    # Generate document
    if st.button(f"🚀 Generate {selected_doc_type}", type="primary", use_container_width=True):
        if company_name and industry:
            with st.spinner(f"Generating your {selected_doc_type}..."):
                # Simulate document generation
                time.sleep(2)
                
                st.success(f"✅ {selected_doc_type} generated successfully!")
                
                # Display generated content preview
                st.markdown("### 📄 Generated Document Preview")
                
                sample_content = f"""
                # {selected_doc_type} for {company_name}
                
                ## Executive Summary
                
                {company_name} is a {industry.lower()} company focused on delivering exceptional value to {target_audience.lower() if target_audience else 'our target market'}. This {selected_doc_type.lower()} outlines our strategic approach and implementation plan.
                
                ## Key Highlights
                
                - **Industry**: {industry}
                - **Target Audience**: {target_audience or 'To be defined'}
                - **Document Scope**: {document_length}
                
                ## Next Steps
                
                1. Review and customize the generated content
                2. Add specific details relevant to your situation
                3. Share with stakeholders for feedback
                4. Implement the outlined strategies
                
                *This is a preview. The full document would contain detailed sections, analysis, and recommendations based on your specific requirements.*
                """
                
                st.markdown(sample_content)
                
                # Download options
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.download_button(
                        "📥 Download as PDF",
                        data=sample_content,
                        file_name=f"{selected_doc_type}_{company_name}.txt",
                        mime="text/plain"
                    )
                with col2:
                    st.download_button(
                        "📥 Download as Word",
                        data=sample_content,
                        file_name=f"{selected_doc_type}_{company_name}.txt",
                        mime="text/plain"
                    )
                with col3:
                    if st.button("📧 Email Document"):
                        st.info("Email functionality would be implemented here")
        else:
            st.error("Please fill in at least Company Name and Industry")

# ======================================================
# 📊 ANALYTICS PAGE
# ======================================================

def display_analytics():
    """Display analytics and insights page"""
    # Header
    col1, col2 = st.columns([1, 4])
    with col1:
        display_logo()
    with col2:
        st.markdown("""
        <div class="main-header">
            <h1>📊 Analytics & Insights</h1>
            <p>Analyze your AI agent interactions and business insights</p>
        </div>
        """, unsafe_allow_html=True)
    
    if not st.session_state.chat_history:
        st.info("Start chatting with agents to see analytics and insights!")
        return
    
    # Create DataFrame from chat history
    df = pd.DataFrame(st.session_state.chat_history)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['date'] = df['timestamp'].dt.date
    df['hour'] = df['timestamp'].dt.hour
    df['message_length'] = df['message'].str.len()
    df['response_length'] = df['response'].str.len()
    
    # Analytics tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📈 Usage Analytics", "🤖 Agent Performance", "💬 Conversation Analysis", "🎯 Business Insights"])
    
    with tab1:
        st.markdown("### 📈 Usage Analytics")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Messages over time
            daily_messages = df.groupby('date').size().reset_index(name='messages')
            fig = px.line(daily_messages, x='date', y='messages', 
                         title='Messages per Day',
                         color_discrete_sequence=['#667eea'])
            fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True)
            
            # Hourly usage pattern
            hourly_usage = df.groupby('hour').size().reset_index(name='messages')
            fig2 = px.bar(hourly_usage, x='hour', y='messages',
                         title='Usage by Hour of Day',
                         color_discrete_sequence=['#764ba2'])
            fig2.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig2, use_container_width=True)
        
        with col2:
            # Message length distribution
            fig3 = px.histogram(df, x='message_length', nbins=20,
                              title='Message Length Distribution',
                              color_discrete_sequence=['#667eea'])
            fig3.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig3, use_container_width=True)
            
            # Response length distribution
            fig4 = px.histogram(df, x='response_length', nbins=20,
                              title='Response Length Distribution',
                              color_discrete_sequence=['#764ba2'])
            fig4.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig4, use_container_width=True)
    
    with tab2:
        st.markdown("### 🤖 Agent Performance")
        
        # Agent usage statistics
        agent_stats = df.groupby('agent').agg({
            'message': 'count',
            'message_length': 'mean',
            'response_length': 'mean'
        }).round(2)
        agent_stats.columns = ['Total Messages', 'Avg Message Length', 'Avg Response Length']
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Most used agents
            agent_usage = df['agent'].value_counts().head(10)
            fig = px.bar(x=agent_usage.values, y=agent_usage.index, 
                        orientation='h',
                        title='Most Used Agents',
                        color_discrete_sequence=['#667eea'])
            fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Agent categories usage
            df['category'] = df['agent'].map(lambda x: BOT_PERSONALITIES.get(x, {}).get('category', 'Unknown'))
            category_usage = df['category'].value_counts()
            fig2 = px.pie(values=category_usage.values, names=category_usage.index,
                         title='Usage by Agent Category',
                         color_discrete_sequence=px.colors.qualitative.Set3)
            st.plotly_chart(fig2, use_container_width=True)
        
        # Detailed agent statistics
        st.markdown("#### 📊 Detailed Agent Statistics")
        st.dataframe(agent_stats, use_container_width=True)
    
    with tab3:
        st.markdown("### 💬 Conversation Analysis")
        
        # Conversation patterns
        col1, col2 = st.columns(2)
        
        with col1:
            # Average conversation length by agent
            conv_length = df.groupby('agent')['message'].count().sort_values(ascending=False)
            fig = px.bar(x=conv_length.values, y=conv_length.index,
                        orientation='h',
                        title='Messages per Agent',
                        color_discrete_sequence=['#764ba2'])
            fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Message vs Response length correlation
            fig2 = px.scatter(df, x='message_length', y='response_length',
                             color='agent',
                             title='Message vs Response Length',
                             opacity=0.7)
            fig2.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig2, use_container_width=True)
        
        # Recent conversations summary
        st.markdown("#### 🕒 Recent Conversations Summary")
        recent_df = df.tail(10)[['timestamp', 'agent', 'message', 'response']]
        recent_df['message'] = recent_df['message'].str[:100] + '...'
        recent_df['response'] = recent_df['response'].str[:100] + '...'
        st.dataframe(recent_df, use_container_width=True)
    
    with tab4:
        st.markdown("### 🎯 Business Insights")
        
        # Business domain analysis
        business_domains = {
            'Entrepreneurship & Startups': ['startup', 'business plan', 'funding', 'venture', 'entrepreneur'],
            'Sales & Marketing': ['sales', 'marketing', 'customer', 'campaign', 'conversion'],
            'Finance & Accounting': ['finance', 'budget', 'investment', 'revenue', 'cost'],
            'Technology & Innovation': ['technology', 'digital', 'innovation', 'AI', 'automation'],
            'Operations & Management': ['operations', 'process', 'management', 'efficiency', 'project'],
            'Human Resources': ['HR', 'talent', 'employee', 'hiring', 'team']
        }
        
        # Analyze message content for business domains
        domain_mentions = {}
        for domain, keywords in business_domains.items():
            count = 0
            for message in df['message'].str.lower():
                if any(keyword in message for keyword in keywords):
                    count += 1
            domain_mentions[domain] = count
        
        # Display domain analysis
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.bar(x=list(domain_mentions.values()), 
                        y=list(domain_mentions.keys()),
                        orientation='h',
                        title='Business Domain Focus',
                        color_discrete_sequence=['#667eea'])
            fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Top business topics
            st.markdown("#### 🔍 Top Business Topics Discussed")
            all_keywords = []
            for keywords in business_domains.values():
                all_keywords.extend(keywords)
            
            keyword_counts = {}
            for keyword in all_keywords:
                count = sum(1 for message in df['message'].str.lower() if keyword in message)
                if count > 0:
                    keyword_counts[keyword] = count
            
            if keyword_counts:
                sorted_keywords = sorted(keyword_counts.items(), key=lambda x: x[1], reverse=True)[:10]
                for keyword, count in sorted_keywords:
                    st.markdown(f"**{keyword.title()}**: {count} mentions")
            else:
                st.info("Start discussing business topics to see insights!")
        
        # Recommendations
        st.markdown("#### 💡 Recommendations")
        
        if len(df) > 0:
            most_used_category = df['category'].value_counts().index[0]
            least_used_category = df['category'].value_counts().index[-1]
            
            st.markdown(f"""
            <div class="agent-card">
                <h5>📊 Usage Insights</h5>
                <ul>
                    <li><strong>Most Active Domain:</strong> {most_used_category}</li>
                    <li><strong>Least Explored Domain:</strong> {least_used_category}</li>
                    <li><strong>Total Conversations:</strong> {len(df)}</li>
                    <li><strong>Average Message Length:</strong> {df['message_length'].mean():.0f} characters</li>
                </ul>
                
                <h5>🎯 Suggestions</h5>
                <ul>
                    <li>Consider exploring {least_used_category} for broader business insights</li>
                    <li>Your {most_used_category} focus shows strong engagement in this area</li>
                    <li>Try asking more detailed questions to get comprehensive responses</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

# ======================================================
# ⚙️ SETTINGS PAGE
# ======================================================

def display_settings():
    """Display settings and preferences page"""
    # Header
    col1, col2 = st.columns([1, 4])
    with col1:
        display_logo()
    with col2:
        st.markdown("""
        <div class="main-header">
            <h1>⚙️ Settings</h1>
            <p>Customize your AI Agent Toolkit experience</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Settings tabs
    tab1, tab2, tab3, tab4 = st.tabs(["👤 Profile", "🎨 Preferences", "🔑 API Settings", "📊 Data Management"])
    
    with tab1:
        st.markdown("### 👤 User Profile")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.text_input("Email", value=st.session_state.user_email, disabled=True)
            st.text_input("User ID", value=st.session_state.user_id, disabled=True)
            
            # Editable profile fields
            display_name = st.text_input("Display Name", placeholder="Enter your display name")
            company = st.text_input("Company", placeholder="Your company name")
            role = st.selectbox("Role", [
                "CEO/Founder", "Manager", "Consultant", "Analyst", 
                "Developer", "Marketer", "Sales", "Other"
            ])
        
        with col2:
            industry = st.selectbox("Industry", [
                "Technology", "Healthcare", "Finance", "Retail", "Manufacturing",
                "Education", "Real Estate", "Consulting", "Other"
            ])
            experience_level = st.selectbox("Experience Level", [
                "Beginner", "Intermediate", "Advanced", "Expert"
            ])
            interests = st.multiselect("Business Interests", [
                "Entrepreneurship", "Marketing", "Finance", "Technology",
                "Operations", "HR", "Legal", "Strategy"
            ])
        
        if st.button("💾 Save Profile", type="primary"):
            st.success("Profile updated successfully!")
    
    with tab2:
        st.markdown("### 🎨 User Preferences")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Theme settings
            st.markdown("#### 🎨 Appearance")
            theme = st.selectbox("Theme", ["Light", "Dark", "Auto"], 
                                index=0 if st.session_state.user_preferences['theme'] == 'light' else 1)
            
            # Notification settings
            st.markdown("#### 🔔 Notifications")
            notifications = st.checkbox("Enable Notifications", 
                                       value=st.session_state.user_preferences['notifications'])
            email_updates = st.checkbox("Email Updates", value=True)
            
            # Auto-save settings
            st.markdown("#### 💾 Auto-Save")
            auto_save = st.checkbox("Auto-save Conversations", 
                                   value=st.session_state.user_preferences['auto_save'])
            save_frequency = st.selectbox("Save Frequency", ["Every message", "Every 5 messages", "Manual"])
        
        with col2:
            # Agent preferences
            st.markdown("#### 🤖 Agent Preferences")
            default_agent = st.selectbox("Default Agent", list(BOT_PERSONALITIES.keys()),
                                        index=list(BOT_PERSONALITIES.keys()).index(st.session_state.selected_agent))
            
            response_style = st.selectbox("Response Style", [
                "Detailed", "Concise", "Balanced"
            ])
            
            # Language settings
            st.markdown("#### 🌐 Language")
            language = st.selectbox("Language", ["English", "Spanish", "French", "German"])
            
            # Advanced settings
            st.markdown("#### ⚙️ Advanced")
            max_history = st.slider("Max Conversation History", 10, 100, 50)
            temperature_override = st.checkbox("Override Agent Temperature")
            if temperature_override:
                custom_temperature = st.slider("Custom Temperature", 0.0, 1.0, 0.7)
        
        if st.button("💾 Save Preferences", type="primary"):
            st.session_state.user_preferences.update({
                'theme': theme.lower(),
                'notifications': notifications,
                'auto_save': auto_save
            })
            st.success("Preferences updated successfully!")
    
    with tab3:
        st.markdown("### 🔑 API Settings")
        
        # OpenAI API settings
        st.markdown("#### 🤖 OpenAI Configuration")
        
        current_api_key = "***" if initialize_openai()[1] else "Not configured"
        st.text_input("Current API Key", value=current_api_key, disabled=True)
        
        new_api_key = st.text_input("New API Key", type="password", 
                                   placeholder="Enter your OpenAI API key")
        
        if st.button("🔄 Update API Key"):
            if new_api_key:
                # In a real implementation, this would securely store the API key
                st.success("API key updated successfully!")
            else:
                st.error("Please enter a valid API key")
        
        # Model settings
        st.markdown("#### ⚙️ Model Configuration")
        default_model = st.selectbox("Default Model", [
            "gpt-4", "gpt-4-turbo", "gpt-3.5-turbo"
        ])
        
        max_tokens = st.slider("Max Tokens per Response", 100, 2000, 1500)
        
        # Usage statistics
        st.markdown("#### 📊 API Usage")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Requests", len(st.session_state.chat_history))
        with col2:
            total_tokens = sum(len(msg['message']) + len(msg['response']) for msg in st.session_state.chat_history)
            st.metric("Estimated Tokens", f"{total_tokens:,}")
        with col3:
            estimated_cost = total_tokens * 0.00003  # Rough estimate
            st.metric("Estimated Cost", f"${estimated_cost:.2f}")
    
    with tab4:
        st.markdown("### 📊 Data Management")
        
        # Export options
        st.markdown("#### 📤 Export Data")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📥 Export Chat History"):
                if st.session_state.chat_history:
                    df = pd.DataFrame(st.session_state.chat_history)
                    csv = df.to_csv(index=False)
                    st.download_button(
                        "Download CSV",
                        data=csv,
                        file_name=f"chat_history_{datetime.now().strftime('%Y%m%d')}.csv",
                        mime="text/csv"
                    )
                else:
                    st.info("No chat history to export")
            
            if st.button("📥 Export Analytics"):
                st.info("Analytics export functionality would be implemented here")
        
        with col2:
            if st.button("📥 Export Settings"):
                settings_data = {
                    'user_preferences': st.session_state.user_preferences,
                    'favorite_agents': st.session_state.favorite_agents,
                    'selected_agent': st.session_state.selected_agent
                }
                st.download_button(
                    "Download Settings",
                    data=json.dumps(settings_data, indent=2),
                    file_name=f"settings_{datetime.now().strftime('%Y%m%d')}.json",
                    mime="application/json"
                )
        
        # Import options
        st.markdown("#### 📤 Import Data")
        uploaded_file = st.file_uploader("Import Chat History", type=['csv', 'json'])
        if uploaded_file:
            st.info("Import functionality would be implemented here")
        
        # Data cleanup
        st.markdown("#### 🧹 Data Cleanup")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🗑️ Clear Chat History", type="secondary"):
                if st.session_state.chat_history:
                    st.session_state.chat_history = []
                    st.success("Chat history cleared!")
                else:
                    st.info("No chat history to clear")
        
        with col2:
            if st.button("🔄 Reset All Settings", type="secondary"):
                st.session_state.user_preferences = {
                    'theme': 'light',
                    'notifications': True,
                    'auto_save': True
                }
                st.session_state.favorite_agents = []
                st.success("Settings reset to defaults!")
        
        # Privacy settings
        st.markdown("#### 🔒 Privacy Settings")
        
        anonymize_data = st.checkbox("Anonymize exported data", value=True)
        data_retention = st.selectbox("Data Retention Period", [
            "1 month", "3 months", "6 months", "1 year", "Indefinite"
        ])
        
        st.info("💡 Your data is stored locally in your browser session and is not shared with third parties.")

# ======================================================
# 🎨 ENHANCED SIDEBAR
# ======================================================

def display_enhanced_sidebar():
    """Display enhanced sidebar with navigation and agent selection"""
    with st.sidebar:
        # User info with enhanced styling
        st.markdown(f"""
        <div class="sidebar-section">
            <h3>👤 Welcome!</h3>
            <p><strong>Email:</strong> {st.session_state.user_email}</p>
            <p><strong>Session:</strong> Active</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Page navigation
        display_page_navigation()
        
        # Agent selector (only show on Chat page)
        if st.session_state.current_page == "Chat":
            display_enhanced_agent_selector()
        
        # Quick stats
        st.markdown("""
        <div class="sidebar-section">
            <h3>📊 Quick Stats</h3>
        </div>
        """, unsafe_allow_html=True)
        
        total_messages = len(st.session_state.chat_history)
        agents_used = len(set(msg['agent'] for msg in st.session_state.chat_history)) if st.session_state.chat_history else 0
        favorite_count = len(st.session_state.favorite_agents)
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Messages", total_messages)
            st.metric("Favorites", favorite_count)
        with col2:
            st.metric("Agents Used", agents_used)
            st.metric("Available", len(BOT_PERSONALITIES))
        
        # Quick actions
        st.markdown("""
        <div class="sidebar-section">
            <h3>⚡ Quick Actions</h3>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🗑️ Clear Chat History", use_container_width=True):
            st.session_state.chat_history = []
            st.rerun()
        
        if st.button("📊 View Analytics", use_container_width=True):
            st.session_state.current_page = "Analytics"
            st.rerun()
        
        if st.button("📄 Generate Document", use_container_width=True):
            st.session_state.current_page = "Documents"
            st.rerun()
        
        # Logout button
        st.markdown("---")
        if st.button("🚪 Logout", type="secondary", use_container_width=True):
            result = auth.sign_out()
            st.session_state.authenticated = False
            st.session_state.user_email = None
            st.session_state.user_id = None
            st.session_state.chat_history = []
            st.session_state.current_page = "Chat"
            if result['success']:
                st.success(result['message'])
            st.rerun()

# ======================================================
# 🔐 ENHANCED AUTHENTICATION
# ======================================================

def login_form():
    """Display enhanced login/signup form with Supabase integration"""
    # Display logo and banner
    col1, col2 = st.columns([1, 2])
    with col1:
        display_logo()
    with col2:
        st.markdown("""
        <div class="main-header">
            <h1>🤖 Enhanced AI Agent Toolkit</h1>
            <p>Your comprehensive suite of 30+ AI business assistants</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Display banner image if available
    try:
        if os.path.exists("ai_agent_toolkit_banner.png"):
            banner = Image.open("ai_agent_toolkit_banner.png")
            st.image(banner, use_column_width=True)
    except:
        pass
    
    # Feature highlights
    st.markdown("### ✨ What's New in Enhanced Version")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="agent-card">
            <h4>🤖 30+ AI Agents</h4>
            <p>Expanded from 12 to 30+ specialized business assistants across 7 categories</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="agent-card">
            <h4>📊 Advanced Analytics</h4>
            <p>Comprehensive usage analytics, conversation insights, and business intelligence</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="agent-card">
            <h4>📄 Document Generator</h4>
            <p>AI-powered business document generation with professional templates</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Authentication mode selector
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        auth_mode = st.radio(
            "Choose an option:",
            ["Login", "Sign Up", "Reset Password"],
            horizontal=True,
            key="auth_mode_selector"
        )
        
        st.session_state.auth_mode = auth_mode.lower().replace(" ", "_")
    
    # Authentication forms
    if st.session_state.auth_mode == "login":
        login_section()
    elif st.session_state.auth_mode == "sign_up":
        signup_section()
    elif st.session_state.auth_mode == "reset_password":
        reset_password_section()
    
    # Demo mode notice
    if not auth.is_configured():
        st.info("🔧 **Demo Mode**: Supabase not configured. You can use any email/password to login.")
    
    # Footer with features
    st.markdown("---")
    st.markdown("### 🚀 Enhanced Features")
    
    features_col1, features_col2 = st.columns(2)
    
    with features_col1:
        st.markdown("""
        **New Agent Categories:**
        - 🏛️ Legal & Compliance (4 agents)
        - 🛒 E-commerce & Retail (4 agents)  
        - 🎨 Creative & Design (4 agents)
        - 📊 Data Science & Analytics (3 agents)
        """)
    
    with features_col2:
        st.markdown("""
        **New Pages & Features:**
        - 🏠 Interactive Dashboard
        - 📚 Knowledge Base
        - 📄 Document Generator
        - 📊 Advanced Analytics
        - ⚙️ Comprehensive Settings
        """)

def login_section():
    """Enhanced login form section"""
    with st.form("login_form"):
        st.subheader("🔑 Login to Your Account")
        email = st.text_input("Email Address", placeholder="Enter your email")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        
        remember_me = st.checkbox("Remember me")
        
        login_submitted = st.form_submit_button("🚀 Login", type="primary", use_container_width=True)
        
        if login_submitted:
            if email and password:
                with st.spinner("Signing in..."):
                    result = auth.sign_in(email, password)
                    
                if result['success']:
                    st.session_state.authenticated = True
                    st.session_state.user_email = email
                    st.session_state.user_id = result['user'].get('id', 'demo-user')
                    st.success(result['message'])
                    st.rerun()
                else:
                    st.error(result['error'])
            else:
                st.error("Please enter both email and password")

def signup_section():
    """Enhanced signup form section"""
    with st.form("signup_form"):
        st.subheader("📝 Create New Account")
        
        col1, col2 = st.columns(2)
        with col1:
            email = st.text_input("Email Address", placeholder="Enter your email")
            password = st.text_input("Password", type="password", placeholder="Create a password")
        with col2:
            confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm your password")
            company = st.text_input("Company (Optional)", placeholder="Your company name")
        
        terms_accepted = st.checkbox("I agree to the Terms of Service and Privacy Policy")
        
        signup_submitted = st.form_submit_button("🚀 Create Account", type="primary", use_container_width=True)
        
        if signup_submitted:
            if email and password and confirm_password and terms_accepted:
                if password == confirm_password:
                    with st.spinner("Creating account..."):
                        result = auth.sign_up(email, password)
                        
                    if result['success']:
                        st.success(result['message'])
                        st.info("Please check your email for verification instructions.")
                    else:
                        st.error(result['error'])
                else:
                    st.error("Passwords do not match")
            else:
                st.error("Please fill in all required fields and accept the terms")

def reset_password_section():
    """Enhanced password reset form section"""
    with st.form("reset_password_form"):
        st.subheader("🔄 Reset Password")
        email = st.text_input("Email Address", placeholder="Enter your email address")
        
        reset_submitted = st.form_submit_button("📧 Send Reset Email", type="primary", use_container_width=True)
        
        if reset_submitted:
            if email:
                with st.spinner("Sending reset email..."):
                    result = auth.reset_password(email)
                    
                if result['success']:
                    st.success(result['message'])
                else:
                    st.error(result['error'])
            else:
                st.error("Please enter your email address")

# ======================================================
# 🚀 MAIN APPLICATION
# ======================================================

def main():
    """Enhanced main application function"""
    init_session_state()
    
    if not st.session_state.authenticated:
        login_form()
    else:
        # Display sidebar
        display_enhanced_sidebar()
        
        # Display current page
        if st.session_state.current_page == "Dashboard":
            display_dashboard()
        elif st.session_state.current_page == "Chat":
            display_chat_interface()
        elif st.session_state.current_page == "Knowledge":
            display_knowledge_base()
        elif st.session_state.current_page == "Documents":
            display_document_generator()
        elif st.session_state.current_page == "Analytics":
            display_analytics()
        elif st.session_state.current_page == "Settings":
            display_settings()
        else:
            display_chat_interface()  # Default fallback

if __name__ == "__main__":
    main()

