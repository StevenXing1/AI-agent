from datetime import datetime

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=1000)


class ChatResponse(BaseModel):
    answer: str
    score: float
    matched_question: str


class QAItemCreate(BaseModel):
    question: str = Field(..., min_length=2, max_length=500)
    answer: str = Field(..., min_length=2, max_length=4000)
    source: str = Field(default="manual", max_length=120)


class QAItemRead(BaseModel):
    id: int
    question: str
    answer: str
    source: str
    created_at: datetime

    class Config:
        from_attributes = True
