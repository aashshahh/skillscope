from pydantic import BaseModel, Field


class AnalyzeTextRequest(BaseModel):
    resume_text: str = Field(..., min_length=10)
    jd_text: str = Field(..., min_length=10)


class SoftMatch(BaseModel):
    jd_skill: str
    resume_skill: str
    score: float


class GapReportResponse(BaseModel):
    resume_skills: list[str]
    jd_skills: list[str]
    matched_skills: list[str]
    soft_matched: list[SoftMatch]
    missing_skills: list[str]
    extra_skills: list[str]
    match_score: float