import time
import requests
import pandas as pd
from pathlib import Path
from loguru import logger

REMOTEOK_URL = "https://remoteok.com/api"
HEADERS = {"User-Agent": "SkillScope-Research/1.0"}

ROLE_TAGS = [
    "machine-learning", "data-science", "nlp", "python",
    "backend", "devops", "frontend", "fullstack"
]


def fetch_remoteok(tags: list[str] | None = None) -> list[dict]:
    logger.info("Fetching jobs from RemoteOK API...")
    time.sleep(1)
    resp = requests.get(REMOTEOK_URL, headers=HEADERS, timeout=15)
    resp.raise_for_status()
    data = resp.json()
    jobs = [j for j in data if isinstance(j, dict) and "position" in j]
    logger.info(f"Fetched {len(jobs)} total jobs")
    if tags:
        tags_lower = [t.lower() for t in tags]
        jobs = [
            j for j in jobs
            if any(t in " ".join(j.get("tags", [])).lower() for t in tags_lower)
        ]
        logger.info(f"Filtered to {len(jobs)} jobs matching tags: {tags}")
    return jobs


def jobs_to_dataframe(jobs: list[dict]) -> pd.DataFrame:
    rows = []
    for j in jobs:
        rows.append({
            "id": j.get("id", ""),
            "position": j.get("position", ""),
            "company": j.get("company", ""),
            "description": j.get("description", ""),
            "tags": ",".join(j.get("tags", [])),
            "date": j.get("date", ""),
            "url": j.get("url", ""),
        })
    return pd.DataFrame(rows)


def scrape_and_save(output_path: str | Path, tags: list[str] | None = None):
    jobs = fetch_remoteok(tags=tags)
    df = jobs_to_dataframe(jobs)
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    logger.info(f"Saved {len(df)} jobs to {output_path}")
    return df


if __name__ == "__main__":
    scrape_and_save("data/raw/jobs.csv", tags=ROLE_TAGS)