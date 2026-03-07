from __future__ import annotations

import requests
import streamlit as st

st.set_page_config(page_title="AI Resume Screener", layout="wide")
st.title("AI Resume Screener")

backend_url = st.sidebar.text_input("Backend URL", value="http://localhost:8000")

job_description = st.text_area("Job Description", height=200, placeholder="Paste the job description here…")
uploaded_files = st.file_uploader(
    "Upload Resumes (PDF / DOCX)",
    type=["pdf", "docx"],
    accept_multiple_files=True,
)

if not job_description or not uploaded_files:
    if st.button("Screen Candidates"):
        st.warning("Please provide a job description and at least one resume.")
else:
    if st.button("Screen Candidates"):
        files = [("resumes", (f.name, f.getvalue(), f.type)) for f in uploaded_files]
        data = {"job_description": job_description}

        with st.spinner("Screening resumes…"):
            try:
                resp = requests.post(f"{backend_url}/screen", data=data, files=files, timeout=120)
                resp.raise_for_status()
            except requests.RequestException as exc:
                st.error(f"Request failed: {exc}")
                st.stop()

        results = resp.json()
        st.subheader("Results")

        for idx, candidate in enumerate(results["candidates"], start=1):
            with st.expander(f"#{idx} — {candidate['name']} (Score: {candidate['score']:.2f})"):
                st.write(candidate["explanation"])
                if candidate["skill_gaps"]:
                    st.write("**Skill Gaps:**", ", ".join(candidate["skill_gaps"]))
