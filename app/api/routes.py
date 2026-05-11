from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.db.models import CandidateModel, EvaluationModel, JobModel, OverrideModel
from app.db.session import SessionLocal
from app.schemas import (
    CandidateEvaluation,
    CandidateProfile,
    EvaluateRequest,
    JobDescription,
    OverrideRequest,
    ShortlistResponse,
    UploadResponse,
)
from app.services.ingest import ingest_upload_file, IngestionError
from app.services.parsing import parse_jd_text, parse_linkedin_json_profile, parse_resume_text
from app.services.shortlist import ShortlistService
from app.utils.metadata import mask_pii


router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def _candidate_from_model(model: CandidateModel) -> CandidateProfile:
    return CandidateProfile.model_validate(model.parsed_data)


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@router.post("/jobs/upload", response_model=JobDescription)
async def upload_job(
    file: Annotated[UploadFile, File(...)],
    role_title: Annotated[str, Form()] = "",
    db: Session = Depends(get_db),
):
    try:
        parsed = await ingest_upload_file(file)
    except IngestionError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    job = parse_jd_text(parsed.text, role_title=role_title)
    model = JobModel(role_title=job.role_title, jd_text=mask_pii(job.raw_text), structured_requirements=job.model_dump())
    db.add(model)
    db.commit()
    db.refresh(model)
    job.job_id = model.id
    return job


@router.post("/candidates/upload", response_model=UploadResponse)
async def upload_candidates(files: Annotated[list[UploadFile], File(...)], db: Session = Depends(get_db)):
    records: list[dict[str, object]] = []
    for upload_file in files:
        try:
            parsed = await ingest_upload_file(upload_file)
            if parsed.source_type == "linkedin_json":
                candidate = parse_linkedin_json_profile(parsed.metadata.get("json_data", {}))
            else:
                candidate = parse_resume_text(parsed.text, source_name=parsed.source_name)
            model = CandidateModel(
                name=candidate.name,
                email=candidate.email,
                source_name=parsed.source_name,
                file_name=upload_file.filename,
                source_type=parsed.source_type,
                raw_text=mask_pii(parsed.text),
                parsed_data=candidate.model_dump(),
            )
            db.add(model)
            db.flush()
            records.append({"candidate_id": model.id, "name": candidate.name, "source": parsed.source_name})
        except IngestionError as exc:
            records.append({"file": upload_file.filename, "error": str(exc)})
    db.commit()
    return UploadResponse(status="processed", records=records)


@router.post("/evaluate", response_model=ShortlistResponse)
def evaluate(request: EvaluateRequest, db: Session = Depends(get_db)):
    job = db.get(JobModel, request.job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    job_schema = JobDescription.model_validate(job.structured_requirements)
    candidates_query = db.query(CandidateModel)
    if request.candidate_ids:
        candidates_query = candidates_query.filter(CandidateModel.id.in_(request.candidate_ids))
    candidates = candidates_query.all()
    profiles = [_candidate_from_model(candidate) for candidate in candidates]
    shortlist = ShortlistService().build_report(job_schema, profiles)

    for evaluation in shortlist.rankings:
        candidate_model = next((candidate for candidate in candidates if (candidate.parsed_data.get("candidate_id") or candidate.name) == evaluation.candidate_id or candidate.name == evaluation.candidate_name), None)
        if candidate_model is None:
            continue
        db_eval = EvaluationModel(
            job_id=job.id,
            candidate_id=candidate_model.id,
            scores={key: value.model_dump() for key, value in evaluation.scores.items()},
            rationale=evaluation.rationale,
            flags=evaluation.flags,
            total_score=evaluation.total_score,
            recommendation=evaluation.recommendation,
            confidence=evaluation.confidence,
            human_override_score=evaluation.human_override_score,
            human_override_reason=evaluation.human_override_reason,
            reviewer=evaluation.reviewer,
        )
        db.add(db_eval)
    db.commit()
    return shortlist


@router.get("/rankings/{job_id}", response_model=ShortlistResponse)
def get_rankings(job_id: int, db: Session = Depends(get_db)):
    job = db.get(JobModel, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    job_schema = JobDescription.model_validate(job.structured_requirements)
    evaluations = db.query(EvaluationModel).filter(EvaluationModel.job_id == job_id).order_by(EvaluationModel.total_score.desc()).all()
    if not evaluations:
        return ShortlistResponse(job=job_schema, rankings=[], summary={"candidate_count": 0})

    rebuilt_rankings = []
    for evaluation in evaluations:
        candidate = db.get(CandidateModel, evaluation.candidate_id)
        if not candidate:
            continue
        stored_scores = {key: value for key, value in evaluation.scores.items()}
        rebuilt_rankings.append(
            CandidateEvaluation(
                candidate_id=candidate.id,
                candidate_name=candidate.name or candidate.parsed_data.get("name", "Unknown"),
                job_id=job.id,
                scores=stored_scores,
                total_score=evaluation.human_override_score or evaluation.total_score,
                recommendation=evaluation.recommendation,
                confidence=evaluation.confidence,
                rationale=evaluation.rationale,
                flags=evaluation.flags,
                human_override_score=evaluation.human_override_score,
                human_override_reason=evaluation.human_override_reason,
                reviewer=evaluation.reviewer,
            )
        )
    return ShortlistResponse(job=job_schema, rankings=rebuilt_rankings, summary={"candidate_count": len(rebuilt_rankings)})


@router.post("/override")
def override_score(request: OverrideRequest, db: Session = Depends(get_db)):
    evaluation = db.get(EvaluationModel, request.evaluation_id)
    if not evaluation:
        raise HTTPException(status_code=404, detail="Evaluation not found")
    old_score = evaluation.total_score
    evaluation.human_override_score = request.new_score
    evaluation.human_override_reason = request.reason
    evaluation.reviewer = request.reviewer
    db.add(
        OverrideModel(
            evaluation_id=evaluation.id,
            reviewer=request.reviewer,
            old_score=old_score,
            new_score=request.new_score,
            reason=request.reason,
        )
    )
    db.commit()
    return {"status": "updated", "evaluation_id": evaluation.id, "old_score": old_score, "new_score": request.new_score}
