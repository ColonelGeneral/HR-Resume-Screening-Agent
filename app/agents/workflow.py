from __future__ import annotations

from app.schemas import CandidateProfile, JobDescription, ShortlistResponse
from app.services.parsing import parse_jd_text, parse_resume_text, parse_linkedin_json_profile
from app.services.shortlist import ShortlistService


class HRWorkflow:
    def __init__(self) -> None:
        self.shortlist_service = ShortlistService()

    def parse_job(self, jd_text: str, role_title: str = "") -> JobDescription:
        return parse_jd_text(jd_text, role_title=role_title)

    def parse_candidate_text(self, text: str, source_name: str = "") -> CandidateProfile:
        return parse_resume_text(text, source_name=source_name)

    def parse_candidate_json(self, data: dict) -> CandidateProfile:
        return parse_linkedin_json_profile(data)

    def shortlist(self, job: JobDescription, candidates: list[CandidateProfile]) -> ShortlistResponse:
        return self.shortlist_service.build_report(job, candidates)


workflow = HRWorkflow()
