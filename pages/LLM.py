import streamlit as st

# Page config
st.set_page_config(
    page_title="LLM Directory",
    page_icon="🤖",
    layout="wide"
)

# Custom CSS for card styling
st.markdown("""
    <style>
    /* Main container styling */
    .main {
        padding: 0 2rem;
    }
    
    /* Card styling */
    .llm-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 12px;
        margin-bottom: 1rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    .llm-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 24px rgba(0, 0, 0, 0.2);
    }
    .llm-card.open-source {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
    }
    .llm-card.local {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    }
    .llm-card.commercial {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
    }
    
    /* Text styling */
    .model-name {
        color: white;
        font-size: 1.5rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    .model-info {
        color: #f0f0f0;
        font-size: 0.95rem;
        line-height: 1.6;
        margin-bottom: 0.5rem;
    }
    
    /* Badge styling */
    .badge {
        background-color: rgba(255, 255, 255, 0.3);
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 15px;
        font-size: 0.8rem;
        display: inline-block;
        margin-right: 0.5rem;
        margin-bottom: 0.5rem;
    }
    .size-badge {
        background-color: rgba(255, 255, 255, 0.4);
        font-weight: bold;
    }
    
    /* Stats bar */
    .stats-bar {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .stat-item {
        text-align: center;
        color: white;
    }
    .stat-number {
        font-size: 2rem;
        font-weight: bold;
        color: #4facfe;
    }
    .stat-label {
        font-size: 0.9rem;
        color: #e0e0e0;
        margin-top: 0.25rem;
    }
    
    /* Settings panel styling */
    .settings-panel {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 12px;
        border: 2px solid #e9ecef;
        margin-bottom: 1.5rem;
    }
    
    /* Header styling */
    .header-section {
        text-align: center;
        padding: 2rem 0 1rem 0;
    }
    
    /* Category headers */
    .category-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        margin: 1.5rem 0 1rem 0;
        font-size: 1.3rem;
        font-weight: bold;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# Title and description
st.markdown('<div class="header-section">', unsafe_allow_html=True)
st.title("🤖 LLM Directory")
st.markdown("*A comprehensive directory of Large Language Models - Local, Cloud, and Open Source*")
st.markdown('</div>', unsafe_allow_html=True)

# LLM data
llm_directory = {
    "Open Source Models": [
        {"name": "Llama 3.2", "developer": "Meta", "sizes": "1B, 3B, 11B, 90B", "description": "Meta's latest open-source model family with multimodal capabilities.", "type": "open-source"},
        {"name": "Llama 3.1", "developer": "Meta", "sizes": "8B, 70B, 405B", "description": "Extended 128K context. The 405B is one of the largest open models.", "type": "open-source"},
        {"name": "Mistral 7B", "developer": "Mistral AI", "sizes": "7B", "description": "High-performance open-source model that outperforms Llama 2 13B.", "type": "open-source"},
        {"name": "Mixtral 8x7B", "developer": "Mistral AI", "sizes": "8x7B MoE (47B)", "description": "Mixture of Experts model with strong performance.", "type": "open-source"},
        {"name": "Phi-3", "developer": "Microsoft", "sizes": "3.8B, 7B, 14B", "description": "Small but powerful models optimized for efficiency.", "type": "open-source"},
        {"name": "Gemma 2", "developer": "Google", "sizes": "2B, 9B, 27B", "description": "Google's open-source models based on Gemini research.", "type": "open-source"},
        {"name": "Qwen 2.5", "developer": "Alibaba", "sizes": "0.5B-72B", "description": "Comprehensive family with excellent multilingual support.", "type": "open-source"},
        {"name": "Yi", "developer": "01.AI", "sizes": "6B, 9B, 34B", "description": "Bilingual (English/Chinese) open-source models.", "type": "open-source"},
    ],
    "Commercial Models": [
        {"name": "GPT-4o", "developer": "OpenAI", "sizes": "Undisclosed", "description": "Multimodal model with native vision, audio, and text capabilities.", "type": "commercial"},
        {"name": "Claude 3.5 Sonnet", "developer": "Anthropic", "sizes": "Undisclosed", "description": "Advanced model with 200K context window.", "type": "commercial"},
        {"name": "Gemini 1.5 Pro", "developer": "Google", "sizes": "Undisclosed", "description": "2M token context window. Exceptional for long documents.", "type": "commercial"},
        {"name": "GPT-4 Turbo", "developer": "OpenAI", "sizes": "Undisclosed", "description": "128K context with vision and function calling.", "type": "commercial"},
    ],
    "Code Specialists": [
        {"name": "CodeLlama", "developer": "Meta", "sizes": "7B, 13B, 34B, 70B", "description": "Specialized for code generation and understanding.", "type": "local"},
        {"name": "DeepSeek Coder", "developer": "DeepSeek", "sizes": "1.3B, 6.7B, 33B", "description": "High-performance code models.", "type": "local"},
        {"name": "StarCoder2", "developer": "BigCode", "sizes": "3B, 7B, 15B", "description": "Open-source code models trained on The Stack v2.", "type": "open-source"},
    ],
    "Specialized Local": [
        {"name": "Vicuna", "developer": "LMSYS", "sizes": "7B, 13B, 33B", "description": "Fine-tuned Llama for instruction following.", "type": "local"},
        {"name": "WizardLM", "developer": "Microsoft", "sizes": "7B, 13B, 70B", "description": "Enhanced instruction-following models.", "type": "local"},
        {"name": "Nous Hermes", "developer": "Nous Research", "sizes": "7B, 13B, 70B", "description": "Community-developed models focused on helpfulness.", "type": "local"},
    ],
}

# Collapsible settings panel
with st.expander("⚙️ Filters & Settings", expanded=False):
    st.markdown('<div class="settings-panel">', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🔍 Search")
        search_term = st.text_input(
            "Search models",
            placeholder="Search by name, developer, or description...",
            label_visibility="collapsed",
            key="search"
        )
        
        st.markdown("#### 📂 Category")
        categories = ["All Categories"] + list(llm_directory.keys())
        selected_category = st.selectbox(
            "Filter by category",
            categories,
            label_visibility="collapsed",
            key="category"
        )
    
    with col2:
        st.markdown("#### 🏷️ Type")
        type_filter = st.multiselect(
            "Filter by type",
            ["open-source", "local", "commercial"],
            default=[],
            label_visibility="collapsed",
            key="type"
        )
        
        st.markdown("#### 📊 Display")
        cols_count = st.select_slider(
            "Cards per row",
            options=[1, 2, 3],
            value=2,
            label_visibility="collapsed",
            key="cols"
        )
    
    # Legend
    st.markdown("---")
    st.markdown("**Legend:**")
    legend_col1, legend_col2, legend_col3 = st.columns(3)
    with legend_col1:
        st.markdown("🟢 **Open Source** - Free weights")
    with legend_col2:
        st.markdown("🔴 **Local Specialized** - Optimized local")
    with legend_col3:
        st.markdown("🔵 **Commercial** - API-based")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Calculate stats
total_models = sum(len(models) for models in llm_directory.values())
filtered_count = 0

for category, models in llm_directory.items():
    for model in models:
        search_match = (
            not search_term or
            search_term.lower() in model["name"].lower() or
            search_term.lower() in model["developer"].lower() or
            search_term.lower() in model["description"].lower()
        )
        category_match = selected_category == "All Categories" or selected_category == category
        type_match = not type_filter or model["type"] in type_filter
        
        if search_match and category_match and type_match:
            filtered_count += 1

# Stats bar
st.markdown(f"""
    <div class="stats-bar">
        <div style="display: flex; justify-content: space-around; align-items: center;">
            <div class="stat-item">
                <div class="stat-number">{total_models}</div>
                <div class="stat-label">Total Models</div>
            </div>
            <div class="stat-item">
                <div class="stat-number">{filtered_count}</div>
                <div class="stat-label">Showing</div>
            </div>
            <div class="stat-item">
                <div class="stat-number">{len(llm_directory)}</div>
                <div class="stat-label">Categories</div>
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

# Display LLM cards
for category, models in llm_directory.items():
    if selected_category != "All Categories" and selected_category != category:
        continue
    
    filtered_models = []
    for model in models:
        search_match = (
            not search_term or
            search_term.lower() in model["name"].lower() or
            search_term.lower() in model["developer"].lower() or
            search_term.lower() in model["description"].lower()
        )
        type_match = not type_filter or model["type"] in type_filter
        
        if search_match and type_match:
            filtered_models.append(model)
    
    if not filtered_models:
        continue
    
    st.markdown(f'<div class="category-header">📚 {category} ({len(filtered_models)} models)</div>', unsafe_allow_html=True)
    
    cols = st.columns(cols_count)
    
    for idx, model_data in enumerate(filtered_models):
        with cols[idx % cols_count]:
            type_class = model_data["type"]
            type_label = "🟢 Open Source" if type_class == "open-source" else "🔴 Local" if type_class == "local" else "🔵 Commercial"
            
            st.markdown(f"""
                <div class="llm-card {type_class}">
                    <div class="model-name">{model_data['name']}</div>
                    <div class="model-info">
                        <span class="badge">{type_label}</span>
                        <span class="badge">{model_data['developer']}</span>
                        <span class="badge size-badge">{model_data['sizes']}</span>
                    </div>
                    <div class="model-info">{model_data['description']}</div>
                </div>
            """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
    <div style="text-align: center; color: #666; padding: 2rem 0;">
        <p><strong>LLM Directory</strong> | Updated October 2024</p>
        <p style="font-size: 0.9rem;">Data compiled from official releases and community sources</p>
    </div>
""", unsafe_allow_html=True)
