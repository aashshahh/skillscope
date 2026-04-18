# SkillScope

Most job advice tells you to "build in-demand skills." Almost none of it tells you 
which ones, for which roles, at which companies, right now.

Course syllabi lag. Generic skill lists are written by people who aren't hiring. 
SkillScope skips both and reads the job postings directly.

🔗 **Live Demo:** [aashshahh.github.io/skillscope](https://aashshahh.github.io/skillscope)

---

## The Problem

You upload your resume to a job application. It goes into a black box. You hear nothing.

Part of what's happening in that black box is a skill match your resume against 
what the job description actually requires. The problem is you never see that comparison. 
You don't know which skills tipped you out of the running, which ones you already have 
that they care about, or what to go learn before the next application.

SkillScope makes that comparison visible.

Paste your resume and a job description. Within seconds you get:
- every skill the JD requires, extracted and normalized
- which of those you already have (exact matches)
- which you're close on similar concepts, different phrasing (semantic matches via 
  Sentence-BERT cosine similarity)
- what's genuinely missing, ranked by how central it is to the role

Not keyword overlap. Actual semantic distance.

---

## How It Works

### Skill Extraction

Job descriptions and resumes don't use consistent language. One posting says 
"proficiency in Postgres," another says "strong SQL background," a third lists 
"PostgreSQL" under requirements. A keyword matcher treats these as three different 
things. SkillScope normalizes them to the same canonical skill using a curated 
taxonomy mapped to the ESCO ontology, then runs spaCy's PhraseMatcher across 150+ 
skills across ten categories.

### Semantic Matching

Exact match only gets you so far. If your resume says PyTorch and the JD says 
TensorFlow, that's not a zero — it's a partial signal. SkillScope embeds every 
extracted skill using Sentence-BERT (`all-MiniLM-L6-v2`), computes a cosine 
similarity matrix between your skills and the JD's skills, and flags anything above 
a 0.65 threshold as a soft match. You see the score, the pairing, and can judge 
it yourself.

### Gap Score

The final output is a 0–100 match score: exact matches count fully, soft matches 
count proportionally by their similarity score. It's not a vibe. It's a number 
you can act on.

---

## Tech Stack

- **NLP:** spaCy, Sentence-Transformers, NLTK
- **Skill taxonomy:** ESCO v1.1 + curated `skills.json` (150+ skills, 10 categories)
- **Backend:** FastAPI, Uvicorn, Pydantic
- **Frontend:** React 18, Vite, no UI framework — custom CSS
- **Evaluation:** SkillSpan dataset (HuggingFace) — precision, recall, F1
- **Data:** RemoteOK API (live job scraping), synthetic resumes
- **CI/CD:** GitHub Actions (test + deploy)
- **Deployment:** GitHub Pages (frontend), Render (API)

---

## Getting Started

```bash
# Clone
git clone https://github.com/aashshahh/skillscope.git
cd skillscope

# Backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python -m spacy download en_core_web_sm

# Test the pipeline directly
python scripts/run_pipeline.py \
  --resume data/raw/sample_resume.txt \
  --jd data/raw/sample_jd.txt

# Start the API
uvicorn src.api.main:app --reload

# Frontend (separate terminal)
cd frontend && npm install && npm run dev
```

Open `http://localhost:5173`. The API runs at `http://localhost:8000/docs`.

---

## Project Structure
```
skillscope/
├── src/
│   ├── ingest/       # resume parser (PDF, DOCX, TXT), job scraper
│   ├── nlp/          # skill extractor, SBERT embedder, normalizer
│   ├── models/       # gap analyzer, evaluator
│   └── api/          # FastAPI routes + schemas
├── frontend/         # React + Vite
├── scripts/          # CLI pipeline runner, evaluation script
├── config/
│   ├── settings.yaml
│   └── skills.json   # skill taxonomy
├── data/raw/         # sample resume + JD for testing
└── tests/            # pytest unit tests
```

---

## Evaluation

Run against the SkillSpan benchmark dataset (HuggingFace):

```bash
python scripts/evaluate.py --n 200 --output results/eval_report.json
```

| Model | Precision | Recall | F1 |
|---|---|---|---|
| spaCy PhraseMatcher + ESCO | 0.87 | 0.84 | 0.85 |
| BERT baseline | 0.82 | 0.79 | 0.80 |

---

**Aash Shah** · [LinkedIn](https://linkedin.com/in/aash-shah-ba002224b) · 
[aashshah.04@gmail.com](mailto:aashshah.04@gmail.com)
