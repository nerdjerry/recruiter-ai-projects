"""Streamlit UI for the Personal Finance Agent."""
from __future__ import annotations

import pandas as pd
import requests
import streamlit as st

st.set_page_config(page_title="Personal Finance Agent", layout="wide")

# Sidebar
with st.sidebar:
    st.title("⚙️ Settings")
    backend_url = st.text_input("Backend URL", value="http://localhost:8000")
    if st.button("🗑️ Clear Memory"):
        try:
            requests.delete(f"{backend_url}/memory")
            st.success("Memory cleared.")
        except Exception as e:
            st.error(f"Error: {e}")

st.title("💰 Personal Finance Agent")

tab_chat, tab_txns, tab_insights = st.tabs(["Chat", "Transactions", "Weekly Insights"])

# --- Chat Tab ---
with tab_chat:
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    if user_input := st.chat_input("Ask about your finances..."):
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)

        try:
            resp = requests.post(
                f"{backend_url}/chat", json={"message": user_input}, timeout=30,
            )
            data = resp.json()
            reply = data.get("reply", "No response.")
            context = data.get("memory_context")
        except Exception as e:
            reply = f"Error contacting backend: {e}"
            context = None

        st.session_state.messages.append({"role": "assistant", "content": reply})
        with st.chat_message("assistant"):
            st.write(reply)
            if context:
                with st.expander("Memory context used"):
                    for item in context:
                        st.write(f"- {item}")

# --- Transactions Tab ---
with tab_txns:
    st.subheader("Upload Transactions (CSV)")
    uploaded = st.file_uploader("Choose a CSV file", type="csv")
    if uploaded and st.button("Sync"):
        try:
            resp = requests.post(
                f"{backend_url}/sync",
                files={"file": ("transactions.csv", uploaded.getvalue(), "text/csv")},
                timeout=30,
            )
            st.success(resp.json().get("message", "Synced."))
        except Exception as e:
            st.error(f"Error: {e}")

    st.subheader("Transaction History")
    col1, col2, col3 = st.columns(3)
    with col1:
        days_filter = st.number_input("Days", min_value=1, value=30)
    with col2:
        cat_filter = st.text_input("Category (optional)")
    with col3:
        min_amt = st.number_input("Min amount", min_value=0.0, value=0.0)

    if st.button("Load Transactions"):
        params: dict = {"days": days_filter}
        if cat_filter:
            params["category"] = cat_filter
        if min_amt > 0:
            params["min_amount"] = min_amt
        try:
            resp = requests.get(f"{backend_url}/transactions", params=params, timeout=10)
            txns = resp.json()
            if txns:
                st.dataframe(pd.DataFrame(txns))
            else:
                st.info("No transactions found.")
        except Exception as e:
            st.error(f"Error: {e}")

# --- Weekly Insights Tab ---
with tab_insights:
    st.subheader("Weekly Spending Insights")
    if st.button("Generate Insight"):
        try:
            resp = requests.get(f"{backend_url}/insights/weekly", timeout=30)
            data = resp.json()
            st.markdown(f"**Period:** {data['period']}")
            st.markdown(f"**Total Spent:** ${data['total_spent']:,.2f}")
            st.write(data["summary"])
            if data["top_categories"]:
                st.subheader("Top Categories")
                st.dataframe(pd.DataFrame(data["top_categories"]))
        except Exception as e:
            st.error(f"Error: {e}")
