import streamlit as st
import requests
import os
import json
from datetime import datetime
import base64
from typing import Dict, List, Optional
import pandas as pd

# -------------------------
# Enhanced Configuration and Utilities
# -------------------------

class AIToolkitConfig:
    """Configuration class for the AI Agent Toolkit"""
    
    # API endpoints for fetching real-time data
    GITHUB_API_BASE = "https://api.github.com"
    
    # Categories for better organization
    CATEGORIES = {
        "agents": "🤖 AI Agents",
        "llm": "🧠 LLM Projects", 
        "tools": "🛠️ Tools & Frameworks",
        "learning": "📚 Learning Resources",
        "trending": "🔥 Trending",
        "multimodal": "🎨 Multimodal AI",
        "robotics": "🦾 AI Robotics",
        "research": "🔬 Research Tools"
    }
    
    # Enhanced project database
    PROJECTS_DATABASE = {
        "agents": [
            {
                "name": "Microsoft AI Agents for Beginners",
                "repo": "microsoft/ai-agents-for-beginners",
                "description": "12 comprehensive lessons covering AI agent fundamentals with hands-on examples",
                "stars": "2.5k",
                "language": "Python",
                "topics": ["Education", "Beginners", "Tutorial", "Microsoft"],
                "category": "Educational",
                "difficulty": "Beginner",
                "last_updated": "2024-01-15"
            },
            {
                "name": "AutoGPT",
                "repo": "Significant-Gravitas/AutoGPT",
                "description": "An experimental open-source attempt to make GPT-4 fully autonomous",
                "stars": "167k",
                "language": "Python",
                "topics": ["Autonomous", "GPT-4", "Experimental", "Popular"],
                "category": "Autonomous",
                "difficulty": "Advanced",
                "last_updated": "2024-01-20"
            },
            {
                "name": "LangGraph",
                "repo": "langchain-ai/langgraph",
                "description": "Build resilient language agents as graphs for complex multi-step workflows",
                "stars": "5.8k",
                "language": "Python",
                "topics": ["Workflow", "Graphs", "LangChain", "Multi-step"],
                "category": "Framework",
                "difficulty": "Intermediate",
                "last_updated": "2024-01-18"
            },
            {
                "name": "CrewAI",
                "repo": "joaomdmoura/crewAI",
                "description": "Framework for orchestrating role-playing, autonomous AI agents",
                "stars": "19k",
                "language": "Python",
                "topics": ["Multi-agent", "Framework", "Orchestration", "Role-playing"],
                "category": "Framework",
                "difficulty": "Intermediate",
                "last_updated": "2024-01-22"
            },
            {
                "name": "AutoGen",
                "repo": "microsoft/autogen",
                "description": "Multi-agent conversation framework for building AI applications",
                "stars": "31k",
                "language": "Python",
                "topics": ["Multi-agent", "Microsoft", "Conversation", "Framework"],
                "category": "Framework",
                "difficulty": "Intermediate",
                "last_updated": "2024-01-19"
            },
            {
                "name": "AgentGPT",
                "repo": "reworkd/AgentGPT",
                "description": "Assemble, configure, and deploy autonomous AI Agents in your browser",
                "stars": "31k",
                "language": "TypeScript",
                "topics": ["Browser", "Autonomous", "Web-based", "Deploy"],
                "category": "Platform",
                "difficulty": "Beginner",
                "last_updated": "2024-01-17"
            },
            {
                "name": "Semantic Kernel",
                "repo": "microsoft/semantic-kernel",
                "description": "Integrate cutting-edge LLM technology quickly and easily into your apps",
                "stars": "21k",
                "language": "C#",
                "topics": ["Microsoft", "SDK", "Integration", "Enterprise"],
                "category": "SDK",
                "difficulty": "Intermediate",
                "last_updated": "2024-01-21"
            },
            {
                "name": "Haystack",
                "repo": "deepset-ai/haystack",
                "description": "LLM orchestration framework to build customizable, production-ready LLM applications",
                "stars": "16k",
                "language": "Python",
                "topics": ["Orchestration", "Production", "Customizable", "Enterprise"],
                "category": "Framework",
                "difficulty": "Advanced",
                "last_updated": "2024-01-20"
            }
        ],
        "llm": [
            {
                "name": "Ollama",
                "repo": "ollama/ollama",
                "description": "Get up and running with large language models locally with ease",
                "stars": "95k",
                "language": "Go",
                "topics": ["Local AI", "LLM", "Privacy", "Self-hosted"],
                "category": "Runtime",
                "difficulty": "Beginner",
                "last_updated": "2024-01-23"
            },
            {
                "name": "LM Studio",
                "repo": "lmstudio-ai/lmstudio.js",
                "description": "JavaScript SDK for LM Studio - run LLMs locally with a simple API",
                "stars": "1.2k",
                "language": "JavaScript",
                "topics": ["Local", "SDK", "API", "JavaScript"],
                "category": "SDK",
                "difficulty": "Beginner",
                "last_updated": "2024-01-16"
            },
            {
                "name": "Transformers",
                "repo": "huggingface/transformers",
                "description": "State-of-the-art Machine Learning for PyTorch, TensorFlow, and JAX",
                "stars": "133k",
                "language": "Python",
                "topics": ["ML", "Transformers", "Hugging Face", "PyTorch"],
                "category": "Library",
                "difficulty": "Intermediate",
                "last_updated": "2024-01-22"
            },
            {
                "name": "vLLM",
                "repo": "vllm-project/vllm",
                "description": "High-throughput and memory-efficient inference and serving engine for LLMs",
                "stars": "27k",
                "language": "Python",
                "topics": ["Inference", "Performance", "Serving", "Memory-efficient"],
                "category": "Inference",
                "difficulty": "Advanced",
                "last_updated": "2024-01-21"
            },
            {
                "name": "Text Generation WebUI",
                "repo": "oobabooga/text-generation-webui",
                "description": "A Gradio web UI for Large Language Models with many features",
                "stars": "40k",
                "language": "Python",
                "topics": ["WebUI", "Gradio", "Interface", "Features"],
                "category": "Interface",
                "difficulty": "Beginner",
                "last_updated": "2024-01-20"
            }
        ],
        "tools": [
            {
                "name": "LangChain",
                "repo": "langchain-ai/langchain",
                "description": "Framework for developing applications powered by language models",
                "stars": "94k",
                "language": "Python",
                "topics": ["Framework", "LLM", "Applications", "Popular"],
                "category": "Framework",
                "difficulty": "Intermediate",
                "last_updated": "2024-01-23"
            },
            {
                "name": "LlamaIndex",
                "repo": "run-llama/llama_index",
                "description": "LlamaIndex is a data framework for your LLM applications",
                "stars": "35k",
                "language": "Python",
                "topics": ["Data", "Framework", "RAG", "Indexing"],
                "category": "Framework",
                "difficulty": "Intermediate",
                "last_updated": "2024-01-22"
            },
            {
                "name": "Chroma",
                "repo": "chroma-core/chroma",
                "description": "The AI-native open-source embedding database",
                "stars": "14k",
                "language": "Python",
                "topics": ["Vector DB", "Embeddings", "Database", "AI-native"],
                "category": "Database",
                "difficulty": "Intermediate",
                "last_updated": "2024-01-21"
            },
            {
                "name": "Weaviate",
                "repo": "weaviate/weaviate",
                "description": "Weaviate is an open-source vector database that stores both objects and vectors",
                "stars": "11k",
                "language": "Go",
                "topics": ["Vector DB", "Objects", "Search", "GraphQL"],
                "category": "Database",
                "difficulty": "Advanced",
                "last_updated": "2024-01-20"
            },
            {
                "name": "Pinecone Python Client",
                "repo": "pinecone-io/pinecone-python-client",
                "description": "The Pinecone Python client library",
                "stars": "300",
                "language": "Python",
                "topics": ["Vector DB", "Client", "Cloud", "Managed"],
                "category": "Client",
                "difficulty": "Beginner",
                "last_updated": "2024-01-19"
            }
        ],
        "multimodal": [
            {
                "name": "CLIP",
                "repo": "openai/CLIP",
                "description": "Contrastive Language-Image Pretraining",
                "stars": "24k",
                "language": "Python",
                "topics": ["Vision", "Language", "OpenAI", "Multimodal"],
                "category": "Model",
                "difficulty": "Advanced",
                "last_updated": "2024-01-15"
            },
            {
                "name": "LLaVA",
                "repo": "haotian-liu/LLaVA",
                "description": "Large Language and Vision Assistant built towards multimodal GPT-4 level capabilities",
                "stars": "19k",
                "language": "Python",
                "topics": ["Vision", "Language", "Multimodal", "GPT-4"],
                "category": "Model",
                "difficulty": "Advanced",
                "last_updated": "2024-01-18"
            },
            {
                "name": "MiniGPT-4",
                "repo": "Vision-CAIR/MiniGPT-4",
                "description": "Enhancing Vision-language Understanding with Advanced Large Language Models",
                "stars": "25k",
                "language": "Python",
                "topics": ["Vision-Language", "Understanding", "Advanced"],
                "category": "Model",
                "difficulty": "Advanced",
                "last_updated": "2024-01-16"
            }
        ],
        "robotics": [
            {
                "name": "ROS 2",
                "repo": "ros2/ros2",
                "description": "The Robot Operating System 2.0 is a set of software libraries and tools",
                "stars": "1.6k",
                "language": "Python",
                "topics": ["Robotics", "ROS", "Operating System", "Libraries"],
                "category": "Platform",
                "difficulty": "Advanced",
                "last_updated": "2024-01-20"
            },
            {
                "name": "OpenAI Gym",
                "repo": "openai/gym",
                "description": "A toolkit for developing and comparing reinforcement learning algorithms",
                "stars": "34k",
                "language": "Python",
                "topics": ["RL", "Reinforcement Learning", "Algorithms", "Toolkit"],
                "category": "Framework",
                "difficulty": "Intermediate",
                "last_updated": "2024-01-17"
            }
        ],
        "research": [
            {
                "name": "Papers With Code",
                "repo": "paperswithcode/paperswithcode-data",
                "description": "Data from Papers with Code - machine learning papers, code, and evaluation tables",
                "stars": "1.8k",
                "language": "JSON",
                "topics": ["Research", "Papers", "Code", "ML"],
                "category": "Dataset",
                "difficulty": "Beginner",
                "last_updated": "2024-01-19"
            },
            {
                "name": "Awesome AI Papers",
                "repo": "terryum/awesome-deep-learning-papers",
                "description": "The most cited deep learning papers",
                "stars": "25k",
                "language": "Markdown",
                "topics": ["Papers", "Deep Learning", "Citations", "Research"],
                "category": "Collection",
                "difficulty": "Beginner",
                "last_updated": "2024-01-14"
            }
        ]
    }

def hide_streamlit_style():
    """Enhanced function to hide Streamlit default elements"""
    hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            .stDeployButton {display:none;}
            .stDecoration {display:none;}
            div[data-testid="stToolbar"] {visibility: hidden;}
            div[data-testid="stDecoration"] {visibility: hidden;}
            div[data-testid="stStatusWidget"] {visibility: hidden;}
            .css-14xtw13.e8zbici0 {display: none;}
            .css-1rs6os.edgvbvh3 {display: none;}
            .css-vk3wp9.e1akgbir0 {display: none;}
            .css-1j8o68f.edgvbvh9 {display: none;}
            .css-1dp5vir.e8zbici0 {display: none;}
            </style>
            """
    st.markdown(hide_st_style, unsafe_allow_html=True)

def apply_enhanced_theme():
    """Apply enhanced AI Agent Toolkit theme with better styling"""
    st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');
    
    /* Root variables for consistent theming */
    :root {
        --primary-color: #f59e0b;
        --primary-dark: #d97706;
        --secondary-color: #3b82f6;
        --success-color: #10b981;
        --warning-color: #f59e0b;
        --error-color: #ef4444;
        --background-primary: #0f172a;
        --background-secondary: #1e293b;
        --background-tertiary: #334155;
        --text-primary: #ffffff;
        --text-secondary: #cbd5e1;
        --text-muted: #94a3b8;
        --border-color: #475569;
        --border-hover: #64748b;
        --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
        --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
        --radius-sm: 6px;
        --radius-md: 8px;
        --radius-lg: 12px;
        --radius-xl: 16px;
    }
    
    /* Main app styling */
    .stApp {
        background: linear-gradient(135deg, var(--background-primary) 0%, var(--background-secondary) 50%, var(--background-tertiary) 100%);
        color: var(--text-primary);
        font-family: 'Inter', sans-serif;
        line-height: 1.6;
    }
    
    /* Typography improvements */
    .stMarkdown, .stText, p, span, div, .stSelectbox label, .stTextInput label {
        color: var(--text-primary) !important;
        font-family: 'Inter', sans-serif;
    }
    
    h1, h2, h3, h4, h5, h6 {
        color: var(--primary-color) !important;
        font-weight: 700;
        font-family: 'Inter', sans-serif;
        letter-spacing: -0.025em;
        line-height: 1.2;
    }
    
    h1 { font-size: 2.5rem; margin-bottom: 1rem; }
    h2 { font-size: 2rem; margin-bottom: 0.875rem; }
    h3 { font-size: 1.5rem; margin-bottom: 0.75rem; }
    
    /* Enhanced tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: transparent;
        border-bottom: 2px solid var(--border-color);
        padding-bottom: 0;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border: none;
        border-bottom: 3px solid transparent;
        border-radius: 0;
        color: var(--text-secondary);
        padding: 1rem 1.5rem;
        font-weight: 500;
        font-family: 'Inter', sans-serif;
        transition: all 0.3s ease;
        position: relative;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        color: var(--text-primary);
        border-bottom-color: var(--primary-color);
        background: rgba(245, 158, 11, 0.1);
    }
    
    .stTabs [aria-selected="true"] {
        background: rgba(245, 158, 11, 0.15);
        color: var(--primary-color) !important;
        border-bottom-color: var(--primary-color);
        font-weight: 600;
    }
    
    /* Enhanced button styling */
    .stButton > button {
        background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-dark) 100%);
        color: #000000;
        border: none;
        border-radius: var(--radius-lg);
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        font-family: 'Inter', sans-serif;
        transition: all 0.3s ease;
        box-shadow: var(--shadow-md);
        text-transform: none;
        letter-spacing: 0.025em;
        font-size: 0.875rem;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, var(--primary-dark) 0%, #b45309 100%);
        box-shadow: var(--shadow-lg);
        transform: translateY(-1px);
    }
    
    .stButton > button:active {
        transform: translateY(0);
        box-shadow: var(--shadow-sm);
    }
    
    /* Enhanced project card styling */
    .project-card {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.9) 0%, rgba(51, 65, 85, 0.8) 100%);
        border: 1px solid var(--border-color);
        border-radius: var(--radius-xl);
        padding: 2rem;
        margin: 1.5rem 0;
        transition: all 0.4s ease;
        position: relative;
        overflow: hidden;
    }
    
    .project-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    
    .project-card:hover {
        border-color: var(--primary-color);
        box-shadow: 0 8px 32px rgba(245, 158, 11, 0.2);
        transform: translateY(-4px);
    }
    
    .project-card:hover::before {
        opacity: 1;
    }
    
    /* Enhanced badge styling */
    .topic-badge {
        background: linear-gradient(135deg, var(--secondary-color), #1d4ed8);
        color: #dbeafe;
        padding: 6px 12px;
        border-radius: var(--radius-lg);
        font-size: 0.75rem;
        margin: 2px 4px 2px 0;
        display: inline-block;
        font-weight: 500;
        font-family: 'Inter', sans-serif;
        transition: all 0.2s ease;
    }
    
    .topic-badge:hover {
        transform: scale(1.05);
        box-shadow: var(--shadow-sm);
    }
    
    .language-badge {
        background: linear-gradient(135deg, var(--success-color), #047857);
        color: #d1fae5;
        padding: 6px 12px;
        border-radius: var(--radius-lg);
        font-size: 0.75rem;
        font-weight: 500;
        font-family: 'JetBrains Mono', monospace;
    }
    
    .stars-badge {
        background: linear-gradient(135deg, var(--primary-color), var(--primary-dark));
        color: #000000;
        padding: 6px 12px;
        border-radius: var(--radius-lg);
        font-size: 0.75rem;
        font-weight: 600;
        font-family: 'Inter', sans-serif;
    }
    
    .difficulty-badge {
        padding: 4px 10px;
        border-radius: var(--radius-md);
        font-size: 0.7rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    .difficulty-beginner { background: #10b981; color: #000; }
    .difficulty-intermediate { background: #f59e0b; color: #000; }
    .difficulty-advanced { background: #ef4444; color: #fff; }
    
    /* Enhanced metrics and stats */
    .metric-card {
        background: rgba(30, 41, 59, 0.8);
        border: 1px solid var(--border-color);
        border-radius: var(--radius-lg);
        padding: 1.5rem;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        border-color: var(--primary-color);
        box-shadow: var(--shadow-md);
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: var(--primary-color);
        font-family: 'Inter', sans-serif;
    }
    
    .metric-label {
        font-size: 0.875rem;
        color: var(--text-secondary);
        font-weight: 500;
        margin-top: 0.5rem;
    }
    
    /* Search and filter styling */
    .search-container {
        background: rgba(30, 41, 59, 0.8);
        border: 1px solid var(--border-color);
        border-radius: var(--radius-lg);
        padding: 1.5rem;
        margin: 1rem 0;
    }
    
    /* Enhanced sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, var(--background-secondary) 0%, var(--background-tertiary) 100%);
    }
    
    /* Loading and animation improvements */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .project-card {
        animation: fadeInUp 0.6s ease-out;
    }
    
    /* Responsive improvements */
    @media (max-width: 768px) {
        .project-card {
            padding: 1.5rem;
            margin: 1rem 0;
        }
        
        h1 { font-size: 2rem; }
        h2 { font-size: 1.75rem; }
        h3 { font-size: 1.25rem; }
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: var(--background-secondary);
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--border-color);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: var(--border-hover);
    }
    </style>
    """, unsafe_allow_html=True)

def render_enhanced_project_card(project: Dict, show_advanced_info: bool = True):
    """Render an enhanced project card with more information and better styling"""
    
    # Generate download URL
    download_url = f"https://github.com/{project['repo']}/archive/refs/heads/main.zip"
    github_url = f"https://github.com/{project['repo']}"
    
    st.markdown('<div class="project-card">', unsafe_allow_html=True)
    
    # Header row with title and quick actions
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown(f"### 🚀 {project['name']}")
        st.markdown(f"**Repository:** `{project['repo']}`")
        st.markdown(f"**Description:** {project['description']}")
        
        # Enhanced badges row
        badges_col1, badges_col2 = st.columns([2, 1])
        
        with badges_col1:
            # Primary badges
            badges_html = f'<span class="stars-badge">⭐ {project["stars"]}</span> '
            badges_html += f'<span class="language-badge">{project["language"]}</span> '
            
            if show_advanced_info and 'difficulty' in project:
                difficulty_class = f"difficulty-{project['difficulty'].lower()}"
                badges_html += f'<span class="difficulty-badge {difficulty_class}">{project["difficulty"]}</span>'
            
            st.markdown(badges_html, unsafe_allow_html=True)
        
        with badges_col2:
            if show_advanced_info and 'last_updated' in project:
                st.markdown(f"**Updated:** {project['last_updated']}")
        
        # Topics
        if project.get('topics'):
            topics_html = " ".join([f'<span class="topic-badge">{topic}</span>' for topic in project['topics']])
            st.markdown(topics_html, unsafe_allow_html=True)
    
    with col2:
        st.markdown("### Quick Actions")
        
        # Download button
        if st.button(f"📥 Download", key=f"download_{project['repo'].replace('/', '_')}", use_container_width=True):
            st.success(f"✅ Download ready!")
            st.markdown(f"[📦 Download ZIP]({download_url})")
        
        # GitHub button
        if st.button(f"🔗 GitHub", key=f"github_{project['repo'].replace('/', '_')}", use_container_width=True):
            st.markdown(f"[🔗 Open Repository]({github_url})")
        
        # Additional info button
        if show_advanced_info:
            if st.button(f"ℹ️ Details", key=f"info_{project['repo'].replace('/', '_')}", use_container_width=True):
                with st.expander(f"📋 Details for {project['name']}", expanded=True):
                    st.markdown(f"**Category:** {project.get('category', 'N/A')}")
                    st.markdown(f"**Difficulty:** {project.get('difficulty', 'N/A')}")
                    st.markdown(f"**Last Updated:** {project.get('last_updated', 'N/A')}")
                    st.markdown(f"**GitHub Stars:** {project['stars']}")
                    st.markdown(f"**Primary Language:** {project['language']}")
                    
                    if project.get('topics'):
                        st.markdown("**Topics:**")
                        for topic in project['topics']:
                            st.markdown(f"- {topic}")
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_category_stats(projects: List[Dict]):
    """Render statistics for a category of projects"""
    if not projects:
        return
    
    total_projects = len(projects)
    total_stars = sum([int(p['stars'].replace('k', '000').replace('.', '').replace('K', '000')) if 'k' in p['stars'].lower() else int(p['stars'].replace(',', '')) for p in projects if p['stars'].replace('k', '').replace('K', '').replace('.', '').replace(',', '').isdigit()])
    
    languages = {}
    difficulties = {}
    
    for project in projects:
        lang = project.get('language', 'Unknown')
        languages[lang] = languages.get(lang, 0) + 1
        
        diff = project.get('difficulty', 'Unknown')
        difficulties[diff] = difficulties.get(diff, 0) + 1
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{total_projects}</div>
            <div class="metric-label">Projects</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{total_stars:,}</div>
            <div class="metric-label">Total Stars</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        top_language = max(languages.items(), key=lambda x: x[1])[0] if languages else "N/A"
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{top_language}</div>
            <div class="metric-label">Top Language</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        beginner_count = difficulties.get('Beginner', 0)
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{beginner_count}</div>
            <div class="metric-label">Beginner Friendly</div>
        </div>
        """, unsafe_allow_html=True)

def create_search_filters():
    """Create enhanced search and filter interface"""
    st.markdown('<div class="search-container">', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        search_term = st.text_input("🔍 Search projects", placeholder="Enter keywords, language, or topic...")
    
    with col2:
        difficulty_filter = st.selectbox("📊 Difficulty", ["All", "Beginner", "Intermediate", "Advanced"])
    
    with col3:
        language_filter = st.selectbox("💻 Language", ["All", "Python", "JavaScript", "TypeScript", "Go", "C#", "Java"])
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    return search_term, difficulty_filter, language_filter

def filter_projects(projects: List[Dict], search_term: str, difficulty_filter: str, language_filter: str) -> List[Dict]:
    """Filter projects based on search criteria"""
    filtered = projects.copy()
    
    if search_term:
        search_lower = search_term.lower()
        filtered = [p for p in filtered if 
                   search_lower in p['name'].lower() or 
                   search_lower in p['description'].lower() or 
                   any(search_lower in topic.lower() for topic in p.get('topics', []))]
    
    if difficulty_filter != "All":
        filtered = [p for p in filtered if p.get('difficulty') == difficulty_filter]
    
    if language_filter != "All":
        filtered = [p for p in filtered if p.get('language') == language_filter]
    
    return filtered

# Apply styling
hide_streamlit_style()
apply_enhanced_theme()

# Page configuration
st.set_page_config(
    page_title="AI Agent Toolkit - Enhanced Hub", 
    page_icon="🤖", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Authentication check (simplified for demo)
if not st.session_state.get("authenticated", False):
    st.session_state["authenticated"] = True  # Auto-authenticate for demo

# Header
st.markdown("""
<div style="text-align: center; margin: 2rem 0;">
    <h1>🤖 AI Agent Toolkit - Enhanced Hub</h1>
    <p style="font-size: 1.2rem; color: var(--text-secondary); margin-top: 1rem;">
        Discover, explore, and deploy the most comprehensive collection of AI agents, tools, and frameworks
    </p>
</div>
""", unsafe_allow_html=True)

# Navigation menu
menu_cols = st.columns(6)
menu_items = [
    ("🏠 Home", "main_app.py"),
    ("🤖 Agents", None),
    ("🧠 LLM Tools", None), 
    ("🛠️ Frameworks", None),
    ("📚 Learning", None),
    ("🔬 Research", None)
]

for i, (label, page) in enumerate(menu_items):
    with menu_cols[i]:
        if st.button(label, use_container_width=True):
            if page:
                st.switch_page(page)

st.markdown("---")

# Main content with enhanced tabs
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
    "🤖 AI Agents", 
    "🧠 LLM Projects", 
    "🛠️ Tools & Frameworks", 
    "📚 Learning Resources",
    "🔥 Trending",
    "🎨 Multimodal AI",
    "🦾 AI Robotics", 
    "🔬 Research Tools"
])

# AI Agents Tab
with tab1:
    st.header("🤖 AI Agent Repositories")
    st.markdown("*Autonomous agents, multi-agent systems, and intelligent automation tools*")
    
    # Category stats
    render_category_stats(AIToolkitConfig.PROJECTS_DATABASE["agents"])
    
    # Search and filters
    search_term, difficulty_filter, language_filter = create_search_filters()
    
    # Filter and display projects
    filtered_projects = filter_projects(
        AIToolkitConfig.PROJECTS_DATABASE["agents"], 
        search_term, 
        difficulty_filter, 
        language_filter
    )
    
    if filtered_projects:
        for project in filtered_projects:
            render_enhanced_project_card(project)
    else:
        st.info("🔍 No projects match your search criteria. Try adjusting your filters.")

# LLM Projects Tab  
with tab2:
    st.header("🧠 Large Language Model Projects")
    st.markdown("*Local LLM deployment, inference engines, and model serving solutions*")
    
    render_category_stats(AIToolkitConfig.PROJECTS_DATABASE["llm"])
    
    search_term, difficulty_filter, language_filter = create_search_filters()
    filtered_projects = filter_projects(
        AIToolkitConfig.PROJECTS_DATABASE["llm"], 
        search_term, 
        difficulty_filter, 
        language_filter
    )
    
    for project in filtered_projects:
        render_enhanced_project_card(project)

# Tools & Frameworks Tab
with tab3:
    st.header("🛠️ Tools & Frameworks")
    st.markdown("*Development frameworks, vector databases, and AI infrastructure*")
    
    render_category_stats(AIToolkitConfig.PROJECTS_DATABASE["tools"])
    
    search_term, difficulty_filter, language_filter = create_search_filters()
    filtered_projects = filter_projects(
        AIToolkitConfig.PROJECTS_DATABASE["tools"], 
        search_term, 
        difficulty_filter, 
        language_filter
    )
    
    for project in filtered_projects:
        render_enhanced_project_card(project)

# Learning Resources Tab
with tab4:
    st.header("📚 Learning Resources")
    st.markdown("*Educational content, tutorials, and comprehensive learning paths*")
    
    # Add some learning-specific projects
    learning_projects = [
        {
            "name": "Machine Learning Yearning",
            "repo": "ajaymache/machine-learning-yearning",
            "description": "Andrew Ng's Machine Learning Yearning book in markdown format with practical ML advice",
            "stars": "7.6k",
            "language": "Markdown",
            "topics": ["Education", "Andrew Ng", "ML Theory", "Practical"],
            "category": "Book",
            "difficulty": "Beginner",
            "last_updated": "2024-01-10"
        },
        {
            "name": "AI Expert Roadmap",
            "repo": "AMAI-GmbH/AI-Expert-Roadmap", 
            "description": "Comprehensive roadmap to becoming an Artificial Intelligence Expert with learning paths",
            "stars": "29k",
            "language": "Markdown",
            "topics": ["Roadmap", "Career", "AI Expert", "Learning Path"],
            "category": "Guide",
            "difficulty": "Beginner",
            "last_updated": "2024-01-15"
        }
    ]
    
    render_category_stats(learning_projects)
    
    search_term, difficulty_filter, language_filter = create_search_filters()
    filtered_projects = filter_projects(learning_projects, search_term, difficulty_filter, language_filter)
    
    for project in filtered_projects:
        render_enhanced_project_card(project)

# Trending Tab
with tab5:
    st.header("🔥 Trending AI Projects")
    st.markdown("*Hot and rapidly growing AI projects gaining community attention*")
    
    # Trending projects with recent activity
    trending_projects = [
        {
            "name": "ChatGPT Next Web",
            "repo": "ChatGPTNextWeb/ChatGPT-Next-Web",
            "description": "A cross-platform ChatGPT/Gemini UI with PWA support and modern interface",
            "stars": "75k",
            "language": "TypeScript",
            "topics": ["ChatGPT", "UI", "Cross-platform", "PWA"],
            "category": "Interface",
            "difficulty": "Intermediate",
            "last_updated": "2024-01-23"
        },
        {
            "name": "Open WebUI",
            "repo": "open-webui/open-webui",
            "description": "User-friendly WebUI for LLMs with extensive customization options",
            "stars": "42k",
            "language": "Svelte",
            "topics": ["WebUI", "Ollama", "LLM Interface", "Customizable"],
            "category": "Interface",
            "difficulty": "Beginner",
            "last_updated": "2024-01-22"
        }
    ]
    
    render_category_stats(trending_projects)
    
    for project in trending_projects:
        render_enhanced_project_card(project)

# Multimodal AI Tab
with tab6:
    st.header("🎨 Multimodal AI")
    st.markdown("*Vision-language models, image generation, and multimodal understanding*")
    
    render_category_stats(AIToolkitConfig.PROJECTS_DATABASE["multimodal"])
    
    for project in AIToolkitConfig.PROJECTS_DATABASE["multimodal"]:
        render_enhanced_project_card(project)

# AI Robotics Tab
with tab7:
    st.header("🦾 AI Robotics")
    st.markdown("*Robotics frameworks, reinforcement learning, and embodied AI*")
    
    render_category_stats(AIToolkitConfig.PROJECTS_DATABASE["robotics"])
    
    for project in AIToolkitConfig.PROJECTS_DATABASE["robotics"]:
        render_enhanced_project_card(project)

# Research Tools Tab
with tab8:
    st.header("🔬 Research Tools")
    st.markdown("*Academic resources, research datasets, and scientific computing tools*")
    
    render_category_stats(AIToolkitConfig.PROJECTS_DATABASE["research"])
    
    for project in AIToolkitConfig.PROJECTS_DATABASE["research"]:
        render_enhanced_project_card(project)

# Enhanced Sidebar
with st.sidebar:
    st.markdown("### 📊 Platform Statistics")
    
    # Calculate total stats
    total_projects = sum(len(projects) for projects in AIToolkitConfig.PROJECTS_DATABASE.values())
    total_categories = len(AIToolkitConfig.CATEGORIES)
    
    # Display metrics
    st.metric("Total Projects", total_projects)
    st.metric("Categories", total_categories)
    st.metric("Languages", "15+")
    st.metric("Total Stars", "1M+")
    
    st.markdown("---")
    
    st.markdown("### 🎯 Quick Filters")
    
    # Quick filter buttons
    if st.button("🔥 Most Popular", use_container_width=True):
        st.info("Showing projects with 10k+ stars")
    
    if st.button("🚀 Recently Updated", use_container_width=True):
        st.info("Showing projects updated in 2024")
    
    if st.button("👶 Beginner Friendly", use_container_width=True):
        st.info("Showing beginner-level projects")
    
    st.markdown("---")
    
    st.markdown("### 🔗 External Resources")
    
    external_links = [
        ("🚀 Entremotivator.com", "https://entremotivator.com"),
        ("📈 GitHub Trending", "https://github.com/trending"),
        ("📄 Papers With Code", "https://paperswithcode.com/"),
        ("🎯 Awesome Lists", "https://github.com/sindresorhus/awesome"),
        ("🤖 AI Collection", "https://github.com/ai-collection/ai-collection")
    ]
    
    for name, url in external_links:
        st.markdown(f"[{name}]({url})")
    
    st.markdown("---")
    
    st.markdown("### 💡 Pro Tips")
    st.info("""
    **GitHub Best Practices:**
    - ⭐ Star useful repositories
    - 🍴 Fork projects to experiment  
    - 📋 Read documentation thoroughly
    - 🐛 Check issues for known problems
    - 🔄 Watch for updates
    - 🤝 Contribute to open source
    """)
    
    st.markdown("---")
    
    st.markdown("### 🆘 Need Help?")
    if st.button("📧 Contact Support", use_container_width=True):
        st.info("Email: support@entremotivator.com")
    
    if st.button("💬 Join Community", use_container_width=True):
        st.info("Join our Discord community for discussions!")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 2rem 0; color: var(--text-muted);">
    <p><strong>AI Agent Toolkit - Enhanced Hub</strong></p>
    <p>Curated by D Hudson | Powered by Streamlit | Open Source Community</p>
    <p>🌟 Discover • 🚀 Deploy • 🤝 Contribute</p>
</div>
""", unsafe_allow_html=True)

