from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

from database import engine, SessionLocal
from models import Base, Resume
from parser import extract_text_from_pdf

import os
import shutil

from ai_analyzer import (
    analyze_with_ai,
    analyze_company_fit_ai,
    analyze_projects_ai,
    generate_ats_feedback_ai,
)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Resume Analyzer API",
    description="Backend API for student resume analysis",
    version="1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_FOLDER = "uploads"

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True,
)


@app.get("/")
def home():
    return {"message": "Resume Analyzer API Running"}


@app.get("/health")
def health():
    return {"status": "running"}


@app.post("/upload-resume")
def upload_resume(file: UploadFile = File(...)):
    db = SessionLocal()

    try:
        if not file.filename.endswith(".pdf"):
            return {"message": "Only PDF files allowed"}

        file_path = os.path.join(
            UPLOAD_FOLDER,
            file.filename,
        )

        with open(
            file_path,
            "wb",
        ) as buffer:
            shutil.copyfileobj(
                file.file,
                buffer,
            )

        extracted_text = extract_text_from_pdf(file_path)

        resume = Resume(
            file_name=file.filename,
            extracted_text=extracted_text,
        )

        db.add(resume)

        db.commit()

        db.refresh(resume)

        return {
            "message": "Resume uploaded successfully",
            "resume_id": resume.id,
            "file_name": file.filename,
            "preview": extracted_text[:500],
        }

    except Exception as e:
        return {
            "message": "Upload failed",
            "error": str(e),
        }

    finally:
        db.close()


@app.get("/resumes")
def get_resumes():
    db = SessionLocal()

    try:
        resumes = db.query(Resume).all()

        return [
            {
                "id": r.id,
                "file_name": r.file_name,
                "uploaded_at": r.uploaded_at,
            }
            for r in resumes
        ]

    finally:
        db.close()


@app.get("/resume/{resume_id}")
def get_resume(resume_id: int):
    db = SessionLocal()

    try:
        resume = db.query(Resume).filter(Resume.id == resume_id).first()

        if not resume:
            return {"message": "Resume not found"}

        return {
            "id": resume.id,
            "file_name": resume.file_name,
            "text": resume.extracted_text,
        }

    finally:
        db.close()


@app.delete("/resume/{resume_id}")
def delete_resume(resume_id: int):
    db = SessionLocal()

    try:
        resume = db.query(Resume).filter(Resume.id == resume_id).first()

        if not resume:
            return {"message": "Resume not found"}

        db.delete(resume)

        db.commit()

        return {"message": "Deleted successfully"}

    finally:
        db.close()


@app.post("/analyze")
def analyze(
    resume_id: int,
    job_description: str,
):
    db = SessionLocal()

    try:
        resume = db.query(Resume).filter(Resume.id == resume_id).first()

        if not resume:
            return {"message": "Resume not found"}

        return analyze_with_ai(
            resume.extracted_text,
            job_description,
        )

    except Exception as e:
        return {
            "message": "Analysis failed",
            "error": str(e),
        }

    finally:
        db.close()


@app.post("/company-fit")
def company_fit(
    resume_id: int,
    company_name: str,
):
    db = SessionLocal()

    try:
        resume = db.query(Resume).filter(Resume.id == resume_id).first()

        if not resume:
            return {"message": "Resume not found"}

        return analyze_company_fit_ai(
            resume.extracted_text,
            company_name,
        )

    except Exception as e:
        return {
            "message": "Company fit failed",
            "error": str(e),
        }

    finally:
        db.close()


@app.post("/company-compare")
def company_compare(
    resume_id: int,
):
    db = SessionLocal()

    try:
        resume = db.query(Resume).filter(Resume.id == resume_id).first()

        if not resume:
            return {"message": "Resume not found"}

        companies = [
            "infosys",
            "amazon",
            "google",
            "tcs",
        ]

        results = []

        for company in companies:
            results.append(
                analyze_company_fit_ai(
                    resume.extracted_text,
                    company,
                )
            )

        return results

    finally:
        db.close()


@app.post("/project-score")
def project_score(
    resume_id: int,
):
    db = SessionLocal()

    try:
        resume = db.query(Resume).filter(Resume.id == resume_id).first()

        if not resume:
            return {"message": "Resume not found"}

        return analyze_projects_ai(
            resume.extracted_text,
        )

    except Exception as e:
        return {
            "message": "Project analysis failed",
            "error": str(e),
        }

    finally:
        db.close()


@app.post("/ats-feedback")
def ats_feedback(
    resume_id: int,
    job_description: str,
):
    db = SessionLocal()

    try:
        resume = db.query(Resume).filter(Resume.id == resume_id).first()

        if not resume:
            return {"message": "Resume not found"}

        return generate_ats_feedback_ai(
            resume.extracted_text,
            job_description,
        )

    except Exception as e:
        return {
            "message": "ATS feedback failed",
            "error": str(e),
        }

    finally:
        db.close()
