# 💼 Job Search AI Agent 🔍🤖

A smart job-hunting assistant that streamlines your job search, helps prepare for interviews, parses resumes, and schedules interview prep sessions — all in one place using **AI** and APIs like **Remotive**, **Affinda**, **Google Calendar**, and **Gemini**.

---

## 🚀 Features

- 📄 **Resume Parsing** with [Affinda](https://www.affinda.com/)
- 🔎 **Job Search** using [Remotive Job API](https://remotive.com/api/remote-jobs)
- 🎤 **Interview Preparation** using Gemini AI
- 📆 **Google Calendar Scheduling** for interview prep sessions

---

## 🛠 Tech Stack

- **Frontend**: [Streamlit](https://streamlit.io/)
- **Resume Parser**: [Affinda Resume API](https://www.affinda.com/)
- **Job Listings**: [Remotive API](https://remotive.com/api/remote-jobs)
- **Interview Q&A**: [Gemini Generative AI](https://ai.google.dev/)
- **Scheduling**: [Google Calendar API](https://developers.google.com/calendar)

---

## 📁 Project Structure

job-search-ai/
├── app.py # Main Streamlit app
├── requirements.txt # Python dependencies
├── creds/ # Google service account credentials
│ └── your_credentials.json # Your downloaded Google JSON key
├── README.md # Project documentation


---

## 🔑 Required API Keys & Setup

### 1. 🔐 Affinda API Key

- Sign up at [Affinda](https://app.affinda.com/)
- Navigate to the API section and generate a key.
- Replace `AFFINDA_API_KEY` in `app.py` with your key.

### 2. 🔐 Google Calendar API

- Go to [Google Cloud Console](https://console.cloud.google.com/)
- Create a new project and enable **Google Calendar API**
- Create a **Service Account**
- Download the credentials JSON and place it in the `creds/` folder
- Share your calendar access with the service account email

### 3. 🔐 Gemini (Google Generative AI) API Key

- Visit [Google AI Studio](https://makersuite.google.com/app)
- Create a project and generate a Gemini API key
- Replace `GENAI_API_KEY` in `app.py` with your key

---


