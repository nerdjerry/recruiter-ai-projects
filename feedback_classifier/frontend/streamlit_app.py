"""Streamlit frontend for the Feedback Classifier."""

import pandas as pd
import requests
import streamlit as st

st.set_page_config(page_title="Customer Feedback Classifier", layout="wide")
st.title("Customer Feedback Classifier")

base_url = st.sidebar.text_input("Backend URL", value="http://localhost:8000")

tab_classify, tab_bulk, tab_dashboard = st.tabs(
    ["Classify", "Bulk Upload", "Dashboard"]
)

# ── Tab 1: Single classification ─────────────────────────────────────
with tab_classify:
    text = st.text_area("Paste customer feedback here")
    if st.button("Classify") and text:
        resp = requests.post(
            f"{base_url}/classify", json={"text": text}, timeout=30
        )
        if resp.ok:
            data = resp.json()
            st.json(data)
        else:
            st.error(f"Error: {resp.status_code} — {resp.text}")

# ── Tab 2: CSV bulk upload ───────────────────────────────────────────
with tab_bulk:
    uploaded = st.file_uploader("Upload CSV (columns: text, source)", type="csv")
    if st.button("Process CSV") and uploaded:
        files = {"file": (uploaded.name, uploaded.getvalue(), "text/csv")}
        resp = requests.post(
            f"{base_url}/classify/bulk", files=files, timeout=120
        )
        if resp.ok:
            df = pd.DataFrame(resp.json())
            st.dataframe(df)
        else:
            st.error(f"Error: {resp.status_code} — {resp.text}")

# ── Tab 3: Dashboard ─────────────────────────────────────────────────
with tab_dashboard:
    sentiment_filter = st.selectbox(
        "Sentiment", ["all", "positive", "neutral", "negative"]
    )
    params: dict = {"page_size": 50}
    if sentiment_filter != "all":
        params["sentiment"] = sentiment_filter

    if st.button("Load results"):
        resp = requests.get(f"{base_url}/results", params=params, timeout=15)
        if resp.ok:
            payload = resp.json()
            items = payload.get("items", [])
            if items:
                df = pd.DataFrame(items)
                col1, col2, col3 = st.columns(3)
                col1.metric("Total", payload["total"])
                col2.metric("Avg severity", round(df["severity"].mean(), 2))
                col3.metric("Avg priority", round(df["priority_score"].mean(), 2))
                st.dataframe(df)
            else:
                st.info("No results yet.")
        else:
            st.error(f"Error: {resp.status_code}")
