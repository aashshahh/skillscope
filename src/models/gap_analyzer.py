import numpy as np
from dataclasses import dataclass, field
from loguru import logger
from src.nlp.embedder import SkillEmbedder
from src.nlp.normalizer import SkillNormalizer
from src.utils.config import load_settings


@dataclass
class GapReport:
    resume_skills: list[str]
    jd_skills: list[str]
    matched_skills: list[str]
    soft_matched: list[dict]
    missing_skills: list[str]
    extra_skills: list[str]
    match_score: float
    category_breakdown: dict[str, dict] = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "resume_skills": self.resume_skills,
            "jd_skills": self.jd_skills,
            "matched_skills": self.matched_skills,
            "soft_matched": self.soft_matched,
            "missing_skills": self.missing_skills,
            "extra_skills": self.extra_skills,
            "match_score": round(self.match_score, 1),
            "category_breakdown": self.category_breakdown,
        }


class GapAnalyzer:
    def __init__(self):
        settings = load_settings()
        self.sim_threshold = settings["model"]["similarity_threshold"]
        self.embedder = SkillEmbedder()
        self.normalizer = SkillNormalizer()

    def analyze(self, resume_skills: list[str], jd_skills: list[str]) -> GapReport:
        resume_norm = self.normalizer.normalize_list(resume_skills)
        jd_norm = self.normalizer.normalize_list(jd_skills)

        resume_set = set(resume_norm)
        jd_set = set(jd_norm)

        exact_matches = list(resume_set & jd_set)

        resume_remaining = [s for s in resume_norm if s not in jd_set]
        jd_remaining = [s for s in jd_norm if s not in resume_set]

        soft_matched = []

        if resume_remaining and jd_remaining:
            sim_matrix = self.embedder.pairwise_similarity(jd_remaining, resume_remaining)
            for i, jd_skill in enumerate(jd_remaining):
                best_idx = int(np.argmax(sim_matrix[i]))
                best_score = float(sim_matrix[i][best_idx])
                if best_score >= self.sim_threshold:
                    soft_matched.append({
                        "jd_skill": jd_skill,
                        "resume_skill": resume_remaining[best_idx],
                        "score": round(best_score, 3),
                    })

        soft_matched_jd = {m["jd_skill"] for m in soft_matched}
        truly_missing = [s for s in jd_remaining if s not in soft_matched_jd]

        soft_matched_resume = {m["resume_skill"] for m in soft_matched}
        extra_skills = [
            s for s in resume_norm
            if s not in jd_set and s not in soft_matched_resume
        ]

        total_jd = len(jd_norm)
        if total_jd == 0:
            score = 0.0
        else:
            exact_contrib = len(exact_matches)
            soft_contrib = sum(m["score"] for m in soft_matched)
            score = min(100.0, ((exact_contrib + soft_contrib) / total_jd) * 100)

        logger.info(f"Gap analysis complete — score: {score:.1f}")

        return GapReport(
            resume_skills=resume_norm,
            jd_skills=jd_norm,
            matched_skills=exact_matches,
            soft_matched=soft_matched,
            missing_skills=truly_missing,
            extra_skills=extra_skills,
            match_score=score,
        )