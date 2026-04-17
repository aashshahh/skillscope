import re
import spacy
from spacy.matcher import PhraseMatcher
from loguru import logger
from src.utils.config import load_skills_taxonomy, flat_skill_list


class SkillExtractor:
    def __init__(self):
        self.taxonomy = load_skills_taxonomy()
        self.all_skills = flat_skill_list(self.taxonomy)
        self._load_spacy()
        self._build_matcher()

    def _load_spacy(self):
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            logger.warning("spaCy model not found. Run: python -m spacy download en_core_web_sm")
            self.nlp = spacy.blank("en")

    def _build_matcher(self):
        self.matcher = PhraseMatcher(self.nlp.vocab, attr="LOWER")
        patterns = [self.nlp.make_doc(skill) for skill in self.all_skills]
        self.matcher.add("SKILL", patterns)

    def extract(self, text: str) -> list[dict]:
        doc = self.nlp(text.lower())
        matches = self.matcher(doc)
        results = []
        seen = set()
        for match_id, start, end in matches:
            span_text = doc[start:end].text.strip()
            if span_text in seen:
                continue
            seen.add(span_text)
            results.append({
                "skill": span_text,
                "category": self._get_category(span_text),
                "start": start,
                "end": end,
            })
        for skill in self._regex_extract(text):
            if skill not in seen:
                seen.add(skill)
                results.append({
                    "skill": skill,
                    "category": self._get_category(skill),
                    "start": -1,
                    "end": -1,
                })
        return results

    def extract_skill_names(self, text: str) -> list[str]:
        return [r["skill"] for r in self.extract(text)]

    def _get_category(self, skill: str) -> str:
        skill_lower = skill.lower()
        for category, skills in self.taxonomy.items():
            if skill_lower in [s.lower() for s in skills]:
                return category
        return "other"

    def _regex_extract(self, text: str) -> list[str]:
        patterns = [
            r"\bc\+\+\b", r"\bc#\b", r"\.net\b",
            r"\bnode\.js\b", r"\bvue\.js\b", r"\breact\.js\b",
            r"\bscikit[-\s]learn\b", r"\bgpt[-\s]?\d*\b", r"\bllm[s]?\b",
        ]
        found = []
        for pat in patterns:
            for m in re.finditer(pat, text, re.IGNORECASE):
                found.append(m.group().lower().strip())
        return found