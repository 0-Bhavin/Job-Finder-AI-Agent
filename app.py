import streamlit as st
import requests
import google.generativeai as genai
from PyPDF2 import PdfReader
from datetime import datetime, timedelta
import json
import os

GENAI_API_KEY = "AIzaSyD_U7_I8t23N1LKbhbCbM5Z42DSHUlC1Js  "
AFFINDA_API_KEY = "aff_131c9ac44d037d14bae2616babff27c9fb874947"
REMOTIVE_URL = "https://remotive.com/api/remote-jobs"

# Setup Gemini
genai.configure(api_key=GENAI_API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash-lite-001")

#  Function: Resume Parser 
def parse_resume_with_affinda(resume_file):
    headers = {
        "Authorization": f"Bearer {AFFINDA_API_KEY}",
    }
    files = {"file": resume_file}
    response = requests.post("https://api.affinda.com/v2/resumes", headers=headers, files=files)
    if response.status_code == 201:
        data = response.json()
        return data["data"]["professionalSummary"], data["data"]["skills"]
    else:
        return None, None

#  Search Jobs 
def search_jobs(keyword, location):
    response = requests.get(REMOTIVE_URL)
    if response.status_code == 200:
        all_jobs = response.json()["jobs"]
        results = []
        for job in all_jobs:
            if keyword.lower() in job["title"].lower() and location.lower() in job["candidate_required_location"].lower():
                results.append(job)
        return results
    return []

#  Function: Suggest Interview Prep 
def interview_prep_with_gemini(job_title):
    prompt = f"Give me a list of 5 common interview questions and sample answers for the position: {job_title}"
    response = model.generate_content(prompt)
    return response.text

# Function: Add to Google Calendar 
def schedule_event(summary, start_time, duration=1):
    from google.oauth2 import service_account
    from googleapiclient.discovery import build

    creds = service_account.Credentials.from_service_account_file(
        'creds/bold-sorter-462413-e0-6cd62332c6d2.json.json',
        scopes=['https://www.googleapis.com/auth/calendar']
    )
    service = build('calendar', 'v3', credentials=creds)

    event = {
        'summary': summary,
        'start': {'dateTime': start_time.isoformat(), 'timeZone': 'Asia/Kolkata'},
        'end': {'dateTime': (start_time + timedelta(hours=duration)).isoformat(), 'timeZone': 'Asia/Kolkata'},
    }

    created_event = service.events().insert(calendarId='primary', body=event).execute()
    return created_event.get('htmlLink')


st.title("🤖 Job Search AI Agent")

st.sidebar.header("1️⃣ Upload Resume")
resume_file = st.sidebar.file_uploader("Upload your resume (PDF/DOCX)", type=["pdf", "docx"])
resume_summary, resume_skills = None, None

if resume_file:
    with st.spinner("Parsing resume..."):
        resume_summary, resume_skills = parse_resume_with_affinda(resume_file)
    if resume_summary:
        st.sidebar.success("Resume parsed successfully!")
    else:
        st.sidebar.error("Parsing failed!")

st.sidebar.header("2️⃣ Job Search Filter")
keyword = st.sidebar.text_input("Job Title", value="Software Engineer")
location = st.sidebar.text_input("Location", value="India")
search = st.sidebar.button("Search Jobs")

if search:
    with st.spinner("Searching jobs..."):
        jobs = search_jobs(keyword, location)
        if jobs:
            st.subheader("🔍 Matching Jobs")
            for job in jobs[:5]:
                st.markdown(f"### {job['title']} at {job['company_name']}")
                st.markdown(f"📍 Location: {job['candidate_required_location']}")
                st.markdown(f"🔗 [Job Link]({job['url']})")
                st.markdown("---")
        else:
            st.warning("No jobs found.")

if st.button("💬 Gemini Interview Prep"):
    if keyword:
        with st.spinner("Preparing interview questions..."):
            content = interview_prep_with_gemini(keyword)
            st.markdown("### 🤖 Gemini Interview Tips")
            st.markdown(content)
    else:
        st.warning("Enter job title first.")

st.sidebar.header("3️⃣ Schedule Prep Session")
schedule_btn = st.sidebar.button("Schedule Interview Prep")
if schedule_btn:
    prep_time = datetime.now() + timedelta(days=1, hours=2)
    link = schedule_event("Interview Prep Session", prep_time)
    st.success(f"✅ Interview prep session scheduled!")
    st.markdown(f"[📅 View in Google Calendar]({link})")

