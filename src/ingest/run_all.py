import logging
import time

from .fetch_indeed_rss import scrape_indeed_rss
from .fetch_remoteok import scrape_remoteok
from .save import save_jobs
from .noise import log_missingness

logging.basicConfig(level=logging.INFO)

def main():
    start = time.time()
    logging.info("Starting ingestion pipeline...")

    # Indeed RSS
    logging.info("Scraping Indeed RSS...")
    indeed_jobs = scrape_indeed_rss(limit=150)
    logging.info(f"Indeed RSS jobs collected: {len(indeed_jobs)}")
    log_missingness(indeed_jobs, "indeed_rss")
    save_jobs(indeed_jobs)

    # RemoteOK
    logging.info("Scraping RemoteOK...")
    remoteok_jobs = scrape_remoteok(limit=150)
    logging.info(f"RemoteOK jobs collected: {len(remoteok_jobs)}")
    log_missingness(remoteok_jobs, "remoteok")
    save_jobs(remoteok_jobs)

    # Final log
    logging.info(f"Pipeline completed in {time.time() - start:.2f}s")

if __name__ == "__main__":
    main()
