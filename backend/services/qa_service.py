import threading
from typing import Optional

import numpy as np
from sentence_transformers import SentenceTransformer, util
from sqlalchemy.orm import Session

from backend.config import settings
from backend.models import ChatLog, QAPair


class QAService:
    def __init__(self):
        self._lock = threading.Lock()
        self.model = None
        self.questions = []
        self.answers = []
        self.embeddings = None
        self.reload_model()

    def reload_model(self):
        with self._lock:
            try:
                self.model = SentenceTransformer(settings.model_dir)
                print(f"Loaded fine-tuned model from {settings.model_dir}")
            except Exception:
                self.model = SentenceTransformer(settings.base_model)
                print(f"Loaded base model {settings.base_model}")

    def refresh_knowledge_base(self, db: Session):
        with self._lock:
            qa_items = db.query(QAPair).order_by(QAPair.id.asc()).all()
            self.questions = [item.question for item in qa_items]
            self.answers = [item.answer for item in qa_items]
            if self.questions:
                self.embeddings = self.model.encode(
                    self.questions,
                    convert_to_tensor=True,
                    normalize_embeddings=True,
                )
            else:
                self.embeddings = None

    def ask(self, message: str, db: Session) -> tuple[str, float, str]:
        if self.embeddings is None or not self.questions:
            fallback = "知识库为空，请先导入问答数据后再试。"
            self._save_chat_log(db, message, fallback, "", 0.0)
            return fallback, 0.0, ""

        query_embedding = self.model.encode(
            message,
            convert_to_tensor=True,
            normalize_embeddings=True,
        )
        scores = util.cos_sim(query_embedding, self.embeddings)[0]
        best_idx = int(np.argmax(scores.cpu().numpy()))
        best_score = float(scores[best_idx])

        if best_score < settings.similarity_threshold:
            reply = "我还不太确定这个问题，建议联系人工客服以获得更准确的帮助。"
            matched_question = ""
        else:
            reply = self.answers[best_idx]
            matched_question = self.questions[best_idx]

        self._save_chat_log(db, message, reply, matched_question, best_score)
        return reply, best_score, matched_question

    @staticmethod
    def _save_chat_log(
        db: Session,
        user_message: str,
        bot_reply: str,
        matched_question: str,
        matched_score: float,
    ):
        log = ChatLog(
            user_message=user_message,
            bot_reply=bot_reply,
            matched_question=matched_question,
            matched_score=matched_score,
        )
        db.add(log)
        db.commit()


qa_service = QAService()
