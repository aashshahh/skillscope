from src.utils.config import load_skills_taxonomy, flat_skill_list

ALIASES: dict[str, str] = {
    "ml": "machine learning",
    "dl": "deep learning",
    "js": "javascript",
    "ts": "typescript",
    "postgres": "postgresql",
    "sk-learn": "scikit-learn",
    "sklearn": "scikit-learn",
    "hf": "huggingface",
    "tf": "tensorflow",
    "k8s": "kubernetes",
    "node": "node.js",
    "react.js": "react",
    "vue.js": "vue",
    "gpt-4": "gpt",
    "gpt-3": "gpt",
    "llms": "llm",
    "cv": "computer vision",
}


class SkillNormalizer:
    def __init__(self):
        self.taxonomy = load_skills_taxonomy()
        self.canonical = set(flat_skill_list(self.taxonomy))

    def normalize(self, skill: str) -> str:
        skill_lower = skill.lower().strip()
        if skill_lower in self.canonical:
            return skill_lower
        if skill_lower in ALIASES:
            return ALIASES[skill_lower]
        for canonical_skill in self.canonical:
            if canonical_skill in skill_lower or skill_lower in canonical_skill:
                return canonical_skill
        return skill_lower

    def normalize_list(self, skills: list[str]) -> list[str]:
        return list(dict.fromkeys(self.normalize(s) for s in skills))