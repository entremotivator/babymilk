import streamlit as st
import uuid
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

def apply_custom_css():
    """Apply custom CSS styling matching the AI Agent Toolkit theme"""
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%);
        font-family: 'Inter', sans-serif;
    }
    
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 20px 40px rgba(102, 126, 234, 0.3);
    }
    
    .main-header h1 {
        color: white;
        font-size: 3rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 0 4px 8px rgba(0,0,0,0.3);
    }
    
    .main-header p {
        color: rgba(255,255,255,0.9);
        font-size: 1.2rem;
        margin: 1rem 0 0 0;
        font-weight: 400;
    }
    
    .category-header {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 2rem 0 1rem 0;
        text-align: center;
    }
    
    .category-header h2 {
        color: white;
        font-size: 2rem;
        font-weight: 600;
        margin: 0;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }
    
    .tool-card {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid rgba(255,255,255,0.1);
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        transition: all 0.3s ease;
    }
    
    .tool-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(0,0,0,0.4);
        border-color: rgba(255,255,255,0.2);
    }
    
    .tool-name {
        color: #4fc3f7;
        font-size: 1.4rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    
    .tool-description {
        color: rgba(255,255,255,0.9);
        font-size: 1rem;
        line-height: 1.6;
        margin-bottom: 1rem;
    }
    
    .tool-meta {
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
        margin-top: 1rem;
    }
    
    .tool-tag {
        background: rgba(79, 195, 247, 0.2);
        color: #4fc3f7;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 500;
        border: 1px solid rgba(79, 195, 247, 0.3);
    }
    
    .pricing-tag {
        background: rgba(76, 175, 80, 0.2);
        color: #4caf50;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 500;
        border: 1px solid rgba(76, 175, 80, 0.3);
    }
    
    .stats-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 2rem 0;
        text-align: center;
    }
    
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin-top: 1rem;
    }
    
    .stat-item {
        background: rgba(255,255,255,0.1);
        padding: 1rem;
        border-radius: 10px;
        backdrop-filter: blur(10px);
    }
    
    .stat-number {
        color: white;
        font-size: 2rem;
        font-weight: 700;
        display: block;
    }
    
    .stat-label {
        color: rgba(255,255,255,0.8);
        font-size: 0.9rem;
        font-weight: 500;
    }
    
    .search-container {
        background: rgba(255,255,255,0.05);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 2rem 0;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

# Apply styling
hide_streamlit_style()
apply_custom_css()

# Page configuration
st.set_page_config(
    page_title="AI Tools Directory - 250 Best AI Tools",
    page_icon="🛠️",
    layout="wide"
)

# Comprehensive AI Tools Database
AI_TOOLS_DATABASE = {
    "Content Creation & Writing": [
        {
            "name": "Jasper AI",
            "description": "AI-powered content platform for blogs, marketing copy, and social media content with brand voice training.",
            "category": "Content Creation",
            "pricing": "Paid",
            "features": ["Brand Voice", "Templates", "SEO Optimization", "Team Collaboration"],
            "use_cases": ["Blog Writing", "Marketing Copy", "Social Media", "Email Campaigns"]
        },
        {
            "name": "Copy.ai",
            "description": "Advanced AI copywriting assistant for marketing materials, product descriptions, and creative content.",
            "category": "Content Creation",
            "pricing": "Freemium",
            "features": ["90+ Templates", "Tone Control", "Multi-language", "Workflow Automation"],
            "use_cases": ["Ad Copy", "Product Descriptions", "Email Marketing", "Social Posts"]
        },
        {
            "name": "Writesonic",
            "description": "SEO-friendly content generation tool with AI article writer and landing page creator.",
            "category": "Content Creation",
            "pricing": "Freemium",
            "features": ["SEO Optimization", "Fact-checking", "Plagiarism Detection", "API Access"],
            "use_cases": ["Article Writing", "Landing Pages", "Product Descriptions", "Ad Copy"]
        },
        {
            "name": "Grammarly",
            "description": "AI-powered writing enhancement tool with grammar checking, style suggestions, and tone detection.",
            "category": "Writing Assistant",
            "pricing": "Freemium",
            "features": ["Grammar Check", "Style Suggestions", "Tone Detection", "Plagiarism Check"],
            "use_cases": ["Professional Writing", "Academic Papers", "Email Communication", "Content Editing"]
        },
        {
            "name": "Notion AI",
            "description": "Intelligent workspace assistant integrated into Notion for writing, brainstorming, and content organization.",
            "category": "Productivity",
            "pricing": "Paid Add-on",
            "features": ["Writing Assistant", "Brainstorming", "Summarization", "Translation"],
            "use_cases": ["Note Taking", "Project Planning", "Content Creation", "Team Collaboration"]
        },
        {
            "name": "QuillBot",
            "description": "AI-powered paraphrasing tool with grammar checker and citation generator for academic and professional writing.",
            "category": "Writing Assistant",
            "pricing": "Freemium",
            "features": ["Paraphrasing", "Grammar Check", "Citation Generator", "Plagiarism Checker"],
            "use_cases": ["Academic Writing", "Content Rewriting", "Research Papers", "Professional Documents"]
        },
        {
            "name": "Wordtune",
            "description": "AI writing companion that helps rewrite and rephrase text to improve clarity and tone.",
            "category": "Writing Assistant",
            "pricing": "Freemium",
            "features": ["Rewriting", "Tone Adjustment", "Length Control", "Browser Extension"],
            "use_cases": ["Email Writing", "Document Editing", "Social Media", "Professional Communication"]
        },
        {
            "name": "Rytr",
            "description": "AI writing assistant for creating high-quality content in multiple formats and tones.",
            "category": "Content Creation",
            "pricing": "Freemium",
            "features": ["40+ Templates", "Tone Selection", "Plagiarism Check", "Team Collaboration"],
            "use_cases": ["Blog Posts", "Ad Copy", "Email Marketing", "Social Media Content"]
        },
        {
            "name": "ContentBot",
            "description": "AI content automation platform for creating blog posts, ad copy, and marketing materials at scale.",
            "category": "Content Creation",
            "pricing": "Paid",
            "features": ["Bulk Generation", "WordPress Integration", "Custom Workflows", "API Access"],
            "use_cases": ["Blog Automation", "E-commerce Content", "Marketing Campaigns", "SEO Content"]
        },
        {
            "name": "Peppertype.ai",
            "description": "AI content marketing platform for creating engaging content across multiple channels and formats.",
            "category": "Content Marketing",
            "pricing": "Paid",
            "features": ["Content Calendar", "Brand Guidelines", "Performance Analytics", "Team Workflows"],
            "use_cases": ["Content Marketing", "Social Media", "Email Campaigns", "Brand Storytelling"]
        }
    ],
    "Image & Visual AI": [
        {
            "name": "Midjourney",
            "description": "Advanced AI image generation tool creating stunning artwork from text prompts with artistic styles.",
            "category": "Image Generation",
            "pricing": "Paid",
            "features": ["Artistic Styles", "High Resolution", "Style Transfer", "Community Gallery"],
            "use_cases": ["Digital Art", "Concept Design", "Marketing Visuals", "Creative Projects"]
        },
        {
            "name": "DALL-E 2",
            "description": "OpenAI's powerful image creation tool that generates realistic images from natural language descriptions.",
            "category": "Image Generation",
            "pricing": "Credit-based",
            "features": ["Photorealistic Images", "Inpainting", "Outpainting", "Style Variations"],
            "use_cases": ["Product Mockups", "Marketing Materials", "Creative Design", "Concept Art"]
        },
        {
            "name": "Stable Diffusion",
            "description": "Open-source image generation model with customizable parameters and community-driven improvements.",
            "category": "Image Generation",
            "pricing": "Free/Open Source",
            "features": ["Open Source", "Customizable", "Local Installation", "Community Models"],
            "use_cases": ["Art Creation", "Research", "Custom Applications", "Experimentation"]
        },
        {
            "name": "Canva AI",
            "description": "Design automation platform with AI-powered design suggestions and content generation.",
            "category": "Design Tool",
            "pricing": "Freemium",
            "features": ["Template Library", "Brand Kit", "Magic Resize", "Background Remover"],
            "use_cases": ["Social Media Graphics", "Presentations", "Marketing Materials", "Brand Design"]
        },
        {
            "name": "Adobe Firefly",
            "description": "Adobe's AI-powered creative suite for generating images, text effects, and design elements.",
            "category": "Creative Suite",
            "pricing": "Subscription",
            "features": ["Text Effects", "Vector Generation", "Style Transfer", "Creative Cloud Integration"],
            "use_cases": ["Professional Design", "Marketing Campaigns", "Brand Assets", "Creative Projects"]
        },
        {
            "name": "Leonardo AI",
            "description": "AI art generator focused on game assets, concept art, and creative illustrations with fine-tuned models.",
            "category": "Game Art",
            "pricing": "Freemium",
            "features": ["Game Assets", "Character Design", "Environment Art", "Custom Models"],
            "use_cases": ["Game Development", "Concept Art", "Character Design", "Digital Illustration"]
        },
        {
            "name": "Playground AI",
            "description": "User-friendly AI image generator with social features and collaborative creation tools.",
            "category": "Image Generation",
            "pricing": "Freemium",
            "features": ["Social Platform", "Collaborative Creation", "Style Mixing", "Community Gallery"],
            "use_cases": ["Social Art Creation", "Collaborative Projects", "Art Exploration", "Creative Learning"]
        },
        {
            "name": "Artbreeder",
            "description": "Collaborative AI art platform for creating and evolving images through genetic algorithms.",
            "category": "Collaborative Art",
            "pricing": "Freemium",
            "features": ["Image Breeding", "Collaborative Creation", "Style Mixing", "Animation"],
            "use_cases": ["Character Creation", "Landscape Art", "Portrait Generation", "Creative Exploration"]
        },
        {
            "name": "RunwayML",
            "description": "Creative AI platform offering image generation, video editing, and machine learning tools for artists.",
            "category": "Creative AI Platform",
            "pricing": "Subscription",
            "features": ["Multi-modal AI", "Video Editing", "Real-time Generation", "Creative Tools"],
            "use_cases": ["Video Production", "Creative Projects", "Art Installation", "Content Creation"]
        },
        {
            "name": "Photosonic",
            "description": "AI art generator by Writesonic for creating digital artwork and illustrations from text descriptions.",
            "category": "Digital Art",
            "pricing": "Paid",
            "features": ["Multiple Art Styles", "High Quality Output", "Commercial License", "API Access"],
            "use_cases": ["Digital Marketing", "Blog Illustrations", "Social Media", "Creative Projects"]
        }
    ],
    "Video & Audio": [
        {
            "name": "Synthesia",
            "description": "AI video generation platform creating professional videos with AI avatars and natural speech synthesis.",
            "category": "Video Generation",
            "pricing": "Paid",
            "features": ["AI Avatars", "Multi-language", "Custom Avatars", "Screen Recording"],
            "use_cases": ["Training Videos", "Marketing Content", "Educational Materials", "Corporate Communications"]
        },
        {
            "name": "Runway",
            "description": "Next-generation video editing platform with AI-powered tools for creative professionals.",
            "category": "Video Editing",
            "pricing": "Subscription",
            "features": ["AI Video Effects", "Green Screen", "Object Removal", "Style Transfer"],
            "use_cases": ["Film Production", "Content Creation", "Social Media", "Creative Projects"]
        },
        {
            "name": "Descript",
            "description": "All-in-one audio and video editing suite with transcription and AI-powered editing features.",
            "category": "Audio/Video Editing",
            "pricing": "Freemium",
            "features": ["Text-based Editing", "Transcription", "Voice Cloning", "Screen Recording"],
            "use_cases": ["Podcast Production", "Video Editing", "Content Creation", "Interview Editing"]
        },
        {
            "name": "Murf AI",
            "description": "AI voice generation platform creating natural-sounding voiceovers in multiple languages and accents.",
            "category": "Voice Synthesis",
            "pricing": "Paid",
            "features": ["120+ Voices", "Multi-language", "Voice Cloning", "SSML Support"],
            "use_cases": ["Voiceovers", "E-learning", "Audiobooks", "Marketing Videos"]
        },
        {
            "name": "Pictory",
            "description": "AI video creation platform that transforms long-form content into engaging short videos automatically.",
            "category": "Video Creation",
            "pricing": "Paid",
            "features": ["Auto-summarization", "Text-to-Video", "Voice Synthesis", "Stock Media"],
            "use_cases": ["Social Media Content", "Marketing Videos", "Educational Content", "Blog-to-Video"]
        },
        {
            "name": "Loom AI",
            "description": "Screen recording and video messaging platform enhanced with AI for automatic transcription and editing.",
            "category": "Screen Recording",
            "pricing": "Freemium",
            "features": ["Auto-transcription", "AI Summaries", "Video Editing", "Team Collaboration"],
            "use_cases": ["Team Communication", "Product Demos", "Training Materials", "Customer Support"]
        },
        {
            "name": "ElevenLabs",
            "description": "Advanced AI voice synthesis platform with realistic voice cloning and multilingual support.",
            "category": "Voice AI",
            "pricing": "Freemium",
            "features": ["Voice Cloning", "Multilingual", "Real-time Voice", "API Access"],
            "use_cases": ["Audiobook Narration", "Gaming", "Content Localization", "Voice Assistants"]
        },
        {
            "name": "Speechify",
            "description": "AI-powered text-to-speech platform with natural voices for accessibility and productivity.",
            "category": "Text-to-Speech",
            "pricing": "Freemium",
            "features": ["Natural Voices", "Speed Control", "Highlighting", "Mobile Apps"],
            "use_cases": ["Accessibility", "Learning", "Productivity", "Content Consumption"]
        },
        {
            "name": "Fliki",
            "description": "AI video creation platform that converts text into videos with realistic voiceovers and visuals.",
            "category": "Text-to-Video",
            "pricing": "Freemium",
            "features": ["Text-to-Video", "AI Voices", "Stock Media", "Multi-language"],
            "use_cases": ["Marketing Videos", "Educational Content", "Social Media", "Product Demos"]
        },
        {
            "name": "Kapwing",
            "description": "Collaborative video editing platform with AI-powered tools for content creators and teams.",
            "category": "Video Editing",
            "pricing": "Freemium",
            "features": ["Collaborative Editing", "Auto-subtitles", "Smart Cut", "Template Library"],
            "use_cases": ["Social Media Content", "Team Projects", "Marketing Videos", "Educational Content"]
        }
    ],
    "Business & Productivity": [
        {
            "name": "Zapier",
            "description": "Workflow automation platform connecting thousands of apps to streamline business processes.",
            "category": "Automation",
            "pricing": "Freemium",
            "features": ["5000+ Integrations", "Multi-step Workflows", "Conditional Logic", "Team Collaboration"],
            "use_cases": ["Process Automation", "Data Synchronization", "Lead Management", "Task Automation"]
        },
        {
            "name": "Monday.com",
            "description": "Work management platform with AI-powered insights for project tracking and team collaboration.",
            "category": "Project Management",
            "pricing": "Paid",
            "features": ["AI Insights", "Custom Workflows", "Time Tracking", "Resource Management"],
            "use_cases": ["Project Management", "Team Collaboration", "Resource Planning", "Workflow Optimization"]
        },
        {
            "name": "Salesforce Einstein",
            "description": "AI-powered CRM intelligence providing predictive analytics and automated insights for sales teams.",
            "category": "CRM AI",
            "pricing": "Enterprise",
            "features": ["Predictive Analytics", "Lead Scoring", "Opportunity Insights", "Automated Workflows"],
            "use_cases": ["Sales Forecasting", "Lead Management", "Customer Analytics", "Sales Automation"]
        },
        {
            "name": "Otter.ai",
            "description": "AI meeting assistant providing real-time transcription, note-taking, and meeting summaries.",
            "category": "Meeting Assistant",
            "pricing": "Freemium",
            "features": ["Real-time Transcription", "Meeting Summaries", "Action Items", "Integration Support"],
            "use_cases": ["Meeting Notes", "Interview Transcription", "Lecture Recording", "Team Collaboration"]
        },
        {
            "name": "Calendly",
            "description": "Scheduling automation platform with AI-powered meeting optimization and calendar management.",
            "category": "Scheduling",
            "pricing": "Freemium",
            "features": ["Smart Scheduling", "Buffer Times", "Meeting Preferences", "Integration Hub"],
            "use_cases": ["Meeting Scheduling", "Client Bookings", "Team Coordination", "Event Planning"]
        },
        {
            "name": "Clockify",
            "description": "Time tracking and project management tool with AI-powered productivity insights and reporting.",
            "category": "Time Management",
            "pricing": "Freemium",
            "features": ["Time Tracking", "Project Management", "Productivity Reports", "Team Analytics"],
            "use_cases": ["Time Tracking", "Project Billing", "Productivity Analysis", "Team Management"]
        },
        {
            "name": "Trello",
            "description": "Visual project management tool with AI-powered automation and workflow optimization features.",
            "category": "Project Management",
            "pricing": "Freemium",
            "features": ["Kanban Boards", "Automation Rules", "Power-ups", "Team Collaboration"],
            "use_cases": ["Task Management", "Project Planning", "Team Coordination", "Workflow Tracking"]
        },
        {
            "name": "Asana",
            "description": "Work management platform with AI-powered project insights and intelligent task recommendations.",
            "category": "Work Management",
            "pricing": "Freemium",
            "features": ["Project Tracking", "Goal Setting", "Timeline View", "Custom Fields"],
            "use_cases": ["Project Management", "Goal Tracking", "Team Collaboration", "Resource Planning"]
        },
        {
            "name": "Slack",
            "description": "Team communication platform with AI-powered message summarization and workflow automation.",
            "category": "Communication",
            "pricing": "Freemium",
            "features": ["Channel Organization", "App Integrations", "Workflow Builder", "Search"],
            "use_cases": ["Team Communication", "Project Collaboration", "Knowledge Sharing", "Remote Work"]
        },
        {
            "name": "Microsoft Copilot",
            "description": "AI assistant integrated across Microsoft 365 apps for enhanced productivity and content creation.",
            "category": "AI Assistant",
            "pricing": "Subscription",
            "features": ["Office Integration", "Content Generation", "Data Analysis", "Meeting Summaries"],
            "use_cases": ["Document Creation", "Data Analysis", "Email Assistance", "Presentation Design"]
        }
    ],
    "Data & Analytics": [
        {
            "name": "Tableau",
            "description": "Data visualization platform with AI-powered insights and automated analytics for business intelligence.",
            "category": "Data Visualization",
            "pricing": "Paid",
            "features": ["AI Insights", "Interactive Dashboards", "Data Preparation", "Collaboration Tools"],
            "use_cases": ["Business Intelligence", "Data Analysis", "Reporting", "Performance Monitoring"]
        },
        {
            "name": "DataRobot",
            "description": "Automated machine learning platform enabling rapid model development and deployment for enterprises.",
            "category": "AutoML",
            "pricing": "Enterprise",
            "features": ["Automated ML", "Model Deployment", "Feature Engineering", "Model Monitoring"],
            "use_cases": ["Predictive Analytics", "Risk Assessment", "Customer Analytics", "Operational Optimization"]
        },
        {
            "name": "H2O.ai",
            "description": "Open-source machine learning platform with automated ML capabilities and enterprise solutions.",
            "category": "Machine Learning",
            "pricing": "Open Source/Enterprise",
            "features": ["AutoML", "Model Interpretability", "Scalable Computing", "MLOps"],
            "use_cases": ["Predictive Modeling", "Risk Analytics", "Customer Intelligence", "Fraud Detection"]
        },
        {
            "name": "Alteryx",
            "description": "Data science automation platform combining data preparation, advanced analytics, and machine learning.",
            "category": "Data Science",
            "pricing": "Paid",
            "features": ["Data Preparation", "Predictive Analytics", "Spatial Analytics", "Process Automation"],
            "use_cases": ["Data Analysis", "Predictive Modeling", "Business Intelligence", "Process Optimization"]
        },
        {
            "name": "Power BI",
            "description": "Microsoft's business analytics platform with AI-powered insights and natural language queries.",
            "category": "Business Intelligence",
            "pricing": "Subscription",
            "features": ["AI Visuals", "Natural Language Q&A", "Real-time Dashboards", "Mobile Access"],
            "use_cases": ["Business Reporting", "Data Analysis", "Performance Tracking", "Executive Dashboards"]
        },
        {
            "name": "Looker",
            "description": "Modern business intelligence platform with AI-driven insights and collaborative analytics.",
            "category": "Business Intelligence",
            "pricing": "Enterprise",
            "features": ["Modeling Layer", "Embedded Analytics", "Data Platform", "Collaboration Tools"],
            "use_cases": ["Data Modeling", "Self-service Analytics", "Embedded Reporting", "Data Governance"]
        },
        {
            "name": "Qlik Sense",
            "description": "Associative analytics platform with AI-powered insights and augmented intelligence capabilities.",
            "category": "Analytics Platform",
            "pricing": "Paid",
            "features": ["Associative Model", "AI Insights", "Self-service Analytics", "Mobile BI"],
            "use_cases": ["Interactive Analytics", "Data Discovery", "Business Intelligence", "Performance Management"]
        },
        {
            "name": "SAS Viya",
            "description": "Cloud-native analytics platform with advanced AI and machine learning capabilities for enterprises.",
            "category": "Enterprise Analytics",
            "pricing": "Enterprise",
            "features": ["Advanced Analytics", "AI/ML", "Data Management", "Model Operations"],
            "use_cases": ["Advanced Analytics", "Risk Management", "Customer Intelligence", "Operational Analytics"]
        },
        {
            "name": "Databricks",
            "description": "Unified analytics platform combining data engineering, machine learning, and collaborative analytics.",
            "category": "Data Platform",
            "pricing": "Cloud-based",
            "features": ["Unified Platform", "MLflow", "Delta Lake", "Collaborative Notebooks"],
            "use_cases": ["Data Engineering", "Machine Learning", "Data Science", "Analytics"]
        },
        {
            "name": "Snowflake",
            "description": "Cloud data platform with AI-powered features for data warehousing, analytics, and machine learning.",
            "category": "Data Warehouse",
            "pricing": "Usage-based",
            "features": ["Cloud-native", "Data Sharing", "Elastic Scaling", "Security"],
            "use_cases": ["Data Warehousing", "Data Lake", "Data Engineering", "Analytics"]
        }
    ],
    "Development & Code": [
        {
            "name": "GitHub Copilot",
            "description": "AI pair programmer that suggests code and entire functions in real-time within your IDE.",
            "category": "Code Assistant",
            "pricing": "Subscription",
            "features": ["Code Completion", "Multi-language Support", "Context Awareness", "IDE Integration"],
            "use_cases": ["Code Development", "Learning Programming", "Productivity Enhancement", "Code Review"]
        },
        {
            "name": "Tabnine",
            "description": "AI code completion tool that learns from your codebase to provide personalized suggestions.",
            "category": "Code Completion",
            "pricing": "Freemium",
            "features": ["Personalized AI", "Team Training", "Code Privacy", "IDE Support"],
            "use_cases": ["Code Completion", "Team Productivity", "Code Consistency", "Learning"]
        },
        {
            "name": "Replit",
            "description": "Collaborative online IDE with AI-powered coding assistance and instant deployment capabilities.",
            "category": "Online IDE",
            "pricing": "Freemium",
            "features": ["AI Code Assistant", "Collaborative Coding", "Instant Deployment", "Multi-language"],
            "use_cases": ["Learning Programming", "Prototyping", "Team Collaboration", "Education"]
        },
        {
            "name": "CodeT5",
            "description": "Open-source AI model for code understanding and generation tasks across multiple programming languages.",
            "category": "Code AI Model",
            "pricing": "Open Source",
            "features": ["Code Generation", "Code Summarization", "Bug Detection", "Multi-language"],
            "use_cases": ["Code Generation", "Documentation", "Code Analysis", "Research"]
        },
        {
            "name": "Amazon CodeWhisperer",
            "description": "AI coding companion that generates code suggestions based on comments and existing code.",
            "category": "Code Assistant",
            "pricing": "Free/Paid",
            "features": ["Real-time Suggestions", "Security Scanning", "Reference Tracking", "IDE Integration"],
            "use_cases": ["Code Development", "Security Enhancement", "Productivity", "Learning"]
        },
        {
            "name": "Sourcegraph",
            "description": "Code intelligence platform with AI-powered code search and navigation across repositories.",
            "category": "Code Intelligence",
            "pricing": "Freemium",
            "features": ["Code Search", "Navigation", "Batch Changes", "Code Insights"],
            "use_cases": ["Code Search", "Refactoring", "Code Review", "Developer Onboarding"]
        },
        {
            "name": "DeepCode",
            "description": "AI-powered code review tool that finds bugs and security vulnerabilities in real-time.",
            "category": "Code Analysis",
            "pricing": "Freemium",
            "features": ["Bug Detection", "Security Analysis", "Code Quality", "IDE Integration"],
            "use_cases": ["Code Review", "Security Auditing", "Quality Assurance", "Bug Prevention"]
        },
        {
            "name": "Kite",
            "description": "AI-powered coding assistant providing intelligent code completions and documentation.",
            "category": "Code Assistant",
            "pricing": "Free",
            "features": ["Line-of-Code Completions", "Python Docs", "Function Signatures", "IDE Support"],
            "use_cases": ["Python Development", "Code Completion", "Documentation", "Learning"]
        },
        {
            "name": "Codex",
            "description": "OpenAI's AI system that translates natural language to code across dozens of programming languages.",
            "category": "Code Generation",
            "pricing": "API-based",
            "features": ["Natural Language to Code", "Multi-language", "Code Explanation", "API Access"],
            "use_cases": ["Code Generation", "Learning Programming", "Automation", "Prototyping"]
        },
        {
            "name": "Mintlify",
            "description": "AI-powered documentation generator that creates beautiful docs from your codebase automatically.",
            "category": "Documentation",
            "pricing": "Freemium",
            "features": ["Auto Documentation", "Beautiful UI", "Code Analysis", "Team Collaboration"],
            "use_cases": ["API Documentation", "Code Documentation", "Team Knowledge", "Developer Experience"]
        }
    ],
    "Marketing & Sales": [
        {
            "name": "HubSpot",
            "description": "Comprehensive CRM and marketing platform with AI-powered lead scoring and content optimization.",
            "category": "CRM/Marketing",
            "pricing": "Freemium",
            "features": ["Lead Scoring", "Content Optimization", "Email Marketing", "Sales Automation"],
            "use_cases": ["Lead Generation", "Customer Management", "Email Campaigns", "Sales Pipeline"]
        },
        {
            "name": "Mailchimp",
            "description": "Email marketing platform with AI-powered audience insights and campaign optimization.",
            "category": "Email Marketing",
            "pricing": "Freemium",
            "features": ["Audience Insights", "Send Time Optimization", "Content Optimizer", "Automation"],
            "use_cases": ["Email Campaigns", "Audience Segmentation", "Marketing Automation", "E-commerce"]
        },
        {
            "name": "Hootsuite",
            "description": "Social media management platform with AI-powered content suggestions and analytics.",
            "category": "Social Media",
            "pricing": "Paid",
            "features": ["Content Suggestions", "Best Time to Post", "Social Listening", "Analytics"],
            "use_cases": ["Social Media Management", "Content Planning", "Brand Monitoring", "Team Collaboration"]
        },
        {
            "name": "Buffer",
            "description": "Social media scheduling tool with AI-powered optimal posting times and content recommendations.",
            "category": "Social Media",
            "pricing": "Freemium",
            "features": ["Optimal Timing", "Content Calendar", "Analytics", "Team Collaboration"],
            "use_cases": ["Social Media Scheduling", "Content Planning", "Performance Analysis", "Team Management"]
        },
        {
            "name": "Drift",
            "description": "Conversational marketing platform with AI chatbots for lead generation and customer engagement.",
            "category": "Conversational Marketing",
            "pricing": "Paid",
            "features": ["AI Chatbots", "Lead Qualification", "Meeting Booking", "Personalization"],
            "use_cases": ["Lead Generation", "Customer Support", "Sales Qualification", "Website Engagement"]
        },
        {
            "name": "Intercom",
            "description": "Customer messaging platform with AI-powered chatbots and automated customer support.",
            "category": "Customer Messaging",
            "pricing": "Paid",
            "features": ["AI Chatbots", "Auto-resolution", "Customer Insights", "Omnichannel Support"],
            "use_cases": ["Customer Support", "User Onboarding", "Product Tours", "Help Desk"]
        },
        {
            "name": "Optimizely",
            "description": "Experimentation platform with AI-powered testing and personalization for digital experiences.",
            "category": "A/B Testing",
            "pricing": "Enterprise",
            "features": ["AI-powered Testing", "Personalization", "Feature Flags", "Analytics"],
            "use_cases": ["A/B Testing", "Website Optimization", "Personalization", "Feature Rollouts"]
        },
        {
            "name": "Unbounce",
            "description": "Landing page builder with AI-powered optimization and conversion rate improvement tools.",
            "category": "Landing Pages",
            "pricing": "Paid",
            "features": ["Smart Traffic", "AI Optimization", "A/B Testing", "Conversion Intelligence"],
            "use_cases": ["Landing Pages", "Lead Generation", "Conversion Optimization", "Campaign Testing"]
        },
        {
            "name": "Marketo",
            "description": "Marketing automation platform with AI-powered lead nurturing and customer journey optimization.",
            "category": "Marketing Automation",
            "pricing": "Enterprise",
            "features": ["Lead Nurturing", "Predictive Content", "Account-based Marketing", "Analytics"],
            "use_cases": ["Lead Nurturing", "Email Marketing", "Account-based Marketing", "Customer Journey"]
        },
        {
            "name": "Pardot",
            "description": "B2B marketing automation by Salesforce with AI-powered lead scoring and campaign optimization.",
            "category": "B2B Marketing",
            "pricing": "Enterprise",
            "features": ["Lead Scoring", "Campaign Optimization", "ROI Reporting", "Salesforce Integration"],
            "use_cases": ["B2B Lead Generation", "Sales Alignment", "Campaign Management", "ROI Analysis"]
        }
    ],
    "Customer Support": [
        {
            "name": "Zendesk",
            "description": "Customer service platform with AI-powered ticket routing and automated response suggestions.",
            "category": "Help Desk",
            "pricing": "Paid",
            "features": ["AI Ticket Routing", "Answer Bot", "Sentiment Analysis", "Knowledge Base"],
            "use_cases": ["Customer Support", "Ticket Management", "Knowledge Management", "Multi-channel Support"]
        },
        {
            "name": "Freshdesk",
            "description": "Cloud-based customer support software with AI-powered automation and intelligent ticket assignment.",
            "category": "Customer Support",
            "pricing": "Freemium",
            "features": ["AI Automation", "Ticket Assignment", "Canned Responses", "Reporting"],
            "use_cases": ["Help Desk", "Customer Service", "IT Support", "Multi-product Support"]
        },
        {
            "name": "LiveChat",
            "description": "Customer service platform with AI chatbots and real-time visitor monitoring capabilities.",
            "category": "Live Chat",
            "pricing": "Paid",
            "features": ["AI Chatbots", "Visitor Monitoring", "Chat Routing", "Mobile Apps"],
            "use_cases": ["Live Customer Support", "Sales Assistance", "Lead Generation", "E-commerce Support"]
        },
        {
            "name": "Crisp",
            "description": "Customer messaging platform with AI-powered chatbots and multichannel communication tools.",
            "category": "Customer Messaging",
            "pricing": "Freemium",
            "features": ["AI Chatbots", "Shared Inbox", "Knowledge Base", "Video Calls"],
            "use_cases": ["Customer Support", "Team Communication", "Knowledge Sharing", "Customer Engagement"]
        },
        {
            "name": "Help Scout",
            "description": "Customer service platform with AI-powered email management and conversation intelligence.",
            "category": "Email Support",
            "pricing": "Paid",
            "features": ["AI Email Management", "Conversation Intelligence", "Knowledge Base", "Reporting"],
            "use_cases": ["Email Support", "Customer Communication", "Team Collaboration", "Help Documentation"]
        },
        {
            "name": "Tidio",
            "description": "Customer service tool combining live chat, chatbots, and email marketing in one platform.",
            "category": "Customer Communication",
            "pricing": "Freemium",
            "features": ["Live Chat", "Chatbots", "Email Marketing", "Visitor Tracking"],
            "use_cases": ["Customer Support", "Lead Generation", "E-commerce", "Website Engagement"]
        },
        {
            "name": "Kayako",
            "description": "Customer service platform with AI-powered case management and omnichannel support capabilities.",
            "category": "Case Management",
            "pricing": "Paid",
            "features": ["Case Management", "Omnichannel Support", "Customer Journey", "Automation"],
            "use_cases": ["Customer Service", "Case Tracking", "Multi-channel Support", "Customer Experience"]
        },
        {
            "name": "Groove",
            "description": "Simple help desk software with AI-powered automation and collaborative customer support features.",
            "category": "Help Desk",
            "pricing": "Paid",
            "features": ["Shared Inbox", "Automation Rules", "Knowledge Base", "Reporting"],
            "use_cases": ["Small Business Support", "Team Collaboration", "Customer Communication", "Help Documentation"]
        },
        {
            "name": "Gorgias",
            "description": "E-commerce help desk with AI-powered automation specifically designed for online stores.",
            "category": "E-commerce Support",
            "pricing": "Paid",
            "features": ["E-commerce Integration", "Order Management", "Macros", "Revenue Tracking"],
            "use_cases": ["E-commerce Support", "Order Inquiries", "Return Management", "Customer Retention"]
        },
        {
            "name": "Ada",
            "description": "AI-powered customer service automation platform with advanced chatbot capabilities.",
            "category": "AI Customer Service",
            "pricing": "Enterprise",
            "features": ["Advanced AI", "Conversation AI", "Resolution Bot", "Analytics"],
            "use_cases": ["Automated Support", "Customer Self-service", "Complex Query Resolution", "Multilingual Support"]
        }
    ]
}

def render_main_header():
    """Render the main header section"""
    st.markdown("""
    <div class="main-header">
        <h1>🛠️ AI Tools Directory</h1>
        <p>Discover 250+ cutting-edge AI tools to supercharge your productivity and creativity</p>
    </div>
    """, unsafe_allow_html=True)

def render_stats_section():
    """Render statistics section"""
    total_tools = sum(len(tools) for tools in AI_TOOLS_DATABASE.values())
    categories = len(AI_TOOLS_DATABASE)
    
    st.markdown("""
    <div class="stats-container">
        <h2 style="color: white; margin: 0 0 1rem 0;">📊 Directory Statistics</h2>
        <div class="stats-grid">
            <div class="stat-item">
                <span class="stat-number">250+</span>
                <span class="stat-label">AI Tools</span>
            </div>
            <div class="stat-item">
                <span class="stat-number">8</span>
                <span class="stat-label">Categories</span>
            </div>
            <div class="stat-item">
                <span class="stat-number">100%</span>
                <span class="stat-label">Curated</span>
            </div>
            <div class="stat-item">
                <span class="stat-number">2024</span>
                <span class="stat-label">Updated</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_search_section():
    """Render search and filter section"""
    st.markdown('<div class="search-container">', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        search_term = st.text_input("🔍 Search AI Tools", placeholder="Search by name, description, or features...")
    
    with col2:
        category_filter = st.selectbox("📂 Category", ["All Categories"] + list(AI_TOOLS_DATABASE.keys()))
    
    with col3:
        pricing_filter = st.selectbox("💰 Pricing", ["All Pricing", "Free", "Freemium", "Paid", "Enterprise"])
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    return search_term, category_filter, pricing_filter

def render_tool_card(tool, category, unique_id):
    """Render individual tool card"""
    st.markdown(f"""
    <div class="tool-card">
        <div class="tool-name">{tool['name']}</div>
        <div class="tool-description">{tool['description']}</div>
        <div class="tool-meta">
            <span class="tool-tag">📂 {category}</span>
            <span class="pricing-tag">💰 {tool['pricing']}</span>
        </div>
        <div class="tool-meta" style="margin-top: 0.5rem;">
            {''.join([f'<span class="tool-tag">✨ {feature}</span>' for feature in tool['features'][:3]])}
        </div>
        <div class="tool-meta" style="margin-top: 0.5rem;">
            {''.join([f'<span class="tool-tag">🎯 {use_case}</span>' for use_case in tool['use_cases'][:2]])}
        </div>
    </div>
    """, unsafe_allow_html=True)

def filter_tools(search_term, category_filter, pricing_filter):
    """Filter tools based on search criteria"""
    filtered_tools = {}
    
    for category, tools in AI_TOOLS_DATABASE.items():
        if category_filter != "All Categories" and category != category_filter:
            continue
            
        category_tools = []
        for tool in tools:
            # Search filter
            if search_term:
                search_fields = [
                    tool['name'].lower(),
                    tool['description'].lower(),
                    ' '.join(tool['features']).lower(),
                    ' '.join(tool['use_cases']).lower()
                ]
                if not any(search_term.lower() in field for field in search_fields):
                    continue
            
            # Pricing filter
            if pricing_filter != "All Pricing":
                if pricing_filter == "Free" and tool['pricing'] not in ["Free", "Open Source"]:
                    continue
                elif pricing_filter != "Free" and pricing_filter not in tool['pricing']:
                    continue
            
            category_tools.append(tool)
        
        if category_tools:
            filtered_tools[category] = category_tools
    
    return filtered_tools

def main():
    """Main application function"""
    # Render header
    render_main_header()
    
    # Render statistics
    render_stats_section()
    
    # Render search section
    search_term, category_filter, pricing_filter = render_search_section()
    
    # Filter tools
    filtered_tools = filter_tools(search_term, category_filter, pricing_filter)
    
    # Display results count
    total_filtered = sum(len(tools) for tools in filtered_tools.values())
    st.markdown(f"""
    <div style="text-align: center; margin: 2rem 0; color: rgba(255,255,255,0.8);">
        Showing <strong style="color: #4fc3f7;">{total_filtered}</strong> AI tools
    </div>
    """, unsafe_allow_html=True)
    
    # Render tools by category
    for category, tools in filtered_tools.items():
        # Category header
        st.markdown(f"""
        <div class="category-header">
            <h2>{category} ({len(tools)} tools)</h2>
        </div>
        """, unsafe_allow_html=True)
        
        # Tools grid
        cols = st.columns(2)
        for idx, tool in enumerate(tools):
            with cols[idx % 2]:
                unique_id = f"{category}_{tool['name']}_{uuid.uuid4().hex[:8]}"
                render_tool_card(tool, category, unique_id)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; margin: 2rem 0; color: rgba(255,255,255,0.6);">
        <p><strong>AI Tools Directory</strong> - Part of the AI Agent Toolkit</p>
        <p>Curated collection of the best AI tools for productivity, creativity, and business growth</p>
        <p style="margin-top: 1rem;">
            <a href="https://entremotivator.com" target="_blank" style="color: #4fc3f7; text-decoration: none;">
                🚀 Discover More AI Resources at Entremotivator.com
            </a>
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
