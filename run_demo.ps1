$ErrorActionPreference = "Stop"

Write-Host "[1/6] Create virtual environment" -ForegroundColor Cyan
python -m venv .venv

Write-Host "[2/6] Activate environment" -ForegroundColor Cyan
. .\.venv\Scripts\Activate.ps1

Write-Host "[3/6] Install dependencies" -ForegroundColor Cyan
pip install -r requirements.txt

Write-Host "[4/6] Initialize database and seed local QA" -ForegroundColor Cyan
python scripts/init_db.py
python scripts/seed_from_csv.py --file data/sample_qa.csv

Write-Host "[5/6] Optional: import online free QA data" -ForegroundColor Cyan
python scripts/import_online_qa.py --tag python --limit 30

Write-Host "[6/6] Fine-tune sentence encoder" -ForegroundColor Cyan
python scripts/fine_tune_encoder.py --epochs 1 --batch-size 8

Write-Host "Start server on http://127.0.0.1:8000" -ForegroundColor Green
uvicorn backend.main:app --reload
