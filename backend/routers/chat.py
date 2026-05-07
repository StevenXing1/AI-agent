from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.schemas import ChatRequest, ChatResponse
from backend.services.qa_service import qa_service


router = APIRouter(prefix="/api", tags=["chat"])


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest, db: Session = Depends(get_db)):
    answer, score, matched_question = qa_service.ask(request.message, db)
    return ChatResponse(answer=answer, score=score, matched_question=matched_question)
