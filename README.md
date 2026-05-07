# AI Customer Service Platform

A fully runnable MVP AI customer service system built from scratch, featuring:

- FastAPI backend API
- SQLite database for storing Q&A pairs and chat logs
- Semantic search Q&A powered by Sentence Transformers
- Fine-tuning script for the encoder model
- Free online Q&A data import via StackExchange API
- Frontend UI with chat interface and knowledge base management

## Project Structure

- `backend/` — Backend service and database models
- `frontend/` — Chat and admin UI
- `scripts/` — Init, import, and fine-tuning scripts
- `data/sample_qa.csv` — Local demo Q&A data
- `run_demo.ps1` — One-click demo runner

## Requirements

- Python 3.10+
- Windows PowerShell
- Internet access to download models and dependencies

## One-Click Demo

Run the following from the project root:

```powershell
.\run_demo.ps1
```

The script will automatically:

1. Create a virtual environment and install dependencies
2. Initialize the SQLite database
3. Seed local Q&A sample data
4. Fetch free online Q&A data from StackExchange
5. Fine-tune the semantic encoder model
6. Start the server

Once running, open:

- Frontend UI: http://127.0.0.1:8000
- Health check: http://127.0.0.1:8000/health
- API docs: http://127.0.0.1:8000/docs

## Step-by-Step Commands

```powershell
python -m venv .venv
. .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

python scripts/init_db.py
python scripts/seed_from_csv.py --file data/sample_qa.csv
python scripts/import_online_qa.py --tag python --limit 30
python scripts/fine_tune_encoder.py --epochs 1 --batch-size 8

uvicorn backend.main:app --reload
```

## CSV Import Format

The CSV file must contain these columns:

- `question`
- `answer`
- `source` (optional)

See `data/sample_qa.csv` for an example.

## Notes

- If fine-tuning fails, the system automatically falls back to the base open-source model.
- The current Q&A strategy is semantic similarity retrieval, well-suited for FAQ and customer service knowledge bases.
- Possible extensions: user login, ticket routing, human agent handoff, RAG with document retrieval.
