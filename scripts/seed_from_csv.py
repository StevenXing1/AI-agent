import argparse
import csv
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from backend.database import SessionLocal
from backend.models import QAPair


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", default="data/sample_qa.csv", help="CSV path")
    args = parser.parse_args()

    inserted = 0
    db = SessionLocal()
    try:
        with open(args.file, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                q = (row.get("question") or "").strip()
                a = (row.get("answer") or "").strip()
                src = (row.get("source") or "seed").strip()[:120]
                if not q or not a:
                    continue
                exists = db.query(QAPair).filter(QAPair.question == q).first()
                if exists:
                    continue
                db.add(QAPair(question=q[:500], answer=a[:4000], source=src or "seed"))
                inserted += 1
        db.commit()
    finally:
        db.close()

    print(f"Inserted {inserted} rows from {args.file}")


if __name__ == "__main__":
    main()
