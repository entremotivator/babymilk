import streamlit as st
import os
import base64
from datetime import datetime

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
            </style>
            """
    st.markdown(hide_st_style, unsafe_allow_html=True)

def apply_ai_toolkit_theme():
    """Apply AI Agent Toolkit theme"""
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
    .stMarkdown, .stText, p, span, div, .stSelectbox label, .stTextInput label {
        color: #ffffff !important;
        font-family: 'Inter', sans-serif;
    }
    
    h1, h2, h3, h4, h5, h6 {
        color: #f59e0b !important;
        font-weight: 600;
        font-family: 'Inter', sans-serif;
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
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background: rgba(30, 41, 59, 0.8);
        border: 1px solid #475569;
        border-radius: 12px;
        color: #ffffff !important;
        font-family: 'Inter', sans-serif;
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
        color: #fbbf24 !important;
    }
    
    /* Logo styling */
    .logo-container {
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 2rem 0;
    }
    
    .logo-container img {
        max-width: 200px;
        height: auto;
        filter: drop-shadow(0 8px 32px rgba(245, 158, 11, 0.3));
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
    
    /* Agent card styling */
    .agent-card {
        background: rgba(30, 41, 59, 0.8);
        border: 1px solid #475569;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        transition: all 0.3s ease;
    }
    
    .agent-card:hover {
        border-color: #f59e0b;
        box-shadow: 0 4px 20px rgba(245, 158, 11, 0.2);
        transform: translateY(-2px);
    }
    
    /* Use case card styling */
    .use-case-card {
        background: linear-gradient(135deg, rgba(245, 158, 11, 0.1) 0%, rgba(217, 119, 6, 0.1) 100%);
        border: 1px solid #f59e0b;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
    }
    
    /* Framework comparison table */
    .framework-table {
        background: rgba(30, 41, 59, 0.8);
        border-radius: 12px;
        border: 1px solid #475569;
        padding: 1rem;
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

# Apply styling and authentication check
hide_streamlit_style()
apply_ai_toolkit_theme()

st.set_page_config(page_title="AI Agents - AI Agent Toolkit", page_icon="🤖", layout="wide")

# Authentication check
if not st.session_state.get("authenticated", False):
    st.warning("🔒 Please sign in to access AI Agents.")
    st.stop()

# Display logo
display_logo()

# Header
st.title("🤖 AI Agents: The Complete Guide")
st.markdown("*Master the fundamentals, frameworks, and future of autonomous AI agents*")

# Horizontal menu
menu_col1, menu_col2, menu_col3, menu_col4, menu_col5 = st.columns(5)
with menu_col1:
    if st.button("🏠 Home", use_container_width=True):
        st.switch_page("main_app.py")
with menu_col2:
    if st.button("🛠️ AI Tools", use_container_width=True):
        st.switch_page("pages/02_🛠️_AI_Tools.py")
with menu_col3:
    if st.button("📚 Resources", use_container_width=True):
        st.switch_page("pages/03_📚_Resources.py")
with menu_col4:
    if st.button("🧠 Knowledge Base", use_container_width=True):
        st.switch_page("pages/04_🧠_AI_Knowledge_Base.py")
with menu_col5:
    if st.button("📦 GitHub Hub", use_container_width=True):
        st.switch_page("pages/07_📦_GitHub_Resources.py")

st.markdown("---")

# Main content tabs
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "🎯 Introduction", 
    "🏗️ Architecture", 
    "🔧 Frameworks", 
    "💼 Use Cases", 
    "🚀 Building Agents", 
    "📊 Evaluation", 
    "🔮 Future Trends"
])

with tab1:
    st.header("🎯 What Are AI Agents?")
    
    st.markdown("""
    ## Understanding AI Agents
    
    **AI Agents** are autonomous software entities that can perceive their environment, make decisions, and take actions to achieve specific goals. Unlike traditional software that follows predetermined instructions, AI agents can adapt, learn, and operate independently with minimal human intervention.
    
    ### Key Characteristics of AI Agents
    
    AI agents possess several fundamental characteristics that distinguish them from conventional software:
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        #### 🧠 **Autonomy**
        - Operate independently without constant human supervision
        - Make decisions based on their programming and learned experiences
        - Adapt to changing environments and circumstances
        - Self-manage their resources and priorities
        
        #### 🎯 **Goal-Oriented Behavior**
        - Designed with specific objectives or missions
        - Can break down complex goals into manageable tasks
        - Prioritize actions based on goal importance
        - Measure progress and adjust strategies accordingly
        
        #### 🔄 **Reactivity**
        - Respond to changes in their environment in real-time
        - Process new information and update their understanding
        - Adapt behavior based on environmental feedback
        - Handle unexpected situations gracefully
        """)
    
    with col2:
        st.markdown("""
        #### 🤝 **Social Ability**
        - Interact with other agents, systems, and humans
        - Communicate through various protocols and interfaces
        - Collaborate to achieve shared objectives
        - Negotiate and coordinate with multiple stakeholders
        
        #### 📚 **Learning Capability**
        - Improve performance through experience
        - Adapt to new situations and environments
        - Update knowledge base with new information
        - Optimize strategies based on outcomes
        
        #### 🔍 **Perception**
        - Gather information from their environment
        - Process multiple data sources simultaneously
        - Filter relevant information from noise
        - Maintain situational awareness
        """)
    
    st.markdown("---")
    
    st.subheader("🏛️ Historical Evolution of AI Agents")
    
    st.markdown("""
    The concept of AI agents has evolved significantly over the decades, building upon advances in artificial intelligence, computer science, and cognitive psychology.
    """)
    
    with st.expander("📅 Timeline of AI Agent Development"):
        st.markdown("""
        **1950s-1960s: Foundational Concepts**
        - Alan Turing's work on machine intelligence
        - Early cybernetics and control theory
        - First autonomous systems in robotics
        
        **1970s-1980s: Expert Systems Era**
        - Rule-based expert systems
        - Knowledge representation frameworks
        - Early decision support systems
        
        **1990s: Multi-Agent Systems**
        - Distributed artificial intelligence
        - Agent communication languages
        - Coordination and negotiation protocols
        
        **2000s: Internet and Web Agents**
        - Web crawlers and search agents
        - E-commerce recommendation systems
        - Personal digital assistants
        
        **2010s: Machine Learning Integration**
        - Deep learning breakthroughs
        - Reinforcement learning agents
        - Natural language processing advances
        
        **2020s: Large Language Model Agents**
        - GPT-based conversational agents
        - Multi-modal AI systems
        - Autonomous code generation
        """)
    
    st.markdown("---")
    
    st.subheader("🔬 Types of AI Agents")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="agent-card">', unsafe_allow_html=True)
        st.markdown("""
        ### 🎭 **Reactive Agents**
        
        **Characteristics:**
        - Respond directly to environmental stimuli
        - No internal state or memory
        - Fast response times
        - Simple rule-based behavior
        
        **Examples:**
        - Thermostat controllers
        - Basic chatbots
        - Simple game AI
        - Reflex-based robots
        
        **Advantages:**
        - Simple to implement
        - Predictable behavior
        - Low computational requirements
        - Real-time responsiveness
        
        **Limitations:**
        - Cannot learn from experience
        - Limited problem-solving capability
        - No planning or foresight
        """)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="agent-card">', unsafe_allow_html=True)
        st.markdown("""
        ### 🎯 **Goal-Based Agents**
        
        **Characteristics:**
        - Maintain explicit goals
        - Plan sequences of actions
        - Evaluate action outcomes
        - Adapt strategies to achieve objectives
        
        **Examples:**
        - GPS navigation systems
        - Project management tools
        - Strategic game AI
        - Automated trading systems
        
        **Advantages:**
        - Flexible problem-solving
        - Can handle complex objectives
        - Strategic thinking capability
        - Adaptable to new goals
        
        **Limitations:**
        - Higher computational complexity
        - May struggle with conflicting goals
        - Requires goal specification
        """)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="agent-card">', unsafe_allow_html=True)
        st.markdown("""
        ### 🧠 **Learning Agents**
        
        **Characteristics:**
        - Improve performance over time
        - Adapt to new environments
        - Update knowledge and strategies
        - Self-optimize behavior
        
        **Examples:**
        - Recommendation systems
        - Adaptive user interfaces
        - Personalized assistants
        - Autonomous vehicles
        
        **Advantages:**
        - Continuous improvement
        - Personalization capability
        - Handles novel situations
        - Long-term optimization
        
        **Limitations:**
        - Requires training data
        - May develop biases
        - Complex to debug
        """)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="agent-card">', unsafe_allow_html=True)
        st.markdown("""
        ### 🤖 **Utility-Based Agents**
        
        **Characteristics:**
        - Maximize utility functions
        - Make trade-offs between competing objectives
        - Quantify preferences and outcomes
        - Optimize for overall satisfaction
        
        **Examples:**
        - Resource allocation systems
        - Portfolio management tools
        - Supply chain optimization
        - Multi-objective planners
        
        **Advantages:**
        - Handles complex trade-offs
        - Quantifiable decision-making
        - Optimal resource utilization
        - Flexible objective functions
        
        **Limitations:**
        - Requires utility function design
        - Computational complexity
        - May be difficult to interpret
        """)
        st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.header("🏗️ AI Agent Architecture")
    
    st.markdown("""
    ## Understanding Agent Architecture
    
    The architecture of an AI agent defines how its components interact to perceive the environment, process information, make decisions, and execute actions. A well-designed architecture is crucial for creating effective and reliable AI agents.
    """)
    
    st.subheader("🔧 Core Components")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 👁️ **Perception Module**
        
        The perception module is responsible for gathering and processing information from the agent's environment.
        
        **Key Functions:**
        - **Sensor Integration**: Collect data from various input sources
        - **Data Preprocessing**: Clean and normalize incoming data
        - **Feature Extraction**: Identify relevant patterns and characteristics
        - **State Representation**: Convert raw data into usable internal representations
        
        **Technologies Used:**
        - Computer vision algorithms
        - Natural language processing
        - Audio signal processing
        - Sensor fusion techniques
        - Real-time data streaming
        
        **Challenges:**
        - Noisy or incomplete data
        - Real-time processing requirements
        - Multi-modal data integration
        - Scalability and performance
        """)
        
        st.markdown("""
        ### 🧠 **Knowledge Base**
        
        The knowledge base stores and organizes the agent's understanding of the world.
        
        **Components:**
        - **Factual Knowledge**: Static information about the domain
        - **Procedural Knowledge**: How to perform specific tasks
        - **Experiential Knowledge**: Learned patterns from past interactions
        - **Meta-Knowledge**: Knowledge about knowledge itself
        
        **Representation Methods:**
        - Semantic networks and ontologies
        - Rule-based systems
        - Neural network embeddings
        - Graph databases
        - Vector stores and embeddings
        """)
    
    with col2:
        st.markdown("""
        ### ⚙️ **Reasoning Engine**
        
        The reasoning engine processes information and makes decisions based on available knowledge.
        
        **Reasoning Types:**
        - **Deductive Reasoning**: Drawing logical conclusions from premises
        - **Inductive Reasoning**: Generalizing from specific observations
        - **Abductive Reasoning**: Finding the best explanation for observations
        - **Analogical Reasoning**: Using similarities to solve new problems
        
        **Implementation Approaches:**
        - Logic programming (Prolog, Answer Set Programming)
        - Probabilistic reasoning (Bayesian networks)
        - Machine learning models
        - Hybrid symbolic-neural systems
        
        **Decision-Making Strategies:**
        - Utility maximization
        - Satisficing approaches
        - Multi-criteria decision analysis
        - Game-theoretic strategies
        """)
        
        st.markdown("""
        ### 🎬 **Action Module**
        
        The action module executes the agent's decisions in the environment.
        
        **Action Types:**
        - **Physical Actions**: Manipulating objects or moving in space
        - **Communication Actions**: Sending messages or signals
        - **Computational Actions**: Processing data or updating knowledge
        - **Social Actions**: Interacting with other agents or humans
        
        **Execution Considerations:**
        - Action planning and sequencing
        - Resource allocation and constraints
        - Error handling and recovery
        - Feedback and monitoring
        """)

with tab3:
    st.header("🔧 AI Agent Frameworks")
    
    st.markdown("""
    ## Popular AI Agent Frameworks
    
    The landscape of AI agent frameworks has evolved rapidly, offering developers powerful tools to build sophisticated autonomous systems. Each framework has its strengths, use cases, and architectural approaches.
    """)
    
    st.subheader("🦜 LangChain & LangGraph")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 🔗 **LangChain Overview**
        
        LangChain is a comprehensive framework for developing applications powered by language models, with strong support for agent-based architectures.
        
        **Key Features:**
        - **Modular Components**: Chains, agents, tools, and memory
        - **LLM Integration**: Support for multiple language model providers
        - **Tool Ecosystem**: Extensive library of pre-built tools
        - **Memory Management**: Persistent and session-based memory
        - **Prompt Engineering**: Template system for prompt management
        
        **Core Components:**
        - **Chains**: Sequences of calls to LLMs or other utilities
        - **Agents**: Entities that use LLMs to decide actions
        - **Tools**: Functions that agents can use to interact with the world
        - **Memory**: Systems to persist state between calls
        - **Callbacks**: Hooks for logging, monitoring, and streaming
        """)
    
    with col2:
        st.markdown("""
        ### 📊 **LangGraph Features**
        
        LangGraph extends LangChain with graph-based agent orchestration capabilities.
        
        **Advanced Capabilities:**
        - **State Management**: Persistent state across agent interactions
        - **Conditional Logic**: Complex decision trees and workflows
        - **Human-in-the-Loop**: Integration points for human oversight
        - **Parallel Execution**: Concurrent agent operations
        - **Error Handling**: Robust error recovery mechanisms
        
        **Use Cases:**
        - Multi-step reasoning tasks
        - Complex workflow automation
        - Interactive agent systems
        - Research and analysis pipelines
        - Customer service automation
        """)

with tab4:
    st.header("💼 AI Agent Use Cases")
    
    st.markdown("""
    ## Real-World Applications of AI Agents
    
    AI agents are transforming industries and creating new possibilities across virtually every sector of the economy. From automating routine tasks to solving complex problems, these intelligent systems are becoming indispensable tools for modern organizations.
    """)
    
    st.subheader("🏢 Business and Enterprise")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="use-case-card">', unsafe_allow_html=True)
        st.markdown("""
        ### 📞 **Customer Service Automation**
        
        **Applications:**
        - 24/7 customer support chatbots
        - Intelligent ticket routing and prioritization
        - Automated response generation
        - Sentiment analysis and escalation
        - Multi-language customer support
        
        **Benefits:**
        - Reduced response times
        - Consistent service quality
        - Cost savings on support staff
        - Improved customer satisfaction
        - Scalable support operations
        
        **Implementation Example:**
        A major e-commerce company deployed AI agents that handle 80% of customer inquiries automatically, reducing average response time from 24 hours to 2 minutes while maintaining 95% customer satisfaction scores.
        """)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="use-case-card">', unsafe_allow_html=True)
        st.markdown("""
        ### 📊 **Business Process Automation**
        
        **Applications:**
        - Invoice processing and approval workflows
        - Contract analysis and review
        - Compliance monitoring and reporting
        - Data entry and validation
        - Report generation and distribution
        
        **Benefits:**
        - Reduced manual errors
        - Faster processing times
        - Improved compliance
        - Cost reduction
        - Employee focus on high-value tasks
        
        **Implementation Example:**
        A financial services firm uses AI agents to process loan applications, reducing approval time from 5 days to 2 hours while improving accuracy by 40%.
        """)
        st.markdown('</div>', unsafe_allow_html=True)

with tab5:
    st.header("🚀 Building AI Agents")
    
    st.markdown("""
    ## Step-by-Step Guide to Building AI Agents
    
    Creating effective AI agents requires careful planning, thoughtful design, and systematic implementation. This comprehensive guide will walk you through the entire process from conception to deployment.
    """)
    
    st.subheader("📋 Phase 1: Planning and Design")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 🎯 **Define Objectives and Requirements**
        
        **Goal Definition:**
        - Clearly articulate what the agent should accomplish
        - Define success metrics and KPIs
        - Identify target users and stakeholders
        - Establish scope and boundaries
        
        **Functional Requirements:**
        - List specific capabilities and features
        - Define input and output specifications
        - Identify integration requirements
        - Specify performance criteria
        
        **Non-Functional Requirements:**
        - Scalability and performance needs
        - Security and privacy requirements
        - Reliability and availability targets
        - Usability and accessibility standards
        """)
    
    with col2:
        st.markdown("""
        ### 🏗️ **Architecture Design**
        
        **System Architecture:**
        - Choose appropriate architectural pattern
        - Define component interactions
        - Plan data flow and storage
        - Design communication protocols
        
        **Agent Architecture:**
        - Select agent type and capabilities
        - Design reasoning and decision-making logic
        - Plan knowledge representation
        - Define learning mechanisms
        
        **Technology Stack:**
        - Choose programming languages and frameworks
        - Select AI/ML libraries and models
        - Plan infrastructure and deployment
        - Consider monitoring and maintenance tools
        """)

with tab6:
    st.header("📊 AI Agent Evaluation")
    
    st.markdown("""
    ## Comprehensive Evaluation Framework
    
    Evaluating AI agents requires a multi-dimensional approach that considers performance, quality, reliability, and business impact. This section provides a comprehensive framework for assessing agent effectiveness.
    """)
    
    st.subheader("🎯 Evaluation Dimensions")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### ⚡ **Performance Metrics**
        
        **Response Time:**
        - Average response latency
        - 95th percentile response time
        - Peak load performance
        - Time-to-first-response
        
        **Throughput:**
        - Requests per second
        - Concurrent user capacity
        - Transaction processing rate
        - Batch processing speed
        
        **Resource Utilization:**
        - CPU and memory usage
        - Network bandwidth consumption
        - Storage requirements
        - Energy efficiency
        """)
    
    with col2:
        st.markdown("""
        ### 🎯 **Accuracy and Quality**
        
        **Task Completion:**
        - Success rate for assigned tasks
        - Partial completion analysis
        - Error categorization
        - Recovery success rate
        
        **Response Quality:**
        - Relevance to user queries
        - Factual accuracy
        - Completeness of responses
        - Coherence and clarity
        
        **Consistency:**
        - Response consistency across sessions
        - Behavior predictability
        - Output format standardization
        - Cross-platform consistency
        """)

with tab7:
    st.header("🔮 Future Trends in AI Agents")
    
    st.markdown("""
    ## The Evolution of AI Agents
    
    The field of AI agents is rapidly evolving, driven by advances in machine learning, computing infrastructure, and our understanding of intelligence itself. This section explores the emerging trends and future directions that will shape the next generation of AI agents.
    """)
    
    st.subheader("🚀 Technological Advances")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 🧠 **Advanced AI Architectures**
        
        **Multimodal Foundation Models:**
        - Integration of text, vision, audio, and sensor data
        - Unified understanding across modalities
        - Cross-modal reasoning capabilities
        - Enhanced real-world interaction
        
        **Neuro-Symbolic AI:**
        - Combination of neural networks and symbolic reasoning
        - Explainable decision-making processes
        - Robust logical reasoning
        - Knowledge graph integration
        
        **Transformer Innovations:**
        - Longer context windows (1M+ tokens)
        - More efficient attention mechanisms
        - Specialized architectures for different tasks
        - Reduced computational requirements
        """)
    
    with col2:
        st.markdown("""
        ### 🔧 **Infrastructure Evolution**
        
        **Edge AI Computing:**
        - Local processing capabilities
        - Reduced latency and bandwidth
        - Enhanced privacy and security
        - Offline operation support
        
        **Distributed Agent Networks:**
        - Peer-to-peer agent communication
        - Decentralized decision-making
        - Resilient system architectures
        - Blockchain integration
        
        **Neuromorphic Computing:**
        - Brain-inspired hardware architectures
        - Ultra-low power consumption
        - Real-time learning capabilities
        - Adaptive processing systems
        """)

# Footer with navigation
st.markdown("---")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🛠️ AI Tools", use_container_width=True):
        st.switch_page("pages/02_🛠️_AI_Tools.py")

with col2:
    if st.button("📚 Resources", use_container_width=True):
        st.switch_page("pages/03_📚_Resources.py")

with col3:
    if st.button("🏠 Back to Home", use_container_width=True):
        st.switch_page("main_app.py")

# Sidebar with quick navigation
with st.sidebar:
    st.markdown("### 🧭 Quick Navigation")
    
    if st.button("🎯 Introduction", use_container_width=True):
        st.rerun()
    
    if st.button("🏗️ Architecture", use_container_width=True):
        st.rerun()
    
    if st.button("🔧 Frameworks", use_container_width=True):
        st.rerun()
    
    if st.button("💼 Use Cases", use_container_width=True):
        st.rerun()
    
    if st.button("🚀 Building Agents", use_container_width=True):
        st.rerun()
    
    if st.button("📊 Evaluation", use_container_width=True):
        st.rerun()
    
    if st.button("🔮 Future Trends", use_container_width=True):
        st.rerun()
    
    st.markdown("### 🔗 External Resources")
    st.markdown("""
    <div style="margin: 1rem 0;">
        <a href="https://entremotivator.com" target="_blank" class="resource-link">
            🚀 Visit Entremotivator.com
        </a>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    - [LangChain Documentation](https://docs.langchain.com/)
    - [CrewAI GitHub](https://github.com/joaomdmoura/crewAI)
    - [Microsoft AutoGen](https://github.com/microsoft/autogen)
    - [AI Agent Research Papers](https://arxiv.org/list/cs.AI/recent)
    """)

st.markdown("---")
st.markdown("*This page is part of the AI Agent Toolkit by D Hudson. Master the art of building intelligent, autonomous AI agents.*")
