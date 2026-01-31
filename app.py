"""
GenAI Learning Assistant - Fixed UI (Broader Bubbles)
"""

import streamlit as st
import requests
import os
from datetime import datetime

# ===== PAGE CONFIG =====
st.set_page_config(
    page_title="GenAI Learning Assistant",
    page_icon="🎓",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ===== CONFIG =====
API_URL = "http://127.0.0.1:8000"  # No trailing space!
API_KEY = "super-secret-key"
# Default to localhost for testing, but allow Cloud to override it
API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

# ===== SESSION STATE =====
if "messages" not in st.session_state:
    st.session_state.messages = []
if "is_processing" not in st.session_state:
    st.session_state.is_processing = False

# ===== CUSTOM CSS =====
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%);
    }
    
    .main-title {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.5rem;
        font-weight: 800;
        text-align: center;
        margin-top: 20px;
        margin-bottom: 10px;
    }
    
    .subtitle {
        text-align: center;
        color: rgba(255,255,255,0.6);
        margin-bottom: 30px;
    }
    
    .chat-container {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 20px;
        padding: 20px;
        margin: 0 auto;
        max-width: 800px;
        min-height: 400px;
        backdrop-filter: blur(10px);
    }
    
    .welcome-box {
        text-align: center;
        padding: 80px 20px;
        color: rgba(255,255,255,0.8);
    }
    
    .welcome-icon {
        font-size: 4rem;
        margin-bottom: 20px;
    }
    
    /* MODIFIED: Increased max-width to 95% for broader bubbles */
    .message-user {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 12px 18px;
        border-radius: 18px 18px 4px 18px;
        margin: 10px 0 10px auto;
        max-width: 95%; /* BROADER */
        width: fit-content;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    /* MODIFIED: Increased max-width to 95% for broader bubbles */
    .message-assistant {
        background: rgba(255,255,255,0.1);
        color: #e2e8f0;
        padding: 12px 18px;
        border-radius: 18px 18px 18px 4px;
        margin: 10px auto 10px 0;
        max-width: 95%; /* BROADER */
        width: fit-content;
        border: 1px solid rgba(255,255,255,0.1);
    }
    
    .loader {
        display: flex;
        flex-direction: column;
        align-items: center;
        padding: 40px;
        gap: 15px;
    }
    
    .spinner {
        width: 40px;
        height: 40px;
        border: 3px solid rgba(102,126,234,0.3);
        border-top-color: #667eea;
        border-radius: 50%;
        animation: spin 1s linear infinite;
    }
    
    @keyframes spin { to { transform: rotate(360deg); } }
</style>
""", unsafe_allow_html=True)

# ===== SIDEBAR =====
with st.sidebar:
    st.title("🎓 Settings")
    
    api_url = st.text_input("API URL", value=API_URL)
    api_key = st.text_input("API Key", value=API_KEY, type="password")
    
    if st.button("Test Connection"):
        try:
            r = requests.get(f"{api_url}/health", timeout=5)
            st.success("✅ Connected") if r.status_code == 200 else st.error("❌ Failed")
        except:
            st.error("❌ Error")
    
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()
    
    st.markdown("### Quick Prompts")
    for prompt in ["What is a loop?", "Explain recursion", "Debug my code"]:
        if st.button(prompt, key=prompt):
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.session_state.is_processing = True
            st.rerun()

# ===== MAIN UI =====
st.markdown('<h1 class="main-title">🎓 GenAI Learning Assistant</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Your personal AI programming tutor</p>', unsafe_allow_html=True)

# ===== CHAT AREA (No container div to avoid blank box) =====
if not st.session_state.messages:
    # Show welcome screen directly (no box)
    st.markdown("""
    <div class="welcome-box">
        <div class="welcome-icon">👋</div>
        <h3 style="color: white; margin-bottom: 15px;">Welcome!</h3>
        <p style="color: rgba(255,255,255,0.7); font-size: 1.1rem;">
            Ask me anything about programming. I'll adapt to your level!<br><br>
            <span style="font-size: 0.9rem;">🐍 Python &nbsp; 💡 Concepts &nbsp; 🐛 Debugging &nbsp; ⚡ Optimization</span>
        </p>
    </div>
    """, unsafe_allow_html=True)
else:
    # Show messages in a container
    with st.container():
        for msg in st.session_state.messages:
            if msg["role"] == "user":
                st.markdown(f'<div class="message-user">{msg["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="message-assistant">{msg["content"]}</div>', unsafe_allow_html=True)
        
        # Loading
        if st.session_state.is_processing:
            st.markdown("""
            <div class="loader">
                <div class="spinner"></div>
                <div style="color: rgba(255,255,255,0.7);">Thinking...</div>
            </div>
            """, unsafe_allow_html=True)

# ===== INPUT (Always at bottom) =====
prompt = st.chat_input("Ask me anything about programming...")

if prompt:
    st.session_state.messages.append({
        "role": "user",
        "content": prompt,
        "timestamp": datetime.now().strftime("%H:%M")
    })
    st.session_state.is_processing = True
    st.rerun()

# ===== PROCESS =====
if st.session_state.is_processing and st.session_state.messages[-1]["role"] == "user":
    last_msg = st.session_state.messages[-1]["content"]
    
    try:
        response = requests.post(
            f"{api_url}/ask",
            json={"user_input": last_msg},
            headers={"Authorization": f"Bearer {api_key}"},
            timeout=120
        )
        
        if response.status_code == 200:
            answer = response.json().get("response", "No response")
        else:
            answer = f"❌ Error {response.status_code}"
            
    except Exception as e:
        answer = f"❌ Cannot connect to API. Make sure the server is running!"
    
    st.session_state.messages.append({
        "role": "assistant",
        "content": answer,
        "timestamp": datetime.now().strftime("%H:%M")
    })
    st.session_state.is_processing = False
    st.rerun()