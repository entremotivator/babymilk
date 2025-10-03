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
Your comprehensive hub for AI agent development resources, tutorials, documentation, and learning materials. Everything you need to master AI development.
""")

# Official Documentation
st.markdown('<h2 class="section-header">📖 Official Documentation</h2>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(create_resource_card(
        "🤖",
        "OpenAI Platform",
        "Complete documentation for GPT-4, ChatGPT API, embeddings, fine-tuning, and best practices for building with OpenAI models.",
        ["GPT-4", "API", "Embeddings"],
        "https://platform.openai.com/docs"
    ), unsafe_allow_html=True)
    
    st.markdown(create_resource_card(
        "🦜",
        "LangChain",
        "Framework for developing applications with LLMs. Includes chains, agents, memory systems, and tool integration.",
        ["Framework", "Agents", "Tools"],
        "https://python.langchain.com/docs"
    ), unsafe_allow_html=True)
    
    st.markdown(create_resource_card(
        "🔥",
        "Hugging Face",
        "Access thousands of pre-trained models, datasets, and tools for NLP, computer vision, and audio processing.",
        ["Models", "NLP", "Datasets"],
        "https://huggingface.co/docs"
    ), unsafe_allow_html=True)

with col2:
    st.markdown(create_resource_card(
        "🧠",
        "Anthropic Claude",
        "Documentation for Claude AI including prompt engineering, function calling, vision capabilities, and API integration.",
        ["Claude", "Prompting", "Vision"],
        "https://docs.anthropic.com"
    ), unsafe_allow_html=True)
    
    st.markdown(create_resource_card(
        "⚡",
        "Streamlit",
        "Build and deploy interactive web apps for machine learning and data science projects with pure Python.",
        ["Web Apps", "Python", "Deployment"],
        "https://docs.streamlit.io"
    ), unsafe_allow_html=True)
    
    st.markdown(create_resource_card(
        "🌊",
        "LlamaIndex",
        "Data framework for LLM applications. Build RAG systems, semantic search, and knowledge bases with ease.",
        ["RAG", "Search", "Data"],
        "https://docs.llamaindex.ai"
    ), unsafe_allow_html=True)

with col3:
    st.markdown(create_resource_card(
        "🎯",
        "Pinecone",
        "Vector database for building semantic search, recommendation systems, and RAG applications at scale.",
        ["Vectors", "Database", "Search"],
        "https://docs.pinecone.io"
    ), unsafe_allow_html=True)
    
    st.markdown(create_resource_card(
        "⚙️",
        "LangSmith",
        "Debug, test, and monitor LLM applications. Track prompts, evaluate outputs, and optimize performance.",
        ["Testing", "Monitoring", "Debug"],
        "https://docs.smith.langchain.com"
    ), unsafe_allow_html=True)
    
    st.markdown(create_resource_card(
        "🔮",
        "Cohere",
        "Enterprise AI platform with powerful language models, embeddings, and reranking capabilities.",
        ["LLM", "Embeddings", "Enterprise"],
        "https://docs.cohere.com"
    ), unsafe_allow_html=True)

# Learning Platforms & Courses
st.markdown('<h2 class="section-header">🎓 Learning Platforms & Courses</h2>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(create_resource_card(
        "🎯",
        "Prompt Engineering Guide",
        "Comprehensive guide to prompt engineering techniques, best practices, and examples for all major LLMs.",
        ["Prompting", "Techniques", "Examples"],
        "https://www.promptingguide.ai"
    ), unsafe_allow_html=True)
    
    st.markdown(create_resource_card(
        "🏫",
        "DeepLearning.AI",
        "Free courses on AI, machine learning, and LLMs taught by Andrew Ng and industry experts.",
        ["Courses", "ML", "Free"],
        "https://www.deeplearning.ai"
    ), unsafe_allow_html=True)
    
    st.markdown(create_resource_card(
        "📚",
        "Fast.ai",
        "Practical deep learning courses with a top-down teaching approach. Free and beginner-friendly.",
        ["Deep Learning", "Practical", "Free"],
        "https://www.fast.ai"
    ), unsafe_allow_html=True)

with col2:
    st.markdown(create_resource_card(
        "🎓",
        "Hugging Face Course",
        "Free comprehensive course on transformers, NLP, and deploying ML models in production.",
        ["Transformers", "NLP", "Deployment"],
        "https://huggingface.co/learn"
    ), unsafe_allow_html=True)
    
    st.markdown(create_resource_card(
        "🧪",
        "Google AI",
        "Machine learning crash courses, guides, and resources from Google's AI research team.",
        ["ML", "Google", "Research"],
        "https://ai.google/education"
    ), unsafe_allow_html=True)
    
    st.markdown(create_resource_card(
        "💡",
        "OpenAI Cookbook",
        "Code examples and guides for common tasks using OpenAI's API. Production-ready snippets.",
        ["Examples", "Code", "Guides"],
        "https://cookbook.openai.com"
    ), unsafe_allow_html=True)

with col3:
    st.markdown(create_resource_card(
        "🎬",
        "Full Stack Deep Learning",
        "Learn to build and deploy production-grade ML systems. Covers the entire ML lifecycle.",
        ["Production", "MLOps", "Full Stack"],
        "https://fullstackdeeplearning.com"
    ), unsafe_allow_html=True)
    
    st.markdown(create_resource_card(
        "🌐",
        "AWS ML University",
        "Free machine learning courses from Amazon engineers. Covers fundamentals to advanced topics.",
        ["AWS", "ML", "Cloud"],
        "https://aws.amazon.com/machine-learning/mlu"
    ), unsafe_allow_html=True)
    
    st.markdown(create_resource_card(
        "🎯",
        "Microsoft AI School",
        "Comprehensive AI learning paths, tutorials, and certification programs from Microsoft.",
        ["Microsoft", "Certification", "Azure"],
        "https://learn.microsoft.com/ai"
    ), unsafe_allow_html=True)

# Research & Advanced Topics
st.markdown('<h2 class="section-header">🔬 Research & Advanced Topics</h2>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(create_resource_card(
        "📄",
        "arXiv AI Papers",
        "Latest research papers in artificial intelligence, machine learning, and natural language processing.",
        ["Research", "Papers", "Cutting-edge"],
        "https://arxiv.org/list/cs.AI/recent"
    ), unsafe_allow_html=True)
    
    st.markdown(create_resource_card(
        "🏗️",
        "Papers With Code",
        "ML papers with code implementations. Compare state-of-the-art results and reproduce research.",
        ["Papers", "Code", "SOTA"],
        "https://paperswithcode.com"
    ), unsafe_allow_html=True)
    
    st.markdown(create_resource_card(
        "🧠",
        "Distill.pub",
        "Clear explanations of machine learning concepts through interactive visualizations.",
        ["Visual", "Explanations", "Interactive"],
        "https://distill.pub"
    ), unsafe_allow_html=True)

with col2:
    st.markdown(create_resource_card(
        "🎯",
        "LLM Evaluation Guide",
        "Comprehensive resource for evaluating and benchmarking large language models and AI agents.",
        ["Evaluation", "Benchmarks", "Testing"],
        "https://github.com/ray-project/llm-numbers"
    ), unsafe_allow_html=True)
    
    st.markdown(create_resource_card(
        "⚡",
        "Agent Architectures",
        "Research and implementations of advanced agent systems: ReAct, AutoGPT, BabyAGI, and more.",
        ["Agents", "Architecture", "Advanced"],
        "https://github.com/Significant-Gravitas/AutoGPT"
    ), unsafe_allow_html=True)
    
    st.markdown(create_resource_card(
        "🔐",
        "AI Safety Resources",
        "Learn about AI alignment, safety, and responsible AI development practices.",
        ["Safety", "Ethics", "Alignment"],
        "https://www.alignmentforum.org"
    ), unsafe_allow_html=True)

with col3:
    st.markdown(create_resource_card(
        "🎨",
        "Stable Diffusion Guide",
        "Comprehensive guide to image generation, fine-tuning, and deploying diffusion models.",
        ["Image Gen", "Diffusion", "Art"],
        "https://stable-diffusion-art.com"
    ), unsafe_allow_html=True)
    
    st.markdown(create_resource_card(
        "🔧",
        "Fine-tuning Resources",
        "Guides for fine-tuning LLMs using LoRA, QLoRA, PEFT, and full parameter tuning methods.",
        ["Fine-tuning", "LoRA", "Training"],
        "https://github.com/huggingface/peft"
    ), unsafe_allow_html=True)
    
    st.markdown(create_resource_card(
        "📊",
        "MLOps Guide",
        "Best practices for deploying, monitoring, and maintaining ML models in production.",
        ["MLOps", "Production", "DevOps"],
        "https://ml-ops.org"
    ), unsafe_allow_html=True)

# Tools & Frameworks
st.markdown('<h2 class="section-header">🛠️ Development Tools & Frameworks</h2>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(create_resource_card(
        "🌊",
        "Weaviate",
        "Open-source vector database with hybrid search, filtering, and multi-modal capabilities.",
        ["Vector DB", "Search", "Open Source"],
        "https://weaviate.io/developers/weaviate"
    ), unsafe_allow_html=True)
    
    st.markdown(create_resource_card(
        "⚡",
        "Chroma",
        "Lightweight embedding database for AI applications. Easy to use and deploy locally.",
        ["Embeddings", "Local", "Simple"],
        "https://docs.trychroma.com"
    ), unsafe_allow_html=True)
    
    st.markdown(create_resource_card(
        "🔄",
        "Haystack",
        "Framework for building search systems and RAG pipelines with LLMs and transformers.",
        ["Search", "RAG", "Pipeline"],
        "https://docs.haystack.deepset.ai"
    ), unsafe_allow_html=True)

with col2:
    st.markdown(create_resource_card(
        "🐍",
        "Instructor",
        "Structured outputs from LLMs using Python type hints. Type-safe AI responses.",
        ["Python", "Types", "Structured"],
        "https://python.useinstructor.com"
    ), unsafe_allow_html=True)
    
    st.markdown(create_resource_card(
        "🎯",
        "DSPy",
        "Programming framework for building LM pipelines. Optimize prompts algorithmically.",
        ["Framework", "Optimization", "Research"],
        "https://dspy-docs.vercel.app"
    ), unsafe_allow_html=True)
    
    st.markdown(create_resource_card(
        "🔮",
        "Guardrails AI",
        "Add validation, structure, and safety checks to LLM outputs. Ensure reliable responses.",
        ["Validation", "Safety", "Quality"],
        "https://docs.guardrailsai.com"
    ), unsafe_allow_html=True)

with col3:
    st.markdown(create_resource_card(
        "🚀",
        "Vercel AI SDK",
        "Build AI-powered streaming interfaces with React, Vue, and Next.js.",
        ["Frontend", "Streaming", "React"],
        "https://sdk.vercel.ai/docs"
    ), unsafe_allow_html=True)
    
    st.markdown(create_resource_card(
        "🎨",
        "Gradio",
        "Create custom UI for ML models with Python. Share demos instantly.",
        ["UI", "Demos", "Python"],
        "https://www.gradio.app/docs"
    ), unsafe_allow_html=True)
    
    st.markdown(create_resource_card(
        "⚙️",
        "Ollama",
        "Run LLMs locally on your machine. Easy setup for Llama, Mistral, and more.",
        ["Local", "LLM", "Privacy"],
        "https://ollama.com"
    ), unsafe_allow_html=True)

# Community & Support
st.markdown('<h2 class="section-header">👥 Community & Support</h2>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(create_resource_card(
        "🐙",
        "Awesome AI Agents",
        "Curated list of AI agent frameworks, tools, papers, and projects. Regularly updated.",
        ["GitHub", "Curated", "Agents"],
        "https://github.com/e2b-dev/awesome-ai-agents"
    ), unsafe_allow_html=True)
    
    st.markdown(create_resource_card(
        "💬",
        "LangChain Discord",
        "Active community for LangChain developers. Get help and share projects.",
        ["Discord", "Community", "Help"],
        "https://discord.gg/langchain"
    ), unsafe_allow_html=True)

with col2:
    st.markdown(create_resource_card(
        "🤖",
        "Hugging Face Forums",
        "Ask questions, share models, and connect with the ML community.",
        ["Forums", "Community", "Models"],
        "https://discuss.huggingface.co"
    ), unsafe_allow_html=True)
    
    st.markdown(create_resource_card(
        "📺",
        "AI YouTube Channels",
        "Video tutorials and project walkthroughs from leading AI educators and practitioners.",
        ["Videos", "Tutorials", "Learning"]
    ), unsafe_allow_html=True)

with col3:
    st.markdown(create_resource_card(
        "📰",
        "AI News & Blogs",
        "Stay updated with the latest AI developments, releases, and breakthrough research.",
        ["News", "Updates", "Trends"]
    ), unsafe_allow_html=True)
    
    st.markdown(create_resource_card(
        "💼",
        "AI Job Boards",
        "Find opportunities in AI development, ML engineering, and research positions.",
        ["Jobs", "Careers", "Opportunities"]
    ), unsafe_allow_html=True)

# Additional Resources
st.markdown('<h2 class="section-header">🌟 Additional Resources</h2>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(create_resource_card(
        "📖",
        "AI Glossary",
        "Comprehensive glossary of AI and ML terms. Understand technical jargon and concepts.",
        ["Definitions", "Terms", "Reference"]
    ), unsafe_allow_html=True)
    
    st.markdown(create_resource_card(
        "🎯",
        "Prompt Templates",
        "Ready-to-use prompt templates for common tasks: summarization, extraction, classification.",
        ["Prompts", "Templates", "Examples"]
    ), unsafe_allow_html=True)
    
    st.markdown(create_resource_card(
        "🎪",
        "AI Demos & Examples",
        "Interactive demos showcasing AI capabilities. Test and learn from working examples.",
        ["Demos", "Interactive", "Examples"],
        "https://huggingface.co/spaces"
    ), unsafe_allow_html=True)

with col2:
    st.markdown(create_resource_card(
        "🔧",
        "AI Project Ideas",
        "Curated list of beginner to advanced AI project ideas with implementation guides.",
        ["Projects", "Ideas", "Practice"]
    ), unsafe_allow_html=True)
    
    st.markdown(create_resource_card(
        "📊",
        "Model Comparison",
        "Compare performance, cost, and capabilities of different LLMs and AI models.",
        ["Comparison", "Benchmarks", "Models"]
    ), unsafe_allow_html=True)
    
    st.markdown(create_resource_card(
        "🔍",
        "AI Research Navigator",
        "Discover and explore the latest AI research papers organized by topic and impact.",
        ["Research", "Papers", "Discovery"],
        "https://www.arxiv-sanity-lite.com"
    ), unsafe_allow_html=True)

with col3:
    st.markdown(create_resource_card(
        "🎓",
        "AI Certifications",
        "Professional certifications in AI, ML, and cloud AI services from major providers.",
        ["Certification", "Professional", "Career"]
    ), unsafe_allow_html=True)
    
    st.markdown(create_resource_card(
        "📝",
        "Technical Blogs",
        "In-depth technical articles on AI implementation, optimization, and best practices.",
        ["Blogs", "Technical", "Deep Dive"]
    ), unsafe_allow_html=True)
    
    st.markdown(create_resource_card(
        "🏆",
        "AI Competitions",
        "Participate in Kaggle competitions, hackathons, and challenges to sharpen your skills.",
        ["Competitions", "Kaggle", "Practice"],
        "https://www.kaggle.com/competitions"
    ), unsafe_allow_html=True)

# Specialized AI Topics
st.markdown('<h2 class="section-header">🎨 Specialized AI Topics</h2>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(create_resource_card(
        "🗣️",
        "Voice AI & TTS",
        "Resources for text-to-speech, voice cloning, and speech recognition with AI models.",
        ["Voice", "TTS", "Speech"],
        "https://elevenlabs.io/docs"
    ), unsafe_allow_html=True)
    
    st.markdown(create_resource_card(
        "🎵",
        "Music Generation AI",
        "Learn about AI music composition, audio synthesis, and generative audio models.",
        ["Music", "Audio", "Generation"],
        "https://github.com/suno-ai/bark"
    ), unsafe_allow_html=True)
    
    st.markdown(create_resource_card(
        "🎬",
        "Video AI Tools",
        "Video generation, editing, and analysis using AI. From synthesis to understanding.",
        ["Video", "Generation", "Analysis"],
        "https://stability.ai/stable-video"
    ), unsafe_allow_html=True)

with col2:
    st.markdown(create_resource_card(
        "👁️",
        "Computer Vision",
        "Object detection, image segmentation, and visual AI with OpenCV, YOLO, and more.",
        ["Vision", "Detection", "Images"],
        "https://opencv.org"
    ), unsafe_allow_html=True)
    
    st.markdown(create_resource_card(
        "🤖",
        "Robotics & AI",
        "Integration of AI with robotics, autonomous systems, and physical world interaction.",
        ["Robotics", "Autonomous", "Control"],
        "https://www.ros.org"
    ), unsafe_allow_html=True)
    
    st.markdown(create_resource_card(
        "💬",
        "Conversational AI",
        "Build chatbots, voice assistants, and dialogue systems with natural interactions.",
        ["Chatbots", "Dialogue", "NLU"],
        "https://rasa.com/docs"
    ), unsafe_allow_html=True)

with col3:
    st.markdown(create_resource_card(
        "📈",
        "Time Series AI",
        "Forecasting, anomaly detection, and pattern recognition in temporal data with AI.",
        ["Forecasting", "Anomaly", "Temporal"],
        "https://github.com/unit8co/darts"
    ), unsafe_allow_html=True)
    
    st.markdown(create_resource_card(
        "🧬",
        "AI for Science",
        "Applications of AI in biology, chemistry, physics, and scientific research.",
        ["Science", "Research", "Discovery"],
        "https://alphafold.ebi.ac.uk"
    ), unsafe_allow_html=True)
    
    st.markdown(create_resource_card(
        "🎮",
        "Game AI & RL",
        "Reinforcement learning, game playing agents, and AI for interactive entertainment.",
        ["Games", "RL", "Agents"],
        "https://gym.openai.com"
    ), unsafe_allow_html=True)

# Data & Infrastructure
st.markdown('<h2 class="section-header">💾 Data & Infrastructure</h2>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(create_resource_card(
        "🗄️",
        "PostgreSQL + pgvector",
        "Add vector similarity search to PostgreSQL for AI applications and embeddings.",
        ["Database", "Vectors", "SQL"],
        "https://github.com/pgvector/pgvector"
    ), unsafe_allow_html=True)
    
    st.markdown(create_resource_card(
        "⚡",
        "Redis AI",
        "Real-time AI with Redis. Vector search, caching, and high-performance data structures.",
        ["Redis", "Cache", "Real-time"],
        "https://redis.io/docs/stack/search/reference/vectors"
    ), unsafe_allow_html=True)
    
    st.markdown(create_resource_card(
        "🔥",
        "Qdrant",
        "High-performance vector database with filtering, hybrid search, and cloud deployment.",
        ["Vectors", "Search", "Performance"],
        "https://qdrant.tech/documentation"
    ), unsafe_allow_html=True)

with col2:
    st.markdown(create_resource_card(
        "☁️",
        "Supabase AI",
        "Postgres database with built-in vector support, edge functions, and real-time subscriptions.",
        ["Supabase", "Backend", "Real-time"],
        "https://supabase.com/docs/guides/ai"
    ), unsafe_allow_html=True)
    
    st.markdown(create_resource_card(
        "🌐",
        "Cloudflare AI",
        "Run AI models at the edge with Workers AI. Low latency, global deployment.",
        ["Edge", "Serverless", "Global"],
        "https://developers.cloudflare.com/workers-ai"
    ), unsafe_allow_html=True)
    
    st.markdown(create_resource_card(
        "🐳",
        "Docker for AI",
        "Containerize AI applications for reproducible, scalable deployments.",
        ["Docker", "Containers", "Deploy"],
        "https://docs.docker.com"
    ), unsafe_allow_html=True)

with col3:
    st.markdown(create_resource_card(
        "☸️",
        "Kubernetes ML",
        "Orchestrate ML workloads with Kubernetes. Scale training and inference.",
        ["K8s", "Orchestration", "Scale"],
        "https://kubernetes.io/docs/tutorials/stateless-application"
    ), unsafe_allow_html=True)
    
    st.markdown(create_resource_card(
        "📊",
        "MLflow",
        "Track experiments, package code, and deploy ML models. Complete MLOps platform.",
        ["MLOps", "Tracking", "Deploy"],
        "https://mlflow.org/docs/latest/index.html"
    ), unsafe_allow_html=True)
    
    st.markdown(create_resource_card(
        "🎯",
        "Weights & Biases",
        "Experiment tracking, hyperparameter optimization, and model management for ML teams.",
        ["Tracking", "Experiments", "Teams"],
        "https://docs.wandb.ai"
    ), unsafe_allow_html=True)

# Programming Languages & SDKs
st.markdown('<h2 class="section-header">💻 Programming Languages & SDKs</h2>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(create_resource_card(
        "🐍",
        "Python for AI",
        "Master Python for AI development. Libraries, best practices, and advanced techniques.",
        ["Python", "Programming", "Fundamentals"],
        "https://docs.python.org/3/tutorial"
    ), unsafe_allow_html=True)
    
    st.markdown(create_resource_card(
        "📊",
        "NumPy & Pandas",
        "Essential libraries for data manipulation, numerical computing, and analysis.",
        ["Data", "Arrays", "Analysis"],
        "https://numpy.org/doc"
    ), unsafe_allow_html=True)
    
    st.markdown(create_resource_card(
        "🔥",
        "PyTorch",
        "Deep learning framework for research and production. Dynamic computation graphs.",
        ["Deep Learning", "Framework", "Research"],
        "https://pytorch.org/tutorials"
    ), unsafe_allow_html=True)

with col2:
    st.markdown(create_resource_card(
        "🧮",
        "TensorFlow",
        "End-to-end platform for machine learning. From research to production deployment.",
        ["ML", "Framework", "Production"],
        "https://www.tensorflow.org/tutorials"
    ), unsafe_allow_html=True)
    
    st.markdown(create_resource_card(
        "⚡",
        "JAX",
        "High-performance numerical computing with automatic differentiation and GPU/TPU support.",
        ["JAX", "Performance", "Research"],
        "https://jax.readthedocs.io"
    ), unsafe_allow_html=True)
    
    st.markdown(create_resource_card(
        "🦀",
        "Rust for AI",
        "Build high-performance AI systems with Rust. Safety and speed combined.",
        ["Rust", "Performance", "Systems"],
        "https://www.arewelearningyet.com"
    ), unsafe_allow_html=True)

with col3:
    st.markdown(create_resource_card(
        "☕",
        "JavaScript AI",
        "Run ML models in the browser with TensorFlow.js, ONNX.js, and WebML.",
        ["JavaScript", "Browser", "Web"],
        "https://www.tensorflow.org/js"
    ), unsafe_allow_html=True)
    
    st.markdown(create_resource_card(
        "💎",
        "Julia for ML",
        "High-level, high-performance programming language for technical computing.",
        ["Julia", "Scientific", "Performance"],
        "https://julialang.org"
    ), unsafe_allow_html=True)
    
    st.markdown(create_resource_card(
        "⚙️",
        "Go for AI",
        "Build scalable AI services with Go. Concurrency and performance for production systems.",
        ["Go", "Scalability", "Backend"],
        "https://github.com/golang/go/wiki"
    ), unsafe_allow_html=True)

# Business & Strategy
st.markdown('<h2 class="section-header">💼 Business & Strategy</h2>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(create_resource_card(
        "📊",
        "AI ROI Calculator",
        "Calculate return on investment for AI projects. Business case templates and metrics.",
        ["ROI", "Business", "Metrics"]
    ), unsafe_allow_html=True)
    
    st.markdown(create_resource_card(
        "🎯",
        "AI Strategy Guides",
        "Develop AI strategies for enterprises. Roadmaps, governance, and transformation.",
        ["Strategy", "Enterprise", "Planning"]
    ), unsafe_allow_html=True)
    
    st.markdown(create_resource_card(
        "⚖️",
        "AI Ethics & Compliance",
        "Navigate AI regulations, ethical considerations, and responsible AI development.",
        ["Ethics", "Legal", "Compliance"],
        "https://www.whitehouse.gov/ostp/ai-bill-of-rights"
    ), unsafe_allow_html=True)

with col2:
    st.markdown(create_resource_card(
        "💰",
        "AI Pricing Models",
        "Understand pricing strategies for AI products. SaaS, usage-based, and enterprise models.",
        ["Pricing", "SaaS", "Business"]
    ), unsafe_allow_html=True)
    
    st.markdown(create_resource_card(
        "📈",
        "AI Market Research",
        "Industry reports, market trends, and competitive analysis in AI.",
        ["Market", "Trends", "Analysis"],
        "https://www.gartner.com/en/research"
    ), unsafe_allow_html=True)
    
    st.markdown(create_resource_card(
        "🤝",
        "AI Partnerships",
        "Build partnerships with AI providers, integrate third-party services, and APIs.",
        ["Partnerships", "Integration", "APIs"]
    ), unsafe_allow_html=True)

with col3:
    st.markdown(create_resource_card(
        "🎓",
        "AI for Startups",
        "Resources specifically for AI startups: funding, MVP development, go-to-market.",
        ["Startups", "Funding", "GTM"]
    ), unsafe_allow_html=True)
    
    st.markdown(create_resource_card(
        "🏢",
        "Enterprise AI",
        "Scaling AI in large organizations. Change management, security, and integration.",
        ["Enterprise", "Scale", "Security"]
    ), unsafe_allow_html=True)
    
    st.markdown(create_resource_card(
        "📢",
        "AI Marketing",
        "Market AI products effectively. Positioning, messaging, and growth strategies.",
        ["Marketing", "Growth", "GTM"]
    ), unsafe_allow_html=True)

# Security & Privacy
st.markdown('<h2 class="section-header">🔐 Security & Privacy</h2>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(create_resource_card(
        "🛡️",
        "AI Security Best Practices",
        "Protect AI systems from adversarial attacks, data poisoning, and model theft.",
        ["Security", "Defense", "Protection"],
        "https://owasp.org/www-project-machine-learning-security-top-10"
    ), unsafe_allow_html=True)
    
    st.markdown(create_resource_card(
        "🔒",
        "Privacy-Preserving AI",
        "Techniques for federated learning, differential privacy, and secure computation.",
        ["Privacy", "Federated", "Encryption"],
        "https://flower.dev"
    ), unsafe_allow_html=True)

with col2:
    st.markdown(create_resource_card(
        "🎭",
        "Prompt Injection Defense",
        "Learn to defend against prompt injection attacks and jailbreaking attempts.",
        ["Security", "Prompts", "Defense"]
    ), unsafe_allow_html=True)
    
    st.markdown(create_resource_card(
        "🔑",
        "API Security",
        "Secure your AI APIs with authentication, rate limiting, and monitoring.",
        ["API", "Auth", "Security"]
    ), unsafe_allow_html=True)

with col3:
    st.markdown(create_resource_card(
        "📜",
        "GDPR & AI Compliance",
        "Navigate data protection regulations when building AI systems in Europe.",
        ["GDPR", "Compliance", "Legal"]
    ), unsafe_allow_html=True)
    
    st.markdown(create_resource_card(
        "🔍",
        "Model Auditing",
        "Audit AI models for bias, fairness, and compliance with regulations.",
        ["Audit", "Fairness", "Bias"]
    ), unsafe_allow_html=True)

# Performance & Optimization
st.markdown('<h2 class="section-header">⚡ Performance & Optimization</h2>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(create_resource_card(
        "🚀",
        "Model Quantization",
        "Reduce model size and improve inference speed with quantization techniques.",
        ["Optimization", "Quantization", "Speed"],
        "https://github.com/pytorch/ao"
    ), unsafe_allow_html=True)
    
    st.markdown(create_resource_card(
        "⚡",
        "ONNX Runtime",
        "Cross-platform inference optimization for machine learning models.",
        ["Inference", "Performance", "Cross-platform"],
        "https://onnxruntime.ai"
    ), unsafe_allow_html=True)

with col2:
    st.markdown(create_resource_card(
        "🔧",
        "vLLM",
        "High-throughput and memory-efficient LLM inference and serving engine.",
        ["LLM", "Inference", "Serving"],
        "https://docs.vllm.ai"
    ), unsafe_allow_html=True)
    
    st.markdown(create_resource_card(
        "💾",
        "Model Compression",
        "Techniques for pruning, distillation, and compressing neural networks.",
        ["Compression", "Pruning", "Distillation"]
    ), unsafe_allow_html=True)

with col3:
    st.markdown(create_resource_card(
        "🎯",
        "Caching Strategies",
        "Implement intelligent caching for AI responses to reduce costs and latency.",
        ["Caching", "Performance", "Cost"]
    ), unsafe_allow_html=True)
    
    st.markdown(create_resource_card(
        "📊",
        "Profiling & Monitoring",
        "Profile AI applications and monitor performance in production.",
        ["Profiling", "Monitoring", "Observability"]
    ), unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    ### 🌱 Beginner Track
    - Python programming fundamentals
    - Introduction to AI & ML concepts
    - Understanding LLMs and APIs
    - Basic prompt engineering
    - Building your first AI agent
    - Simple RAG applications
    """)

with col2:
    st.markdown("""
    ### 📈 Intermediate Track
    - Advanced prompt techniques
    - Vector databases & embeddings
    - Agent architectures (ReAct, Chain-of-Thought)
    - API integration & webhooks
    - Performance optimization
    - Testing & evaluation strategies
    """)

with col3:
    st.markdown("""
    ### 🏆 Advanced Track
    - Multi-agent systems
    - Fine-tuning & customization
    - Enterprise deployment
    - Security & compliance
    - MLOps & monitoring
    - Research & innovation
    """)

# Call to Action
st.markdown("---")
st.markdown("""
<div style="text-align: center; margin: 3rem 0;">
    <a href="https://entremotivator.com" target="_blank" style="display: inline-block; background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%); color: #000000 !important; padding: 1rem 2rem; border-radius: 12px; text-decoration: none; font-weight: 600; font-family: 'Inter', sans-serif; transition: all 0.3s ease; box-shadow: 0 4px 12px rgba(245, 158, 11, 0.3); margin: 0.5rem; font-size: 1.1rem;">
        🚀 Explore More at Entremotivator.com
    </a>
</div>
""", unsafe_allow_html=True)

st.markdown("---")
st.markdown("*This comprehensive resource hub is part of the AI Agent Toolkit by D Hudson. Bookmark this page and return often for updates!*")
