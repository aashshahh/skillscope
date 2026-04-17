import random
import time
import requests
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

USER_AGENTS = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0 Safari/537.36",
]

def get_session():
    return requests.Session()

def header():
    return {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Referer": "https://www.google.com/",
        "Upgrade-Insecure-Requests": "1",
        "DNT": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
    }

def safe_get(session, url, params=None, max_retries=3, backoff=1.3):
    for attempt in range(max_retries):
        try:
            res = session.get(url, params=params, headers=header(), timeout=15)
            if res.status_code == 200:
                return res
            logging.warning(f"Non-200 {res.status_code} for {url}")
        except Exception as e:
            logging.warning(f"Request failed: {e}")

        wait = backoff ** (attempt + 1)
        logging.info(f"Retrying in {wait:.1f}s...")
        time.sleep(wait)

    logging.error(f"Failed to fetch {url}")
    return None
