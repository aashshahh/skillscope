import json
import yaml
from pathlib import Path
from loguru import logger

ROOT = Path(__file__).resolve().parents[2]


def load_settings() -> dict:
    path = ROOT / "config" / "settings.yaml"
    with open(path) as f:
        settings = yaml.safe_load(f)
    return settings


def load_skills_taxonomy() -> dict:
    path = ROOT / "config" / "skills.json"
    with open(path) as f:
        taxonomy = json.load(f)
    return taxonomy


def flat_skill_list(taxonomy: dict) -> list[str]:
    skills = []
    for category_skills in taxonomy.values():
        skills.extend(category_skills)
    return list(dict.fromkeys(skills))