JOB_COLUMNS = [
    "job_id",
    "title",
    "company",
    "industry",
    "location",
    "description_raw",
    "tags",
    "source",
    "date_posted",
    "scraped_at",
]

from datetime import datetime

def normalize(job, source):
    base = {col: None for col in JOB_COLUMNS}

    base["job_id"] = job.get("job_id")
    base["title"] = job.get("title")
    base["company"] = job.get("company")
    base["industry"] = job.get("industry")
    base["location"] = job.get("location")
    base["description_raw"] = job.get("description_raw")

    tags = job.get("tags")
    if isinstance(tags, list):
        base["tags"] = ", ".join(tags)
    else:
        base["tags"] = tags

    base["source"] = source
    base["date_posted"] = job.get("date_posted")
    base["scraped_at"] = datetime.utcnow().isoformat()

    return base
