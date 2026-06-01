import os
import json

from dotenv import load_dotenv
from google import genai

from analyzer import (
    analyze_resume,
    analyze_company_fit,
    analyze_projects,
    generate_ats_feedback,
)

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def ask_gemini(
    prompt,
    fallback=None,
):
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
        )

        text = response.text.replace("```json", "").replace("```", "").strip()

        return json.loads(text)

    except Exception as e:
        print(
            "Gemini error:",
            str(e),
        )

        if fallback:
            return fallback()

        raise


def analyze_with_ai(
    resume_text,
    job_description,
):
    prompt = f"""
Analyze this resume.

Return ONLY JSON:

{{
  "match_score": 0,
  "matched_skills": [],
  "missing_skills": [],
  "suggestions": [],
  "ats_feedback": [],
  "resume_summary": [],
  "priority_skill": ""
}}

Resume:
{resume_text}

Job Description:
{job_description}
"""

    return ask_gemini(
        prompt,
        fallback=lambda: analyze_resume(
            resume_text,
            job_description,
        ),
    )


def analyze_company_fit_ai(
    resume_text,
    company_name,
):
    prompt = f"""
Check company fit.

Return ONLY JSON:

{{
  "company": "",
  "fit_score": 0,
  "strengths": [],
  "weak_areas": [],
  "recommendations": []
}}

Resume:
{resume_text}

Company:
{company_name}
"""

    return ask_gemini(
        prompt,
        fallback=lambda: analyze_company_fit(
            resume_text,
            company_name,
        ),
    )


def analyze_projects_ai(
    resume_text,
):
    prompt = f"""
Extract only real projects.

Ignore:
- education
- internships
- certifications
- name
- descriptions

Return ONLY JSON array:

[
  {{
    "project": "",
    "score": 0,
    "level": "",
    "tech_stack": [],
    "tips": []
  }}
]

Resume:
{resume_text}
"""

    return ask_gemini(
        prompt,
        fallback=lambda: analyze_projects(
            resume_text,
        ),
    )


def generate_ats_feedback_ai(
    resume_text,
    job_description,
):
    prompt = f"""
Give ATS feedback.

Return ONLY JSON array.

Resume:
{resume_text}

Job Description:
{job_description}
"""

    return ask_gemini(
        prompt,
        fallback=lambda: generate_ats_feedback(
            resume_text,
            job_description,
        ),
    )
