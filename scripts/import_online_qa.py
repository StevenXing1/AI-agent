import argparse
import html
import re
import sys
from pathlib import Path
from typing import Dict

import requests

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from backend.database import SessionLocal
from backend.models import QAPair


def clean_html(raw_text: str) -> str:
    text = re.sub(r"<[^>]+>", " ", raw_text or "")
    text = html.unescape(text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def fetch_stackoverflow_pairs(tag: str, pagesize: int) -> list[Dict[str, str]]:
    q_url = (
        "https://api.stackexchange.com/2.3/questions"
        f"?order=desc&sort=votes&tagged={tag}&site=stackoverflow"
        f"&pagesize={pagesize}&filter=withbody"
    )
    questions_data = requests.get(q_url, timeout=20).json()
    questions = questions_data.get("items", [])

    accepted_ids = [str(q.get("accepted_answer_id")) for q in questions if q.get("accepted_answer_id")]
    if not accepted_ids:
        return []

    a_url = (
        "https://api.stackexchange.com/2.3/answers/"
        + ";".join(accepted_ids)
        + "?order=desc&sort=votes&site=stackoverflow&filter=withbody"
    )
    answers_data = requests.get(a_url, timeout=20).json()
    answers = {str(a["answer_id"]): clean_html(a.get("body", "")) for a in answers_data.get("items", [])}

    pairs = []
    for q in questions:
        aid = str(q.get("accepted_answer_id", ""))
        ans = answers.get(aid, "")
        question = clean_html(q.get("title", ""))
        if question and ans:
            pairs.append(
                {
                    "question": question[:500],
                    "answer": ans[:4000],
                    "source": f"stackoverflow:{tag}",
                }
            )
    return pairs


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--tag", default="python", help="StackOverflow tag")
    parser.add_argument("--limit", type=int, default=40, help="max question count")
    args = parser.parse_args()

    pairs = fetch_stackoverflow_pairs(tag=args.tag, pagesize=min(args.limit, 100))
    if not pairs:
        print("No pairs fetched. Try another tag.")
        return

    db = SessionLocal()
    inserted = 0
    try:
        for item in pairs:
            exists = (
                db.query(QAPair)
                .filter(QAPair.question == item["question"], QAPair.source == item["source"])
                .first()
            )
            if exists:
                continue
            db.add(QAPair(**item))
            inserted += 1
        db.commit()
    finally:
        db.close()

    print(f"Imported {inserted} QA pairs from online source.")


if __name__ == "__main__":
    main()
