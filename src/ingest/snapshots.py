import hashlib
from datetime import datetime
import os

SNAPSHOT_DIR = "data/raw/snapshots"

def save_snapshot(source, content):
    os.makedirs(SNAPSHOT_DIR, exist_ok=True)
    ts = datetime.utcnow().strftime("%Y%m%dT%H%M%S")
    h = hashlib.md5(content.encode()).hexdigest()[:10]
    fname = f"{source}_{ts}_{h}.txt"

    with open(f"{SNAPSHOT_DIR}/{fname}", "w", encoding="utf-8") as f:
        f.write(content)
