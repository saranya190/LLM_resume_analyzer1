
import streamlit as st
from openai import OpenAI
import pdfplumber

# Page setup
st.set_page_config(page_title="LLM-Powered Resume Analyzer", layout="centered")
st.title("📄 LLM-Powered Resume Analyzer")

# Initialize OpenAI client using secrets
try:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
except KeyError:
    st.error("Please add your OpenAI API key in .streamlit/secrets.toml")
    st.stop()

# Function to extract text from uploaded PDF
def extract_text_from_pdf(uploaded_file):
    with pdfplumber.open(uploaded_file) as pdf:
        return "\n".join(page.extract_text() for page in pdf.pages if page.extract_text())

# Function to send prompt to OpenAI
def get_feedback_from_llm(resume_text, job_desc):
    prompt = f"""
You are a resume reviewer AI. Given the following resume and job description, provide:
1. Grammar or formatting corrections
2. Missing skills or improvements
3. Tailoring tips for better alignment

Resume:
{resume_text}

Job Description:
{job_desc}
"""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=800
    )
    return response.choices[0].message.content

# UI Elements
uploaded_file = st.file_uploader("Upload your Resume (PDF)", type="pdf")
job_description = st.text_area("Paste Job Description", height=200)

if uploaded_file and job_description:
    with st.spinner("Analyzing your resume with GPT-3.5..."):
        resume_text = extract_text_from_pdf(uploaded_file)
        feedback = get_feedback_from_llm(resume_text, job_description)
        st.subheader("🔍 Feedback from GPT-3.5:")
        st.write(feedback)
