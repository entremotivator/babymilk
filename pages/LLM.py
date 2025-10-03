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
    "Open Source (Local-Capable)": [
        {"name": "Llama 3.2", "developer": "Meta", "sizes": "1B, 3B, 11B, 90B", "description": "Meta's latest open-source model family with multimodal capabilities. Can run locally on consumer hardware.", "type": "open-source"},
        {"name": "Llama 3.1", "developer": "Meta", "sizes": "8B, 70B, 405B", "description": "Previous generation with extended 128K context. The 405B is one of the largest open models available.", "type": "open-source"},
        {"name": "Llama 2", "developer": "Meta", "sizes": "7B, 13B, 70B", "description": "Widely used foundation models. Great for fine-tuning and local deployment.", "type": "open-source"},
        {"name": "Mistral 7B", "developer": "Mistral AI", "sizes": "7B", "description": "High-performance open-source model that outperforms Llama 2 13B. Excellent for local deployment.", "type": "open-source"},
        {"name": "Mixtral 8x7B", "developer": "Mistral AI", "sizes": "8x7B MoE (47B)", "description": "Mixture of Experts model with strong performance. Can run locally with sufficient VRAM.", "type": "open-source"},
        {"name": "Mixtral 8x22B", "developer": "Mistral AI", "sizes": "8x22B MoE (141B)", "description": "Larger MoE model with enhanced capabilities. Competitive with proprietary models.", "type": "open-source"},
        {"name": "Phi-3", "developer": "Microsoft", "sizes": "3.8B, 7B, 14B", "description": "Small but powerful models optimized for efficiency. Perfect for local deployment on laptops.", "type": "open-source"},
        {"name": "Phi-2", "developer": "Microsoft", "sizes": "2.7B", "description": "Tiny but capable model that runs on almost any hardware. Great for resource-constrained environments.", "type": "open-source"},
        {"name": "Gemma 2", "developer": "Google", "sizes": "2B, 9B, 27B", "description": "Google's open-source models based on Gemini research. Optimized for various hardware configurations.", "type": "open-source"},
        {"name": "Gemma", "developer": "Google", "sizes": "2B, 7B", "description": "First generation Gemma models. Lightweight and efficient for edge deployment.", "type": "open-source"},
        {"name": "Falcon", "developer": "TII (UAE)", "sizes": "7B, 40B, 180B", "description": "High-quality open-source models trained on web data. Strong multilingual capabilities.", "type": "open-source"},
        {"name": "Yi", "developer": "01.AI", "sizes": "6B, 9B, 34B", "description": "Bilingual (English/Chinese) open-source models with strong performance. Local-friendly.", "type": "open-source"},
        {"name": "Qwen 2.5", "developer": "Alibaba", "sizes": "0.5B, 1.5B, 3B, 7B, 14B, 32B, 72B", "description": "Comprehensive model family with excellent multilingual support. Wide range of sizes.", "type": "open-source"},
        {"name": "Qwen 2", "developer": "Alibaba", "sizes": "0.5B, 1.5B, 7B, 72B", "description": "Previous generation with strong coding and math capabilities. Still widely used.", "type": "open-source"},
        {"name": "StableLM 2", "developer": "Stability AI", "sizes": "1.6B, 12B", "description": "Efficient models trained on diverse datasets. Good for chat and instruction following.", "type": "open-source"},
        {"name": "OpenHermes 2.5", "developer": "Teknium", "sizes": "7B, 13B", "description": "Fine-tuned Mistral models with enhanced instruction following. Popular in the community.", "type": "open-source"},
        {"name": "Solar", "developer": "Upstage", "sizes": "10.7B", "description": "Depth-upscaled model with strong performance. Unique architecture approach.", "type": "open-source"},
        {"name": "Zephyr", "developer": "HuggingFace", "sizes": "7B", "description": "Aligned version of Mistral using DPO. Excellent for chatbot applications.", "type": "open-source"},
        {"name": "StarCoder2", "developer": "BigCode", "sizes": "3B, 7B, 15B", "description": "Open-source code models trained on The Stack v2. Strong programming capabilities.", "type": "open-source"},
        {"name": "BLOOM", "developer": "BigScience", "sizes": "560M, 1.1B, 3B, 7.1B, 176B", "description": "Multilingual model covering 46 languages. Community-driven research project.", "type": "open-source"},
        {"name": "OLMo", "developer": "AI2", "sizes": "1B, 7B", "description": "Fully open model with training data, code, and weights. Complete transparency.", "type": "open-source"},
        {"name": "Amber", "developer": "LLM360", "sizes": "7B", "description": "Fully open LLM with all training checkpoints released. Educational focus.", "type": "open-source"},
    ],
    "Specialized Local Models": [
        {"name": "CodeLlama", "developer": "Meta", "sizes": "7B, 13B, 34B, 70B", "description": "Specialized for code generation and understanding. Based on Llama 2.", "type": "local"},
        {"name": "Deepseek Coder", "developer": "DeepSeek", "sizes": "1.3B, 6.7B, 33B", "description": "High-performance code models that rival larger models. Excellent for local development.", "type": "local"},
        {"name": "WizardCoder", "developer": "WizardLM Team", "sizes": "7B, 13B, 15B, 34B", "description": "Code-specialized models with Evol-Instruct training. Strong at complex programming.", "type": "local"},
        {"name": "Phind CodeLlama", "developer": "Phind", "sizes": "34B", "description": "Fine-tuned CodeLlama for technical search and coding. Optimized for developers.", "type": "local"},
        {"name": "Orca 2", "developer": "Microsoft", "sizes": "7B, 13B", "description": "Reasoning-focused models trained with synthetic data. Strong performance on smaller sizes.", "type": "local"},
        {"name": "Vicuna", "developer": "LMSYS", "sizes": "7B, 13B, 33B", "description": "Fine-tuned Llama models optimized for instruction following. Popular for chatbots.", "type": "local"},
        {"name": "WizardLM", "developer": "Microsoft", "sizes": "7B, 13B, 70B", "description": "Enhanced instruction-following models. Good balance of performance and resources.", "type": "local"},
        {"name": "Nous Hermes", "developer": "Nous Research", "sizes": "7B, 13B, 70B", "description": "Community-developed models focused on helpfulness and coherence.", "type": "local"},
        {"name": "Airoboros", "developer": "Jon Durbin", "sizes": "7B, 13B, 70B", "description": "Creative writing and roleplaying specialist. Uses synthetic training data.", "type": "local"},
        {"name": "Goliath", "developer": "AlpineDale", "sizes": "120B", "description": "Frankenmerge of two 70B models. Strong creative and reasoning capabilities.", "type": "local"},
        {"name": "Dolphin", "developer": "Eric Hartford", "sizes": "7B, 13B, 70B, 72B", "description": "Uncensored models based on various foundations. Used for research.", "type": "local"},
        {"name": "OpenChat", "developer": "OpenChat Team", "sizes": "7B, 13B", "description": "Open-source chatbot models with C-RLFT training. Efficient and capable.", "type": "local"},
        {"name": "Samantha", "developer": "Eric Hartford", "sizes": "7B, 13B, 70B", "description": "Companion-style conversational models. Empathetic and engaging.", "type": "local"},
        {"name": "MythoMax", "developer": "Gryphe", "sizes": "13B", "description": "Merge optimized for creative writing and storytelling. Popular for fiction.", "type": "local"},
        {"name": "Nous Capybara", "developer": "Nous Research", "sizes": "7B, 34B", "description": "RLHF-trained models with diverse capabilities. Strong multi-turn conversations.", "type": "local"},
        {"name": "Guanaco", "developer": "Tim Dettmers", "sizes": "7B, 13B, 33B, 65B", "description": "QLoRA fine-tuned models. Efficient training with strong results.", "type": "local"},
    ],
    "Commercial/API-Based Models": [
        {"name": "GPT-4 Turbo", "developer": "OpenAI", "sizes": "Undisclosed (est. 1.7T+)", "description": "OpenAI's most capable model with vision, function calling, and 128K context.", "type": "commercial"},
        {"name": "GPT-4o", "developer": "OpenAI", "sizes": "Undisclosed", "description": "Multimodal model with native vision, audio, and text. Faster than GPT-4.", "type": "commercial"},
        {"name": "GPT-4o mini", "developer": "OpenAI", "sizes": "Undisclosed", "description": "Smaller, faster, cheaper version of GPT-4o. Great for high-volume applications.", "type": "commercial"},
        {"name": "GPT-4", "developer": "OpenAI", "sizes": "Undisclosed (est. 1.7T+)", "description": "Original GPT-4 with strong reasoning. 8K and 32K context versions.", "type": "commercial"},
        {"name": "GPT-3.5 Turbo", "developer": "OpenAI", "sizes": "Undisclosed", "description": "Fast and cost-effective model for most tasks. 16K context window.", "type": "commercial"},
        {"name": "Claude 3.5 Sonnet", "developer": "Anthropic", "sizes": "Undisclosed", "description": "Advanced model with 200K context. Excels at analysis, coding, long-form content.", "type": "commercial"},
        {"name": "Claude 3 Opus", "developer": "Anthropic", "sizes": "Undisclosed", "description": "Anthropic's most capable model for complex tasks. Strong reasoning.", "type": "commercial"},
        {"name": "Claude 3 Sonnet", "developer": "Anthropic", "sizes": "Undisclosed", "description": "Balanced model for everyday tasks. Good speed and capability trade-off.", "type": "commercial"},
        {"name": "Claude 3 Haiku", "developer": "Anthropic", "sizes": "Undisclosed", "description": "Fastest and most compact Claude model. Ideal for high-throughput apps.", "type": "commercial"},
        {"name": "Gemini 1.5 Pro", "developer": "Google", "sizes": "Undisclosed", "description": "Multimodal model with 2M token context. Exceptional for long documents.", "type": "commercial"},
        {"name": "Gemini 1.5 Flash", "developer": "Google", "sizes": "Undisclosed", "description": "Fast and efficient model for high-frequency tasks. Good balance.", "type": "commercial"},
        {"name": "Gemini Ultra", "developer": "Google", "sizes": "Undisclosed", "description": "Google's most capable model, competitive with GPT-4. Multimodal.", "type": "commercial"},
        {"name": "Gemini Pro", "developer": "Google", "sizes": "Undisclosed", "description": "Versatile model for various tasks. Powers Bard and Google AI services.", "type": "commercial"},
        {"name": "PaLM 2", "developer": "Google", "sizes": "Multiple (Gecko-Unicorn)", "description": "Powers Google services. Strong multilingual and reasoning.", "type": "commercial"},
        {"name": "Cohere Command R+", "developer": "Cohere", "sizes": "104B", "description": "Enterprise-focused with RAG optimization and multilingual support.", "type": "commercial"},
        {"name": "Cohere Command R", "developer": "Cohere", "sizes": "35B", "description": "Efficient model optimized for retrieval-augmented generation.", "type": "commercial"},
        {"name": "Claude 2.1", "developer": "Anthropic", "sizes": "Undisclosed", "description": "Previous generation with 200K context. Still used for long documents.", "type": "commercial"},
        {"name": "Perplexity 70B", "developer": "Perplexity AI", "sizes": "70B", "description": "Search-focused combining LLM with real-time web search.", "type": "commercial"},
        {"name": "AI21 Jurassic-2", "developer": "AI21 Labs", "sizes": "Multiple sizes", "description": "Enterprise-grade models with strong language understanding.", "type": "commercial"},
    ],
    "Hybrid (Open + API)": [
        {"name": "Mistral Large", "developer": "Mistral AI", "sizes": "Undisclosed", "description": "High-performance model available via API. Company provides open alternatives.", "type": "commercial"},
        {"name": "DeepSeek V2", "developer": "DeepSeek", "sizes": "236B MoE", "description": "MoE model available as open weights and via API. Cost-effective.", "type": "open-source"},
        {"name": "Llama 3.1 405B", "developer": "Meta", "sizes": "405B", "description": "Meta's largest open model. Available for download or via cloud.", "type": "open-source"},
        {"name": "Yi-Large", "developer": "01.AI", "sizes": "Undisclosed", "description": "Proprietary version via API. Strong bilingual capabilities.", "type": "commercial"},
        {"name": "Grok-1", "developer": "xAI", "sizes": "314B MoE", "description": "Elon Musk's AI with open weights. Trained on X/Twitter data.", "type": "open-source"},
    ],
    "Tiny/Edge Models": [
        {"name": "TinyLlama", "developer": "TinyLlama Team", "sizes": "1.1B", "description": "Compact model trained on 3T tokens. Runs on phones and embedded devices.", "type": "open-source"},
        {"name": "MobileLLM", "developer": "Meta", "sizes": "125M, 350M", "description": "Designed for mobile devices. Extreme efficiency focus.", "type": "open-source"},
        {"name": "Phi-1.5", "developer": "Microsoft", "sizes": "1.3B", "description": "Tiny but capable for code and reasoning. Can run on CPU.", "type": "open-source"},
        {"name": "SmolLM", "developer": "HuggingFace", "sizes": "135M, 360M, 1.7B", "description": "Small language models for on-device applications. Extremely efficient.", "type": "open-source"},
        {"name": "H2O-Danube", "developer": "H2O.ai", "sizes": "1.8B", "description": "Small but powerful multilingual. Edge deployment optimized.", "type": "open-source"},
    ],
    "Multimodal Models": [
        {"name": "LLaVA", "developer": "Microsoft/UW", "sizes": "7B, 13B, 34B", "description": "Vision-language model combining CLIP and Llama. Strong image understanding.", "type": "open-source"},
        {"name": "LLaVA-NeXT", "developer": "Microsoft/UW", "sizes": "7B, 13B, 34B", "description": "Improved version with better visual reasoning. Enhanced OCR.", "type": "open-source"},
        {"name": "CogVLM", "developer": "Tsinghua University", "sizes": "17B", "description": "Visual language model with attention mechanism. Strong at VQA.", "type": "open-source"},
        {"name": "Qwen-VL", "developer": "Alibaba", "sizes": "7B", "description": "Multimodal model with vision capabilities. Multilingual support.", "type": "open-source"},
        {"name": "Yi-VL", "developer": "01.AI", "sizes": "6B, 34B", "description": "Bilingual vision-language models. Strong performance on visual tasks.", "type": "open-source"},
    ],
    "Math & Reasoning": [
        {"name": "WizardMath", "developer": "WizardLM Team", "sizes": "7B, 13B, 70B", "description": "Specialized for mathematical reasoning. Strong on MATH benchmark.", "type": "local"},
        {"name": "MetaMath", "developer": "Meta/Community", "sizes": "7B, 13B, 70B", "description": "Fine-tuned for math problem solving. Excellent step-by-step reasoning.", "type": "local"},
        {"name": "Llemma", "developer": "EleutherAI", "sizes": "7B, 34B", "description": "Specialized for formal mathematics and theorem proving.", "type": "open-source"},
        {"name": "DeepSeek Math", "developer": "DeepSeek", "sizes": "7B", "description": "Mathematics-focused with strong problem-solving abilities.", "type": "open-source"},
    ],
    "Chinese Models": [
        {"name": "ChatGLM3", "developer": "Tsinghua University", "sizes": "6B", "description": "Latest bilingual conversational model. Enhanced capabilities and tool use.", "type": "open-source"},
        {"name": "Baichuan2", "developer": "Baichuan AI", "sizes": "7B, 13B", "description": "Improved training with better performance on Chinese benchmarks.", "type": "open-source"},
        {"name": "InternLM2", "developer": "Shanghai AI Lab", "sizes": "7B, 20B", "description": "Enhanced version with 200K context and improved capabilities.", "type": "open-source"},
        {"name": "TigerBot", "developer": "TigerBot", "sizes": "7B, 13B, 70B", "description": "Chinese-centric models with strong instruction following.", "type": "open-source"},
    ],
    "Multilingual Models": [
        {"name": "XGLM", "developer": "Meta", "sizes": "564M-7.5B", "description": "Multilingual model covering 30+ languages. Good for cross-lingual tasks.", "type": "open-source"},
        {"name": "Aya", "developer": "Cohere For AI", "sizes": "8B, 35B", "description": "Massively multilingual model covering 101 languages.", "type": "open-source"},
        {"name": "PolyLM", "developer": "DAMO Academy", "sizes": "1.7B, 13B", "description": "Multilingual model with 18 languages. Balanced coverage.", "type": "open-source"},
    ],
    "Research Models": [
        {"name": "GPT-J", "developer": "EleutherAI", "sizes": "6B", "description": "Open-source GPT alternative. Important for research and experimentation.", "type": "open-source"},
        {"name": "GPT-NeoX", "developer": "EleutherAI", "sizes": "20B", "description": "Larger open-source model. Trained on The Pile dataset.", "type": "open-source"},
        {"name": "Pythia", "developer": "EleutherAI", "sizes": "70M-12B", "description": "Suite of models for research on training dynamics. All checkpoints released.", "type": "open-source"},
        {"name": "OPT", "developer": "Meta", "sizes": "125M-175B", "description": "Open Pre-trained Transformers. Research-focused model family.", "type": "open-source"},
        {"name": "MPT", "developer": "MosaicML", "sizes": "7B, 30B", "description": "MosaicML Pretrained Transformer. Optimized for commercial use.", "type": "open-source"},
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
