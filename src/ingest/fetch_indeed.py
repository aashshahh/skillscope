from bs4 import BeautifulSoup
from datetime import datetime
import logging

from .base_scraper import get_session, safe_get
from .schema import normalize

BASE_URL = "https://www.indeed.com/jobs"
QUERY = "data scientist"
LOCATION = "Remote"
SOURCE = "indeed"

def parse_card(card):
    title_el = card.find("h2")
    title = title_el.get_text(strip=True) if title_el else None

    company_el = card.find("span", attrs={"data-testid": "company-name"})
    company = company_el.get_text(strip=True) if company_el else None

    location_el = card.find("div", attrs={"data-testid": "text-location"})
    location = location_el.get_text(strip=True) if location_el else None

    job_id = card.get("data-jk") or card.get("data-jobid")

    desc_el = card.find("div", attrs={"data-testid": "job-snippet"})
    desc = desc_el.get_text(" ", strip=True) if desc_el else None

    return {
        "job_id": job_id,
        "title": title,
        "company": company,
        "industry": None,
        "location": location,
        "description_raw": desc,
        "tags": [],
        "date_posted": None,
        "scraped_at": datetime.utcnow().isoformat()
    }

def scrape_indeed(limit=150):
    session = get_session()
    jobs = []
    start = 0

    # Warm up session with initial GET (important for cookies)
    warm = safe_get(session, "https://www.indeed.com")
    if warm is None:
        logging.error("Warm-up request failed. Indeed blocking us.")
        return []


    while len(jobs) < limit:
        params = {"q": QUERY, "l": LOCATION, "start": start}
        res = safe_get(session, BASE_URL, params=params)

        if res is None:
            break

        soup = BeautifulSoup(res.text, "html.parser")
        cards = soup.find_all("div", attrs={"data-testid": "jobCard"})

        if not cards:
            break

        for card in cards:
            raw = parse_card(card)
            if not raw["job_id"]:
                continue

            jobs.append(normalize(raw, SOURCE))

            if len(jobs) >= limit:
                break
        
        # Sleep to mimic human behavior and avoid 403 blocking
        time.sleep(random.uniform(1.5, 3.0))
        
        start += 10
        


    return jobs


