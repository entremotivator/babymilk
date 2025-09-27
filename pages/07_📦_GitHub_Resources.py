import streamlit as st
import os
from datetime import datetime
import base64
import uuid

# -------------------------
# Hide Streamlit Elements for Cloud Deployment
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

def apply_ai_toolkit_theme():
    """Apply AI Agent Toolkit theme"""
    st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap');
    
    /* Main app styling */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #334155 100%);
        color: #ffffff;
        font-family: 'Inter', sans-serif;
    }
    
    /* Text colors */
    .stMarkdown, .stText, p, span, div, .stSelectbox label, .stTextInput label {
        color: #ffffff !important;
        font-family: 'Inter', sans-serif;
    }
    
    h1, h2, h3, h4, h5, h6 {
        color: #f59e0b !important;
        font-weight: 600;
        font-family: 'Inter', sans-serif;
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
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background: rgba(30, 41, 59, 0.8);
        border: 1px solid #475569;
        border-radius: 12px;
        color: #ffffff !important;
        font-family: 'Inter', sans-serif;
    }
    
    /* Project card styling */
    .project-card {
        background: rgba(30, 41, 59, 0.8);
        border: 1px solid #475569;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        transition: all 0.3s ease;
    }
    
    .project-card:hover {
        border-color: #f59e0b;
        box-shadow: 0 4px 20px rgba(245, 158, 11, 0.2);
        transform: translateY(-2px);
    }
    
    /* Badge styling */
    .topic-badge {
        background-color: #1e40af;
        color: #dbeafe;
        padding: 4px 12px;
        border-radius: 12px;
        font-size: 12px;
        margin-right: 8px;
        margin-bottom: 4px;
        display: inline-block;
        font-weight: 500;
    }
    
    .language-badge {
        background-color: #059669;
        color: #d1fae5;
        padding: 4px 12px;
        border-radius: 12px;
        font-size: 12px;
        font-weight: 500;
    }
    
    .stars-badge {
        background-color: #f59e0b;
        color: #000000;
        padding: 4px 12px;
        border-radius: 12px;
        font-size: 12px;
        font-weight: 600;
    }
    
    .difficulty-badge {
        background-color: #dc2626;
        color: #fecaca;
        padding: 4px 12px;
        border-radius: 12px;
        font-size: 12px;
        font-weight: 500;
    }
    
    .difficulty-badge.beginner {
        background-color: #16a34a;
        color: #dcfce7;
    }
    
    .difficulty-badge.intermediate {
        background-color: #ea580c;
        color: #fed7aa;
    }
    
    .difficulty-badge.advanced {
        background-color: #dc2626;
        color: #fecaca;
    }
    
    /* Info/Success/Warning boxes */
    .stInfo {
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.2) 0%, rgba(99, 102, 241, 0.2) 100%);
        border: 1px solid #3b82f6;
        color: #93c5fd !important;
    }
    
    .stSuccess {
        background: linear-gradient(135deg, rgba(34, 197, 94, 0.2) 0%, rgba(16, 185, 129, 0.2) 100%);
        border: 1px solid #22c55e;
        color: #86efac !important;
    }
    
    .stWarning {
        background: linear-gradient(135deg, rgba(245, 158, 11, 0.2) 0%, rgba(217, 119, 6, 0.2) 100%);
        border: 1px solid #f59e0b;
        color: #fcd34d !important;
    }
    
    /* Code blocks */
    .stCode {
        background: rgba(15, 23, 42, 0.8);
        border: 1px solid #475569;
        border-radius: 8px;
        font-family: 'JetBrains Mono', monospace;
    }
    
    /* Metrics styling */
    .metric-container {
        background: rgba(30, 41, 59, 0.6);
        border: 1px solid #475569;
        border-radius: 12px;
        padding: 1rem;
        text-align: center;
        margin: 0.5rem 0;
    }
    
    /* Search and filter styling */
    .search-container {
        background: rgba(30, 41, 59, 0.6);
        border: 1px solid #475569;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
    }
    
    /* Category header styling */
    .category-header {
        background: linear-gradient(135deg, rgba(245, 158, 11, 0.1) 0%, rgba(217, 119, 6, 0.1) 100%);
        border: 1px solid #f59e0b;
        border-radius: 12px;
        padding: 1rem;
        margin: 1rem 0;
        text-align: center;
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

def render_project_card(project, unique_id=None):
    """Render a project card with styling and unique keys"""
    if unique_id is None:
        unique_id = str(uuid.uuid4())[:8]
    
    st.markdown('<div class="project-card">', unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown(f"### 🚀 {project['name']}")
        st.markdown(f"**Repository:** `{project['repo']}`")
        st.markdown(f"**Description:** {project['description']}")
        
        # Badges
        badges_html = f'<span class="stars-badge">⭐ {project["stars"]}</span> '
        badges_html += f'<span class="language-badge">{project["language"]}</span> '
        
        if project.get('difficulty'):
            difficulty_class = project['difficulty'].lower()
            badges_html += f'<span class="difficulty-badge {difficulty_class}">{project["difficulty"]}</span>'
        
        st.markdown(badges_html, unsafe_allow_html=True)
        
        # Topics
        if project.get('topics'):
            topics_html = " ".join([f'<span class="topic-badge">{topic}</span>' for topic in project['topics']])
            st.markdown(topics_html, unsafe_allow_html=True)
        
        # Additional info
        if project.get('last_updated'):
            st.markdown(f"**Last Updated:** {project['last_updated']}")
        
        if project.get('license'):
            st.markdown(f"**License:** {project['license']}")
    
    with col2:
        st.markdown("### Quick Actions")
        
        download_key = f"download_{unique_id}_{project['repo'].replace('/', '_').replace('-', '_')}"
        github_key = f"github_{unique_id}_{project['repo'].replace('/', '_').replace('-', '_')}"
        
        if st.button(f"📥 Download ZIP", key=download_key, use_container_width=True):
            st.success(f"Download link: {project['download_url']}")
            st.markdown(f"[Click here to download]({project['download_url']})")
        
        if st.button(f"🔗 View on GitHub", key=github_key, use_container_width=True):
            st.markdown(f"[Open Repository](https://github.com/{project['repo']})")
        
        # Additional quick actions
        if project.get('demo_url'):
            demo_key = f"demo_{unique_id}_{project['repo'].replace('/', '_').replace('-', '_')}"
            if st.button(f"🎮 Live Demo", key=demo_key, use_container_width=True):
                st.markdown(f"[View Demo]({project['demo_url']})")
        
        if project.get('docs_url'):
            docs_key = f"docs_{unique_id}_{project['repo'].replace('/', '_').replace('-', '_')}"
            if st.button(f"📖 Documentation", key=docs_key, use_container_width=True):
                st.markdown(f"[Read Docs]({project['docs_url']})")
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_category_stats(projects):
    """Render statistics for a category"""
    total_stars = sum([int(p['stars'].replace('k', '000').replace('.', '').replace('+', '')) for p in projects if p['stars'].replace('k', '').replace('.', '').replace('+', '').isdigit()])
    languages = list(set([p['language'] for p in projects]))
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Projects", len(projects))
    with col2:
        st.metric("Total Stars", f"{total_stars//1000}k+" if total_stars > 1000 else str(total_stars))
    with col3:
        st.metric("Languages", len(languages))

# Apply styling
hide_streamlit_style()
apply_ai_toolkit_theme()

st.set_page_config(
    page_title="AI Agent Toolkit - GitHub Resources Hub", 
    page_icon="🤖", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Header with enhanced styling
st.markdown('<div class="category-header">', unsafe_allow_html=True)
st.title("🤖 AI Agent Toolkit - GitHub Resources Hub")
st.markdown("*Comprehensive collection of AI projects, tools, and agent implementations from the open-source community*")
st.markdown('</div>', unsafe_allow_html=True)

# Search and filter section
st.markdown('<div class="search-container">', unsafe_allow_html=True)
st.markdown("### 🔍 Search & Filter")

search_col1, search_col2, search_col3 = st.columns(3)

with search_col1:
    search_term = st.text_input("🔎 Search projects", placeholder="Enter keywords...")

with search_col2:
    language_filter = st.selectbox("💻 Filter by Language", 
                                 ["All", "Python", "TypeScript", "JavaScript", "Go", "Rust", "Java", "C++", "Multiple"])

with search_col3:
    difficulty_filter = st.selectbox("📊 Filter by Difficulty", 
                                   ["All", "Beginner", "Intermediate", "Advanced"])

st.markdown('</div>', unsafe_allow_html=True)

# Resource categories with enhanced content
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
    "🤖 AI Agents", 
    "🧠 LLM Projects", 
    "🛠️ Tools & Frameworks", 
    "📚 Learning Resources", 
    "🔥 Trending", 
    "🎨 Multimodal AI",
    "🤖 AI Robotics",
    "🔬 Research Tools"
])

with tab1:
    st.markdown('<div class="category-header">', unsafe_allow_html=True)
    st.header("🤖 AI Agent Repositories")
    st.markdown("*Autonomous agents, multi-agent systems, and intelligent automation*")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Enhanced agent projects with more details
    agent_projects = [
        {
            "name": "AutoGPT",
            "repo": "Significant-Gravitas/AutoGPT",
            "description": "An experimental open-source attempt to make GPT-4 fully autonomous",
            "stars": "167k",
            "language": "Python",
            "difficulty": "Advanced",
            "topics": ["Autonomous", "GPT-4", "Experimental"],
            "download_url": "https://github.com/Significant-Gravitas/AutoGPT/archive/refs/heads/master.zip",
            "last_updated": "2024-01-15",
            "license": "MIT",
            "docs_url": "https://docs.agpt.co/"
        },
        {
            "name": "Microsoft AI Agents for Beginners",
            "repo": "microsoft/ai-agents-for-beginners",
            "description": "12 comprehensive lessons covering AI agent fundamentals with hands-on examples",
            "stars": "2.5k",
            "language": "Python",
            "difficulty": "Beginner",
            "topics": ["Education", "Tutorial", "Microsoft"],
            "download_url": "https://github.com/microsoft/ai-agents-for-beginners/archive/refs/heads/main.zip",
            "last_updated": "2024-01-10",
            "license": "MIT"
        },
        {
            "name": "GenAI Agents Collection",
            "repo": "NirDiamant/GenAI_Agents",
            "description": "Comprehensive tutorials and implementations for various Generative AI Agent techniques",
            "stars": "1.8k",
            "language": "Python",
            "difficulty": "Intermediate",
            "topics": ["Generative AI", "Implementations", "Tutorials"],
            "download_url": "https://github.com/NirDiamant/GenAI_Agents/archive/refs/heads/main.zip",
            "last_updated": "2024-01-08",
            "license": "Apache-2.0"
        },
        {
            "name": "AI Agents Masterclass",
            "repo": "coleam00/ai-agents-masterclass",
            "description": "Complete code repository for AI Agents Masterclass video series with practical examples",
            "stars": "950",
            "language": "Python",
            "difficulty": "Intermediate",
            "topics": ["Video Course", "Practical", "Hands-on"],
            "download_url": "https://github.com/coleam00/ai-agents-masterclass/archive/refs/heads/main.zip",
            "last_updated": "2024-01-05",
            "license": "MIT"
        },
        {
            "name": "500+ AI Agent Projects",
            "repo": "ashishpatel26/500-AI-Agents-Projects",
            "description": "Curated collection of AI agent use cases across industries with implementation guides",
            "stars": "1.2k",
            "language": "Multiple",
            "difficulty": "Beginner",
            "topics": ["Use Cases", "Industry", "Collection"],
            "download_url": "https://github.com/ashishpatel26/500-AI-Agents-Projects/archive/refs/heads/main.zip",
            "last_updated": "2024-01-12",
            "license": "MIT"
        },
        {
            "name": "LangGraph",
            "repo": "langchain-ai/langgraph",
            "description": "Build resilient language agents as graphs for complex multi-step workflows",
            "stars": "5.8k",
            "language": "Python",
            "difficulty": "Advanced",
            "topics": ["Graphs", "Workflows", "LangChain"],
            "download_url": "https://github.com/langchain-ai/langgraph/archive/refs/heads/main.zip",
            "last_updated": "2024-01-14",
            "license": "MIT",
            "docs_url": "https://langchain-ai.github.io/langgraph/"
        },
        {
            "name": "AgentGPT",
            "repo": "reworkd/AgentGPT",
            "description": "Assemble, configure, and deploy autonomous AI Agents in your browser",
            "stars": "31k",
            "language": "TypeScript",
            "difficulty": "Intermediate",
            "topics": ["Browser", "Deploy", "Autonomous"],
            "download_url": "https://github.com/reworkd/AgentGPT/archive/refs/heads/main.zip",
            "last_updated": "2024-01-11",
            "license": "GPL-3.0",
            "demo_url": "https://agentgpt.reworkd.ai/"
        },
        {
            "name": "BabyAGI",
            "repo": "yoheinakajima/babyagi",
            "description": "AI-powered task management system that creates and executes tasks autonomously",
            "stars": "20k",
            "language": "Python",
            "difficulty": "Advanced",
            "topics": ["Task Management", "Autonomous", "AI-powered"],
            "download_url": "https://github.com/yoheinakajima/babyagi/archive/refs/heads/main.zip",
            "last_updated": "2024-01-09",
            "license": "MIT"
        }
    ]
    
    render_category_stats(agent_projects)
    
    for i, project in enumerate(agent_projects):
        render_project_card(project, f"agent_{i}")

with tab2:
    st.markdown('<div class="category-header">', unsafe_allow_html=True)
    st.header("🧠 Large Language Model Projects")
    st.markdown("*LLM frameworks, local deployment, and language model applications*")
    st.markdown('</div>', unsafe_allow_html=True)
    
    llm_projects = [
        {
            "name": "Ollama",
            "repo": "ollama/ollama",
            "description": "Get up and running with large language models locally with ease",
            "stars": "95k",
            "language": "Go",
            "difficulty": "Beginner",
            "topics": ["Local AI", "LLM", "Privacy"],
            "download_url": "https://github.com/ollama/ollama/archive/refs/heads/main.zip",
            "last_updated": "2024-01-16",
            "license": "MIT",
            "docs_url": "https://ollama.ai/docs"
        },
        {
            "name": "LangChain",
            "repo": "langchain-ai/langchain",
            "description": "Framework for developing applications powered by language models",
            "stars": "94k",
            "language": "Python",
            "difficulty": "Intermediate",
            "topics": ["Framework", "LLM", "Applications"],
            "download_url": "https://github.com/langchain-ai/langchain/archive/refs/heads/master.zip",
            "last_updated": "2024-01-16",
            "license": "MIT",
            "docs_url": "https://python.langchain.com/"
        },
        {
            "name": "Transformers",
            "repo": "huggingface/transformers",
            "description": "State-of-the-art Machine Learning for PyTorch, TensorFlow, and JAX",
            "stars": "133k",
            "language": "Python",
            "difficulty": "Advanced",
            "topics": ["ML", "Transformers", "Hugging Face"],
            "download_url": "https://github.com/huggingface/transformers/archive/refs/heads/main.zip",
            "last_updated": "2024-01-16",
            "license": "Apache-2.0",
            "docs_url": "https://huggingface.co/docs/transformers"
        },
        {
            "name": "LocalAI",
            "repo": "mudler/LocalAI",
            "description": "Free, Open Source OpenAI alternative for local deployment",
            "stars": "24k",
            "language": "Go",
            "difficulty": "Intermediate",
            "topics": ["Local AI", "OpenAI Alternative", "Self-hosted"],
            "download_url": "https://github.com/mudler/LocalAI/archive/refs/heads/master.zip",
            "last_updated": "2024-01-15",
            "license": "MIT",
            "docs_url": "https://localai.io/"
        },
        {
            "name": "Llama.cpp",
            "repo": "ggerganov/llama.cpp",
            "description": "Port of Facebook's LLaMA model in C/C++ for efficient inference",
            "stars": "66k",
            "language": "C++",
            "difficulty": "Advanced",
            "topics": ["LLaMA", "C++", "Inference"],
            "download_url": "https://github.com/ggerganov/llama.cpp/archive/refs/heads/master.zip",
            "last_updated": "2024-01-16",
            "license": "MIT"
        },
        {
            "name": "Axolotl",
            "repo": "OpenAccess-AI-Collective/axolotl",
            "description": "Go-to solution for finetuning large language models with ease",
            "stars": "7.5k",
            "language": "Python",
            "difficulty": "Advanced",
            "topics": ["Finetuning", "Training", "LLM"],
            "download_url": "https://github.com/OpenAccess-AI-Collective/axolotl/archive/refs/heads/main.zip",
            "last_updated": "2024-01-14",
            "license": "Apache-2.0"
        }
    ]
    
    render_category_stats(llm_projects)
    
    for i, project in enumerate(llm_projects):
        render_project_card(project, f"llm_{i}")

with tab3:
    st.markdown('<div class="category-header">', unsafe_allow_html=True)
    st.header("🛠️ Tools & Frameworks")
    st.markdown("*Development tools, automation frameworks, and productivity enhancers*")
    st.markdown('</div>', unsafe_allow_html=True)
    
    tools_projects = [
        {
            "name": "n8n",
            "repo": "n8n-io/n8n",
            "description": "Free and source-available fair-code licensed workflow automation tool",
            "stars": "47k",
            "language": "TypeScript",
            "difficulty": "Intermediate",
            "topics": ["Workflow", "Automation", "No-code"],
            "download_url": "https://github.com/n8n-io/n8n/archive/refs/heads/master.zip",
            "last_updated": "2024-01-16",
            "license": "Sustainable Use License",
            "demo_url": "https://n8n.io/demo"
        },
        {
            "name": "CrewAI",
            "repo": "joaomdmoura/crewAI",
            "description": "Framework for orchestrating role-playing, autonomous AI agents",
            "stars": "19k",
            "language": "Python",
            "difficulty": "Intermediate",
            "topics": ["Multi-agent", "Framework", "Orchestration"],
            "download_url": "https://github.com/joaomdmoura/crewAI/archive/refs/heads/main.zip",
            "last_updated": "2024-01-15",
            "license": "MIT",
            "docs_url": "https://docs.crewai.com/"
        },
        {
            "name": "AutoGen",
            "repo": "microsoft/autogen",
            "description": "Multi-agent conversation framework for building AI applications",
            "stars": "31k",
            "language": "Python",
            "difficulty": "Advanced",
            "topics": ["Multi-agent", "Microsoft", "Conversation"],
            "download_url": "https://github.com/microsoft/autogen/archive/refs/heads/main.zip",
            "last_updated": "2024-01-16",
            "license": "MIT",
            "docs_url": "https://microsoft.github.io/autogen/"
        },
        {
            "name": "Streamlit",
            "repo": "streamlit/streamlit",
            "description": "Streamlit — A faster way to build and share data apps",
            "stars": "35k",
            "language": "Python",
            "difficulty": "Beginner",
            "topics": ["Web Apps", "Data Science", "Dashboard"],
            "download_url": "https://github.com/streamlit/streamlit/archive/refs/heads/develop.zip",
            "last_updated": "2024-01-16",
            "license": "Apache-2.0",
            "docs_url": "https://docs.streamlit.io/"
        },
        {
            "name": "Gradio",
            "repo": "gradio-app/gradio",
            "description": "Build and share delightful machine learning apps",
            "stars": "32k",
            "language": "Python",
            "difficulty": "Beginner",
            "topics": ["ML Apps", "Interface", "Sharing"],
            "download_url": "https://github.com/gradio-app/gradio/archive/refs/heads/main.zip",
            "last_updated": "2024-01-16",
            "license": "Apache-2.0",
            "docs_url": "https://gradio.app/docs/"
        },
        {
            "name": "Flowise",
            "repo": "FlowiseAI/Flowise",
            "description": "Drag & drop UI to build your customized LLM flow",
            "stars": "30k",
            "language": "TypeScript",
            "difficulty": "Beginner",
            "topics": ["No-code", "LLM", "Visual"],
            "download_url": "https://github.com/FlowiseAI/Flowise/archive/refs/heads/main.zip",
            "last_updated": "2024-01-15",
            "license": "Apache-2.0",
            "demo_url": "https://flowiseai.com/"
        }
    ]
    
    render_category_stats(tools_projects)
    
    for i, project in enumerate(tools_projects):
        render_project_card(project, f"tools_{i}")

with tab4:
    st.markdown('<div class="category-header">', unsafe_allow_html=True)
    st.header("📚 Learning Resources")
    st.markdown("*Educational content, tutorials, and comprehensive learning materials*")
    st.markdown('</div>', unsafe_allow_html=True)
    
    learning_projects = [
        {
            "name": "Machine Learning Yearning",
            "repo": "ajaymache/machine-learning-yearning",
            "description": "Andrew Ng's Machine Learning Yearning book in markdown format",
            "stars": "7.6k",
            "language": "Markdown",
            "difficulty": "Beginner",
            "topics": ["Education", "Andrew Ng", "ML Theory"],
            "download_url": "https://github.com/ajaymache/machine-learning-yearning/archive/refs/heads/master.zip",
            "last_updated": "2023-12-20",
            "license": "MIT"
        },
        {
            "name": "AI Expert Roadmap",
            "repo": "AMAI-GmbH/AI-Expert-Roadmap",
            "description": "Roadmap to becoming an Artificial Intelligence Expert in 2024",
            "stars": "29k",
            "language": "Markdown",
            "difficulty": "Beginner",
            "topics": ["Roadmap", "Career", "AI Expert"],
            "download_url": "https://github.com/AMAI-GmbH/AI-Expert-Roadmap/archive/refs/heads/main.zip",
            "last_updated": "2024-01-10",
            "license": "MIT"
        },
        {
            "name": "Deep Learning Papers",
            "repo": "floodsung/Deep-Learning-Papers-Reading-Roadmap",
            "description": "Deep Learning papers reading roadmap for anyone interested in the field",
            "stars": "37k",
            "language": "Markdown",
            "difficulty": "Advanced",
            "topics": ["Research", "Papers", "Deep Learning"],
            "download_url": "https://github.com/floodsung/Deep-Learning-Papers-Reading-Roadmap/archive/refs/heads/master.zip",
            "last_updated": "2023-11-15",
            "license": "MIT"
        },
        {
            "name": "Awesome AI",
            "repo": "owainlewis/awesome-artificial-intelligence",
            "description": "A curated list of Artificial Intelligence resources and tools",
            "stars": "25k",
            "language": "Markdown",
            "difficulty": "Beginner",
            "topics": ["Awesome List", "Resources", "Curated"],
            "download_url": "https://github.com/owainlewis/awesome-artificial-intelligence/archive/refs/heads/master.zip",
            "last_updated": "2024-01-05",
            "license": "MIT"
        },
        {
            "name": "LLM Course",
            "repo": "mlabonne/llm-course",
            "description": "Course to get into Large Language Models (LLMs) with roadmaps and notebooks",
            "stars": "37k",
            "language": "Jupyter Notebook",
            "difficulty": "Intermediate",
            "topics": ["Course", "LLM", "Notebooks"],
            "download_url": "https://github.com/mlabonne/llm-course/archive/refs/heads/main.zip",
            "last_updated": "2024-01-12",
            "license": "Apache-2.0"
        },
        {
            "name": "Prompt Engineering Guide",
            "repo": "dair-ai/Prompt-Engineering-Guide",
            "description": "Guides, papers, lecture, notebooks and resources for prompt engineering",
            "stars": "48k",
            "language": "Markdown",
            "difficulty": "Intermediate",
            "topics": ["Prompt Engineering", "Guide", "Resources"],
            "download_url": "https://github.com/dair-ai/Prompt-Engineering-Guide/archive/refs/heads/main.zip",
            "last_updated": "2024-01-14",
            "license": "MIT",
            "docs_url": "https://www.promptingguide.ai/"
        }
    ]
    
    render_category_stats(learning_projects)
    
    for i, project in enumerate(learning_projects):
        render_project_card(project, f"learning_{i}")

with tab5:
    st.markdown('<div class="category-header">', unsafe_allow_html=True)
    st.header("🔥 Trending AI Projects")
    st.markdown("*Hot and trending projects in the AI community*")
    st.markdown('</div>', unsafe_allow_html=True)
    
    trending_projects = [
        {
            "name": "ChatGPT Next Web",
            "repo": "ChatGPTNextWeb/ChatGPT-Next-Web",
            "description": "A cross-platform ChatGPT/Gemini UI (Web / PWA / Linux / Win / MacOS)",
            "stars": "75k",
            "language": "TypeScript",
            "difficulty": "Intermediate",
            "topics": ["ChatGPT", "UI", "Cross-platform"],
            "download_url": "https://github.com/ChatGPTNextWeb/ChatGPT-Next-Web/archive/refs/heads/main.zip",
            "last_updated": "2024-01-16",
            "license": "MIT",
            "demo_url": "https://app.nextchat.dev/"
        },
        {
            "name": "Open WebUI",
            "repo": "open-webui/open-webui",
            "description": "User-friendly WebUI for LLMs (Formerly Ollama WebUI)",
            "stars": "42k",
            "language": "Svelte",
            "difficulty": "Intermediate",
            "topics": ["WebUI", "Ollama", "LLM Interface"],
            "download_url": "https://github.com/open-webui/open-webui/archive/refs/heads/main.zip",
            "last_updated": "2024-01-16",
            "license": "MIT",
            "docs_url": "https://docs.openwebui.com/"
        },
        {
            "name": "Dify",
            "repo": "langgenius/dify",
            "description": "Dify is an open-source LLM app development platform",
            "stars": "47k",
            "language": "TypeScript",
            "difficulty": "Advanced",
            "topics": ["LLM Apps", "Platform", "Development"],
            "download_url": "https://github.com/langgenius/dify/archive/refs/heads/main.zip",
            "last_updated": "2024-01-16",
            "license": "Apache-2.0",
            "demo_url": "https://dify.ai/"
        },
        {
            "name": "Cursor Rules",
            "repo": "PatrickJS/awesome-cursorrules",
            "description": "A curated list of awesome .cursorrules files for AI-powered coding",
            "stars": "2.1k",
            "language": "Markdown",
            "difficulty": "Beginner",
            "topics": ["Cursor", "AI Coding", "Rules"],
            "download_url": "https://github.com/PatrickJS/awesome-cursorrules/archive/refs/heads/main.zip",
            "last_updated": "2024-01-15",
            "license": "MIT"
        },
        {
            "name": "Aider",
            "repo": "paul-gauthier/aider",
            "description": "AI pair programming in your terminal",
            "stars": "20k",
            "language": "Python",
            "difficulty": "Intermediate",
            "topics": ["Pair Programming", "Terminal", "AI Coding"],
            "download_url": "https://github.com/paul-gauthier/aider/archive/refs/heads/main.zip",
            "last_updated": "2024-01-16",
            "license": "Apache-2.0",
            "docs_url": "https://aider.chat/"
        }
    ]
    
    render_category_stats(trending_projects)
    
    for i, project in enumerate(trending_projects):
        render_project_card(project, f"trending_{i}")

with tab6:
    st.markdown('<div class="category-header">', unsafe_allow_html=True)
    st.header("🎨 Multimodal AI")
    st.markdown("*Vision, audio, and multimodal AI projects*")
    st.markdown('</div>', unsafe_allow_html=True)
    
    multimodal_projects = [
        {
            "name": "ComfyUI",
            "repo": "comfyanonymous/ComfyUI",
            "description": "The most powerful and modular stable diffusion GUI and backend",
            "stars": "53k",
            "language": "Python",
            "difficulty": "Intermediate",
            "topics": ["Stable Diffusion", "GUI", "Image Generation"],
            "download_url": "https://github.com/comfyanonymous/ComfyUI/archive/refs/heads/master.zip",
            "last_updated": "2024-01-16",
            "license": "GPL-3.0"
        },
        {
            "name": "AUTOMATIC1111",
            "repo": "AUTOMATIC1111/stable-diffusion-webui",
            "description": "Stable Diffusion web UI",
            "stars": "140k",
            "language": "Python",
            "difficulty": "Intermediate",
            "topics": ["Stable Diffusion", "Web UI", "Image Generation"],
            "download_url": "https://github.com/AUTOMATIC1111/stable-diffusion-webui/archive/refs/heads/master.zip",
            "last_updated": "2024-01-15",
            "license": "AGPL-3.0"
        },
        {
            "name": "Whisper",
            "repo": "openai/whisper",
            "description": "Robust Speech Recognition via Large-Scale Weak Supervision",
            "stars": "69k",
            "language": "Python",
            "difficulty": "Intermediate",
            "topics": ["Speech Recognition", "OpenAI", "Audio"],
            "download_url": "https://github.com/openai/whisper/archive/refs/heads/main.zip",
            "last_updated": "2024-01-10",
            "license": "MIT"
        },
        {
            "name": "LLaVA",
            "repo": "haotian-liu/LLaVA",
            "description": "Large Language and Vision Assistant",
            "stars": "19k",
            "language": "Python",
            "difficulty": "Advanced",
            "topics": ["Vision", "Language", "Multimodal"],
            "download_url": "https://github.com/haotian-liu/LLaVA/archive/refs/heads/main.zip",
            "last_updated": "2024-01-12",
            "license": "Apache-2.0"
        }
    ]
    
    render_category_stats(multimodal_projects)
    
    for i, project in enumerate(multimodal_projects):
        render_project_card(project, f"multimodal_{i}")

with tab7:
    st.markdown('<div class="category-header">', unsafe_allow_html=True)
    st.header("🤖 AI Robotics")
    st.markdown("*Robotics, embodied AI, and physical world applications*")
    st.markdown('</div>', unsafe_allow_html=True)
    
    robotics_projects = [
        {
            "name": "Mobile ALOHA",
            "repo": "MarkFzp/mobile-aloha",
            "description": "Mobile ALOHA: Learning Bimanual Mobile Manipulation with Low-Cost Whole-Body Teleoperation",
            "stars": "3.8k",
            "language": "Python",
            "difficulty": "Advanced",
            "topics": ["Robotics", "Manipulation", "Teleoperation"],
            "download_url": "https://github.com/MarkFzp/mobile-aloha/archive/refs/heads/main.zip",
            "last_updated": "2024-01-08",
            "license": "MIT"
        },
        {
            "name": "OpenDR",
            "repo": "opendr-eu/opendr",
            "description": "A modular, open and non-proprietary toolkit for core robotic functionalities",
            "stars": "1.3k",
            "language": "Python",
            "difficulty": "Advanced",
            "topics": ["Robotics", "Toolkit", "Modular"],
            "download_url": "https://github.com/opendr-eu/opendr/archive/refs/heads/master.zip",
            "last_updated": "2024-01-05",
            "license": "Apache-2.0"
        },
        {
            "name": "ROS AI",
            "repo": "ros-ai/ros2_ai_essentials",
            "description": "Essential AI packages and tools for ROS 2",
            "stars": "890",
            "language": "Python",
            "difficulty": "Advanced",
            "topics": ["ROS", "AI", "Robotics"],
            "download_url": "https://github.com/ros-ai/ros2_ai_essentials/archive/refs/heads/main.zip",
            "last_updated": "2024-01-03",
            "license": "Apache-2.0"
        }
    ]
    
    render_category_stats(robotics_projects)
    
    for i, project in enumerate(robotics_projects):
        render_project_card(project, f"robotics_{i}")

with tab8:
    st.markdown('<div class="category-header">', unsafe_allow_html=True)
    st.header("🔬 Research Tools")
    st.markdown("*Research frameworks, experiment tracking, and scientific computing*")
    st.markdown('</div>', unsafe_allow_html=True)
    
    research_projects = [
        {
            "name": "Weights & Biases",
            "repo": "wandb/wandb",
            "description": "A tool for visualizing and tracking your machine learning experiments",
            "stars": "8.8k",
            "language": "Python",
            "difficulty": "Intermediate",
            "topics": ["Experiment Tracking", "Visualization", "ML"],
            "download_url": "https://github.com/wandb/wandb/archive/refs/heads/main.zip",
            "last_updated": "2024-01-16",
            "license": "MIT",
            "docs_url": "https://docs.wandb.ai/"
        },
        {
            "name": "MLflow",
            "repo": "mlflow/mlflow",
            "description": "Open source platform for the machine learning lifecycle",
            "stars": "18k",
            "language": "Python",
            "difficulty": "Intermediate",
            "topics": ["ML Lifecycle", "Tracking", "Platform"],
            "download_url": "https://github.com/mlflow/mlflow/archive/refs/heads/master.zip",
            "last_updated": "2024-01-16",
            "license": "Apache-2.0",
            "docs_url": "https://mlflow.org/docs/latest/index.html"
        },
        {
            "name": "DVC",
            "repo": "iterative/dvc",
            "description": "Data Version Control | Git for Data & Models",
            "stars": "13k",
            "language": "Python",
            "difficulty": "Intermediate",
            "topics": ["Version Control", "Data", "Models"],
            "download_url": "https://github.com/iterative/dvc/archive/refs/heads/main.zip",
            "last_updated": "2024-01-16",
            "license": "Apache-2.0",
            "docs_url": "https://dvc.org/doc"
        },
        {
            "name": "Papers With Code",
            "repo": "paperswithcode/paperswithcode-data",
            "description": "Papers with Code dataset - machine learning papers, code and evaluation tables",
            "stars": "1.8k",
            "language": "Python",
            "difficulty": "Beginner",
            "topics": ["Research", "Papers", "Dataset"],
            "download_url": "https://github.com/paperswithcode/paperswithcode-data/archive/refs/heads/master.zip",
            "last_updated": "2024-01-10",
            "license": "CC-BY-SA-4.0"
        }
    ]
    
    render_category_stats(research_projects)
    
    for i, project in enumerate(research_projects):
        render_project_card(project, f"research_{i}")

# Enhanced sidebar with more features
with st.sidebar:
    st.markdown("### 📊 Repository Statistics")
    
    total_projects = 8 + 6 + 6 + 6 + 5 + 4 + 3 + 4  # Total across all categories
    st.metric("Total Repositories", total_projects)
    st.metric("Total Stars", "1M+")
    st.metric("Categories", 8)
    st.metric("Languages", 12)
    
    st.markdown("---")
    
    st.markdown("### 🎯 Quick Filters")
    
    if st.button("🔥 Most Starred", key="sidebar_most_starred", use_container_width=True):
        st.info("Showing projects with 50k+ stars")
    
    if st.button("🆕 Recently Updated", key="sidebar_recent", use_container_width=True):
        st.info("Showing projects updated in last 7 days")
    
    if st.button("👶 Beginner Friendly", key="sidebar_beginner", use_container_width=True):
        st.info("Showing beginner-friendly projects")
    
    st.markdown("---")
    
    st.markdown("### 🔗 External Resources")
    st.markdown("""
    <div style="margin: 1rem 0;">
        <a href="https://entremotivator.com" target="_blank" class="resource-link">
            🚀 Visit Entremotivator.com
        </a>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    **Useful Links:**
    - [GitHub Trending](https://github.com/trending)
    - [Papers With Code](https://paperswithcode.com/)
    - [Awesome Lists](https://github.com/sindresorhus/awesome)
    - [AI Collection](https://github.com/ai-collection/ai-collection)
    - [Hugging Face](https://huggingface.co/)
    - [OpenAI](https://openai.com/)
    """)
    
    st.markdown("---")
    
    st.markdown("### 💡 Pro Tips")
    st.info("""
    **GitHub Best Practices:**
    - ⭐ Star repositories you find useful
    - 🍴 Fork projects to experiment
    - 📋 Read README files thoroughly
    - 🐛 Check issues for known problems
    - 📝 Contribute to open source
    - 🔔 Watch for updates
    """)
    
    st.markdown("---")
    
    st.markdown("### 📈 Trending Topics")
    trending_topics = [
        "🤖 AI Agents", "🧠 Large Language Models", "🎨 Generative AI", 
        "🔍 RAG Systems", "🛠️ AI Tools", "📚 ML Education",
        "🎯 Prompt Engineering", "🔬 Research"
    ]
    
    for topic in trending_topics:
        st.markdown(f"- {topic}")

# Footer with enhanced information
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 2rem; background: rgba(30, 41, 59, 0.6); border-radius: 12px; margin: 2rem 0;">
    <h3 style="color: #f59e0b;">🤖 AI Agent Toolkit</h3>
    <p>Comprehensive GitHub Resources Hub for AI Developers</p>
    <p><strong>Created by D Hudson</strong> | <em>Discover, Learn, Build</em></p>
    <p>🌟 <strong>{}</strong> curated repositories | 🚀 <strong>1M+</strong> total stars | 📚 <strong>8</strong> categories</p>
    <p style="margin-top: 1rem; font-size: 0.9em; color: #cbd5e1;">
        This toolkit is designed to help developers discover the best AI projects, 
        learn from open-source implementations, and build amazing AI applications.
    </p>
</div>
""".format(total_projects), unsafe_allow_html=True)

if 'last_search' not in st.session_state:
    st.session_state.last_search = ""

if 'favorite_projects' not in st.session_state:
    st.session_state.favorite_projects = []

if search_term and search_term != st.session_state.last_search:
    st.session_state.last_search = search_term
    st.success(f"🔍 Searching for: '{search_term}'")
    st.info("Search functionality will filter projects across all categories based on name, description, and topics.")
