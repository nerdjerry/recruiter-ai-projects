"""Streamlit frontend for the Research Copilot."""

import streamlit as st
import requests

BACKEND_URL = st.sidebar.text_input("Backend URL", value="http://localhost:8000")

st.title("🔬 Research Copilot")

# --- Main panel: research ---
question = st.text_input("Enter your research question")

if st.button("Research") and question:
    with st.spinner("Researching..."):
        try:
            resp = requests.post(
                f"{BACKEND_URL}/research",
                json={"question": question},
                timeout=60,
            )
            resp.raise_for_status()
            data = resp.json()

            st.subheader("Answer")
            st.write(data["answer"])

            st.subheader("Confidence")
            st.progress(data["confidence_score"])
            st.caption(f"{data['confidence_score']:.0%}")

            st.subheader("Citations")
            for c in data["citations"]:
                st.markdown(f"- **{c['source']}** — {c['title']}: {c['snippet']}")

            with st.expander("Reasoning Trace"):
                for step in data["reasoning_trace"]:
                    st.text(step)
        except Exception as exc:
            st.error(f"Error: {exc}")

# --- Sidebar: document management ---
st.sidebar.header("📄 Documents")

uploaded = st.sidebar.file_uploader("Upload PDF or TXT", type=["pdf", "txt"])
if uploaded and st.sidebar.button("Upload"):
    with st.spinner("Uploading..."):
        try:
            files = {"file": (uploaded.name, uploaded.getvalue(), uploaded.type)}
            resp = requests.post(f"{BACKEND_URL}/documents", files=files, timeout=30)
            resp.raise_for_status()
            st.sidebar.success(f"Uploaded: {resp.json()['filename']}")
        except Exception as exc:
            st.sidebar.error(f"Upload failed: {exc}")

if st.sidebar.button("Refresh document list"):
    try:
        resp = requests.get(f"{BACKEND_URL}/documents", timeout=10)
        resp.raise_for_status()
        docs = resp.json()["documents"]
        if docs:
            for d in docs:
                st.sidebar.write(f"• {d['filename']} ({d['chunk_count']} chunks)")
        else:
            st.sidebar.info("No documents uploaded yet.")
    except Exception as exc:
        st.sidebar.error(f"Error: {exc}")
