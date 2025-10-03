import streamlit as st
import pandas as pd
from collections import defaultdict

# Page configuration - hide GitHub settings
st.set_page_config(
    page_title="📘 AI Terms Glossary",
    layout="wide",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': None
    }
)

# Custom CSS for card-based UI
st.markdown("""
<style>
    /* Hide GitHub icon and settings */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Card styling */
    .term-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 12px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        border-left: 5px solid #ffd700;
    }
    
    .term-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 12px rgba(0, 0, 0, 0.2);
    }
    
    .term-title {
        color: #ffffff;
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 10px;
    }
    
    .term-definition {
        color: #f0f0f0;
        font-size: 16px;
        line-height: 1.6;
    }
    
    .category-header {
        background: linear-gradient(90deg, #11998e 0%, #38ef7d 100%);
        color: white;
        padding: 15px 20px;
        border-radius: 8px;
        margin: 20px 0 10px 0;
        font-size: 20px;
        font-weight: bold;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    .hero-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 40px;
        border-radius: 15px;
        margin-bottom: 30px;
        text-align: center;
        color: white;
    }
    
    .hero-title {
        font-size: 48px;
        font-weight: bold;
        margin-bottom: 15px;
    }
    
    .hero-subtitle {
        font-size: 20px;
        opacity: 0.9;
    }
    
    .stats-container {
        display: flex;
        justify-content: space-around;
        margin: 30px 0;
    }
    
    .stat-card {
        background: white;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        flex: 1;
        margin: 0 10px;
    }
    
    .stat-number {
        font-size: 36px;
        font-weight: bold;
        color: #667eea;
    }
    
    .stat-label {
        font-size: 14px;
        color: #666;
        margin-top: 5px;
    }
</style>
""", unsafe_allow_html=True)

# Enhanced AI glossary with more comprehensive definitions
ai_terms = [
    ("AI", "Artificial Intelligence", "Technology that enables computers and machines to simulate human intelligence, including learning, reasoning, problem-solving, perception, and language understanding. AI systems can analyze data, recognize patterns, and make decisions with minimal human intervention."),
    ("AGI", "Artificial General Intelligence", "A theoretical form of AI that possesses the ability to understand, learn, and apply knowledge across a wide range of tasks at a level equal to or beyond human capability. Unlike narrow AI, AGI would demonstrate flexible intelligence applicable to any intellectual task."),
    ("ANN", "Artificial Neural Network", "A computational model inspired by biological neural networks in the human brain. ANNs consist of interconnected nodes (neurons) organized in layers that process information through weighted connections, enabling pattern recognition and learning from data."),
    ("API", "Application Programming Interface", "A set of protocols, tools, and definitions that allows different software applications to communicate with each other. APIs enable developers to access specific features or data from an application, service, or platform without understanding its internal workings."),
    ("ASR", "Automatic Speech Recognition", "Technology that converts spoken language into written text. ASR systems use acoustic and language models to process audio signals, identify phonemes, and transcribe words, enabling voice-controlled applications and accessibility features."),
    ("AutoML", "Automated Machine Learning", "A process that automates the end-to-end pipeline of applying machine learning to real-world problems. AutoML handles tasks such as data preprocessing, feature engineering, model selection, hyperparameter tuning, and evaluation, making ML accessible to non-experts."),
    ("AUC", "Area Under the Curve", "A performance metric for classification models that measures the area under the Receiver Operating Characteristic (ROC) curve. AUC values range from 0 to 1, with higher values indicating better model performance in distinguishing between classes."),
    ("Backpropagation", "Backpropagation Algorithm", "A fundamental algorithm for training neural networks that calculates gradients of the loss function with respect to network weights. It works by propagating errors backward through the network, enabling efficient optimization of complex models."),
    ("BERT", "Bidirectional Encoder Representations from Transformers", "A transformer-based language model developed by Google that processes text bidirectionally, considering both left and right context simultaneously. BERT has revolutionized natural language processing by achieving state-of-the-art results on numerous NLP tasks."),
    ("Bias", "Model Bias", "Systematic errors in a model's predictions that consistently deviate from true values. Bias can arise from training data, algorithm design, or assumptions, and may reflect or amplify societal prejudices, leading to unfair or discriminatory outcomes."),
    ("BM25", "Best Matching 25", "A probabilistic ranking algorithm used in information retrieval to estimate the relevance of documents to a search query. BM25 considers term frequency, document length, and inverse document frequency to produce relevance scores."),
    ("Black Box", "Black Box Model", "A model whose internal decision-making process is opaque or difficult to interpret. While black box models may achieve high accuracy, their lack of transparency can be problematic in applications requiring explainability and accountability."),
    ("CatBoost", "Categorical Boosting", "A gradient boosting library developed by Yandex that excels at handling categorical features without extensive preprocessing. CatBoost uses ordered boosting and innovative techniques to reduce overfitting and improve model performance."),
    ("Chain-of-Thought", "Chain-of-Thought Prompting", "A prompting technique that encourages large language models to break down complex reasoning tasks into intermediate steps. This approach improves model performance on tasks requiring multi-step reasoning and problem-solving."),
    ("CNN", "Convolutional Neural Network", "A specialized neural network architecture designed for processing grid-like data such as images. CNNs use convolutional layers to automatically learn spatial hierarchies of features, making them highly effective for computer vision tasks."),
    ("Cold Start", "Cold Start Problem", "A challenge in recommendation systems where insufficient data exists for new users or items, making it difficult to generate accurate recommendations. Solutions include content-based filtering, demographic information, and hybrid approaches."),
    ("Contrastive Learning", "Contrastive Learning Method", "A self-supervised learning approach that teaches models to distinguish between similar and dissimilar examples. By learning to pull similar samples together and push dissimilar ones apart in representation space, models develop robust feature representations."),
    ("Curriculum Learning", "Curriculum Learning Strategy", "A training methodology that presents examples to a model in a meaningful order, typically from simple to complex. This approach mimics human learning and can improve model performance, convergence speed, and generalization."),
    ("CV", "Computer Vision", "A field of artificial intelligence that enables computers to interpret and understand visual information from the world. Computer vision applications include image recognition, object detection, facial recognition, and autonomous navigation."),
    ("CUDA", "Compute Unified Device Architecture", "A parallel computing platform and programming model developed by NVIDIA that allows developers to use GPU acceleration for general-purpose processing. CUDA is essential for training deep learning models efficiently."),
    ("DALL·E", "DALL·E Image Generator", "A deep learning model developed by OpenAI that generates images from textual descriptions. DALL·E combines natural language understanding with image synthesis to create novel, creative visual content based on user prompts."),
    ("Data Augmentation", "Data Augmentation Technique", "A strategy for artificially expanding training datasets by creating modified versions of existing samples. Techniques include rotation, flipping, cropping, and color adjustment for images, helping models generalize better and reducing overfitting."),
    ("Data Drift", "Data Drift Phenomenon", "The change in statistical properties of input data over time, which can degrade model performance. Monitoring and addressing data drift is crucial for maintaining model accuracy in production environments."),
    ("DeepFake", "Deep Fake Media", "AI-generated synthetic media, particularly audio and video, that convincingly depicts people saying or doing things they never actually did. DeepFakes use deep learning techniques like GANs and autoencoders to create realistic but fabricated content."),
    ("DL", "Deep Learning", "A subset of machine learning based on artificial neural networks with multiple layers. Deep learning models automatically learn hierarchical feature representations from data, achieving breakthrough performance in areas like image recognition, speech processing, and natural language understanding."),
    ("Edge AI", "Edge Artificial Intelligence", "The deployment of AI algorithms and models on edge devices such as smartphones, IoT sensors, and embedded systems. Edge AI enables real-time processing, reduces latency, enhances privacy, and decreases dependence on cloud connectivity."),
    ("EDA", "Exploratory Data Analysis", "An approach to analyzing datasets to summarize their main characteristics, often using visual methods. EDA helps identify patterns, detect anomalies, test hypotheses, and check assumptions before applying formal modeling techniques."),
    ("ELMo", "Embeddings from Language Models", "A deep contextualized word representation model that generates embeddings based on the entire context of a word. Unlike static embeddings, ELMo produces different representations for the same word depending on its usage context."),
    ("Embedding", "Vector Embedding", "A learned representation that maps discrete objects (words, images, users) into continuous vector spaces. Embeddings capture semantic relationships and enable mathematical operations on categorical data, facilitating machine learning tasks."),
    ("Ensemble", "Ensemble Learning", "A machine learning technique that combines predictions from multiple models to produce a more accurate and robust final prediction. Ensemble methods like bagging, boosting, and stacking often outperform individual models."),
    ("ETL", "Extract, Transform, Load", "A data integration process that extracts data from various sources, transforms it into a suitable format, and loads it into a target system. ETL pipelines are fundamental to data warehousing and analytics workflows."),
    ("F1 Score", "F1 Score Metric", "The harmonic mean of precision and recall, providing a balanced measure of a model's performance. The F1 score is particularly useful when dealing with imbalanced datasets where accuracy alone may be misleading."),
    ("FAIR", "Facebook AI Research", "The artificial intelligence research division of Meta (formerly Facebook) that conducts fundamental and applied research in machine learning, computer vision, natural language processing, and other AI domains."),
    ("Feature Engineering", "Feature Engineering Process", "The process of creating, selecting, and transforming raw data into features that better represent the underlying problem to predictive models. Effective feature engineering can significantly improve model performance and is often considered an art in machine learning."),
    ("Few-shot Learning", "Few-shot Learning Paradigm", "A machine learning approach where models learn to perform tasks with only a small number of training examples. Few-shot learning is crucial for scenarios where labeled data is scarce or expensive to obtain."),
    ("FLOPs", "Floating Point Operations Per Second", "A measure of computational performance indicating how many floating-point calculations a system can perform in one second. FLOPs are commonly used to quantify the computational requirements of machine learning models."),
    ("GAN", "Generative Adversarial Network", "A deep learning architecture consisting of two neural networks—a generator and a discriminator—that compete against each other. GANs excel at generating realistic synthetic data, including images, audio, and text."),
    ("GPT", "Generative Pre-trained Transformer", "A family of large language models developed by OpenAI that use transformer architecture and are pre-trained on vast amounts of text data. GPT models can generate human-like text and perform various natural language tasks."),
    ("Gradient Clipping", "Gradient Clipping Technique", "A method to prevent the exploding gradient problem in neural network training by limiting the magnitude of gradients during backpropagation. This technique stabilizes training and improves convergence, especially in recurrent neural networks."),
    ("GRU", "Gated Recurrent Unit", "A type of recurrent neural network architecture that uses gating mechanisms to control information flow. GRUs are simpler than LSTMs but often achieve comparable performance while being computationally more efficient."),
    ("Hallucination", "AI Hallucination", "A phenomenon where large language models generate information that appears plausible but is factually incorrect or entirely fabricated. Hallucinations represent a significant challenge in deploying LLMs for applications requiring factual accuracy."),
    ("Hugging Face", "Hugging Face Platform", "An AI community and platform that provides tools, libraries, and repositories for natural language processing and machine learning. Hugging Face hosts thousands of pre-trained models and datasets, facilitating collaboration and innovation."),
    ("Human-in-the-loop", "Human-in-the-loop Learning", "An approach where humans actively participate in the training or decision-making process of AI systems. This collaboration combines machine efficiency with human judgment, improving model accuracy and addressing edge cases."),
    ("Hyperparameter", "Hyperparameter Configuration", "Parameters that control the learning process and model architecture, set before training begins. Examples include learning rate, batch size, and number of layers. Hyperparameter tuning is essential for optimizing model performance."),
    ("Inference", "Model Inference", "The process of using a trained machine learning model to make predictions on new, unseen data. Inference is the deployment phase where models deliver value by generating outputs for real-world applications."),
    ("Intent Detection", "Intent Detection System", "A natural language understanding task that identifies the underlying intention or goal behind user input. Intent detection is fundamental to conversational AI, enabling chatbots and virtual assistants to respond appropriately."),
    ("IoT", "Internet of Things", "A network of physical devices embedded with sensors, software, and connectivity that enables them to collect and exchange data. IoT devices generate massive amounts of data that can be analyzed using AI for insights and automation."),
    ("JAX", "JAX Library", "A numerical computing library developed by Google that combines NumPy-like syntax with automatic differentiation and GPU/TPU acceleration. JAX is increasingly popular for machine learning research due to its flexibility and performance."),
    ("Keras", "Keras API", "A high-level deep learning API written in Python that provides a user-friendly interface for building and training neural networks. Keras runs on top of TensorFlow and emphasizes ease of use and rapid prototyping."),
    ("KNN", "K-Nearest Neighbors", "A simple, non-parametric machine learning algorithm that classifies data points based on the majority class of their k nearest neighbors in feature space. KNN is intuitive and effective for many classification and regression tasks."),
    ("LangChain", "LangChain Framework", "A framework for developing applications powered by large language models. LangChain provides tools for chaining LLM calls, integrating external data sources, and building complex workflows involving language models."),
    ("Latent Space", "Latent Space Representation", "A compressed, abstract representation of data learned by models like autoencoders and GANs. Latent spaces capture essential features and enable operations like interpolation, generation, and semantic manipulation."),
    ("LLM", "Large Language Model", "A neural network model trained on vast amounts of text data, typically containing billions of parameters. LLMs can understand and generate human-like text, performing tasks like translation, summarization, question-answering, and creative writing."),
    ("LLMOps", "Large Language Model Operations", "Practices and tools for deploying, monitoring, and maintaining large language models in production. LLMOps addresses challenges like model versioning, prompt management, cost optimization, and performance monitoring."),
    ("LoRA", "Low-Rank Adaptation", "An efficient fine-tuning technique for large language models that adds trainable low-rank matrices to model layers. LoRA significantly reduces the number of trainable parameters while maintaining performance, making fine-tuning more accessible."),
    ("LSTM", "Long Short-Term Memory", "A recurrent neural network architecture designed to handle long-term dependencies in sequential data. LSTMs use gating mechanisms to selectively remember or forget information, making them effective for tasks like language modeling and time series prediction."),
    ("Meta AI", "Meta AI Research", "The artificial intelligence research and development division of Meta Platforms. Meta AI works on advancing AI technologies across computer vision, natural language processing, robotics, and other domains."),
    ("Meta Prompt", "Meta Prompting Technique", "A prompting strategy where an initial prompt provides structure, context, or instructions for generating or processing subsequent prompts. Meta prompts help organize complex interactions with language models."),
    ("ML", "Machine Learning", "A subset of artificial intelligence focused on developing algorithms that enable computers to learn from and make predictions or decisions based on data. Machine learning systems improve their performance through experience without being explicitly programmed."),
    ("MLOps", "Machine Learning Operations", "A set of practices that combines machine learning, DevOps, and data engineering to deploy and maintain ML models in production reliably and efficiently. MLOps encompasses model training, versioning, deployment, monitoring, and retraining."),
    ("Model Card", "Model Documentation Card", "Standardized documentation that provides essential information about machine learning models, including intended use, training data, performance metrics, limitations, and ethical considerations. Model cards promote transparency and responsible AI deployment."),
    ("Model Compression", "Model Compression Technique", "Methods for reducing the size and computational requirements of machine learning models while preserving performance. Techniques include pruning, quantization, knowledge distillation, and architecture optimization."),
    ("Multi-modal Learning", "Multi-modal Machine Learning", "An approach that enables models to process and integrate information from multiple modalities such as text, images, audio, and video. Multi-modal learning creates richer representations and enables applications like image captioning and video understanding."),
    ("NER", "Named Entity Recognition", "A natural language processing task that identifies and classifies named entities (people, organizations, locations, dates, etc.) in text. NER is fundamental to information extraction and knowledge graph construction."),
    ("OCR", "Optical Character Recognition", "Technology that converts images of text into machine-readable text format. OCR enables digitization of printed documents, automatic data entry, and accessibility features for visually impaired users."),
    ("ONNX", "Open Neural Network Exchange", "An open format for representing machine learning models that enables interoperability between different frameworks. ONNX allows models trained in one framework to be deployed in another, facilitating model portability."),
    ("Online Learning", "Online Learning Method", "A machine learning paradigm where models are updated continuously as new data arrives, rather than being trained on a fixed dataset. Online learning is essential for applications with streaming data or evolving patterns."),
    ("OpenAI", "OpenAI Organization", "An artificial intelligence research organization focused on developing safe and beneficial AI. OpenAI has created influential models like GPT, DALL·E, and ChatGPT, advancing the field of generative AI."),
    ("Outlier Detection", "Outlier Detection Method", "The process of identifying data points that significantly deviate from the majority of the data. Outlier detection is crucial for data quality, fraud detection, system monitoring, and understanding unusual patterns."),
    ("Overfitting", "Overfitting Problem", "A modeling error where a machine learning model learns the training data too well, including noise and outliers, resulting in poor generalization to new data. Overfitting is addressed through regularization, cross-validation, and appropriate model complexity."),
    ("Parameter", "Model Parameter", "Learnable weights and biases within a machine learning model that are adjusted during training to minimize loss. The number of parameters often indicates model capacity and computational requirements."),
    ("Pinecone", "Pinecone Vector Database", "A managed vector database service optimized for storing and querying high-dimensional embeddings. Pinecone enables efficient similarity search for applications like recommendation systems, semantic search, and retrieval-augmented generation."),
    ("Pretraining", "Model Pretraining", "The initial phase of training where a model learns general features from large datasets before being fine-tuned for specific tasks. Pretraining enables transfer learning and reduces the data requirements for downstream applications."),
    ("Prompt Engineering", "Prompt Engineering Practice", "The art and science of designing effective prompts to elicit desired responses from large language models. Prompt engineering involves crafting instructions, providing examples, and structuring queries to optimize model performance."),
    ("Pruning", "Neural Network Pruning", "A model compression technique that removes unnecessary weights, neurons, or layers from neural networks. Pruning reduces model size and computational cost while maintaining acceptable performance levels."),
    ("Q-Learning", "Q-Learning Algorithm", "A model-free reinforcement learning algorithm that learns the value of actions in different states. Q-learning enables agents to learn optimal policies through trial and error without requiring a model of the environment."),
    ("Qdrant", "Qdrant Vector Search", "An open-source vector similarity search engine designed for high-performance retrieval of embeddings. Qdrant supports filtering, payload storage, and distributed deployment for scalable vector search applications."),
    ("Quantization", "Model Quantization", "A technique that reduces the precision of model weights and activations from floating-point to lower-bit representations. Quantization significantly decreases model size and inference time with minimal accuracy loss."),
    ("RAG", "Retrieval-Augmented Generation", "An approach that enhances language model outputs by retrieving relevant information from external knowledge sources before generation. RAG improves factual accuracy and enables models to access up-to-date information."),
    ("Recall", "Recall Metric", "A performance metric that measures the proportion of actual positive cases correctly identified by a model. Recall is calculated as true positives divided by the sum of true positives and false negatives."),
    ("ReLU", "Rectified Linear Unit", "An activation function that outputs the input directly if positive, otherwise outputs zero. ReLU is widely used in neural networks due to its simplicity, computational efficiency, and effectiveness in addressing vanishing gradient problems."),
    ("Reranking", "Result Reranking", "A process that reorders search or retrieval results using more sophisticated models to improve relevance. Reranking typically follows an initial retrieval stage and applies computationally expensive models to a smaller candidate set."),
    ("Reward Model", "Reward Model System", "A model that assigns scores to outputs based on desired qualities, used in reinforcement learning from human feedback. Reward models guide language model behavior by providing learning signals aligned with human preferences."),
    ("RL", "Reinforcement Learning", "A machine learning paradigm where agents learn to make decisions by interacting with an environment and receiving rewards or penalties. RL has achieved remarkable success in game playing, robotics, and autonomous systems."),
    ("RLHF", "Reinforcement Learning from Human Feedback", "A technique for fine-tuning language models using human preferences as reward signals. RLHF aligns model behavior with human values and has been instrumental in creating helpful, harmless, and honest AI assistants."),
    ("RNN", "Recurrent Neural Network", "A neural network architecture designed for sequential data that maintains hidden states to capture temporal dependencies. RNNs process sequences element by element, making them suitable for tasks like language modeling and time series analysis."),
    ("ROC", "Receiver Operating Characteristic", "A graphical plot that illustrates the diagnostic ability of binary classifiers as discrimination thresholds vary. ROC curves plot true positive rate against false positive rate, helping evaluate and compare model performance."),
    ("Sampling", "Sampling Strategy", "The process of selecting a subset of data from a larger population or generating outputs from a probability distribution. In generative models, sampling techniques like temperature scaling and top-k sampling control output diversity."),
    ("SDXL", "Stable Diffusion XL", "An advanced version of the Stable Diffusion text-to-image model with improved architecture and training. SDXL generates higher quality images with better composition, lighting, and adherence to prompts."),
    ("Segmentation", "Data Segmentation", "The process of dividing data into meaningful groups or regions. In computer vision, segmentation identifies object boundaries; in marketing, it groups customers with similar characteristics for targeted strategies."),
    ("Self-attention", "Self-attention Mechanism", "A mechanism that allows models to weigh the importance of different parts of the input when processing each element. Self-attention is the core component of transformer architectures, enabling models to capture long-range dependencies."),
    ("SHAP", "SHapley Additive exPlanations", "A method for explaining individual predictions of machine learning models based on game theory. SHAP values quantify each feature's contribution to a prediction, providing interpretable and consistent explanations."),
    ("Stable Diffusion", "Stable Diffusion Model", "An open-source text-to-image diffusion model that generates high-quality images from textual descriptions. Stable Diffusion has democratized AI image generation by being computationally efficient and freely available."),
    ("SVM", "Support Vector Machine", "A supervised learning algorithm that finds the optimal hyperplane separating different classes in feature space. SVMs are effective for classification tasks and can handle non-linear boundaries through kernel functions."),
    ("Tensor", "Tensor Data Structure", "A multi-dimensional array used to represent data in machine learning frameworks. Tensors generalize scalars, vectors, and matrices to arbitrary dimensions, enabling efficient computation on modern hardware."),
    ("TensorFlow", "TensorFlow Framework", "An open-source machine learning framework developed by Google that provides comprehensive tools for building and deploying ML models. TensorFlow supports various platforms and offers both high-level and low-level APIs."),
    ("Token", "Text Token", "The smallest unit of text processed by natural language models, which can be a word, subword, or character. Tokenization breaks text into tokens, enabling models to process and generate language efficiently."),
    ("Tokenization", "Tokenization Process", "The process of breaking text into smaller units (tokens) for processing by language models. Tokenization strategies balance vocabulary size, semantic meaning, and computational efficiency."),
    ("Transfer Learning", "Transfer Learning Approach", "A technique that applies knowledge gained from solving one problem to a different but related problem. Transfer learning reduces training time and data requirements by leveraging pre-trained models."),
    ("Transformer", "Transformer Architecture", "A neural network architecture based on self-attention mechanisms that processes sequences in parallel rather than sequentially. Transformers have revolutionized NLP and are increasingly used in computer vision and other domains."),
    ("TTS", "Text-to-Speech", "Technology that converts written text into spoken audio. TTS systems use deep learning to generate natural-sounding speech with appropriate prosody, intonation, and emotion."),
    ("Underfitting", "Underfitting Problem", "A modeling error where a machine learning model is too simple to capture the underlying patterns in the data, resulting in poor performance on both training and test sets. Underfitting is addressed by increasing model complexity or improving features."),
    ("Unsupervised Learning", "Unsupervised Learning Method", "A machine learning paradigm where models learn patterns from unlabeled data without explicit target outputs. Unsupervised learning includes clustering, dimensionality reduction, and anomaly detection."),
    ("Validation Set", "Validation Dataset", "A portion of data held out during training to evaluate model performance and tune hyperparameters. The validation set helps prevent overfitting and guides model selection without contaminating the final test set."),
    ("Vector", "Vector Representation", "A numerical representation of data as an ordered array of numbers. Vectors enable mathematical operations on diverse data types and are fundamental to machine learning algorithms."),
    ("Vector Database", "Vector Database System", "A specialized database optimized for storing, indexing, and querying high-dimensional vector embeddings. Vector databases enable efficient similarity search for AI applications like semantic search and recommendation."),
    ("Vision Transformer (ViT)", "Vision Transformer Model", "An adaptation of the transformer architecture for computer vision tasks that treats images as sequences of patches. ViTs have achieved competitive or superior performance compared to convolutional networks on many vision tasks."),
    ("Weights", "Neural Network Weights", "Learnable parameters in neural networks that determine the strength of connections between neurons. Weights are adjusted during training through optimization algorithms to minimize loss and improve predictions."),
    ("Whisper", "Whisper Speech Recognition", "An automatic speech recognition model developed by OpenAI that achieves robust performance across multiple languages and acoustic conditions. Whisper is trained on diverse audio data and handles various accents and background noise."),
    ("XAI", "Explainable Artificial Intelligence", "A field focused on creating AI systems whose decisions and processes can be understood by humans. XAI techniques provide transparency, build trust, and enable debugging and validation of AI systems."),
    ("YOLO", "You Only Look Once", "A real-time object detection algorithm that processes entire images in a single forward pass. YOLO's speed and accuracy make it popular for applications requiring fast object detection like autonomous driving and surveillance."),
    ("Zero-shot Learning", "Zero-shot Learning Capability", "The ability of models to perform tasks without any task-specific training examples. Zero-shot learning relies on transferring knowledge from related tasks or leveraging pre-trained representations."),
]

# Hero section
st.markdown("""
<div class="hero-section">
    <div class="hero-title">🤖 AI Glossary</div>
    <div class="hero-subtitle">Your Comprehensive Guide to Artificial Intelligence Terms & Concepts</div>
</div>
""", unsafe_allow_html=True)

# Statistics
total_terms = len(ai_terms)
unique_letters = len(set(term[0][0].upper() for term in ai_terms))

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-number">{total_terms}+</div>
        <div class="stat-label">AI Terms</div>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-number">{unique_letters}</div>
        <div class="stat-label">Categories</div>
    </div>
    """, unsafe_allow_html=True)
with col3:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-number">100%</div>
        <div class="stat-label">Free Access</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Introduction
st.markdown("""
### Welcome to the AI Glossary

Artificial Intelligence is transforming every aspect of our lives, from how we work and communicate to how we solve complex problems. 
This comprehensive glossary provides clear, detailed explanations of essential AI terms, acronyms, and concepts. Whether you're a 
student, professional, researcher, or simply curious about AI, this resource will help you navigate the rapidly evolving landscape 
of artificial intelligence and machine learning.

Each term includes not just a brief definition, but also context about its significance, applications, and relationships to other 
concepts in the field. Use the search function below to quickly find specific terms, or browse through categories to discover new 
concepts and deepen your understanding of AI.
""")

st.markdown("---")

# CSV Download
df = pd.DataFrame([(term[0], term[1], term[2]) for term in ai_terms], 
                  columns=["Acronym/Term", "Full Name", "Description"])
csv = df.to_csv(index=False).encode("utf-8")
st.download_button("📥 Download Complete Glossary as CSV", csv, "ai_glossary_complete.csv", "text/csv", use_container_width=True)

st.markdown("---")

# Search Bar
st.markdown("### 🔍 Search the Glossary")
query = st.text_input("Enter a term, acronym, or keyword to search", placeholder="e.g., transformer, neural network, GPT...").lower()

# Filter terms
if query:
    filtered_terms = [item for item in ai_terms if query in item[0].lower() or query in item[1].lower() or query in item[2].lower()]
    st.info(f"Found {len(filtered_terms)} result(s) for '{query}'")
else:
    filtered_terms = ai_terms

# Group by first letter
grouped = defaultdict(list)
for term, full_name, description in filtered_terms:
    grouped[term[0].upper()].append((term, full_name, description))

# Display cards
st.markdown("---")
st.markdown("### 📚 Browse Terms by Category")

for letter in sorted(grouped):
    st.markdown(f'<div class="category-header">📖 {letter} — {len(grouped[letter])} Terms</div>', unsafe_allow_html=True)
    
    for term, full_name, description in grouped[letter]:
        st.markdown(f"""
        <div class="term-card">
            <div class="term-title">{term}</div>
            <div class="term-definition"><strong>{full_name}</strong></div>
            <div class="term-definition" style="margin-top: 10px;">{description}</div>
        </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 20px; color: #666;">
    <p><strong>AI Glossary</strong> — Continuously updated with the latest terms and concepts in artificial intelligence</p>
    <p>Stay curious, keep learning, and explore the fascinating world of AI! 🚀</p>
</div>
""", unsafe_allow_html=True)
