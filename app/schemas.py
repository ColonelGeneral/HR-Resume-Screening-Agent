from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class JobDescriptionCreate(BaseModel):
    role_title: str = ""
    jd_text: str
    source: str | None = None


class JobDescription(BaseModel):
    job_id: int | None = None
    role_title: str = ""
    required_skills: list[str] = Field(default_factory=list)
    preferred_skills: list[str] = Field(default_factory=list)
    experience_years: float = 0.0
    education: list[str] = Field(default_factory=list)
    certifications: list[str] = Field(default_factory=list)
    domain: str = ""
    seniority: str = ""
    responsibilities: list[str] = Field(default_factory=list)
    raw_text: str = ""
    metadata: dict[str, Any] = Field(default_factory=dict)


class ExperienceEntry(BaseModel):
    title: str = ""
    company: str = ""
    start_date: str = ""
    end_date: str = ""
    description: str = ""


class EducationEntry(BaseModel):
    institution: str = ""
    degree: str = ""
    field: str = ""
    start_year: str = ""
    end_year: str = ""


class ProjectEntry(BaseModel):
    name: str = ""
    description: str = ""
    technologies: list[str] = Field(default_factory=list)


class CandidateProfile(BaseModel):
    candidate_id: str | None = None
    name: str = ""
    email: str = ""
    phone: str = ""
    skills: list[str] = Field(default_factory=list)
    experience: list[ExperienceEntry] = Field(default_factory=list)
    education: list[EducationEntry] = Field(default_factory=list)
    projects: list[ProjectEntry] = Field(default_factory=list)
    certifications: list[str] = Field(default_factory=list)
    communication_score: float = 0.0
    total_years_experience: float = 0.0
    employment_gaps: list[str] = Field(default_factory=list)
    github_url: str = ""
    linkedin_url: str = ""
    portfolio_url: str = ""
    raw_text: str = ""
    metadata: dict[str, Any] = Field(default_factory=dict)


class CandidateCreate(BaseModel):
    source_name: str = ""
    file_name: str = ""
    raw_text: str
    source_type: str = "resume"
    linkedin_json: dict[str, Any] | None = None


class ScoreDimension(BaseModel):
    score: float
    weight: float
    justification: str
    evidence: list[str] = Field(default_factory=list)


class CandidateEvaluation(BaseModel):
    candidate_id: int | str
    candidate_name: str
    job_id: int | None = None
    scores: dict[str, ScoreDimension] = Field(default_factory=dict)
    total_score: float = 0.0
    recommendation: str = "Review"
    confidence: float = 0.0
    rationale: list[str] = Field(default_factory=list)
    flags: list[str] = Field(default_factory=list)
    human_override_score: float | None = None
    human_override_reason: str | None = None
    reviewer: str | None = None


class ShortlistResponse(BaseModel):
    job: JobDescription
    rankings: list[CandidateEvaluation]
    generated_at: datetime = Field(default_factory=datetime.utcnow)
    summary: dict[str, Any] = Field(default_factory=dict)


class OverrideRequest(BaseModel):
    evaluation_id: int
    reviewer: str
    new_score: float
    reason: str


class ParsedDocument(BaseModel):
    source_name: str
    source_type: str
    text: str
    metadata: dict[str, Any] = Field(default_factory=dict)


class UploadResponse(BaseModel):
    status: str
    records: list[dict[str, Any]] = Field(default_factory=list)


class EvaluateRequest(BaseModel):
    job_id: int
    candidate_ids: list[int] | None = None


class EvaluationCreate(BaseModel):
    job_id: int
    candidate_id: int
    candidate_name: str
    total_score: float
    recommendation: str
    confidence: float
    scores: dict[str, Any]
    rationale: list[str] = Field(default_factory=list)
    flags: list[str] = Field(default_factory=list)
