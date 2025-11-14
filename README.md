# SkillScope  
### Mapping the Skills That Power Modern Data Roles  

**Author:** Aash Shah   
**Email:** aashshah.04@gmail.com  
**GitHub:** [aashshahh](https://github.com/aashshahh)  
**LinkedIn:** [linkedin.com/in/aash-shah-ba002224b](https://linkedin.com/in/aash-shah-ba002224b)  


## Project Purpose  

SkillScope analyzes live job postings to uncover which technical skills matter most across data focused roles such as Data Scientist, Machine Learning Engineer, Data Analyst, and related positions.
The project collects realtime listings, extracts relevant skills using NLP, and builds interpretable datasets that reflect actual hiring patterns rather than static or outdated assumptions. 


## Overview  

SkillScope is an end to end data analysis pipeline that starts with raw job postings and ends with clear insight into the tools, frameworks, and languages companies are asking for today.
The workflow mirrors how real analytics teams operate: acquire data, clean it, extract meaningful signals, and present insights that support decision making. 


## Motivation  

Technology evolves fast. Course syllabi and generic skill lists usually lag behind what employers expect right now.
SkillScope addresses that gap by grounding its insights in freshly scraped job data. The goal is simple: help learners, educators, and early-career professionals invest their time in the skills that are actually showing up in current job descriptions.


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
├── .venv/                 # Local virtual environment
├── data/
│   ├── raw/               # Original scraped job data
│   ├── interim/           # Cleaned intermediate datasets
│   └── processed/         # Final datasets ready for analysis
├── data_collection/       # Scrapers and automation logic
│   └── test_playwright.py
├── notebooks/             # EDA, cleaning, and transformation notebooks
│   └── 01_data_cleaning.ipynb
├── src/                   # Core modules for parsing, TF-IDF, etc.
├── visuals/               # Generated figures and plots
├── report/                # Project reports and presentation material
├── dashboard/             # Streamlit app (under development)
├── requirements.txt       # Python dependencies
├── .gitignore
└── README.md


## Setup  
Clone the repository and install dependencies:
git clone https://github.com/aashshahh/skillscope.git
cd skillscope
pip install -r requirements.txt
Run the scraper:
python data_collection/test_playwright.py
Open the analysis notebooks:
jupyter notebook notebooks/





