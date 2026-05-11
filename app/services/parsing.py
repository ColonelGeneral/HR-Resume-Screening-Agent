from __future__ import annotations

import re
from typing import Iterable

from app.schemas import (
    CandidateProfile,
    EducationEntry,
    ExperienceEntry,
    JobDescription,
)
from app.utils.metadata import (
    dedupe_preserve_order,
    extract_years_from_text,
    normalize_skill,
    normalize_skills,
    normalize_text,
    sentence_split,
)


SKILL_HINTS = [
    "python", "fastapi", "sql", "sqlalchemy", "pandas", "numpy", "machine learning",
    "deep learning", "nlp", "llm", "langchain", "langgraph", "faiss", "docker",
    "kubernetes", "aws", "gcp", "azure", "react", "tailwind", "javascript", "typescript",
    "communication", "leadership", "project management", "data analysis", "prompt engineering",
]


def _keyword_hits(text: str, candidates: Iterable[str]) -> list[str]:
    lowered = (text or "").lower()
    return [candidate for candidate in candidates if candidate in lowered]


def parse_jd_text(jd_text: str, role_title: str = "") -> JobDescription:
    text = normalize_text(jd_text)
    skills = normalize_skills(_keyword_hits(text, SKILL_HINTS))
    preferred = normalize_skills(_keyword_hits(text, ["fastapi", "docker", "kubernetes", "aws", "gcp", "azure", "langchain", "langgraph", "faiss"]))
    experience_years = extract_years_from_text(text)

    education = []
    for token in ("bachelor", "master", "phd", "mba", "b.tech", "m.tech", "degree"):
        if token in text.lower():
            education.append(token)

    certifications = _keyword_hits(text, ["pmp", "cfa", "aws certified", "azure certified", "gcp certified"])
    responsibilities = sentence_split(text)[:8]
    domain = ""
    for token in ("healthcare", "finance", "fintech", "recruitment", "talent acquisition", "hr", "data", "software", "ai", "ml"):
        if token in text.lower():
            domain = token
            break
    seniority = ""
    for token in ("intern", "junior", "associate", "mid", "senior", "lead", "principal", "manager", "director"):
        if token in text.lower():
            seniority = token
            break

    return JobDescription(
        role_title=role_title or role_title_from_text(text),
        required_skills=skills,
        preferred_skills=preferred,
        experience_years=experience_years,
        education=dedupe_preserve_order(education),
        certifications=dedupe_preserve_order(certifications),
        domain=domain,
        seniority=seniority,
        responsibilities=responsibilities,
        raw_text=text,
        metadata={"source": "jd_parser"},
    )


def role_title_from_text(text: str) -> str:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    if lines:
        return lines[0][:120]
    return ""


def _extract_email(text: str) -> str:
    match = re.search(r"[\w\.-]+@[\w\.-]+\.[a-zA-Z]{2,}", text)
    return match.group(0) if match else ""


def _extract_phone(text: str) -> str:
    match = re.search(r"(?:\+?\d[\d\s\-()]{7,}\d)", text)
    return match.group(0).strip() if match else ""


def _extract_name(text: str) -> str:
    for line in [line.strip() for line in text.splitlines() if line.strip()]:
        if len(line.split()) <= 4 and not re.search(r"@|\d", line):
            return line
    return ""


def _extract_education(text: str) -> list[EducationEntry]:
    entries: list[EducationEntry] = []
    for sentence in sentence_split(text):
        lowered = sentence.lower()
        if any(token in lowered for token in ("bachelor", "master", "phd", "b.tech", "m.tech", "mba", "degree")):
            entries.append(EducationEntry(degree=sentence[:120], institution="", field=""))
    return entries[:4]


def _extract_projects(text: str) -> list[dict[str, object]]:
    projects: list[dict[str, object]] = []
    for sentence in sentence_split(text):
        if any(token in sentence.lower() for token in ("project", "built", "developed", "deployed")):
            projects.append({"name": sentence[:80], "description": sentence, "technologies": _keyword_hits(sentence, SKILL_HINTS)})
    return projects[:5]


def _extract_experience_entries(text: str) -> list[ExperienceEntry]:
    entries: list[ExperienceEntry] = []
    bullets = [line.strip("-• \t") for line in text.splitlines() if line.strip()]
    for bullet in bullets:
        lowered = bullet.lower()
        if any(token in lowered for token in ("worked", "engineer", "developer", "manager", "analyst", "intern", "lead", "consultant")):
            entries.append(ExperienceEntry(description=bullet[:300]))
    return entries[:8]


def parse_resume_text(text: str, source_name: str = "") -> CandidateProfile:
    cleaned = normalize_text(text)
    skills = normalize_skills(_keyword_hits(cleaned, SKILL_HINTS + ["communication", "teamwork", "leadership", "stakeholder management"]))
    years = extract_years_from_text(cleaned)
    experience = _extract_experience_entries(cleaned)
    education = _extract_education(cleaned)
    projects = _extract_projects(cleaned)
    certifications = normalize_skills(_keyword_hits(cleaned, ["aws certified", "pmp", "scrum", "google cloud", "azure", "cfa", "data science", "machine learning"]))
    communication_score = 7.5 if len(cleaned) > 800 else 6.0

    return CandidateProfile(
        candidate_id=source_name or None,
        name=_extract_name(cleaned),
        email=_extract_email(cleaned),
        phone=_extract_phone(cleaned),
        skills=skills,
        experience=experience,
        education=education,
        projects=projects,
        certifications=certifications,
        communication_score=communication_score,
        total_years_experience=years,
        employment_gaps=[],
        raw_text=cleaned,
        metadata={"source": source_name, "parser": "resume_parser"},
    )


def parse_linkedin_json_profile(data: dict) -> CandidateProfile:
    text_parts = []
    for key in ("name", "headline", "summary", "about"):
        value = data.get(key)
        if value:
            text_parts.append(str(value))
    for key in ("skills", "experience", "education", "projects"):
        value = data.get(key)
        if isinstance(value, list):
            text_parts.extend(str(item) for item in value)
        elif value:
            text_parts.append(str(value))
    raw_text = normalize_text("\n".join(text_parts))
    profile = parse_resume_text(raw_text, source_name=data.get("name", "LinkedIn profile"))
    profile.linkedin_url = str(data.get("linkedin_url", ""))
    profile.github_url = str(data.get("github_url", ""))
    profile.portfolio_url = str(data.get("portfolio_url", ""))
    profile.metadata.update({"source": "linkedin_json", "linked_profile": True})
    return profile
