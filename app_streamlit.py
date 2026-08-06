"""
app_streamlit.py

Streamlit frontend for the AI Medical Assistant.
Place this file in the PROJECT ROOT (same level as the `backend/` folder).

Run locally:
    streamlit run app_streamlit.py
"""

import streamlit as st
from backend.pipeline import run_pipeline
import os

try:
    if "GEMINI_API_KEY" in st.secrets:
        os.environ["GEMINI_API_KEY"] = st.secrets["GEMINI_API_KEY"]
except Exception:
    pass  
# ==========================================================
# Page Config
# ==========================================================

st.set_page_config(
    page_title="AI Medical Assistant",
    page_icon="🩺",
    layout="centered"
)

st.title("🩺 AI Medical Assistant")
st.caption(
    "This assistant provides educational health information based on "
    "verified medical sources. It is NOT a substitute for professional "
    "medical advice."
)

# ==========================================================
# Session State (keeps chat history while the app is open)
# ==========================================================

if "history" not in st.session_state:
    st.session_state.history = []  # list of (role, text) tuples

# ==========================================================
# Render Previous Messages
# ==========================================================

for role, text in st.session_state.history:
    with st.chat_message(role):
        st.markdown(text)

# ==========================================================
# Chat Input
# ==========================================================

user_input = st.chat_input("Describe your symptoms...")

if user_input:
    # Show the user's message immediately
    st.session_state.history.append(("user", user_input))
    with st.chat_message("user"):
        st.markdown(user_input)

    # Run the pipeline and show a spinner while waiting
    with st.chat_message("assistant"):
        with st.spinner("Analyzing your symptoms..."):
            try:
                result = run_pipeline(user_input)
            except Exception as e:
                result = {
                    "status": "error",
                    "response": f"Something went wrong: {e}"
                }

        # ---- Emergency case: show a prominent alert ----
        if result.get("status") == "emergency":
            st.error(result["response"])
            final_text = result["response"]

        # ---- Normal successful case ----
        elif result.get("status") == "success":
            st.markdown(result["response"])
            final_text = result["response"]

            # Optional: show retrieved sources in a collapsible section
            with st.expander("Sources used for this answer"):
                for chunk in result.get("retrieved_chunks", [])[:3]:
                    st.markdown(
                        f"**{chunk['focus_area']}** "
                        f"(similarity: {chunk['similarity_score']:.2f})"
                    )
                    st.caption(chunk["text"][:300] + "...")

        # ---- Error / fallback case ----
        else:
            st.warning(result.get("response", "Something went wrong."))
            final_text = result.get("response", "Something went wrong.")

    st.session_state.history.append(("assistant", final_text))

# ==========================================================
# Sidebar: reset button
# ==========================================================

with st.sidebar:
    st.header("About")
    st.write(
        "This assistant uses Retrieval-Augmented Generation (RAG) over "
        "the MedQuAD medical dataset, combined with Gemini and a safety "
        "review layer."
    )
    if st.button("Clear conversation"):
        st.session_state.history = []
        st.rerun()