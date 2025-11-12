import requests
import pandas as pd

# RemoteOK has a public JSON endpoint
url = "https://remoteok.com/api"

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0 Safari/537.36"
}

response = requests.get(url, headers=headers)
data = response.json()

# first element is metadata, skip it
jobs = data[1:]

records = []
for job in jobs:
    records.append({
        "title": job.get("position"),
        "company": job.get("company"),
        "location": job.get("location"),
        "tags": ", ".join(job.get("tags", [])),
        "date": job.get("date"),
        "url": job.get("url")
    })

df = pd.DataFrame(records)
print(df.head(10))
print(f"Total jobs scraped: {len(df)}")

df.to_csv("remoteok_jobs.csv", index=False)
print("Saved to remoteok_jobs.csv")
