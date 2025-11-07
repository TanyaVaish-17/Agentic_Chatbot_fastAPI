import streamlit as st
import requests

# --- Page Setup ---
st.set_page_config(page_title="Veya Intelligent System", layout="wide")

# --- Sidebar ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712109.png", width=120)  # slightly bigger here too
    st.markdown("### ⚙️ Settings")

    theme = st.radio("Theme", ["Dark", "Light"], index=0)

    provider = st.selectbox("Model Provider", ["Groq", "OpenAI"])
    if provider == "Groq":
        selected_model = st.selectbox("Groq Models", ["llama-3.3-70b-versatile", "mixtral-8x7b-32768"])
    else:
        selected_model = st.selectbox("OpenAI Models", ["gpt-4o-mini"])

    st.markdown("---")
    st.markdown("### 🧠 Veya Intelligent System")
    st.write("Seamlessly create, define, and interact with custom AI Agents powered by Groq or OpenAI.")

# --- Global Theme CSS (applies to whole page) ---
if theme == "Dark":
    page_bg = "#0E1117"
    container_bg = "#0B0D12"
    card_bg = "#1E1E2F"
    text_color = "#DDD"
    muted = "#AAA"
else:
    page_bg = "#F7F7F7"
    container_bg = "#FFFFFF"
    card_bg = "#F2F2F6"
    text_color = "#111"
    muted = "#666"

st.markdown(
    f"""
    <style>
    /* root level backgrounds */
    html, body, [data-testid="stAppViewContainer"], .stApp, .css-1d391kg {{
        background-color: {page_bg} !important;
        color: {text_color} !important;
    }}

    /* main content container (center column) */
    .block-container {{
        background-color: transparent !important;
    }}

    /* sidebar */
    .css-1d391kg, .stSidebar {{
        background-color: {container_bg} !important;
        color: {text_color} !important;
    }}

    /* header / text areas / inputs */
    .stTextArea>div>div>textarea, .stTextInput>div>input, .stTextArea>div>div, textarea {{
        background-color: {card_bg} !important;
        color: {text_color} !important;
        border: 1px solid rgba(255,255,255,0.06) !important;
    }}

    /* buttons */
    .stButton>button {{
        background-color: #A259FF !important;
        color: white !important;
        border-radius: 8px !important;
        border: none !important;
        padding: .6rem 1.1rem !important;
        font-weight: 600 !important;
    }}
    .stButton>button:hover {{
        filter: brightness(.95);
    }}

    /* response card */
    .agent-response {{
        background-color: {card_bg} !important;
        color: {text_color} !important;
        padding: 16px;
        border-radius: 10px;
    }}

    /* header layout: robot beside centered text (keeps text centered like before) */
    .veya-header {{
        display:flex;
        align-items:center;
        justify-content:center;
        gap:16px;
        margin-top:-8px;
        margin-bottom: 8px;
    }}
    .veya-header img {{
        width:140px;             /* larger robot image */
        height:140px;
        object-fit:contain;
    }}
    .veya-title {{
        text-align:center;       /* keep centered text (as you requested) */
        line-height:0.95;
    }}
    .veya-title h1 {{
        color:#A259FF;
        margin:0;
        font-size:42px;
    }}
    .veya-title p {{
        margin:0;
        color: {muted};
    }}

    /* small screens: stack robot above text */
    @media (max-width: 720px) {{
        .veya-header {{
            flex-direction: column;
            gap:6px;
        }}
        .veya-header img {{ width:110px; height:110px; }}
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# --- Header with larger Robot Icon beside centered text ---
st.markdown(
    """
    <div class="veya-header">
        <img src="https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExY2x2YTh2cXl0eGhpdWU2cGF5NDNuMWUxdnRvdGs5eDRzNzRicXl1OSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9cw/TcqEqZZ2KwSSDyy6BI/giphy.gif" alt="robot">
        <div class="veya-title">
            <h1>Veya</h1>
            <p>AI Chatbot Agents</p>
            <p style="font-size:14px;">Define. Create. Interact with your Intelligent Agents.</p>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# --- Define Agent Section ---
st.markdown("#### 💬 Define your AI Agent")
system_prompt = st.text_area(" ", height=70, placeholder="Describe what your agent should do...")

allow_web_search = st.checkbox("🔍 Allow Web Search")

# --- Chat Section ---
st.markdown("#### 🤖 Enter your Query")
user_query = st.text_area(" ", height=150, placeholder="Ask anything...")

col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    ask_button = st.button("🚀 Ask Agent!", use_container_width=True)

# --- Response Display ---
if ask_button:
    if user_query.strip():
        API_URL = "https://agentic-chatbot-fastapi-k9jt.onrender.com/chat"
        payload = {
            "model_name": selected_model,
            "model_provider": provider,
            "system_prompt": system_prompt,
            "messages": [user_query],
            "allow_search": allow_web_search
        }

        try:
            response = requests.post(API_URL, json=payload, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if "error" in data:
                    st.error(data["error"])
                else:
                    st.markdown("### 🧩 Agent Response")
                    st.markdown(f'<div class="agent-response">{data}</div>', unsafe_allow_html=True)
            else:
                st.error("⚠️ Failed to connect with backend.")
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.warning("Please enter a query before asking the agent.")
