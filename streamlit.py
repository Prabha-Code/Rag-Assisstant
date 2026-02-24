import streamlit as st
from utils import extract_text_from_pdf, skill_gap_analysis, generate_questions

st.set_page_config(page_title="AI Interview Mentor", layout="wide")

st.title("🚀 AI Interview Mentor + Skill Gap Analyzer")

resume_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
jd_text = st.text_area("Paste Job Description")

if st.button("Analyze"):

    if resume_file and jd_text:

        resume_text = extract_text_from_pdf(resume_file)
        resume_skills, jd_skills, missing_skills = skill_gap_analysis(resume_text, jd_text)

        st.subheader("✅ Your Skills")
        st.write(resume_skills)

        st.subheader("📌 Required Skills")
        st.write(jd_skills)

        st.subheader("❌ Missing Skills")
        st.write(missing_skills)

        if missing_skills:
            if st.button("Generate Interview Questions"):
                questions = generate_questions(missing_skills)
                st.subheader("🎯 Interview Questions")
                st.write(questions)

    else:
        st.warning("Upload resume and paste job description.")
