"""
GenAI Learning Assistant - Modern Streamlit UI
"""

import streamlit as st
import requests
import os

# ===== CONFIGURATION =====
API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")
API_KEY = os.getenv("API_SECRET_KEY", "super-secret-key")
ASK_ENDPOINT = f"{API_URL}/ask"
HEALTH_ENDPOINT = f"{API_URL}/health"

# ===== SESSION STATE =====
st.session_state.setdefault("messages", [])
st.session_state.setdefault("api_connected", False)
st.session_state.setdefault("is_processing", False)

# ===== PAGE CONFIG =====
st.set_page_config(
    page_title="GenAI Learning Assistant",
    page_icon="🤖",
    layout="wide",
)

# ===== SIDEBAR =====
with st.sidebar:
    st.markdown("### ⚙️ Configuration")
    api_url = st.text_input("API URL", value=API_URL)
    api_key = st.text_input("API Key", value=API_KEY, type="password")

    st.markdown("### 🔌 Status")
    try:
        r = requests.get(f"{api_url}/health", timeout=5)
        st.session_state.api_connected = r.status_code == 200
    except Exception:
        st.session_state.api_connected = False

    if st.session_state.api_connected:
        st.success("✅ API Online")
    else:
        st.error("❌ API Offline")

    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# ===== HEADER =====
st.title("🤖 GenAI Learning Assistant")
st.caption("Your AI-powered programming tutor")

# ===== CHAT HISTORY =====
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ===== USER INPUT =====
if prompt := st.chat_input("Ask me anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    st.session_state.is_processing = True

    try:
        response = requests.post(
            ASK_ENDPOINT,
            json={"user_input": prompt},  # ⚠️ confirm schema in /docs
            headers={"Authorization": f"Bearer {api_key}"},
            timeout=120,
        )

        if response.status_code == 200:
            answer = response.json().get("response", "")
        else:
            answer = f"❌ Error {response.status_code}: {response.text}"

    except Exception as e:
        answer = f"❌ Request failed: {e}"

    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
    )

    with st.chat_message("assistant"):
        st.markdown(answer)

    st.session_state.is_processing = False
