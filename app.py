"""
GenAI Learning Assistant - Modern Streamlit UI
"""
import streamlit as st
import requests
import os
from datetime import datetime

# ===== CONFIGURATION =====
API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")
API_KEY = os.getenv("API_SECRET_KEY", "super-secret-key")

# ===== SESSION STATE =====
if "messages" not in st.session_state:
    st.session_state.messages = []
if "api_connected" not in st.session_state:
    st.session_state.api_connected = False
if "is_processing" not in st.session_state:
    st.session_state.is_processing = False

# ===== PAGE CONFIG =====
st.set_page_config(
    page_title="GenAI Learning Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===== CSS =====
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
.main { font-family: 'Inter', sans-serif; background: #0f0f23; }
.app-header { text-align: center; padding: 2.5rem 2rem; background: linear-gradient(90deg, #4f46e5, #7c3aed); border-radius: 24px; margin-bottom: 2rem; }
.app-header h1 { color: white !important; font-size: 2.8rem !important; font-weight: 700 !important; margin: 0 !important; }
.app-header p { color: rgba(255,255,255,0.8) !important; font-size: 1.1rem !important; margin-top: 0.5rem !important; }
.status-online { background: rgba(16, 185, 129, 0.15); color: #10b981; padding: 0.75rem 1rem; border-radius: 12px; border: 1px solid rgba(16, 185, 129, 0.3); }
.status-offline { background: rgba(239, 68, 68, 0.15); color: #ef4444; padding: 0.75rem 1rem; border-radius: 12px; border: 1px solid rgba(239, 68, 68, 0.3); }
.chat-wrapper { background: #1a1a2e; border-radius: 24px; padding: 1.5rem; margin-bottom: 1.5rem; border: 1px solid rgba(102, 126, 234, 0.15); min-height: 300px; max-height: 500px; overflow-y: auto; }
.message-wrapper { display: flex; margin-bottom: 1rem; }
.message-wrapper.user { justify-content: flex-end; }
.message-bubble { max-width: 75%; padding: 1rem 1.25rem; border-radius: 20px; word-wrap: break-word; }
.message-bubble.user { background: linear-gradient(135deg, #667eea, #764ba2); color: white; border-bottom-right-radius: 4px; }
.message-bubble.assistant { background: rgba(255,255,255,0.05); color: white; border-bottom-left-radius: 4px; border: 1px solid rgba(102, 126, 234, 0.2); }
.input-container { background: #1a1a2e; border-radius: 20px; padding: 1rem; border: 1px solid rgba(102, 126, 234, 0.15); }
.stTextArea textarea { background: rgba(0,0,0,0.2) !important; border: 2px solid rgba(102, 126, 234, 0.2) !important; border-radius: 16px !important; color: white !important; }
.stTextArea textarea:focus { border-color: #667eea !important; box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.2) !important; }
.stButton button { background: linear-gradient(135deg, #667eea, #764ba2) !important; color: white !important; border: none !important; border-radius: 16px !important; padding: 0.875rem 2rem !important; font-weight: 600 !important; width: 100% !important; }
.thinking-indicator { display: flex; align-items: center; gap: 0.75rem; padding: 1rem; background: rgba(102, 126, 234, 0.1); border-radius: 16px; margin-bottom: 1rem; }
.thinking-dot { width: 8px; height: 8px; background: #667eea; border-radius: 50%; animation: bounce 1.4s infinite ease-in-out; }
.thinking-dot:nth-child(1) { animation-delay: 0s; }
.thinking-dot:nth-child(2) { animation-delay: 0.2s; }
.thinking-dot:nth-child(3) { animation-delay: 0.4s; }
@keyframes bounce { 0%, 80%, 100% { transform: scale(0); } 40% { transform: scale(1); } }
.alert-error { background: rgba(239, 68, 68, 0.1); border: 1px solid rgba(239, 68, 68, 0.3); color: #fca5a5; padding: 1rem; border-radius: 12px; margin-bottom: 1rem; }
#MainMenu, footer, header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ===== SIDEBAR =====
with st.sidebar:
    st.markdown("### ⚙️ Configuration")
    api_url = st.text_input("API URL", value=API_URL)
    api_key = st.text_input("API Key", value=API_KEY, type="password")

    st.markdown("### 🔌 Status")
    try:
        r = requests.get(f"{api_url}/", timeout=5)
        connected = r.status_code == 200
    except:
        connected = False

    st.session_state.api_connected = connected

    if connected:
        st.markdown('<div class="status-online">✅ Online</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="status-offline">❌ Offline</div>', unsafe_allow_html=True)

    st.markdown("### 🎯 Actions")
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    if st.button("🔄 Reconnect", use_container_width=True):
        st.rerun()

# ===== HEADER =====
st.markdown("""
<div class="app-header">
    <h1>🤖 GenAI Learning Assistant</h1>
    <p>Your AI-powered programming tutor - Learn, Code, and Grow!</p>
</div>
""", unsafe_allow_html=True)

# ===== CHAT =====
st.markdown('<div class="chat-wrapper">', unsafe_allow_html=True)

if not st.session_state.messages:
    st.markdown('<div style="text-align: center; padding: 3rem; color: rgba(255,255,255,0.5);"><div style="font-size: 3rem; margin-bottom: 1rem;">💬</div><h3>Start a Conversation</h3><p>Ask me anything about programming!</p></div>', unsafe_allow_html=True)
else:
    for msg in st.session_state.messages:
        role_class = "user" if msg["role"] == "user" else "assistant"
        st.markdown(f'<div class="message-wrapper {role_class}"><div class="message-bubble {role_class}">{msg["content"]}</div></div>', unsafe_allow_html=True)

if st.session_state.is_processing:
    st.markdown('<div class="thinking-indicator"><div class="thinking-dot"></div><div class="thinking-dot"></div><div class="thinking-dot"></div><span>Thinking...</span></div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ===== INPUT =====
if st.session_state.is_processing:
    msgs = st.session_state.messages
    if msgs and msgs[-1]["role"] == "user":
        user_input = msgs[-1]["content"]
        try:
            r = requests.post(
                f"{api_url}/ask",
                headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
                json={"user_input": user_input},
                timeout=120
            )
            if r.status_code == 200:
                st.session_state.messages.append({"role": "assistant", "content": r.json()["response"]})
            else:
                st.error(f"Error: {r.status_code}")
        except Exception as e:
            st.error(f"Error: {e}")
        st.session_state.is_processing = False
        st.rerun()
else:
    st.markdown('<div class="input-container">', unsafe_allow_html=True)
    c1, c2 = st.columns([5, 1])
    with c1:
        inp = st.text_area("Message", placeholder="Ask me anything...", height=80, label_visibility="collapsed")
    with c2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🚀 Send", use_container_width=True, disabled=not inp.strip()):
            st.session_state.messages.append({"role": "user", "content": inp.strip()})
            st.session_state.is_processing = True
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# ===== QUICK ACTIONS =====
st.markdown("---")
st.markdown("### 🚀 Quick Start")
quick = [
    ("💡 Explain", "Explain what is recursion in programming?"),
    ("🐍 Python", "How do list comprehensions work in Python?"),
    ("🐛 Debug", "Find the bug: for i in range(10) print(i)"),
    ("📊 Compare", "What's the difference between arrays and linked lists?"),
]
cols = st.columns(len(quick))
for i, (label, query) in enumerate(quick):
    with cols[i]:
        if st.button(label, use_container_width=True, key=f"q{i}"):
            st.session_state.messages.append({"role": "user", "content": query})
            st.session_state.is_processing = True
            st.rerun()

# ===== FOOTER =====
st.markdown('<div style="text-align: center; padding: 2rem; color: rgba(255,255,255,0.5); margin-top: 2rem;"><p>Made with 💜 using CrewAI, FastAPI & Streamlit</p></div>', unsafe_allow_html=True)