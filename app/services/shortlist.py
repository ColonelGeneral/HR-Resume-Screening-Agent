from __future__ import annotations

from datetime import datetime

from app.schemas import JobDescription, ShortlistResponse, CandidateProfile
from app.services.embeddings import EmbeddingService
from app.services.scoring import rank_candidates


class ShortlistService:
    def __init__(self, embeddings: EmbeddingService | None = None) -> None:
        self.embeddings = embeddings or EmbeddingService()

    def build_report(self, job: JobDescription, candidates: list[CandidateProfile]) -> ShortlistResponse:
        rankings = rank_candidates(job, candidates, self.embeddings)
        summary = {
            "candidate_count": len(candidates),
            "top_score": rankings[0].total_score if rankings else 0,
            "generated_at": datetime.utcnow().isoformat(),
        }
        return ShortlistResponse(job=job, rankings=rankings, summary=summary)


def build_shortlist(job: JobDescription, candidates: list[CandidateProfile]) -> ShortlistResponse:
    return ShortlistService().build_report(job, candidates)
