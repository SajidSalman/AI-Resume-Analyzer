import re

COMPANY_SKILLS = {
    "infosys": [
        "python",
        "sql",
        "testing tools",
        "agile",
        "react",
        "debugging",
    ],
    "tcs": [
        "java",
        "sql",
        "spring",
        "testing tools",
    ],
    "amazon": [
        "aws",
        "python",
        "docker",
        "system design",
    ],
    "google": [
        "algorithms",
        "python",
        "system design",
    ],
}

COMMON_SKILLS = {
    "python",
    "java",
    "sql",
    "react",
    "docker",
    "aws",
    "fastapi",
    "machine learning",
    "generative ai",
    "rag",
    "quality assurance",
    "testing tools",
    "debugging",
    "agile",
    "test planning",
    "devops",
    "continuous delivery",
    "continuous deployment",
    "grafana",
    "solid design",
    "architecture",
    "backend",
}


def clean_text(text):
    text = text.lower()

    text = re.sub(
        r"[^a-z0-9\s\-]",
        " ",
        text,
    )

    return text


def extract_skills(text):
    text = clean_text(text)

    found = set()

    for skill in COMMON_SKILLS:
        if skill in text:
            found.add(skill)

    return found


def analyze_resume(
    resume_text,
    job_description,
):
    resume_skills = extract_skills(resume_text)

    jd_skills = extract_skills(job_description)

    matched_skills = list(resume_skills.intersection(jd_skills))

    missing_skills = list(jd_skills - resume_skills)

    total = len(matched_skills) + len(missing_skills)

    match_score = int(len(matched_skills) / total * 100) if total > 0 else 0

    suggestions = [f"Add project experience related to {s}" for s in missing_skills]

    ats_feedback = []

    if missing_skills:
        ats_feedback.append("Add keywords from JD")

    if "github" not in resume_text.lower():
        ats_feedback.append("Add GitHub links")

    if "%" not in resume_text:
        ats_feedback.append("Add measurable achievements")

    summary = []

    if len(matched_skills) >= 5:
        summary.append("Strong technical alignment with job description")

    if "react" in resume_skills:
        summary.append("Good frontend development profile")

    if "python" in resume_skills:
        summary.append("Strong Python background")

    priority_skill = missing_skills[0] if missing_skills else ""

    return {
        "match_score": match_score,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "suggestions": suggestions,
        "ats_feedback": ats_feedback,
        "resume_summary": summary,
        "priority_skill": priority_skill,
    }


def analyze_company_fit(
    resume_text,
    company_name,
):
    resume_text = resume_text.lower()

    company_skills = COMPANY_SKILLS.get(
        company_name.lower(),
        [],
    )

    matched = []

    missing = []

    for skill in company_skills:
        if skill in resume_text:
            matched.append(skill)
        else:
            missing.append(skill)

    total = len(matched) + len(missing)

    fit_score = int(len(matched) / total * 100) if total > 0 else 0

    recommendations = [f"Add experience with {m}" for m in missing[:3]]

    return {
        "company": company_name,
        "fit_score": fit_score,
        "tips": recommendations,
        "strengths": matched,
        "weak_areas": missing,
        "recommendations": recommendations,
    }


def analyze_projects(
    resume_text,
):
    resume_text = resume_text.lower()

    project_scores = []

    match = re.search(
        r"projects?(.*?)(skills|education|certifications|$)",
        resume_text,
        re.DOTALL,
    )

    if not match:
        return []

    projects_text = match.group(1)

    lines = [line.strip() for line in projects_text.split("\n") if line.strip()]

    projects = []

    current_title = None

    current_desc = ""

    for line in lines:

        if line.startswith("–") or line.startswith("-"):
            current_desc += " " + line
            continue

        is_title = False

        if "|" in line:
            is_title = True

        elif len(line.split()) <= 6:
            is_title = True

        if is_title:

            if current_title:
                projects.append(
                    (
                        current_title,
                        current_desc,
                    )
                )

            if "|" in line:
                current_title = line.split("|")[0].strip()
            else:
                current_title = line

            current_desc = ""

        else:
            current_desc += " " + line

    if current_title:
        projects.append(
            (
                current_title,
                current_desc,
            )
        )

    for title, desc in projects[:5]:

        score = 6

        tech_stack = []

        if "python" in desc:
            tech_stack.append("Python")
            score += 1

        if "react" in desc:
            tech_stack.append("React")

        if "fastapi" in desc:
            tech_stack.append("FastAPI")

        if "github" in desc:
            score += 1

        if "%" in desc:
            score += 1

        project_scores.append(
            {
                "project": title.title(),
                "score": score,
                "level": ("Advanced" if score >= 8 else "Intermediate"),
                "tech_stack": tech_stack,
                "tips": [
                    "Add GitHub link",
                    "Mention measurable impact",
                ],
            }
        )

    return project_scores


def generate_ats_feedback(
    resume_text,
    job_description,
):
    resume_text = resume_text.lower()

    jd_skills = extract_skills(job_description)

    resume_skills = extract_skills(resume_text)

    feedback = []

    missing = list(jd_skills - resume_skills)

    if missing:
        feedback.append("Add keywords from JD: " + ", ".join(missing[:5]))

    if "github" not in resume_text:
        feedback.append("Add GitHub links")

    if "%" not in resume_text:
        feedback.append("Add measurable impact")

    return feedback
