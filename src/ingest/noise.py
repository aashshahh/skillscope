import pandas as pd
from datetime import datetime
import os

NOISE_PATH = "data/raw/scraping_noise.csv"

def log_missingness(jobs, source):
    if not jobs:
        return

    df = pd.DataFrame(jobs)
    missing_counts = df.isna().sum()

    rows = []
    for col, count in missing_counts.items():
        rows.append({
            "source": source,
            "column": col,
            "missing": int(count),
            "total": len(df),
            "missing_rate": float(count) / len(df),
            "logged_at": datetime.utcnow().isoformat(),
        })

    df_log = pd.DataFrame(rows)

    if os.path.exists(NOISE_PATH):
        old = pd.read_csv(NOISE_PATH)
        df_log = pd.concat([old, df_log], ignore_index=True)

    os.makedirs("data/raw", exist_ok=True)
    df_log.to_csv(NOISE_PATH, index=False)
