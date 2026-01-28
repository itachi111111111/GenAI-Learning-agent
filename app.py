import streamlit as st
import requests

# ---- CONFIG ----
API_URL = "http://127.0.0.1:8000/ask"  # change later to ngrok URL
API_KEY = "super-secret-key"

st.set_page_config(page_title="GenAI Learning Assistant")
st.title("GenAI Learning Assistant")

user_input = st.text_area("Ask your question")

if st.button("Ask"):
    if not user_input.strip():
        st.warning("Please enter a question")
    else:
        with st.spinner("Thinking..."):
            r = requests.post(
                API_URL,
                headers={
                    "Authorization": f"Bearer {API_KEY}",
                    "Content-Type": "application/json",
                },
                json={"user_input": user_input},
                timeout=60
            )

            if r.status_code == 200:
                st.success("Response")
                st.write(r.json()["response"])
            else:
                st.error(f"Error {r.status_code}")
                st.json(r.json())
