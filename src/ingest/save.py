import os
import pandas as pd
from .schema import JOB_COLUMNS

RAW_PATH = "data/raw/jobs_raw.csv"

def load_existing():
    if os.path.exists(RAW_PATH):
        return pd.read_csv(RAW_PATH)
    return pd.DataFrame(columns=JOB_COLUMNS)

def save_jobs(new_jobs):
    df_old = load_existing()
    df_new = pd.DataFrame(new_jobs)

    df_all = pd.concat([df_old, df_new], ignore_index=True)
    df_all.drop_duplicates(subset=["job_id", "source"], inplace=True)

    os.makedirs("data/raw", exist_ok=True)
    df_all.to_csv(RAW_PATH, index=False)
    return df_all
