import pandas as pd
from loguru import logger


def compute_token_metrics(predicted: list[str], ground_truth: list[str]) -> dict[str, float]:
    pred_set = set(s.lower() for s in predicted)
    true_set = set(s.lower() for s in ground_truth)
    tp = len(pred_set & true_set)
    fp = len(pred_set - true_set)
    fn = len(true_set - pred_set)
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0.0
    return {"precision": precision, "recall": recall, "f1": f1}


def evaluate_corpus(predictions: list[list[str]], ground_truths: list[list[str]]) -> dict[str, float]:
    results = [compute_token_metrics(p, g) for p, g in zip(predictions, ground_truths)]
    df = pd.DataFrame(results)
    micro = df.mean().to_dict()
    logger.info(f"Precision: {micro['precision']:.3f} | Recall: {micro['recall']:.3f} | F1: {micro['f1']:.3f}")
    return micro


def load_skillspan_sample(n: int = 100) -> list[dict]:
    try:
        from datasets import load_dataset
        logger.info("Loading SkillSpan dataset...")
        ds = load_dataset("jensjorisdecorte/skillspan", split="test")
        samples = []
        for row in list(ds)[:n]:
            tokens = row.get("tokens", [])
            tags = row.get("tags", [])
            skills = _bio_to_skills(tokens, tags)
            samples.append({"text": " ".join(tokens), "skills": skills})
        return samples
    except Exception as e:
        logger.warning(f"Could not load SkillSpan: {e}. Using synthetic samples.")
        return _synthetic_samples()


def _bio_to_skills(tokens: list[str], tags: list) -> list[str]:
    skills, current = [], []
    for token, tag in zip(tokens, tags):
        tag_str = str(tag)
        if "B-SKILL" in tag_str or tag_str == "1":
            if current:
                skills.append(" ".join(current))
            current = [token]
        elif "I-SKILL" in tag_str or tag_str == "2":
            current.append(token)
        else:
            if current:
                skills.append(" ".join(current))
                current = []
    if current:
        skills.append(" ".join(current))
    return skills


def _synthetic_samples() -> list[dict]:
    return [
        {"text": "Experience with Python, TensorFlow, and AWS required.", "skills": ["python", "tensorflow", "aws"]},
        {"text": "Must know React, Node.js, and PostgreSQL.", "skills": ["react", "node.js", "postgresql"]},
        {"text": "Proficiency in Docker, Kubernetes, and CI/CD pipelines.", "skills": ["docker", "kubernetes", "ci/cd"]},
    ]