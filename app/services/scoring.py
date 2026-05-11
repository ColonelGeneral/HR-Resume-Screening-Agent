from __future__ import annotations

from typing import Iterable

from app.core.config import settings
from app.schemas import CandidateEvaluation, CandidateProfile, JobDescription, ScoreDimension
from app.services.embeddings import EmbeddingService
from app.utils.metadata import normalize_skill


WEIGHTS = {
    "skills_match": 30.0,
    "experience_relevance": 25.0,
    "education_certifications": 15.0,
    "project_portfolio": 20.0,
    "communication_quality": 10.0,
}


def _overlap_score(required: Iterable[str], candidate: Iterable[str]) -> tuple[float, list[str]]:
    required_set = {normalize_skill(skill) for skill in required if skill}
    candidate_set = {normalize_skill(skill) for skill in candidate if skill}
    if not required_set:
        return 5.0, []
    overlap = sorted(required_set & candidate_set)
    score = min(10.0, (len(overlap) / len(required_set)) * 10.0)
    return score, overlap


def _experience_score(required_years: float, candidate_years: float) -> float:
    if required_years <= 0:
        return min(10.0, max(5.0, candidate_years))
    ratio = candidate_years / required_years if required_years else 1.0
    if ratio >= 1.5:
        return 10.0
    if ratio >= 1.0:
        return 8.5
    if ratio >= 0.75:
        return 7.0
    if ratio >= 0.5:
        return 5.0
    return max(2.0, ratio * 10.0)


def _education_score(job: JobDescription, candidate: CandidateProfile) -> tuple[float, list[str]]:
    evidence: list[str] = []
    candidate_text = " ".join([edu.degree.lower() for edu in candidate.education] + candidate.certifications)
    for requirement in job.education + job.certifications:
        if requirement and requirement.lower() in candidate_text:
            evidence.append(requirement)
    if not (job.education or job.certifications):
        return 5.0, []
    score = min(10.0, (len(evidence) / max(1, len(job.education) + len(job.certifications))) * 10.0)
    return score, evidence


def _project_score(job: JobDescription, candidate: CandidateProfile, embeddings: EmbeddingService | None) -> tuple[float, list[str]]:
    project_text = " ".join(project.name + " " + project.description for project in candidate.projects)
    if not project_text:
        return 2.5, []
    evidence = []
    for token in job.required_skills + job.preferred_skills + [job.domain, job.seniority]:
        if token and token.lower() in project_text.lower():
            evidence.append(token)
    if embeddings is not None and project_text.strip() and job.raw_text.strip():
        semantic = embeddings.similarity(job.raw_text[:4000], project_text[:4000])
        score = max(2.5, min(10.0, semantic * 10.0))
    else:
        score = min(10.0, 4.0 + len(evidence) * 1.5)
    return score, evidence


def _communication_score(candidate: CandidateProfile) -> float:
    if candidate.communication_score:
        return max(0.0, min(10.0, candidate.communication_score))
    text_length = len(candidate.raw_text)
    if text_length > 2000:
        return 8.0
    if text_length > 1000:
        return 7.0
    return 6.0


def _confidence(candidate: CandidateProfile, evidence_counts: list[int]) -> float:
    coverage = sum(evidence_counts) / max(1, len(evidence_counts) * 10)
    profile_completeness = 0.0
    if candidate.name:
        profile_completeness += 0.2
    if candidate.skills:
        profile_completeness += 0.2
    if candidate.experience:
        profile_completeness += 0.2
    if candidate.education:
        profile_completeness += 0.2
    if candidate.projects:
        profile_completeness += 0.2
    return round(min(1.0, 0.35 + coverage + profile_completeness / 2), 3)


def evaluate_candidate(
    job: JobDescription,
    candidate: CandidateProfile,
    embeddings: EmbeddingService | None = None,
) -> CandidateEvaluation:
    skills_score, skills_evidence = _overlap_score(job.required_skills + job.preferred_skills, candidate.skills)
    experience_score = _experience_score(job.experience_years, candidate.total_years_experience)
    education_score, education_evidence = _education_score(job, candidate)
    project_score, project_evidence = _project_score(job, candidate, embeddings)
    communication_score = _communication_score(candidate)

    dimensions = {
        "skills_match": ScoreDimension(score=skills_score, weight=WEIGHTS["skills_match"], justification="Overlap between JD and candidate skill set.", evidence=skills_evidence),
        "experience_relevance": ScoreDimension(score=experience_score, weight=WEIGHTS["experience_relevance"], justification="Years of experience compared with JD requirement.", evidence=[f"{candidate.total_years_experience} years"]),
        "education_certifications": ScoreDimension(score=education_score, weight=WEIGHTS["education_certifications"], justification="Education and certifications evidence.", evidence=education_evidence),
        "project_portfolio": ScoreDimension(score=project_score, weight=WEIGHTS["project_portfolio"], justification="Project and portfolio relevance.", evidence=project_evidence),
        "communication_quality": ScoreDimension(score=communication_score, weight=WEIGHTS["communication_quality"], justification="Heuristic communication quality assessment.", evidence=[]),
    }

    weighted_total = sum((dimension.score / 10.0) * dimension.weight for dimension in dimensions.values())
    confidence = _confidence(candidate, [len(skills_evidence), len(education_evidence), len(project_evidence)])
    flags = []
    if confidence < settings.confidence_threshold:
        flags.append("low_confidence")
    if not candidate.skills:
        flags.append("missing_skills")
    if not candidate.experience:
        flags.append("missing_experience")

    recommendation = "Hire" if weighted_total >= 70 and confidence >= settings.confidence_threshold else "Review"
    if weighted_total < 55:
        recommendation = "No-Hire"

    rationale = [
        f"Skills evidence: {', '.join(skills_evidence) if skills_evidence else 'none'}",
        f"Education evidence: {', '.join(education_evidence) if education_evidence else 'none'}",
        f"Project evidence: {', '.join(project_evidence) if project_evidence else 'none'}",
    ]

    return CandidateEvaluation(
        candidate_id=candidate.candidate_id or candidate.name or "unknown",
        candidate_name=candidate.name or candidate.candidate_id or "Unknown",
        scores=dimensions,
        total_score=round(weighted_total, 2),
        recommendation=recommendation,
        confidence=confidence,
        rationale=rationale,
        flags=flags,
    )


def rank_candidates(job: JobDescription, candidates: list[CandidateProfile], embeddings: EmbeddingService | None = None) -> list[CandidateEvaluation]:
    evaluated = [evaluate_candidate(job, candidate, embeddings) for candidate in candidates]
    return sorted(evaluated, key=lambda item: (-item.total_score, -item.confidence, item.candidate_name.lower()))
