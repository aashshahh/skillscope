import sys
import json
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from loguru import logger
from src.ingest.parser import load_document, clean_text
from src.nlp.extractor import SkillExtractor
from src.models.gap_analyzer import GapAnalyzer


def parse_args():
    p = argparse.ArgumentParser(description="SkillScope — Skill Gap Analysis CLI")
    p.add_argument("--resume", required=True)
    p.add_argument("--jd", required=True)
    p.add_argument("--output", default=None)
    p.add_argument("--verbose", action="store_true")
    return p.parse_args()


def print_report(report):
    print("\n" + "=" * 60)
    print("  SKILLSCOPE — GAP ANALYSIS REPORT")
    print("=" * 60)
    print(f"\n  Match Score: {report.match_score:.1f} / 100")
    print(f"\n  JD Skills ({len(report.jd_skills)}): {', '.join(report.jd_skills)}")
    print(f"  Resume Skills ({len(report.resume_skills)}): {', '.join(report.resume_skills)}")
    print(f"\n  Exact Matches ({len(report.matched_skills)}):")
    for s in report.matched_skills:
        print(f"    [+] {s}")
    if report.soft_matched:
        print(f"\n  Semantic Matches ({len(report.soft_matched)}):")
        for m in report.soft_matched:
            print(f"    [~] {m['jd_skill']} <- {m['resume_skill']} ({m['score']:.2f})")
    print(f"\n  Missing Skills ({len(report.missing_skills)}):")
    for s in report.missing_skills:
        print(f"    [-] {s}")
    print("\n" + "=" * 60)


def main():
    args = parse_args()
    if not args.verbose:
        logger.remove()

    resume_text = clean_text(load_document(args.resume))
    jd_text = clean_text(load_document(args.jd))

    extractor = SkillExtractor()
    resume_skills = extractor.extract_skill_names(resume_text)
    jd_skills = extractor.extract_skill_names(jd_text)

    analyzer = GapAnalyzer()
    report = analyzer.analyze(resume_skills, jd_skills)
    print_report(report)

    if args.output:
        out_path = Path(args.output)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with open(out_path, "w") as f:
            json.dump(report.to_dict(), f, indent=2)
        print(f"\n  Report saved to: {out_path}")


if __name__ == "__main__":
    main()