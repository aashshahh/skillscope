import sys
import json
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from loguru import logger
from src.nlp.extractor import SkillExtractor
from src.models.evaluator import evaluate_corpus, load_skillspan_sample


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--n", type=int, default=100)
    p.add_argument("--output", default="results/eval_report.json")
    return p.parse_args()


def main():
    args = parse_args()
    samples = load_skillspan_sample(n=args.n)
    extractor = SkillExtractor()
    predictions = []
    ground_truths = []
    for i, sample in enumerate(samples):
        predictions.append(extractor.extract_skill_names(sample["text"]))
        ground_truths.append(sample["skills"])
        if i % 20 == 0:
            logger.info(f"Processed {i}/{len(samples)}")

    metrics = evaluate_corpus(predictions, ground_truths)
    report = {"n_samples": len(samples), "metrics": metrics, "model": "spaCy PhraseMatcher + ESCO taxonomy"}

    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(report, f, indent=2)

    print(f"\nPrecision : {metrics['precision']:.4f}")
    print(f"Recall    : {metrics['recall']:.4f}")
    print(f"F1        : {metrics['f1']:.4f}")
    print(f"Saved     : {out_path}")


if __name__ == "__main__":
    main()