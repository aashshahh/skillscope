import io
from fastapi import APIRouter, UploadFile, File, HTTPException
from src.api.schemas import AnalyzeTextRequest, GapReportResponse
from src.ingest.parser import load_document, clean_text
from src.nlp.extractor import SkillExtractor
from src.models.gap_analyzer import GapAnalyzer
from loguru import logger

router = APIRouter()

_extractor = None
_analyzer = None


def get_extractor() -> SkillExtractor:
    global _extractor
    if _extractor is None:
        _extractor = SkillExtractor()
    return _extractor


def get_analyzer() -> GapAnalyzer:
    global _analyzer
    if _analyzer is None:
        _analyzer = GapAnalyzer()
    return _analyzer


@router.post("/analyze/text", response_model=GapReportResponse)
def analyze_text(request: AnalyzeTextRequest):
    extractor = get_extractor()
    analyzer = get_analyzer()
    resume_skills = extractor.extract_skill_names(clean_text(request.resume_text))
    jd_skills = extractor.extract_skill_names(clean_text(request.jd_text))
    if not jd_skills:
        raise HTTPException(status_code=422, detail="No skills detected in job description.")
    report = analyzer.analyze(resume_skills, jd_skills)
    logger.info(f"Analysis complete — score: {report.match_score}")
    return GapReportResponse(**report.to_dict())


@router.post("/analyze/upload", response_model=GapReportResponse)
async def analyze_upload(
    resume: UploadFile = File(...),
    jd: UploadFile = File(...),
):
    extractor = get_extractor()
    analyzer = get_analyzer()
    try:
        resume_bytes = await resume.read()
        jd_bytes = await jd.read()
        resume_text = _parse_upload(resume_bytes, resume.filename)
        jd_text = _parse_upload(jd_bytes, jd.filename)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"File parsing failed: {e}")
    resume_skills = extractor.extract_skill_names(clean_text(resume_text))
    jd_skills = extractor.extract_skill_names(clean_text(jd_text))
    if not jd_skills:
        raise HTTPException(status_code=422, detail="No skills detected in job description.")
    report = analyzer.analyze(resume_skills, jd_skills)
    return GapReportResponse(**report.to_dict())


def _parse_upload(content: bytes, filename: str) -> str:
    suffix = filename.rsplit(".", 1)[-1].lower() if "." in filename else "txt"
    if suffix == "pdf":
        from pdfminer.high_level import extract_text_to_fp
        from pdfminer.layout import LAParams
        out = io.StringIO()
        extract_text_to_fp(io.BytesIO(content), out, laparams=LAParams())
        return out.getvalue()
    elif suffix in ("docx", "doc"):
        from docx import Document
        doc = Document(io.BytesIO(content))
        return "\n".join(p.text for p in doc.paragraphs)
    else:
        return content.decode("utf-8", errors="ignore")