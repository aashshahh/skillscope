import requests
from datetime import datetime
from .schema import normalize
from .snapshots import save_snapshot

SOURCE = "remoteok"
API_URL = "https://remoteok.com/api"

def scrape_remoteok(limit=150):
    try:
        res = requests.get(API_URL, timeout=10)
        data = res.json()
        save_snapshot("remoteok", res.text)  # snapshot AFTER fetch
    except Exception as e:
        print(f"RemoteOK fetch failed: {e}")
        return []

    jobs = []

    # RemoteOK includes metadata at index 0
    for item in data[1:limit+1]:
        raw = {
            "job_id": str(item.get("id")),
            "title": item.get("position"),
            "company": item.get("company"),
            "industry": None,
            "location": item.get("location") or "Remote",
            "description_raw": item.get("description"),
            "tags": item.get("tags", []),
            "date_posted": item.get("date") or item.get("created_at"),
            "scraped_at": datetime.utcnow().isoformat(),
        }

        jobs.append(normalize(raw, SOURCE))

    return jobs
