import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pytest
from src.nlp.extractor import SkillExtractor
from src.nlp.normalizer import SkillNormalizer
from src.models.gap_analyzer import GapAnalyzer
from src.ingest.parser import clean_text


@pytest.fixture(scope="module")
def extractor():
    return SkillExtractor()

@pytest.fixture(scope="module")
def normalizer():
    return SkillNormalizer()

@pytest.fixture(scope="module")
def analyzer():
    return GapAnalyzer()


def test_extractor_finds_python(extractor):
    skills = extractor.extract_skill_names("We need a Python developer with SQL experience.")
    assert "python" in skills

def test_extractor_finds_multiple(extractor):
    skills = extractor.extract_skill_names("Experience with PyTorch, Docker, and AWS required.")
    assert len(skills) >= 2

def test_extractor_empty_text(extractor):
    assert isinstance(extractor.extract_skill_names(""), list)

def test_normalizer_alias(normalizer):
    assert normalizer.normalize("sklearn") == "scikit-learn"

def test_normalizer_exact(normalizer):
    assert normalizer.normalize("python") == "python"

def test_normalizer_dedup(normalizer):
    assert len(normalizer.normalize_list(["python", "python", "pytorch"])) == 2

def test_perfect_match(analyzer):
    report = analyzer.analyze(["python", "sql", "docker"], ["python", "sql", "docker"])
    assert report.match_score == 100.0

def test_complete_mismatch(analyzer):
    report = analyzer.analyze(["excel"], ["pytorch", "kubernetes", "spark"])
    assert report.match_score < 30.0

def test_partial_match(analyzer):
    report = analyzer.analyze(["python", "docker"], ["python", "docker", "kubernetes", "spark"])
    assert 0 < report.match_score < 100
    assert "python" in report.matched_skills

def test_report_has_required_keys(analyzer):
    report = analyzer.analyze(["python"], ["python", "sql"])
    d = report.to_dict()
    for key in ["match_score", "missing_skills", "matched_skills", "soft_matched"]:
        assert key in d

def test_clean_text_removes_urls():
    assert "http" not in clean_text("Visit https://example.com today")