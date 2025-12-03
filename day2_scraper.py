import requests
import pandas as pd

url = "https://remoteok.com/api"
response = requests.get(url)
data = response.json()[1:]  # skip metadata

df = pd.DataFrame(data)
df.to_csv("remoteok_jobs.csv", index=False)
print("Data saved successfully! Rows:", len(df))
print(df.head(5))

import re
from bs4 import BeautifulSoup

# Step 1: Clean job descriptions (remove HTML tags, lowercase, etc.)
def clean_text(text):
    if not isinstance(text, str):
        return ""
    text = BeautifulSoup(text, "html.parser").get_text()
    return text.lower()

df["description"] = df["description"].apply(clean_text)

# Step 2: Extract common skill keywords
common_skills = [
    "python", "sql", "excel", "pandas", "numpy", "tensorflow",
    "pytorch", "aws", "azure", "git", "java", "r", "docker",
    "spark", "hadoop", "powerbi", "tableau", "ml", "nlp"
]

def extract_skills(text):
    return [skill for skill in common_skills if re.search(rf'\b{skill}\b', text)]

df["skills"] = df["description"].apply(extract_skills)

# Step 3: Save cleaned version
df[["company", "position", "location", "description", "skills"]].to_csv(
    "jobs_with_skills.csv", index=False
)

print("✅ Skill extraction complete! Saved as jobs_with_skills.csv")
print(df[["company", "skills"]].head(10))

