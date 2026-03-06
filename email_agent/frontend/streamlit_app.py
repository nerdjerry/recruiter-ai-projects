"""Streamlit UI — Email Intelligence Agent review queue."""

import streamlit as st
import requests

BACKEND_DEFAULT = "http://localhost:8000"

st.set_page_config(page_title="Email Intelligence Agent", layout="wide")
st.title("📧 Email Intelligence Agent")

backend_url = st.sidebar.text_input("Backend URL", value=BACKEND_DEFAULT)

URGENCY_COLORS = {"high": "🔴", "medium": "🟡", "low": "🟢"}


def fetch_emails():
    resp = requests.get(f"{backend_url}/emails", timeout=30)
    resp.raise_for_status()
    return resp.json()


def approve(email_id: str):
    requests.post(f"{backend_url}/emails/{email_id}/approve", timeout=10)


def reject(email_id: str):
    requests.post(f"{backend_url}/emails/{email_id}/reject", timeout=10)


if st.button("🔄 Fetch & Classify Emails"):
    with st.spinner("Processing emails…"):
        try:
            st.session_state["emails"] = fetch_emails()
        except requests.RequestException as exc:
            st.error(f"Backend error: {exc}")

for item in st.session_state.get("emails", []):
    email = item["email"]
    clf = item["classification"]
    draft = item["draft_reply"]
    status = item["status"]

    icon = URGENCY_COLORS.get(clf["urgency"], "⚪")
    with st.expander(
        f"{icon} {email['subject']} — from {email['sender']}  "
        f"[{clf['intent']}]  status: **{status}**"
    ):
        st.markdown(f"**Intent:** {clf['intent']}  |  "
                     f"**Urgency:** {clf['urgency']}  |  "
                     f"**Confidence:** {clf['confidence']:.0%}")
        st.text_area("Original body", email["body"], height=100,
                      disabled=True, key=f"body-{email['id']}")
        st.text_area("Draft reply", draft["body"], height=100,
                      disabled=True, key=f"draft-{email['id']}")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ Approve", key=f"approve-{email['id']}"):
                approve(email["id"])
                st.success("Approved!")
        with col2:
            if st.button("❌ Reject", key=f"reject-{email['id']}"):
                reject(email["id"])
                st.warning("Rejected — flagged for manual handling.")
