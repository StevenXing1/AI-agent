import csv
from io import StringIO

from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy import func
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models import ChatLog, QAPair
from backend.schemas import QAItemCreate, QAItemRead
from backend.services.qa_service import qa_service


router = APIRouter(prefix="/api/admin", tags=["admin"])


@router.get("/qa", response_model=list[QAItemRead])
def list_qa(limit: int = 100, db: Session = Depends(get_db)):
    return db.query(QAPair).order_by(QAPair.id.desc()).limit(limit).all()


@router.post("/qa", response_model=QAItemRead)
def create_qa(item: QAItemCreate, db: Session = Depends(get_db)):
    qa = QAPair(question=item.question, answer=item.answer, source=item.source)
    db.add(qa)
    db.commit()
    db.refresh(qa)
    qa_service.refresh_knowledge_base(db)
    return qa


@router.post("/upload-csv")
async def upload_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    content = await file.read()
    text = content.decode("utf-8", errors="ignore")
    reader = csv.DictReader(StringIO(text))

    inserted = 0
    for row in reader:
        q = (row.get("question") or "").strip()
        a = (row.get("answer") or "").strip()
        src = (row.get("source") or "csv").strip()[:120]
        if not q or not a:
            continue
        db.add(QAPair(question=q[:500], answer=a[:4000], source=src or "csv"))
        inserted += 1

    db.commit()
    qa_service.refresh_knowledge_base(db)
    return {"inserted": inserted}


@router.post("/reload-model")
def reload_model(db: Session = Depends(get_db)):
    qa_service.reload_model()
    qa_service.refresh_knowledge_base(db)
    return {"message": "model and knowledge base reloaded"}


@router.get("/stats")
def stats(db: Session = Depends(get_db)):
    qa_count = db.query(func.count(QAPair.id)).scalar() or 0
    chat_count = db.query(func.count(ChatLog.id)).scalar() or 0
    return {"qa_count": qa_count, "chat_count": chat_count}
