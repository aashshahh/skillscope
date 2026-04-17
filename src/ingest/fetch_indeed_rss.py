import feedparser
from datetime import datetime
import hashlib

from .schema import normalize
from .snapshots import save_snapshot

SOURCE = "indeed_rss"

RSS_DOMAINS = [
    "https://rss.indeed.com/rss",
    "https://www.indeed.com/rss",
    "https://in.indeed.com/rss",
    "https://uk.indeed.com/rss",
    "https://ca.indeed.com/rss",
    "https://au.indeed.com/rss",
]


def make_feed_urls(query="data", location=None):
    """Build multiple RSS URLs across global Indeed endpoints."""
    q = query.replace(" ", "+")
    urls = []

    for base in RSS_DOMAINS:
        if location:
            l = location.replace(" ", "+")
            urls.append(f"{base}?q={q}&l={l}")
        else:
            urls.append(f"{base}?q={q}")

    return urls


def scrape_indeed_rss(limit=150):
    """Scrapes Indeed RSS feeds and returns a list of normalized job dicts.
       Always returns a list — never None.
    """
    jobs = []
    urls = make_feed_urls(query="data", location=None)

    for url in urls:
        print("Fetching:", url)

        try:
            feed = feedparser.parse(url)
        except Exception as e:
            print(f"Failed to parse RSS feed {url}: {e}")
            continue

        # Save a snapshot to disk for debugging
        try:
            save_snapshot("indeed_rss", str(feed))
        except Exception:
            pass

        # If the feed has no entries, skip it
        if not hasattr(feed, "entries") or len(feed.entries) == 0:
            continue

        for entry in feed.entries:
            try:
                job_id = hashlib.md5(entry.link.encode()).hexdigest()[:12]
            except Exception:
                continue

            raw = {
                "job_id": job_id,
                "title": entry.get("title"),
                "company": entry.get("author"),
                "industry": None,
                "location": None,
                "description_raw": entry.get("summary", ""),
                "tags": [],
                "date_posted": entry.get("published"),
                "scraped_at": datetime.utcnow().isoformat(),
            }

            jobs.append(normalize(raw, SOURCE))

            if len(jobs) >= limit:
                return jobs

    # Guarantee: ALWAYS return a list — even if empty
    return jobs
