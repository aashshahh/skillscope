import re
from pathlib import Path
from loguru import logger


def read_text_file(path: str | Path) -> str:
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()


def read_pdf(path: str | Path) -> str:
    try:
        from pdfminer.high_level import extract_text
        text = extract_text(str(path))
        logger.info(f"Extracted {len(text)} chars from PDF: {path}")
        return text
    except Exception as e:
        logger.error(f"PDF parse failed: {e}")
        return ""


def read_docx(path: str | Path) -> str:
    try:
        from docx import Document
        doc = Document(str(path))
        text = "\n".join(p.text for p in doc.paragraphs)
        return text
    except Exception as e:
        logger.error(f"DOCX parse failed: {e}")
        return ""


def load_document(path: str | Path) -> str:
    path = Path(path)
    suffix = path.suffix.lower()
    if suffix == ".pdf":
        return read_pdf(path)
    elif suffix in (".docx", ".doc"):
        return read_docx(path)
    elif suffix in (".txt", ".md", ""):
        return read_text_file(path)
    else:
        raise ValueError(f"Unsupported file type: {suffix}")


def clean_text(text: str) -> str:
    text = re.sub(r"http\S+|www\.\S+", " ", text)
    text = re.sub(r"\S+@\S+", " ", text)
    text = re.sub(r"[^\w\s\.\,\-\+\#\/]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()