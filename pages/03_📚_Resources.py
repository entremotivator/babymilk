import streamlit as st
import os
import base64

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

def add_card_styles():
    """Add custom CSS for card-based UI"""
    st.markdown("""
    <style>
    .resource-card {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border: 1px solid rgba(245, 158, 11, 0.2);
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1rem 0;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
    }
    
    .resource-card:hover {
        transform: translateY(-5px);
        border-color: rgba(245, 158, 11, 0.5);
        box-shadow: 0 8px 24px rgba(245, 158, 11, 0.2);
    }
    
    .card-icon {
        font-size: 2.5rem;
        margin-bottom: 1rem;
        display: block;
    }
    
    .card-title {
        color: #f59e0b;
        font-size: 1.4rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        font-family: 'Inter', sans-serif;
    }
    
    .card-description {
        color: #cbd5e1;
        font-size: 1rem;
        line-height: 1.6;
        margin-bottom: 1rem;
    }
    
    .card-tags {
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
        margin-top: 1rem;
    }
    
    .tag {
        background: rgba(245, 158, 11, 0.1);
        color: #f59e0b;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.85rem;
        border: 1px solid rgba(245, 158, 11, 0.3);
    }
    
    .resource-link {
        color: #60a5fa;
        text-decoration: none;
        font-weight: 500;
        transition: color 0.2s ease;
    }
    
    .resource-link:hover {
        color: #93c5fd;
    }
    
    .section-header {
        color: #f59e0b;
        font-size: 2rem;
        font-weight: 700;
        margin: 2rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid rgba(245, 158, 11, 0.3);
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
        <div style="display: flex; justify-content: center; align-items: center; margin: 2rem 0;">
            <img src="data:image/png;base64,{get_base64_of_bin_file(logo_path)}" alt="AI Agent Toolkit Logo" style="max-width: 300px; height: auto; filter: drop-shadow(0 8px 32px rgba(245, 158, 11, 0.3));">
        </div>
        """, unsafe_allow_html=True)

def create_resource_card(icon, title, description, tags, link=None):
    """Create a styled resource card"""
    tags_html = "".join([f'<span class="tag">{tag}</span>' for tag in tags])
    link_html = f'<a href="{link}" class="resource-link" target="_blank">🔗 Visit Resource →</a>' if link else ""
    
    return f"""
    <div class="resource-card">
        <span class="card-icon">{icon}</span>
        <h3 class="card-title">{title}</h3>
        <p class="card-description">{description}</p>
        <div class="card-tags">{tags_html}</div>
        {link_html}
    </div>
    """

# Apply styling
hide_streamlit_style()
add_card_styles()

# Page configuration
st.set_page_config(
    page_title="Resources - AI Agent Toolkit",
    page_icon="📚",
    layout="wide"
)

# Display logo
display_logo()

# Page header
st.title("📚 AI Agent Toolkit Resources")
st.markdown("""
Your comprehensive hub for AI agent development resources, tutorials, documentation, and learning materials.
""")

# Premium Downloads Section
st.markdown('<h2 class="section-header">📥 Premium Downloads</h2>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown(create_resource_card(
        "📋",
        "The Ultimate AI & Bot Checklist",
        "A comprehensive, step-by-step checklist covering every aspect of AI agent development from planning to deployment and maintenance.",
        ["Planning", "Development", "Testing", "Deployment"]
    ), unsafe_allow_html=True)
    
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
    st.markdown(create_resource_card(
        "🛠️",
        "250 Best AI Tools Directory",
        "Curated directory of the most powerful AI development tools, frameworks, and platforms with detailed descriptions and use cases.",
        ["Tools", "Frameworks", "Platforms", "APIs"]
    ), unsafe_allow_html=True)
    
    if os.path.exists("/home/ubuntu/ai-agent-toolkit/250_Best_AI_Tools.pdf"):
        with open("/home/ubuntu/ai-agent-toolkit/250_Best_AI_Tools.pdf", "rb") as file:
            st.download_button(
                label="📥 Download Tools PDF",
                data=file.read(),
                file_name="250_Best_AI_Tools.pdf",
                mime="application/pdf",
                use_container_width=True
            )

# Learning Resources
st.markdown('<h2 class="section-header">🎓 Learning Resources</h2>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(create_resource_card(
        "📖",
        "OpenAI Documentation",
        "Official guide to GPT models, API integration, prompt engineering, and best practices for building with OpenAI's platform.",
        ["GPT", "API", "Prompting"],
        "https://platform.openai.com/docs"
    ), unsafe_allow_html=True)
    
    st.markdown(create_resource_card(
        "🦜",
        "LangChain Documentation",
        "Comprehensive framework documentation for building LLM applications with chains, agents, and memory systems.",
        ["Framework", "LLM", "Agents"],
        "https://python.langchain.com/docs"
    ), unsafe_allow_html=True)

with col2:
    st.markdown(create_resource_card(
        "🤖",
        "Anthropic Claude Docs",
        "Learn to build with Claude AI, including prompt engineering, API usage, and advanced features like function calling.",
        ["Claude", "API", "Integration"],
        "https://docs.anthropic.com"
    ), unsafe_allow_html=True)
    
    st.markdown(create_resource_card(
        "⚡",
        "Streamlit Documentation",
        "Build interactive web apps for your AI agents with Python. Tutorials, components, and deployment guides included.",
        ["Web Apps", "Python", "UI"],
        "https://docs.streamlit.io"
    ), unsafe_allow_html=True)

with col3:
    st.markdown(create_resource_card(
        "🔥",
        "Hugging Face Course",
        "Free course on transformers, NLP, and deploying machine learning models. Perfect for intermediate learners.",
        ["NLP", "Transformers", "ML"],
        "https://huggingface.co/learn"
    ), unsafe_allow_html=True)
    
    st.markdown(create_resource_card(
        "🎯",
        "Prompt Engineering Guide",
        "Master the art of crafting effective prompts with techniques, examples, and best practices for all major LLMs.",
        ["Prompting", "Techniques", "Guide"],
        "https://www.promptingguide.ai"
    ), unsafe_allow_html=True)

# Advanced Resources
st.markdown('<h2 class="section-header">🚀 Advanced Resources</h2>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown(create_resource_card(
        "🧠",
        "AI Agent Architectures",
        "Research papers and implementations of advanced agent systems including ReAct, AutoGPT, and multi-agent frameworks.",
        ["Architecture", "Research", "Advanced"],
        "https://arxiv.org/list/cs.AI/recent"
    ), unsafe_allow_html=True)
    
    st.markdown(create_resource_card(
        "🔬",
        "LLM Evaluation & Benchmarks",
        "Resources for testing and evaluating AI agents, including benchmark datasets and performance metrics.",
        ["Testing", "Evaluation", "Benchmarks"]
    ), unsafe_allow_html=True)

with col2:
    st.markdown(create_resource_card(
        "🌐",
        "Vector Database Guides",
        "Learn about Pinecone, Weaviate, and Chroma for building RAG systems and semantic search capabilities.",
        ["RAG", "Embeddings", "Search"],
        "https://www.pinecone.io/learn"
    ), unsafe_allow_html=True)
    
    st.markdown(create_resource_card(
        "⚙️",
        "Fine-tuning Resources",
        "Guides and tutorials for fine-tuning LLMs on custom datasets, including LoRA, PEFT, and full fine-tuning approaches.",
        ["Fine-tuning", "Training", "Customization"]
    ), unsafe_allow_html=True)

# Community Resources
st.markdown('<h2 class="section-header">👥 Community & Support</h2>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(create_resource_card(
        "💬",
        "AI Discord Communities",
        "Join active Discord servers for real-time help, project collaboration, and networking with AI developers.",
        ["Community", "Chat", "Support"]
    ), unsafe_allow_html=True)

with col2:
    st.markdown(create_resource_card(
        "🐙",
        "GitHub Repositories",
        "Explore open-source AI agent projects, frameworks, and implementations to learn from real-world code.",
        ["Open Source", "Code", "Projects"],
        "https://github.com/topics/ai-agents"
    ), unsafe_allow_html=True)

with col3:
    st.markdown(create_resource_card(
        "📺",
        "YouTube Tutorials",
        "Video walkthroughs, project builds, and in-depth explanations from leading AI educators and practitioners.",
        ["Videos", "Tutorials", "Learning"]
    ), unsafe_allow_html=True)

# Additional Learning Paths
st.markdown('<h2 class="section-header">🎯 Structured Learning Paths</h2>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    ### 🌱 Beginner Track
    - Understanding AI Fundamentals
    - Introduction to AI Agents
    - Building Your First Bot
    - Basic Deployment Strategies
    - Prompt Engineering Basics
    """)

with col2:
    st.markdown("""
    ### 📈 Intermediate Track
    - Advanced Agent Architectures
    - API & Database Integration
    - Natural Language Processing
    - Performance Optimization
    - RAG System Development
    """)

with col3:
    st.markdown("""
    ### 🏆 Advanced Track
    - Multi-Agent Systems
    - Machine Learning Integration
    - Enterprise Deployment
    - Custom Framework Development
    - Security & Scalability
    """)

# Call to Action
st.markdown("---")
st.markdown("""
<div style="text-align: center; margin: 3rem 0;">
    <a href="https://entremotivator.com" target="_blank" style="display: inline-block; background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%); color: #000000 !important; padding: 1rem 2rem; border-radius: 12px; text-decoration: none; font-weight: 600; font-family: 'Inter', sans-serif; transition: all 0.3s ease; box-shadow: 0 4px 12px rgba(245, 158, 11, 0.3); margin: 0.5rem; font-size: 1.1rem;">
        🚀 Explore More Resources at Entremotivator.com
    </a>
</div>
""", unsafe_allow_html=True)

st.markdown("---")
st.markdown("*This page is part of the AI Agent Toolkit by D Hudson. Explore other sections for comprehensive AI development resources.*")
