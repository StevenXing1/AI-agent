import argparse
import os
import random
import sys
from pathlib import Path

from sentence_transformers import InputExample, SentenceTransformer, losses
from torch.utils.data import DataLoader

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from backend.config import settings
from backend.database import SessionLocal
from backend.models import QAPair


def build_pairs(qa_rows, negative_per_item: int = 1):
    examples = []
    questions = [x.question for x in qa_rows]
    answers = [x.answer for x in qa_rows]

    for i, q in enumerate(questions):
        a = answers[i]
        examples.append(InputExample(texts=[q, a], label=1.0))
        examples.append(InputExample(texts=[q, q], label=1.0))

        for _ in range(negative_per_item):
            j = random.randint(0, len(questions) - 1)
            while j == i:
                j = random.randint(0, len(questions) - 1)
            examples.append(InputExample(texts=[q, questions[j]], label=0.0))
    random.shuffle(examples)
    return examples


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--epochs", type=int, default=2)
    parser.add_argument("--batch-size", type=int, default=16)
    parser.add_argument("--negative-per-item", type=int, default=1)
    args = parser.parse_args()

    db = SessionLocal()
    qa_rows = db.query(QAPair).all()
    db.close()

    if len(qa_rows) < 10:
        print("Need at least 10 QA rows before fine-tuning.")
        return

    model = SentenceTransformer(settings.base_model)
    train_examples = build_pairs(qa_rows, negative_per_item=args.negative_per_item)
    train_dataloader = DataLoader(train_examples, shuffle=True, batch_size=args.batch_size)
    train_loss = losses.CosineSimilarityLoss(model)

    os.makedirs(os.path.dirname(settings.model_dir), exist_ok=True)
    model.fit(
        train_objectives=[(train_dataloader, train_loss)],
        epochs=args.epochs,
        warmup_steps=max(10, len(train_dataloader) // 5),
        show_progress_bar=True,
    )
    model.save(settings.model_dir)
    print(f"Fine-tuned model saved to {settings.model_dir}")


if __name__ == "__main__":
    main()
