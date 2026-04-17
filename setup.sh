#!/usr/bin/env bash
set -e

echo ""
echo "  SkillScope — Setup"
echo "  =========================="
echo ""

echo "  [1/4] Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

echo "  [2/4] Installing Python dependencies..."
pip install --upgrade pip -q
pip install -r requirements.txt -q

echo "  [3/4] Downloading spaCy model..."
python -m spacy download en_core_web_sm -q

echo "  [4/4] Creating data directories..."
mkdir -p data/raw data/processed results

echo ""
echo "  Setup complete."
echo ""
echo "  Run backend:  uvicorn src.api.main:app --reload"
echo "  Run frontend: cd frontend && npm install && npm run dev"
echo "  Run pipeline: python scripts/run_pipeline.py --resume data/raw/sample_resume.txt --jd data/raw/sample_jd.txt"
echo "  Run tests:    pytest tests/ -v"
echo ""