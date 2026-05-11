from app.schemas import CandidateProfile, ExperienceEntry, JobDescription, ProjectEntry
from app.services.scoring import rank_candidates, evaluate_candidate


def test_evaluation_prefers_stronger_match():
    job = JobDescription(
        role_title="AI Engineer",
        required_skills=["python", "fastapi", "sql"],
        preferred_skills=["docker"],
        experience_years=3,
        education=["bachelor"],
        certifications=[],
        domain="ai",
        seniority="mid",
        responsibilities=["build systems"],
        raw_text="Need Python FastAPI SQL and 3 years experience",
    )
    strong = CandidateProfile(
        candidate_id="1",
        name="Strong Candidate",
        skills=["python", "fastapi", "sql", "docker"],
        experience=[ExperienceEntry(description="4 years as engineer")],
        education=[],
        projects=[ProjectEntry(name="AI Dashboard", description="Built FastAPI AI dashboard", technologies=["python", "fastapi"])],
        total_years_experience=4,
        communication_score=8,
        raw_text="Strong candidate with Python and FastAPI",
    )
    weak = CandidateProfile(
        candidate_id="2",
        name="Weak Candidate",
        skills=["excel"],
        experience=[],
        education=[],
        projects=[],
        total_years_experience=1,
        communication_score=5,
        raw_text="Basic profile",
    )
    rankings = rank_candidates(job, [weak, strong])
    assert rankings[0].candidate_name == "Strong Candidate"
    assert rankings[0].total_score >= rankings[1].total_score


def test_evaluate_candidate_returns_recommendation():
    job = JobDescription(role_title="HR Analyst", required_skills=["communication"], raw_text="HR role")
    candidate = CandidateProfile(candidate_id="1", name="A", skills=["communication"], raw_text="excellent communication skills", total_years_experience=2)
    evaluation = evaluate_candidate(job, candidate)
    assert evaluation.recommendation in {"Hire", "Review", "No-Hire"}
    assert evaluation.total_score > 0
