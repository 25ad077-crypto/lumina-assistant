import os
import json
import time
from datetime import datetime
import streamlit as st
from dotenv import load_dotenv

# Load local environment variables if available
load_dotenv()

# Streamlit Page Setup
st.set_page_config(
    page_title="Lumina Assistant",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# System Personas Presets
PERSONAS = {
    "🌟 Helpful Assistant": (
        "You are a helpful, empathetic, and highly capable AI assistant. "
        "Answer questions clearly, thoughtfully, and accurately."
    ),
    "💻 Senior AI & Software Engineer": (
        "You are an expert Senior Software Engineer and AI Systems Architect. "
        "Provide production-ready, clean, secure code with brief explanations, "
        "best practices, and actionable trade-offs."
    ),
    "⚡ Concise Executive": (
        "You are a concise executive advisor. Keep responses short, direct, "
        "action-oriented, and formatted using high-impact bullet points."
    ),
    "📝 Creative Writer": (
        "You are an imaginative creative writer and storyteller. "
        "Use vivid descriptions, engaging narrative pacing, and expressive tone."
    ),
    "🛠️ Custom Persona": ""
}

# State Management
if "messages" not in st.session_state:
    st.session_state.messages = []

if "api_key_input" not in st.session_state:
    st.session_state.api_key_input = ""

# Resolve API Key

def get_groq_api_key():
    # 1. Check Streamlit secrets (Cloud deployment)
    if hasattr(st, "secrets") and "GROQ_API_KEY" in st.secrets:
        return st.secrets["GROQ_API_KEY"]
    # 2. Check environment variable (.env)
    env_key = os.getenv("GROQ_API_KEY")
    if env_key:
        return env_key
    # 3. Check sidebar input
    if st.session_state.api_key_input.strip():
        return st.session_state.api_key_input.strip()
    return None

# -----------------------------------------------------------------------------
# Sidebar: Configuration & Controls
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("## ⚡ **AI Engine Settings**")
    st.caption("Powered by open-source LLMs & Groq Free Tier")

    current_api_key = get_groq_api_key()

    # API Key Input
    if not current_api_key:
        st.warning("🔑 No API Key detected")
        key_input = st.text_input(
            "Enter Groq API Key:",
            type="password",
            placeholder="gsk_...",
            help="Get your 100% free key with no credit card at https://console.groq.com",
            key="api_key_field"
        )
        if key_input:
            st.session_state.api_key_input = key_input
            st.rerun()
        st.markdown(
            "👉 **[Get Free Key at Groq Console](https://console.groq.com)**\n"
            "*(Sign in with Google/GitHub — zero credit card required)*"
        )
    else:
        st.success("✅ API Key active")
        with st.expander("Change API Key"):
            new_key = st.text_input("New Groq Key:", type="password", key="change_key_field")
            if st.button("Update Key"):
                st.session_state.api_key_input = new_key
                st.rerun()

    st.markdown("---")

    # Model Selection
    model_choice = st.selectbox(
        "🧠 Model Architecture",
        options=[
            "llama-3.3-70b-versatile",
            "llama-3.1-8b-instant",
            "gemma2-9b-it",
            "mixtral-8x7b-32768"
        ],
        index=0,
        help="Llama 3.3 70B: highest reasoning intelligence.\nLlama 3.1 8B: ultra-fast low-latency."
    )

    # Persona Selection
    persona_choice = st.selectbox(
        "🎭 Assistant Persona",
        options=list(PERSONAS.keys()),
        index=0
    )

    if persona_choice == "🛠️ Custom Persona":
        system_instruction = st.text_area(
            "Custom System Prompt:",
            value="You are a helpful AI assistant.",
            height=120
        )
    else:
        system_instruction = PERSONAS[persona_choice]

    # Hyperparameters
    st.markdown("### 🎛️ Parameters")
    temperature = st.slider(
        "Temperature (Creativity)",
        min_value=0.0,
        max_value=1.0,
        value=0.7,
        step=0.05,
        help="0.0 = Deterministic and precise. 1.0 = Highly creative."
    )

    max_tokens = st.slider(
        "Max Output Tokens",
        min_value=256,
        max_value=4096,
        value=2048,
        step=256,
        help="Maximum length of the generated response."
    )

    memory_window = st.slider(
        "Context Memory (Turns)",
        min_value=2,
        max_value=20,
        value=10,
        step=2,
        help="How many previous conversation turns are retained in context."
    )

    st.markdown("---")

    # Session Management & Export
    st.markdown("### 💾 Conversation Actions")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🧹 Clear", use_container_width=True):
            st.session_state.messages = []
            st.rerun()

    with col2:
        # Download conversation as Markdown
        if st.session_state.messages:
            md_content = f"# Chat Conversation Export - {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
            for m in st.session_state.messages:
                md_content += f"**{m['role'].upper()}:**\n{m['content']}\n\n---\n\n"
            st.download_button(
                label="📥 Export",
                data=md_content,
                file_name=f"chat_export_{int(time.time())}.md",
                mime="text/markdown",
                use_container_width=True
            )
        else:
            st.button("📥 Export", disabled=True, use_container_width=True)

    # Chat Statistics
    msg_count = len(st.session_state.messages)
    user_msgs = len([m for m in st.session_state.messages if m["role"] == "user"])
    st.caption(f"📊 Stats: {msg_count} total messages ({user_msgs} user queries)")

# Main Chat Area

header_col1, header_col2 = st.columns([0.8, 0.2])
with header_col1:
    st.title("⚡ Lumina Assistant")
    st.caption(f"Active Model: `{model_choice}` • Zero-Cost Cloud Architecture")
with header_col2:
    if current_api_key:
        st.markdown(
            '<div style="text-align: right; padding-top: 15px;">'
            '<span style="background-color: #064E3B; color: #34D399; padding: 4px 10px; border-radius: 9999px; font-size: 0.85rem; font-weight: 600;">'
            '● Live Connected</span></div>',
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            '<div style="text-align: right; padding-top: 15px;">'
            '<span style="background-color: #78350F; color: #FBBF24; padding: 4px 10px; border-radius: 9999px; font-size: 0.85rem; font-weight: 600;">'
            '○ Key Required</span></div>',
            unsafe_allow_html=True
        )

# Welcome banner if conversation is empty
if not st.session_state.messages:
    with st.container():
        st.markdown(
            """
            ### Welcome to Lumina Assistant! 👋
            This application is built entirely with **free, open-source AI tools**:
            * **Ultra-Fast Open Models**: Llama 3.3 70B, Llama 3.1 8B, and Gemma 2 via Groq's free tier.
            * **Zero Cost & No Credit Card**: 100% free forever for development and personal projects.
            * **Privacy Friendly**: Real-time token streaming with local session state.
            """
        )
        st.markdown("---")

# Render Conversation History
for msg in st.session_state.messages:
    avatar = "👤" if msg["role"] == "user" else "⚡"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

# User Input Box
if prompt := st.chat_input("Ask Lumina anything..."):
    active_key = get_groq_api_key()
    
    if not active_key:
        st.error("⚠️ Please provide a Groq API Key in the left sidebar to start chatting. You can get one for free at https://console.groq.com (no credit card needed).")
        st.stop()

    # 1. Append and render user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    # 2. Slice messages according to memory window
    recent_history = st.session_state.messages[-(memory_window * 2):]

    # 3. Build payload with system prompt
    payload = [{"role": "system", "content": system_instruction}]
    for m in recent_history:
        payload.append({"role": m["role"], "content": m["content"]})

    # 4. Stream response from Groq
    with st.chat_message("assistant", avatar="⚡"):
        response_box = st.empty()
        full_response = ""
        
        try:
            from groq import Groq
            client = Groq(api_key=active_key)
            
            stream = client.chat.completions.create(
                model=model_choice,
                messages=payload,
                temperature=temperature,
                max_tokens=max_tokens,
                stream=True,
            )
            
            for chunk in stream:
                delta = chunk.choices[0].delta.content or ""
                full_response += delta
                response_box.markdown(full_response + "▌")
                
            response_box.markdown(full_response)
            
            # Save assistant message in state
            st.session_state.messages.append({
                "role": "assistant",
                "content": full_response
            })
            
        except Exception as err:
            err_msg = str(err)
            if "invalid_api_key" in err_msg.lower() or "401" in err_msg:
                response_box.error("❌ Invalid API Key. Please verify your Groq API key in the sidebar.")
            elif "rate_limit_exceeded" in err_msg.lower() or "429" in err_msg:
                response_box.warning("⏳ Groq free rate limit reached for this minute. Please wait ~20 seconds and retry.")
            else:
                response_box.error(f"⚠️ Error: {err_msg}")
