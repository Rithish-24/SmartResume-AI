import pdfplumber
import streamlit as st


skills_list = [
    "python", "sql", "machine learning", "deep learning",
    "data analysis", "tensorflow", "pytorch",
    "java", "c++", "html", "css", "javascript"
]


def extract_text_from_pdf(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text


def extract_skills(text):
    text = text.lower()
    found_skills = []

    for skill in skills_list:
        if skill in text:
            found_skills.append(skill)

    return found_skills


st.title("SmartResume AI")

resume = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
jd = st.text_area("Paste Job Description")


if st.button("Analyze"):
    if resume and jd:

        # Extract text
        resume_text = extract_text_from_pdf(resume)

        # Extract skills
        resume_skills = extract_skills(resume_text)
        jd_skills = extract_skills(jd)

        # Match calculation
        matched_skills = set(resume_skills) & set(jd_skills)
        match_percent = (len(matched_skills) / len(jd_skills)) * 100 if jd_skills else 0

        
        st.subheader("Skill Matching")
        st.write("Resume Skills:", resume_skills)
        st.write("JD Skills:", jd_skills)
        st.write(f"Match Percentage: {match_percent:.2f}%")

        
        if match_percent >= 80:
            st.success("Excellent match! Your resume is highly suitable 🎉")
        elif match_percent >= 50:
            st.info("Good match, but you can improve 🔥")
        else:
            st.error("Low match! Improve your skills ❌")

        
        st.subheader("Final Score")
        st.metric(label="Match Score", value=f"{match_percent:.2f}%")

       
        missing_skills = list(set(jd_skills) - set(resume_skills))

        st.subheader("Missing Skills")
        st.write(missing_skills)

        
        st.subheader("AI Feedback")

        if missing_skills:
            st.write("To improve your chances:")

            for skill in missing_skills:
                st.write(f"✔ Add {skill} to your resume with projects")

        else:
            st.success("Your resume matches all required skills! 🎉")

    else:
        st.error("Please upload resume and enter job description ❌")
 
