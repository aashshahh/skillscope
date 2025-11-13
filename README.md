# SkillScope  
### Mapping the Skills That Power Today’s Data Roles  

**Author:** Aash Shah   
**Email:** aashshah.04@gmail.com  
**GitHub:** [aashshahh](https://github.com/aashshahh)  
**LinkedIn:** [linkedin.com/in/aash-shah-ba002224b](https://linkedin.com/in/aash-shah-ba002224b)  


## Project Purpose  

SkillScope identifies and visualizes the most in demand technical skills across data driven roles such as Data Scientist, Machine Learning Engineer, and Data Analyst.  
The project captures live job listings, extracts relevant skills through NLP and parsing, and builds interpretable datasets that highlight real world hiring trends.  


## Overview  

SkillScope is a data centric analysis pipeline that starts from real job postings and ends with insights on which tools, frameworks, and languages dominate current hiring landscapes.  
It demonstrates an end-to-end data workflow, from **collection** and **cleaning** to **analysis** and **visualization** — designed to mirror how data teams extract business intelligence from open sources.  


## Motivation  

The rapid evolution of technology makes static skill lists obsolete. Employers update job requirements faster than academic programs or online courses adapt.  
SkillScope bridges this lag by using scraped job data to show which skills are actually appearing in current postings.  
The intent is to help learners, educators, and early-career professionals align their upskilling with market demand.  


## Data Pipeline  

| Stage | Description | Key Tools |
|--------|--------------|-----------|
| **1. Collection** | Scraped live postings using RemoteOK’s public API and Playwright automation. | Python, Requests, Playwright |
| **2. Cleaning** | Removed duplicates, standardized fields, normalized skill tags. | Pandas, NumPy |
| **3. Skill Extraction** | Tokenized and filtered tags to isolate individual technical skills. | NLTK, regex |
| **4. Analysis & Visualization** | Counted skill frequencies and plotted demand trends. | Matplotlib, Plotly |
| **5. Dashboard (Planned)** | Interactive web interface for exploring skill demand by category and region. | Streamlit |


## Repository Structure  
skillscope/
├── .venv/                 # Virtual environment (local use only)
├── data/
│   ├── raw/               # Original scraped job data
│   ├── interim/           # Cleaned intermediate files
│   └── processed/         # Final datasets ready for visualization
├── data_collection/       # Scraper scripts and automation logic
│   └── test_playwright.py
├── notebooks/             # Googele Colab notebooks for EDA and cleaning
│   └── 01_data_cleaning.ipynb
├── src/                   # Core modules for data parsing, TF-IDF, etc.
├── visuals/               # Generated figures and plots
├── report/                # Project reports, presentation material
├── dashboard/             # Streamlit dashboard (under development)
├── requirements.txt       # Python dependencies
├── .gitignore             # Files to exclude from Git tracking
└── README.md              # Main project documentation



---

## Setup  






