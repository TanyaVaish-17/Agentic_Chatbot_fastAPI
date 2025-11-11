import streamlit as st
import requests
from datetime import datetime
import json

st.set_page_config(
    page_title="Veya Intelligent System", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Model information
MODEL_INFO = {
    "llama-3.3-70b-versatile": {
        "tokens": "70B parameters",
        "speed": "Fast",
        "description": "Versatile model for general tasks"
    },
    "mixtral-8x7b-32768": {
        "tokens": "32K context",
        "speed": "Very Fast",
        "description": "Great for long context tasks"
    },
    "gpt-4o-mini": {
        "tokens": "128K context",
        "speed": "Fast",
        "description": "OpenAI's efficient mini model"
    }
}

# Example prompts
EXAMPLE_PROMPTS = {
    "📊 Business Analyst": {
        "system": "You are an expert business analyst who provides data-driven insights and strategic recommendations.",
        "query": "What are the key trends in the e-commerce industry for 2025?"
    },
    "💻 Code Helper": {
        "system": "You are a senior software engineer who helps with coding problems and best practices.",
        "query": "Explain how to implement a REST API using FastAPI with authentication."
    },
    "📰 News Summarizer": {
        "system": "You are a news analyst who summarizes current events objectively and concisely.",
        "query": "What are the latest developments in AI technology this week?"
    },
    "✍️ Content Writer": {
        "system": "You are a creative content writer who crafts engaging and informative content.",
        "query": "Write a compelling blog post introduction about sustainable living."
    }
}

# --- Sidebar ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712109.png", width=120)
    st.markdown("### ⚙️ Settings")

    theme = st.radio("Theme", ["Dark", "Light"], index=0)

    provider = st.selectbox("Model Provider", ["Groq", "OpenAI"])
    if provider == "Groq":
        selected_model = st.selectbox("Groq Models", ["llama-3.3-70b-versatile", "mixtral-8x7b-32768"])
    else:
        selected_model = st.selectbox("OpenAI Models", ["gpt-4o-mini"])

    # Model Info Card
    if selected_model in MODEL_INFO:
        info = MODEL_INFO[selected_model]
        st.markdown(f"""
        <div style="background: rgba(162, 89, 255, 0.1); padding: 12px; border-radius: 8px; margin-top: 10px; border-left: 3px solid #A259FF;">
            <div style="font-size: 12px; opacity: 0.8;">MODEL INFO</div>
            <div style="font-weight: 600; margin: 4px 0;">{info['tokens']}</div>
            <div style="font-size: 13px; opacity: 0.9;">⚡ {info['speed']}</div>
            <div style="font-size: 12px; opacity: 0.7; margin-top: 4px;">{info['description']}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("---")
    st.markdown("### 🧠 Veya Intelligent System")
    st.write("Seamlessly create, define, and interact with custom AI Agents powered by Groq or OpenAI.")

# --- Global Theme CSS ---
if theme == "Dark":
    page_bg = "#0E1117"
    container_bg = "#1A1C24"
    card_bg = "#262730"
    text_color = "#FFFFFF"
    muted = "#B8B8B8"
    input_bg = "#1E1E2F"
    border_color = "rgba(255,255,255,0.08)"
    label_color = "#E0E0E0"
    example_bg = "#1E1E2F"
    example_hover = "#2A2A3F"
else:
    page_bg = "#F7F7F7"
    container_bg = "#FFFFFF"
    card_bg = "#F2F2F6"
    text_color = "#111111"
    muted = "#666666"
    input_bg = "#FFFFFF"
    border_color = "rgba(0,0,0,0.1)"
    label_color = "#333333"
    example_bg = "#F8F9FA"
    example_hover = "#E9ECEF"

st.markdown(
    f"""
    <style>
    .block-container {{
        padding-top: 1rem !important;
        padding-bottom: 0rem !important;
        max-width: 1200px !important;
    }}
    
    html, body, [data-testid="stAppViewContainer"], .stApp {{
        background-color: {page_bg} !important;
        color: {text_color} !important;
    }}
    
    [data-testid="stSidebar"] {{
        background-color: {container_bg} !important;
    }}
    
    [data-testid="stSidebar"] * {{
        color: {text_color} !important;
    }}
    
    .stTextArea label, .stTextInput label, .stSelectbox label, .stRadio label, .stCheckbox label {{
        color: {label_color} !important;
        font-weight: 500 !important;
        font-size: 15px !important;
    }}
    
    .stTextArea>div>div>textarea, .stTextInput>div>input {{
        background-color: {input_bg} !important;
        color: {text_color} !important;
        border: 1px solid {border_color} !important;
        border-radius: 8px !important;
        font-size: 14px !important;
    }}
    
    .stTextArea>div>div>textarea::placeholder, .stTextInput>div>input::placeholder {{
        color: {muted} !important;
        opacity: 0.7 !important;
    }}
    
    .stSelectbox>div>div {{
        background-color: {input_bg} !important;
        color: {text_color} !important;
        border: 1px solid {border_color} !important;
    }}
    
    .stRadio>div {{
        background-color: transparent !important;
    }}
    
    .stCheckbox {{
        background-color: transparent !important;
    }}
    
    .stCheckbox span {{
        color: {text_color} !important;
    }}
    
    /* Buttons */
    .stButton>button {{
        background: linear-gradient(135deg, #A259FF 0%, #8B3FFF 100%) !important;
        color: white !important;
        border-radius: 10px !important;
        border: none !important;
        padding: 0.75rem 1.5rem !important;
        font-weight: 600 !important;
        font-size: 16px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 12px rgba(162, 89, 255, 0.3) !important;
    }}
    
    .stButton>button:hover {{
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 16px rgba(162, 89, 255, 0.4) !important;
    }}
    
    /* Response card with better styling */
    .agent-response {{
        background-color: {card_bg} !important;
        color: {text_color} !important;
        padding: 20px !important;
        border-radius: 12px !important;
        border: 1px solid {border_color} !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1) !important;
        line-height: 1.6 !important;
        margin-bottom: 20px !important;
    }}
    
    /* Example prompt card */
    .example-card {{
        background-color: {example_bg} !important;
        border: 1px solid {border_color} !important;
        border-radius: 10px !important;
        padding: 15px !important;
        cursor: pointer !important;
        transition: all 0.3s ease !important;
        margin-bottom: 10px !important;
    }}
    
    .example-card:hover {{
        background-color: {example_hover} !important;
        border-color: #A259FF !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 12px rgba(162, 89, 255, 0.2) !important;
    }}
    
    .example-title {{
        color: {text_color} !important;
        font-weight: 600 !important;
        font-size: 15px !important;
        margin-bottom: 6px !important;
    }}
    
    .example-text {{
        color: {muted} !important;
        font-size: 13px !important;
    }}
    
    /* Header layout */
    .veya-header {{
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 20px;
        margin-bottom: 30px;
        padding: 20px 0;
    }}
    
    .veya-header img {{
        width: 140px;
        height: 140px;
        object-fit: contain;
    }}
    
    .veya-title {{
        text-align: center;
    }}
    
    .veya-title h1 {{
        background: linear-gradient(135deg, #A259FF 0%, #FF6B9D 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0;
        font-size: 48px;
        font-weight: 700;
    }}
    
    .veya-title p {{
        margin: 4px 0 0 0;
        color: {muted};
        font-size: 16px;
    }}
    
    .veya-title .subtitle {{
        font-size: 14px !important;
        color: {muted} !important;
        margin-top: 2px !important;
    }}
    
    /* Section headers */
    .section-header {{
        color: {text_color} !important;
        font-size: 20px !important;
        font-weight: 600 !important;
        margin: 25px 0 12px 0 !important;
        display: flex !important;
        align-items: center !important;
        gap: 8px !important;
    }}
    
    /* Markdown headers */
    h4 {{
        color: {text_color} !important;
        font-weight: 600 !important;
    }}
    
    h3 {{
        color: {text_color} !important;
        font-weight: 600 !important;
    }}
    
    /* Success/Error/Warning messages */
    .stAlert {{
        background-color: {card_bg} !important;
        color: {text_color} !important;
        border-radius: 8px !important;
    }}
    
    /* Expander styling */
    .streamlit-expanderHeader {{
        background-color: {card_bg} !important;
        color: {text_color} !important;
        border-radius: 8px !important;
    }}
    /* Fix expander header white background in dark mode */
    details > summary {{
        background-color: {card_bg} !important;
        color: {text_color} !important;
        border-radius: 10px !important;
    }}

    /* Mobile responsiveness */
    @media (max-width: 720px) {{
        .veya-header {{
            flex-direction: column;
            gap: 10px;
        }}
        .veya-header img {{
            width: 110px;
            height: 110px;
        }}
        .veya-title h1 {{
            font-size: 36px;
        }}
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# --- Header Section---
st.markdown(
    """
    <div class="veya-header">
        <img src="https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExY2x2YTh2cXl0eGhpdWU2cGF5NDNuMWUxdnRvdGs5eDRzNzRicXl1OSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9cw/TcqEqZZ2KwSSDyy6BI/giphy.gif" alt="robot">
        <div class="veya-title">
            <h1>Veya</h1>
            <p><strong>AI Chatbot Agents</strong></p>
            <p class="subtitle">Define. Create. Interact with your Intelligent Agents.</p>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# --- Example Prompts Section ---
with st.expander("✨ Try Example Prompts", expanded=False):
    cols = st.columns(2)
    for idx, (title, content) in enumerate(EXAMPLE_PROMPTS.items()):
        with cols[idx % 2]:
            if st.button(
                f"{title}\n{content['query'][:50]}...",
                key=f"example_{idx}",
                use_container_width=True
            ):
                st.session_state.selected_example = content
                st.rerun()

if 'selected_example' in st.session_state:
    system_prompt_default = st.session_state.selected_example['system']
    query_default = st.session_state.selected_example['query']
else:
    system_prompt_default = ""
    query_default = ""

# --- Define Agent Section ---
st.markdown('<div class="section-header">💬 Define your AI Agent</div>', unsafe_allow_html=True)
system_prompt = st.text_area(
    "System Prompt",
    value=system_prompt_default,
    height=100,
    placeholder="e.g., You are a helpful business analyst who provides data-driven insights...",
    label_visibility="collapsed"
)

allow_web_search = st.checkbox("🔍 Allow Web Search", help="Enable web search for real-time information")
st.markdown("<br>", unsafe_allow_html=True)

# --- Chat Section ---
st.markdown('<div class="section-header">🤖 Enter your Query</div>', unsafe_allow_html=True)
user_query = st.text_area(
    "User Query",
    value=query_default,
    height=150,
    placeholder="e.g., What are the current trends in AI technology?",
    label_visibility="collapsed"
)
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    ask_button = st.button("🚀 Ask Agent!", use_container_width=True)

# --- Response Display ---
if ask_button:
    if user_query.strip():
        with st.spinner("🤔 Agent is thinking..."):
            API_URL = "https://agentic-chatbot-fastapi-k9jt.onrender.com/chat"
            payload = {
                "model_name": selected_model,
                "model_provider": provider,
                "system_prompt": system_prompt,
                "messages": [user_query],
                "allow_search": allow_web_search
            }

            try:
                response = requests.post(API_URL, json=payload, timeout=60)
                if response.status_code == 200:
                    data = response.json()
                    if "error" in data:
                        st.error(f"⚠️ {data['error']}")
                    else:
                        st.markdown("<br>", unsafe_allow_html=True)
                        st.markdown("### ✨ Agent Response")
                        response_text = data if isinstance(data, str) else str(data)
                        st.markdown(f'<div class="agent-response">{response_text}</div>', unsafe_allow_html=True)
                else:
                    st.error(f"⚠️ Backend returned status code: {response.status_code}")
            except requests.exceptions.Timeout:
                st.error("⏱️ Request timed out. The agent might be processing a complex query. Please try again.")
            except requests.exceptions.ConnectionError:
                st.error("🔌 Cannot connect to backend. Please check if the backend service is running.")
            except Exception as e:
                st.error(f"❌ Unexpected error: {str(e)}")
    else:
        st.warning("⚠️ Please enter a query before asking the agent.")

